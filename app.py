from __future__ import unicode_literals
from flask import Flask, render_template, request, jsonify
import os
import webbrowser
import json
import youtube_dl


def writeurl(urlname):
    with open("links.json", "r") as f:
        links = json.loads(f.read())
    if urlname in links["links"]:
        pass
    else:
        links["links"].append(urlname)
    with open("links.json", "w") as f:
        json.dump(links, f, indent=1)

def clearjson():
    with open("links.json", "r") as f:
        links = json.loads(f.read())
    links_list = links["links"]
    del links_list[:]
    with open("links.json", "w") as f:
        json.dump(links, f, indent=1)

def createfolder(foldername="Videos"):
    CurrPath = os.getcwd()
    if not os.path.exists(CurrPath + f"/{foldername}"):# For linux we must use / instead of \
        os.mkdir(CurrPath + f"/{foldername}")
        os.chdir(CurrPath + f"/{foldername}")

def download():
    url = []
    with open("links.json") as f:
        links = json.loads(f.read())["links"]
        for link in links:
            url.append(link)
    if not url:
        return False
    else:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            createfolder()
            ydl.download(url)
    clearjson()

def getjsoncontent():
    urls = """
            <style>
            .main {
                padding-top: 15%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: Arial, Helvetica, sans-serif;
            }
            </style>
            <div class="main"><div><h3>Links:</h3>
        """
    with open("links.json", "r") as f:
        links = json.loads(f.read())["links"]
        for link in links:
            urls = urls + str(link) + "<br>"
        urls = urls + "</div></div>"
    return urls


app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        urlname = request.form['urlname']
        writeurl(urlname)
        return render_template('index.html')
    
    return render_template('index.html')

@app.route('/down', methods=['GET','POST'])
def dwn():
    if request.method == 'POST':
        if download():
            return render_template('index.html')
        else:
            return """
                    <style>
                    h3 {
                        padding-top: 15%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-family: Arial, Helvetica, sans-serif;
                    }
                    </style>
                    <h3>URL list empty</h3>
                """
    
    return render_template('index.html')

@app.route('/json_content')
def json_content():
    return getjsoncontent()

@app.route('/clear_json')
def clear_json():
    clearjson()
    return getjsoncontent()

if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', threaded=True)
