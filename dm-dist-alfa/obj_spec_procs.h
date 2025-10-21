/* ************************************************************************
*  file: obj_spec_procs.h, Object special procedures.     Part of DIKUMUD *
*  Usage: Header for YAML-based object special procedures                 *
************************************************************************* */

#ifndef _OBJ_SPEC_PROCS_H_
#define _OBJ_SPEC_PROCS_H_

/* Special procedure types */
#define SPEC_PROC_NONE          0
#define SPEC_PROC_VALVE_ROPE    1  /* Use rope with valve mechanism */
#define SPEC_PROC_KEY_PANEL     2  /* Use key with maintenance panel */

/* Maximum length for special procedure strings */
#define MAX_SPEC_MSG_LEN 512

/* Structure to hold special procedure configuration */
struct obj_spec_proc_data {
    int spec_type;              /* Type of special procedure */
    int target_room;            /* Room where procedure works */
    char *success_msg;          /* Message on success */
    char *fail_msg;             /* Message on failure */
    char *room_msg;             /* Message to room on success */
    int xp_reward;              /* XP reward for first use (0 = no reward) */
    int discovery_bit;          /* Quest completion bit for tracking first use */
    int consume_item;           /* 1 if item is consumed on use, 0 otherwise */
};

/* Function prototypes */
void init_obj_spec_procs(void);
void free_obj_spec_procs(void);
struct obj_spec_proc_data *get_obj_spec_proc(int obj_vnum);
int execute_obj_spec_proc(struct char_data *ch, struct obj_data *obj, char *argument, int cmd);

/* Specific procedure handlers */
int spec_proc_valve_rope(struct char_data *ch, struct obj_data *obj, 
                         struct obj_spec_proc_data *spec_data, char *argument);
int spec_proc_key_panel(struct char_data *ch, struct obj_data *obj,
                        struct obj_spec_proc_data *spec_data, char *argument);

#endif /* _OBJ_SPEC_PROCS_H_ */
