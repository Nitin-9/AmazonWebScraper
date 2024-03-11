import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
from urllib.request import urlopen as uReq
from selenium import webdriver

# # Set up the webdriver (make sure you have the appropriate driver installed)
# driver = webdriver.Chrome()
#
# # Navigate to the page
# driver.get("https://www.amazon.in")
#
# # Find the element containing the pseudo-element content
# element = driver.find_element_by_css_selector(".your-element::before")
#
# # Extract the text content
# content = element.get_attribute("content")
#
#
# # Close the browser
# driver.quit()
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
            # uClient = uReq(amazon_url)
            # amazonPage = uClient.read()
            # uClient.close()
            amazonPage = requests.get(amazon_url)
            amazonPage.encoding = 'utf-8'
            amazon_html = bs(amazonPage.text,"html.parser")
            link = amazon_html.findAll("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
            # del bigBoxes[0:2]
            # box = bigBoxes[0]

            hrefLink = link[2].get("href")
            productLink = "https://www.amazon.in" + hrefLink
            #productLink = productLinkPath.div.div.div.h2.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding ='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            commentBoxes = prod_html.findAll("div", {"class": "a-section review aok-relative"})

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentBox in commentBoxes:
                try:
                    name = commentBox.find("span", attrs={"class": "a-profile-name"}).text
                except:
                    name = 'No Name'

                try:
                    rating = commentBox.find("span", {"class": "a-icon-alt"}).text
                except:
                    rating = 'No Rating'

                try:
                    commentHead = (commentBox.find("a", attrs={"class":"a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"})).find("span",{"class":""}).text
                except:
                    commentHead = 'No Comment Head'

                try:
                    custComment = (commentBox.find("div", {"class":"a-row a-spacing-small review-data"})).span.span.text
                except Exception as e:
                    print("Exception while creating dictionary: ", e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                reviews.append(mydict)
            keys = reviews[0].keys()
            with open(filename, 'w', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(reviews)
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
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



























