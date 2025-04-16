from flask import Flask, render_template, request, url_for, redirect, flash, session
app = Flask(__name__)
app.secret_key = "chave_muito_segura"
import database


@app.route('/') 
def index():
    return render_template('index.html')
 
@app.route('/cadastrar',methods = ["GET","POST"])
def cadastrar():
    form = request.form
    if database.cadastro(form) == True:
        return render_template('index.html')
    
    else:
        return ("erro")
        
    



if __name__ == '__main__':
    app.run(debug=True)