import sys

# promotions
NUM_PROMOTIONS = 14
BUILTIN_PROMOTION_OFFSET = 0x3A03C
BUILTIN_PROMOTION_SHORT_OFFSET = 0x3A1C2
PROMOTION_NAME_SIZE = 24
PROMOTION_SHORT_NAME_SIZE = 12

# builtin wrestlers
NUM_BUILTIN_WRESTLERS = 160
BUILTIN_WRESTLER_OFFSET = 0x3a680
BUILTIN_WRESTLER_SIZE = 0x1AC
BUILTIN_WRESTLER_NAME_SIZE = 61
NUM_BUILTIN_ATTIRES = 6

SAVE_INTERNAL_SIZE = 20308
SAVE_CART_SIZE = 31820

SAVE_INTERNAL = 0
SAVE_CART = 1

MAGIC_SIZE = 8
MAGIC_INTERNAL = "FPS_DATA"
MAGIC_CART = "FPS_EDIT"

EDIT_SIZE = 0x1f0

NUM_EDITS_SAVE_INTERNAL = 16
NUM_EDITS_SAVE_CART = 64
SAVE_WRESTLER_NAME_SIZE = 0x37

SAVE_PROMOTION_SIZE = 36

SAVE_INTERNAL_PROMOTION_OFFSET = 8 + NUM_EDITS_SAVE_INTERNAL + (NUM_EDITS_SAVE_INTERNAL * EDIT_SIZE)
WRESTLER_OFFSET = SAVE_INTERNAL_PROMOTION_OFFSET + (NUM_PROMOTIONS * SAVE_PROMOTION_SIZE)

# offset to wrestler palettes in FPS.SBL
FPS_SBL_OFFSET = 0x252000 # 0 = 0021ac00 in memory view


def requirePython3():
    if sys.version_info.major < 3:
        print("Python 3 required")
        sys.exit(-1)


#
# Rename
#

#
# Appearance
#
def lookupAppearancePose(pose):

    poses = {

        0 : "Strong",
        1 : "Technical",
        2 : "Amateur",
        3 : "Power",
        4 : "Lucha",
        5 : "Shooting",
        6 : "Mysterious",
        7 : "Bone",
        8 : "Kobudo",


    }

    if pose not in poses:

        print("Failed to lookuped pose: " + str(pose))
        return(str(hex(pose)))

    return poses[pose]

def lookupAppearanceSize(size):

    sizes = {
        0 : "S",
        1 : "M",
        2 : "L",
    }

    if size not in sizes:

        print("Failed to lookuped size: " + str(size))

    return sizes[size]

def lookupAppearanceChest(chest):

    size = ""

    mod = chest // 11
    if mod == 0:
        size = "D"
    elif mod == 1:
        size = "L"
    elif mod == 2:
        size = "M"
    elif mod == 3:
        size = "S"
    else:
        print("chest size is invalid: " + str(chest) + " " + str(mod))
        sys.exit(-1)

    chests = {
        0 : "Bare",
        1 : "Amat1",
        2 : "Kaiser",
        3 : "Single",
        4 : "T-Shirt",
        5 : "Ninja",
        6 : "Aztec",
        7 : "Amat2",
        8 : "Doji",
        9 : "Firesuit",
        10 : "Body Paint"
    }

    outfit = chest % 11

    if outfit not in chests:

        print("Failed to lookuped chest: " + str(chest) + " " + str(outfit))
        return(str(hex(chest)))
        #sys.exit(0)

    return size + ", " + chests[outfit]

def lookupAppearanceWaist(waist):

    size = ""

    mod = waist // 22
    if mod == 0:
        size = "D"
    elif mod == 1:
        size = "L"
    elif mod == 2:
        size = "M"
    elif mod == 3:
        size = "S"
    else:
        print("waist size is invalid: " + str(waist) + " " + str(mod))
        #sys.exit(-1)

    waists = {

        0 : "Tights",
        1 : "Amat1",
        2 : "Kaiser",
        3 : "Striped Belt",
        5 : "Single",
        6 : "TShirt + Jeans",
        7 : "Ninja",
        8 : "Solid Belt",
        11: "Shima",
        12 : "Amat2",
        13: "Doji",
        14: "Firesuit",
        17: "Stripe",
        20: "Body Paint",
        21: "Belt + Shirt",
    }

    outfit = waist % 22

    if outfit not in waists:

        print("Failed to lookuped waist: " + str(waist) + " " + str(outfit))
        return(str(hex(waist)))
        #sys.exit(0)

    return size + ", " + waists[outfit]

def lookupAppearanceUpperArm(upperArm):

    size = ""

    mod = upperArm // 9
    if mod == 0:
        size = "D"
    elif mod == 1:
        size = "L"
    elif mod == 2:
        size = "M"
    elif mod == 3:
        size = "S"
    else:
        print("upper arm size is invalid: " + str(upperArm) + " " + str(mod))
        #sys.exit(-1)

    upperArms = {

        0 : "Bare",
        1 : "Kaiser",
        2 : "Brace",
        3 : "T-Shirt",
        4 : "Ninja",
        5 : "Guards",
        6 : "Bands",
        8 : "Ripped",
    }

    outfit = upperArm % 9

    if outfit not in upperArms:

        print("Failed to lookuped upper arm: " + str(upperArm) + " " + str(outfit))
        return(str(hex(upperArm)))
        #sys.exit(0)

    return size + ", " + upperArms[outfit]

def lookupAppearanceLowerArm(lowerArm):

    size = ""

    mod = lowerArm // 7
    if mod == 0:
        size = "D"
    elif mod == 1:
        size = "L"
    elif mod == 2:
        size = "M"
    elif mod == 3:
        size = "S"
    else:
        print("lower arm size is invalid: " + str(lowerArm) + " " + str(mod))
        #sys.exit(-1)

    lowerArms = {
        0 : "Bare",
        1 : "Kaiser",
        3 : "Bracers",
        4 : "Ninja",
        5 : "Wrist Band",
        6 : "Pad + Wrist",

    }

    outfit = lowerArm % 7

    if outfit not in lowerArms:

        print("Failed to lookuped lower arm: " + str(lowerArm) + " " + str(outfit))
        return(str(hex(lowerArm)))
        #sys.exit(0)

    return size + ", " + lowerArms[outfit]

def lookupAppearanceHand(hand):

    hands = {

        0 : "Bare",
        1 : "Gloves",
        2 : "Handtape",
    }

    if hand not in hands:

        print("Failed to lookuped hand: " + str(hand))
        sys.exit(0)

    return hands[hand]

