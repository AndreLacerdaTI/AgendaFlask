""" CONVERTENDO TODOS OS MACs COM SEPARAÇÃO '-' PARA SEPARAÇÃO EM ':' """

import sqlite3 # IMPORTANDO BANCO PARA FAZER A BUSCA
conexao = sqlite3.connect('tabelaIP.db')
c = conexao.cursor()
c.execute('SELECT id, mac FROM tabelaIP')
tabelaMAC = c.fetchall()
conexao.close()

def convertendoMac(int): # FUNÇÃO QUE CONVERTE E SALVA
    import sqlite3
    conexao = sqlite3.connect('tabelaIP.db')
    c = conexao.cursor()
    c.execute("SELECT mac FROM tabelaIP WHERE id = ?", (int,))
    mac = c.fetchall()
    #print("MAC:", mac[0])
    for i in mac:
        print("MAC:", i[0])
        mac_antigo = i[0]
        mac_novo = mac_antigo.replace("-", ":")
        print('MAC novo: ',mac_novo)
        c.execute('UPDATE tabelaIP SET mac = ? WHERe id = ?', (mac_novo, int))
        conexao.commit()
    conexao.close()
    return True

for i in tabelaMAC: # PERCORRENDO A LISTA PROCURANDO POR MACs FORMATADOS ERRADOS
    valor = i[1]
    #print(i)
    if (valor != None):
        #if (valor[2:3]==':'):
            #print("É um MAC separado por :")
        if (valor[2:3]=='-'):
            print("É um MAC separado por -")
            id = i[0]
            print(id)
            convertendoMac(id)