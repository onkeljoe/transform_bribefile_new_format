# transform bribefiles to new format
batch add general reward key to bribefiles

## start
python app.py

## folders
./oldfiles -> keeps original data files
./newfiles -> transformed files will be saved here

## format switch
set const NEW_FORMAT_ONLY = True to create files without old reward types, NEW_FORMAT_ONLY = False to create files with combined old and new format