import sqlite3
#from jinja2 import Template
from flask import Flask, render_template, request, session, send_file
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'
logado = []
# rota principal
@app.route('/')
def index():
    directory = 'static/images/Banners'
    
    # Obtém a lista de arquivos existentes no diretório
    file_list = os.listdir(directory)
    
    print('arquivos',file_list)
    return render_template('index.html',imagens=file_list)

@app.route('/home', methods=['POST'])
def home():
    directory = 'static/images/Banners'
    
    # Obtém a lista de arquivos existentes no diretório
    file_list = os.listdir(directory)
    
    print('arquivos',file_list)
    return render_template('index.html',imagens=file_list)

@app.route('/paginaCadastro',methods=['POST'])
def paginaCadastro():
    return render_template('cadastrar.html')



# Cadastrando Ramal Direto
@app.route('/cadastrarDireto', methods=['POST'])
def cadastrarDireto():
    nome_form = request.form['nome']
    nome_minusculo = nome_form.lower()
    nome = nome_minusculo
    ramal = int(request.form['ramal'])
    setor = request.form['setor']
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
        c.execute("INSERT INTO agendaDireta (nome, ramal, setor) VALUES (?, ?, ?)", (nome, ramal, setor))

        conexao.commit()
        conexao.close()

        retorno = 'Ramal Direto: '+str(ramal)+' - '+nome+' - '+setor+' \ncadastrado com sucesso!'

        #return f'Obrigado, {nome}, nós entraremos em contato em breve no email {ramal}.'
        #textoRetorno = 'Ramal '+ramal+'-'+nome+' cadastrado com sucesso!'
        #return render_template('cadastrar.html', error=textoRetorno)

    return render_template('cadastrar.html', mensagemRetorno=retorno)

# rota para receber dados do formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    import sqlite3
    nome_form = request.form['nome']
    nome_minusculo = nome_form.lower()
    nome = nome_minusculo
    ramal = int(request.form['ramal'])
    setor = request.form['setor']
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
        c.execute("INSERT INTO agendaInterna (nome, ramal, setor) VALUES (?, ?, ?)", (nome, ramal, setor))

        conexao.commit()
        conexao.close()

        retorno = 'Ramal Interno: '+str(ramal)+' - '+nome+' - '+setor+' \ncadastrado com sucesso!'

        #return f'Obrigado, {nome}, nós entraremos em contato em breve no email {ramal}.'
        #textoRetorno = 'Ramal '+ramal+'-'+nome+' cadastrado com sucesso!'
        #return render_template('cadastrar.html', error=textoRetorno)

    return render_template('cadastrar.html', mensagemRetorno=retorno)
@app.route('/paginaCadastroDireto',methods=['POST'])
def paginaCadastroDireto():
    return render_template('cadastrarDireto.html')

# Editar ----------------------------------------------------------------------------------

# Abrindo a pagina de busca
@app.route('/search_term', methods=['POST'])
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
        nome_minusculo = busca_term.lower()
        nome = nome_minusculo
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


@app.route('/search_select',  methods=['POST'])
def search_select():
    import sqlite3
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT nome, ramal, setor, id FROM agendaInterna')
    ramais = c.fetchall()

    listaRamaisI = []
    listaRamaisD = []
    tipos = []
    for i in ramais:
        tipos.append('interno')
        listaRamaisI.append(i)

    c.execute('SELECT nome, ramal, setor, id FROM agendaDireta')
    ramais = c.fetchall()
    conexao.close()
    for i in ramais:
        tipos.append('direto')
        listaRamaisD.append(i)
    return render_template('search_select.html', rows=listaRamaisI, rows2=listaRamaisD)

