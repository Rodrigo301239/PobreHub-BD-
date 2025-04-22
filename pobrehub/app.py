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

@app.route('/buscar_usuario')
def buscar_usuario():
    nome_usuario = request.args.get('nome')
    if not nome_usuario:
        return "Nome não fornecido."

    nome_usuario = nome_usuario.strip()  # remove espaços extras

    conexao = database.conectar_banco()
    cursor = conexao.cursor()

    # Consulta ignorando maiúsculas/minúsculas (opcional)
    cursor.execute("SELECT nome FROM usuarios WHERE LOWER(nome) = LOWER(?)", (nome_usuario.lower(),))
    resultado = cursor.fetchone()
    cursor.execute("SELECT id FROM usuarios WHERE id = ?", (1,))
    id = cursor.fetchone()
    conexao.close()

    if resultado and id:
        return redirect(url_for('perfil.html'))

    if resultado:
        return redirect (url_for('perfil_usuario', nome=resultado[0]))
    else:
        return f"usuário '{nome_usuario}' não encontrado"

@app.route('/perfil/<nome>')
def perfil_usuario(nome):
    return render_template('perfil_usuario.html', nome=nome)


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
            return redirect(url_for('home'))
        
        else:
            return "coroa"
    
    else:
        return "vanderlei"


@app.route('/excluir_post/<int:id>')
def excluir_post(id):
    
    if database.excluir_post(id) == True:
        return redirect(url_for('home'))


        
        


        
    



if __name__ == '__main__':
    app.run(debug=True)