def lookupAppearanceQuad(quad):

    # 0-19 = large
    # 20-39 = medium
    # 40-59 = small?

    size = ""

    mod = quad // 20
    if mod == 0:
        size = "L"
    elif mod == 1:
        size = "M"
    elif mod == 2:
        size = "S"
    else:
        print("quad size is invalid: " + str(quad) + " " + str(mod))
        sys.exit(-1)

    quads = {
        0: "Bare",
        1: "Tights1",
        2: "Kaiser",
        3: "Lines",
        4: "Firesuit",
        5: "Arrow",
        6: "Spat",
        7: "Doji",
        8: "Jean",
        10: "Hikawa",
        11: "Tights1",
        13: "Kazama",
        14: "Tights2",
        15: "Tights3",
        16: "Shorts2",
        17: "Shorts1",
        18: "Brace",
        19: "Thunder",
    }

    outfit = quad % 20


    if outfit not in quads:

        print("Failed to lookuped quad: " + str(quad))
        return(str(hex(quad)))
        #sys.exit(0)

    return size + ", " + quads[outfit]



def lookupAppearanceShin(shin):

    shins = {

        0 : "Bare",
        2 : "Normal",
        3 : "Pad + Boot1",
        4 : "Tights",
        5 : "Tights + Shoes",
        6 : "Pad + Boot2",
        7 : "Pad + Boot3",
        8 : "Pad + Boot4",
        9 : "Full",
        10 : "Doji",
        11 : "Jean",
        12 : "Pants",
        14 : "Ninja 2",
        16 : "Mexican 2",
        17 : "Shoe + Kneepad",
        18 : "American Shoes",
        21 : "Jean + Cowboy",
        22 : "Mexican 1",
        25 : "Low Boot"
    }

    if shin not in shins:

        print("Failed to lookuped shin: " + str(shin))
        return(str(shin))
        #sys.exit(0)

    return shins[shin]

def lookupAppearanceFeet(feet):

    feets = {

        0 : "Bare",
        1 : "Shoe1",
        2 : "Shoe2",
        3 : "Shoe3",
        4 : "Shoe4",
        5 : "Full",
        6 : "Kung Fu",
        9 : "American Shoes",
        10 : "Panther",
        11 : "Cowboy",
        12 : "Shoe5",
        13 : "Ankle Tape",

    }

    if feet not in feets:

        print("Failed to lookuped feet: " + str(feet))
        return(str(feet))
        #sys.exit(0)

    return feets[feet]

#
# Palette
#

def convertRGBToList(rgb):

    rgb_list = []

    for i in range(0, len(rgb)):
        if i % 2 != 0:
           continue

        val = (rgb[i] << 8) + rgb[i+1]

        r = val & 0x1f
        g = (val >> 5) & 0x1f
        b = (val >> 10) & 0x1f
        rgb_list.append((r, g, b))

    return rgb_list

#
# Character
#
def lookupCharacterWeightClass(weight_class):

    weight_classes = {
        1 : "Heavy Weight",
        2 : "Junior Heavy Weight",
        3 : "Free"
    }

    if weight_class not in weight_classes:

        print("Failed to lookuped wc: " + str(wcweight_class))
        sys.exit(0)

    return weight_classes[weight_class]

def lookupCharacterOrigin(origin):

    origins = {
        0: "Parts Unknown",
        1: "Japan",
        2: "America",
        3: "Canada",
        4: "Dutch",
        5: "Mexico",
        6: "England",
        7: "France",
        8: "Brazil",
        9: "Russia",
        10: "Puerto Rico",
        11: "India",
        12: "Sudan",
        13: "Jordon",
        14: "Cuba",
        15: "Finland",
        16: "Croatia Republic",
        17: "Holland",
        18: "Italy",
        19: "Spain",
        20: "Switzerland",
        21: "China",
        22: "North Korea",
        23: "South Korea",
        24: "Mongolia",
        25: "Thailand",
        26: "Australia",
        27: "New Zealand",
        28: "Bulgaria",
        29: "Botswana",
        30: "Republic of South Africa",
        31: "Tonga"
    }

    if origin not in origins:

        print("Failed to lookuped origin: " + str(origin))
        sys.exit(0)

    return origins[origin]


def lookupCharacterPromotion(promotion):

    promotions = {
        0: "New Japan PW",
        1: "H. Ishingun",
        2: "All Japan PW",
        3: "ECW / Indies",
        4: "Pro - W.A.R.",
        5: "Michinoku PW",
        6: "W.C.W.F.",
        7: "U.W.F. Inter.",
        8: "R.I.N.G.S",
        9: "FugiwaraGumi",
        10: "Pancrase",
        11: "Triple A",
        12: "Martial Arts",
        13: "Legendary PW"
    }

    if promotion not in promotions:

        print("Failed to lookuped promotion: " + str(promotion))
        sys.exit(0)

    return promotions[promotion]

def lookupCharacterCritical(critical):

    criticals = {
        0: "Finisher",
        1: "Suplex",
        2: "Power",
        3: "Technical",
        4: "Striking",
        5: "Submission"

    }

    if critical not in criticals:

        print("Failed to lookuped critical: " + str(critical))
        sys.exit(0)

    return criticals[critical]

def lookupCharacterRecoveryPower(recoveryPower):

    recoveryPowers = {
        0: "Slow",
        1: "Medium",
        2: "Fast"
    }

    if recoveryPower not in recoveryPowers:

        print("Failed to lookuped recoveryPower: " + str(recoveryPower))
        sys.exit(0)

    return recoveryPowers[recoveryPower]


def lookupCharacterBreathing(breathingPower):

    breathingPowers = {
        0: "Below",
        1: "Medium",
        2: "Above"
    }

    if breathingPower not in breathingPowers:

        print("Failed to breathingPower: " + str(breathingPower))
        sys.exit(0)

    return breathingPowers[breathingPower]

def lookupCharacterSpritualPower(spiritualPower):

    spiritualPowers = {
        0: "Poor",
        1: "Medium",
        2: "Strong"
    }

    if spiritualPower not in spiritualPowers:

        print("Failed to spiritualPower: " + str(spiritualPower))
        sys.exit(0)

    return spiritualPowers[spiritualPower]

def lookupCharacterStamina(stamina):

    staminas = {
        0: "Low",
        1: "Medium",
        2: "High"
    }

    if stamina not in staminas:

        print("Failed to lookuped stamina: " + str(stamina))
        sys.exit(0)

    return staminas[stamina]

