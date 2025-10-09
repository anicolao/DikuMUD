/* Shop validation utility */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "structs.h"
#include "db.h"
#include "utils.h"

#define SHOP_FILE "tinyworld.shp"
#define MAX_TRADE 5
#define MAX_PROD 6

struct shop_data
{
	int producing[MAX_PROD];/* Which item to produce (virtual)      */
	float profit_buy;       /* Factor to multiply cost with.        */
	float profit_sell;      /* Factor to multiply cost with.        */
	byte type[MAX_TRADE];   /* Which item to trade.                 */
	char *no_such_item1;    /* Message if keeper hasn't got an item */
	char *no_such_item2;    /* Message if player hasn't got an item */
	char *missing_cash1;    /* Message if keeper hasn't got cash    */
	char *missing_cash2;    /* Message if player hasn't got cash    */
	char *do_not_buy;			/* If keeper dosn't buy such things. 	*/
	char *message_buy;      /* Message when player buys item        */
	char *message_sell;     /* Message when player sells item       */
	int temper1;           	/* How does keeper react if no money    */
	int temper2;           	/* How does keeper react when attacked  */
	int keeper;             /* The mobil who owns the shop (virtual)*/
	int with_who;		/* Who does the shop trade with?	*/
	int in_room;		/* Where is the shop?			*/
	int open1,open2;	/* When does the shop open?		*/
	int close1,close2;	/* When does the shop close?		*/
};

extern struct index_data *mob_index;
extern struct index_data *obj_index;
extern struct room_data *world;
extern int top_of_mobt;
extern int top_of_objt;
extern int top_of_world;

struct shop_data *shop_index;
int number_of_shops;

char *fread_string(FILE *fl);
int real_mobile(int virtual);
int real_object(int virtual);
int real_room(int virtual);

void boot_db();

