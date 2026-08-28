import champfuncs as chp
import pandas as pd
from filefuncs import getLastDirName,isFileExist
from trackcomparator import TrackComparator
from leaderboard import printLeaderBoard
import time


if __name__ == "__main__":
    num_seconds = 7    
    musicdir = r"tracks\\classic"
    mp3champfilename= f"mp3champ_{getLastDirName(musicdir)}.xls".replace(" ","_")
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
    print("LET'S GO")    
    time.sleep(0.2)
    ####
    if isFileExist(mp3champfilename) is False:
        chp.initMp3Champ(musicdir,mp3champfilename)
    df = chp.LoadMp3Champ(mp3champfilename)
    # Поехали
    while True:
        try:
            df_match,tour,index1,index2 = chp.getNextMatch_v2(df)
            if df_match is None:
                print("Championship is over...")
                printLeaderBoard(mp3champfilename)
                break
            print(f"{'='*20} {tour+1} ROUND {'='*20}:")
            win_points = 3
            tie_points = 1
            while True:
                for index,row in df_match.iterrows():
                    print(f"Playing track # {index+1}...")
                    chp.play_random_num_seconds_pygame(row['file_path'],num_seconds)
                comparator = TrackComparator()
                # Получаем выбор оператора (без Enter)
                choice = comparator.get_user_choice()
                if choice == 1:
                    df.loc[index1,'score'] += win_points
                elif choice == 2:
                    df.loc[index2,'score'] += win_points
                elif choice == 3:
                    df.loc[index1,'score'] += tie_points
                    df.loc[index2,'score'] += tie_points
                elif choice == 4:
                    win_points = 2
                if choice < 4:
                    df.loc[index1,'times_played'] += 1
                    df.loc[index2,'times_played'] += 1
                    df['matchindex'] += 1
                # Обрабатываем выбор
                should_repeat = comparator.process_choice(choice)
                # should_repeat = False  Для отладки
                if not should_repeat:
                    break  # Выходим из цикла, если не выбрано "прослушать ещё раз"
                # Если выбрано "прослушать ещё раз", цикл продолжается
            # Сохраняем в файл
            df.to_csv(mp3champfilename, sep="|", encoding='utf-8')
        except KeyboardInterrupt:
            print("\nChamp interrupted by User (Ctrl+C)\n Current champ table:")
            printLeaderBoard(mp3champfilename) 
            sys.exit(0)   
        

    