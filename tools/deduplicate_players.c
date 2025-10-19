/* Deduplicate player file - removes duplicate character entries
 * 
 * This tool fixes player files that have duplicate entries from the bug
 * where characters were saved twice when first created.
 * 
 * Usage: ./deduplicate_players [player_file]
 * 
 * If no argument is provided, defaults to "lib/players"
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "../dm-dist-alfa/structs.h"
#include "../dm-dist-alfa/utils.h"

typedef struct player_entry {
    struct char_file_u data;
    int position;  /* Position in original file */
    struct player_entry *next;
} player_entry_t;

typedef struct player_list {
    char *name;  /* Lowercase name for comparison */
    player_entry_t *entries;  /* Linked list of entries for this player */
    int count;  /* Number of duplicate entries */
    struct player_list *next;
} player_list_t;

/* Convert string to lowercase for comparison */
static void str_tolower(char *dest, const char *src) {
    int i;
    for (i = 0; src[i]; i++) {
        dest[i] = tolower((unsigned char)src[i]);
    }
    dest[i] = '\0';
}

/* Find or create player in list */
static player_list_t* find_or_create_player(player_list_t **head, const char *name) {
    player_list_t *current = *head;
    player_list_t *new_player;
    char lowercase_name[20];
    
    str_tolower(lowercase_name, name);
    
    /* Search for existing player */
    while (current) {
        if (strcmp(current->name, lowercase_name) == 0) {
            return current;
        }
        current = current->next;
    }
    
    /* Create new player entry */
    new_player = (player_list_t*)malloc(sizeof(player_list_t));
    if (!new_player) {
        perror("malloc failed");
        exit(1);
    }
    
    new_player->name = strdup(lowercase_name);
    new_player->entries = NULL;
    new_player->count = 0;
    new_player->next = *head;
    *head = new_player;
    
    return new_player;
}

/* Add entry to player's list */
static void add_entry(player_list_t *player, struct char_file_u *data, int position) {
    player_entry_t *new_entry = (player_entry_t*)malloc(sizeof(player_entry_t));
    if (!new_entry) {
        perror("malloc failed");
        exit(1);
    }
    
    memcpy(&new_entry->data, data, sizeof(struct char_file_u));
    new_entry->position = position;
    new_entry->next = player->entries;
    player->entries = new_entry;
    player->count++;
}

/* Select the best entry for a player (most recent or most progressed) */
static player_entry_t* select_best_entry(player_list_t *player) {
    player_entry_t *current = player->entries;
    player_entry_t *best = current;
    
    if (!current) return NULL;
    
    /* Choose entry with highest level, or if same level, most recent logon */
    while (current) {
        if (current->data.level > best->data.level) {
            best = current;
        } else if (current->data.level == best->data.level) {
            if (current->data.last_logon > best->data.last_logon) {
                best = current;
            }
        }
        current = current->next;
    }
    
    return best;
}

