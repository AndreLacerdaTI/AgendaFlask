from flask import Flask, request
import sqlite3

def criarBanco():
    #LiberarForeignKey = """PRAGMA foreign_keys = OFF;"""
    CriarTabelaLicenca= """ CREATE TABLE licenca (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            descricao TEXT NOT NULL,
                            chave_licenca TEXT NOT NULL,
                            id_microsoft TEXT,
                            nf INTEGER,
                            fornecedor TEXT
                        );"""    
    CriarTabelaEquipamento= """ CREATE TABLE equipamento (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            cod_siggi TEXT NOT NULL,
                            tipo_equipamento TEXT NOT NULL,
                            ip INTEGER,
                            usuario TEXT,
                            licenca_id INTEGER,
                            FOREIGN KEY (licenca_id) REFERENCES licenca(id)
                        );"""               
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute(CriarTabelaLicenca)
    #cursor.execute(LiberarForeignKey)
    cursor.execute(CriarTabelaEquipamento)
    #cursor.execute(CriarAgendaDireta)

    return 'banco'

def InserirDadosLicenca():
    
    descricao = 'Windows 7 Professional x86'
    chave_licenca = 'MGB87-4MPCJ-BMRGJ-QMV27-W24M3'
    id_microsoft = '00371-OEM-9046295-32206'
    nf = 28966
    fornecedor = 'Ômega Informática LTDA'

    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    c = conexao.cursor()
    c.execute("INSERT INTO licenca (descricao, chave_licenca, id_microsoft,nf,fornecedor) VALUES (?, ?, ?, ?, ?)", (descricao, chave_licenca, id_microsoft,nf,fornecedor))

    conexao.commit()
    conexao.close()

    return 'banco'

def InserirDadosEquipamento():
    cod_siggi = '396'
    tipo_equipamento = 'Desktop Montado'
    ip = '95'
    usuario = 'Ana Elisa Rodrigues'
    licenca_id = 1

    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    c = conexao.cursor()
    c.execute("INSERT INTO equipamento (cod_siggi, tipo_equipamento, ip,usuario,licenca_id) VALUES (?, ?, ?, ?, ?)", (cod_siggi, tipo_equipamento, ip,usuario,licenca_id))

    conexao.commit()
    conexao.close()

def ListarEquipamentos():
    equipamentos = []
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM equipamento')
    equipamentos = list(cursor.fetchall())
    conexao.close()

    licencas = []
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM licenca')
    licencas = cursor.fetchall()
    return equipamentos, licencas

def FiltrarEquipamentos(filtro):
    equipamentos = []
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    print(filtro)
    if (filtro=='cod_siggi'):
        query = "SELECT * FROM equipamento ORDER BY CAST(" + filtro + " AS INTEGER)"
    else:
        query = ("SELECT * FROM equipamento ORDER BY " + filtro)

    cursor.execute(query)
    equipamentos = list(cursor.fetchall())
    conexao.close()

    licencas = []
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM licenca')
    licencas = cursor.fetchall()
    return equipamentos, licencas

def ListarLicencas():
    licencas = []
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM licenca')
    licencas = cursor.fetchall()
    return licencas

def select_equipamento_id(int):
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM equipamento WHERE id = ?", (int,))
    #equipamentos = list(cursor.fetchall())
    equipamentos_banco = cursor.fetchall()
    equipamentos = []
    for equipamento in equipamentos_banco:
        for i in equipamento:
            equipamentos.append(i)
            print(i)
    conexao.close()
    return equipamentos

def select_licenca_id(int):
    conexao = sqlite3.connect('banco_de_dados_equipamentos_licencas.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM licenca WHERE id = ?", (int,))
    #licencas = cursor.fetchall()
    licencas_banco = cursor.fetchall()
    licencas = []
    for licenca in licencas_banco:
        for i in licenca:
            licencas.append(i)
            print(i)
    return licencas