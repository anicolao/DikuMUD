/* ************************************************************************
*  file: obj_spec_procs.c, Object special procedures.     Part of DIKUMUD *
*  Usage: YAML-based object special procedure system                      *
************************************************************************* */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "structs.h"
#include "utils.h"
#include "comm.h"
#include "db.h"
#include "handler.h"
#include "interpreter.h"
#include "quest.h"
#include "obj_spec_procs.h"

/* External functions */
extern struct room_data *world;
extern struct char_data *character_list;
extern void gain_exp(struct char_data *ch, int gain);
extern void act(char *str, int hide_invisible, struct char_data *ch,
                struct obj_data *obj, void *vict_obj, int type);

/* Global array to store special procedure data */
static struct obj_spec_proc_data *spec_proc_table = NULL;
static int spec_proc_count = 0;
static int spec_proc_capacity = 0;

/* Initialize the special procedure system */
void init_obj_spec_procs(void)
{
    FILE *fl;
    char line[MAX_STRING_LENGTH];
    char buf[MAX_STRING_LENGTH];
    int vnum, target_room, xp_reward, discovery_bit, consume_item;
    char spec_type_str[256];
    char keywords[MAX_STRING_LENGTH];
    struct obj_spec_proc_data *spec;
    extern void slog(char *str);
    
    /* Initial capacity for spec proc table */
    spec_proc_capacity = 10;
    CREATE(spec_proc_table, struct obj_spec_proc_data, spec_proc_capacity);
    spec_proc_count = 0;
    
    /* Open the specials file */
    if (!(fl = fopen("tinyworld.specials", "r"))) {
        slog("   No tinyworld.specials file - no object special procedures loaded");
        return;
    }
    
    /* Read special procedures from file */
    while (fgets(line, sizeof(line), fl)) {
        /* Skip blank lines and comments */
        if (line[0] == '\n' || line[0] == '*')
            continue;
        
        /* Check for EOF marker */
        if (line[0] == '$')
            break;
        
        /* Read vnum line */
        if (line[0] == '#') {
            vnum = atoi(line + 1);
            
            /* Read spec type, target room, xp, discovery bit, consume flag, reward items */
            if (!fgets(line, sizeof(line), fl))
                break;
            int reward_item1 = 0, reward_item2 = 0;
            int scanned = sscanf(line, "%s %d %d %d %d %d %d", spec_type_str, &target_room, &xp_reward, &discovery_bit, &consume_item, &reward_item1, &reward_item2);
            /* If old format (5 fields), reward items default to 0 */
            if (scanned < 6) {
                reward_item1 = 0;
                reward_item2 = 0;
            }
            
            /* Read target keywords line */
            if (!fgets(keywords, sizeof(keywords), fl))
                break;
            keywords[strcspn(keywords, "\n")] = '\0';  /* Remove newline */
            
            /* Expand table if needed */
            if (spec_proc_count >= spec_proc_capacity) {
                spec_proc_capacity *= 2;
                RECREATE(spec_proc_table, struct obj_spec_proc_data, spec_proc_capacity);
            }
            
            /* Add new spec */
            spec = &spec_proc_table[spec_proc_count++];
            spec->target_room = target_room;
            spec->xp_reward = xp_reward;
            spec->discovery_bit = discovery_bit;
            spec->consume_item = consume_item;
            spec->reward_item1 = reward_item1;
            spec->reward_item2 = reward_item2;
            
            /* Determine spec type from string */
            if (strcmp(spec_type_str, "use_target") == 0) {
                spec->spec_type = SPEC_PROC_USE_TARGET;
            } else {
                slog("Unknown special procedure type in tinyworld.specials");
                spec_proc_count--;
                continue;
            }
            
            /* Store target keywords */
            CREATE(spec->target_keywords, char, strlen(keywords) + 1);
            strcpy(spec->target_keywords, keywords);
            
            /* Read success message (tilde-terminated) */
            CREATE(spec->success_msg, char, MAX_SPEC_MSG_LEN);
            if (!fgets(buf, sizeof(buf), fl)) break;
            buf[strcspn(buf, "~")] = '\0';  /* Remove tilde */
            strncpy(spec->success_msg, buf, MAX_SPEC_MSG_LEN - 1);
            
            /* Read fail message (tilde-terminated) */
            CREATE(spec->fail_msg, char, MAX_SPEC_MSG_LEN);
            if (!fgets(buf, sizeof(buf), fl)) break;
            buf[strcspn(buf, "~")] = '\0';  /* Remove tilde */
            strncpy(spec->fail_msg, buf, MAX_SPEC_MSG_LEN - 1);
            
            /* Read room message (tilde-terminated) */
            CREATE(spec->room_msg, char, MAX_SPEC_MSG_LEN);
            if (!fgets(buf, sizeof(buf), fl)) break;
            buf[strcspn(buf, "~")] = '\0';  /* Remove tilde */
            strncpy(spec->room_msg, buf, MAX_SPEC_MSG_LEN - 1);
            
            /* Store vnum mapping */
            spec->obj_vnum = vnum;
        }
    }
    
    fclose(fl);
    
    snprintf(buf, sizeof(buf), "   Loaded %d object special procedures", spec_proc_count);
    slog(buf);
}

