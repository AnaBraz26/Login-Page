from flask import Flask, render_template, redirect, request, flash
import json
import ast
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ENGSOFT'

logado = False

#pagina inicial do login
@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

#pagina do adm
@app.route('/adm')
def adm():    
    if logado == True:
        #Com JSon
        # with open('usuarios.json') as usuariosTemp:
        #     usuarios = json.load(usuariosTemp)
        
        #Usando banco de dados
        connect_BD = mysql.connector.connect(host = 'localhost', database='usuarios', user='root', password='218001')
    
        if connect_BD.is_connected():        
            print('CONECTADO')
            
            cursur = connect_BD.cursor()
            cursur.execute('select * from usuario;')
            usuarios = cursur.fetchall()
            return render_template('administrador.html', usuarios = usuarios)
        
    if logado == False:
        return redirect('/')
            
    
#pagina que redireciona
@app.route('/login', methods=['POST'])
def login():    
    
    global logado
    
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    
    # with open('usuarios.json') as usuariosTemp:
    #     usuarios = json.load(usuariosTemp)
    
    # utilizando banco de dados 
    connect_BD = mysql.connector.connect(host = 'localhost', database='usuarios', user='root', password='218001')
    
    cont = 0
    
    if connect_BD.is_connected():        
        print('CONECTADO')
        
        cursur = connect_BD.cursor()
        cursur.execute('select * from usuario;')
        
        usuariosBD = cursur.fetchall()
        
        for usuario in usuariosBD:
            cont += 1
            usuarioNome = str(usuario[1])            
            usuariosSenha = str(usuario[2])
            
            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')
            
            if usuarioNome == nome and usuariosSenha == senha:
                return render_template("usuarios.html")
            
            if cont >= len(usuariosBD):
                flash('USUÁRIO INVÁLIDO')
                return redirect("/")
    else:
        return redirect("/")

#pagina de cadastro do usuario (apenas para admin)
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    
    #Utilizando o JSON
    #user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    
    connect_BD = mysql.connector.connect(host = 'localhost', database='usuarios', user='root', password='218001')
    
    if connect_BD.is_connected():        
        print('CONECTADO')       
        
        cursur = connect_BD.cursor()
        cursur.execute(f"insert into usuario values (default, '{nome}', '{senha}');")
        
    if connect_BD.is_connected():  
         cursur.close()
         connect_BD.close()
    
    # user = [
    #     {
    #         "nome": nome,
    #         "senha": senha 
    #     }
    # ]
    
    # with open('usuarios.json') as usuariosTemp:
    #     usuarios = json.load(usuariosTemp)
     
    # usuarioNovo = usuarios + user
    
    # with open('usuarios.json', 'w') as gravarTemp:
    #     json.dump(usuarioNovo, gravarTemp, indent=4)
    
    logado = True
    
    flash(F'{nome} Cadastrado!')
    
    return redirect('/adm')

#rota para excluir usuario
@app.route('/excluirusuario', methods=['POST'])
def excluirusurio():
    global logado
    logado = True
    
    #Utilizando Json
    # usuario = request.form.get('usuario_excluir')
    # usuarioDict = ast.literal_eval(usuario) #transforma string em dicionario
    # nome = usuarioDict['nome']
    
    # with open('usuarios.json') as usuariosTemp:
    #     usuariosJson = json.load(usuariosTemp)
    #     for c in usuariosJson:
    #         if c == usuarioDict:
    #             usuariosJson.remove(usuarioDict)
    #             with open('usuarios.json', 'w') as usuario_excluir:
    #                 json.dump(usuariosJson, usuario_excluir, indent=4)
    
    #Utilizando banco de dados
    usuarioID = request.form.get('usuario_excluir')
    nome = request.form.get('nome')
    connect_BD = mysql.connector.connect(host = 'localhost', database='usuarios', user='root', password='218001')
    
    if connect_BD.is_connected():        
        print('CONECTADO')       
        
        cursur = connect_BD.cursor()
        cursur.execute(f"delete from usuario where id= '{usuarioID}';")
        
    if connect_BD.is_connected():  
         cursur.close()
         connect_BD.close()
    
    
    flash(F'{nome} Excluido')
    return redirect('/adm')

#inicializador
if __name__ in "__main__":
    app.run(debug=True)