void validate_shops()
{
	char *buf;
	int temp;
	int count;
	FILE *shop_f;
	int shop_nr;
	int errors = 0;
	int warnings = 0;

	if (!(shop_f = fopen(SHOP_FILE, "r")))
	{
		perror("Error opening shop file\n");
		exit(1);
	}

	number_of_shops = 0;
	printf("=== Shop Validation Report ===\n\n");

	for(;;)
	{
		buf = fread_string(shop_f);
		if(*buf == '#')	/* a new shop */
		{
			int shop_num;
			sscanf(buf, "#%d", &shop_num);
			
			if(!number_of_shops)	/* first shop */
				CREATE(shop_index, struct shop_data, 1);
			else
			  if(!(shop_index=
				(struct shop_data*) realloc(
				shop_index,(number_of_shops + 1)*
				sizeof(struct shop_data))))
				{
					perror("Error allocating shop memory\n");
					exit(1);
				}

			printf("Shop #%d:\n", shop_num);

			for(count=0;count<MAX_PROD;count++)
				{
					fscanf(shop_f,"%d \n", &temp);
					if (temp >= 0) {
						int real_obj = real_object(temp);
						shop_index[number_of_shops].producing[count] = real_obj;
						if (real_obj < 0) {
							printf("  ERROR: Producing item vnum %d does not exist!\n", temp);
							errors++;
						} else {
							printf("  Produces: vnum %d (real %d)\n", 
								temp, real_obj);
						}
					}
					else {
						shop_index[number_of_shops].producing[count]= temp;
					}
				}
			
			fscanf(shop_f,"%f \n",
				&shop_index[number_of_shops].profit_buy);
			printf("  Buy markup: %.2f", shop_index[number_of_shops].profit_buy);
			if (shop_index[number_of_shops].profit_buy <= 0.0) {
				printf(" WARNING: Buy markup should be positive!");
				warnings++;
			}
			printf("\n");
			
			fscanf(shop_f,"%f \n",
				&shop_index[number_of_shops].profit_sell);
			printf("  Sell markup: %.2f", shop_index[number_of_shops].profit_sell);
			if (shop_index[number_of_shops].profit_sell <= 0.0) {
				printf(" WARNING: Sell markup should be positive!");
				warnings++;
			}
			printf("\n");
			
			for(count=0;count<MAX_TRADE;count++)
				{
					fscanf(shop_f,"%d \n", &temp);
					shop_index[number_of_shops].type[count] =
					(byte) temp;
					if (temp > 0) {
						printf("  Buys item type: %d\n", temp);
					}
				}
			
			shop_index[number_of_shops].no_such_item1 =
				fread_string(shop_f);
			shop_index[number_of_shops].no_such_item2 =
				fread_string(shop_f);
			shop_index[number_of_shops].do_not_buy =
				fread_string(shop_f);
			shop_index[number_of_shops].missing_cash1 =
				fread_string(shop_f);
			shop_index[number_of_shops].missing_cash2 =
				fread_string(shop_f);
			shop_index[number_of_shops].message_buy =
				fread_string(shop_f);
			shop_index[number_of_shops].message_sell =
				fread_string(shop_f);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].temper1);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].temper2);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].keeper);

			int keeper_vnum = shop_index[number_of_shops].keeper;
			shop_index[number_of_shops].keeper =
			  real_mobile(shop_index[number_of_shops].keeper);

			if (shop_index[number_of_shops].keeper < 0) {
				printf("  ERROR: Keeper mob vnum %d does not exist!\n", keeper_vnum);
				errors++;
			} else {
				printf("  Keeper: vnum %d (real %d)\n", 
					keeper_vnum, shop_index[number_of_shops].keeper);
			}

			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].with_who);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].in_room);
			
			int room_vnum = shop_index[number_of_shops].in_room;
			int real_rm = real_room(room_vnum);
			if (real_rm < 0) {
				printf("  ERROR: Shop room vnum %d does not exist!\n", room_vnum);
				errors++;
			} else {
				printf("  Room: vnum %d (real %d)\n", room_vnum, real_rm);
			}
			
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].open1);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].close1);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].open2);
			fscanf(shop_f,"%d \n",
				&shop_index[number_of_shops].close2);

			printf("  Hours: %d-%d, %d-%d", 
				shop_index[number_of_shops].open1,
				shop_index[number_of_shops].close1,
				shop_index[number_of_shops].open2,
				shop_index[number_of_shops].close2);
			
			/* Validate hours */
			if (shop_index[number_of_shops].open1 < 0 || shop_index[number_of_shops].open1 > 23 ||
			    shop_index[number_of_shops].close1 < 0 || shop_index[number_of_shops].close1 > 23 ||
			    shop_index[number_of_shops].open2 < 0 || shop_index[number_of_shops].open2 > 23 ||
			    shop_index[number_of_shops].close2 < 0 || shop_index[number_of_shops].close2 > 23) {
				printf(" WARNING: Hours should be 0-23");
				warnings++;
			}
			printf("\n");

			/* Check if shop produces nothing */
			int produces_something = 0;
			for(count=0;count<MAX_PROD;count++) {
				if (shop_index[number_of_shops].producing[count] >= 0) {
					produces_something = 1;
					break;
				}
			}
			if (!produces_something) {
				printf("  WARNING: Shop produces nothing (no items for sale)\n");
				warnings++;
			}

			number_of_shops++;
			printf("\n");
		}
		else 
			if(*buf == '$')	/* EOF */
				break;

		free(buf);
	}

	fclose(shop_f);
	
	printf("=== Summary ===\n");
	printf("Total shops: %d\n", number_of_shops);
	printf("Errors: %d\n", errors);
	printf("Warnings: %d\n", warnings);
	
	if (errors > 0) {
		printf("\nValidation FAILED - please fix errors above.\n");
		exit(1);
	} else if (warnings > 0) {
		printf("\nValidation completed with warnings.\n");
	} else {
		printf("\nAll shops validated successfully!\n");
	}
}

int main(int argc, char **argv)
{
	printf("DikuMUD Shop Validation Tool\n\n");
	
	boot_db();
	validate_shops();
	
	return 0;
}
