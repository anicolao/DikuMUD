/* ************************************************************************
*  file: constants.c                                      Part of DIKUMUD *
*  Usage: For constants used by the game.                                 *
*  Copyright (C) 1990, 1991 - see 'license.doc' for complete information. *
************************************************************************* */

#include "structs.h"
#include "limits.h"


const char *spell_wear_off_msg[] = {
  "RESERVED DB.C",
  "Your personal shield device powers down.",
  "!Teleport!",
  "Your performance optimizer deactivates.",
  "Your optical disruptor effect wears off.",
  "!Burning Hands!",
  "!Call Lightning",
  "Your neural controller effect fades.",
  "!Chill Touch!",
  "!Clone!",
  "!Color Spray!",
  "!Control Weather!",
  "!Create Food!",
  "!Create Water!",
  "!Cure Blind!",
  "!Cure Critic!",
  "!Cure Light!",
  "Your neural inhibitor effect dissipates.",
  "Your alignment scanner deactivates.",
  "Your invisibility detector powers down.",
  "Your technology scanner deactivates.",
  "Your toxin analyzer shuts off.",
  "!Dispel Evil!",
  "!Earthquake!",
  "!Enchant Weapon!",
  "!Energy Drain!",
  "!Fireball!",
  "!Harm!",
  "!Heal",
  "Your invisibility cloak deactivates and you become visible.",
  "!Lightning Bolt!",
  "!Locate object!",
  "!Magic Missile!",
  "Your toxin injector effect subsides.",
  "Your evil ward device deactivates.",
  "!Remove Curse!",
  "Your sanctuary field collapses.",
  "!Shocking Grasp!",
  "Your soporific gas effect wears off.",
  "Your strength amplifier powers down.",
  "!Summon!",
  "!Ventriloquate!",
  "!Word of Recall!",
  "!Remove Poison!",
  "Your life detector shuts down.",
  "",  /* NO MESSAGE FOR SNEAK*/
  "!Hide!",
  "!Steal!",
  "!Backstab!",
  "!Pick Lock!",
  "!Kick!",
  "!Bash!",
  "!Rescue!",
  "!UNUSED!"
};


const int rev_dir[] = 
{
	2,
	3,
	0,
	1,	
	5,
	4
}; 

const int movement_loss[]=
{
	1,	/* Inside     */
	2,  /* City       */
	2,  /* Field      */
	3,  /* Forest     */
	4,  /* Hills      */
	6,  /* Mountains  */
  4,  /* Swimming   */
  1   /* Unswimable */
};

const char *dirs[] = 
{
	"north",
	"east",
	"south",
	"west",
	"up",
	"down",
	"\n"
};

const char *weekdays[7] = { 
	"the Day of the Moon",
	"the Day of the Bull",
	"the Day of the Deception",
	"the Day of Thunder",
	"the Day of Freedom",
	"the day of the Great Gods",
	"the Day of the Sun" };

const char *month_name[17] = {
	"Month of Winter",           /* 0 */
	"Month of the Winter Wolf",
	"Month of the Frost Giant",
	"Month of the Old Forces",
	"Month of the Grand Struggle",
	"Month of the Spring",
	"Month of Nature",
	"Month of Futility",
	"Month of the Dragon",
	"Month of the Sun",
	"Month of the Heat",
	"Month of the Battle",
	"Month of the Dark Shades",
	"Month of the Shadows",
	"Month of the Long Shadows",
	"Month of the Ancient Darkness",
	"Month of the Great Evil"
};

const int sharp[] = {
   0,
   0,
   0,
   1,    /* Slashing */
   0,
   0,
   0,
   0,    /* Bludgeon */
   0,
   0,
   0,
   0 };  /* Pierce   */

