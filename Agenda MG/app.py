import sqlite3
#from jinja2 import Template
from flask import Flask, render_template, request, session
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
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

def eh_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

# Abrindo a pagina de resultado
@app.route('/search',  methods=['POST'])
def search():
    if request.method == 'POST':
        # Get the search term from the form data
        busca_term = request.form['busca_term']
        nome = busca_term
        if eh_int(busca_term):
            ramal = int(busca_term)
        else:
            ramal = ''
        import sqlite3
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        c.execute('SELECT nome, ramal FROM agendaInterna')
        ramais = c.fetchall()
        #conexao.close()
        encontrados = 0
        tipos = []
        listaRamaisI = []
        listaRamaisD = []
        for i in ramais:
            #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
            if(i[0]==nome):
                encontrados = encontrados+1
                tipos.append('interno')
                print("Nome encontrado no banco")
                listaRamaisI.append(i)
                #return render_template('search_select.html')
                #return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='interno')
            if(i[1]==ramal):
                encontrados = encontrados+1
                tipos.append('interno')
                print("Ramal encontrado no banco")
                listaRamaisI.append(i)
                #return render_template('search_select.html')
                #return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='interno')
        c.execute('SELECT nome, ramal FROM agendaDireta')
        ramais = c.fetchall()
        conexao.close()
        for i in ramais:
            #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
            if(i[0]==nome):
                encontrados = encontrados+1
                tipos.append('direto')
                print("Nome encontrado no banco")
                listaRamaisD.append(i)
                #return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='direto')
            if(i[1]==ramal):
                encontrados = encontrados+1
                tipos.append('direto')
                print("Ramal encontrado no banco")
                listaRamaisD.append(i)
                #return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='direto')

    if (encontrados==0):
        return render_template('search_form.html')
    elif (encontrados==1):
        if(tipos[0]=='interno'):
            import sqlite3
            conexao = sqlite3.connect('agenda.db')
            c = conexao.cursor()
            c.execute('SELECT nome, ramal FROM agendaInterna')
            ramais = c.fetchall()
            conexao.close()
            for i in ramais:
                #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
                if(i[0]==nome):
                    print("ENVIANDO")
                    return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='interno')
                if(i[1]==ramal):
                    print("ENVIANDO")
                    return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='interno')
            #return render_template('search_results.html', search_results=str(ramais[]),resultado_ramal=str(ramais[]),tipo_ramal=tipos[0])
        if(tipos[0]=='direto'):
            import sqlite3
            conexao = sqlite3.connect('agenda.db')
            c = conexao.cursor()
            c.execute('SELECT nome, ramal FROM agendaDireta')
            ramais = c.fetchall()
            conexao.close()
            for i in ramais:
                #print('Ramal cadastrado: '+(i[1])+'Ramal novo:'+ramal)
                if(i[0]==nome):
                    print("ENVIANDO")
                    return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='direto')
                if(i[1]==ramal):
                    print("ENVIANDO")
                    return render_template('search_results.html', search_results=str(i[0]),resultado_ramal=str(i[1]),tipo_ramal='direto')
    elif (encontrados>1):
        return render_template('search_select.html', rows=listaRamaisI, rows2=listaRamaisD)
    return render_template('search_select.html')

@app.route('/search_results_table',  methods=['POST'])
def search_results_table():
    dados = request.form['editar']
    listaFiltros = dados.replace("(", "")
    listaFiltros = listaFiltros.replace(")", "")
    listaFiltros = listaFiltros.replace("[", "")
    listaFiltros = listaFiltros.replace("]", "")
    listaFiltros = listaFiltros.replace("'", "")
    listaFiltros = listaFiltros.replace(" ", "")
    listaFiltros = listaFiltros.split(",")
    return render_template('search_results.html',search_results=str(listaFiltros[0]),resultado_ramal=str(listaFiltros[1]),tipo_ramal=listaFiltros[2])

@app.route('/search_results',  methods=['POST'])
def search_results():
    return render_template('search_results.html')

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
    return render_template('table.html', rows=rows, rows2=rows2, filtro='desativado')

