import pandas as pd
from champfuncs import LoadMp3Champ
from filefuncs import getFileList


def printLeaderBoard(mp3champfilename):
    print(f"{'='*20} {mp3champfilename} {'='*20}")
    df = LoadMp3Champ(mp3champfilename)
    # Because some mp3 files may not contain all tags we get what we can
    fields_to_show = ['file_name','title','artist','album','score','times_played']
    fields_to_show_in_df = []
    for field in fields_to_show:
        if field in df.columns:
            fields_to_show_in_df.append(field)
    df_sorted = df.sort_values(by=['score','times_played'], ascending=[False,True])[fields_to_show_in_df].reset_index()
    df_sorted.index += 1   # for beginning first index from 1
    print(df_sorted.head(len(df_sorted)))


if __name__ == "__main__":
    mp3champfilenames = getFileList(".",".xls")
    for mp3champfilename in mp3champfilenames:
        printLeaderBoard(mp3champfilename)
