import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("Banco.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("CREATE table if not exists usuarios (id integer primary key, email text, nome text, senha text,imagem text default 'none', descricao text default 'none', seguidores integer default 0, seguindo integer default 0,publicacao text default 'none')")
    
    cursor.execute("CREATE table if not exists postagem(id integer primary key, imagem text, descricao text, metodo text, like integer, deslike integer)")
    
    cursor.execute("CREATE table if not exists mensagens(id integer primary key, imagem text, hora text, mensagem text, email text)")
    conexao.commit()
    
def cadastro(informacoes):
    conexao = conectar_banco()
    cursor = conexao.cursor() 
    
    cursor.execute("SELECT COUNT(email) FROM usuarios WHERE email=?", (informacoes['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    if (quantidade_de_emails[0] > 0):
        print ("email já cadastrado, tente novamente")
        return False
    

    cursor.execute("INSERT INTO usuarios (email,nome,senha) VALUES (?,?,?)", (informacoes['email'], informacoes['nome'], informacoes['senha']))
    

    
    conexao.commit()
    return True

def criar_postagem(form):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("INSERT INTO postagem (imagem,descricao,metodo) VALUES (?,?,?)", (form['imagem'], form['descricao'], form['metodo'],))
    cursor.execute("UPDATE usuarios SET publicacao = ?",(form['imagem'],))
    
    conexao.commit()
    cursor.close()
    conexao.close()
    return True

def excluir_post(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("DELETE from postagem WHERE id = ?", (id,))
    conexao.commit()

    return True

def editar_perfil(perfil, usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("UPDATE usuarios SET nome = ?,descricao = ?,imagem = ? WHERE id = ?",(perfil['nome'],perfil['descricao'],perfil['imagem'],usuario_id))
    conexao.commit()
    return True

def selecionar (id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT email FROM usuarios WHERE id = ?", (id,))
    verificacao = cursor.fetchone()
    cursor.execute("SELECT imagem FROM postagem WHERE id = ?", (id,))
    fotos = cursor.fetchone()
    
    return verificacao, fotos
    




    
    
    



if __name__ == '__main__':
    criar_tabela()
    