/* Free special procedure data */
void free_obj_spec_procs(void)
{
    int i;
    
    if (spec_proc_table) {
        for (i = 0; i < spec_proc_count; i++) {
            if (spec_proc_table[i].target_keywords) free(spec_proc_table[i].target_keywords);
            if (spec_proc_table[i].success_msg) free(spec_proc_table[i].success_msg);
            if (spec_proc_table[i].fail_msg) free(spec_proc_table[i].fail_msg);
            if (spec_proc_table[i].room_msg) free(spec_proc_table[i].room_msg);
        }
        free(spec_proc_table);
        spec_proc_table = NULL;
    }
    spec_proc_count = 0;
    spec_proc_capacity = 0;
}

/* Get special procedure data for an object */
struct obj_spec_proc_data *get_obj_spec_proc(int obj_vnum)
{
    int i;
    
    /* Search for special procedure matching the object vnum */
    for (i = 0; i < spec_proc_count; i++) {
        if (spec_proc_table[i].obj_vnum == obj_vnum) {
            return &spec_proc_table[i];
        }
    }
    
    return NULL;
}

/* Grant discovery reward to character and their group */
void grant_discovery_reward(struct char_data *ch, struct obj_spec_proc_data *spec_data)
{
    struct char_data *k;
    struct follow_type *f;
    char buf[MAX_STRING_LENGTH];
    int already_discovered = 0;
    
    /* Check if this character already discovered this */
    if (is_quest_completed(ch, spec_data->discovery_bit)) {
        already_discovered = 1;
    }
    
    /* If this is a first discovery, grant reward */
    if (!already_discovered && spec_data->xp_reward > 0) {
        /* Reward the character */
        gain_exp(ch, spec_data->xp_reward);
        snprintf(buf, sizeof(buf), "You gain %d experience for this discovery!\r\n", 
                spec_data->xp_reward);
        send_to_char(buf, ch);
        set_quest_completed(ch, spec_data->discovery_bit);
        
        /* If in a group, reward all group members in the same room */
        if (ch->master) {
            /* Character is a follower */
            k = ch->master;
        } else {
            /* Character is the leader */
            k = ch;
        }
        
        /* Reward the leader if in same room and haven't discovered */
        if (k != ch && k->in_room == ch->in_room && !IS_NPC(k)) {
            if (!is_quest_completed(k, spec_data->discovery_bit)) {
                gain_exp(k, spec_data->xp_reward);
                snprintf(buf, sizeof(buf), 
                        "You gain %d experience for this discovery!\r\n",
                        spec_data->xp_reward);
                send_to_char(buf, k);
                set_quest_completed(k, spec_data->discovery_bit);
            }
        }
        
        /* Reward followers in same room who haven't discovered */
        for (f = k->followers; f; f = f->next) {
            if (f->follower != ch && f->follower->in_room == ch->in_room && 
                !IS_NPC(f->follower)) {
                if (!is_quest_completed(f->follower, spec_data->discovery_bit)) {
                    gain_exp(f->follower, spec_data->xp_reward);
                    snprintf(buf, sizeof(buf),
                            "You gain %d experience for this discovery!\r\n",
                            spec_data->xp_reward);
                    send_to_char(buf, f->follower);
                    set_quest_completed(f->follower, spec_data->discovery_bit);
                }
            }
        }
    }
}

