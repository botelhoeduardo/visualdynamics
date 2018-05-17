from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selecao_arquivo = request.form['file']
        pasta = os.path.dirname(selecao_arquivo)
        arquivo = os.path.basename(selecao_arquivo)
        (nome_arquivo, extensao) = arquivo.split('.')

        campo_forca = request.form.get('campoforca')

        modelo_agua = request.form.get('modeloagua')

        tipo_caixa = request.form.get('tipocaixa')

        distancia_caixa = request.form['distanciacaixa']

        neutralizar_sistema = request.form['neutralize']

        arquivo_gro = nome_arquivo + '.gro'
        arquivo_top = nome_arquivo + '.top'
        arquivo_box = nome_arquivo + '_box'
        arquivo_ionizado = nome_arquivo + '_charged'
        
        

    return render_template('index.html')

if __name__ == '__main__':
    app.run()