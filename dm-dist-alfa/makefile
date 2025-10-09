#CFLAGS=-O1 -g -Wall -Werror -Wno-error=deprecated-declarations -Wno-error=implicit-function-declaration -Wno-error=char-subscripts -Wno-unused-but-set-variable -Wno-unused-value -Wno-unused-variable
CFLAGS=-O1 -g -Wno-error=deprecated-declarations -Wno-error=implicit-function-declaration -Wno-error=char-subscripts -Wno-unused-but-set-variable -Wno-unused-value -Wno-unused-variable
# bad ideas
CFLAGS+=-Wno-error=parentheses -Wno-error=return-type -Wno-error=pointer-sign -Wno-error=dangling-else -Wno-error=missing-braces -Wno-error=unused-result -Wno-implicit-function-declaration
# good, optional ideas!
CFLAG+=-fsanitize=address -fno-omit-frame-pointer

LDLIBS=-lcrypt
HEADERFILES = structs.h utils.h comm.h interpreter.h db.h

# Zone files - ordered by zone number
ZONE_ORDER = limbo zone_1200 lesser_helium dead_sea_bottom_channel southern_approach dead_sea_wilderness greater_helium zodanga zodanga_wilderness gathol ptarth gathol_ptarth_wilderness thark_territory atmosphere_factory atmosphere_lower system

# YAML source files
YAML_ZONES = $(foreach zone,$(ZONE_ORDER),lib/zones_yaml/$(zone).yaml)

# Build world data files from YAML zone files
lib/tinyworld.wld: $(YAML_ZONES) ../tools/world_builder.py
	python3 ../tools/world_builder.py build wld $@ $(YAML_ZONES)

lib/tinyworld.mob: $(YAML_ZONES) ../tools/world_builder.py
	python3 ../tools/world_builder.py build mob $@ $(YAML_ZONES)

lib/tinyworld.obj: $(YAML_ZONES) ../tools/world_builder.py
	python3 ../tools/world_builder.py build obj $@ $(YAML_ZONES)

lib/tinyworld.zon: $(YAML_ZONES) ../tools/world_builder.py
	python3 ../tools/world_builder.py build zon $@ $(YAML_ZONES)

lib/tinyworld.shp: $(YAML_ZONES) ../tools/world_builder.py
	python3 ../tools/world_builder.py build shp $@ $(YAML_ZONES)

# Main build targets
all: delplay dmserver worldfiles

worldfiles: lib/tinyworld.wld lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.zon lib/tinyworld.shp

dmserver : comm.o act.comm.o act.informative.o act.movement.o act.obj1.o act.obj2.o act.offensive.o act.other.o act.social.o act.wizard.o handler.o db.o interpreter.o utility.o spec_assign.o shop.o limits.o mobact.o fight.o modify.o weather.o spell_parser.o spells1.o spells2.o reception.o constants.o spec_procs.o signals.o board.o mar_fiz_maz.o magic.o
dmserver : changes.o
	$(CC) $(LDFLAGS) $^ $(LOADLIBES) $(LDLIBS) -o $@

delplay: delplay.o

comm.o : comm.c structs.h utils.h comm.h interpreter.h handler.h db.h
act.comm.o : act.comm.c structs.h utils.h comm.h interpreter.h handler.h \
  db.h spells.h
act.informative.o : act.informative.c structs.h utils.h comm.h \
  interpreter.h handler.h db.h spells.h limits.h
act.movement.o : act.movement.c structs.h utils.h comm.h interpreter.h \
  handler.h db.h spells.h
act.obj1.o : act.obj1.c structs.h utils.h comm.h interpreter.h handler.h \
  db.h spells.h
act.obj2.o : act.obj2.c structs.h utils.h comm.h interpreter.h handler.h \
  db.h spells.h
act.offensive.o : act.offensive.c structs.h utils.h comm.h interpreter.h \
  handler.h db.h spells.h
act.other.o : act.other.c structs.h utils.h comm.h interpreter.h handler.h \
  db.h spells.h
act.social.o : act.social.c structs.h utils.h comm.h interpreter.h \
  handler.h db.h spells.h
act.wizard.o : act.wizard.c structs.h utils.h comm.h interpreter.h \
  handler.h db.h spells.h limits.h
handler.o : handler.c structs.h utils.h db.h
db.o : db.c structs.h utils.h db.h comm.h handler.h
interpreter.o : interpreter.c structs.h comm.h interpreter.h db.h utils.h \
  limits.h
utility.o : utility.c structs.h utils.h
spec_assign.o : spec_assign.c structs.h db.h
spec_procs.o : spec_procs.c structs.h utils.h comm.h interpreter.h \
  handler.h db.h spells.h limits.h
limits.o : limits.c limits.h structs.h utils.h spells.h comm.h
fight.o : fight.c structs.h utils.h comm.h handler.h interpreter.h db.h \
  spells.h
weather.o : weather.c structs.h utils.h comm.h handler.h interpreter.h db.h
shop.o : shop.c structs.h comm.h handler.h db.h interpreter.h utils.h
spells1.o : spells1.c structs.h utils.h comm.h db.h interpreter.h spells.h \
  handler.h
spells2.o : spells2.c structs.h utils.h comm.h db.h interpreter.h spells.h \
  handler.h
magic.o : spells2.c structs.h utils.h comm.h db.h interpreter.h spells.h \
  handler.h
spell_parser.o : spell_parser.c structs.h utils.h comm.h db.h interpreter.h \
  spells.h handler.h
mobact.o : mobact.c utils.h structs.h db.h
modify.o : modify.c structs.h utils.h interpreter.h handler.h db.h comm.h
reception.o : reception.c structs.h comm.h handler.h db.h interpreter.h \
  utils.h spells.h
constants.o : constants.c limits.h structs.h
board.o : board.c structs.h comm.h
list.o : list.c structs.h
signals.o : signals.c utils.h
mar_fiz_maz.o : mar_fiz_maz.c structs.h utils.h comm.h interpreter.h \
  handler.h db.h spells.h limits.h
changes.o : changes.c structs.h utils.h comm.h interpreter.h handler.h \
  db.h spells.h limits.h

delplay.o : delplay.c structs.h

clean:
	rm -f *.o dmserver delplay lib/tinyworld.wld lib/tinyworld.mob lib/tinyworld.obj lib/tinyworld.zon lib/tinyworld.shp
