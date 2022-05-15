from flask import Flask, render_template, url_for, request, redirect
import requests
from bs4 import BeautifulSoup

def beautify(res, word):
	res2=f'{word} is a valid Scrabble word'
	resno=1
	if(res=='0'):
		res2=f'{word} is not a valid Scrabble word'
		resno=0
		defi=[]
	else:
		defi=[]
		soup=BeautifulSoup(res,'lxml')
		pos=soup.find_all(class_="pos")
		tempdefi=soup.find_all(class_="def")
		for i in range(len(pos)):
			defi.append(f'({pos[i].text}) - {tempdefi[i].text}')
	return res2, defi, resno

def do(word):
	url=f'https://unikove.com/projects/scrabble_widget/scrabble_api.php?word={word.lower()}'
	response=requests.get(url)
	return response.text

app=Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def search():
	title=0
	if(request.method=='POST'):
		title = request.form['word']
	if(title==0):
		return render_template("index.html")
		res='-'*120
	res=do(title)
	res2, defi, resno=beautify(res,title)
	return render_template("results.html", word=title, res2=res2, defi=defi, resno=resno)

@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
