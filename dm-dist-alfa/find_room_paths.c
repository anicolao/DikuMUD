/* ************************************************************************
*  Room Path Finder                                                       *
*                                                                          *
*  This tool finds paths to multiple rooms from a starting room using     *
*  breadth-first search. It's useful for understanding how overlapping    *
*  rooms are reached in the zone layout.                                  *
*                                                                          *
*  Usage: ./find_room_paths <zone_index> <room_vnum1> [<room_vnum2> ...]  *
*                                                                          *
************************************************************************* */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#include "structs.h"
#include "db.h"
#include "utils.h"

extern struct room_data *world;
extern int top_of_world;

/* Path structure to track how we reached a room */
struct path_node {
	int room_index;
	int from_room;     /* room we came from (-1 for start) */
	int direction;     /* direction we took to get here */
	struct path_node *next;
};

/* Queue structure for BFS */
struct queue_node {
	int room_index;
	struct path_node *path;  /* path taken to reach this room */
	struct queue_node *next;
};

struct queue {
	struct queue_node *head;
	struct queue_node *tail;
};

void boot_db();
int real_room(int virtual);

/* Stub functions for missing dependencies */
void *descriptor_list = NULL;
void *combat_list = NULL;
int find_name(char *name) { return -1; }
void set_title(struct char_data *ch) {}
int mana_limit(struct char_data *ch) { return 0; }
int hit_limit(struct char_data *ch) { return 0; }
int move_limit(struct char_data *ch) { return 0; }
void build_help_index() {}
void load_messages() {}
void boot_social_messages() {}
void boot_pose_messages() {}
void no_specials(struct char_data *ch, int cmd, char *arg) {}
void assign_command_pointers() {}
void assign_spell_pointers() {}
void boot_quests() {}
void assign_quest_givers() {}
void update_obj_file() {}
void assign_mobiles() {}
void assign_objects() {}
void assign_rooms() {}
void act(char *str, int hide_invisible, struct char_data *ch,
         struct obj_data *obj, void *vict_obj, int type) {}
void die_follower(struct char_data *ch) {}
void send_to_char(char *messg, struct char_data *ch) {}
void stop_fighting(struct char_data *ch) {}
void do_return(struct char_data *ch, char *argument, int cmd) {}
void write_to_q(char *txt, struct txt_q *queue) {}
int search_block(char *arg, char **list, bool exact) { return -1; }

/* Queue operations */
void init_queue(struct queue *q)
{
	q->head = NULL;
	q->tail = NULL;
}

void enqueue(struct queue *q, int room_index, struct path_node *path)
{
	struct queue_node *node;
	
	CREATE(node, struct queue_node, 1);
	node->room_index = room_index;
	node->path = path;
	node->next = NULL;
	
	if (q->tail == NULL) {
		q->head = node;
		q->tail = node;
	} else {
		q->tail->next = node;
		q->tail = node;
	}
}

int dequeue(struct queue *q, struct path_node **path)
{
	struct queue_node *node;
	int room_index;
	
	if (q->head == NULL)
		return -1;
	
	node = q->head;
	room_index = node->room_index;
	*path = node->path;
	q->head = node->next;
	
	if (q->head == NULL)
		q->tail = NULL;
	
	free(node);
	return room_index;
}

int is_queue_empty(struct queue *q)
{
	return q->head == NULL;
}

/* Create a new path node */
struct path_node *create_path_node(int room, int from, int dir, struct path_node *prev)
{
	struct path_node *node;
	CREATE(node, struct path_node, 1);
	node->room_index = room;
	node->from_room = from;
	node->direction = dir;
	node->next = NULL;
	
	/* Link to previous path if provided */
	if (prev != NULL) {
		/* Find the end of the previous path and append */
		struct path_node *tail = prev;
		while (tail->next != NULL) {
			tail = tail->next;
		}
		tail->next = node;
		return prev;  /* Return head of path */
	}
	
	return node;
}

/* Copy a path */
struct path_node *copy_path(struct path_node *path)
{
	struct path_node *new_head = NULL;
	struct path_node *new_tail = NULL;
	struct path_node *current = path;
	
	while (current != NULL) {
		struct path_node *new_node;
		CREATE(new_node, struct path_node, 1);
		new_node->room_index = current->room_index;
		new_node->from_room = current->from_room;
		new_node->direction = current->direction;
		new_node->next = NULL;
		
		if (new_head == NULL) {
			new_head = new_node;
			new_tail = new_node;
		} else {
			new_tail->next = new_node;
			new_tail = new_node;
		}
		
		current = current->next;
	}
	
	return new_head;
}