def lookupCharacterFightStyle(fightStyle):

    fightStyles = {
        0: "Orthodox",
        1: "Technician",
        2: "Wrestling",
        3: "Ground",
        4: "Power",
        5: "Junior",
        6: "Luchadore",
        7: "Heel",
        8: "Mysterious",
        9: "Shooter",
        10: "Fighter",
        11: "Grappler",
        12: "Panther",
        13: "Giant",
        14: "Vicious"
    }

    if fightStyle not in fightStyles:

        print("Failed to lookuped fight style: " + str(fightStyle))
        sys.exit(0)

    return fightStyles[fightStyle]

def lookupCharacterDefenseStyle(defenseStyle):

    defenseStyles = {
        0: "Orthodox",
        1: "Technician",
        2: "Power",
        3: "Junior",
        4: "Luchadore",
        5: "Heel",
        6: "Mysterious",
        7: "All-Round",
        8: "Shooter",
        9: "Fighter",
        10: "Grappler",
        11: "Giant",
        12: "Vicious"
    }

    if defenseStyle not in defenseStyles:

        print("Failed to lookuped defenseStyle style: " + str(defenseStyle))
        sys.exit(0)

    return defenseStyles[defenseStyle]

def lookupCharacterVoice(voice):

    voices = {
        0 : "Nihon-jin 1",
        1 : "Nihon-jin 2",
        2 : "Nihon-jin 3",
        3 : "Nihon-jin 4",
        4 : "Gaijin 1",
        5 : "Gaijin 2",
        6 : "Gaijin 3",
        7 : "Gaijin 4",
    }

    if voice not in voices:

        print("Failed to lookuped voice: " + str(voice))
        sys.exit(0)

    return voices[voice]

def lookupCharacterMovementSpeed(movementSpeed):

    movementSpeeds = {

        3 : "Slow",
        4 : "Medium Slow",
        5 : "Medium",
        6 : "Medium Fast",
        7 : "Fast",

    }

    if movementSpeed not in movementSpeeds:

        print("Failed to lookuped movementSpeed: " + str(movementSpeed))
        return(hex(movementSpeed))

    return movementSpeeds[movementSpeed]

def lookupCharacterClimb(climb):

    climbs = {

        0 : "I Cannot Ascend",
        1 : "I Can Ascend",
        2 : "I Can Ascend While I Run",

    }

    if climb not in climbs:

        print("Failed to lookuped climb: " + str(climb))
        return(hex(climb))

    return climbs[climb]


#
# Moves
#

def lookupMoveAttributes(moveAttributes):

    attributes = ""

    if moveAttributes & 0x10:
        attributes += "- specialty "
    if moveAttributes & 0x20:
        attributes += "- finisher "
    if moveAttributes & 0x40:
        attributes += "- sound1 "
    if moveAttributes & 0x80:
        attributes += "- sound2"

    return attributes


def lookupMoveType(moveType):

    moveTypes = {
        0 : "Stnd + A",
        1 : "Stnd + B",
        2 : "Stnd + C",
        3 : "Stnd + A+B",
        4 : "Run + A",
        5 : "Run + B",
        6 : "Counter + A",
        7 : "Counter + B",
        8 : "Run to Corner",
        9 : "Outside Run",
        10 : "Jump Outside",
        11 : "Jump Inside",
        12 : "Corner + A",
        13 : "Corner + B",
        14 : "Corner + C",
        15 : "Corner + A+B",
        16 : "Grab + A",
        17 : "Grab + A + U",
        18 : "Grab + A + LR",
        19 : "Grab + A + D",
        20 : "Grab + B",
        21 : "Grab + B + U",
        22 : "Grab + B + LR",
        23 : "Grab + B + D",
        24 : "Grab + C",
        25 : "Grab + C + U",
        26 : "Grab + C + LR",
        27 : "Grab + C + D",
        28 : "Grab + A + B",
        29 : "Back + A",
        30 : "Back + B",
        31 : "Back + C",
        32 : "Back + C + UD",
        33 : "Back + C + LR",
        34 : "Back + A+B",
        35 : "Back Def + A",
        36 : "Back Def + B",
        37 : "Supine Head + B",
        38 : "Supine Leg + B",
        39 : "Prone Head + B",
        40 : "Prone Leg + B",
        41 : "Supine Head + C",
        42 : "Supine Leg + C",
        43 : "Prone Head + C",
        44 : "Prone Leg + C",
        45 : "Corner Grab + C + U",
        46 : "Corner Grab + C + LR",
        47 : "Corner Grab + C + D",
        48 : "Performance LT",
        49 : "Performance RT",
        50 : "Front 2 Platon",
        51 : "Front 3 Platon",
        52 : "Back 2 Platon",
        53 : "Back 3 Platon",
        54 : "Corner 2 Platon",
        55 : "Corner 3 Platon",
    }

    if moveType not in moveTypes:

        print("Failed to lookup move type: " + str(moveType))

        return moveTypes[moveType]

