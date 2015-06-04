# Poetry
from urllib import request # web access
from bs4 import BeautifulSoup, NavigableString # For navigating html
from io import BytesIO # to convert mp3 url to io object
from pydub import playback, AudioSegment # to read poem

# Poem of the day from Poets.org
class potd_poets_org:
    def __init__(self):
        # Get poem
        print("Retrieving poem info...")
        with request.urlopen(r'http://www.poets.org/poetsorg/poem-day') as web_page:
            page_contents = web_page.read()
            soup = BeautifulSoup(page_contents)

            self.title = soup.find(id="poem-content").h1.get_text()
            self.author = soup.find(id="poem-content").h2.get_text().split(',')[0]
            poem_html = soup.find(id="poem-content").find("p").contents
            self.lines = [item for item in poem_html if isinstance(item,NavigableString)]          

# Poem of the day from the poetry foundation
class potd_poetry_foundation:
    def __init__(self):
        # Get poem url
        print("Retrieving poem info...")
        with request.urlopen(r'http://www.poetryfoundation.org/features/audio?show=Poem%20of%20the%20Day') as web_page:
            page_contents = web_page.read()
            soup = BeautifulSoup(page_contents)

            self.title = soup.find(class_="title large").get_text()
            self.author = soup.find(class_="author").get_text()

            audio_url_end = soup.find(class_="relatedlinks").find(class_="linklist").li.a.get('href')
            self.audio_url = r'http://www.poetryfoundation.org{}'.format(audio_url_end)
            
            try:
                poem_url_end = soup.find("a",class_="title lightview").get('href').split('?')[0]
                self.poem_url = r'http://www.poetryfoundation.org{}'.format(poem_url_end)

                with request.urlopen(self.poem_url) as poem_page:
                    page_contents = poem_page.read()
                    soup = BeautifulSoup(page_contents)
                    poem_html = soup.find(class_="poem")
                    
                    self.lines = [line.get_text() for line in poem_html.find_all("div")]
                    
            except AttributeError:
                self.lines = ["This poem text is not available."]



    def read_poem(self):
        mp3 = request.urlopen(self.audio_url).read()
        poem = AudioSegment.from_mp3(BytesIO(mp3))
        playback.play(poem)

if __name__ == '__main__':
    print(potd_poets_org().lines)
    print(potd_poetry_foundation().lines)
