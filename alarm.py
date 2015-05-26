from pydub import AudioSegment
from pydub import playback
import time

SONG_PATH = 'You Are All I See.mp3'

def play_song():
    print("Retrieving alarm...")
    song = AudioSegment.from_mp3(SONG_PATH)
    song = song[:10000] #first ten seconds
    song_duration = len(song)
    playback.play(song)
    #time.sleep(song_duration/1000)

if __name__ == '__main__':
    play_song()