def lookupMove(meta, move):

    moveId = ((meta & 0x0f) << 8) | move

    moves = {

        # Stand A/B
        0x1: "Punch",
        0x4: "Slap",
        0x7: "Jab",
        0xa: "Open Palm",
        0x1f: "Thigh",        
        0x43: "Front Kick",
        0x46: "Boot Kick",
        0xd: "Low Kick",
        0x10: "Low Roundhouse Kick",
        0x13: "Muay Thai Low Kick",        
        0x16: "Middle Kick",
        0x19: "Center Kick",
        0x1c: "Muay Thai Mid",

        # Stand C/A+B
        0x87: "SPNF",
        0xcc: "Kesageri Chop",
        0xb7: "Elbow Roll",
        0x4b: "High Kick",
        0x4e: "Muay Thai High Kick",        
        0x51: "Roundhouse Kick",
        0xab: "Highman Kick",
        0x7e: "Thrust Kick",
        0x8a: "Giant boot",
        0x69: "Sole Butt",        
        0x66: "Sole Roll",
        0x57: "Back Spin",
        0x6f: "Dropkick",
        0x72: "Turn Dropkick",
        0x75: "Missile Dropkick",        
        0x78: "Low Dropkick",        
        0x54: "Jump High Kick",
        0x6c: "Enzugiri",
        0x63: "Kopou Abise Giri",
        0x5d: "Wheel",        
        0x60: "Spin Wheel",        
        0x7b: "Big Wheel",
        0x84: "Tackle",
        0xc9: "Spear",
        0xc6: "Victory Roll Pin",
        0x8d: "Big Fire",
        0x90: "Mist", 

        # Run + A/Run + B
        0x152: "Harite",
        0x138: "Shoulder",
        0x140: "Kitchen Sink",
        0x13c: "Elbow Pat",
        0x16e: "Jumping Elbow",
        0x172: "Boot",
        0x142: "Kenka",
        0x178: "Jumping Knee",
        0x180: "Jumping Hip Attack",
        0x13e: "3 Point Stance",
        0x17c: "Body Splash",
        0x17a: "Vader",
        0x176: "Thesz Press",
        0x13a: "Spear",
        0x14a: "Drop Kick",
        0x14c: "Spin Drop Kick",
        0x14e: "Missile Drop Kick",
        0x150: "Low Dropkick",
        0x146: "Wheel",
        0x148: "Flying Wheel",
        0x170: "Zero Sen",
        0x17e: "Inadsma Leg",
        0x1a2: "Flying Shoulder",
        0x174: "Body Attack",
        0x15a: "Cross Chop",
        0x15e: "Jump Lariat",
        0x160: "Run Neckbreaker",
        0x162: "Jump Neck Breaker",
        0x164: "Lariat",
        0x168: "Clothesline",
        0x166: "Tatakitsuke",
        0x16c: "Duggan Hammer",
        0x16a: "Western Lariat",
        0x158: "Frankensteiner",
        0x190: "Flying Head Scissors",
        0x1ac: "FLying DDT",
        0x1b2: "Backswitch",

        # Counter A/B
        0x1cc: "Slap",
        0x1ce: "Harite",
        0x2a4: "Jab",
        0x2a6: "Open Palm",
        0x1d0: "Fore Arm",
        0x1d2: "Back Elbow",
        0x1d6: "Knee Arrow",
        0x1d4: "SPNF",
        0x232: "Kesagiri Chop",
        0x236: "Elbow Roll",
        0x2aa: "Thigh Kick",
        0x1dc: "Front Kick",
        0x2a8: "Boot Kick",
        0x1da: "Boot Kick Arms",
        0x1e0: "Low Kick",
        0x1de: "Low Round",
        0x1e2: "Thai Low",
        0x1e6: "Mid Kick",
        0x1e4: "Center Kick",
        0x1e8: "Thai Mid",
        0x202: "Super Kick",
        0x1fe: "Big Boot",
        0x200: "Gut Kick",
        0x1f0: "Spin Kick",
        0x204: "Sole Butt",
        0x206: "Sole Roll",
        0x1f2: "Back Spin",
        0x1d8: "Knee Lift",
        0x218: "Jump Hip Attack",
        0x1f4: "Drop Kick",
        0x1fa: "Turn Drop Kick",
        0x1f6: "Missile Drop Kick",
        0x1f8: "Low Dropkick",
        0x1fc: "Drop Toe",
        0x208: "Body Drop",
        0x20c: "Arm Drag",
        0x298: "Gorilla Press Slam",
        0x21e: "Sideslam",
        0x222: "Tiltslam",
        0x21a: "Tilt A Whirl",
        0x21c: "Silfin Breaker",
        0x242: "Head Scissors",
        0x20e: "Hurricanrana",
        0x210: "Frankensteiner Pin",
        0x2ac: "Frankensteiner",
        0x212: "Powerslam Pin",
        0x216: "Urnage",
        0x226: "Back Ipponzi",
        0x228: "Mountain",
        0x280: "Spine Bomb",
        0x214: "Choke Slam",
        0x224: "Flying Jumping DDT",
        0x220: "Cobra",
        0x258: "Gatame",
        0x26c: "Backswitch",

        # Run To Corner
        0x0: "",
        0x2b6: "",
        0x2b7: "",
        0x2b8: "",
        0x2cc: "",
        0x2bb: "",
        0x2c6: "",
        0x2bc: "",
        0x2d0: "",
        0x2bd: "",
        0x2be: "",
        0x2c4: "",
        0x2ca: "",
        0x2bf: "",
        0x2d1: "",
        0x2b9: "",
        0x2c0: "",
        0x2c1: "",
        0x2c5: "",
        0x2c7: "",
        0x2ba: "",
        0x2c3: "",

        # outside run
        0x0: "",
        0x2df: "",
        0x2e3: "",
        0x2dd: "",
        0x2ef: "",
        0x2e1: "",
        0x2e5: "",
        0x2e7: "",
        0x2ed: "",
        0x2eb: "",
        0x2e9: "",

        # jump outside
        0x0: "",
        0x30f: "",
        0x2fd: "",
        0x30d: "",
        0x2ff: "",
        0x301: "",

        # jump inside
        0x0: "",
        0x785: "",
        0x787: "",
        0x763: "",
        0x769: "",
        0x76f: "",

        # corner a
        0x0: "",
        0x323: "",
        0x31b: "",
        0x325: "",
        0x31d: "",
        0x31f: "",
        0x361: "",
        0x321: "",
        0x385: "",
        0x327: "",
        0x32b: "",
        0x331: "",
        0x333: "",
        0x335: "",
        0x32d: "",
        0x32f: "",
        0x339: "",
        0x337: "",
        0x33f: "",
        0x33b: "",
        0x371: "",
        0x341: "",
        0x343: "",
        0x349: "",
        0x345: "",
        0x357: "",
        0x34d: "",
        0x347: "",
        0x353: "",
        0x34f: "",
        0x355: "",
        0x359: "",
        0x379: "",
        0x37b: "",
        0x35b: "",
        0x35d: "",

        # grab a
        0x394: "",
        0x397: "",
        0x395: "",
        0x398: "",
        0x396: "",
        0x3b4: "",
        0x393: "",
        0x392: "",
        0x399: "",
        0x3bd: "",
        0x390: "",
        0x391: "",
        0x39a: "",
        0x38f: "",
        0x3c1: "",
        0x39b: "",
        0x39d: "",
        0x39e: "",
        0x3a6: "",
        0x39f: "",
        0x3a0: "",
        0x3a4: "",
        0x3a2: "",
        0x3a3: "",
        0x3a5: "",
        0x3a1: "",
        0x3a7: "",
        0x3a9: "",
        0x3ae: "",
        0x3a8: "",
        0x3aa: "",
        0x3ab: "",
        0x3ac: "",
        0x3af: "",
        0x3b0: "",
        0x3b1: "",
        0x3b2: "",
        0x3c3: "",
        0x3ad: "",
        0x3b3: "",
        0x44d: "",

        # grab b
        0x4e1: "",
        0x3d8: "",
        0x3cb: "",
        0x3cc: "",
        0x40e: "",
        0x3cf: "",
        0x3d0: "",
        0x3d1: "",
        0x4e4: "",
        0x3ce: "",
        0x3cd: "",
        0x3f4: "",
        0x3f6: "",
        0x3f5: "",
        0x41e: "",
        0x3d3: "",
        0x3f7: "",
        0x3d2: "",
        0x3e5: "",
        0x3e7: "",
        0x3e6: "",
        0x405: "",
        0x406: "",
        0x433: "",
        0x3f8: "",
        0x45e: "",
        0x3d4: "",
        0x49a: "",
        0x40f: "",
        0x3d5: "",
        0x3d6: "",
        0x3db: "",
        0x4e3: "",
        0x3dd: "",
        0x421: "",
        0x3dc: "",
        0x3de: "",
        0x3df: "",
        0x3e0: "",
        0x3d9: "",
        0x3da: "",
        0x3fb: "",
        0x3fc: "",
        0x3e3: "",
        0x3e4: "",
        0x401: "",
        0x403: "",
        0x402: "",
        0x3f3: "",
        0x3fe: "",
        0x4e2: "",
        0x3ea: "",
        0x3ef: "",
        0x3ee: "",
        0x3ec: "",
        0x3ed: "",
        0x400: "",
        0x3e8: "",
        0x3e9: "",
        0x499: "",
        0x40a: "",
        0x4ee: "",
        0x489: "",
        0x3f1: "",
        0x3f2: "",
        0x3eb: "",
        0x3ff: "",
        0x3f9: "",
        0x3fa: "",
        0x454: "",
        0x455: "",
        0x394: "",
        0x397: "",
        0x395: "",
        0x398: "",
        0x396: "",
        0x3b4: "",
        0x393: "",
        0x392: "",
        0x399: "",
        0x3bd: "",
        0x390: "",
        0x391: "",
        0x39a: "",
        0x38f: "",
        0x3c1: "",
        0x39b: "",
        0x39d: "",
        0x39e: "",
        0x3a6: "",
        0x39f: "",
        0x3a0: "",
        0x3a4: "",
        0x3a2: "",
        0x3a3: "",
        0x3a5: "",
        0x3a1: "",
        0x3a7: "",
        0x3a9: "",
        0x3ae: "",
        0x3a8: "",
        0x3aa: "",
        0x3ab: "",
        0x3ac: "",
        0x3af: "",
        0x3b0: "",
        0x3b1: "",
        0x3b2: "",
        0x3c3: "",
        0x3ad: "",
        0x3b3: "",
        0x44d: "",

        # grab c
        0x40b: "",
        0x40c: "",
        0x404: "",
        0x49b: "",
        0x4e0: "",
        0x407: "",
        0x4e6: "",
        0x4e8: "",
        0x4e5: "",
        0x4e7: "",
        0x475: "",
        0x4eb: "",
        0x41b: "",
        0x41c: "",
        0x41d: "",
        0x451: "",
        0x474: "",
        0x434: "",
        0x450: "",
        0x477: "",
        0x4ed: "",
        0x4d2: "",
        0x408: "",
        0x449: "",
        0x4de: "",
        0x44b: "",
        0x42e: "",
        0x42f: "",
        0x430: "",
        0x411: "",
        0x412: "",
        0x413: "",
        0x447: "",
        0x4d9: "",
        0x414: "",
        0x415: "",
        0x410: "",
        0x44c: "",
        0x4a7: "",
        0x4d5: "",
        0x417: "",
        0x448: "",
        0x4be: "",
        0x416: "",
        0x445: "",
        0x446: "",
        0x44f: "",
        0x42c: "",
        0x419: "",
        0x42d: "",
        0x420: "",
        0x4ab: "",
        0x423: "",
        0x424: "",
        0x422: "",
        0x439: "",
        0x4b3: "",
        0x429: "",
        0x4bb: "",
        0x42a: "",
        0x425: "",
        0x42b: "",
        0x441: "",
        0x442: "",
        0x443: "",
        0x444: "",
        0x440: "",
        0x43e: "",
        0x43f: "",
        0x43d: "",
        0x40d: "",
        0x41f: "",
        0x43c: "",
        0x470: "",
        0x426: "",
        0x427: "",
        0x435: "",
        0x46f: "",
        0x438: "",
        0x43a: "",
        0x476: "",
        0x436: "",
        0x4ea: "",
        0x4c6: "",
        0x437: "",
        0x4ac: "",
        0x43b: "",
        0x44a: "",
        0x452: "",
        0x456: "",
        0x458: "",
        0x459: "",
        0x4ca: "",
        0x46c: "",
        0x4df: "",
        0x46d: "",
        0x46e: "",
        0x45a: "",
        0x45d: "",
        0x45b: "",
        0x461: "",
        0x45c: "",
        0x4c1: "",
        0x4f0: "",
        0x45f: "",
        0x460: "",
        0x462: "",
        0x468: "",
        0x473: "",
        0x467: "",
        0x469: "",
        0x46a: "",
        0x463: "",
        0x464: "",
        0x465: "",
        0x46b: "",
        0x466: "",
        0x4e1: "",
        0x3d8: "",
        0x3cb: "",
        0x3cc: "",
        0x40e: "",
        0x3cf: "",
        0x3d0: "",
        0x3d1: "",
        0x4e4: "",
        0x3ce: "",
        0x3cd: "",
        0x3f4: "",
        0x3f6: "",
        0x3f5: "",
        0x41e: "",
        0x3d3: "",
        0x3f7: "",
        0x3d2: "",
        0x3e5: "",
        0x3e7: "",
        0x3e6: "",
        0x405: "",
        0x406: "",
        0x433: "",
        0x3f8: "",
        0x45e: "",
        0x3d4: "",
        0x49a: "",
        0x40f: "",
        0x3d5: "",
        0x3d6: "",
        0x3db: "",
        0x4e3: "",
        0x3dd: "",
        0x421: "",
        0x3dc: "",
        0x3de: "",
        0x3df: "",
        0x3e0: "",
        0x3d9: "",
        0x3da: "",
        0x3fb: "",
        0x3fc: "",
        0x3e3: "",
        0x3e4: "",
        0x401: "",
        0x403: "",
        0x402: "",
        0x3f3: "",
        0x3fe: "",
        0x4e2: "",
        0x3ea: "",
        0x3ef: "",
        0x3ee: "",
        0x3ec: "",
        0x3ed: "",
        0x400: "",
        0x3e8: "",
        0x3e9: "",
        0x499: "",
        0x40a: "",
        0x4ee: "",
        0x489: "",
        0x3f1: "",
        0x3f2: "",
        0x3eb: "",
        0x3ff: "",
        0x3f9: "",
        0x3fa: "",
        0x454: "",
        0x455: "",
        0x394: "",
        0x397: "",
        0x395: "",
        0x398: "",
        0x396: "",
        0x3b4: "",
        0x393: "",
        0x392: "",
        0x399: "",
        0x3bd: "",
        0x390: "",
        0x391: "",
        0x39a: "",
        0x38f: "",
        0x3c1: "",
        0x39b: "",
        0x39d: "",
        0x39e: "",
        0x3a6: "",
        0x39f: "",
        0x3a0: "",
        0x3a4: "",
        0x3a2: "",
        0x3a3: "",
        0x3a5: "",
        0x3a1: "",
        0x3a7: "",
        0x3a9: "",
        0x3ae: "",
        0x3a8: "",
        0x3aa: "",
        0x3ab: "",
        0x3ac: "",
        0x3af: "",
        0x3b0: "",
        0x3b1: "",
        0x3b2: "",
        0x3c3: "",
        0x3ad: "",
        0x3b3: "",
        0x44d: "",

        # back a
        0x4f1: "",
        0x4f2: "",
        0x4f3: "",
        0x4f4: "",
        0x4f7: "",
        0x53b: "",
        0x4f6: "",
        0x4fb: "",
        0x4f8: "",
        0x4fa: "",
        0x4f9: "",

        # back b
        0x509: "",
        0x4fc: "",
        0x4fd: "",
        0x4fe: "",
        0x505: "",
        0x503: "",
        0x502: "",
        0x501: "",
        0x508: "",
        0x506: "",
        0x507: "",
        0x4ff: "",
        0x500: "",
        0x53f: "",
        0x527: "",
        0x53e: "",
        0x55e: "",
        0x4f1: "",
        0x4f2: "",
        0x4f3: "",
        0x4f4: "",
        0x4f7: "",
        0x53b: "",
        0x4f6: "",
        0x4fb: "",
        0x4f8: "",
        0x4fa: "",
        0x4f9: "",

        # back c
        0x567: "",
        0x566: "",
        0x512: "",
        0x515: "",
        0x50e: "",
        0x50f: "",
        0x510: "",
        0x511: "",
        0x517: "",
        0x513: "",
        0x556: "",
        0x548: "",
        0x50a: "",
        0x50b: "",
        0x50c: "",
        0x50d: "",
        0x528: "",
        0x529: "",
        0x54d: "",
        0x536: "",
        0x55f: "",
        0x51b: "",
        0x51c: "",
        0x51a: "",
        0x52d: "",
        0x51d: "",
        0x52c: "",
        0x518: "",
        0x519: "",
        0x51e: "",
        0x523: "",
        0x522: "",
        0x525: "",
        0x537: "",
        0x524: "",
        0x54c: "",
        0x521: "",
        0x560: "",
        0x51f: "",
        0x520: "",
        0x54b: "",
        0x526: "",
        0x561: "",
        0x52e: "",
        0x52f: "",
        0x530: "",
        0x562: "",
        0x531: "",
        0x532: "",
        0x533: "",
        0x535: "",
        0x509: "",
        0x4fc: "",
        0x4fd: "",
        0x4fe: "",
        0x505: "",
        0x503: "",
        0x502: "",
        0x501: "",
        0x508: "",
        0x506: "",
        0x507: "",
        0x4ff: "",
        0x500: "",
        0x53f: "",
        0x527: "",
        0x53e: "",
        0x55e: "",
        0x4f1: "",
        0x4f2: "",
        0x4f3: "",
        0x4f4: "",
        0x4f7: "",
        0x53b: "",
        0x4f6: "",
        0x4fb: "",
        0x4f8: "",
        0x4fa: "",
        0x4f9: "",

        # back defense + a
        0x56d: "",

        # back defense b
        0x56d: "",
        0x56e: "",
        0x56f: "",
        0x570: "",
        0x574: "",
        0x572: "",
        0x578: "",
        0x571: "",
        0x577: "",
        0x576: "",
        0x575: "",
        0x579: "",
        0x58c: "",
        0x57a: "",
        0x573: "",

        #Supine head b
        0x5ea: "",
        0x5ed: "",
        0x5ef: "",
        0x59a: "",
        0x59c: "",
        0x5ac: "",
        0x59b: "",
        0x59d: "",
        0x5e4: "",
        0x59e: "",
        0x59f: "",
        0x5f3: "",
        0x5ad: "",
        0x5ae: "",
        0x5af: "",
        0x5b3: "",
        0x5b4: "",
        0x5b6: "",
        0x5b7: "",
        0x5b9: "",
        0x5ba: "",
        0x5bc: "",
        0x5be: "",
        0x5bf: "",
        0x5a1: "",
        0x5cb: "",
        0x5e7: "",
        0x5f1: "",
        0x5db: "",
        0x5a0: "",
        0x5a2: "",
        0x5aa: "",
        0x5a3: "",
        0x5a5: "",
        0x5d5: "",
        0x5a6: "",
        0x5a7: "",
        0x5a9: "",
        0x5ab: "",
        0x5a8: "",
        0x5f2: "",
        0x5f4: "",
        0x5fe: "",
        0x600: "",
        0x5fa: "",
        0x604: "",
        0x5fc: "",
        0x5f6: "",
        0x602: "",
        0x5f8: "",

        # supine leg b
        0x625: "",
        0x608: "",
        0x614: "",
        0x615: "",
        0x61d: "",
        0x61e: "",
        0x620: "",
        0x63c: "",
        0x63d: "",
        0x63e: "",
        0x609: "",
        0x648: "",
        0x62b: "",
        0x60c: "",
        0x60d: "",
        0x60e: "",
        0x60f: "",
        0x631: "",
        0x60b: "",
        0x60a: "",
        0x629: "",
        0x613: "",
        0x611: "",
        0x612: "",
        0x641: "",
        0x64b: "",
        0x64d: "",
        0x64f: "",
        0x651: "",

        # prone head b
        0x666: "FAD",
        0x662: "Elbow",
        0x663: "Jump Elbow",
        0x664: "Rk Elbow",
        0x665: "Lg Drop",
        0x6ad: "",
        0x6b0: "",
        0x667: "",
        0x668: "",
        0x6ae: "",
        0x66e: "",
        0x66f: "",
        0x670: "",
        0x674: "",
        0x675: "",
        0x67a: "",
        0x67b: "",
        0x67d: "",
        0x67e: "",
        0x682: "",
        0x683: "",
        0x684: "",
        0x68b: "",
        0x66d: "",
        0x6a0: "",
        0x669: "",
        0x66a: "",
        0x6af: "",
        0x694: "",
        0x66c: "",
        0x6a4: "",
        0x6a5: "",
        0x6ab: "",
        0x6a2: "",
        0x6a3: "",
        0x6a1: "",

        # prone leg b
        0x6b1: "",
        0x6b2: "",
        0x6d4: "",
        0x6c0: "",
        0x6c1: "",
        0x6c4: "",
        0x6c6: "",
        0x6c9: "",
        0x6cc: "",
        0x6b6: "",
        0x6b7: "",
        0x6b8: "",
        0x6b9: "",
        0x6ba: "",
        0x6bb: "",
        0x6b5: "",
        0x6bc: "",
        0x6bd: "",
        0x6d7: "",
        0x6be: "",
        0x6b3: "",
        0x6b4: "",
        0x6df: "",
        0x6bf: "",
        0x6e6: "",
        0x6e7: "",
        0x6e8: "",
        0x6e3: "",
        0x6e5: "",
        0x6e1: "",      

        # Corner Grab + C + U/Corner Grab + C + LR/Corner Grab + C + D
        0x6ee: "Middle Rope Suplex",
        0x6ef: "Superplex",
        0x6f0: "Belly2Back Release",
        0x6f1: "Fisherman Suplex",
        0x6f2: "Top Rope Gut",
        0x6f3: "DDT",
        0x6f4: "Hurricanrana",
        0x6f5: "Chokeslam",
        0x6fe: "Tomestone",
        0x70a: "Head Butt",
        0x73d: "High Chops",
        0x70b: "Flair Chops",
        0x712: "Wheel Kick",
        0x70e: "Back Clubs",
        0x70d: "Flurry",
        0x713: "Shoulder",
        0x70f: "Mudhole",
        0x710: "Knees",
        0x711: "Low Dropkick",
        0x740: "OK Stampede",
        0x717: "Taker",
        0x716: "Taker2",
        0x73b: "Stungun",
        0x73f: "Body Press",
        0x73c: "RVD Sault",
        0x714: "Tornado",
        0x715: "Spin DDT",
        0x73a: "Apron Slam",
        0x748: "Top Rope Backdrop",
        0x74b: "Back Destroyer",
        0x74a: "RV2Arm",
        0x74c: "S Bomb",

        # performance L/R
        0x792: "Hand Up",
        0x793: "Fist Up 1",
        0x794: "Fist Up 2",
        0x795: "Arm Pump",
        0x797: "Arm Roll",
        0x80d: "Flex Raise",
        0x7b1: "Number One",
        0x7ba: "Long Horn",
        0x7a7: "Whip",
        0x809: "Circle",
        0x79b: "Find You",
        0x798: "Flex",
        0x7fb: "Flex + Fist",
        0x7c9: "Cross Wave",
        0x791: "Yeah",
        0x79e: "Rampage",
        0x79f: "Two Arm",
        0x808: "Come On",
        0x7a0: "Clap",
        0x79a: "Two Arms Up",
        0x79c: "Scream",
        0x7ab: "Rays",
        0x80a: "Ripsaw",
        0x7a6: "Slice",
        0x7bf: "Delphin",
        0x80c: "Flip",
        0x7ce: "Backflip",
        0x80b: "Flip Flex",
        0x7cc: "Green Mist",
        0x7f3: "Jeff",
        0x7b8: "Oh!",
        0x7bb: "Peace",
        0x7b9: "Diesel",
        0x796: "Spirit",
        0x7f8: "Fist Pull",
        0x7a3: "Poke",
        0x7b2: "Hey U!",
        0x7bc: "Bang! Bang!s",
        0x7a5: "Over",
        0x7a8: "Under",
        0x7aa: "Leap",
        0x79d: "Fist",
        0x7a2: "Cross Cut",
        0x7ac: "Buff",
        0x7be: "No",
        0x807: "No Drink",
        0x7e1: "Sting",
        0x7ee: "Ready Up",
        0x7bd: "Wow! Wow!",
        0x7c2: "Big",
        0x7ed: "Power",
        0x7b4: "Hogan",
        0x799: "Open Rage",
        0x7c6: "Belly",
        0x7a4: "Rude",
        0x7ca: "Marching",
        0x7a1: "X Finish",
        0x7b0: "Bow",
        0x7ae: "Pray",
        0x7af: "Bow Wave",
        0x7c1: "Pray 2",
        0x7cb: "Back Wave",
        0x7a9: "Sabu Point",
        0x7b3: "Sweep",
        0x7c0: "Swoop",
        0x7b5: "Scott Steiner",
        0x7b6: "Rick Steiner",
        0x7ad: "Wheel",
        0x7b7: "Begs",

        # front 2
        0x80e: "Team Suplex",
        0x810: "Team Dropkick",
        0x811: "Team Power Bomb",

        # front 3
        0x832: "Triple Beatdown",

        # back 2
        0x81d: "Double Backdrop",
        0x81e: "Otoshi + Backdrop",

        # back 3
        0x83b: "Triple Beatdown Back",

        # corner 2
        0x826: "Combination DDT",
        0x827: "Hijack Piledriver",
        0x828: "Top Rope Team Bulldog",
        0x829: "Top Rope Backdrop + Neckbreaker",

        # corner 3
        0x844 : "Triple Power Bomb Corner",
        0x845 : "Doomsday Device",
        0x846 : "Triple Hammer Corner",
    }

    if moveId not in moves:

        return("Unknown move " + str(moveId) + " " + hex(moveId))

    return moves[moveId]

