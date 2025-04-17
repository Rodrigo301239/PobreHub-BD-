from flask import Flask, render_template, request, url_for, redirect, flash, session
app = Flask(__name__)
app.secret_key = 'chave_supersecreta'
import database


@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')
 
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
        


        
    



if __name__ == '__main__':
    app.run(debug=True)