#!/usr/bin/env python3
"""
DikuMUD World Builder Tool

This tool handles conversion between DikuMUD legacy format and YAML format,
validates world data, and builds the final tinyworld.* files.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Room:
    """Represents a room in the world."""
    vnum: int
    name: str
    description: str
    zone: int
    room_flags: int
    sector_type: int
    exits: List[Dict[str, Any]] = field(default_factory=list)
    extra_descriptions: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class Mobile:
    """Represents a mobile/NPC."""
    vnum: int
    namelist: str
    short_desc: str
    long_desc: str
    detailed_desc: str
    action_flags: int
    affection_flags: int
    alignment: int
    type: str  # "simple" or "detailed"
    simple: Optional[Dict[str, Any]] = None


@dataclass
class Object:
    """Represents an object/item."""
    vnum: int
    namelist: str
    short_desc: str
    long_desc: str
    action_desc: str
    type_flag: int
    extra_flags: int
    wear_flags: int
    value0: int
    value1: int
    value2: int
    value3: int
    weight: int
    cost: int
    rent: int
    extra_descriptions: List[Dict[str, str]] = field(default_factory=list)
    affects: List[Dict[str, int]] = field(default_factory=list)


@dataclass
class ResetCommand:
    """Represents a zone reset command."""
    command: str
    if_flag: int
    arg1: int
    arg2: int
    arg3: Optional[int] = None
    arg4: Optional[int] = None
    comment: Optional[str] = None


@dataclass
class Zone:
    """Represents a zone with all its data."""
    number: int
    name: str
    top_room: int
    lifespan: int
    reset_mode: int


@dataclass
class ZoneData:
    """Complete zone data including all entities."""
    zone: Zone
    rooms: List[Room] = field(default_factory=list)
    mobiles: List[Mobile] = field(default_factory=list)
    objects: List[Object] = field(default_factory=list)
    resets: List[ResetCommand] = field(default_factory=list)
    shops: List[Dict[str, Any]] = field(default_factory=list)


class DikuMUDParser:
    """Parser for legacy DikuMUD format files."""

    @staticmethod
    def read_string(file) -> str:
        """Read a tilde-terminated string from file."""
        lines = []
        while True:
            line = file.readline()
            if not line:
                raise ValueError("Unexpected EOF while reading string")
            # Check if line ends with ~ (with or without newline)
            if line.rstrip().endswith('~'):
                # Remove the ~ and any trailing whitespace/newline
                last_line = line.rstrip()[:-1]
                if last_line:
                    lines.append(last_line)
                break
            lines.append(line.rstrip('\n'))
        return '\n'.join(lines) if lines else ''

    def parse_rooms(self, filename: str) -> List[Room]:
        """Parse a .wld file and return list of rooms."""
        rooms = []
        
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line or line.startswith('*'):
                    continue
                    
                # Check for EOF marker
                if line.startswith('$'):
                    break
                    
                # Look for room vnum
                if line.startswith('#'):
                    vnum = int(line[1:])
                    
                    # Check if this is just an EOF marker number (like #9000)
                    # by peeking at the next line
                    pos = f.tell()
                    next_line = f.readline().strip()
                    if next_line.startswith('$'):
                        # This is just the EOF marker vnum, not a real room
                        break
                    f.seek(pos)
                    
                    # Read room data
                    name = self.read_string(f)
                    description = self.read_string(f)
                    
                    # Read zone, flags, sector
                    stats_line = f.readline().strip().split()
                    zone = int(stats_line[0])
                    room_flags = int(stats_line[1])
                    sector_type = int(stats_line[2])
                    
                    room = Room(
                        vnum=vnum,
                        name=name,
                        description=description,
                        zone=zone,
                        room_flags=room_flags,
                        sector_type=sector_type
                    )
                    
                    # Read direction blocks and extra descriptions
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        line = line.strip()
                        
                        if line == 'S':
                            break
                        elif line.startswith('D'):
                            direction = int(line[1:])
                            exit_desc = self.read_string(f)
                            keywords = self.read_string(f)
                            exit_line = f.readline().strip().split()
                            door_flag = int(exit_line[0])
                            key_vnum = int(exit_line[1])
                            to_room = int(exit_line[2])
                            
                            room.exits.append({
                                'direction': direction,
                                'description': exit_desc,
                                'keywords': keywords,
                                'door_flag': door_flag,
                                'key_vnum': key_vnum,
                                'to_room': to_room
                            })
                        elif line == 'E':
                            keywords = self.read_string(f)
                            description = self.read_string(f)
                            room.extra_descriptions.append({
                                'keywords': keywords,
                                'description': description
                            })
                    
                    rooms.append(room)
        
        return rooms

    def parse_mobiles(self, filename: str) -> List[Mobile]:
        """Parse a .mob file and return list of mobiles."""
        mobiles = []
        
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line or line.startswith('*'):
                    continue
                    
                if line.startswith('$'):
                    break
                    
                if line.startswith('#'):
                    vnum = int(line[1:])
                    
                    namelist = self.read_string(f)
                    short_desc = self.read_string(f)
                    long_desc = self.read_string(f)
                    detailed_desc = self.read_string(f)
                    
                    flags_line = f.readline().strip().split()
                    action_flags = int(flags_line[0])
                    affection_flags = int(flags_line[1])
                    alignment = int(flags_line[2])
                    type_flag = flags_line[3] if len(flags_line) > 3 else 'S'
                    
                    mob = Mobile(
                        vnum=vnum,
                        namelist=namelist,
                        short_desc=short_desc,
                        long_desc=long_desc,
                        detailed_desc=detailed_desc,
                        action_flags=action_flags,
                        affection_flags=affection_flags,
                        alignment=alignment,
                        type='simple' if type_flag == 'S' else 'detailed'
                    )
                    
                    if type_flag == 'S':
                        # Simple mobile
                        line1 = f.readline().strip().split()
                        line2 = f.readline().strip().split()
                        line3 = f.readline().strip().split()
                        
                        mob.simple = {
                            'level': int(line1[0]),
                            'thac0': int(line1[1]),
                            'ac': int(line1[2]),
                            'hp_dice': line1[3],
                            'damage_dice': line1[4],
                            'gold': int(line2[0]),
                            'experience': int(line2[1]),
                            'position': int(line3[0]),
                            'default_position': int(line3[1]),
                            'sex': int(line3[2])
                        }
                    
                    mobiles.append(mob)
        
        return mobiles

    def parse_objects(self, filename: str) -> List[Object]:
        """Parse a .obj file and return list of objects."""
        objects = []
        
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line or line.startswith('*'):
                    continue
                    
                if line.startswith('$'):
                    break
                    
                if line.startswith('#'):
                    vnum = int(line[1:])
                    
                    namelist = self.read_string(f)
                    short_desc = self.read_string(f)
                    long_desc = self.read_string(f)
                    action_desc = self.read_string(f)
                    
                    type_line = f.readline().strip().split()
                    type_flag = int(type_line[0])
                    extra_flags = int(type_line[1])
                    wear_flags = int(type_line[2])
                    
                    values_line = f.readline().strip().split()
                    value0 = int(values_line[0])
                    value1 = int(values_line[1])
                    value2 = int(values_line[2])
                    value3 = int(values_line[3])
                    
                    weight_line = f.readline().strip().split()
                    weight = int(weight_line[0])
                    cost = int(weight_line[1])
                    rent = int(weight_line[2])
                    
                    obj = Object(
                        vnum=vnum,
                        namelist=namelist,
                        short_desc=short_desc,
                        long_desc=long_desc,
                        action_desc=action_desc,
                        type_flag=type_flag,
                        extra_flags=extra_flags,
                        wear_flags=wear_flags,
                        value0=value0,
                        value1=value1,
                        value2=value2,
                        value3=value3,
                        weight=weight,
                        cost=cost,
                        rent=rent
                    )
                    
                    # Read extra descriptions and affects
                    while True:
                        pos = f.tell()
                        line = f.readline()
                        if not line:
                            break
                        line = line.strip()
                        
                        if line.startswith('#') or line.startswith('$'):
                            f.seek(pos)
                            break
                        elif line == 'E':
                            keywords = self.read_string(f)
                            description = self.read_string(f)
                            obj.extra_descriptions.append({
                                'keywords': keywords,
                                'description': description
                            })
                        elif line == 'A':
                            affect_line = f.readline().strip().split()
                            obj.affects.append({
                                'location': int(affect_line[0]),
                                'modifier': int(affect_line[1])
                            })
                    
                    objects.append(obj)
        
        return objects

    def parse_zone(self, filename: str) -> Tuple[Zone, List[ResetCommand]]:
        """Parse a .zon file and return zone and reset commands."""
        with open(filename, 'r') as f:
            # Read zone header
            while True:
                line = f.readline()
                if not line:
                    raise ValueError("Empty zone file or no zone header found")
                line = line.strip()
                if not line or line.startswith('*'):
                    continue
                if line.startswith('#'):
                    zone_num = int(line[1:])
                    break
            
            zone_name = self.read_string(f)
            
            stats_line = f.readline().strip().split()
            top_room = int(stats_line[0])
            lifespan = int(stats_line[1])
            reset_mode = int(stats_line[2])
            
            zone = Zone(
                number=zone_num,
                name=zone_name,
                top_room=top_room,
                lifespan=lifespan,
                reset_mode=reset_mode
            )
            
            # Read reset commands
            resets = []
            while True:
                line = f.readline()
                if not line:
                    break
                    
                line = line.strip()
                if not line:
                    continue
                    
                if line == 'S' or line.startswith('$'):
                    break
                    
                if line.startswith('*'):
                    # Comment line
                    continue
                    
                parts = line.split()
                if len(parts) < 3:
                    continue
                    
                cmd = parts[0]
                if_flag = int(parts[1])
                arg1 = int(parts[2])
                arg2 = int(parts[3]) if len(parts) > 3 else 0
                arg3 = int(parts[4]) if len(parts) > 4 else None
                arg4 = int(parts[5]) if len(parts) > 5 else None
                
                resets.append(ResetCommand(
                    command=cmd,
                    if_flag=if_flag,
                    arg1=arg1,
                    arg2=arg2,
                    arg3=arg3,
                    arg4=arg4
                ))
        
        return zone, resets


class YAMLConverter:
    """Converts between DikuMUD format and YAML format."""

    def __init__(self, parser: DikuMUDParser):
        self.parser = parser

    def dikumud_to_yaml(self, zone_name: str, input_dir: str, output_file: str):
        """Convert DikuMUD zone files to YAML format."""
        # Parse all files
        rooms = self.parser.parse_rooms(f"{input_dir}/{zone_name}.wld")
        
        # Try to parse mobiles, handle empty files
        try:
            mobiles = self.parser.parse_mobiles(f"{input_dir}/{zone_name}.mob")
        except:
            mobiles = []
        
        # Try to parse objects, handle empty files
        try:
            objects = self.parser.parse_objects(f"{input_dir}/{zone_name}.obj")
        except:
            objects = []
        
        # Try to parse zone, handle empty/missing files
        try:
            zone, resets = self.parser.parse_zone(f"{input_dir}/{zone_name}.zon")
        except:
            # Create a default zone if zone file is empty or missing
            zone = Zone(number=0, name=zone_name, top_room=0, lifespan=0, reset_mode=0)
            resets = []
        
        # Convert to dictionary
        data = {
            'zone': {
                'number': zone.number,
                'name': zone.name,
                'top_room': zone.top_room,
                'lifespan': zone.lifespan,
                'reset_mode': zone.reset_mode
            },
            'rooms': [self._room_to_dict(r) for r in rooms],
            'mobiles': [self._mobile_to_dict(m) for m in mobiles],
            'objects': [self._object_to_dict(o) for o in objects],
            'resets': [self._reset_to_dict(r) for r in resets],
            'shops': []
        }
        
        # Write YAML
        with open(output_file, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def _room_to_dict(self, room: Room) -> dict:
        return {
            'vnum': room.vnum,
            'name': room.name,
            'description': room.description,
            'zone': room.zone,
            'room_flags': room.room_flags,
            'sector_type': room.sector_type,
            'exits': room.exits,
            'extra_descriptions': room.extra_descriptions
        }
    
    def _mobile_to_dict(self, mobile: Mobile) -> dict:
        data = {
            'vnum': mobile.vnum,
            'namelist': mobile.namelist,
            'short_desc': mobile.short_desc,
            'long_desc': mobile.long_desc,
            'detailed_desc': mobile.detailed_desc,
            'action_flags': mobile.action_flags,
            'affection_flags': mobile.affection_flags,
            'alignment': mobile.alignment,
            'type': mobile.type
        }
        if mobile.simple:
            data['simple'] = mobile.simple
        return data
    
    def _object_to_dict(self, obj: Object) -> dict:
        return {
            'vnum': obj.vnum,
            'namelist': obj.namelist,
            'short_desc': obj.short_desc,
            'long_desc': obj.long_desc,
            'action_desc': obj.action_desc,
            'type_flag': obj.type_flag,
            'extra_flags': obj.extra_flags,
            'wear_flags': obj.wear_flags,
            'value0': obj.value0,
            'value1': obj.value1,
            'value2': obj.value2,
            'value3': obj.value3,
            'weight': obj.weight,
            'cost': obj.cost,
            'rent': obj.rent,
            'extra_descriptions': obj.extra_descriptions,
            'affects': obj.affects
        }
    
    def _reset_to_dict(self, reset: ResetCommand) -> dict:
        data = {
            'command': reset.command,
            'if_flag': reset.if_flag,
            'arg1': reset.arg1,
            'arg2': reset.arg2
        }
        if reset.arg3 is not None:
            data['arg3'] = reset.arg3
        if reset.arg4 is not None:
            data['arg4'] = reset.arg4
        if reset.comment:
            data['comment'] = reset.comment
        return data


class WorldBuilder:
    """Builds DikuMUD format files from YAML source."""

    def build_world_file(self, yaml_files: List[str], output_file: str, file_type: str):
        """Build a complete world file from multiple YAML zone files."""
        all_records = []
        
        for yaml_file in yaml_files:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)
            
            if file_type == 'wld':
                records = data.get('rooms', [])
                all_records.extend([(r['vnum'], self._build_room(r)) for r in records])
            elif file_type == 'mob':
                records = data.get('mobiles', [])
                all_records.extend([(m['vnum'], self._build_mobile(m)) for m in records])
            elif file_type == 'obj':
                records = data.get('objects', [])
                all_records.extend([(o['vnum'], self._build_object(o)) for o in records])
            elif file_type == 'zon':
                zone = data.get('zone', {})
                resets = data.get('resets', [])
                all_records.append((zone['number'], self._build_zone(zone, resets)))
            elif file_type == 'shp':
                # Shop files are not yet implemented in YAML
                # For now, just skip them
                pass
        
        # Sort by vnum
        all_records.sort(key=lambda x: x[0])
        
        # Write output
        with open(output_file, 'w') as f:
            if file_type == 'shp':
                # For shop files, just write EOF marker for now
                f.write("$~\n")
            else:
                for _, record_text in all_records:
                    f.write(record_text)
                # Add final EOF marker
                if file_type == 'wld':
                    f.write("#9000\n$~\n")
                else:
                    f.write("$~\n")
    
    def _build_room(self, room: dict) -> str:
        """Build DikuMUD format room record."""
        lines = []
        lines.append(f"#{room['vnum']}")
        lines.append(f"{room['name']}~")
        lines.append(f"{room['description']}")
        lines.append("~")
        lines.append(f"{room['zone']} {room['room_flags']} {room['sector_type']}")
        
        for exit_data in room.get('exits', []):
            lines.append(f"D{exit_data['direction']}")
            lines.append(f"{exit_data['description']}")
            lines.append("~")
            lines.append(f"{exit_data['keywords']}~")
            lines.append(f"{exit_data['door_flag']} {exit_data['key_vnum']} {exit_data['to_room']}")
        
        for extra in room.get('extra_descriptions', []):
            lines.append("E")
            lines.append(f"{extra['keywords']}~")
            lines.append(f"{extra['description']}")
            lines.append("~")
        
        lines.append("S")
        return '\n'.join(lines) + '\n'
    
    def _build_mobile(self, mobile: dict) -> str:
        """Build DikuMUD format mobile record."""
        lines = []
        lines.append(f"#{mobile['vnum']}")
        lines.append(f"{mobile['namelist']}~")
        lines.append(f"{mobile['short_desc']}~")
        lines.append(f"{mobile['long_desc']}")
        lines.append("~")
        lines.append(f"{mobile['detailed_desc']}")
        lines.append("~")
        
        type_flag = 'S' if mobile['type'] == 'simple' else 'D'
        lines.append(f"{mobile['action_flags']} {mobile['affection_flags']} {mobile['alignment']} {type_flag}")
        
        if mobile['type'] == 'simple' and 'simple' in mobile:
            s = mobile['simple']
            lines.append(f"{s['level']} {s['thac0']} {s['ac']} {s['hp_dice']} {s['damage_dice']}")
            lines.append(f"{s['gold']} {s['experience']}")
            lines.append(f"{s['position']} {s['default_position']} {s['sex']}")
        
        lines.append("")
        return '\n'.join(lines) + '\n'
    
    def _build_object(self, obj: dict) -> str:
        """Build DikuMUD format object record."""
        lines = []
        lines.append(f"#{obj['vnum']}")
        lines.append(f"{obj['namelist']}~")
        lines.append(f"{obj['short_desc']}~")
        lines.append(f"{obj['long_desc']}~")
        lines.append(f"{obj['action_desc']}~")
        lines.append(f"{obj['type_flag']} {obj['extra_flags']} {obj['wear_flags']}")
        lines.append(f"{obj['value0']} {obj['value1']} {obj['value2']} {obj['value3']}")
        lines.append(f"{obj['weight']} {obj['cost']} {obj['rent']}")
        
        for extra in obj.get('extra_descriptions', []):
            lines.append("E")
            lines.append(f"{extra['keywords']}~")
            lines.append(f"{extra['description']}")
            lines.append("~")
        
        for affect in obj.get('affects', []):
            lines.append("A")
            lines.append(f"{affect['location']} {affect['modifier']}")
        
        lines.append("")
        return '\n'.join(lines) + '\n'
    
    def _build_zone(self, zone: dict, resets: list) -> str:
        """Build DikuMUD format zone record."""
        lines = []
        lines.append(f"#{zone['number']}")
        lines.append(f"{zone['name']}~")
        lines.append(f"{zone['top_room']} {zone['lifespan']} {zone['reset_mode']}")
        
        for reset in resets:
            cmd_line = f"{reset['command']} {reset['if_flag']} {reset['arg1']} {reset['arg2']}"
            if 'arg3' in reset and reset['arg3'] is not None:
                cmd_line += f" {reset['arg3']}"
            if 'arg4' in reset and reset['arg4'] is not None:
                cmd_line += f" {reset['arg4']}"
            lines.append(cmd_line)
            if 'comment' in reset and reset['comment']:
                lines.append(f"* {reset['comment']}")
        
        lines.append("S")
        return '\n'.join(lines) + '\n'


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  world_builder.py convert <zone_name> <input_dir> <output_yaml>")
        print("  world_builder.py build <file_type> <output_file> <yaml_file1> [yaml_file2 ...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'convert':
        if len(sys.argv) != 5:
            print("Usage: world_builder.py convert <zone_name> <input_dir> <output_yaml>")
            sys.exit(1)
        
        zone_name = sys.argv[2]
        input_dir = sys.argv[3]
        output_yaml = sys.argv[4]
        
        parser = DikuMUDParser()
        converter = YAMLConverter(parser)
        converter.dikumud_to_yaml(zone_name, input_dir, output_yaml)
        print(f"Converted {zone_name} to {output_yaml}")
    
    elif command == 'build':
        if len(sys.argv) < 5:
            print("Usage: world_builder.py build <file_type> <output_file> <yaml_file1> [yaml_file2 ...]")
            sys.exit(1)
        
        file_type = sys.argv[2]
        output_file = sys.argv[3]
        yaml_files = sys.argv[4:]
        
        builder = WorldBuilder()
        builder.build_world_file(yaml_files, output_file, file_type)
        print(f"Built {output_file} from {len(yaml_files)} zone files")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