#
# Logic
#

def displayLogic(logic, count, numChoices):

    logic = logic[:numChoices]

    print("Logic " + str(count) + ": ", end="")
    lastVal = 0
    for l in logic:
        print(str(l - lastVal) + " ", end="")
        lastVal = l
    print(str(100 - lastVal))

def parseLogic(logic):

    displayLogic(logic, 1, 6)
    logic = logic[6:]

    displayLogic(logic, 2, 6)
    logic = logic[6:]

    displayLogic(logic, 3, 14)
    logic = logic[14:]

    displayLogic(logic, 4, 14)
    logic = logic[14:]

    displayLogic(logic, 5, 14)
    logic = logic[14:]

    displayLogic(logic, 6, 5)
    logic = logic[5:]

    displayLogic(logic, 7, 5)
    logic = logic[5:]

    displayLogic(logic, 8, 5)
    logic = logic[5:]

    displayLogic(logic, 9, 5)
    logic = logic[5:]

    displayLogic(logic, 10, 5)
    logic = logic[5:]

    displayLogic(logic, 11, 5)
    logic = logic[5:]

    displayLogic(logic, 12, 2)
    logic = logic[2:]

    displayLogic(logic, 13, 2)
    logic = logic[2:]

    displayLogic(logic, 14, 2)
    logic = logic[2:]

    displayLogic(logic, 15, 4)
    logic = logic[4:]

    displayLogic(logic, 16, 4)
    logic = logic[4:]

    displayLogic(logic, 17, 3)
    logic = logic[3:]

    displayLogic(logic, 18, 3)
    logic = logic[3:]

    displayLogic(logic, 19, 6)
    logic = logic[6:]

    displayLogic(logic, 20, 6)
    logic = logic[6:]

    displayLogic(logic, 21, 5)
    logic = logic[5:]

    displayLogic(logic, 22, 5)
    logic = logic[5:]

    displayLogic(logic, 23, 1)
    logic = logic[1:]

    displayLogic(logic, 24, 3)
    logic = logic[3:]

    displayLogic(logic, 25, 2)
    logic = logic[2:]

    displayLogic(logic, 26, 2)
    logic = logic[2:]

    displayLogic(logic, 27, 2)
    logic = logic[2:]

    displayLogic(logic, 28, 2)
    logic = logic[2:]

    displayLogic(logic, 29, 1)
    logic = logic[1:]

    displayLogic(logic, 30, 1)
    logic = logic[1:]

    displayLogic(logic, 31, 1)
    logic = logic[1:]

    displayLogic(logic, 32, 1)
    logic = logic[1:]

    print("")

