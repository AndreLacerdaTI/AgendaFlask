import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# rota principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    return render_template('index.html')

@app.route('/paginaCadastro',methods=['POST'])
def paginaCadastro():
    return render_template('cadastrar.html')



# Cadastrando Ramal Direto
@app.route('/cadastrarDireto', methods=['POST'])
def cadastrarDireto():
    nome = request.form['nome']
    ramal = int(request.form['ramal'])
    # Verificando se existe o ramal
    import sqlite3
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT nome, ramal FROM agendaDireta')
    ramais = c.fetchall()
    conexao.close()
    validador = 0
    for i in ramais:
        #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
        if(i[0]==nome):
            retorno = 'Nome já está cadastrado!\n Verifique se é a mesma pessoa ou adicione mais alguma identificação'
            validador = 1
            print("Nome encontrado no banco")
        if(i[1]==ramal):
            retorno = 'Ramal já está cadastrado'
            validador = 1
            print("Ramal encontrado no banco")
        print(i)

    # Verificando se podemos cadastrar o ramal
    if (validador==0):
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        c.execute("INSERT INTO agendaDireta (nome, ramal) VALUES (?, ?)", (nome, ramal))

        conexao.commit()
        conexao.close()

        retorno = 'Ramal Direto: '+str(ramal)+' - '+nome+' \ncadastrado com sucesso!'

        #return f'Obrigado, {nome}, nós entraremos em contato em breve no email {ramal}.'
        #textoRetorno = 'Ramal '+ramal+'-'+nome+' cadastrado com sucesso!'
        #return render_template('cadastrar.html', error=textoRetorno)

    return render_template('cadastrar.html', mensagemRetorno=retorno)

# rota para receber dados do formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    import sqlite3
    nome = request.form['nome']
    ramal = int(request.form['ramal'])
    # Verificando se existe o ramal
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT nome, ramal FROM agendaInterna')
    ramais = c.fetchall()
    conexao.close()
    validador = 0
    for i in ramais:
        #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
        if(i[0]==nome):
            retorno = 'Nome já está cadastrado!\n Verifique se é a mesma pessoa ou adicione mais alguma identificação'
            validador = 1
            print("Nome encontrado no banco")
        if(i[1]==ramal):
            retorno = 'Ramal já está cadastrado'
            validador = 1
            print("Ramal encontrado no banco")
        print(i)

    # Verificando se podemos cadastrar o ramal
    if (validador==0):
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        c.execute("INSERT INTO agendaInterna (nome, ramal) VALUES (?, ?)", (nome, ramal))

        conexao.commit()
        conexao.close()

        retorno = 'Ramal Interno: '+str(ramal)+' - '+nome+' \ncadastrado com sucesso!'

        #return f'Obrigado, {nome}, nós entraremos em contato em breve no email {ramal}.'
        #textoRetorno = 'Ramal '+ramal+'-'+nome+' cadastrado com sucesso!'
        #return render_template('cadastrar.html', error=textoRetorno)

    return render_template('cadastrar.html', mensagemRetorno=retorno)
@app.route('/paginaCadastroDireto',methods=['POST'])
def paginaCadastroDireto():
    return render_template('cadastrarDireto.html')

# Editar ----------------------------------------------------------------------------------

# Abrindo a pagina de busca
@app.route('/seach_term', methods=['POST'])
def search_term():
    return render_template('search_form.html')

# Abrindo a pagina de resultado
@app.route('/search',  methods=['POST'])
def search():
    if request.method == 'POST':
        # Get the search term from the form data
        busca_term = request.form['busca_term']
        nome = busca_term
        ramal = int(busca_term)

        import sqlite3
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        c.execute('SELECT nome, ramal FROM agendaInterna')
        ramais = c.fetchall()
        conexao.close()
        validador = 0
        for i in ramais:
            #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
            print(i[1])
            if(i[0]==nome):
                validador = 1
                print("Nome encontrado no banco")
                return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='interno')
            if(i[1]==ramal):
                validador = 1
                print("Ramal encontrado no banco")
                return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='interno')

        import sqlite3
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        c.execute('SELECT nome, ramal FROM agendaDireta')
        ramais = c.fetchall()
        conexao.close()
        validador = 0
        for i in ramais:
            #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
            print(i[1])
            if(i[0]==nome):
                validador = 1
                print("Nome encontrado no banco")
                return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='direto')
            if(i[1]==ramal):
                validador = 1
                print("Ramal encontrado no banco")
                return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='direto')
        print(validador)



        # Search for the term in the list of items
        #search_results = [item for item in items if busca_term in item]
        # Render the search results template with the search results
        #return render_template('search_results.html', search_results=search_results)
    # If a GET request is received, render the search form template
    return render_template('search_form.html')


