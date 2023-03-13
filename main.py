## Importing Necessary Modules

import sys
import os.path
import random
from time import strftime, gmtime
import threading
from time import sleep
from bs4 import BeautifulSoup

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal


import requests # to get image from the web
import shutil # to save it locally

class Backend(QObject):
    def __init__(self):
        QObject.__init__(self)    
    updated = pyqtSignal(str, arguments=['updater'])    
    def updater(self, curr_time):
        self.updated.emit(curr_time)    
    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()    
    def _bootUp(self):
        while True:
            curr_time = strftime("%H:%M:%S", gmtime())
            self.updater(curr_time)
            sleep(0.1)

def getURLs():
    
    url = 'https://apod.nasa.gov/apod/archivepix.html'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
 
    # Links to all APOD pages
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    urls = urls[4:-12]
    urls = ['https://apod.nasa.gov/apod/' + s for s in urls]
    
    # Get random link
    random_url= str(random.choice(urls))
    getURL = requests.get(random_url)
    soup = BeautifulSoup(getURL.text, 'html.parser')
    return soup

def getImage(soup):
    
        # Get image from link
    
    images = soup.find_all('img')
    imageSource = ''

    for image in images:
        imageSource += str(image.get('src'))

    image_url = 'https://apod.nasa.gov/apod/' + imageSource
    file_name = 'RAPOD.jpg'

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(file_name,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            
        print('Image successfully Downloaded: ',file_name)
    else:
        print('Image couldn\'t be retrieved')
    
def getExplanation(soup):
    explanation = soup.get_text()
    explanation = explanation.split()
    index1 = explanation.index('Explanation:') + 1
    index2 = explanation.index('Tomorrow\'s')
    explanation = explanation[index1:index2]
    explanation = ' '.join(explanation)

    return explanation
    
def getDateTitle(soup):
    date_title = soup.get_text()
    date_title = date_title.split()
    index1 = date_title.index('astronomer.') + 1
    index2 = date_title.index('Image')
    date_title = date_title[index1:index2]
    date = date_title[0:3]
    title = date_title[3:]
    date = ' '.join(date)
    title =' '.join(title)
    print(date)
    print(title)
    return date, title




url = getURLs()
getImage(url)





QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./main.qml')
back_end = Backend()
engine.rootObjects()[0].setProperty('backend', back_end)
back_end.bootUp()
sys.exit(app.exec())