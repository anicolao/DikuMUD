/* ************************************************************************
*  Zone Layout Validator                                                  *
*                                                                          *
*  This tool validates the spatial consistency of zone layouts by:        *
*  1. Walking all rooms in a zone using breadth-first search (BFS)        *
*  2. Assigning (x, y, z) coordinates based on exit directions            *
*  3. Detecting rooms with inconsistent coordinates (same room reached    *
*     via different paths that would assign different coordinates)        *
*  4. Detecting rooms that overlap (different rooms at same coordinates)  *
*                                                                          *
*  Usage: ./zone_layout_validator [zone_index]                            *
*         (omit zone_index to validate all zones)                         *
*                                                                          *
*  See doc/zone_layout_validator.doc for more information                 *
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

/* Coordinate structure for rooms */
struct room_coordinate {
	int x;
	int y;
	int z;
	int visited;
	int room_vnum;  /* virtual number */
};

/* Queue structure for BFS */
struct queue_node {
	int room_index;  /* real room index */
	struct queue_node *next;
};

struct queue {
	struct queue_node *head;
	struct queue_node *tail;
};

/* Direction vectors for N, E, S, W, U, D */
int dx[] = { 0,  1,  0, -1,  0,  0};  /* NORTH, EAST, SOUTH, WEST, UP, DOWN */
int dy[] = { 1,  0, -1,  0,  0,  0};
int dz[] = { 0,  0,  0,  0,  1, -1};

/* Opposite directions */
int opposite_dir[] = {SOUTH, WEST, NORTH, EAST, DOWN, UP};

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

void enqueue(struct queue *q, int room_index)
{
	struct queue_node *node;
	
	CREATE(node, struct queue_node, 1);
	node->room_index = room_index;
	node->next = NULL;
	
	if (q->tail == NULL) {
		q->head = node;
		q->tail = node;
	} else {
		q->tail->next = node;
		q->tail = node;
	}
}

