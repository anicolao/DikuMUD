/* Create a test player file for integration testing */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <crypt.h>
#include "../dm-dist-alfa/structs.h"
#include "../dm-dist-alfa/utils.h"

/* Helper function to make salt like the server does */
static void make_salt(const char *lsalt, char *salt_buf, size_t bufsize) {
    snprintf(salt_buf, bufsize, "$6$%s$", lsalt);
}

/* Helper function to encrypt password like the server does */
static const char *encrypt_password(const char *pass, const char *salt) {
    struct crypt_data crypted;
    memset(&crypted, 0, sizeof(crypted));
    const char *ret = crypt_r(pass, salt, &crypted);
    if (!ret) {
        perror("password encryption failure");
        return NULL;
    }
    return ret;
}

int main(int argc, char *argv[]) {
    struct char_file_u player;
    FILE *fl;
    char *name, *password;
    int load_room;
    char salt[256];
    char lowercase_name[20];
    
    if (argc < 4) {
        printf("Usage: %s <name> <password> <load_room>\n", argv[0]);
        printf("Example: %s TestChar test 3014\n", argv[0]);
        return 1;
    }
    
    name = argv[1];
    password = argv[2];
    load_room = atoi(argv[3]);
    
    /* Initialize structure to zeros */
    bzero(&player, sizeof(struct char_file_u));
    
    /* Set basic character data */
    player.sex = SEX_MALE;
    player.class = CLASS_WARRIOR;
    player.level = 1;
    player.birth = time(0);
    player.played = 0;
    
    player.weight = 180;
    player.height = 70;
    
    strcpy(player.title, " the Warrior");
    player.hometown = 3001;  /* Lesser Helium */
    strcpy(player.description, "A test character for integration testing.");
    
    /* Set load room - THIS IS THE KEY FIELD */
    player.load_room = load_room;
    
    /* Set abilities */
    player.abilities.str = 16;
    player.abilities.intel = 16;
    player.abilities.wis = 16;
    player.abilities.dex = 16;
    player.abilities.con = 16;
    player.abilities.str_add = 0;
    
    /* Set points */
    player.points.hit = 20;
    player.points.max_hit = 20;
    player.points.mana = 100;
    player.points.max_mana = 100;
    player.points.move = 100;
    player.points.max_move = 100;
    player.points.armor = 100;
    player.points.gold = 100;
    player.points.exp = 0;
    player.points.hitroll = 0;
    player.points.damroll = 0;
    
    /* Set name and password */
    /* Convert name to lowercase */
    memset(lowercase_name, 0, sizeof(lowercase_name));
    for (int i = 0; name[i] && i < sizeof(lowercase_name)-1; i++) {
        lowercase_name[i] = LOWER(name[i]);
        player.name[i] = LOWER(name[i]);
    }
    
    /* Encrypt password using the same method as the server */
    make_salt(lowercase_name, salt, sizeof(salt));
    const char *encrypted = encrypt_password(password, salt);
    if (!encrypted) {
        fprintf(stderr, "Failed to encrypt password\n");
        return 1;
    }
    strncpy(player.pwd, encrypted, sizeof(player.pwd) - 1);
    player.pwd[sizeof(player.pwd) - 1] = '\0';
    
    /* Set conditions (not hungry, not thirsty, not drunk) */
    player.conditions[0] = 24;  /* full */
    player.conditions[1] = 24;  /* not thirsty */
    player.conditions[2] = 0;   /* not drunk */
    
    player.alignment = 0;
    player.last_logon = time(0);
    player.act = 0;
    
    /* Write player file */
    if (!(fl = fopen("lib/players", "wb"))) {
        perror("Failed to create player file");
        return 1;
    }
    
    if (fwrite(&player, sizeof(struct char_file_u), 1, fl) < 1) {
        perror("Failed to write player data");
        fclose(fl);
        return 1;
    }
    
    fclose(fl);
    
    printf("Created test player '%s' with load_room %d\n", name, load_room);
    printf("Player file size: %lu bytes\n", sizeof(struct char_file_u));
    
    return 0;
}
