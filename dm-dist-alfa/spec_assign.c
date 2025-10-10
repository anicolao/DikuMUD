/* ************************************************************************
*  file: spec_assign.c , Special module.                  Part of DIKUMUD *
*  Usage: Procedures assigning function pointers.                         *
*  Copyright (C) 1990, 1991 - see 'license.doc' for complete information. *
************************************************************************* */

#include <stdio.h>
#include "structs.h"
#include "db.h"

extern struct room_data *world;
extern struct index_data *mob_index;
extern struct index_data *obj_index;
void boot_the_shops();
void assign_the_shopkeepers();

/* ********************************************************************
*  Assignments                                                        *
******************************************************************** */

/* assign special procedures to mobiles */
void assign_mobiles(void)
{
	int cityguard(struct char_data *ch, int cmd, char *arg);
	int receptionist(struct char_data *ch, int cmd, char *arg);
	int guild(struct char_data *ch, int cmd, char *arg);
	int guild_guard(struct char_data *ch, int cmd, char *arg);
	int puff(struct char_data *ch, int cmd, char *arg);
	int fido(struct char_data *ch, int cmd, char *arg);
	int janitor(struct char_data *ch, int cmd, char *arg);
	int mayor(struct char_data *ch, int cmd, char *arg);
	int snake(struct char_data *ch, int cmd, char *arg);
	int thief(struct char_data *ch, int cmd, char *arg);
	int magic_user(struct char_data *ch, int cmd, char *arg);
	int bat_red(struct char_data *ch, int cmd, char *arg);
	int bat_blue(struct char_data *ch, int cmd, char *arg);
	int bat_green(struct char_data *ch, int cmd, char *arg);
	int bat_black(struct char_data *ch, int cmd, char *arg);
	int bat_white(struct char_data *ch, int cmd, char *arg);

	mob_index[real_mobile(1)].func = puff;

	mob_index[real_mobile(3060)].func = cityguard;
	mob_index[real_mobile(3067)].func = cityguard;
	mob_index[real_mobile(3061)].func = janitor;
	mob_index[real_mobile(3062)].func = fido;
	mob_index[real_mobile(3066)].func = fido;

	mob_index[real_mobile(3005)].func = receptionist;

	mob_index[real_mobile(3020)].func = guild;
	mob_index[real_mobile(3021)].func = guild;
	mob_index[real_mobile(3022)].func = guild;
	mob_index[real_mobile(3023)].func = guild;

	mob_index[real_mobile(3024)].func = guild_guard;
	mob_index[real_mobile(3025)].func = guild_guard;
	mob_index[real_mobile(3026)].func = guild_guard;
	mob_index[real_mobile(3027)].func = guild_guard;

	mob_index[real_mobile(3143)].func = mayor;

	/* Quest givers are now assigned automatically in assign_quest_givers()
	 * after boot_quests() loads quest data from tinyworld.qst */

	boot_the_shops();
	assign_the_shopkeepers();
}



/* assign special procedures to objects */
void assign_objects(void)
{
	int board(struct char_data *ch, int cmd, char *arg);

	obj_index[real_object(3099)].func = board;
}



/* assign special procedures to rooms */
void assign_rooms(void)
{
	int dump(struct char_data *ch, int cmd, char *arg);
	int chalice(struct char_data *ch, int cmd, char *arg);
	int kings_hall(struct char_data *ch, int cmd, char *arg);
	int pet_shops(struct char_data *ch, int cmd, char *arg);
	int mar_gate(struct char_data *ch, int cmd, char *arg);
	int pray_for_items(struct char_data *ch, int cmd, char *arg);
	int worm_ritual(struct char_data *ch, int cmd, char *arg);

	world[real_room(3030)].funct = dump;
	world[real_room(3054)].funct = pray_for_items;

	world[real_room(3031)].funct = pet_shops;
}