const char *where[] = {
	"<used as light>      ",
	"<worn on finger>     ",
	"<worn on finger>     ",
	"<worn around neck>   ",
	"<worn around neck>   ",
	"<worn on body>       ",
	"<worn on head>       ",
	"<worn on legs>       ",
	"<worn on feet>       ",
	"<worn on hands>      ",
	"<worn on arms>       ",
	"<worn as shield>     ",
	"<worn about body>    ",
	"<worn about waist>   ",
	"<worn around wrist>  ",
	"<worn around wrist>  ",
	"<wielded>            ",
	"<held>               " 
}; 

const char *drinks[]=
{
	"water",
	"beer",
	"wine",
	"ale",
	"dark ale",
	"whisky",
	"lemonade",
	"firebreather",
	"local speciality",
	"slime mold juice",
	"milk",
	"tea",
	"coffee",
	"blood",
	"salt water",
	"coca cola"
};

const char *drinknames[]=
{
	"water",
	"beer",
	"wine",
	"ale",
	"ale",
	"whisky",
	"lemonade",
	"firebreather",
	"local",
	"juice",
	"milk",
	"tea",
	"coffee",
	"blood",
	"salt",
	"cola"
};

const int drink_aff[][3] = {
	{ 0,1,10 },  /* Water    */
	{ 3,2,5 },   /* beer     */
	{ 5,2,5 },   /* wine     */
	{ 2,2,5 },   /* ale      */
	{ 1,2,5 },   /* ale      */
	{ 6,1,4 },   /* Whiskey  */
	{ 0,1,8 },   /* lemonade */
	{ 10,0,0 },  /* firebr   */
	{ 3,3,3 },   /* local    */
	{ 0,4,-8 },  /* juice    */
	{ 0,3,6 },
	{ 0,1,6 },
	{ 0,1,6 },
	{ 0,2,-1 },
	{ 0,1,-2 },
	{ 0,1,5 }
};

const char *color_liquid[]=
{
	"clear",
	"brown",
	"clear",
	"brown",
	"dark",
	"golden",
	"red",
	"green",
	"clear",
	"light green",
	"white",
	"brown",
	"black",
	"red",
	"clear",
	"black"
};

const char *fullness[] =
{
	"less than half ",
	"about half ",
	"more than half ",
	""
};