'''
@app.route('/search_results_table',  methods=['POST'])
def search_results_table():
    dados = request.form['editar']
    teste = request.form.to_dict()
    print('teste:',teste)
    minha_lista = list((request.form.to_dict()).values())
    print('convertido:',minha_lista)
    print('dados:',dados)
    listaFiltros = dados.replace("(", "")
    listaFiltros = listaFiltros.replace(")", "")
    listaFiltros = listaFiltros.replace("[", "")
    listaFiltros = listaFiltros.replace("]", "")
    listaFiltros = listaFiltros.replace("'", "")
    #listaSetor = listaFiltros.split(",")
    listaFiltros = listaFiltros.replace(" ", "")
    listaFiltros = listaFiltros.split(",")
    #setor = str(listaSetor[2])
    #print('SETOR',setor)
    #print('SETOR tamanho', len(setor))
    print(listaFiltros)
    #return render_template('search_results.html',search_results=str(listaFiltros[0]),resultado_ramal=str(listaFiltros[1]),resultado_setor=setor,tipo_ramal=listaFiltros[3])
    return render_template('search_results.html',search_results=str(listaFiltros[0]),resultado_ramal=str(listaFiltros[1]),resultado_setor=listaFiltros[2],id=listaFiltros[3],tipo_ramal=listaFiltros[4])
'''
@app.route('/buscar_ramal_search_select',  methods=['POST'])
def buscar_ramal_search_select():
    busca = request.form['busca_term']
    rows = select_like(busca, str(busca))
    return render_template('search_select.html', rows=rows)

