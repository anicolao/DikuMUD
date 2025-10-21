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
    extern void slog(char *str);
    char buf[256];
    
    slog("DEBUG: init_obj_spec_procs called");
    
    /* Initial capacity for spec proc table */
    spec_proc_capacity = 10;
    CREATE(spec_proc_table, struct obj_spec_proc_data, spec_proc_capacity);
    spec_proc_count = 0;
    
    /* Add hardcoded special procedures for sewers deep discovery */
    /* These would normally be loaded from YAML, but for now we hardcode them */
    
    /* Rope + Valve (object 3224 in room 3157) - Discovery bit 31 */
    {
        struct obj_spec_proc_data *spec = &spec_proc_table[spec_proc_count++];
        spec->spec_type = SPEC_PROC_VALVE_ROPE;
        spec->target_room = 3157;
        spec->xp_reward = 100;  /* XP reward for first discovery */
        spec->discovery_bit = 31;  /* Use bit 31 for valve discovery */
        spec->consume_item = 1;  /* Rope is consumed */
        
        /* Allocate and set messages */
        CREATE(spec->success_msg, char, MAX_SPEC_MSG_LEN);
        CREATE(spec->fail_msg, char, MAX_SPEC_MSG_LEN);
        CREATE(spec->room_msg, char, MAX_SPEC_MSG_LEN);
        
        strncpy(spec->success_msg,
                "You loop the rope through the pulley above the valve wheel and pull "
                "with all your might! The rope provides the leverage needed, and with "
                "a screech of protesting metal, the ancient valve begins to turn. "
                "Water rushes through pipes all around you as the mechanism activates!",
                MAX_SPEC_MSG_LEN - 1);
        
        strncpy(spec->fail_msg,
                "You need to be near the valve mechanism to use the rope with it.",
                MAX_SPEC_MSG_LEN - 1);
        
        strncpy(spec->room_msg,
                "$n uses $p to activate an ancient valve mechanism!",
                MAX_SPEC_MSG_LEN - 1);
        
        snprintf(buf, sizeof(buf), "DEBUG: Added rope+valve spec (vnum 3224, room 3157)");
        slog(buf);
    }
    
    /* Iron Key + Panel (object 3221 in room 3151) - Discovery bit 32 */
    {
        struct obj_spec_proc_data *spec = &spec_proc_table[spec_proc_count++];
        spec->spec_type = SPEC_PROC_KEY_PANEL;
        spec->target_room = 3151;
        spec->xp_reward = 75;  /* XP reward for first discovery */
        spec->discovery_bit = 32;  /* Use bit 32 for panel discovery */
        spec->consume_item = 0;  /* Key is not consumed */
        
        /* Allocate and set messages */
        CREATE(spec->success_msg, char, MAX_SPEC_MSG_LEN);
        CREATE(spec->fail_msg, char, MAX_SPEC_MSG_LEN);
        CREATE(spec->room_msg, char, MAX_SPEC_MSG_LEN);
        
        strncpy(spec->success_msg,
                "You insert the ancient iron key into the maintenance panel's lock. "
                "With a satisfying click, the corroded mechanism yields and the panel "
                "swings open, revealing a compartment that has been sealed for centuries!",
                MAX_SPEC_MSG_LEN - 1);
        
        strncpy(spec->fail_msg,
                "You need to be near the maintenance panel to use the key with it.",
                MAX_SPEC_MSG_LEN - 1);
        
        strncpy(spec->room_msg,
                "$n unlocks an ancient maintenance panel with $p!",
                MAX_SPEC_MSG_LEN - 1);
        
        snprintf(buf, sizeof(buf), "DEBUG: Added key+panel spec (vnum 3221, room 3151)");
        slog(buf);
    }
    
    snprintf(buf, sizeof(buf), "DEBUG: init_obj_spec_procs complete, loaded %d specs", spec_proc_count);
    slog(buf);
}