# calculate the number of edit points used
def calculateEditPoints(wrestler):

    points = 0

    critical = wrestler["CHARACTER_critical"]
    if critical == 0: # finisher
        points += 0
    elif critical == 1 or critical == 2: # suplex, power
        points += 20
    elif critical == 3: # technical
        points += 25
    elif critical == 4 or critical == 5: # striking, submission
        points += 30

    recover = wrestler["CHARACTER_recover"]
    points += (10*recover)

    recover_bloody = wrestler["CHARACTER_recover_bloody"]
    points += (5*recover_bloody)

    breath = wrestler["CHARACTER_breath"]
    points += (10*breath)

    breath_bloody = wrestler["CHARACTER_breath_bloody"]
    points += (5*breath_bloody)

    spirit = wrestler["CHARACTER_spirit"]
    points += (10*spirit)

    spirit_bloody = wrestler["CHARACTER_spirit_bloody"]
    points += (5*spirit_bloody)

    neck = wrestler["CHARACTER_neck_durability"]
    points += (2*neck)

    arms = wrestler["CHARACTER_arm_durability"]
    points += (2*arms)

    waist = wrestler["CHARACTER_waist_durability"]
    points += (2*waist)

    legs = wrestler["CHARACTER_leg_durability"]
    points += (2*legs)

    move_speed = wrestler["CHARACTER_movement_speed"]
    points += (4*(move_speed-3))

    ring_climb = wrestler["CHARACTER_climbing_speed"]
    points += (2*(ring_climb-3))

    can_climb = wrestler["CHARACTER_climb"]
    points += (8*can_climb)

    offense = 0
    defense = 0

    # subtract 3 because all values are already +2, and 1 counts as 0 pts
    for i in wrestler["ATTRIBUTES_offense"]:
        offense += (i - 3)

    points += offense

    for i in wrestler["ATTRIBUTES_defense"]:
        defense += (i -3)

    points += defense
    return points

