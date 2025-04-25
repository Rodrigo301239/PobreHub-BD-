from flask import Flask, render_template, request, url_for, redirect, flash, session
app = Flask(__name__)
app.secret_key = 'chave_supersecreta'
import database


@app.route('/') 
def index():
    return render_template('index.html')

@app.route('/home')
def home():
   
    conexao = database.conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM postagem ORDER BY id DESC") 
    postagem = cursor.fetchall()
    
    
    cursor.close()
    conexao.close()
    return render_template('home.html', postagem=postagem, usuario=session['id'])
 
@app.route('/cadastrar',methods = ["GET","POST"])
def cadastrar():
    form = request.form
    if database.cadastro(form) == True:
        return render_template('index.html')
    
    else:
        return ("erro1")


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
        print (usuario)
        if usuario and usuario[3] == senha:
            session['id'] = usuario[0]
            session['email'] = usuario[1]
            return redirect (url_for('home'))
        
        else:
            flash ("usuario ou senha incorretos")
    
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    return render_template('buscar.html')

@app.route('/buscar_usuario')
def buscar_usuario():
    nome_usuario = request.args.get('nome')
    if not nome_usuario:
        return "Nome não fornecido."

    nome_usuario = nome_usuario.strip()

    conexao = database.conectar_banco()
    cursor = conexao.cursor()

    # Buscar nome e ID ao mesmo tempo
    cursor.execute("SELECT id, nome FROM usuarios WHERE LOWER(nome) = LOWER(?)", (nome_usuario.lower(),))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        id_usuario = resultado[0]
        return redirect(url_for('perfil', id=id_usuario))  # 👈 Rota correta
    else:
        return f"Usuário '{nome_usuario}' não encontrado."


@app.route('/perfil/<nome>')
def perfil_usuario(nome):
    return render_template('perfil_usuario.html', nome=nome)


@app.route('/mensagens')
def mensagens():
    return render_template('mensagens.html')

@app.route('/notificacoes')
def notificacoes():
    return render_template('notificacoes.html')

@app.route('/perfil/<int:id>',methods = ['GET','POST'])        
def perfil(id):
    conexao = database.conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    perfil_usuario = cursor.fetchone()
    
    
    if request.method == "POST" and perfil_usuario:
        extra = request.form.get('extra')

        perfil_dict = {
            'id': perfil_usuario[0],
            'nome': perfil_usuario[2],
            'imagem': perfil_usuario[4],
            'descricao': perfil_usuario[5],
            'seguidores': perfil_usuario[6],
            'seguindo': perfil_usuario[7],
            'postagem': perfil_usuario[8]
            }
        
        verificacao,fotos = database.selecionar(id)
        
        return render_template('perfil.html', perfil=perfil_dict, extra = extra, verificacao=verificacao, fotos=fotos)

    elif request.method == "GET":
        extra = request.args.get('extra')

        perfil_dict = {
            'id': perfil_usuario[0],
            'nome': perfil_usuario[2],
            'imagem': perfil_usuario[4],
            'descricao': perfil_usuario[5],
            'seguidores': perfil_usuario[6],
            'seguindo': perfil_usuario[7]
        }
        verificacao = database.selecionar(id)
        return render_template('perfil.html', perfil=perfil_dict, extra=extra, verificacao=verificacao)

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
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/editar_perfil/<int:id>',methods = ['GET','POST'])
def editar_perfil(id):
    if request.method == "POST":
        form = request.form
        if database.editar_perfil(form, id) == True:
            return redirect(url_for('perfil', id=id))



    return render_template('editar.html', id=id)

@app.route('/like',methods = ['POST'])
def likes():
    post_id = request.form.get('post_id')  # Pega o ID do post
    like_value = request.form.get('like')  # Pega o valor de like/deslike
    
    print("Post ID:", post_id)
    print("Like/Deslike:", like_value)
        
    if like_value == "like":
        if database.likes(post_id,like_value) == True:
            return redirect(url_for('home'))
    elif like_value == "deslike":
        if database.deslikes(post_id,like_value) == True:
            return redirect(url_for('home'))
    
    return "Erro ao registrar like/deslike", 400
    
    


        
        


        
    



if __name__ == '__main__':
    app.run(debug=True)