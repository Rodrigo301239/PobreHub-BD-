import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("Banco.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("CREATE table if not exists usuarios (email text primary key, nome text, senha text)")
    
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
    
    senha_criptografada = generate_password_hash (informacoes['senha'])
    cursor.execute("INSERT INTO usuarios (email,nome,senha) VALUES (?,?,?)", (informacoes['email'], informacoes['nome'], senha_criptografada))
    
    conexao.commit()
    return True



if __name__ == '__main__':
    criar_tabela()
    