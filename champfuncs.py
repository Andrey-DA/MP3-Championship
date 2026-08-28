import pandas as pd
from filefuncs import getRecursiveFileList
from mutagen.mp3 import MP3
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TRCK, TCON, APIC
from mutagen.easyid3 import EasyID3
# Для воспроизведения аудио
import pygame
import random
import time
import ast
from functools import lru_cache

def round_robin_pairs(k):
    """
    Generates a round-robin tournament schedule for k tracks (numbers 0 to k-1). 
    Returns a list of rounds, each round contains a list of pairs (a, b).
    """
    # Add a dummy track if k is odd.
    n = k if k % 2 == 0 else k + 1
    
    # Teams: 0, 1, 2, ..., n-2 (all except the dummy)
    # Dummy track = n-1
    circle = list(range(0, n - 1))  # [0, 1, 2, ..., n-2]
    fixed = n - 1  # Dummy track 
    
    all_rounds = []
    
    for r in range(n - 1):
        current_round = []
        
        # Pair with dummy track
        current_round.append((fixed, circle[0]))
        
        # Other pairs
        for i in range(1, n // 2):
            current_round.append((circle[i], circle[n - 1 - i]))
        
        # Remove pairs with dummy track (if k is odd)
        if k % 2 != 0:
            current_round = [(a, b) for a, b in current_round 
                           if a != fixed and b != fixed]
        
        all_rounds.append(current_round)
        
        # Spin the circle (first track goes to the end)
        circle = circle[1:] + [circle[0]]
   
    return all_rounds

@lru_cache(maxsize=1024) 
def round_robin_pairs_flat(k):
    all_matches = round_robin_pairs(k)
    all_marches_flat = []
    for tour in all_matches:
        for one_match in tour:
            all_marches_flat.append(one_match)
    return all_marches_flat 

def play_random_num_seconds_pygame(file_path,num_seconds=5):
    """
    Play track random num_seconds block using pygame.
    """
    try:
        # Initialize pygame mixer
        pygame.mixer.init()
        audio = MP3(file_path)
        duration = audio.info.length  # getting track duration
        
        # get ranfod track num_seconds interval
        if duration <= num_seconds:
            print(f"Файл короче {num_seconds} секунд ({duration:.1f} сек), проигрываем полностью")
            start_time = 0
            play_duration = duration
        else:
            max_start = duration - num_seconds
            start_time = random.uniform(0, max_start)
            play_duration = num_seconds
            print(f"Проигрываем отрезок: {start_time:.1f} - {start_time + num_seconds:.1f} секунд")
        
        pygame.mixer.music.load(file_path)          # Loading and playing file
        pygame.mixer.music.play(start=start_time)   # begin playing
        time.sleep(play_duration)                   # Waiting while playing
        pygame.mixer.music.stop()                   # stop playing
        pygame.mixer.quit()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def fix_cyrrilic_encoding_wrong(text):
    """
    Fixes a Cyrillic string that was incorrectly decoded.
    Latin-1 (ISO-8859-1) -> Windows-1251
    Most often works for such cases.
    """
    return text.encode('latin-1').decode('cp1251')


def extract_mp3_metadata(file_path):
    """
    Extracting metadata from mp3 file
    """
    try:
        audio = MP3(file_path)
        
        # Main metadata dict
        metadata = {
            'file_path': str(file_path),
            'file_name': os.path.basename(file_path),
            'duration_seconds': round(audio.info.length, 2),
            'bitrate_kbps': round(audio.info.bitrate / 1000, 1),
            'sample_rate_hz': audio.info.sample_rate,
            'channels': audio.info.channels,
            'file_size_mb': round(os.path.getsize(file_path) / (1024 * 1024), 2)
        }
        
        # trying to get ID3 tags
        try:
            tags = EasyID3(file_path)
            
            # Main tags (with EasyID3 help)
            metadata['title'] = tags.get('title', [''])[0]
            metadata['artist'] = tags.get('artist', [''])[0]
            metadata['album'] = tags.get('album', [''])[0]
            metadata['album'] = fix_cyrrilic_encoding_wrong(metadata['album'])
            metadata['artist'] = fix_cyrrilic_encoding_wrong(metadata['artist'])
            metadata['title'] = fix_cyrrilic_encoding_wrong(metadata['title'])
            metadata['genre'] = tags.get('genre', [''])[0]
            metadata['date'] = tags.get('date', [''])[0]  
            metadata['tracknumber'] = tags.get('tracknumber', [''])[0]
            
        except:
            # If EasyID3 didm't work trying using ID3
            try:
                tags = ID3(file_path)
                metadata['title'] = str(tags.get('TIT2', [''])[0]) if tags.get('TIT2') else ''
                metadata['artist'] = str(tags.get('TPE1', [''])[0]) if tags.get('TPE1') else ''
                metadata['album'] = str(tags.get('TALB', [''])[0]) if tags.get('TALB') else ''
                metadata['genre'] = str(tags.get('TCON', [''])[0]) if tags.get('TCON') else ''
                metadata['date'] = str(tags.get('TDRC', [''])[0]) if tags.get('TDRC') else ''
                metadata['tracknumber'] = str(tags.get('TRCK', [''])[0]) if tags.get('TRCK') else ''
            except:
                # If there are no tags - leaving empty strings
                pass
        
        # Check for album covers
        try:
            tags = ID3(file_path)
            has_cover = any(isinstance(frame, APIC) for frame in tags.values())
            metadata['has_cover_art'] = has_cover
        except:
            metadata['has_cover_art'] = False
        metadata['score'] = 0
        metadata['times_played'] = 0
        return metadata
        
    except Exception as e:
        print(f"Error while reading {file_path}: {e}")
        return None

def create_metadata_dataframe(file_list):
    """
    Takes a list of paths to MP3 files and returns a DataFrame with metadata.
    """
    all_metadata = []
    
    for file_path in file_list:
        if os.path.exists(file_path):
            metadata = extract_mp3_metadata(file_path)
            if metadata:
                all_metadata.append(metadata)
        else:
            print(f"File not found: {file_path}")
    
    # Creating DataFrame
    df = pd.DataFrame(all_metadata)
    df['next_adversary'] = [[] for _ in range(len(df))]
    df['matchindex'] = [0 for _ in range(len(df))]

    # Convert data types for convenience.
    if not df.empty:
        # Convert track_number field to a number (if present).
        if 'tracknumber' in df.columns:
            df['tracknumber'] = df['tracknumber'].str.split('/').str[0].astype(float, errors='ignore')
            # Sorting by artist and track_number
            df = df.sort_values(['artist', 'tracknumber'], na_position='last')        
        # Add a column with human-readable duration.
        df['duration_formatted'] = df['duration_seconds'].apply(
            lambda x: f"{int(x//60)}:{int(x%60):02d}"
        )
        

    
    return df

def initMp3Champ(musicdir,
                 mp3champfilename="mp3champ.xls"):
    random.random()
    mp3filenames = getRecursiveFileList(musicdir,filterstr="*.mp3")
    df = create_metadata_dataframe(mp3filenames)
    print("====== NEW MP3-championship ======")
    print(df.head(20))
    df = df.sample(frac=1).reset_index(drop=True)      # shuffling tracks
    k= len(df)
    all_matches = round_robin_pairs(k)
    # Building adversary track list (right now - it's obsolete, but maybe it will come in handy later...
    for tour in all_matches:
        for one_match in tour:
            print(f"{one_match[0]} vs {one_match[1]}")
            df.at[one_match[0],'next_adversary'].append(one_match[1])
            df.at[one_match[1],'next_adversary'].append(one_match[0])
    df.to_csv(mp3champfilename, sep="|", encoding='utf-8')
    print(f"Mp3-championship saved to {mp3champfilename}.")


def LoadMp3Champ(dffilename):
    df = pd.read_csv(dffilename,sep="|", encoding='utf-8')
    df['next_adversary'] = df['next_adversary'].apply(ast.literal_eval)
    print(f"====== Mp3-championship loaded from {dffilename}")
    return df


def getTwoRandomTracks(df):
    """
    Obsolete function that get two random tracks for battle
    Now two tracks selected from champ-grid     
    """
    min_times_played = df['times_played'].min()
    result = df[df['times_played'] == min_times_played]
    if len(result) > 1:
        result = result.sample(n=2)    
    elif len(result) < 2:
        result2 = df[df['times_played']==min_times_played+1].sample(n=1)
        result = pd.concat([result,result2])
    result = result.reset_index()
    return result,min_times_played


def getNextMatch(df):
    """
    First version of champ-grid function, works good with even-numbered champs
    but slightly wrong with odd-numbered (now obsolete)
    Main advantage: doesn't care about champ history? trying two found battle
    only using info on times_played and times_played field
    """
    min_times_played = df['times_played'].min()
    if min_times_played == len(df)-1:
        return None,min_times_played,None,None
    # Отбираем строки с этим значением и берем 2 случайных
    result = df[df['times_played'] == min_times_played]
    # df_track1 = result.sample(n=1)
    df_track1 = result.iloc[[0]]
    index1 = result.index[0]
    index2 = result.loc[index1,'next_adversary'][min_times_played]
    df_track2 = df.loc[[index2]]
    result = pd.concat([df_track1,df_track2])
    return result,min_times_played,index1,index2


def getNextMatch_v2(df):
    """
    Right now it's main get next battle function
    Get next match in round-robin algo and does'nt give a f**k, works good
    with both even-bumbered and odd-numbered champs
    """
    matchindex = df.loc[0,'matchindex']
    all_matches = round_robin_pairs_flat(len(df))
    min_times_played = df['times_played'].min()
    if min_times_played == len(df)-1:
        return None,min_times_played,None,None
    index1,index2 = all_matches[matchindex]
    df_track1 = df.loc[[index1]]
    df_track2 = df.loc[[index2]]
    result = pd.concat([df_track1,df_track2])
    return result,min_times_played,index1,index2