#
# Misc
#
def areAllElementsZero(someBytes):
    for i in someBytes:
        if i != 0:
            return False

    return True

# returns the promotion (0-13) based on the wrestler num (0-160)
def getPromotionNumByWrestlerNum(wrestlerNum):

    if wrestlerNum < 0 or wrestlerNum > 159:
        print("Invalid wrestlerNum specified!!")
        sys.exit(-1)

    # default wrestlers
    if wrestlerNum >= 0 and wrestlerNum <= 23:
        # New Japan Pro-Wrestling
        return 0
    elif wrestlerNum >= 24 and wrestlerNum <= 30:
        # Heisei Ishingun
        return 1
    elif wrestlerNum >= 31 and wrestlerNum <= 50:
        # All Japan
        return 2
    elif wrestlerNum >= 51 and wrestlerNum <= 68:
        # Japan Independents
        return 3
    elif wrestlerNum >= 69 and wrestlerNum <= 79:
        # WAR
        return 4
    elif wrestlerNum >= 80 and wrestlerNum <= 88:
        # Michinoku Puroresu
        return 5
    elif wrestlerNum >= 89 and wrestlerNum <= 107:
        # America Style Pro Wrestling
        return 6
    elif wrestlerNum >= 108 and wrestlerNum <= 114:
        # UWF International
        return 7
    elif wrestlerNum >= 115 and wrestlerNum <= 123:
        # Rings
        return 8
    elif wrestlerNum >= 124 and wrestlerNum <= 124:
        # Fujiwara Gumi
        return 9
    elif wrestlerNum >= 125 and wrestlerNum <= 129:
        # Pancrase
        return 10
    elif wrestlerNum >= 130 and wrestlerNum <= 133:
        # Lucha Libre
        return 11
    elif wrestlerNum >= 134 and wrestlerNum <= 137:
        # Martial Arts
        return 12

    # hidden wrestlers
    if wrestlerNum == 138:
        return 3
    elif wrestlerNum == 139:
        return 0
    elif wrestlerNum == 140:
        return 2
    elif wrestlerNum == 141:
        return 13
    elif wrestlerNum == 142:
        return 11
    elif wrestlerNum == 143:
        return 11
    elif wrestlerNum == 144:
        return 12
    elif wrestlerNum == 145:
        return 3
    elif wrestlerNum == 146:
        return 2
    elif wrestlerNum == 147:
        return 2
    elif wrestlerNum == 147:
        return 2
    elif wrestlerNum == 148:
        return 2
    elif wrestlerNum == 149:
        return 3
    elif wrestlerNum == 150:
        return 6
    elif wrestlerNum == 151:
        return 14
    elif wrestlerNum == 152:
        return 14
    elif wrestlerNum == 153:
        return 14
    elif wrestlerNum == 154:
        return 5
    elif wrestlerNum == 155:
        return 2
    elif wrestlerNum == 156:
        return 0
    elif wrestlerNum == 157:
        return 0
    elif wrestlerNum == 158:
        return 0
    elif wrestlerNum == 159:
        return 0


    print("Invalid wrestlerNum specified2!!")
    sys.exit(-1)
    return None
