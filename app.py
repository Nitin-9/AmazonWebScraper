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
@app.route('/review', methods = ['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            amazon_url = "https://www.amazon.in/s?k=" + searchString
            uClient = uReq(amazon_url)
            amazonPage = uClient.read()
            uClient.close()
            amazon_html = bs(amazonPage,"html.parser")
            bigBoxes = amazon_html.findAll("div",{"class": "puisg-col-inner"})
            del bigBoxes[0:2]
            box = bigBoxes[0]
            productLink = "https://www.amazon.in" + bigBoxes.div.div.div.h2.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding ='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            commentBoxes = prod_html.findAll("div",{"class": "a-section review aok-relative"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentBox in commentBoxes:
                try:
                    name = commentBoxes.div.div.div.a.div[1].findall("span", {"class": "a-profile-name"})[0].text

                except:
                    name = 'No Name'

                try:
                    rating = commentBoxes.div.div.div[1].a.i.findall("span", {"class": "a-icon-alt"}).text
                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentBoxes.div.div.div[1].a.span[1].text
                except:
                    commentHead = 'No Comment Head'

                try:
                    custComment = commentBoxes.div.div.div[3].span.div.div.span.text

                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                reviews.append(mydict)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')
# port =int(os.getenv("PORT"))
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=8001, debug=True)
    # app.run(debug=True)



























