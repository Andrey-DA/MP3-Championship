import pandas as pd
import src.champfuncs as chp
from src.filefuncs import getLastDirName,isFileExist,checkDir
from src.trackcomparator import TrackComparator
from leaderboard import printLeaderBoard
import time
import argparse
import sys


if __name__ == "__main__":
    # Default parameters
    num_seconds = 7    
    musicdir = r"tracks/classic"
    # Setting parser
    parser = argparse.ArgumentParser(add_help=False)    
    parser.add_argument('-d','--musicdir', default=musicdir,help='Mp3 track directory')
    parser.add_argument('-s','--num_seconds', default=num_seconds,help='track playing interval')
    parser.add_argument('-h', '--help', action='store_true', 
                           help='Show help')    
    args = parser.parse_args()
    if args.help:
        parser.print_help()
        response = input("Press Enter, to quit...")   
        sys.exit(0)
    num_seconds = float(args.num_seconds)
    musicdir = args.musicdir
    print(f"Command string arguments: {num_seconds=} {musicdir=}")
    mp3champfilename= f"champs/mp3champ_{getLastDirName(musicdir)}.xls".replace(" ","_")
    #### Splash screen
    print(f"="*50)
    print("WELCOME TO MP3 CHAMPIONSHIP!!!!!!")
    print(f"You would listen random {num_seconds} seconds of Two tracks: you can chhose the winner (press 1 or 2) or make tie (press 3)")
    print(f"You can listen again another random seconds of tracks - just press 4, but the winner gain one point less!")
    time.sleep(1) 
    print("3....")
    time.sleep(1)  
    print("2....")
    time.sleep(1)
    print("1....")
    time.sleep(1)
    print("LET'S GO!")    
    time.sleep(0.2)
    ####
    # If we did not find a file with the given name, we create a new one:
    checkDir('champs')
    if isFileExist(mp3champfilename) is False:
        chp.initMp3Champ(musicdir,mp3champfilename)
    df = chp.LoadMp3Champ(mp3champfilename)
    # Let's go
    while True:
        try:
            df_match,tour,index1,index2 = chp.getNextMatch_v2(df)
            if df_match is None:
                print("Championship is over...")
                printLeaderBoard(mp3champfilename)
                # response = input("Press Enter, to quit...") 
                break
            print(f"{'='*20} {tour+1} ROUND {'='*20}:")
            win_points = 3
            tie_points = 1
            while True:
                for index,row in df_match.iterrows():
                    print(f"Playing track # {index+1}...")
                    chp.play_random_num_seconds_pygame(row['file_path'],num_seconds)
                comparator = TrackComparator()
                # Getting operator choice (without pressing Enter)
                choice = comparator.get_user_choice()
                if choice == 1:
                    df.loc[index1,'score'] += win_points
                    df.loc[index1,'wins'] += 1
                    df.loc[index2,'loses'] += 1
                elif choice == 2:
                    df.loc[index2,'score'] += win_points
                    df.loc[index2,'wins'] += 1
                    df.loc[index1,'loses'] += 1
                elif choice == 3:
                    df.loc[index1,'score'] += tie_points
                    df.loc[index2,'score'] += tie_points
                    df.loc[index1,'ties'] += 1
                    df.loc[index2,'ties'] += 1
                elif choice == 4:
                    win_points = 2
                if choice < 4:
                    df.loc[index1,'times_played'] += 1
                    df.loc[index2,'times_played'] += 1
                    df.loc[index1,'W-L-T'] = f"{df.loc[index1,'wins']}-{df.loc[index1,'loses']}-{df.loc[index1,'ties']}"
                    df.loc[index2,'W-L-T'] = f"{df.loc[index2,'wins']}-{df.loc[index2,'loses']}-{df.loc[index2,'ties']}"
                    df['matchindex'] += 1
                # Processing choice
                should_repeat = comparator.process_choice(choice)
                if not should_repeat:
                    break  # End cycle, id we don't want to listen again
            # Saving current champ after each battle
            df.to_csv(mp3champfilename, sep="|", encoding='utf-8')
        except KeyboardInterrupt:
            print("\nChamp interrupted by User (Ctrl+C)\n Current champ table:")
            printLeaderBoard(mp3champfilename)
            # response = input("Press Enter, to quit...") 
            sys.exit(0)
    response = input("Press Enter, to quit...")    
        

    
