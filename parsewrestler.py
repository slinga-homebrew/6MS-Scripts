import sys
import json
from firepro import *

def usage():
    print('parsewrestler.py wrestler.json')
    sys.exit(1)

def main():

    if len(sys.argv) != 2:
        usage()

    with open(sys.argv[1]) as json_file:
        wrestler_struct = json.load(json_file)

    print("===RENAME===")
    print("RENAME_last_name: " + str(wrestler_struct["RENAME_last_name"]))
    print("RENAME_first_name: " + str(wrestler_struct["RENAME_first_name"]))
    print("RENAME_nickname: " + str(wrestler_struct["RENAME_nickname"]))
    print("RENAME_modifier: " + str(wrestler_struct["RENAME_modifier"]))
    print("")

    print("===APPEARANCE===")
    print("APPEARANCE_pose: " + lookupAppearancePose(wrestler_struct["APPEARANCE_pose"]))
    print("APPEARANCE_size: " + lookupAppearanceSize(wrestler_struct["APPEARANCE_size"]))

    for i in range(0, 6):

        appearance_num = "APPEARANCE_" + str(i)

        if appearance_num not in wrestler_struct:
            continue

        appearance = wrestler_struct[appearance_num]

        print("")
        print(appearance_num)
        print("APPEARANCE_head: " + str(appearance["APPEARANCE_head"]))
        print("APPEARANCE_chest: " + lookupAppearanceChest(appearance["APPEARANCE_chest"]))
        print("APPEARANCE_waist: " + lookupAppearanceWaist(appearance["APPEARANCE_waist"]))
        print("APPEARANCE_upper_arm: " + lookupAppearanceUpperArm(appearance["APPEARANCE_upper_arm"]))
        print("APPEARANCE_lower_arm: " + lookupAppearanceLowerArm(appearance["APPEARANCE_lower_arm"]))
        print("APPEARANCE_hand: " + lookupAppearanceHand(appearance["APPEARANCE_hand"]))
        print("APPEARANCE_quad: " + lookupAppearanceQuad(appearance["APPEARANCE_quad"]))
        print("APPEARANCE_shin: " + lookupAppearanceShin(appearance["APPEARANCE_shin"]))
        print("APPEARANCE_feet: " + lookupAppearanceFeet(appearance["APPEARANCE_feet"]))

        # BUGBUG: RGB palettes is missing for builtin wrestlers
        if "APPEARANCE_pal" not in appearance:
            continue

        rgb_list = convertRGBToList(appearance["APPEARANCE_pal"])

        print("APPEARANCE_pal R: ", end="")
        for r,g,b in rgb_list:
            print(str(r).zfill(2) + " ", end="")
        print("")

        print("APPEARANCE_pal G: ", end="")
        for r,g,b in rgb_list:
            print(str(g).zfill(2) + " ", end="")
        print("")

        print("APPEARANCE_pal B: ", end="")
        for r,g,b in rgb_list:
            print(str(b).zfill(2) + " ", end="")
        print("")

    print("")

    print("===CHARACTER===")

    print("CHARACTER_promotion: " + lookupCharacterPromotion(wrestler_struct["CHARACTER_promotion"]))
    print("CHARACTER_division: " + lookupCharacterWeightClass(wrestler_struct["CHARACTER_division"]))
    print("CHARACTER_height: " + str(wrestler_struct["CHARACTER_height"]))
    print("CHARACTER_weight: " + str(wrestler_struct["CHARACTER_weight"]))
    print("CHARACTER_year: " + str(wrestler_struct["CHARACTER_year"]))
    print("CHARACTER_month: " + str(wrestler_struct["CHARACTER_month"]))
    print("CHARACTER_day: " + str(wrestler_struct["CHARACTER_day"]))
    print("CHARACTER_origin: " + lookupCharacterOrigin(wrestler_struct["CHARACTER_origin"]))
    print("CHARACTER_fight_style: " + lookupCharacterFightStyle(wrestler_struct["CHARACTER_fight_style"]))
    print("CHARACTER_defend_style: " + lookupCharacterDefenseStyle(wrestler_struct["CHARACTER_defend_style"]))
    print("CHARACTER_critical: " + lookupCharacterCritical(wrestler_struct["CHARACTER_critical"]))
    print("CHARACTER_recover: " + lookupCharacterRecoveryPower(wrestler_struct["CHARACTER_recover"]))
    print("CHARACTER_recover_bloody: " + lookupCharacterRecoveryPower(wrestler_struct["CHARACTER_recover_bloody"]))
    print("CHARACTER_breath: " + lookupCharacterBreathing(wrestler_struct["CHARACTER_breath"]))
    print("CHARACTER_breath_bloody: " + lookupCharacterBreathing(wrestler_struct["CHARACTER_breath_bloody"]))
    print("CHARACTER_spirit: " + lookupCharacterSpritualPower(wrestler_struct["CHARACTER_spirit"]))
    print("CHARACTER_spirit_bloody: " + lookupCharacterSpritualPower(wrestler_struct["CHARACTER_spirit_bloody"]))
    print("CHARACTER_neck_durability: " + lookupCharacterStamina(wrestler_struct["CHARACTER_neck_durability"]))
    print("CHARACTER_arm_durability: " + lookupCharacterStamina(wrestler_struct["CHARACTER_arm_durability"]))
    print("CHARACTER_waist_durability: " + lookupCharacterStamina(wrestler_struct["CHARACTER_waist_durability"]))
    print("CHARACTER_leg_durability: " + lookupCharacterStamina(wrestler_struct["CHARACTER_leg_durability"]))
    print("CHARACTER_movement_speed: " + lookupCharacterMovementSpeed(wrestler_struct["CHARACTER_movement_speed"]))
    print("CHARACTER_climbing_speed: " + lookupCharacterMovementSpeed(wrestler_struct["CHARACTER_climbing_speed"]))
    print("CHARACTER_climb: " + lookupCharacterClimb(wrestler_struct["CHARACTER_climb"]))
    print("CHARACTER_ring_return: " + str(wrestler_struct["CHARACTER_ring_return"]))
    print("CHARACTER_teamwork: " + lookupCharacterRecoveryPower(wrestler_struct["CHARACTER_teamwork"]))
    print("CHARACTER_song: " + str(wrestler_struct["CHARACTER_song"]))
    print("CHARACTER_voice_type1: " + lookupCharacterVoice(wrestler_struct["CHARACTER_voice_type1"]))
    print("CHARACTER_sound1: " + str(wrestler_struct["CHARACTER_sound1"]))
    print("CHARACTER_voice_type2: " + lookupCharacterVoice(wrestler_struct["CHARACTER_voice_type2"]))
    print("CHARACTER_sound2: " + str(wrestler_struct["CHARACTER_sound2"]))
    print("")

    print("===ATTRIBUTES===")
    print("ATTRIBUTES_offense: ", end="")
    for i in wrestler_struct["ATTRIBUTES_offense"]:
        print(str(int(i)-2).zfill(2) + " ", end="")
    print("")
    print("ATTRIBUTES_defense: ", end="")
    for i in wrestler_struct["ATTRIBUTES_defense"]:
        print(str(int(i)-2).zfill(2) + " ", end="")
    print("")
    print("")

    points = calculateEditPoints(wrestler_struct)
    print("Points: " + str(points) + "/255")

    print("===MOVES===")
    for i in range(0, len(wrestler_struct["MOVES"])):
        if i % 2 != 0:
            continue

        meta = wrestler_struct["MOVES"][i]
        move = wrestler_struct["MOVES"][i+1]

        print("MOVES_" +lookupMoveType(i//2) + ": " + hex(meta) + " " + lookupMove(meta, move))

        if meta & 0x10:
            print("- specialty")
        if meta & 0x20:
            print("- MOVES_finisher: ", end="")

            if "MOVES_finisher" in wrestler_struct:
                print(wrestler_struct["MOVES_finisher"])
            else:
                print("unnamed")

            # BUGBUG: finisher names missing for builtin wrestlers
            # maybe print the default name here then??


        if meta & 0x40:
            print("- sound1")
        if meta & 0x80:
            print("- sound2")
    print("")

    print("===LOGIC===")
    parseLogic(wrestler_struct["LOGIC"])

if __name__ == "__main__":

    if sys.version_info.major < 3:
        print("Python 3 required")
        sys.exit(-1)

    main()