def select_like(int, str):
    conn = sqlite3.connect('agenda.db')
    c = conn.cursor()
    #cur.execute('SELECT * FROM agendaInterna')
    c.execute("SELECT nome, ramal, setor FROM agendaInterna WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (int,str))
    rows = c.fetchall()
    c.execute("SELECT nome, ramal, setor FROM agendaDireta WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (int,str))
    rows.extend(c.fetchall())
    conn.close()
    return rows

def select_id(int,str):
    if str=='interno':
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        #cur.execute('SELECT * FROM agendaInterna')
        c.execute("SELECT nome, ramal, setor FROM agendaInterna WHERE id = ?", (int,))
    elif str=='direto':
        conn = sqlite3.connect('agenda.db')
        c = conn.cursor()
        #cur.execute('SELECT * FROM agendaInterna')
        c.execute("SELECT nome, ramal, setor FROM agendaDireta WHERE id = ?", (int,))
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/search_results_table',  methods=['POST'])
def search_results_table():
    dados = request.form['editar']
    info = dados.replace(")", "")
    info = info.replace("(", "")
    info = info.replace("'", "")
    info = info.replace(" ", "")
    info = info.split(',')
    print(info)
    data = select_id(info[0],info[1]) # chama a função que busca pelo id e retorna as informações
    infodb = []
    for dados in data[0]:
        infodb.append(dados)
    return render_template('search_results.html',nome=infodb[0],ramal=infodb[1],setor=infodb[2],id=info[0],tipo_ramal=info[1])

@app.route('/search_results',  methods=['POST'])
def search_results():
    return render_template('search_results.html')

@app.route('/salvar_alteracao', methods=['POST'])
def salvar_alteracao():
    tipo_ramal = request.form['tipo_ramal']
    id = request.form['id']
    print(tipo_ramal)
    if request.form['action'] == 'cadastrar':
        conexao = sqlite3.connect('agenda.db')
        c = conexao.cursor()
        nome = request.form['nome']
        resultado_ramal = request.form['resultado_ramal']
        resultado_setor = request.form['resultado_setor']
        nome = nome.lower()
        ramal = int(resultado_ramal)
        setor = resultado_setor.lower()
        if (tipo_ramal=='interno'):
            c.execute('UPDATE agendaInterna SET nome = ?, ramal = ?, setor = ? WHERE id = ?', (nome, ramal, setor, id))
            conexao.commit()
            conexao.close()
            retorno = 'Ramal Interno: '+str(ramal)+' - '+nome+' - '+setor+' alterado com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
        elif(tipo_ramal=='direto'):
            c.execute('UPDATE agendaDireta SET nome = ?, ramal = ?, setor = ? WHERE ramal = ?', (nome, ramal, setor, ramal))
            conexao.commit()
            conexao.close()
            retorno = 'Ramal Direto: '+str(ramal)+' - '+nome+' - '+setor+' alterado com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
    elif request.form['action'] == 'excluir':
        conexao = sqlite3.connect('agenda.db')
        search_results = request.form['search_results']
        resultado_ramal = request.form['resultado_ramal']
        nome = search_results
        ramal = int(resultado_ramal)
        if(tipo_ramal=='interno'):
            c = conexao.cursor()
            c.execute("DELETE FROM agendaInterna WHERE id=?", (id,))
            conexao.commit()
            conexao.close()

            retorno = 'Ramal Interno: '+str(ramal)+' - '+nome+' excluido com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
        if(tipo_ramal=='direto'):
            c = conexao.cursor()
            c.execute("DELETE FROM agendaDireta WHERE id=?", (id,))
            conexao.commit()
            conexao.close()

            retorno = 'Ramal Direto: '+str(ramal)+' - '+nome+' excluido com sucesso!'
            return render_template('admin.html', mensagemRetorno=retorno)
        return render_template('admin.html', mensagemRetorno='Erro: conflito interno')
@app.route('/abrirAgenda', methods=['POST'])
def abrirAgenda():
    # Importando agenda interna
    conn = sqlite3.connect('agenda.db')
    cur = conn.cursor()
    #cur.execute('SELECT * FROM agendaInterna')
    cur.execute('SELECT nome, ramal, setor FROM agendaInterna ORDER BY nome')
    rows = cur.fetchall()
    # Importando agenda direta
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT nome, ramal, setor FROM agendaDireta ORDER BY nome')
    rows2 = c.fetchall()
    #rows.extend(rows2)
    return render_template('table.html', rows=rows, rows2=rows2, ativados=['interno','direto'], filtro='desativado')
@app.route('/abrirFiltro', methods=['POST'])
def abrirFiltro():
    abrir = 'sim'
    return render_template('table.html', ativados=['interno','direto'], filtro='desativado',abrir=abrir)
@app.route('/abrirAgendaFiltrando', methods=['POST'])
def abrirAgendaFiltrando():
    filtros = request.form.getlist('tipo')
    if (filtros==''):
        filtros = ['interno','direto']
    print(filtros)
    rows = []
    rows2 = []
    if (len(filtros)>1):
        if (filtros[0]=='interno') and (filtros[1]=='direto'):
            return abrirAgenda()
        
    for i in filtros:
        if (i=='interno'):
            # Importando agenda interna
            conn = sqlite3.connect('agenda.db')
            cur = conn.cursor()
            #cur.execute('SELECT * FROM agendaInterna')
            cur.execute('SELECT nome, ramal, setor FROM agendaInterna ORDER BY nome')
            rows = cur.fetchall()
        # Importando agenda direta
        if(i=='direto'):
            conexao = sqlite3.connect('agenda.db')
            c = conexao.cursor()
            c.execute('SELECT nome, ramal, setor FROM agendaDireta ORDER BY nome')
            rows2 = c.fetchall()
    rows.extend(rows2)
    return render_template('ramais.html', rows=rows, ativados=filtros, filtro='desativado')

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
            c.execute("SELECT nome, ramal FROM agendaInterna WHERE ramal LIKE '%' || ? || '%' OR nome LIKE '%' || ? || '%'", (i,str(i)))
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
        return render_template('admin.html',nome=session['usuario'],acesso=session['nivel_acesso'])
    else:
        return render_template('login.html')

@app.route('/validarLogin', methods=['POST'])
def validarLogin():
    usuario = request.form['usuario']
    senha = request.form['senha']
    # Importando agenda interna
    conn = sqlite3.connect('teste.db')
    cur = conn.cursor()
    #cur.execute('SELECT * FROM agendaInterna')
    cur.execute('SELECT usuario, senha, acesso, id FROM usuarios ORDER BY usuario')
    lista = cur.fetchall()
    for i in lista:
        if i[0]==usuario:
            print('Usuario encontrado')
            if (i[1]==senha):
                print('Senha validada, acesso liberado!')
                print('ID: ',i[3])
                print('Nivel de acesso: ',i[2])
                logado.append(i)
                print('logado',logado)
                session['logged_in'] = True
                session['nivel_acesso'] = i[2]
                session['usuario'] = usuario
                return render_template('admin.html', nome=usuario, acesso=i[2], id=i[3])
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


@app.route('/uploadDrop', methods=['POST'])
def uploadDrop():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    retorno = 'Arquivo {} enviado com sucesso!'.format(file.filename)
    return render_template('editarBanner.html',mensagemRetorno=retorno)


@app.route('/upload', methods=['POST'])
def upload():
    # Verifica se o arquivo está presente no request
    if 'file' not in request.files:
        retorno = 'Nenhum arquivo enviado'
        return render_template('editarBanner.html',mensagemRetorno=retorno)

    file = request.files['file']

    # Verifica se o arquivo possui um nome
    if file.filename == '':
        retorno = 'Nome do arquivo não encontrado'
        return render_template('editarBanner.html',mensagemRetorno=retorno)

    # Salva o arquivo no diretório de upload
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))


    retorno = 'Arquivo {} enviado com sucesso!'.format(file.filename)
    return render_template('editarBanner.html',mensagemRetorno=retorno)

