import sys
import getopt
import json
from firepro import *

# display usage and exit
def usage():
    print('binedit.py --input_1st 1ST.BIN --input_fps FPS.SBL --list_builtins')
    print('binedit.py --input_1st 1ST.BIN --output_1st 1ST.BIN.edited --input_fps FPS.SBL --output_fps FPS.SBL--insert_builtin builtin_0.json')

    print('binedit.py --input_1st 1ST.BIN --list_promotions')
    print('binedit.py --input_1st 1ST.BIN --output_1st 1ST.BIN.edited --insert_promotions promotions.txt')

    print('binedit.py --input_1st 1ST.BIN --list_wrestlers')
    print('binedit.py --input_1st 1ST.BIN --output_1st 1ST.BIN.edited --insert_wrestlers wrestlers.txt')
    sys.exit(0)

# convert JSON wrestler to builtin wrestler struct
def builtinToBytes(parsed_edit):

    #parsed_edit = {}
    pos = 0

    edit = b''

    edit += parsed_edit["CHARACTER_division"].to_bytes(1, 'big')
    edit += parsed_edit["RENAME_modifier"].to_bytes(1, 'big')


    last_name = parsed_edit["RENAME_last_name"].encode(encoding='sjis')
    while len(last_name) < 14:
        last_name = last_name + bytes(1)
    edit += last_name

    first_name = parsed_edit["RENAME_first_name"].encode(encoding='sjis')
    while len(first_name) < 20:
        first_name = first_name + bytes(1)
    edit += first_name

    nickname = parsed_edit["RENAME_nickname"].encode(encoding='sjis')
    while len(nickname) < 26:
        nickname = nickname + bytes(1)
    edit += nickname

    print("CHARACTER_height: " + str(hex(len(edit))))


    edit += parsed_edit["CHARACTER_height"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_weight"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_origin"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_year"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_month"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_day"].to_bytes(1, 'big')

    # BUGBUG: promotions have to match
    parsed_edit["CHARACTER_promotion"] = 0

    edit += parsed_edit["CHARACTER_promotion"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_fight_style"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_defend_style"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_recover"].to_bytes(1, 'big')

    print("CHARACTER_recover: " + str(hex(len(edit))))

    edit += parsed_edit["CHARACTER_recover_bloody"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_breath"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_breath_bloody"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_spirit"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_spirit_bloody"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_neck_durability"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_arm_durability"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_waist_durability"].to_bytes(1, 'big')

    edit += parsed_edit["CHARACTER_leg_durability"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_movement_speed"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_climbing_speed"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_climb"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_critical"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_ring_return"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_teamwork"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_song"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_voice_type1"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_sound1"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_voice_type2"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_sound2"].to_bytes(1, 'big')

    print("sound2: " + str(hex(len(edit))))

    edit += parsed_edit["APPEARANCE_pose"].to_bytes(1, 'big')
    edit += parsed_edit["APPEARANCE_size"].to_bytes(1, 'big')

    print("size: " + str(hex(len(edit))))


    for i in parsed_edit["ATTRIBUTES_offense"]:
        edit += i.to_bytes(1, 'big')

    for i in parsed_edit["ATTRIBUTES_defense"]:
        edit += i.to_bytes(1, 'big')

    print("defense: " + str(hex(len(edit))))

    for i in parsed_edit["MOVES"]:
        edit += i.to_bytes(1, 'big')

    print("moves: " + str(hex(len(edit))))

    parsed_edit["LOGIC"] = parsed_edit["LOGIC"][0:0x8e]

    for i in parsed_edit["LOGIC"]:
        edit += i.to_bytes(1, 'big')

    print("logic: " + str(hex(len(edit))))

    for i in range(0, 6):

        if "APPEARANCE_0" not in parsed_edit:
            print("Missing APPEARANCE_0!!")
            sys.exit(-1)

        appearance_num = "APPEARANCE_" + str(i)

        if appearance_num not in parsed_edit:
            appearance_num = "APPEARANCE_0"

        appearance = parsed_edit[appearance_num]

        edit += appearance["APPEARANCE_head"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_chest"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_waist"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_upper_arm"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_lower_arm"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_shin"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_quad"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_hand"].to_bytes(1, 'big')
        edit += appearance["APPEARANCE_feet"].to_bytes(1, 'big')

    while len(edit) != BUILTIN_WRESTLER_SIZE:
        edit += bytes(1)

    if len(edit) != BUILTIN_WRESTLER_SIZE:
        print ("Edit size is wrong!! " + str(hex(len(edit))) + " " + hex(BUILTIN_WRESTLER_SIZE))
        return None

    return edit

def insert_builtin(inBuf, builtinFilename):

    builtinFile = open(builtinFilename, "r")
    builtinBuf = builtinFile.read()
    builtinFile.close()

    builtin_struct = json.loads(builtinBuf)

    builtin = builtinToBytes(builtin_struct)

    pos = BUILTIN_WRESTLER_OFFSET

    outBuf = inBuf[0:BUILTIN_WRESTLER_OFFSET]
    outBuf += builtin
    outBuf += inBuf[BUILTIN_WRESTLER_OFFSET + BUILTIN_WRESTLER_SIZE:]

    return outBuf

# queries the builtin wrestlers palette from FPS.SBL
# wrestlerNum = 0-159 matching the wrestler number from edit a wrestler
# attireNum = 0-5, where 5 is equal to the 'A' button outfit for the wrestler
def get_builtin_palette(fpsBuffer, wrestlerNum, attireNum):

    # only valid for wrestlers 0-159


    # how many RGB entries each pallete component is
    # they should total to 34 entries or 68 bytes
    palette_component_sizes = [4, 3, 3, 3, 3, 3, 5, 3, 3, 4]

    # types > 0xff are treated differently
    pallete_component_type = [0x001c, 0x009c, 0x00d2, 0x0131, 0x00dc, 0x00be, 0x00c5, 0x006b, 0x0077, 0x0062]

    pallete_component_index = [0x0020, 0x0200, 0x03e0, 0x05c0, 0x0980, 0x0b60, 0x0d40, 0x0f20, 0x1100, 0x12e0]


    # some offset into another table???
    pallete_component_offset = [0x14c0, 0x1530, 0x1704, 0x197a, 0x1d0d, 0x1fa1, 0x21db, 0x25b4, 0x26f5, 0x285a, 0x29e2]

    wrestlerIndex = (wrestlerNum * 6) + attireNum
    #print(hex(wrestlerIndex))

    pal = b'';

    for i in range(0, 10):

        if 0xFF < pallete_component_type[i]:

            wrestlerIndex_partIndex = pallete_component_index[i]*2 + wrestlerIndex*2
            wrestlerIndex_partIndex = (fpsBuffer[wrestlerIndex_partIndex]*256) + fpsBuffer[wrestlerIndex_partIndex+1]

        else:

            wrestlerIndex_partIndex = pallete_component_index[i]*2 + wrestlerIndex
            wrestlerIndex_partIndex = fpsBuffer[wrestlerIndex_partIndex]

        src_offset = (wrestlerIndex_partIndex*2*palette_component_sizes[i]) + (pallete_component_offset[i]*2)


        for j in range(0, palette_component_sizes[i] * 2):

                pal += fpsBuffer[src_offset + j].to_bytes(1, 'big')

    if len(pal) != 68:
        print("Error computing wrestler palette!!")
        return None

    return pal


# parse builtin struct to JSON wrestler
def parse_builtin(wrestlerNum, builtin, fpsBuf):
    wrestler_struct = {}

    #
    # struct PREBUILT_WRESTLER
    #

    # offset 0
    pos = 0

    wrestler_struct["CHARACTER_division"] = builtin[pos]
    pos += 1
    wrestler_struct["RENAME_modifier"] = builtin[pos]
    pos += 1

    # wrestler name
    wrestler_struct["RENAME_last_name"] = builtin[pos: pos + 14].decode(encoding='sjis')
    pos += 14

    wrestler_struct["RENAME_first_name"] = builtin[pos: pos + 20].decode(encoding='sjis')
    pos += 20
    wrestler_struct["RENAME_nickname"] = builtin[pos: pos + 26].decode(encoding='sjis')
    pos += 26

    wrestler_struct["CHARACTER_height"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_weight"] = builtin[pos]
    pos += 1

    # offset 0x40
    if pos != 0x40:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["CHARACTER_origin"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_year"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_month"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_day"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_promotion"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_fight_style"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_defend_style"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_recover"] = builtin[pos]
    pos += 1

    # offset 0x48
    if pos != 0x48:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["CHARACTER_recover_bloody"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_breath"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_breath_bloody"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_spirit"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_spirit_bloody"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_neck_durability"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_arm_durability"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_waist_durability"] = builtin[pos]
    pos += 1

    # offset 0x50
    if pos != 0x50:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["CHARACTER_leg_durability"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_movement_speed"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_climbing_speed"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_climb"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_critical"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_ring_return"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_teamwork"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_song"] = builtin[pos]
    pos += 1

    # offset 0x58
    if pos != 0x58:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["CHARACTER_voice_type1"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_sound1"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_voice_type2"] = builtin[pos]
    pos += 1
    wrestler_struct["CHARACTER_sound2"] = builtin[pos]
    pos += 1
    wrestler_struct["APPEARANCE_pose"] = builtin[pos]
    pos += 1
    wrestler_struct["APPEARANCE_size"] = builtin[pos]
    pos += 1

    # offset 0x5e
    if pos != 0x5e:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["ATTRIBUTES_offense"] = list(builtin[pos:pos+10])
    pos += 10
    wrestler_struct["ATTRIBUTES_defense"] = list(builtin[pos:pos+10])
    pos += 10

    # offset 0x72
    if pos != 0x72:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["MOVES"] = list(builtin[pos:pos+112])
    pos += 112

    # offset 0xe2
    if pos != 0xe2:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    wrestler_struct["LOGIC"] = list(builtin[pos:pos+0x8e])
    pos += 0x8e

    # offset 0x170
    if pos != 0x170:
        print("Pos is wrong!! " + str(hex(pos)))
        sys.exit(-1)

    for i in range(0, 6):

        appearance_num = "APPEARANCE_" + str(i)

        wrestler_struct[appearance_num] = {}

        wrestler_struct[appearance_num]["APPEARANCE_head"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_chest"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_waist"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_upper_arm"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_lower_arm"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_shin"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_quad"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_hand"] = builtin[pos]
        pos += 1
        wrestler_struct[appearance_num]["APPEARANCE_feet"] = builtin[pos]
        pos += 1

        # the wrestler palette is stored in FPS.SBL
        pal = get_builtin_palette(fpsBuf, wrestlerNum, i)
        wrestler_struct[appearance_num]["APPEARANCE_pal"] = list(pal)

    unused = builtin[pos:]

    if areAllElementsZero(unused) != True:
        print("error unused bytes are not all zero!!")
        print(unused)
        sys.exit(-1)

    return wrestler_struct

# list all of the builtin wrestlers in 1ST.BIN
# FPS.SBL contains the wrestler palettes
def list_builtins(inBuf, inFpsBuf):

    fpsBuf = inFpsBuf[FPS_SBL_OFFSET:]

    for i in range(0, NUM_BUILTIN_WRESTLERS):

        pos = BUILTIN_WRESTLER_OFFSET + (i * BUILTIN_WRESTLER_SIZE)

        builtin = parse_builtin(i, inBuf[pos:pos + BUILTIN_WRESTLER_SIZE], fpsBuf)

        print("Builtin slot: " + str(i))
        print("RENAME_last_name: " + str(builtin["RENAME_last_name"]))
        print("RENAME_first_name: " + str(builtin["RENAME_first_name"]))
        print("RENAME_nickname: " + str(builtin["RENAME_nickname"]))

        outFilename = "builtin_" + str(i) + ".json"
        outFile = open(outFilename, "w")
        outFile.write(json.dumps(builtin))

        print("Wrote " + outFilename)
        print("")

# list all of the promotions in 1ST.BIN
def list_promotions(inBuf):

    for i in range(0, NUM_PROMOTIONS):

        pos = BUILTIN_PROMOTION_OFFSET + (i * PROMOTION_NAME_SIZE)
        full_name = inBuf[pos:pos+PROMOTION_NAME_SIZE].decode(encoding='shift-jis').rstrip('\x00')

        pos = BUILTIN_PROMOTION_SHORT_OFFSET + (i * PROMOTION_SHORT_NAME_SIZE)
        short_name = inBuf[pos:pos+PROMOTION_SHORT_NAME_SIZE].decode(encoding='shift-jis').rstrip('\x00')

        seperator = ","

        print(full_name + str(seperator) + short_name)

# inject a list of promotions into 1ST.BIN
def insert_promotions(inBuf, promotionsFilename):

    promotion_names = b''
    promotion_short_names = b''

    promotionsFile = open(promotionsFilename, "r", encoding='utf-8')
    promotionsBuf = promotionsFile.readlines()

    for l in promotionsBuf:
        l = l.strip()
        l = l.split(",")

        full_name = l[0].encode(encoding="shift-jis")
        short_name = l[1].encode(encoding="shift-jis")

        while len(full_name) < PROMOTION_NAME_SIZE:
            full_name += bytes([0])

        if len(full_name) > PROMOTION_NAME_SIZE:
            print("Promotion full name " + l[0] + " is greater than 24 bytes")
            sys.exit(-1)

        while len(short_name) < PROMOTION_SHORT_NAME_SIZE:
            short_name += bytes([0])

        if len(short_name) > PROMOTION_SHORT_NAME_SIZE:
            print("Promotion short name " + l[1] + " is greater than 12 bytes")
            sys.exit(-1)

        promotion_names += full_name
        promotion_short_names += short_name

    if len(promotion_names) != NUM_PROMOTIONS * PROMOTION_NAME_SIZE:
        print("Promotion data length is wrong!!")
        sys.exit(-1)

    if len(promotion_short_names) != NUM_PROMOTIONS * PROMOTION_SHORT_NAME_SIZE:
        print("Promotion data length is wrong!!")
        sys.exit(-1)

    # create the output data
    pos = BUILTIN_PROMOTION_OFFSET
    outBuf = inBuf[0:BUILTIN_PROMOTION_OFFSET]

    outBuf += promotion_names
    pos += len(promotion_names)

    outBuf += inBuf[pos:BUILTIN_PROMOTION_SHORT_OFFSET]
    outBuf += promotion_short_names

    pos = BUILTIN_PROMOTION_SHORT_OFFSET + len(promotion_short_names)
    outBuf += inBuf[pos:]

    return outBuf

# list all of the wrestler names in 1ST.BIN
def list_wrestlers(inBuf):

    for i in range(0, NUM_BUILTIN_WRESTLERS):

        pos = BUILTIN_WRESTLER_OFFSET + (i * BUILTIN_WRESTLER_SIZE) + 1
        wrestlers = inBuf[pos:pos + BUILTIN_WRESTLER_NAME_SIZE]

        rename_modifier = wrestlers[0]
        if rename_modifier & 0x80:
            swap_order = 1
        else:
            swap_order = 0

        rename_modifier = rename_modifier & 0x7f

        first_name = wrestlers[1:13].decode(encoding='shift-jis').rstrip('\x00')
        last_name = wrestlers[13:31].decode(encoding='shift-jis').rstrip('\x00')
        nick_name = wrestlers[31:55].decode(encoding='shift-jis').rstrip('\x00')
        seperator = ","

        print(str(swap_order) + seperator + str(rename_modifier) + seperator + first_name + seperator + last_name + seperator + nick_name)

# insert a list of wrestler names in 1ST.BIN
def insert_wrestlers(inBuf, wrestlersFilename):

    wrestlersList = []

    wrestlersFile = open(wrestlersFilename, "r", encoding='utf-8')
    wrestlersBuf = wrestlersFile.readlines()

    for l in wrestlersBuf:
        l = l.strip()
        l = l.split(",")

        data = b''

        swap_order = int(l[0])
        rename_modifier = int(l[1])
        first_name = l[2].encode(encoding="shift-jis")
        last_name = l[3].encode(encoding="shift-jis")
        nick_name = l[4].encode(encoding="shift-jis")

        if swap_order != 0 and swap_order != 1:
            print("Invalid swap order!! Must be 0 or 1: " + str(swap_order))
            sys.exit(-1)

        if rename_modifier < 0 and rename_modifier > 3:
            print("Invalid rename modifier!! Must be 0-3: " + str(rename_modifier))
            sys.exit(-1)

        if swap_order == 1:
            rename_modifier = rename_modifier | 0x80

        FIRST_NAME_SIZE = 14
        LAST_NAME_SIZE = 20
        NICK_NAME_SIZE = 26

        while len(first_name) < FIRST_NAME_SIZE:
            first_name += bytes([0])

        if len(first_name) > FIRST_NAME_SIZE:
            print("wrestler first name " + l[2] + " is greater than 12 bytes")
            sys.exit(-1)

        while len(last_name) < LAST_NAME_SIZE:
            last_name += bytes([0])

        if len(last_name) > LAST_NAME_SIZE:
            print("Wrestler last name " + l[3] + " is greater than 18 bytes")
            sys.exit(-1)

        while len(nick_name) < NICK_NAME_SIZE:
            nick_name += bytes([0])

        if len(nick_name) > NICK_NAME_SIZE:
            print("Wrestler last name " + l[4] + " is greater than 18 bytes")
            sys.exit(-1)

        data += rename_modifier.to_bytes(1, byteorder='big')
        data += first_name;
        data += last_name;
        data += nick_name;

        if len(data) != BUILTIN_WRESTLER_NAME_SIZE:
            print(len(data))
            print("Wrestler name size is wrong!!")
            return None

        wrestlersList.append(data)

    if len(wrestlersList) != NUM_BUILTIN_WRESTLERS:
        print(str(NUM_BUILTIN_WRESTLERS * BUILTIN_WRESTLER_NAME_SIZE))
        print("Rename wrestlers count is wrong!!")
        print(len(data))
        sys.exit(-1)

    # Now that we have the data, inject it into inBuf
    outBuf = inBuf[0:BUILTIN_WRESTLER_OFFSET]

    for i in range(0, len(wrestlersList)):

        pos = BUILTIN_WRESTLER_OFFSET + (i * BUILTIN_WRESTLER_SIZE)

        wrestlerName = inBuf[pos:pos + 1] + wrestlersList[i] + inBuf[pos + len(wrestlersList[i]) + 1:pos + BUILTIN_WRESTLER_SIZE]

        outBuf += wrestlerName

    outBuf += inBuf[BUILTIN_WRESTLER_OFFSET + (BUILTIN_WRESTLER_SIZE * NUM_BUILTIN_WRESTLERS):]

    return outBuf

def main(argv):

    inBinFile = ""
    outBinFile = ""
    inBinBuf = b''
    outBinBuf = b''
    inFpsFile = b''
    inFpsBuf = b''

    listPromotions = False
    insertPromotions = False
    inPromotionsFile = ""

    listWrestlers = False
    insertWrestlers = False
    inWrestlersFile = ""

    listBuiltins = False
    insertBuiltin = False
    inBuiltinFile = ""

    try:
      opts, args = getopt.getopt(argv,"hi:o:",["input_1st=","output_1st=", "input_fps=","output_fps=", "list_builtins", "list_promotions", "list_wrestlers", "insert_builtin=", "insert_promotions=", "insert_wrestlers="])
    except getopt.GetoptError:
      usage()

    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--input_1st"):
            inBinFile = arg
        elif opt in ("-o", "--output_1st"):
            outBinFile = arg
        elif opt in ("-i", "--input_fps"):
            inFpsFile = arg
        elif opt in ("-o", "--output_fps"):
            outFpsFile = arg
        elif opt in ("--list_builtins"):
            listBuiltins = True
        elif opt in ("--insert_builtin"):
            insertBuiltin = True
            inBuiltinFile = arg
        elif opt in ("--list_promotions"):
            listPromotions = True
        elif opt in ("--insert_promotions"):
            insertPromotions = True
            inPromotionsFile = arg
        elif opt in ("--list_wrestlers"):
            listWrestlers = True
        elif opt in ("--insert_wrestlers"):
            insertWrestlers = True
            inWrestlersFile = arg

    if len(inBinFile) == 0:
        print("--input_1st required!!");
        usage()
    else:
        # read 1ST.BIN
        inFile = open(inBinFile, "rb")
        inBinBuf = inFile.read()
        inFile.close()

    if len(inFpsFile) != 0:
        # read FPS.SBL
        inFile = open(inFpsFile, "rb")
        inFpsBuf = inFile.read()
        inFile.close()

    if listBuiltins == True:

        if len(inFpsBuf) == 0:
            print("--input_fps required!!");
            usage()

        list_builtins(inBinBuf, inFpsBuf)
        sys.exit(0)

    if listPromotions == True:
        list_promotions(inBinBuf)
        sys.exit(0)

    if listWrestlers == True:
        list_wrestlers(inBinBuf)
        sys.exit(0)

    if insertBuiltin == True:

        if len(outBinFile) == 0:
            usage()

        inBinBuf = insert_builtin(inBinBuf, inBuiltinFile)

    if insertPromotions == True:

        if len(outBinFile) == 0:
            usage()

        inBinBuf = insert_promotions(inBinBuf, inPromotionsFile)

    if insertWrestlers == True:

        if len(outBinFile) == 0:
            usage()

        inBinBuf = insert_wrestlers(inBinBuf, inWrestlersFile)

    if outBinFile != "":
        # write the output file
        outFile = open(outBinFile, "wb")
        outFile.write(inBinBuf)
        outFile.close()

    return 0

if __name__ == "__main__":
    requirePython3()
    main(sys.argv[1:])
