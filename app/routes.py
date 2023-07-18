from cgitb import text
from bs4 import BeautifulSoup
import requests
from markupsafe import escape
from flask import jsonify
from app import app
from cryptography.fernet import Fernet

domain = "https://www.themoviedb.org"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/517.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/517.36"} 


f = Fernet(b'u6XOwSZ7JZvr8ibrixGZY6rBsrTMG4gD-GTlIl39Eq0=')
@app.route('/')
def index():
    return jsonify({
        "movie_links": response_maker(""),
        "now_playing_links": response_maker("/now-playing"),
        "upcoming_links": response_maker("/upcoming"),
        "top_rated_links": response_maker("/top-rated"),
    })
def response_maker(sub_path):
    response = requests.get(f"{domain}/movie"+sub_path, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    movie_soup =  soup.select("div#page_1 > div.card.style_1")
    # list scraper 
    temp_list = []
    for  l in movie_soup:
        image = l.select_one("div.image img")
        if image :
            final_image = image["src"].replace("/t/p/w220_and_h330_face","")

            link = l.select_one("div.content > h2 a")["href"]
            title = l.select_one("div.content > h2 a").text.strip()
            ratings = l.select_one("div.content div.percent span")["class"][1]
            temp_list.append({
                "type":link.split("/")[1].capitalize() if link.split("/")[1] == "movie" else  "TV Series" ,
                "id":link.split("/")[2],
                "image": f"https://www.themoviedb.org/t/p/original{final_image}",
                "title": title,
                "ratings": 0 if ratings.replace("icon-r","") == "NR" else  ratings.replace("icon-r","")
            })


    return temp_list


def encryptor(text):
    temp_bytes = f.encrypt(text.encode())
    bytes_to_string = temp_bytes.decode("utf-8")
    return bytes_to_string

