from flask import Flask, url_for, render_template, request, abort
import os
import requests
import json
app=Flask(__name__)

@app.route('/',methods=["GET"])
def prueba():
	r=requests.get('http://ergast.com/api/f1/2018/drivers.json')
	if r.status_code==200:
		piloto=json.loads(r.text)
		pilotos=piloto["MRData"]["DriverTable"]["Drivers"]
		return render_template("prueba.html",drivers=pilotos)

@app.route('/circuitos',methods=["GET"])
def circuitos():
	c=requests.get('http://ergast.com/api/f1/2018/circuits.json')
	if c.status_code==200:
		circuito=json.loads(c.text)
		circuits=circuito["MRData"]["CircuitTable"]["Circuits"]
		return render_template("circuitos.html",circuit=circuits)

@app.route('/circuitos/<circuitId>')
def circuito_individual(circuitId):
	b=requests.get('http://ergast.com/api/f1/circuits/%s.json' %(circuitId))
	datos=json.loads(b.text)
	dato=datos["MRData"]["CircuitTable"]["Circuits"]
	for i in dato:
		pais=i["Location"]["country"]
	with open("paises.json") as fichero:
		doc=json.load(fichero)
	for h in doc:
		namepais=h[" name"]
		if pais==namepais:
			cod=h[" iso2"]
			print(cod.lower())
	return render_template("resultado.html",date=dato,codigo=cod)

@app.route('/campeonato',methods=["GET"])
def campeonato():
	a=requests.get('https://ergast.com/api/f1/current/driverStandings.json')
	mun=json.loads(a.text)
	mundial=mun["MRData"]["StandingsTable"]["StandingsLists"][0]
	e=requests.get('https://ergast.com/api/f1/current/constructorStandings.json')
	cons=json.loads(e.text)
	constructor=cons["MRData"]["StandingsTable"]["StandingsLists"][0]
	return render_template("mundial.html",mundials=mundial,constructors=constructor)

@app.route('/carrera', methods=["GET"])
def carrera():
	f=requests.get('https://ergast.com/api/f1/current/last/results.json')
	race=json.loads(f.text)
	races=race["MRData"]["RaceTable"]["Races"]
	return render_template("carreras.html",career=races)

@app.route('/wiki', methods=["GET","POST"])
def wiki(año=None):
	if request.method=="GET":
		return render_template('wiki.html')
	else:
		año=request.form.get("año")
		p=requests.get('https://ergast.com/api/f1/%s/driverStandings.json' %(año))
		if p.status_code==200:
			clasi=json.loads(p.text)
			standings=clasi["MRData"]["StandingsTable"]["StandingsLists"][0]
			return render_template('wiki.html',año=año,resultados=standings)

if __name__ == '__main__':
	port=os.environ["PORT"]
	app.run('0.0.0.0',int(port), debug=True)