/* Print a path */
void print_path(struct path_node *path, int target_vnum)
{
	struct path_node *node = path;
	int step = 0;
	
	printf("\nPath to room %d:\n", target_vnum);
	
	if (node == NULL) {
		printf("  (start room)\n");
		return;
	}
	
	while (node != NULL) {
		if (node->from_room == -1) {
			printf("  Start: Room %d (vnum %d)\n", 
			       node->room_index, world[node->room_index].number);
		} else {
			const char *dir_name;
			switch (node->direction) {
				case NORTH: dir_name = "north"; break;
				case EAST: dir_name = "east"; break;
				case SOUTH: dir_name = "south"; break;
				case WEST: dir_name = "west"; break;
				case UP: dir_name = "up"; break;
				case DOWN: dir_name = "down"; break;
				default: dir_name = "unknown"; break;
			}
			printf("  Step %d: From room %d (vnum %d) go %s to room %d (vnum %d)\n",
			       ++step,
			       node->from_room, world[node->from_room].number,
			       dir_name,
			       node->room_index, world[node->room_index].number);
		}
		node = node->next;
	}
}

/* Free path memory */
void free_path(struct path_node *path)
{
	struct path_node *node = path;
	struct path_node *next;
	
	while (node != NULL) {
		next = node->next;
		free(node);
		node = next;
	}
}

/* Find paths to target rooms using BFS */
void find_paths(int zone_num, int *target_vnums, int num_targets)
{
	struct queue q;
	int *visited;
	int *found;
	int start_room = -1;
	int room, dir, target_room;
	struct path_node *path;
	int i;
	int found_count = 0;
	
	/* Allocate visited array */
	CREATE(visited, int, top_of_world + 1);
	CREATE(found, int, num_targets);
	
	/* Initialize visited flags and found flags */
	for (room = 0; room <= top_of_world; room++) {
		visited[room] = 0;
	}
	for (i = 0; i < num_targets; i++) {
		found[i] = 0;
	}
	
	/* Find first room in zone as start room */
	for (room = 0; room <= top_of_world; room++) {
		if (world[room].zone == zone_num) {
			start_room = room;
			break;
		}
	}
	
	if (start_room == -1) {
		printf("No rooms found in zone %d\n", zone_num);
		free(visited);
		free(found);
		return;
	}
	
	printf("\n=== Finding Paths in Zone %d ===\n", zone_num);
	printf("Starting from room %d (vnum %d)\n", start_room, world[start_room].number);
	printf("Looking for %d target rooms\n", num_targets);
	
	/* BFS to find paths */
	init_queue(&q);
	path = create_path_node(start_room, -1, -1, NULL);
	enqueue(&q, start_room, path);
	visited[start_room] = 1;
	
	while (!is_queue_empty(&q)) {
		room = dequeue(&q, &path);
		
		/* Check if this is one of our target rooms */
		for (i = 0; i < num_targets; i++) {
			if (world[room].number == target_vnums[i] && !found[i]) {
				found[i] = 1;
				found_count++;
				print_path(path, target_vnums[i]);
				
				if (found_count == num_targets) {
					/* Found all targets, can stop */
					free_path(path);
					free(visited);
					free(found);
					return;
				}
			}
		}
		
		/* Explore neighbors */
		for (dir = 0; dir < 6; dir++) {
			if (world[room].dir_option[dir] == NULL)
				continue;
			
			target_room = world[room].dir_option[dir]->to_room;
			
			if (target_room < 0 || target_room > top_of_world)
				continue;
			
			/* Only process rooms in the same zone */
			if (world[target_room].zone != zone_num)
				continue;
			
			if (!visited[target_room]) {
				visited[target_room] = 1;
				/* Create new path by copying current path and adding this step */
				struct path_node *new_path = copy_path(path);
				new_path = create_path_node(target_room, room, dir, new_path);
				enqueue(&q, target_room, new_path);
			}
		}
		
		free_path(path);
	}
	
	/* Report any rooms that weren't found */
	for (i = 0; i < num_targets; i++) {
		if (!found[i]) {
			printf("\nWARNING: Room vnum %d was not found in zone %d\n", 
			       target_vnums[i], zone_num);
		}
	}
	
	free(visited);
	free(found);
}

int main(int argc, char **argv)
{
	int zone_num;
	int *target_vnums;
	int num_targets;
	int i;
	
	if (argc < 3) {
		printf("Usage: %s <zone_index> <room_vnum1> [<room_vnum2> ...]\n", argv[0]);
		printf("  zone_index: The zone table index (0-based)\n");
		printf("  room_vnums: Virtual room numbers to find paths to\n");
		return 1;
	}
	
	zone_num = atoi(argv[1]);
	num_targets = argc - 2;
	
	CREATE(target_vnums, int, num_targets);
	for (i = 0; i < num_targets; i++) {
		target_vnums[i] = atoi(argv[2 + i]);
	}
	
	/* Change to lib directory where world files are located */
	if (chdir("lib") < 0) {
		perror("chdir to lib");
		exit(1);
	}
	
	boot_db();
	
	find_paths(zone_num, target_vnums, num_targets);
	
	free(target_vnums);
	
	return 0;
}
