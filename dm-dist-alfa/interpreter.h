/* ************************************************************************
*  file: Interpreter.h , Command interpreter module.      Part of DIKUMUD *
*  Usage: Procedures interpreting user command                            *
************************************************************************* */

/* Command number constants
 * These correspond to positions in the command[] array in interpreter.c
 * Using constants instead of hardcoded numbers prevents bugs when the
 * command array is modified.
 * 
 * Note: All commands should use these constants instead of hardcoded numbers.
 */
#define CMD_NORTH       1
#define CMD_EAST        2
#define CMD_SOUTH       3
#define CMD_WEST        4
#define CMD_UP          5
#define CMD_DOWN        6
#define CMD_ENTER       7
#define CMD_EXITS       8
#define CMD_KISS        9
#define CMD_GET         10
#define CMD_DRINK       11
#define CMD_EAT         12
#define CMD_WEAR        13
#define CMD_WIELD       14
#define CMD_LOOK        15
#define CMD_SCORE       16
#define CMD_SAY         17
#define CMD_SHOUT       18
#define CMD_TELL        19
#define CMD_INVENTORY   20
#define CMD_QUI         21
#define CMD_BOUNCE      22
#define CMD_SMILE       23
#define CMD_DANCE       24
#define CMD_KILL        25
#define CMD_CACKLE      26
#define CMD_LAUGH       27
#define CMD_GIGGLE      28
#define CMD_SHAKE       29
#define CMD_PUKE        30
#define CMD_GROWL       31
#define CMD_SCREAM      32
#define CMD_INSULT      33
#define CMD_COMFORT     34
#define CMD_NOD         35
#define CMD_SIGH        36
#define CMD_SULK        37
#define CMD_HELP        38
#define CMD_WHO         39
#define CMD_EMOTE       40
#define CMD_ECHO        41
#define CMD_STAND       42
#define CMD_SIT         43
#define CMD_REST        44
#define CMD_SLEEP       45
#define CMD_WAKE        46
#define CMD_FORCE       47
#define CMD_TRANSFER    48
#define CMD_HUG         49
#define CMD_SNUGGLE     50
#define CMD_CUDDLE      51
#define CMD_NUZZLE      52
#define CMD_CRY         53
#define CMD_NEWS        54
#define CMD_EQUIPMENT   55
#define CMD_BUY         56
#define CMD_SELL        57
#define CMD_VALUE       58
#define CMD_LIST        59
#define CMD_DROP        60
#define CMD_GOTO        61
#define CMD_WEATHER     62
#define CMD_READ        63
#define CMD_POUR        64
#define CMD_GRAB        65
#define CMD_REMOVE      66
#define CMD_PUT         67
#define CMD_SHUTDOW     68
#define CMD_SAVE        69
#define CMD_HIT         70
#define CMD_STRING      71
#define CMD_GIVE        72
#define CMD_QUIT        73
#define CMD_STAT        74
#define CMD_SET         75
#define CMD_TIME        76
#define CMD_LOAD        77
#define CMD_PURGE       78
#define CMD_SHUTDOWN    79
#define CMD_IDEA        80
#define CMD_TYPO        81
#define CMD_BUG         82
#define CMD_WHISPER     83
#define CMD_ACTIVATE    84
#define CMD_AT          85
#define CMD_ASK         86
#define CMD_ORDER       87
#define CMD_SIP         88
#define CMD_TASTE       89
#define CMD_SNOOP       90
#define CMD_FOLLOW      91
#define CMD_RENT        92
#define CMD_OFFER       93
#define CMD_POKE        94
#define CMD_ADVANCE     95
#define CMD_ACCUSE      96
#define CMD_GRIN        97
#define CMD_BOW         98
#define CMD_OPEN        99
#define CMD_CLOSE       100
#define CMD_LOCK        101
#define CMD_UNLOCK      102
#define CMD_LEAVE       103
#define CMD_APPLAUD     104
#define CMD_BLUSH       105
#define CMD_BURP        106
#define CMD_CHUCKLE     107
#define CMD_CLAP        108
#define CMD_COUGH       109
#define CMD_CURTSEY     110
#define CMD_FART        111
#define CMD_FLIP        112
#define CMD_FONDLE      113
#define CMD_FROWN       114
#define CMD_GASP        115
#define CMD_GLARE       116
#define CMD_GROAN       117
#define CMD_GROPE       118
#define CMD_HICCUP      119
#define CMD_LICK        120
#define CMD_LOVE        121
#define CMD_MOAN        122
#define CMD_NIBBLE      123
#define CMD_POUT        124
#define CMD_PURR        125
#define CMD_RUFFLE      126
#define CMD_SHIVER      127
#define CMD_SHRUG       128
#define CMD_SING        129
#define CMD_SLAP        130
#define CMD_SMIRK       131
#define CMD_SNAP        132
#define CMD_SNEEZE      133
#define CMD_SNICKER     134
#define CMD_SNIFF       135
#define CMD_SNORE       136
#define CMD_SPIT        137
#define CMD_SQUEEZE     138
#define CMD_STARE       139
#define CMD_STRUT       140
#define CMD_THANK       141
#define CMD_TWIDDLE     142
#define CMD_WAVE        143
#define CMD_WHISTLE     144
#define CMD_WIGGLE      145
#define CMD_WINK        146
#define CMD_YAWN        147
#define CMD_SNOWBALL    148
#define CMD_WRITE       149
#define CMD_HOLD        150
#define CMD_FLEE        151
#define CMD_SNEAK       152
#define CMD_HIDE        153
#define CMD_BACKSTAB    154
#define CMD_PICK        155
#define CMD_STEAL       156
#define CMD_BASH        157
#define CMD_RESCUE      158
#define CMD_KICK        159
#define CMD_FRENCH      160
#define CMD_COMB        161
#define CMD_MASSAGE     162
#define CMD_TICKLE      163
#define CMD_PRACTICE    164
#define CMD_PAT         165
#define CMD_EXAMINE     166
#define CMD_TAKE        167
#define CMD_INFO        168
#define CMD_SAY_QUOTE   169
#define CMD_PRACTISE    170
#define CMD_CURSE       171
#define CMD_USE         172
#define CMD_WHERE       173
#define CMD_LEVELS      174
#define CMD_REROLL      175
#define CMD_PRAY        176
#define CMD_EMOTE_COMMA 177
#define CMD_BEG         178
#define CMD_BLEED       179
#define CMD_CRINGE      180
#define CMD_DAYDREAM    181
#define CMD_FUME        182
#define CMD_GROVEL      183
#define CMD_HOP         184
#define CMD_NUDGE       185
#define CMD_PEER        186
#define CMD_POINT       187
#define CMD_PONDER      188
#define CMD_PUNCH       189
#define CMD_SNARL       190
#define CMD_SPANK       191
#define CMD_STEAM       192
#define CMD_TACKLE      193
#define CMD_TAUNT       194
#define CMD_THINK       195
#define CMD_WHINE       196
#define CMD_WORSHIP     197
#define CMD_YODEL       198
#define CMD_BRIEF       199
#define CMD_WIZ         200
#define CMD_CONSIDER    201
#define CMD_GROUP       202
#define CMD_RESTORE     203
#define CMD_RETURN      204
#define CMD_SWITCH      205
#define CMD_QUAFF       206
#define CMD_RECITE      207
#define CMD_USERS       208
#define CMD_POSE        209
#define CMD_NOSHOUT     210
#define CMD_WIZHELP     211
#define CMD_CREDITS     212
#define CMD_COMPACT     213
#define CMD_WIZLOCK     214
#define CMD_NOTELL      215
#define CMD_NOEMOTE     216
#define CMD_FREEZE      217
#define CMD_GOL         218
#define CMD_WIZLIST     219
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
