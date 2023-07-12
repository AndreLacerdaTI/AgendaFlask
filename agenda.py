import sqlite3

def select_direta():
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT * FROM agendaDireta')
    direta = c.fetchall()
    conexao.close()
    return direta

def select_interna():
    conexao = sqlite3.connect('agenda.db')
    c = conexao.cursor()
    c.execute('SELECT * FROM agendaInterna')
    interna = c.fetchall()
    conexao.close()
    return interna