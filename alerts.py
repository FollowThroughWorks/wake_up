# ADD AUDIO STREAM TO potd_poetry_foundation

import pywapi # For weather
from urllib import request
from bs4 import BeautifulSoup, NavigableString

# Weather information
class forecast_info:
    def __init__(self,zip_in):
        zip_code = zip_in
        
        weather = pywapi.get_weather_from_weather_com(zip_code,units='imperial')
        weather_today = weather['forecasts'][0]
        
        self.location = weather['location']['name'].split('(')[0]

        self.temp_high = weather_today['high']
        self.temp_low = weather_today['low']
        self.day_humidity = weather_today['day']['humidity']
        self.day_precip = weather_today['day']['chance_precip']
        self.night_humidity = weather_today['night']['humidity']
        self.night_precip = weather_today['night']['chance_precip']
        self.sunrise = weather_today['sunrise']
        self.sunset = weather_today['sunset']

# Poem of the day from Poets.org
class potd_poets_org:
    def __init__(self):
        # Get poem
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
        with request.urlopen(r'http://www.poetryfoundation.org/features/audio?show=Poem%20of%20the%20Day') as web_page:
            page_contents = web_page.read()
            soup = BeautifulSoup(page_contents)
            
            poem_url_end = soup.find("a",class_="title lightview").get('href').split('?')[0]
            poem_url = r'http://www.poetryfoundation.org{}'.format(poem_url_end)

            audio_url_end = soup.find(class_="relatedlinks").find(class_="linklist").li.a.get('href')
            audio_url = r'http://www.poetryfoundation.org{}'.format(audio_url_end)

            # ADD STREAM AUDIO

        # Get poem
        with request.urlopen(poem_url) as poem_page:
            page_contents = poem_page.read()
            soup = BeautifulSoup(page_contents)
            poem_html = soup.find(class_="poem")

            self.title = soup.find(id="poem-top").h1.get_text()
            self.author = soup.find(class_="author").a.get_text()
            self.lines = [line.get_text() for line in poem_html.find_all("div")]
