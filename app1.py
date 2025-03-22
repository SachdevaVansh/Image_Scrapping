from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename=
                    'scrapper1.log', level=logging.INFO)
import os

app=Flask(__name__)

@app.route("/", methods =['GET'])
def homepage():
    return render_template('index.html')

@app.route("/review", methods=['POST','GET'])
def index():
    if request.method=='POST':
        try:
            #query to search for images
            query=request.form['content'].replace(" ","")

            #directory to store the downloaded images
            save_directory="images/"

            ##Create the directory if does not exists
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            #Fake user agent to avoid getting blocked by google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

            #Fetch the search results page
            response=requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M")

            #Parse the HTML using Beautiful soup
            soup=BeautifulSoup(response.content, 'html.parser')

            #Find all images tags
            image_tags=soup.find_all("img")

            #download each image and save it to the specific directory
            del image_tags[0]
            img_data=[]
            for index,image_tag in enumerate(image_tags):
                #Getting the image source url
                image_url=image_tag['src']

                #Sending a request to the image URL & save the image
                image_data=requests.get(image_url).content
                mydict={'Index':index, 'Image':image_data}
                img_data.append(mydict)
                with open(os.path.join(save_directory,f"{query}_{image_tags.index(image_tag)}.jpg"),'wb') as f:
                    f.write(img_data)
            client=pymongo.MongoClient("mongodb+srv://vansh:pwskills1@pwskills.wjulo.mongodb.net/?retryWrites=true&w=majority&appName=Pwskills")
            db=client['Image_Scrap']
            review_col=db['Image_scrap_data']
            review_col.insert_many(img_data)

            return "Image Loaded"
        except Exception as e:
            logging.info(e)
            return "Something went wrong"
        
    else:
        return render_template('index.html')
    
if __name__=='__main__':
    app.run(host="127.0.0.1", port=8000)
    






        