@app.route('/excluirImagem', methods=['POST'])
def excluirImagem():
    botaoExcluir = request.form['botaoExcluir']
    print(botaoExcluir)
    # Caminho completo para o arquivo que será excluído
    nomeArquivo = 'static/images/Banners/'+botaoExcluir
    file_path = nomeArquivo
    
    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        # Exclui o arquivo
        os.remove(file_path)
        retorno = 'Arquivo excluído com sucesso!'
        return render_template('editarBanner.html',mensagemRetorno=retorno)
    else:
        retorno = 'Arquivo não encontrado.'
        return render_template('editarBanner.html',mensagemRetorno=retorno)

@app.route('/listarDiretorio', methods=['POST'])
def listarDiretorio():
    # Diretório onde estão os arquivos
    directory = 'static/images/Banners'
    
    # Obtém a lista de arquivos existentes no diretório
    file_list = os.listdir(directory)
    
    print('arquivos',file_list)

    return render_template('editarBanner.html', files=file_list)
@app.route('/renomearImagem', methods=['POST'])
def renomearImagem():
    # Diretório onde estão as imagens
    directory = 'static/images/Banners'

    nomeNovo = request.form['nome_novo']
    nomeAntigo = request.form['nome_antigo']
    # Nome antigo do arquivo
    old_name = nomeAntigo
    
    # Novo nome desejado para o arquivo
    new_name = nomeNovo
    
    # Caminho completo para o arquivo antigo
    old_path = os.path.join(directory, old_name)
    
    # Caminho completo para o arquivo com o novo nome
    new_path = os.path.join(directory, new_name)
    
    # Verifica se o arquivo antigo existe
    if os.path.exists(old_path):
        # Renomeia o arquivo
        os.rename(old_path, new_path)
        retorno = 'Arquivo renomeado com sucesso!'
        return render_template('editarBanner.html',mensagemRetorno=retorno)
    else:
        retorno = 'Arquivo não encontrado.'
        return render_template('editarBanner.html',mensagemRetorno=retorno)
@app.route('/ti', methods=['POST'])
def ti():
    return render_template('TI.html')

@app.route('/download')
def download_file():
    # Caminho para o arquivo que você deseja disponibilizar para download
    path_to_file = '/static/download/teste.txt'

    return "<a href='{{ url_for('get-file') }}'>Download</a>"

@app.route('/get-file')
def get_file():
    # Caminho para o arquivo que você deseja disponibilizar para download
    path_to_file = '/static/download/teste.txt'

    # Envia o arquivo para o cliente
    return send_file(path_to_file, as_attachment=True)

if __name__ == '__main__':
    #app.run(host='192.168.20.125')
    app.run(debug=True)