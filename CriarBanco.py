import sqlite3
'''
CriarBancoUsuarios = """ CREATE TABLE usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT NOT NULL,
                        senha TEXT NOT NULL,
                        acesso INTEGER
                      );"""
CriarAgendaInterna = """ CREATE TABLE IF NOT EXISTS agendaInterna (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        nome text NOT NULL,
                        ramal integer NOT NULL
                      ); """
CriarAgendaDireta = """ CREATE TABLE IF NOT EXISTS agendaDireta (
                        id integer PRIMARY KEY AUTOINCREMENT,
                        nome text NOT NULL,
                        ramal integer NOT NULL
                      ); """                      
'''
conexao = sqlite3.connect('teste.db')
cursor = conexao.cursor()
#cursor.execute(CriarBancoUsuarios)
#cursor.execute(CriarAgendaDireta)

usuario = 'Wagner'
senha = 123
acesso = 2
conexao = sqlite3.connect('teste.db')
c = conexao.cursor()
c.execute("INSERT INTO usuarios (usuario, senha, acesso) VALUES (?, ?, ?)", (usuario, senha, acesso))

conexao.commit()
conexao.close()
