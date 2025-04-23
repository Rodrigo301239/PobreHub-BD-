import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("Banco.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("CREATE table if not exists usuarios (id integer primary key, email text, nome text, senha text, imagem text)")
    
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



    
    
    



if __name__ == '__main__':
    criar_tabela()
    