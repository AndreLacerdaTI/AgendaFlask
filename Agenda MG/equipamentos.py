from flask import Flask, render_template, flash, redirect, url_for
from flask import request
from bancoComputadores import *

@app.route('/listar_equipamentos',methods=['POST'])
def listar_equipamentos():
    lista = list(ListarEquipamentos())
    print(lista)
    return render_template('equipamentos.html',equipamentos=lista[0])

@app.route('/listar_licenca',methods=['POST'])
def listar_licenca():
    id_licenca = request.form['id_licenca']
    licenca = select_licenca_id(id_licenca)
    flash(licenca)
    return render_template('equipamentos.html',licenca=licenca)

@app.route('/editar_equipamento',methods=['POST'])
def editar_equipamento():
    id_equipamento = request.form['id_equipamento']
    print(id_equipamento)
    equipamento = select_equipamento_id(id_equipamento)
    licencas = ListarLicencas()
    #flash(equipamento)
    return render_template('equipamentos.html',equipamento=equipamento, licencas=licencas)

@app.route('/salvar_alteracoes_equipamento',methods=['POST'])
def salvar_alteracoes_equipamento():
    usuario = request.form['usuario']
    licencas = request.form['licencas']
    print("Licenca:",licencas)
    return render_template('equipamentos.html',notificacao='Alterações realizadas com sucesso!')