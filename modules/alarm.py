from pydub import AudioSegment
from pydub import playback
import time

class sound():
    def __init__(self,song_path='bugle.mp3'):
        print("Retrieving alarm...")
        self.audio = AudioSegment.from_mp3(song_path)
        self.length = len(self.audio)/1000
    
    def play(self,duration_secs):
        audio = self.audio[:(duration_secs*1000)]
        audio_duration = len(audio)
        playback.play(audio)
        #time.sleep(song_duration/1000)

if __name__ == '__main__':
    s = sound()
    s.play_song(3)