const struct title_type titles[4][25] = {
{ {"the Man","the Woman",0},
  {"the Apprentice","the Apprentice",1},
  {"the Student","the Student",2500},
  {"the Journeyman","the Journeywoman",5000},
  {"the Adept","the Adept",10000},
  {"the Savant","the Savant",20000},
  {"the Master Savant","the Master Savant",40000},
  {"the First Savant","the First Savant",60000},
  {"the Elder Savant","the Elder Savant",90000},
  {"the High Savant","the High Savant",135000},
  {"the Supreme Savant","the Supreme Savant",250000},
  {"the Scientist","the Scientist",375000},
  {"the Master Scientist","the Master Scientist",750000},
  {"the First Scientist","the First Scientist",1125000},
  {"the Elder Scientist","the Elder Scientist",1500000},
  {"the High Scientist","the High Scientist",1875000},
  {"the Supreme Scientist","the Supreme Scientist",2250000},
  {"the Master Mind","the Master Mind",2625000},
  {"the Legendary Master Mind","the Legendary Master Mind",3000000},
  {"the Supreme Master Mind","the Supreme Master Mind",3375000},
  {"the Transcendent Mind","the Transcendent Mind",3750000},
  {"the Immortal Genius","the Immortal Genius",4000000},
  {"the Demi-God of Knowledge","the Demi-Goddess of Knowledge",5000000},
  {"the God of Knowledge","the Goddess of Knowledge",6000000},
  {"the Implementator","the Implementress",7000000} },

{ {"the Man","the Woman",0},
  {"the Minor Noble","the Minor Noble",1},
  {"the Noble","the Noble",1500},
  {"the High Noble","the High Noble",3000},
  {"the Odwar","the Odwar",6000},
  {"the Senior Odwar","the Senior Odwar",13000},
  {"the Jed","the Princess",27500},
  {"the High Jed","the High Princess",55000},
  {"the Supreme Jed","the Supreme Princess",110000},
  {"the Lesser Jeddak","the Lesser Jeddara",225000},
  {"the Jeddak","the Jeddara",450000},
  {"the High Jeddak","the High Jeddara",675000},
  {"the Greater Jeddak","the Greater Jeddara",900000},
  {"the Supreme Jeddak","the Supreme Jeddara",1125000},
  {"the Jeddak of Jeddaks","the Jeddara of Jeddaras",1350000},
  {"the Prince of Mars","the Princess of Mars",1575000},
  {"the Warlord","the Warlord",1800000},
  {"the High Warlord","the High Warlord",2025000},
  {"the Supreme Warlord","the Supreme Warlord",2250000},
  {"the Warlord of Mars","the Warlord of Mars",2475000},
  {"the Emperor of Mars","the Empress of Mars",2700000},
  {"the Immortal Sovereign","the Immortal Sovereign",3000000},
  {"the Demi-God Ruler","the Demi-Goddess Ruler",5000000},
  {"the God-King","the God-Queen",6000000},
  {"the Implementator","the Implementress",7000000} },

{ {"the Man","the Woman",0},
  {"the Initiate","the Initiate",1},
  {"the Novice Blade","the Novice Blade",1250},
  {"the Blade","the Blade",2500},
  {"the Skilled Blade","the Skilled Blade",5000},
  {"the Silent Blade","the Silent Blade",10000},
  {"the Master Blade","the Master Blade",20000},
  {"the Guild Blade","the Guild Blade",30000},
  {"the Elite Blade","the Elite Blade",70000},
  {"the Shadow","the Shadow",110000},
  {"the Silent Shadow","the Silent Shadow",160000},
  {"Death's Shadow","Death's Shadow",220000},
  {"the Master Shadow","the Master Shadow",440000},
  {"the Elder Shadow","the Elder Shadow",660000},
  {"the High Shadow","the High Shadow",880000},
  {"the Shadow Lord","the Shadow Lady",1100000},
  {"the Shadow Master","the Shadow Mistress",1320000},
  {"the Guild Master","the Guild Mistress",1540000},
  {"the Legendary Shadow","the Legendary Shadow",1760000},
  {"the Shadow of Death","the Shadow of Death",1980000},
  {"the Supreme Shadow","the Supreme Shadow",2200000},
  {"the Immortal Shadow","the Immortal Shadow",2500000},
  {"the Demi-God of Death","the Demi-Goddess of Death",5000000},
  {"the God of Death","the Goddess of Death",6000000},
  {"the Implementator","the Implementress",7000000} },

{ {"the Man","the Woman",0},
  {"the Recruit","the Recruit",1},
  {"the Warrior","the Warrior",2000},
  {"the Veteran Warrior","the Veteran Warrior",4000},
  {"the Padwar","the Padwar",8000},
  {"the Senior Padwar","the Senior Padwar",16000},
  {"the Dwar","the Dwar",32000},
  {"the Dwar Commander","the Dwar Commander",64000},
  {"the Senior Dwar","the Senior Dwar",125000},
  {"the Odwar","the Odwar",250000},
  {"the Odwar of the Armies","the Odwar of the Armies",500000},
  {"the High Odwar","the High Odwar",750000},
  {"the Supreme Odwar","the Supreme Odwar",1000000},
  {"the Warlord","the Warlord",1250000},
  {"the Warlord of Legions","the Warlord of Legions",1500000},
  {"the High Warlord","the High Warlord",1750000},
  {"the Supreme Warlord","the Supreme Warlord",2000000},
  {"the Jeddak's Champion","the Jeddara's Champion",2250000},
  {"the Legendary Warlord","the Legendary Warlord",2500000},
  {"the Warlord of Mars","the Warlord of Mars",2750000},
  {"the Supreme Warlord of Mars","the Supreme Warlord of Mars",3000000},
  {"the Immortal Warrior","the Immortal Warrior",3250000},
  {"the Demi-God of War","the Demi-Goddess of War",5000000},
  {"the God of War","the Goddess of War",6000000},
  {"the Implementator","the Implementress",7000000} }
};

