from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# class Jogo:
#     def __init__(self, nome, categoria, console):
#         self.nome = nome
#         self.categoria = categoria
#         self.console = console
#
# class Usuario:
#     def __init__(self, nome, nickname, senha):
#         self.nome = nome
#         self.nickname = nickname
#         self.senha = senha
#
# usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
# usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
# usuario3 = Usuario("Guilherme Louro", "Cake", "python_eh_vida")
#
# jogo1 = Jogo('Tetris', "Logico", "Nintendo")
# jogo2 = Jogo('God of War', "Action", "Ps2")
# jogo3 = Jogo('Mortal Combat', "Fight", "Ps2")
#
# lista_jogos = [jogo1, jogo2, jogo3]
# usuarios = {u.nickname: u for u in [usuario1, usuario2, usuario3]}

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'ale00407',
        servidor = 'localhost',
        database = 'jogoteca'
    )


app.secret_key = 'alessandro'


class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String,nullable=False)
    console = db.Column(db.String,nullable=False)
    def __repr__(self):
        return '<Name %r>' % self.name


class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

    def __repr__(self):
        return '<Name %r>' % self.nickname



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] is None:
            return redirect(url_for('login', proxima=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/inicio')
def inicio():
    lista = Jogos.query.order_by(Jogos.id)

    return render_template('lista.html', title='Jogos', jogos=lista)

@app.route('/new_game')
@login_required
def novo_jogo():
    return render_template('new_game.html', titulo='Novo Jogo')


@app.route('/cadastro')
def cadastro():
    return render_template('Cadastro.html', titulo='Realizar Cadastramento')


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    nickname = request.form['nickname']
    senha = request.form['senha']

    if not nome or not nickname or not senha:
        flash('Todos os campos são obrigatórios!')
        return redirect(url_for('inicio'))

    usuario = Usuarios.query.filter_by(nome=nome).first()
    nick = Usuarios.query.filter_by(nickname=nickname).first()

    if usuario or nick:
        flash('Usuario ou Nickname ja existe!')
        return redirect(url_for('inicio'))

    novo_usuario = Usuarios(nome=nome, nickname=nickname, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    flash('Usuario Cadastrado com sucesso!')

    return redirect(url_for('inicio'))


@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('inicio'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('inicio'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima is None:
        return redirect(url_for('inicio'))

    return render_template("login.html", proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))

    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))





@app.route('/deletar')
@login_required
def deletar():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('del_game.html', titulo='Excluir Jogo', jogos=lista)




@app.route('/apagar', methods=['POST'])
def apagar():
    nome = request.form['nome']

    # Busca o jogo pelo nome
    jogo = Jogos.query.filter_by(nome=nome).first()

    if not jogo:
        flash('Jogo não encontrado!')
        return redirect(url_for('inicio'))

    # Remove o jogo encontrado
    db.session.delete(jogo)
    db.session.commit()

    flash('Jogo deletado com sucesso!')
    return redirect(url_for('inicio'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout realizado com sucesso")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
