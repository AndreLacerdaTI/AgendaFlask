
import sqlite3

printar = "SELECT * FROM agendaInterna"

conexao = sqlite3.connect('agenda.db')
cursor = conexao.cursor()

cursor.execute(printar)
agendaInterna = cursor.fetchall()
print("Agenda Interna")
for i in agendaInterna:
  print("Nome: ", i[1], "Ramal", i[2])

printarDireta = "SELECT * FROM agendaDireta"

conexao = sqlite3.connect('agenda.db')
cursor = conexao.cursor()

cursor.execute(printarDireta)
agendaDireta = cursor.fetchall()
print("Agenda Direta")
for i in agendaDireta:
  print("Nome: ", i[1], "Ramal", i[2])