const char *item_types[] = {
	"UNDEFINED",
	"LIGHT",
	"SCROLL",
	"WAND",
	"STAFF",
	"WEAPON",
	"FIRE WEAPON",
	"MISSILE",
	"TREASURE",
	"ARMOR",
	"POTION",
	"WORN",
	"OTHER",
	"TRASH",
	"TRAP",
	"CONTAINER",
	"NOTE",
	"LIQUID CONTAINER",
	"KEY",
	"FOOD",
	"MONEY",
	"PEN",
	"BOAT",
	"\n"
};

const char *wear_bits[] = {
	"TAKE",
	"FINGER",
	"NECK",
	"BODY",
	"HEAD",
	"LEGS",
	"FEET",
	"HANDS",
	"ARMS",
	"SHIELD",
	"ABOUT",
	"WAISTE",
	"WRIST",
	"WIELD",
	"HOLD",
	"THROW",
	"LIGHT-SOURCE",
	"\n"
};

const char *extra_bits[] = {
	"GLOW",
	"HUM",
	"DARK",
	"LOCK",
	"EVIL",
	"INVISIBLE",
	"MAGIC",
	"NODROP",
	"BLESS",
	"ANTI-GOOD",
	"ANTI-EVIL",
	"ANTI-NEUTRAL",
	"\n"
};

const char *room_bits[] = {
	"DARK",
	"DEATH",
	"NO_MOB",
	"INDOORS",
	"LAWFULL",
	"NEUTRAL",
	"CHAOTOC",
	"NO_MAGIC",
	"TUNNEL",
	"PRIVATE",
	"\n"
};

const char *exit_bits[] = {
	"IS-DOOR",
	"CLOSED",
	"LOCKED",
	"\n"
};

const char *sector_types[] = {
	"Inside",
	"City",
	"Field",
	"Forest",
	"Hills",
	"Mountains",
	"Water Swim",
	"Water NoSwim",
	"\n"
};

const char *equipment_types[] = {
	"Special",
	"Worn on right finger",
	"Worn on left finger",
	"First worn around Neck",
	"Second worn around Neck",
	"Worn on body",
	"Worn on head",
	"Worn on legs",
	"Worn on feet",
	"Worn on hands",
	"Worn on arms",
	"Worn as shield",
	"Worn about body",
	"Worn around waiste",
	"Worn around right wrist",
	"Worn around left wrist",
	"Wielded",
	"Held",
	"\n"
};
	
const char *affected_bits[] = 
{	"BLIND",
	"INVISIBLE",
	"DETECT-EVIL",
	"DETECT-INVISIBLE",
	"DETECT-MAGIC",
	"SENCE-LIFE",
	"HOLD",
	"SANCTUARY",
	"GROUP",
	"UNUSED",
	"CURSE",
	"FLAMING-HANDS",
	"POISON",
	"PROTECT-EVIL",
	"PARALYSIS",
	"MORDENS-SWORD",
	"FLAMING-SWORD",
	"SLEEP",
	"DODGE",
	"SNEAK",
	"HIDE",
	"FEAR",
	"CHARM",
	"FOLLOW",
	"SAVED_OBJECTS",
	"\n"
};

const char *apply_types[] = {
	"NONE",
	"STR",
	"DEX",
	"INT",
	"WIS",
	"CON",
	"SEX",
	"CLASS",
	"LEVEL",
	"AGE",
	"CHAR_WEIGHT",
	"CHAR_HEIGHT",
	"MANA",
	"HIT",
	"MOVE",
	"GOLD",
	"EXP",
	"ARMOR",
	"HITROLL",
	"DAMROLL",
	"SAVING_PARA",
	"SAVING_ROD",
	"SAVING_PETRI",
	"SAVING_BREATH",
	"SAVING_SPELL",
	"\n"
};

const char *pc_class_types[] = {
	"UNDEFINED",
	"Scientist",
	"Noble",
	"Assassin",
	"Warrior",
	"\n"
};

