import pandas as pd
from src.champfuncs import LoadMp3Champ
from src.filefuncs import getFileList
import argparse
import os

def printLeaderBoard(mp3champfilename):
    """
    Print to console screen current champ standing of given mp3champfilename 
    """
    print(f"{'='*20} {mp3champfilename} {'='*20}")
    df = LoadMp3Champ(mp3champfilename)
    # Because some mp3 files may not contain all tags we get what we can
    fields_to_show = ['file_name','title','artist','album','times_played','W-L-T','score']
    fields_to_show_in_df = []
    for field in fields_to_show:
        if field in df.columns:
            fields_to_show_in_df.append(field)
    df_sorted = df.sort_values(by=['score','times_played'], ascending=[False,True])[fields_to_show_in_df].reset_index()
    df_sorted.index += 1   # for beginning first index from 1
    print(df_sorted.head(len(df_sorted)))
    response = input("Press Enter, to continue...") 


def printLeaderBoards(mp3champfilenames):
    """
    printLeaderBoard a whole bunch of championships given as mp3champfilenames
    """
    for mp3champfilename in mp3champfilenames:
        printLeaderBoard(mp3champfilename)


def main():
    mp3champfilenames = getFileList("./champs",".xls")

    parser = argparse.ArgumentParser(description='File processing')
    
    # Create mutual exclusive group
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--all', 
                      action='store_true',
                      help='Process all files in champ directory')
    group.add_argument('-f', '--file', 
                      type=str,
                      help='Process single file')
    
    args = parser.parse_args()
    
    # Business logic
    if args.file:
        mp3champfilename = os.path.join('./champs', args.file)
        if os.path.exists(filepath):
            printLeaderBoard(mp3champfilename)
        else:
            print(f"Error: '{args.file}' did not found in champs dicrectory")
    elif args.all:
        printLeaderBoards(mp3champfilenames)
    else:
        # If there is no paramteres proceesing all files in champs dir
        printLeaderBoards(mp3champfilenames)


if __name__ == "__main__":
    main()
