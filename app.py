import csv
from flask import Flask, render_template, request, url_for, redirect
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key="AIzaSyB7Ptl2kGl4gwSGd14P5efvhhFMjceP7qc")
model = genai.GenerativeModel("gemini-2.0-flash")

@app.route("/gemini", methods=["GET", "POST"])
def gemini():
    resposta = ""
    pergunta = ""
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        try:
            resposta = model.generate_content(pergunta).text
        except Exception as e:
            resposta = f"Erro ao obter resposta: {str(e)}"
    return render_template("gemini.html", resposta=resposta, pergunta=pergunta)

@app.route('/')
def ola():
    # return '<h1>Olá, Mundo!</h1>'
    return render_template('index.html')

@app.route('/sobre-equipe')
def sobre_equipe():
    return render_template('sobre.html')


@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open('bd_glossario.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        for t in reader:
            glossario_de_termos.append(t)

    return render_template('glossario.html', glossario=glossario_de_termos)

@app.route('/novo_termo')
def novo_termo():
    return render_template('novo_termo.html')


@app.route('/criar_termo', methods=['POST'])
def criar_termo():

    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))

@app.route('/fundamentos')
def fundamentos_menu():
    return render_template('fundamentos/menu_fundamentos.html')

@app.route('/fundamentos/selecao')
def selecao():
    return render_template('fundamentos/selecao.html')

@app.route('/fundamentos/repeticao')
def repeticao():
    return render_template('fundamentos/repeticao.html')

@app.route('/fundamentos/vetores')
def vetores():
    return render_template('fundamentos/vetores.html')

@app.route('/fundamentos/funcoes')
def funcoes():
    return render_template('fundamentos/funcoes.html')

@app.route('/fundamentos/excecoes')
def excecoes():
    return render_template('fundamentos/excecoes.html')


app.run(debug=True)


