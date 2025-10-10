/* ************************************************************************
*  file: quest.h , Quest system                           Part of DIKUMUD *
*  Usage: Quest management functions and data                             *
************************************************************************* */

#ifndef _QUEST_H_
#define _QUEST_H_

/* Global quest index (loaded from lib/tinyworld.qst) */
extern struct quest_data *quest_index;
extern int top_of_quest_table;

/* Quest management functions */
void boot_quests(void);
void assign_quest_givers(void);
struct quest_data *find_quest_by_giver(int giver_vnum);
void grant_quest_reward(struct char_data *ch, struct quest_data *quest);
int has_quest_type(struct char_data *ch, int quest_type);

#endif /* _QUEST_H_ */
