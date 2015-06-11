from pydub import AudioSegment
from pydub import playback
import time

def play_song(duration_secs,song_path='music/bugle.mp3'):
    print("Retrieving alarm...")
    song = AudioSegment.from_mp3(song_path)
    song = song[:(duration_secs*1000)] #first ten seconds
    song_duration = len(song)
    playback.play(song)
    #time.sleep(song_duration/1000)

if __name__ == '__main__':
    play_song()
