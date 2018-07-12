from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/movie/<moviename>")
def movie(moviename):
    JSONObject = getJSON(moviename)
    return JSONObject

def getJSON(moviename):
    movienameAsString=str(moviename)
    if movienameAsString=="moviename":
        return "Please replace 'moviename' with a movie title. For instance, http://localhost:5000/movie/inception"
    movienameAsString=movienameAsString.replace(' ','+')
    rawLink="http://www.imdb.com/find?&q="
    imdbLink=rawLink+movienameAsString

    try:
    	response=requests.get(imdbLink)
    except:
    	return "SERVER ERROR"
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    try:
        link=soup.find('table',class_='findList')
        link=link.find('a')
        link=link.get('href')
    except:
        return "NULL"
    imdbCode=link[:16][::-1][:-7][::-1]
    response=requests.get("http://www.yifysubtitles.com/movie-imdb/"+imdbCode)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    listOfRatings=[]
    listOfLinks=[]
    for article in soup.find_all('tr'):
        data=article.text
        if "English" in data:
            for a in article.find_all('span',class_='label label-success'):
                listOfRatings.append(int(a.text))
                listOfLinks.append(str(article.a.get('href')))
    subtitles = dict(zip(listOfRatings, listOfLinks))
    allLinks=[]
    constant_url="http://www.yifysubtitles.com/subtitle/"
    for i in sorted(subtitles):
        allLinks.append(subtitles[i])
    if allLinks==[]:
        return "NO LINKS FOUND"
    else:
        url=allLinks[-1].split('/')[2]
        p1 = "{"
        p2 = "link"
        p3 = ":"
        p4 = '"'
        p5 = constant_url+url+".zip"
        p6 = "}"
        return p1+p4+p2+p4+p3+p4+p5+p4+p6
if __name__=='__main__':
    app.run(debug=True)
