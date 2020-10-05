import sys
import getopt
import binascii
import json
from firepro import *

def usage():
    print('saveedit.py --input_save FPS_6MEN._01 --list_edits')
    print('saveedit.py --input_save FPS_6MEN._01 --output_save FPS_6MEN._01.edited --insert_edit edit_1.json --edit_slot 1 --appearance_number 0')
    print('')

    print('saveedit.py --input_save FPS_6MEN._01 --list_promotions')
    print('saveedit.py --input_save FPS_6MEN._01 --output_save FPS_6MEN._01.edited --insert_promotions promotions.txt')
    print('')

    print('saveedit.py --input_save FPS_6MEN._01 --list_wrestlers')
    print('saveedit.py --input_save FPS_6MEN._01 --output_save FPS_6MEN._01.edited --insert_wrestlers wrestlers.txt')

    sys.exit(1)

def editToBytes(parsed_edit, appearance_number):

    if appearance_number < 0 or appearance_number > 5:
        print("Invalid appearance number specified!! Must be 1-5")
        sys.exit(-1)

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

    edit += parsed_edit["CHARACTER_height"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_weight"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_origin"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_year"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_month"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_day"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_promotion"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_fight_style"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_defend_style"].to_bytes(1, 'big')
    edit += parsed_edit["CHARACTER_recover"].to_bytes(1, 'big')

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

    edit += parsed_edit["APPEARANCE_pose"].to_bytes(1, 'big')
    edit += parsed_edit["APPEARANCE_size"].to_bytes(1, 'big')

    for i in parsed_edit["ATTRIBUTES_offense"]:
        edit += i.to_bytes(1, 'big')

    for i in parsed_edit["ATTRIBUTES_defense"]:
        edit += i.to_bytes(1, 'big')

    for i in parsed_edit["MOVES"]:
        edit += i.to_bytes(1, 'big')

    for i in parsed_edit["LOGIC"]:
        edit += i.to_bytes(1, 'big')

    # not sure what these two bytes are for
    # the first byte always appears to be zero
    # the second byte varies possibly related to number
    # of unlock points available?
    edit += b'\x00'
    edit += b'\xFF'

    # builtins have 0-5 appearances
    # edits only have one
    # Allow the user to specify at the command line if there are more than one appearances in the JSON file
    appearance_num = "APPEARANCE_" + str(appearance_number)
    appearance = parsed_edit[appearance_num]

    if "APPEARANCE_pal" in appearance:
        for i in appearance["APPEARANCE_pal"]:
            edit += i.to_bytes(1, 'big')
    else:
        print("APPEARANCE_pal not found!!")
        sys.exit(-1)

        # BUGBUG: no rgb values, just put 0
        edit += bytes(68)

    if "MOVES_finisher" in parsed_edit:

        finisher = parsed_edit["MOVES_finisher"].encode(encoding='sjis')

        while len(finisher) < 42:
            finisher = finisher + bytes(1)

        edit += finisher

    else:
        #print("MOVES_finisher not found!!")
        #sys.exit(-1)

        # BUGBUG: no rgb values, just put 0
        edit += bytes(42)

    edit += appearance["APPEARANCE_head"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_chest"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_waist"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_upper_arm"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_lower_arm"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_shin"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_quad"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_hand"].to_bytes(1, 'big')
    edit += appearance["APPEARANCE_feet"].to_bytes(1, 'big')

    while len(edit) != EDIT_SIZE:
        edit += bytes(1)

    if len(edit) != EDIT_SIZE:
        print ("Edit size is wrong!! " + str(hex(len(edit))) + " " + hex(EDIT_SIZE))
        return None

    return edit

def insert_edit(inBuf, editFilename, editSlot, appearanceNumber, saveType):

    if saveType == SAVE_INTERNAL:
        numEdits = NUM_EDITS_SAVE_INTERNAL
    elif saveType == SAVE_CART:
        numEdits = NUM_EDITS_SAVE_CART

    if editSlot < 1 or editSlot > numEdits:
        print("Invalid edit slot number!! Must be 1-" + str(numEdits))
        sys.exit(-1)

    if appearanceNumber < 0 or appearanceNumber > 5:
        print("Invalid appearance number specified!! Must be 1-5")
        sys.exit(-1)

    editFile = open(editFilename, "r")
    editBuf = editFile.read()
    editFile.close()

    edit_struct = json.loads(editBuf)

    edit = editToBytes(edit_struct, appearanceNumber)

    # header
    outBuf = inBuf[0:MAGIC_SIZE]

    # is edit present flags
    for i in range(0, numEdits):

        if i + 1 == editSlot:
            # this is the wrestler we are inserting, make sure the bit is set to 1
            temp = 1
            outBuf += temp.to_bytes(1, "big")
        else:
            # not our edit, copy over the existing one
            outBuf += inBuf[MAGIC_SIZE + i].to_bytes(1, "big")

    # the actual edit
    for i in range(0, numEdits):

        if i + 1 == editSlot:
            # this is the wrestler we are inserting
            temp = 1
            outBuf += edit
        else:
            # not our edit, copy over the existing one
            outBuf += inBuf[MAGIC_SIZE + numEdits + (i*EDIT_SIZE):MAGIC_SIZE + numEdits + (i*EDIT_SIZE) + EDIT_SIZE]

    outBuf += inBuf[MAGIC_SIZE + numEdits + (numEdits*EDIT_SIZE):]

    return outBuf

def parseEdit(edit):

    parsed_edit = {}
    pos = 0

    if len(edit) != EDIT_SIZE:
        print ("Edit size is wrong!! " + str(len(edit)))
        return None

    parsed_edit["CHARACTER_division"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit["RENAME_modifier"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit["RENAME_last_name"] = edit[pos:pos+14].decode(encoding='sjis').rstrip('\x00')
    pos += 14

    parsed_edit["RENAME_first_name"] = edit[pos:pos+20].decode(encoding='sjis').rstrip('\x00')
    pos += 20

    parsed_edit["RENAME_nickname"] = edit[pos:pos+26].decode(encoding='sjis').rstrip('\x00')
    pos += 26

    # character
    parsed_edit["CHARACTER_height"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_weight"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_origin"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_year"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_month"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_day"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_promotion"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_fight_style"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_defend_style"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_recover"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_recover_bloody"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_breath"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_breath_bloody"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_spirit"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_spirit_bloody"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_neck_durability"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_arm_durability"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_waist_durability"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_leg_durability"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_movement_speed"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_climbing_speed"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_climb"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_critical"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_ring_return"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_teamwork"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_song"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_voice_type1"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_sound1"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_voice_type2"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["CHARACTER_sound2"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit["APPEARANCE_pose"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1
    parsed_edit["APPEARANCE_size"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit["ATTRIBUTES_offense"] = list(edit[pos:pos+10])
    pos += 10
    parsed_edit["ATTRIBUTES_defense"] = list(edit[pos:pos+10])
    pos += 10

    parsed_edit["MOVES"] = list(edit[pos:pos+112])
    pos += 112

    parsed_edit["LOGIC"] = list(edit[pos:pos+142])
    pos += 142

    # not sure what these two bytes are for
    # the first byte always appears to be zero
    # the second byte varies possibly related to number
    # of unlock points available?
    unknown1 = edit[pos]
    pos += 1

    unknown2 = edit[pos]
    pos += 1

    appearance_num = "APPEARANCE_0"
    parsed_edit[appearance_num] = {}

    parsed_edit[appearance_num]["APPEARANCE_pal"] = list(edit[pos:pos+68])
    pos += 68

    parsed_edit["MOVES_finisher"] = edit[pos:pos+42].decode(encoding='sjis').rstrip('\x00')
    pos += 42

    parsed_edit[appearance_num]["APPEARANCE_head"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_chest"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_waist"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_upper_arm"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_lower_arm"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_shin"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_quad"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_hand"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit[appearance_num]["APPEARANCE_feet"] = int.from_bytes(edit[pos:pos+1], "little")
    pos += 1

    parsed_edit["UNUSED"] = list(edit[pos:])

    return parsed_edit


# list all of the Edits in the save
# and dump to json
def list_edits(inBuf, saveType):

    if saveType == SAVE_INTERNAL:
        numEdits = NUM_EDITS_SAVE_INTERNAL
    elif saveType == SAVE_CART:
        numEdits = NUM_EDITS_SAVE_CART

    for i in range(0, numEdits):

        pos = MAGIC_SIZE + numEdits + (i * EDIT_SIZE)

        if inBuf[MAGIC_SIZE + i] != 1:
            print("Edit slot " + str(i+1) + " is empty")
            continue

        edit = parseEdit(inBuf[pos:pos + EDIT_SIZE])

        print("Edit slot: " + str(i+1))
        print("RENAME_last_name: " + str(edit["RENAME_last_name"]))
        print("RENAME_first_name: " + str(edit["RENAME_first_name"]))
        print("RENAME_nickname: " + str(edit["RENAME_nickname"]))
        print("RENAME_modifier: " + str(edit["RENAME_modifier"]))

        outFilename = "edit_" + str(i+1) + ".json"
        outFile = open(outFilename, "w")
        outFile.write(json.dumps(edit))

        print("Wrote " + outFilename + "\n")

# list all of the Promotions in the save
def list_promotions(inBuf, saveType):

    if saveType != SAVE_INTERNAL:
        print("Only internal saves have promotions")
        sys.exit(-1)

    for i in range(0, NUM_PROMOTIONS):

        pos = SAVE_INTERNAL_PROMOTION_OFFSET + (i * SAVE_PROMOTION_SIZE)
        promotion = inBuf[pos:pos + SAVE_PROMOTION_SIZE]
        full_name = promotion[0:24].decode(encoding='shift-jis').rstrip('\x00')
        short_name = promotion[24:36].decode(encoding='shift-jis').rstrip('\x00')
        seperator = ","

        print(full_name + str(seperator) + short_name)

def insert_promotions(inBuf, promotionsFilename, saveType):

    if saveType != SAVE_INTERNAL:
        print("Only internal saves have promotions")
        sys.exit(-1)

    data = b''

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

        data += full_name + short_name

    if len(data) != NUM_PROMOTIONS * SAVE_PROMOTION_SIZE:
        print("Promotion data length is wrong!!")
        sys.exit(-1)

    # create the output data
    pos = SAVE_INTERNAL_PROMOTION_OFFSET
    outBuf = inBuf[0:pos]

    outBuf += data
    outBuf += inBuf[pos + len(data):]
    return outBuf

# list all of the wrestlers in the save
def list_wrestlers(inBuf, saveType):

    if saveType != SAVE_INTERNAL:
        print("Only internal saves have wrestler names")
        sys.exit(-1)

    for i in range(0, NUM_BUILTIN_WRESTLERS):

        pos = WRESTLER_OFFSET + (i * SAVE_WRESTLER_NAME_SIZE)
        wrestlers = inBuf[pos:pos + SAVE_WRESTLER_NAME_SIZE]

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

def insert_wrestlers(inBuf, wrestlersFilename, saveType):

    if saveType != SAVE_INTERNAL:
        print("Only internal saves have wrestler names")
        sys.exit(-1)

    data = b''

    wrestlersFile = open(wrestlersFilename, "r", encoding='utf-8')
    wrestlersBuf = wrestlersFile.readlines()

    for l in wrestlersBuf:
        l = l.strip()
        l = l.split(",")

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

        FIRST_NAME_SIZE = 12
        LAST_NAME_SIZE = 18
        NICK_NAME_SIZE = 24

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

    if len(data) != NUM_BUILTIN_WRESTLERS * SAVE_WRESTLER_NAME_SIZE:
        print("Rename wrestlers data length is wrong!!")
        sys.exit(-1)

    # create the output data
    pos = WRESTLER_OFFSET
    outBuf = inBuf[0:pos]

    outBuf += data
    outBuf += inBuf[pos + len(data):]
    return outBuf

# the checksum is computed by adding all of the bytes in the save except for the checksum itself
# the checksum is the last 4 bytes
def computeChecksum(inBuf):

    checksum = 0

    for i in range(0, len(inBuf) - 4):
        checksum += inBuf[i]

    return checksum

def main(argv):

    inSaveFile = ""
    outSaveFile = ""
    inSaveBuf = b''
    outSaveBuf = b''
    saveType = None

    listEdits = False
    insertEdit = False
    inEditFile = ""
    editSlot = 1
    appearanceNumber = 0

    listPromotions = False
    insertPromotions = False
    inPromotionsFile = ""

    listWrestlers = False
    insertWrestlers = False
    inWrestlersFile = ""

    try:
      opts, args = getopt.getopt(argv,"hi:o:",["input_save=","output_save=", "list_edits", "list_promotions", "list_wrestlers", "insert_edit=", "insert_promotions=", "insert_wrestlers=", "edit_slot=", "appearance_number="])
    except getopt.GetoptError:
      usage()

    for opt, arg in opts:
        if opt == '-h':
            print ('6mssaveedit.py -i <input_save> -o <output_save>')
            sys.exit()
        elif opt in ("-i", "--input_save"):
            inSaveFile = arg
        elif opt in ("-o", "--output_save"):
            outSaveFile = arg
        elif opt in ("--list_edits"):
            listEdits = True
        elif opt in ("--insert_edit"):
            insertEdit = True
            inEditFile = arg
        elif opt in ("--edit_slot"):
            editSlot = int(arg)
        elif opt in ("--appearance_number"):
            appearanceNumber = int(arg)
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

    if len(inSaveFile) == 0:
        print("input_save required!!");
        usage()
    else:

        # open and sanity check the input save file
        inFile = open(inSaveFile, "rb")
        inSaveBuf = inFile.read()
        inFile.close()

        if len(inSaveBuf) < MAGIC_SIZE:
            print(inSaveFile + " too small!")
            sys.exit(2)

        magic = inSaveBuf[0:8].decode(encoding='utf-8')

        # internal memory save
        if magic == MAGIC_INTERNAL:

            if len(inSaveBuf) != SAVE_INTERNAL_SIZE:
                print(inSaveFile + " is " + str(len(inSaveBuf)) + " expected " + str(SAVE_INTERNAL_SIZE))
                sys.exit(2)

            saveType = SAVE_INTERNAL

        elif magic == MAGIC_CART:

            if len(inSaveBuf) != SAVE_CART_SIZE:
                print(inSaveFile + " is " + str(len(inSaveBuf)) + " expected " + str(SAVE_CART_SIZE))
                sys.exit(2)

            saveType = SAVE_CART

        else:
            print("Unexpected magic bytes. Save is invalid.")
            sys.exit(-2)

        checksum = computeChecksum(inSaveBuf)

        saveChecksum = int.from_bytes(inSaveBuf[-3:], "big")
        if checksum != saveChecksum:
            print("Save checksum is invalid: expected " + str(hex(checksum)) + " got " + str(hex(saveChecksum)))

    if listEdits == True:
        list_edits(inSaveBuf, saveType)
        sys.exit(0)

    if listPromotions == True:
        list_promotions(inSaveBuf, saveType)
        sys.exit(0)

    if listWrestlers == True:
        list_wrestlers(inSaveBuf, saveType)
        sys.exit(0)

    if insertEdit == True:

        if len(outSaveFile) == 0:
            usage()

        inSaveBuf = insert_edit(inSaveBuf, inEditFile, editSlot, appearanceNumber, saveType)

    if insertPromotions == True:

        if len(outSaveFile) == 0:
            usage()

        inSaveBuf = insert_promotions(inSaveBuf, inPromotionsFile, saveType)

    if insertWrestlers == True:

        if len(outSaveFile) == 0:
            usage()

        inSaveBuf = insert_wrestlers(inSaveBuf, inWrestlersFile, saveType)


    if outSaveFile != "":
        newChecksum = computeChecksum(inSaveBuf)

        outSaveBuf = inSaveBuf[0:-4] + newChecksum.to_bytes(4, byteorder='big')

        # open and sanity check the input save file
        outFile = open(outSaveFile, "wb")
        outFile.write(outSaveBuf)
        outFile.close()

        print("Wrote " + outSaveFile + ".")

    return 0

if __name__ == "__main__":

    if sys.version_info.major < 3:
        print("Python 3 required")
        sys.exit(-1)

    main(sys.argv[1:])
