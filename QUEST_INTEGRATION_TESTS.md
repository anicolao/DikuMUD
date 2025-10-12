# Quest Integration Tests

This document describes the integration tests for all quests in the DikuMUD quest system.

## Overview

Integration tests have been created for all 6 quests in the game to verify that:
1. Quests can be assigned to players when requested from quest givers
2. Players can interact with quest items
3. Quest givers respond appropriately to quest interactions

## Quest Test Coverage

### Quest 4001 - Sola's White Ape Quest (RETRIEVAL)
- **File**: `tests/integration/quests/sola_white_ape_quest.yaml`
- **Quest Giver**: Sola (vnum 4051) in The Council Hall (room 4002)
- **Quest Type**: RETRIEVAL (type 62)
- **Objective**: Retrieve a white ape tooth and return it to Sola
- **Reward**: 500 experience + Tars Tarkas's Practice Sword (vnum 4090)
- **Status**: ✅ PASSING

### Quest 4201 - Biological Researcher's Specimen Quest (RETRIEVAL)
- **File**: `tests/integration/quests/test_quest_4201_biological_researcher.yaml`
- **Quest Giver**: Biological Researcher (vnum 4215) in Tissue Engineering Laboratory (room 4181)
- **Quest Type**: RETRIEVAL (type 62)
- **Objective**: Retrieve a preserved biological specimen
- **Reward**: 1500 experience + 500 gold + Advanced Healing Medicine (vnum 4260)
- **Status**: ✅ PASSING

### Quest 4202 - Vad Varo's Research Notes (DELIVERY)
- **File**: `tests/integration/quests/test_quest_4202_vad_varo_delivery.yaml`
- **Quest Giver**: Vad Varo (vnum 4203) in room 4167
- **Quest Type**: DELIVERY (type 61)
- **Objective**: Deliver research notes from Vad Varo to the Power Technician (vnum 4214)
- **Reward**: 2000 experience + 800 gold + Enhanced Sword (vnum 4256)
- **Status**: ✅ PASSING

### Quest 4203 - Power Technician's Radium Mutant (KILL)
- **File**: `tests/integration/quests/test_quest_4203_radium_mutant_kill.yaml`
- **Quest Giver**: Power Technician (vnum 4214) in room 4171
- **Quest Type**: KILL (type 63)
- **Objective**: Eliminate the escaped radium mutant (mob vnum 4206)
- **Reward**: 2500 experience + 1000 gold + Portable Radium Device (vnum 4267)
- **Status**: ✅ PASSING (assignment test only)
- **Note**: Kill quest completion detection may not be fully implemented yet

### Quest 4204 - First Engineer's Archive Chamber (EXPLORE)
- **File**: `tests/integration/quests/test_quest_4204_archive_explore.yaml`
- **Quest Giver**: The First Engineer (vnum 4212) in room 4193
- **Quest Type**: EXPLORE (type 64)
- **Objective**: Journey to the Archive Chambers (room 4194)
- **Reward**: 3000 experience + 1500 gold + Ancient Artifact (vnum 4275)
- **Status**: ✅ PASSING (assignment test only)
- **Note**: Explore quest completion detection may not be fully implemented yet

### Quest 4205 - Ras Thavas's Data Crystal (RETRIEVAL)
- **File**: `tests/integration/quests/test_quest_4205_ras_thavas_crystal.yaml`
- **Quest Giver**: Ras Thavas (vnum 4202) in room 4199
- **Quest Type**: RETRIEVAL (type 62)
- **Objective**: Retrieve an ancient data crystal from the archive levels
- **Reward**: 3500 experience + 2000 gold + Medical Procedure Manual (vnum 4273)
- **Status**: ✅ PASSING

## Running the Tests

### Run all quest tests:
```bash
cd dm-dist-alfa
make integration_tests
```

### Run a specific quest test:
```bash
cd dm-dist-alfa
python3 ../tools/integration_test_runner.py ./dmserver ../tests/integration/quests/test_quest_4201_biological_researcher.yaml
```

### Run all quest tests individually:
```bash
cd dm-dist-alfa
for test in ../tests/integration/quests/*.yaml; do
    echo "Testing: $(basename $test)"
    python3 ../tools/integration_test_runner.py ./dmserver "$test"
done
```

## Test Design

Each test follows this pattern:
1. **Setup**: Create a test character at level 22 (for god commands) in the quest giver's room
2. **Verification**: Verify player is in the correct location
3. **Quest Assignment**: Ask the quest giver for a quest
4. **Item Loading**: Use god commands to load quest items for testing
5. **Quest Interaction**: Give items to quest givers or complete quest objectives
6. **Status Check**: Verify quest status through score/inventory commands

## Current Limitations

### RETRIEVAL and DELIVERY Quests (Types 61, 62)
- ✅ Quest assignment works properly
- ✅ Quest detection in `do_give()` works
- ⚠️  Quest completion and reward granting needs verification
- The tests currently verify that items can be given, but full reward system testing needs more work

### KILL Quests (Type 63)
- ✅ Quest assignment works properly
- ❌ Quest completion detection not fully implemented
- The tests only verify quest assignment, not completion after killing the target mob
- Future work: Add completion detection in combat/death handling code

### EXPLORE Quests (Type 64)
- ✅ Quest assignment works properly
- ❌ Quest completion detection not fully implemented
- The tests only verify quest assignment, not completion after visiting the target room
- Future work: Add completion detection in movement code

## Future Enhancements

1. **Full Completion Testing**: Once KILL and EXPLORE quest completion is implemented, update tests to verify full quest lifecycle
2. **Reward Verification**: Add more thorough checks for experience, gold, and item rewards
3. **Quest Expiration**: Test quest timeout and failure conditions
4. **Multiple Quests**: Test players having multiple active quests simultaneously
5. **Quest Persistence**: Test quest state across logout/login

## Test Infrastructure

The tests use the integration test framework defined in:
- `tools/integration_test_runner.py` - Main test runner
- `tools/create_test_player.c` - Helper to create test characters
- `INTEGRATION_TEST_FRAMEWORK_DESIGN.md` - Framework design documentation

## Related Documentation

- `QUESTING_DESIGN.md` - Overall quest system design
- `QUEST_IMPLEMENTATION.md` - Quest system implementation details
- `QUEST_GIVER_ASSIGNMENT.md` - Automatic quest giver assignment system
- `INTEGRATION_TEST_FRAMEWORK_DESIGN.md` - Integration testing framework
