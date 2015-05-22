from pydub import AudioSegment
from pydub import playback
import time

def play_song():
    song = AudioSegment.from_mp3('C:/m/Kalimba.mp3')
    song = song[:10000] #first ten seconds
    song_duration = len(song)
    playback.play(song)
    #time.sleep(song_duration/1000)

if __name__ == '__main__':
    play_song()