const char *npc_class_types[] = {
	"Normal",
	"Undead",
	"\n"
};

const char *action_bits[] = {
	"SPEC",
	"SENTINEL",
	"SCAVENGER",
	"ISNPC",
	"NICE-ASSASSIN",
	"AGGRESSIVE",
	"STAY-ZONE",
	"WIMPY",
	"\n"
};


const char *player_bits[] = {
	"BRIEF",
	"NOSHOUT",
	"COMPACT",
	"DONTSET",
	"NOTELL",
	"NOEMOTE",
	"",
	"FREEZE",
	"\n"
};


const char *position_types[] = {
	"Dead",
	"Mortally wounded",
	"Incapasitated",
	"Stunned",
	"Sleeping",
	"Resting",
	"Sitting",
	"Fighting",
	"Standing",
	"\n"
};

const char *connected_types[]	=	{
	"Playing",
	"Get name",
	"Confirm name",
	"Read Password",
	"Get new password",
	"Confirm new password",
	"Get sex",
	"Read messages of today",
	"Read Menu",
	"Get extra description",
	"Get class",
	"\n"
};

/* [class], [level] (all) */
const int thaco[4][25] = {
	 { 100,20,20,20,19,19,19,18,18,18,17,17,17,16,16,16,15,15,15,14,14,14,13,13,13},
   { 100,20,20,20,18,18,18,16,16,16,14,14,14,12,12,12,10,10,10, 8, 8, 8, 6, 6, 6},
   { 100,20,20,19,19,18,18,17,17,16,16,15,15,14,13,13,12,12,11,11,10,10, 9, 9, 8},
   { 100,20,19,18,17,16,15,14,13,12,11,10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1}
};

/* [ch] strength apply (all) */
const struct str_app_type str_app[31] = {
	{ -5,-4,   0,  0 },  /* 0  */
	{ -5,-4,   3,  1 },  /* 1  */
	{ -3,-2,   3,  2 },
	{ -3,-1,  10,  3 },  /* 3  */
	{ -2,-1,  25,  4 },
	{ -2,-1,  55,  5 },  /* 5  */
	{ -1, 0,  80,  6 },
	{ -1, 0,  90,  7 },
	{  0, 0, 100,  8 },
	{  0, 0, 100,  9 },
	{  0, 0, 115, 10 }, /* 10  */
	{  0, 0, 115, 11 },
	{  0, 0, 140, 12 },
	{  0, 0, 140, 13 },
	{  0, 0, 170, 14 },
	{  0, 0, 170, 15 }, /* 15  */
	{  0, 1, 195, 16 },
	{  1, 1, 220, 18 },
	{  1, 2, 255, 20 }, /* 18  */
	{  3, 7, 640, 40 },
	{  3, 8, 700, 40 }, /* 20  */
	{  4, 9, 810, 40 },
	{  4,10, 970, 40 },
	{  5,11,1130, 40 },
	{  6,12,1440, 40 },
	{  7,14,1750, 40 }, /* 25            */
	{  1, 3, 280, 22 }, /* 18/01-50      */
	{  2, 3, 305, 24 }, /* 18/51-75      */
	{  2, 4, 330, 26 }, /* 18/76-90      */
	{  2, 5, 380, 28 }, /* 18/91-99      */
	{  3, 6, 480, 30 }  /* 18/100   (30) */
};

