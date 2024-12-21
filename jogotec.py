import flask
from flask import Flask , render_template,request,redirect,session,flash

class Jogo:
    def __init__(self,nome,categoria,console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class usuario:
    def __init__(self,login,senha):
        self.login = login
        self.senha  = senha



jogo1 =  Jogo('Tetris',"Logico","Nintendo")
jogo2 = Jogo('God of War', "Action", "Ps2")
jogo3 = Jogo('Mortal Combat', "Fight", "Ps2")

lista_jogos = [jogo1,jogo2,jogo3]





app = Flask(__name__)
app.secret_key = 'alessandro'
@app.route('/inicio')
def inicio():



    return render_template('lista.html' ,title='Jogos', jogos=lista_jogos)


@app.route('/novo_jogo')
def novo_jogo():
    return render_template("new_game.html")



@app.route('/criar' ,methods=['POST','GET'])
def pergar_jogo():
    name = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(name,categoria,console)
    lista_jogos.append(jogo)
    return redirect('/inicio')


@app.route('/login' )
def login():
    return render_template("login.html")

@app.route('/autenticar',methods=['POST','GET'] )
def autenticar():
    if "spale12" == request.form['senha']:
        session['usuario'] = request.form['usuario']
        flash(session['usuario'] + "Login sucesso")
        return redirect('/inicio')
        return redirect('/inicio')
    else:
        flask.flash("Usuario ou senha incorretos")
        return redirect('/login')



@app.route('/logout')
def logout():
    session['usuario'] = None
    flash("Logout sucesso")
    return redirect('/inicio')




app.run(debug=True)




