/* ************************************************************************
*  file: Interpreter.h , Command interpreter module.      Part of DIKUMUD *
*  Usage: Procedures interpreting user command                            *
************************************************************************* */

/* Command number constants
 * These correspond to positions in the command[] array in interpreter.c
 * Using constants instead of hardcoded numbers prevents bugs when the
 * command array is modified.
 */
#define CMD_NORTH       1
#define CMD_EAST        2
#define CMD_SOUTH       3

#define CMD_BUY         56
#define CMD_LIST        59
#define CMD_DROP        60

#define CMD_ASK         86
#define CMD_SNEAK       152

#define CMD_PRACTICE    164
#define CMD_PRACTISE    170

#define CMD_PRAY        176
#define CMD_QUAFF       206

#define CMD_REEQUIP     220
#define CMD_ZONE        221
#define CMD_FILL        222

void command_interpreter(struct char_data *ch, char *argument);
int search_block(char *arg, char **list, bool exact);
int old_search_block(char *argument,int begin,int length,char **list,int mode);
char lower( char c );
void argument_interpreter(char *argument, char *first_arg, char *second_arg);
char *one_argument(char *argument,char *first_arg);
int fill_word(char *argument);
void half_chop(char *string, char *arg1, char *arg2);
void nanny(struct descriptor_data *d, char *arg);
int is_abbrev(char *arg1, char *arg2);


struct command_info
{
	void (*command_pointer) (struct char_data *ch, char *argument, int cmd);
	byte minimum_position;
	byte minimum_level;
};
