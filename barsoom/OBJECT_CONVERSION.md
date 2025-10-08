# Object Conversion Summary

This document describes the conversion of all objects in `tinyworld.obj` to Barsoom-themed items appropriate for Lesser Helium.

## Conversion Principles

All objects have been converted following these guidelines:

1. **Setting-Appropriate**: All items are thematically consistent with the Barsoom/John Carter universe
2. **Lesser Helium Focus**: Items are COMMON-frequency items appropriate for Lesser Helium, the starting zone
3. **Functional Equivalence**: Game mechanics remain unchanged; only names and descriptions are modified
4. **Lore Consistency**: Names and descriptions reference OBJECTS.md and TECHS.md documentation

## Category Conversions

### Food and Drink (8 items)

**Before → After**
- Beer barrel → Water barrel (sealed water storage)
- Beer bottle → Water flask (portable water container)
- Dark ale → Wine flask (red wine)
- Firebreather → Strong whiskey (Heliumetic whiskey)
- Local bottle → Local wine flask
- Bread → Martian bread loaf
- Danish pastry → Dried fruit pastry

**Rationale**: Water is precious on Mars. Wine and whiskey are luxury drinks appropriate for a civilized city.

### Weapons (5 items)

**Before → After**
- Dagger → Short dagger
- Small sword → Short sword
- Long sword → Long sword of Helium
- Wooden club → Wooden club
- Warhammer → Heavy mace

**Rationale**: Martian combat emphasizes swords and bladed weapons. Names updated to fit Barsoom conventions while maintaining weapon types.

### Lighting (2 items)

**Before → After**
- Torch → Torch (unchanged - torches still used for signals)
- Lantern → Radium lamp

**Rationale**: Radium lamps are the primary lighting technology in Barsoom, providing perpetual soft illumination.

### Containers (2 items)

**Before → After**
- Bag → Leather bag
- Box → Metal box

**Rationale**: Simple functional items, names clarified for material composition.

### Writing Implements (2 items)

**Before → After**
- Paper note → Parchment note
- Goose-feather quill → Writing stylus

**Rationale**: Metal stylus more appropriate for Martian technology than Earth bird feathers.

### Magic Items → Barsoom Technology (5 items)

**Before → After**
- Scroll of identify → Map scroll
- Yellow potion of see invisible → Sight enhancement potion
- Scroll of recall → Recall scroll (mystical symbols)
- Wand of invisibility → Invisibility device
- Staff of sleep → Sleeping staff

**Rationale**: "Magic" items converted to scientific/technological equivalents or mystical artifacts appropriate to Barsoom.

### Armor → Harnesses (46 items)

All armor pieces converted to Martian harness system:

**Leather Armor (6 items)**
- Jerkin → Leather chest harness
- Cap → Leather helm
- Pants → Leather leg harness
- Boots → Leather boots
- Gloves → Leather gloves
- Sleeves → Leather sleeves

**Studded Leather (6 items)**
- All studded leather items → Studded harness equivalents

**Scale/Chain Mail (12 items)**
- All scale and chain items → Heavy metal harnesses

**Plate Armor (12 items)**
- Bronze plate pieces → Bronze harnesses
- Iron plate pieces → Iron harnesses

**Shields (3 items)**
- Small wooden shield → Small wooden shield
- Small metal shield → Small metal shield
- Large metal shield → Large metal shield

**Rationale**: Martians wear harnesses rather than full armor, with metal components for protection. This maintains game balance while being setting-appropriate.

### Boats → Riding Equipment (2 items)

**Before → After**
- Raft → Thoat saddle
- Canoe → Calot harness

**Rationale**: Mars has dried seas; boats are not needed. Riding equipment for native animals is more appropriate.

### Keys and Security (8 items)

**Before → After**
- Keys (various) → Keys (material names retained)
- Hand cuffs → Shackles

**Rationale**: Security and lock mechanisms are universal; names clarified for materials.

### Furniture and Fixtures (6 items)

**Before → After**
- Desk → Desk
- Safe → Safe (heavy, wall-mounted)
- Bench → Stone bench
- Fountain → Water fountain
- Bulletin board → Bulletin board
- Mailbox → Mailbox

**Rationale**: Functional items largely unchanged, with clarifying descriptions.

### Treasure Items (5 items)

**Before → After**
- Gold coins → Gold coins
- Small pile of gold → Small pile of gold coins
- Amethyst → Amethyst gem
- Silver pendant → Silver pendant
- Silver dagger → Silver dagger

**Rationale**: Precious metals and gems are treasure items in Barsoom; minimal changes needed.

### Drink Dispensers (3 items)

**Before → After**
- Coke machine → Water dispenser
- Can of Coke → Metal water flask

**Rationale**: Anachronistic Earth items converted to water dispensers (critical resource on Mars).

### Tools and Equipment (5 items)

**Before → After**
- Wheelbarrow → Hand cart
- Shovel → Metal shovel
- Rake → Metal rake
- Candlestick → Radium lamp
- Skeleton → Ancient skeleton

**Rationale**: Functional tools with material specifications; candlesticks converted to radium lamps for lighting.

### Special Named Items (4 items)

**Before → After**
- Manxam's heavy mace → Ornate heavy mace
- Manxam's brass breast plate → Brass chest harness
- Manxam's brass leggings → Brass leg harness
- City Key → City key (ceremonial)

**Rationale**: Character names removed; items made generic but retained as special/ornate versions.

### Unique Items

**Before → After**
- Golden armor set (7 pieces) → Golden harness set
- Mithril key → Mithril key
- The pit → The pit (unchanged)
- Ruby talisman → Ruby talisman

**Rationale**: High-value items converted to harness equivalents; rare materials retained.

## Technical Details

### File Modified
- `/dm-dist-alfa/lib/tinyworld.obj`

### Backup Created
- `/dm-dist-alfa/lib/tinyworld.obj.backup`

### Objects Converted
- Total: 124 objects
- Object IDs: #1, #3000-3137, #3300-3323, #3400, #3600-3613

### Testing
- Server compiled successfully
- All objects loaded without errors
- Object file format integrity maintained
- Game mechanics unchanged

## Implementation Notes

1. **Object Numbers**: All original object numbers (vnums) preserved
2. **Object Types**: Item types unchanged (ITEM_WEAPON, ITEM_ARMOR, etc.)
3. **Values**: All value fields preserved (damage, AC, capacities, etc.)
4. **Extra Descriptions**: Preserved where present
5. **Flags**: All flags preserved (wear locations, special properties)

## Future Considerations

These objects are all COMMON items appropriate for Lesser Helium. As additional zones are added:

1. **Valley Dor** - Add Thern religious items, pilgrim wealth
2. **Thark Territory** - Add green Martian equipment, crude weapons
3. **First Born Cities** - Add naval equipment, slave items
4. **Polar Regions** - Add cold weather equipment, yellow Martian items

## References

- `barsoom/summaries/OBJECTS.md` - Comprehensive object catalog
- `barsoom/summaries/TECHS.md` - Technology descriptions
- `barsoom/LESSER_HELIUM.md` - Zone description
- `dm-dist-alfa/doc/values.doc` - Item type documentation
- `dm-dist-alfa/doc/database.doc` - File format documentation