int main(int argc, char *argv[]) {
    FILE *fl;
    struct char_file_u player_data;
    const char *player_file = "lib/players";
    char backup_file[512];
    char output_file[512];
    player_list_t *players = NULL;
    player_list_t *current_player;
    player_entry_t *best_entry;
    int position = 0;
    int total_read = 0;
    int total_duplicates = 0;
    int total_written = 0;
    char *dir_part = NULL;
    char *file_part = NULL;
    
    /* Parse command line arguments */
    if (argc > 1) {
        player_file = argv[1];
    }
    
    /* Construct backup and output filenames based on input file location */
    snprintf(backup_file, sizeof(backup_file), "%s.backup", player_file);
    snprintf(output_file, sizeof(output_file), "%s.dedup", player_file);
    
    printf("==========================================================\n");
    printf("Player File Deduplication Tool\n");
    printf("==========================================================\n\n");
    printf("Reading player file: %s\n", player_file);
    
    /* Open player file for reading */
    fl = fopen(player_file, "rb");
    if (!fl) {
        fprintf(stderr, "Error: Could not open player file '%s'\n", player_file);
        fprintf(stderr, "Make sure you run this from the dm-dist-alfa directory.\n");
        return 1;
    }
    
    /* Read all entries and organize by player name */
    while (fread(&player_data, sizeof(struct char_file_u), 1, fl) == 1) {
        if (player_data.name[0] != '\0') {  /* Valid entry */
            player_list_t *player = find_or_create_player(&players, player_data.name);
            add_entry(player, &player_data, position);
            total_read++;
        }
        position++;
    }
    fclose(fl);
    
    printf("Read %d player entries from file\n\n", total_read);
    
    /* Analyze duplicates */
    printf("Analyzing for duplicates...\n");
    current_player = players;
    while (current_player) {
        if (current_player->count > 1) {
            printf("  Player '%s': %d duplicate entries found\n", 
                   current_player->name, current_player->count);
            total_duplicates += (current_player->count - 1);
        }
        current_player = current_player->next;
    }
    
    if (total_duplicates == 0) {
        printf("\n✓ No duplicates found! Player file is clean.\n");
        printf("==========================================================\n");
        return 0;
    }
    
    printf("\nTotal duplicate entries to remove: %d\n\n", total_duplicates);
    
    /* Create backup of original file */
    printf("Creating backup: %s\n", backup_file);
    {
        FILE *src = fopen(player_file, "rb");
        FILE *dst = fopen(backup_file, "wb");
        char buffer[4096];
        size_t bytes;
        
        if (!src || !dst) {
            fprintf(stderr, "Error: Could not create backup file\n");
            return 1;
        }
        
        while ((bytes = fread(buffer, 1, sizeof(buffer), src)) > 0) {
            fwrite(buffer, 1, bytes, dst);
        }
        
        fclose(src);
        fclose(dst);
    }
    
    /* Write deduplicated file */
    printf("Writing deduplicated file: %s\n", output_file);
    fl = fopen(output_file, "wb");
    if (!fl) {
        fprintf(stderr, "Error: Could not create output file\n");
        return 1;
    }
    
    current_player = players;
    while (current_player) {
        best_entry = select_best_entry(current_player);
        if (best_entry) {
            if (fwrite(&best_entry->data, sizeof(struct char_file_u), 1, fl) != 1) {
                fprintf(stderr, "Error: Failed to write player data\n");
                fclose(fl);
                return 1;
            }
            total_written++;
            
            if (current_player->count > 1) {
                printf("  Kept best entry for '%s' (level %d, last logon: %ld)\n",
                       current_player->name, best_entry->data.level, 
                       best_entry->data.last_logon);
            }
        }
        current_player = current_player->next;
    }
    fclose(fl);
    
    printf("\n");
    printf("==========================================================\n");
    printf("Deduplication Summary:\n");
    printf("==========================================================\n");
    printf("  Original entries:     %d\n", total_read);
    printf("  Duplicates removed:   %d\n", total_duplicates);
    printf("  Final entries:        %d\n", total_written);
    printf("\n");
    printf("Files created:\n");
    printf("  Backup:              %s\n", backup_file);
    printf("  Deduplicated file:   %s\n", output_file);
    printf("\n");
    printf("To apply the changes:\n");
    printf("  1. Stop the MUD server if running\n");
    printf("  2. Run: mv %s %s\n", output_file, player_file);
    printf("  3. Verify the file works correctly\n");
    printf("  4. If everything works, you can delete: %s\n", backup_file);
    printf("\n");
    printf("✓ Deduplication complete!\n");
    printf("==========================================================\n");
    
    /* Free memory */
    while (players) {
        player_list_t *next_player = players->next;
        while (players->entries) {
            player_entry_t *next_entry = players->entries->next;
            free(players->entries);
            players->entries = next_entry;
        }
        free(players->name);
        free(players);
        players = next_player;
    }
    
    return 0;
}