/* Execute object special procedure */
int execute_obj_spec_proc(struct char_data *ch, struct obj_data *obj, 
                          char *argument, int cmd)
{
    struct obj_spec_proc_data *spec_data;
    int result = 0;
    int obj_vnum;
    extern struct index_data *obj_index;
    
    /* Only handle USE command */
    if (cmd != CMD_USE)
        return 0;
    
    /* Get virtual number from object */
    if (obj->item_number >= 0 && obj->item_number < 99999) {
        obj_vnum = obj_index[obj->item_number].virtual;
    } else {
        return 0;
    }
    
    /* Get special procedure data for this object */
    spec_data = get_obj_spec_proc(obj_vnum);
    if (!spec_data)
        return 0;
    
    /* Execute the appropriate handler based on spec type */
    switch (spec_data->spec_type) {
        case SPEC_PROC_USE_TARGET:
            result = spec_proc_use_target(ch, obj, spec_data, argument);
            break;
        default:
            return 0;
    }
    
    return result;
}

/* Generic handler for use_target procedure - completely data-driven */
int spec_proc_use_target(struct char_data *ch, struct obj_data *obj,
                         struct obj_spec_proc_data *spec_data, char *argument)
{
    char *keyword;
    char *arg_lower;
    char *kw_copy;
    int match_found = 0;
    
    /* Check if in the correct room */
    if (world[ch->in_room].number != spec_data->target_room) {
        send_to_char(spec_data->fail_msg, ch);
        send_to_char("\r\n", ch);
        return 1;
    }
    
    /* If no argument provided, prompt for target */
    if (!argument || !*argument) {
        send_to_char("Use it with what?\r\n", ch);
        return 1;
    }
    
    /* Convert argument to lowercase for matching */
    CREATE(arg_lower, char, strlen(argument) + 1);
    strcpy(arg_lower, argument);
    for (char *p = arg_lower; *p; p++) {
        *p = tolower(*p);
    }
    
    /* Check if argument matches any of the target keywords */
    /* Keywords are space-separated in target_keywords field */
    CREATE(kw_copy, char, strlen(spec_data->target_keywords) + 1);
    strcpy(kw_copy, spec_data->target_keywords);
    
    keyword = strtok(kw_copy, " ");
    while (keyword != NULL) {
        if (strstr(arg_lower, keyword)) {
            match_found = 1;
            break;
        }
        keyword = strtok(NULL, " ");
    }
    
    free(kw_copy);
    free(arg_lower);
    
    /* If no keyword matched, fail */
    if (!match_found) {
        send_to_char("Use it with what?\r\n", ch);
        return 1;
    }
    
    /* Success! Display success message */
    send_to_char(spec_data->success_msg, ch);
    send_to_char("\r\n", ch);
    
    /* Show room message */
    act(spec_data->room_msg, FALSE, ch, obj, 0, TO_ROOM);
    
    /* Give reward items if specified (only on first discovery) */
    if (!is_quest_completed(ch, spec_data->discovery_bit)) {
        extern struct obj_data *read_object(int nr, int type);
        extern struct index_data *obj_index;
        struct obj_data *reward_obj;
        char buf[MAX_STRING_LENGTH];
        
        if (spec_data->reward_item1 > 0) {
            reward_obj = read_object(spec_data->reward_item1, VIRTUAL);
            if (reward_obj) {
                obj_to_char(reward_obj, ch);
                snprintf(buf, sizeof(buf), "You find %s!\r\n", reward_obj->short_description);
                send_to_char(buf, ch);
            }
        }
        
        if (spec_data->reward_item2 > 0) {
            reward_obj = read_object(spec_data->reward_item2, VIRTUAL);
            if (reward_obj) {
                obj_to_char(reward_obj, ch);
                snprintf(buf, sizeof(buf), "You find %s!\r\n", reward_obj->short_description);
                send_to_char(buf, ch);
            }
        }
    }
    
    /* Grant discovery reward to character and group (this sets quest as completed) */
    grant_discovery_reward(ch, spec_data);
    
    /* Consume the item if specified */
    if (spec_data->consume_item) {
        extract_obj(obj);
    }
    
    return 1;
}
