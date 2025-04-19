from flask import Flask, render_template, request, url_for, redirect, flash, session
app = Flask(__name__)
app.secret_key = 'chave_supersecreta'
import database


@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    # Apenas busca as postagens existentes, sem criar novas
    conexao = database.conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM postagem ORDER BY id DESC")  # Adicionei ORDER BY
    postagem = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('home.html', postagem=postagem)
 
@app.route('/cadastrar',methods = ["GET","POST"])
def cadastrar():
    form = request.form
    if database.cadastro(form) == True:
        return render_template('index.html')
    
    else:
        return ("erro")


@app.route('/login',methods = ['GET','POST'])   
def login():
    form =  request.form

    if request.method == 'POST':
        email = form['email']
        senha = form['senha']
        conexao = database.conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        conexao.close()
        if usuario and usuario[2] == senha:
            session['usuario'] = usuario[0]
            return redirect (url_for('home'))
        
        else:
            flash ("usuario ou senha incorretos")
    
    return "erro"

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/mensagens')
def mensagens():
    return render_template('mensagens.html')

@app.route('/notificacoes')
def notificacoes():
    return render_template('notificacoes.html')

@app.route('/perfil')        
def perfil():
    return render_template('perfil.html')

@app.route('/criar',methods = ['GET','POST'])
def criar():
    if request.method == "GET":
        return render_template('criar.html')
    
    elif request.method == "POST":
        form = request.form
        
        if database.criar_postagem(form) == True:
            return render_template('home.html')
        
        else:
            return "coroa"
    
    else:
        return "vanderlei"
        
        


        
    



if __name__ == '__main__':
    app.run(debug=True)