/* [dex] skill apply (thieves only) */
const struct dex_skill_type dex_app_skill[26] = {
	{-99,-99,-90,-99,-60},   /* 0 */
	{-90,-90,-60,-90,-50},   /* 1 */
	{-80,-80,-40,-80,-45},
	{-70,-70,-30,-70,-40},
	{-60,-60,-30,-60,-35},
	{-50,-50,-20,-50,-30},   /* 5 */
	{-40,-40,-20,-40,-25},
	{-30,-30,-15,-30,-20},
	{-20,-20,-15,-20,-15},
	{-15,-10,-10,-20,-10},
	{-10, -5,-10,-15, -5},   /* 10 */
	{ -5,  0, -5,-10,  0},
	{  0,  0,  0, -5,  0},
	{  0,  0,  0,  0,  0},
	{  0,  0,  0,  0,  0},
	{  0,  0,  0,  0,  0},   /* 15 */
	{  0,  5,  0,  0,  0},
	{  5, 10,  0,  5,  5},
	{ 10, 15,  5, 10, 10},
	{ 15, 20, 10, 15, 15},
	{ 15, 20, 10, 15, 15},   /* 20 */
	{ 20, 25, 10, 15, 20},
	{ 20, 25, 15, 20, 20},
	{ 25, 25, 15, 20, 20},
	{ 25, 30, 15, 25, 25},
	{ 25, 30, 15, 25, 25}    /* 25 */
};

/* [level] backstab multiplyer (thieves only) */
const byte backstab_mult[25] = {
	1,   /* 0 */
	2,   /* 1 */
	2,
	2,
	2,
	3,   /* 5 */
	3,
	3,
	3,
	4,
	4,   /* 10 */
	4,
	4,
	4,
	5,
	5,   /* 15 */
	5,
	5,
	5,
	5,
	5,   /* 20 */
	5,
	5,
	5,
	5    /* 25 */
};

/* [dex] apply (all) */
struct dex_app_type dex_app[26] = {
	{-7,-7, 6},   /* 0 */
	{-6,-6, 5},   /* 1 */
	{-4,-4, 5},
	{-3,-3, 4},
	{-2,-2, 3},
	{-1,-1, 2},   /* 5 */
	{ 0, 0, 1},
	{ 0, 0, 0},
	{ 0, 0, 0},
	{ 0, 0, 0},
	{ 0, 0, 0},   /* 10 */
	{ 0, 0, 0},
	{ 0, 0, 0},
	{ 0, 0, 0},
	{ 0, 0, 0},
	{ 0, 0,-1},   /* 15 */
	{ 1, 1,-2},
	{ 2, 2,-3},
	{ 2, 2,-4},
	{ 3, 3,-4},
	{ 3, 3,-4},   /* 20 */
	{ 4, 4,-5},
	{ 4, 4,-5},
	{ 4, 4,-5},
	{ 5, 5,-6},
	{ 5, 5,-6}    /* 25 */
};

/* [con] apply (all) */
struct con_app_type con_app[26] = {
	{-4,20},   /* 0 */
	{-3,25},   /* 1 */
	{-2,30},
	{-2,35},
	{-1,40},
	{-1,45},   /* 5 */
	{-1,50},
	{ 0,55},
	{ 0,60},
	{ 0,65},
	{ 0,70},   /* 10 */
	{ 0,75},
	{ 0,80},
	{ 0,85},
	{ 0,88},
	{ 1,90},   /* 15 */
	{ 2,95},
	{ 2,97},
	{ 3,99},
	{ 3,99},
	{ 4,99},   /* 20 */
	{ 5,99},
	{ 5,99},
	{ 5,99},
	{ 6,99},
	{ 7,100}   /* 25 */
};

/* [int] apply (all) */
struct int_app_type int_app[26] = {
	3,
	5,    /* 1 */
	7,
	8,
	9,
	10,   /* 5 */
	11,
	12,
	13,
	15,
	17,   /* 10 */
	19,
	22,
	25,
	30,
	35,   /* 15 */
	40,
	45,
	50,
	53,
	55,   /* 20 */
	56,
	60,
	70,
	80,
	99    /* 25 */
};

/* [wis] apply (all) */
struct wis_app_type wis_app[26] = {
	0,   /* 0 */
	0,   /* 1 */
	0,
	0,
	0,
	0,   /* 5 */
	0,
	0,
	0,
	0,
	0,   /* 10 */
	0,
	2,
	2,
	3,
	3,   /* 15 */
	3,
	4,
	5,   /* 18 */
	6,
	6,   /* 20 */
	6,
	6,
	6,
	6,
	6   /* 25 */
};
