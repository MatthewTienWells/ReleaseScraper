from bs4 import BeautifulSoup
import requests
from flask import Flask
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


#Urls of upcoming media pages on different publishers' websites
NINTENDO = "https://www.nintendo.com/store/games/coming-soon/"
SONY = "https://www.playstation.com/en-us/ps5/games/"
MICROSOFT = "https://www.microsoft.com/en-us/store/coming-soon/games/xbox"

#initialize app class
app = Flask(__name__, static_url_path='', static_folder='static')

#Provides webpages when route url is called
@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/contact')
def contactpage():
    return app.send_static_file('contact.html')

@app.route('/about')
def aboutpage():
    return app.send_static_file('about.html')


@app.route("/getvideogames")
def videogames():
    """Collate video games- currently only does Nintendo. Returns a json
    data structure.
    """
    print('getting video games')
    results = []
    results += nintendo()
    print('Finished getting all video games')
    return json.dumps(results)


def nintendo():
    """Read through Nintendo's upcoming games with Selenium, then grab their
    release dates with BeautifulSoup. Returns a json-friendly list of games.
    """
    games = []
    driver.get(NINTENDO)
    print('Nintendo.com accessed')
    elem = driver.find_elements(
        By.CLASS_NAME,
        "BasicTilestyles__Tile-sc-sh8sf3-15"
        )
    for link in elem:
        game = link.get_attribute("href")
        page = requests.get(game)
        soup = BeautifulSoup(page.text, "html.parser")
        datesection = soup.find_all(text="Release date")
        if len(datesection) > 0:
            release_date = datesection[-1].findNext('div')
            games.append({
                'title':soup.title.string[0:-45],
                'publisher':"Nintendo",
                'mediatype':"Video Game",
                'releasedate':release_date.text
                })
    return games
        

#Start webserver
app.run(host='0.0.0.0', port=81)
            
        
            

