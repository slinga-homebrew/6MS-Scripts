# Fire Pro Wrestling S: 6Men Scramble Scripts
[Fire Pro Wrestling S: 6Men Scramble](https://segaretro.org/Fire_Pro_Wrestling_S:_6Men_Scramble) game and save game editing scripts. These scripts can:
- list/insert wrestlers renames from/into a save game or directly into the game itself
- list/insert promotion renames from/into a save game or directly into the game itself
- dump builtin wrestlers from the game to JSON
- dump create-a-wrestler edits from a save game to JSON
- insert wrestlers to a save game
- insert wrestlers overwriting a builtin wrestler

Some more advanced features:
- create an edit that uses more than the 255 skill points
- create an edit that has every move set to finisher
- replace a builtin wrestler with an edit
- copy a builtin wrestler to an edit slot, edit them, and copy them back

# Usage
## saveedit.py
saveedit.py is used for listing\inserting wrestler edits, promotion names, and wrestler names into a save game file. Both internal and cart save file formats are supported. The input\output files can be used interchangeably with binedit.py.

### Edits
python3 saveedit.py --input_save FPS.6MEN.01 --list_edits
- dumps all the edits (create-a-wrestlers) to JSON files
- This JSON file can be edited and reinserted back to the save or inserted directly into the game overwriting an existing wrestler

python3 saveedit.py --input_save FPS_6MEN.01 --output_save FPS_6MEN.01.edited --insert_edit edit_1.json --edit_slot 1 --appearance_number 0
- inserts a wrestler JSON file into the specified edit slot in the save
- the JSON file can be either an edit or a builtin wrestler JSON
- the edited save is specified by --output_save
- --appearance_number is optional and specifies which of the appearances to use for the wrestler. Builtin wrestlers have 6 appearances (0-5) whereas edits only have one. When copying a builtin to an edit slot you can specify which appearance to use. The numbers correspond to the buttons as follows: z = 0, y = 1, x = 2, b = 3, c = 4, and a = 5.

### Promotions
python3 saveedit.py --input_save FPS.6MEN.01 --list_promotions > promotions.txt
- dumps all of the promotion names to a UTF-8 encoded file
- this UTF-8 encoded file can be edited and reinserted back to the save or insterted directly into the game

python saveedit.py --input_save FPS_6MEN.01 --output_save FPS_6MEN.01.edited --insert_promotions promotions.txt
- inserts UTF-8 encoded promotions.txt file into the save

### Wrestler Names
python3 saveedit.py --input_save FPS.6MEN.01 --list_wrestlers > wrestlers.txt
- dumps all of the wrestler names to a UTF-8 encoded file
- this UTF-8 encoded file can be edited and reinserted back to the save or insterted directly into the game

python saveedit.py --input_save FPS_6MEN.01 --output_save FPS_6MEN.01.edited --insert_wrestlers wrestlers.txt
- inserts UTF-8 encoded wrestlers.txt file into the save

## binedit.py
binedit.py is used for listing\inserting builtin wrestlers, promotion names, and wrestler names into a save game file. Both internal and cart save file formats are supported. The input\output files can be used interchangeably with saveedit.py. The script requires 1ST.BIN and FPS.SBL from the Fire Pro disc.

### Builtins
python3 binedit.py --input_1st 1ST.BIN --input_fps FPS.SBL --list_builtins
- dumps all 160 builtin wrestlers to JSON files
- These JSON files can be edited and reinserted back to the save or inserted directly into the game overwriting an existing wrestler

python3 binedit.py --input_1st 1ST.BIN --output_1st 1ST.BIN.edited --input_fps FPS.SBL --output_fps FPS.SBL --insert_builtin builtin_153.json --builtin_slot 0
- inserts the specified wrestler to the specified builtin slot
- it is possible to insert an edit and replace an existing wrestler
- Caveat: The builtin wrestler's promotion number cannot change or the wrestler will not appear in the listing
- Caveat: Builtin wrestlers have 6 outfits, edits only have 1.

### Promotions
python3 binedit.py --input_1st 1ST.BIN --list_promotions > promototions.txt
- dumps all of the promotion names to a UTF-8 encoded file
- this UTF-8 encoded file can be edited and reinserted back to the save or insterted directly into the game

python3 binedit.py --input_1st 1ST.BIN --output_1st 1ST.BIN.edited --insert_promotions promotions.txt
- inserts UTF-8 encoded promotions.txt file into the save
- Caveat: If you already have a Fire Pro save, the rename information is taken from there and not from the game. So you must either delete your save or insert the renamed promotions into the save file.

### Wrestler Names
python3 binedit.py --input_1st 1ST.BIN --list_wrestlers > wrestlers.txt
- dumps all of the wrestler names to a UTF-8 encoded file
- this UTF-8 encoded file can be edited and reinserted back to the save or insterted directly into the game

python3 binedit.py --input_1st 1ST.BIN --output_1st 1ST.BIN.edited --insert_wrestlers wrestlers.txt
- inserts UTF-8 encoded wrestlers.txt file into the save
- Caveat: If you already have a Fire Pro save, the rename information is taken from there and not from the game. So you must either delete your save or insert the renamed promotions into the save file.

## parsewrestler.py
parsewerstler.py is a script used to dump information about the wrestler JSON file. Example usage: python3 parsewrestler.py builtin_153.json.

# Frequently Asked Questions
1) How do I get my save game off the Saturn?
Answer: See [Retroreversing.com](https://www.retroreversing.com/sega-saturn-save-data/)

2) How do I get my save game back to the Saturn?
Answer: See [Retroreversing.com](https://www.retroreversing.com/sega-saturn-save-data/)

3) I inserted my wrestler into the game and everything works except for his name is wrong.
Answer: Fire Pro has a list of wrestler renames in the save game. Your options would be to either 1) delete your save 2) rename the wrestler using the games builtin rename option or 3) use the binedit.py and saveedit.py scripts to dump the wrestler names and insert them into your save.

4) I inserted my wrestler into the game and everything works except his palette is slightly off. What gives?
Long story short see notes/builtin_palettes.txt. TL;DR while edits can use all possible combinations of RGB values, the builtins cannot. Use one of the predefined palettes in builtin_palettes.txt and you can avoid this issue.

# Credits
- Thank you to Malenko for pretty much translating Fire Pro Wrestling S by himself. I hope my scripts saved you at least a little bit of time
- Thank you to A Murder of Crows for bouncing ideas off of and providing reference wrestler templates
