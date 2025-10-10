/* ************************************************************************
*  file: quest.c , Quest system                           Part of DIKUMUD *
*  Usage: Quest management functions                                      *
************************************************************************* */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "structs.h"
#include "utils.h"
#include "comm.h"
#include "db.h"
#include "handler.h"
#include "spells.h"
#include "quest.h"

/* Global quest data */
struct quest_data *quest_index = NULL;
int top_of_quest_table = 0;

/* External functions */
extern void slog(char *str);
extern char *fread_string(FILE *fl);
extern struct char_data *character_list;

/* Find quest data by giver vnum */
struct quest_data *find_quest_by_giver(int giver_vnum)
{
	int i;
	
	for (i = 0; i < top_of_quest_table; i++) {
		if (quest_index[i].giver_vnum == giver_vnum) {
			return &quest_index[i];
		}
	}
	
	return NULL;
}

/* Check if character has a quest of specific type */
int has_quest_type(struct char_data *ch, int quest_type)
{
	struct affected_type *af;
	
	for (af = ch->affected; af; af = af->next) {
		if (af->type == quest_type) {
			return 1;
		}
	}
	
	return 0;
}

/* Grant quest rewards to character */
void grant_quest_reward(struct char_data *ch, struct quest_data *quest)
{
	char buf[MAX_STRING_LENGTH];
	struct obj_data *obj;
	
	/* Experience reward */
	if (quest->reward_exp > 0) {
		gain_exp(ch, quest->reward_exp);
		snprintf(buf, sizeof(buf), "You gain %d experience!\n\r", quest->reward_exp);
		send_to_char(buf, ch);
	}
	
	/* Gold reward */
	if (quest->reward_gold > 0) {
		GET_GOLD(ch) += quest->reward_gold;
		snprintf(buf, sizeof(buf), "You receive %d gold coins!\n\r", quest->reward_gold);
		send_to_char(buf, ch);
	}
	
	/* Item reward */
	if (quest->reward_item > 0) {
		obj = read_object(quest->reward_item, VIRTUAL);
		if (obj) {
			obj_to_char(obj, ch);
			snprintf(buf, sizeof(buf), "You receive %s!\n\r", 
				obj->short_description);
			send_to_char(buf, ch);
		}
	}
}

/* Boot quests from file */
void boot_quests(void)
{
	FILE *fl;
	int nr = 0, i;
	char buf[256];
	char line[256];
	
	if (!(fl = fopen("tinyworld.qst", "r"))) {
		slog("   No quest file found - quests disabled");
		return;
	}
	
	/* Count quests by counting # markers */
	while (fgets(line, sizeof(line), fl)) {
		if (*line == '#' && line[1] != '9') {  /* Skip #99999 */
			nr++;
		}
	}
	
	if (nr == 0) {
		slog("   No quests found in quest file");
		fclose(fl);
		return;
	}
	
	rewind(fl);
	
	CREATE(quest_index, struct quest_data, nr);
	
	for (i = 0; i < nr; i++) {
		/* Read quest number */
		if (!fgets(line, sizeof(line), fl) || *line != '#') {
			slog("   Error reading quest number");
			break;
		}
		sscanf(line + 1, "%d", &quest_index[i].qnum);
		
		/* Read giver, type, duration */
		if (fscanf(fl, " %d %d %d\n", 
			&quest_index[i].giver_vnum,
			&quest_index[i].quest_type,
			&quest_index[i].duration) != 3) {
			slog("   Error reading quest giver/type/duration");
			break;
		}
		
		/* Read target, item, flags */
		if (fscanf(fl, " %d %d %d\n",
			&quest_index[i].target_vnum,
			&quest_index[i].item_vnum,
			&quest_index[i].quest_flags) != 3) {
			slog("   Error reading quest target/item/flags");
			break;
		}
		
		/* Read rewards */
		if (fscanf(fl, " %d %d %d\n",
			&quest_index[i].reward_exp,
			&quest_index[i].reward_gold,
			&quest_index[i].reward_item) != 3) {
			slog("   Error reading quest rewards");
			break;
		}
		
		/* Read text strings */
		quest_index[i].quest_text = fread_string(fl);
		quest_index[i].complete_text = fread_string(fl);
		quest_index[i].fail_text = fread_string(fl);
		
		/* Read S terminator */
		if (!fgets(line, sizeof(line), fl)) {
			slog("   Error reading quest terminator");
			break;
		}
	}
	
	fclose(fl);
	top_of_quest_table = i;
	
	snprintf(buf, sizeof(buf), "   %d quests loaded", top_of_quest_table);
	slog(buf);
}

/* Automatically assign quest_giver special procedure to all quest-giving mobs */
void assign_quest_givers(void)
{
	extern struct index_data *mob_index;
	extern int real_mobile(int virtual);
	extern int quest_giver(struct char_data *ch, int cmd, char *arg);
	int i, real_mob;
	char buf[256];
	int assigned = 0;
	
	for (i = 0; i < top_of_quest_table; i++) {
		real_mob = real_mobile(quest_index[i].giver_vnum);
		if (real_mob >= 0) {
			mob_index[real_mob].func = quest_giver;
			assigned++;
		} else {
			snprintf(buf, sizeof(buf), 
				"   Warning: Quest %d references non-existent mob %d",
				quest_index[i].qnum, quest_index[i].giver_vnum);
			slog(buf);
		}
	}
	
	snprintf(buf, sizeof(buf), "   %d quest givers assigned", assigned);
	slog(buf);
}
