import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("Banco.db")
    return conexao


def criar_tabela():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("CREATE table if not exists usuarios (id integer primary key, email text, nome text, senha text,imagem text default 'none', descricao text default 'none', seguidores integer default 0, seguindo integer default 0,publicacao text default 'none')")
    
    cursor.execute("CREATE table if not exists postagem(id integer primary key, imagem text, descricao text, metodo text, like integer default 0, deslike integer default 0)")
    
    cursor.execute("CREATE table if not exists mensagens(id integer primary key, imagem text, hora text, mensagem text, email text)")

    cursor.execute("CREATE table if not exists rastreador(id integer primary key,email_perfil text default 'none', id_dequemvocesegue integer default '0', id_dequemseguevoce integer default '0')")
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

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (informacoes['email'],))
    id = cursor.fetchone()

    id_usuario = id[0]

    cursor.execute("UPDATE rastreador SET email_perfil = ? WHERE id = ?", (informacoes['email'],id_usuario,))

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
    
    
def likes(id,like):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("UPDATE postagem SET like = like + 1 WHERE id = ?", (id,))
    
    conexao.commit()
    conexao.close()
    return True

def deslikes(id,like):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute("UPDATE postagem SET deslike = deslike + 1 WHERE id = ?", (id,))
    
    conexao.commit()
    conexao.close()
    return True

def seguir(id_seguido, email_seguidor):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Pega o ID de quem está seguindo
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email_seguidor,))
    id_seguidor = cursor.fetchone()[0]

    # Verifica se já está seguindo
    cursor.execute("SELECT * FROM rastreador WHERE email_perfil = ? AND id_dequemvocesegue = ?", (email_seguidor, id_seguido))
    if cursor.fetchone():
        return False  # Já está seguindo

    # Atualiza contadores
    cursor.execute("UPDATE usuarios SET seguidores = seguidores + 1 WHERE id = ?", (id_seguido,))
    cursor.execute("UPDATE usuarios SET seguindo = seguindo + 1 WHERE id = ?", (id_seguidor,))

    # Adiciona ao rastreador
    cursor.execute("INSERT INTO rastreador (email_perfil, id_dequemvocesegue) VALUES (?, ?)", (email_seguidor, id_seguido))

    conexao.commit()
    conexao.close()
    return True

def parar_seguir(id_seguido, email_seguidor):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Pega o ID de quem está seguindo
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email_seguidor,))
    id_seguidor = cursor.fetchone()[0]

    # Remove do rastreador
    cursor.execute("DELETE FROM rastreador WHERE email_perfil = ? AND id_dequemvocesegue = ?", (email_seguidor, id_seguido))

    # Atualiza contadores
    cursor.execute("UPDATE usuarios SET seguidores = seguidores - 1 WHERE id = ?", (id_seguido,))
    cursor.execute("UPDATE usuarios SET seguindo = seguindo - 1 WHERE id = ?", (id_seguidor,))

    conexao.commit()
    conexao.close()
    return True






    
    
    



if __name__ == '__main__':
    criar_tabela()
    