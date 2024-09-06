#pip install flask
#pip install Flask-SQLAlchemy
#pip install Flask-Migrate
#pip install Flask-Script
#pip install pymysql
#flask db init
#flask db migrate -m "Migração inicial"
#flask db upgrade
#flask run --debug "rodar o site"

from flask import Flask, render_template, request, flash, redirect
app = Flask(__name__)
from database import db
from flask_migrate import Migrate
from models import Usuario
app.config['SECRET_KEY'] = '23ttnd4gnd55y-23md98'

#drive://usuario:senha@servidor/banco_de_dados
conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/thiago"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')
5
@app.route('/aula')
@app.route('/aula/<nome>')
@app.route('/aula/<nome>/<curso>')
@app.route('/aula/<nome>/<curso>/<int:ano>')
def aula(nome = 'João', curso = 'Informática', ano = 1):
    dados = {'nome':nome,'curso':curso, 'ano':ano}
    return render_template('aula.html',dados_curso = dados)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/dados', methods=['POST'])
def dados():
    flash('Dados ')
    dados = request.form
    return render_template('dados.html', dados=dados)

@app.route('/usuario')
def usuario():
    u = Usuario.query.all()
    return render_template('usuario_lista.html', dados = u)

@app.route('/usuario/add')
def usuario_add():
    return render_template('usuario_add.html')

@app.route('/usuario/save', methods=['POST'])
def usuario_save():
    nome = request.form.get('nome')
    email = request.form.get('email')
    idade = request.form.get('idade')
    if nome and email and idade:
        usuario = Usuario(nome, email, idade)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!!!')
        return redirect('/usuario')
    else:
        flash('Preencha todos os campos')
        return redirect ('/usuario/add')

@app.route('/usuario/remove/<int:id>')
def usuario_remove(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário removido com sucesso!')
        return redirect('/usuario')
    else:
        flash('Caminho Incorreto!')
        return redirect('/usuario')

@app.route('/usuario/edita/<int:id>')
def usuario_edita(id):
    usuario = Usuario.query.get(id)
    return render_template('usuario_edita.html', dados = usuario)    

@app.route('/usuario/edita/save', methods=['POST'])
def usuario_edita_save():
    nome = request.form.get('nome')
    email = request.form.get('email')
    idade = request.form.get('idade')
    id = request.form.get('id')
    if id and nome and email and idade:
        usuario = Usuario.query.get(id)
        usuario.nome = nome
        usuario.email = email
        usuario.idade = idade
        db.session.commit()
        flash('Dados atualizados com sucesso!!')
        return redirect('/usuario')
    else:
        flash('Faltando dados!')
        return redirect('/usuario')


if __name__ == '__main__':
    app.run()