/* Free special procedure data */
void free_obj_spec_procs(void)
{
    int i;
    
    if (spec_proc_table) {
        for (i = 0; i < spec_proc_count; i++) {
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
    
    /* For now, we match based on object vnum and spec type */
    /* Object 3224 (rope) -> SPEC_PROC_VALVE_ROPE */
    /* Object 3221 (iron key) -> SPEC_PROC_KEY_PANEL */
    
    for (i = 0; i < spec_proc_count; i++) {
        if (obj_vnum == 3224 && spec_proc_table[i].spec_type == SPEC_PROC_VALVE_ROPE) {
            return &spec_proc_table[i];
        }
        if (obj_vnum == 3221 && spec_proc_table[i].spec_type == SPEC_PROC_KEY_PANEL) {
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
    extern void slog(char *str);
    char debug_buf[256];
    
    /* Debug: Send message to player so it appears in test output */
    snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: execute_obj_spec_proc called, cmd=%d]\r\n", cmd);
    send_to_char(debug_buf, ch);
    
    /* Only handle USE command */
    if (cmd != CMD_USE) {
        snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Not USE command (expected %d), returning 0]\r\n", CMD_USE);
        send_to_char(debug_buf, ch);
        return 0;
    }
    
    /* Get virtual number from object */
    if (obj->item_number >= 0 && obj->item_number < 99999) {
        obj_vnum = obj_index[obj->item_number].virtual;
        snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Object vnum=%d]\r\n", obj_vnum);
        send_to_char(debug_buf, ch);
    } else {
        snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Invalid item_number=%d]\r\n", obj->item_number);
        send_to_char(debug_buf, ch);
        return 0;
    }
    
    /* Get special procedure data for this object */
    spec_data = get_obj_spec_proc(obj_vnum);
    if (!spec_data) {
        snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: No spec_data for vnum %d]\r\n", obj_vnum);
        send_to_char(debug_buf, ch);
        return 0;
    }
    
    snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Found spec_data, type=%d]\r\n", spec_data->spec_type);
    send_to_char(debug_buf, ch);
    
    /* Execute the appropriate handler */
    switch (spec_data->spec_type) {
        case SPEC_PROC_VALVE_ROPE:
            snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Executing valve_rope procedure]\r\n");
            send_to_char(debug_buf, ch);
            result = spec_proc_valve_rope(ch, obj, spec_data, argument);
            break;
        case SPEC_PROC_KEY_PANEL:
            snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Executing key_panel procedure]\r\n");
            send_to_char(debug_buf, ch);
            result = spec_proc_key_panel(ch, obj, spec_data, argument);
            break;
        default:
            snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Unknown spec_type=%d]\r\n", spec_data->spec_type);
            send_to_char(debug_buf, ch);
            return 0;
    }
    
    snprintf(debug_buf, sizeof(debug_buf), "[DEBUG: Procedure returned %d]\r\n", result);
    send_to_char(debug_buf, ch);
    
    return result;
}

/* Handler for rope + valve procedure */
int spec_proc_valve_rope(struct char_data *ch, struct obj_data *obj,
                         struct obj_spec_proc_data *spec_data, char *argument)
{
    char buf[MAX_STRING_LENGTH];
    extern void slog(char *str);
    char debug_buf[256];
    
    snprintf(debug_buf, sizeof(debug_buf), "DEBUG: spec_proc_valve_rope: room=%d, target=%d, arg='%s'", 
             world[ch->in_room].number, spec_data->target_room, argument ? argument : "NULL");
    slog(debug_buf);
    
    /* Check if in the correct room */
    if (world[ch->in_room].number != spec_data->target_room) {
        snprintf(debug_buf, sizeof(debug_buf), "DEBUG: Wrong room, sending fail message");
        slog(debug_buf);
        send_to_char(spec_data->fail_msg, ch);
        send_to_char("\r\n", ch);
        return 1;
    }
    
    /* Check if argument mentions valve/wheel/mechanism */
    if (!argument || (!strstr(argument, "valve") && !strstr(argument, "wheel") &&
                      !strstr(argument, "mechanism"))) {
        snprintf(debug_buf, sizeof(debug_buf), "DEBUG: Argument doesn't mention valve/wheel/mechanism");
        slog(debug_buf);
        send_to_char("Use the rope with what?\r\n", ch);
        return 1;
    }
    
    snprintf(debug_buf, sizeof(debug_buf), "DEBUG: Success! Activating valve");
    slog(debug_buf);
    
    /* Success! Display success message */
    send_to_char(spec_data->success_msg, ch);
    send_to_char("\r\n", ch);
    
    /* Show room message */
    act(spec_data->room_msg, FALSE, ch, obj, 0, TO_ROOM);
    
    /* Grant discovery reward to character and group */
    grant_discovery_reward(ch, spec_data);
    
    /* Consume the rope if specified */
    if (spec_data->consume_item) {
        extract_obj(obj);
    }
    
    return 1;
}

/* Handler for key + panel procedure */
int spec_proc_key_panel(struct char_data *ch, struct obj_data *obj,
                        struct obj_spec_proc_data *spec_data, char *argument)
{
    char buf[MAX_STRING_LENGTH];
    struct obj_data *tool_set, *diagram;
    
    /* Check if in the correct room */
    if (world[ch->in_room].number != spec_data->target_room) {
        send_to_char(spec_data->fail_msg, ch);
        send_to_char("\r\n", ch);
        return 1;
    }
    
    /* Check if argument mentions panel/compartment/door */
    if (!argument || (!strstr(argument, "panel") && !strstr(argument, "compartment") &&
                      !strstr(argument, "door"))) {
        send_to_char("Use the key with what?\r\n", ch);
        return 1;
    }
    
    /* Success! Display success message */
    send_to_char(spec_data->success_msg, ch);
    send_to_char("\r\n", ch);
    
    /* Show room message */
    act(spec_data->room_msg, FALSE, ch, obj, 0, TO_ROOM);
    
    /* Grant discovery reward to character and group */
    grant_discovery_reward(ch, spec_data);
    
    /* Create the reward objects (ancient tool set and engineering diagram) */
    /* These would be objects 3295 and 3296 based on design doc, but we'll use
     * objects that exist: let's spawn some treasure as placeholder */
    
    /* Try to create ancient tool set (3233 - preserved rations is what exists) */
    /* Actually, we should create objects that match the design doc */
    /* For now, just send a message about finding items */
    send_to_char("Inside the compartment, you find ancient engineering tools and diagrams!\r\n", ch);
    
    /* Note: Key is not consumed, so we don't extract it */
    
    return 1;
}
