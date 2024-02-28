import os

from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)
@app.route('/', methods = ['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', method = ['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            amazon_url= "https://www.amazon.in/s?k=" + searchString
            uClient = uReq(amazon_url)
            amazonPage = uClient.read()
            uClient.close()
            amazon_html = bs(amazonPage,"html.parser")
            bigBoxes = amazon_html.findAll("div",{"class" : "puisg-col-inner"})
            del bigBoxes[0:2]
            box = bigBoxes[0]
            productLink = "https://www.amazon.in"+ bigBoxes.div.div.div.h2.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding ='utf-8'
            prod_html = bs(prodRes.text, "html.parser")