@app.route('/filtrarAgenda', methods=['POST'])
def filtrarAgenda():
    pesquisar = request.form['pesquisar']
    if (pesquisar==''):
        print('Consulta vazia')
    else:
        filtros = pesquisar.split()
        listaFiltros = []
        listaFiltros2 = []
        import sqlite3
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        for i in filtros:
            c.execute("SELECT nome, ramal FROM agendaInterna WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (i,i))
            listaFiltros.append(c.fetchall())
        for i in filtros:
            c.execute("SELECT nome, ramal FROM agendaDireta WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (i,str(i)))
            listaFiltros2.append(c.fetchall())
        conexao.close()
        ramais = listaFiltros
        ramais2 = listaFiltros2
        print(listaFiltros)
        return render_template('table.html', rows=ramais, rows2=ramais2,filtros=filtros,filtro='ativado')
        #return render_template('table.html', rows=rows, rows2=rows2)
    return abrirAgenda()

@app.route('/excluirFiltro', methods=['POST'])
def excluirFiltro():
    # O botão vai retornar uma string ['nomeExemplo',('nomeExemplo2','nomeExemplo3')]
    # A string vai passar por todos os filtros para remover os caracteres e separar em uma lista
    filtros = request.form['filtro']
    listaFiltros = filtros.replace("(", "")
    listaFiltros = listaFiltros.replace(")", "")
    listaFiltros = listaFiltros.replace("[", "")
    listaFiltros = listaFiltros.replace("]", "")
    listaFiltros = listaFiltros.replace("'", "")
    listaFiltros = listaFiltros.replace(" ", "")
    listaFiltros = listaFiltros.split(",")
    # A primeira posição da lista é o filtro que será excluido
    filtroExcluido = listaFiltros[0]
    del listaFiltros[0]
    # Agora vamos percorrer a lista buscando a posição do filtro para ser excluido
    tamanhoLista = len(listaFiltros)
    i=0
    while (i<tamanhoLista):
        if (listaFiltros[i]==filtroExcluido):
            posicaoFiltroExcluido = i
        i = i+1
    # Deletando o filtro dentro da lista
    del listaFiltros[posicaoFiltroExcluido]
    for i in listaFiltros:
        print('Restante da lista:',i)
    print('tamanho da lista',len(listaFiltros))
    # Filtrando novamente e retornando
    if ((len(listaFiltros))>0):
        print('entrou')
        filtros = listaFiltros
        ramaisFiltrados = []
        ramaisFiltrados2 = []
        import sqlite3
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        for i in filtros:
            c.execute("SELECT nome, ramal FROM agendaInterna WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (i,i))
            ramaisFiltrados.append(c.fetchall())
        for i in filtros:
            c.execute("SELECT nome, ramal FROM agendaDireta WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (i,str(i)))
            ramaisFiltrados2.append(c.fetchall())
        conexao.close()
        ramais = ramaisFiltrados
        ramais2 = ramaisFiltrados2
        return render_template('table.html', rows=ramais, rows2=ramais2,filtros=filtros,filtro='ativado')
    else:
        print('entrou')
        return abrirAgenda()

@app.route('/login', methods=['POST'])
def login():
    print('login')
    if 'logged_in' in session:
        return render_template('admin.html')
    else:
        return render_template('login.html')

@app.route('/validarLogin', methods=['POST'])
def validarLogin():
    usuario = request.form['usuario']
    senha = request.form['senha']
    users = ['Andre Lacerda',
             'Wagner',
             'Ana Elisa']
    passwords = ['segurancati',
                 'segurancati',
                 'copomg23!@']
    i = 0
    while (i<len(users)):
        print('user:')
        print(users[i])
        print('senha:')
        print(passwords[i])
        if (usuario==users[i])and(senha==passwords[i]):
            session['logged_in'] = True
            return render_template('admin.html', nome=usuario)
        i = i+1
    session.pop('logged_in', None)
    return render_template('login.html',mensagemRetorno='Usuario ou senha incorreto')

@app.route('/admin', methods=['POST'])
def admin():
    return render_template('admin.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return render_template('index.html')

@app.route('/editarBanner', methods=['POST'])
def editarBanner():
    return render_template('editarBanner.html')

# Adicionar e excluir imagens do diretorio

UPLOAD_FOLDER = 'static/images/Banners'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/upload', methods=['POST'])
def upload():
    # Verifica se o arquivo está presente no request
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado'

    file = request.files['file']

    # Verifica se o arquivo possui um nome
    if file.filename == '':
        return 'Nome do arquivo não encontrado'

    # Salva o arquivo no diretório de upload
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return 'Arquivo {} enviado com sucesso!'.format(file.filename)

def excluir():
    # Caminho completo para o arquivo que será excluído
    file_path = 'static/images/imagem4.jpg'
    
    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        # Exclui o arquivo
        os.remove(file_path)
        return 'Arquivo excluído com sucesso!'
    else:
        return 'Arquivo não encontrado.'

def listarDiretorio():
    # Diretório onde estão os arquivos
    directory = 'static/images'
    
    # Obtém a lista de arquivos existentes no diretório
    file_list = os.listdir(directory)
    
    return render_template('index.html', files=file_list)

if __name__ == '__main__':
    #app.run(host='192.168.20.125')
    app.run(debug=True)