@app.route('/salvar_alteracao', methods=['POST'])
def salvar_alteracao():
    tipo_ramal = request.form['tipo_ramal']
    if request.form['action'] == 'cadastrar':
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        search_results = request.form['search_results']
        resultado_ramal = request.form['resultado_ramal']
        nome = search_results
        ramal = int(resultado_ramal)
        if (tipo_ramal=='interno'):
            c.execute('UPDATE agendaInterna SET nome = ?, ramal = ? WHERE ramal = ?', (nome, ramal, ramal))
            conexao.commit()
            conexao.close()
            retorno = 'Ramal Interno: '+str(ramal)+' - '+nome+' alterado com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
        elif(tipo_ramal=='direto'):
            c.execute('UPDATE agendaDireta SET nome = ?, ramal = ? WHERE ramal = ?', (nome, ramal, ramal))
            conexao.commit()
            conexao.close()
            retorno = 'Ramal Direto: '+str(ramal)+' - '+nome+' alterado com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
    elif request.form['action'] == 'excluir':
        conexao = sqlite3.connect('agenda.db')
        search_results = request.form['search_results']
        resultado_ramal = request.form['resultado_ramal']
        nome = search_results
        ramal = int(resultado_ramal)
        if(tipo_ramal=='interno'):
            c = conexao.cursor()
            c.execute("DELETE FROM agendaInterna WHERE ramal=?", (ramal,))
            conexao.commit()
            conexao.close()

            retorno = 'Ramal Interno: '+str(ramal)+' - '+nome+' excluido com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
        if(tipo_ramal=='direto'):
            c = conexao.cursor()
            c.execute("DELETE FROM agendaDireta WHERE ramal=?", (ramal,))
            conexao.commit()
            conexao.close()

            retorno = 'Ramal Direto: '+str(ramal)+' - '+nome+' excluido com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
@app.route('/abrirAgenda', methods=['POST'])
def abrirAgenda():
    # Importando agenda interna
    conn = sqlite3.connect('agenda.db')
    cur = conn.cursor()
    #cur.execute('SELECT * FROM agendaInterna')
    cur.execute('SELECT nome, ramal FROM agendaInterna ORDER BY nome')
    rows = cur.fetchall()
    # Importando agenda direta
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT nome, ramal FROM agendaDireta ORDER BY nome')
    rows2 = c.fetchall()
    return render_template('table.html', rows=rows, rows2=rows2)

@app.route('/filtrarAgenda', methods=['POST'])
def filtrarAgenda():
    pesquisar = request.form['pesquisar']
    filtros = pesquisar.split()
    print(filtros)
    import sqlite3
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute("SELECT nome, ramal FROM agendaInterna WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (pesquisar,pesquisar))
    ramais = c.fetchall()
    #c.execute("SELECT nome, ramal FROM agendaDireta WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (pesquisar,pesquisar))
    #sql = "SELECT nome, ramal FROM agendaDireta WHERE nome LIKE %s OR ramal LIKE %s OR setor LIKE %s"
    
    #sql = "SELECT nome, ramal FROM agendaDireta WHERE nome LIKE '%'|| ? ||'%' OR ramal LIKE '%' || ? || '%'"
    #params = (filtros,filtros)
    c.execute(sql, params)
    ramais2 = c.fetchall()
    conexao.close()
    #minha_string = "Olá, mundo!"
    #nova_string = minha_string.upper()
    return render_template('table.html', rows=ramais, rows2=ramais2,filtros=pesquisar)
    #return render_template('table.html', rows=rows, rows2=rows2)

@app.route('/login', methods=['POST'])
def login():
    print('login')
    return render_template('login.html')

@app.route('/validarLogin', methods=['POST'])
def validarLogin():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if (usuario=='Andre Lacerda')and(senha=='segurancadeti'):
        return render_template('admin.html', nome=usuario)
    else:
        return render_template('login.html',mensagemRetorno='Usuario ou senha incorreto')

@app.route('/admin', methods=['POST'])
def admin():
    return render_template('admin.html')
if __name__ == '__main__':
    #app.run(host='192.168.20.125')
    app.run(debug=True)