int dequeue(struct queue *q)
{
	struct queue_node *node;
	int room_index;
	
	if (q->head == NULL)
		return -1;
	
	node = q->head;
	room_index = node->room_index;
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

/* Check if two coordinates are equal */
int coords_equal(struct room_coordinate *a, struct room_coordinate *b)
{
	return (a->x == b->x && a->y == b->y && a->z == b->z);
}

/* Validate zone layout using BFS */
int validate_zone_layout(int zone_num)
{
	struct room_coordinate *coords;
	struct queue q;
	int start_room = -1;
	int room, dir, target_room;
	int errors = 0;
	int warnings = 0;
	int rooms_in_zone = 0;
	int x, y, z;
	int i;
	
	/* Allocate coordinate array */
	CREATE(coords, struct room_coordinate, top_of_world + 1);
	
	/* Initialize coordinates */
	for (room = 0; room <= top_of_world; room++) {
		coords[room].visited = 0;
		coords[room].x = 0;
		coords[room].y = 0;
		coords[room].z = 0;
		coords[room].room_vnum = world[room].number;
	}
	
	/* Find first room in zone and count total rooms */
	for (room = 0; room <= top_of_world; room++) {
		if (world[room].zone == zone_num) {
			if (start_room == -1) {
				start_room = room;
			}
			rooms_in_zone++;
		}
	}
	
	if (start_room == -1) {
		printf("No rooms found in zone %d\n", zone_num);
		free(coords);
		return 0;
	}
	
	printf("\n=== Zone %d Layout Validation ===\n", zone_num);
	printf("Starting from room %d (vnum %d)\n", start_room, world[start_room].number);
	printf("Total rooms in zone: %d\n\n", rooms_in_zone);
	
	/* BFS to assign coordinates */
	init_queue(&q);
	enqueue(&q, start_room);
	coords[start_room].visited = 1;
	coords[start_room].x = 0;
	coords[start_room].y = 0;
	coords[start_room].z = 0;
	
	while (!is_queue_empty(&q)) {
		room = dequeue(&q);
		
		/* Check all directions */
		for (dir = 0; dir < 6; dir++) {
			if (world[room].dir_option[dir] == NULL)
				continue;
			
			/* Note: to_room is already a real room index after boot_db, not a virtual number */
			target_room = world[room].dir_option[dir]->to_room;
			
			if (target_room < 0 || target_room > top_of_world)
				continue;
			
			/* Only process rooms in the same zone */
			if (world[target_room].zone != zone_num)
				continue;
			
			/* Calculate what the coordinates should be */
			x = coords[room].x + dx[dir];
			y = coords[room].y + dy[dir];
			z = coords[room].z + dz[dir];
			
			if (!coords[target_room].visited) {
				/* First time visiting this room */
				coords[target_room].visited = 1;
				coords[target_room].x = x;
				coords[target_room].y = y;
				coords[target_room].z = z;
				enqueue(&q, target_room);
			} else {
				/* Already visited - check if coordinates match */
				if (coords[target_room].x != x ||
				    coords[target_room].y != y ||
				    coords[target_room].z != z) {
					printf("ERROR: Room %d (vnum %d) has inconsistent coordinates!\n",
					       target_room, world[target_room].number);
					printf("       From room %d (vnum %d) going %s: would be (%d,%d,%d)\n",
					       room, world[room].number,
					       dir == NORTH ? "north" :
					       dir == EAST ? "east" :
					       dir == SOUTH ? "south" :
					       dir == WEST ? "west" :
					       dir == UP ? "up" : "down",
					       x, y, z);
					printf("       But already assigned: (%d,%d,%d)\n",
					       coords[target_room].x,
					       coords[target_room].y,
					       coords[target_room].z);
					errors++;
				}
			}
		}
	}
	
	/* Check for rooms at the same coordinates */
	for (room = 0; room <= top_of_world; room++) {
		if (world[room].zone != zone_num || !coords[room].visited)
			continue;
		
		for (i = room + 1; i <= top_of_world; i++) {
			if (world[i].zone != zone_num || !coords[i].visited)
				continue;
			
			if (coords_equal(&coords[room], &coords[i])) {
				printf("ERROR: Rooms %d (vnum %d) and %d (vnum %d) overlap at coordinates (%d,%d,%d)!\n",
				       room, world[room].number,
				       i, world[i].number,
				       coords[room].x, coords[room].y, coords[room].z);
				errors++;
			}
		}
	}
	
	/* Check for unreachable rooms in zone */
	for (room = 0; room <= top_of_world; room++) {
		if (world[room].zone == zone_num && !coords[room].visited) {
			printf("WARNING: Room %d (vnum %d) is unreachable from start room!\n",
			       room, world[room].number);
			warnings++;
		}
	}
	
	free(coords);
	
	printf("\n=== Summary ===\n");
	printf("Errors: %d\n", errors);
	printf("Warnings: %d\n", warnings);
	
	return errors;
}

int main(int argc, char **argv)
{
	int zone_num = -1;
	int total_errors = 0;
	int zone;
	
	printf("DikuMUD Zone Layout Validator\n\n");
	
	if (argc > 1) {
		zone_num = atoi(argv[1]);
		printf("Validating zone %d\n", zone_num);
	} else {
		printf("Validating all zones\n");
	}
	
	/* Change to lib directory where world files are located */
	if (chdir("lib") < 0) {
		perror("chdir to lib");
		exit(1);
	}
	
	boot_db();
	
	if (zone_num >= 0) {
		/* Validate single zone */
		total_errors = validate_zone_layout(zone_num);
	} else {
		/* Validate all zones */
		/* Find all unique zones */
		for (zone = 0; zone <= top_of_world; zone++) {
			int z = world[zone].zone;
			int already_checked = 0;
			int i;
			
			/* Check if we already validated this zone */
			for (i = 0; i < zone; i++) {
				if (world[i].zone == z) {
					already_checked = 1;
					break;
				}
			}
			
			if (!already_checked) {
				total_errors += validate_zone_layout(z);
			}
		}
	}
	
	printf("\n=== Overall Summary ===\n");
	printf("Total errors across all zones: %d\n", total_errors);
	
	if (total_errors > 0) {
		printf("\nValidation FAILED - please fix errors above.\n");
		return 1;
	} else {
		printf("\nAll zones validated successfully!\n");
		return 0;
	}
}
