from json import dumps, loads
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError

# neste codigo foi utulizado apenas o endpoint relatorio e aluno.
# os dados manipulados são de alunos e relatorios, o ideal seria esses dados estarem salvos em um banco de dados.
# os dados que devem ser fornecidos de inicio para o json, em alunos é idade e disciplina, e em relatorio: titulo, criacao e aluno(dados da classe aluno)

# Inicializa as listas vazias de alunos e relatorios
alunos = []
relatorios = []

# Classe AlunoSchema que tem como parametro Schema que é utilizado para definir a estrutura dos dados a ser utilizada. 
class AlunoSchema(Schema):
    idade = fields.Integer(required=True) # variável idade que recebe apenas números inteiros utilizando o metódo Integer. E é um campo obrigatório definido.
    disciplina = fields.String(required=True) # variável idade que recebe somente strings utilizando o metódo String. E é um campo obrigatório definido  

# Classe RelatorioSchema que tem como parametro Schema que é utilizado para definir a estrutura dos dados a ser utilizada. 
class RelatorioSchema(Schema):
    titulo = fields.Str() # variável titulo que recebe apenas Strings 
    criacao = fields.Date() # variável criacao, o dado é em formato de data
    aluno = fields.Nested(AlunoSchema()) # nesta variável, ele chama a classe AlunoSchema para validar aluno.

# Função para cadastrar aluno
def cadastrarAluno(json_str: str):
    aluno = loads(json_str) # obtem a lista de alunos, e converte de json para objeto
    alunos.append(aluno) # adiciona o aluno na lista de alunos
    return aluno # retorna o objeto aluno

# Função para cadastrar relatorio
def cadastrarRelatorio(json_str: str):
    relatorio = loads(json_str) # obtem a lista de relatorio, e converte de json para objeto
    relatorios.append(relatorio)  # adiciona relatorios na lista de relatorios
    return relatorio # retorna relatorio

# inicia a aplicação flask
app = Flask(__name__)

# endpoint post utilizado para enviar requisição para adicionar aluno
# o objetivo é receber os dados como Json de aluno e validar utilizando marshmallow
@app.post('/aluno')
def aluno_post():
    # obtem os dados enviados
    request_data = request.json
    # instancia AlunoSchema para a validação
    schema = AlunoSchema()
    # entra no try
    try:
        # valida os dados do corpo da requisição
        result = schema.load(request_data)
        # salva para formato Json
        data_now_json_str = dumps(result)
        # adiciona aluno na lista
        response_data = cadastrarAluno(data_now_json_str)
    # tratamento de erro, caso dê errado
    except ValidationError as err:
        return jsonify(err.messages), 400 # retorna a mensagem de erro

    return jsonify(response_data), 200 # retorna os dados de response_data

# endpoint post utilizado para enviar requisição para adicionar aluno,
# o objetivo é receber os dados como Json de relatorio e validar utilizando marshmallow
@app.post('/relatorio')
def relatorio_post():
    # obtem os dados enviados 
    request_data = request.json
    # instancia RelatorioSchema para validação
    schema = RelatorioSchema()
    # entra no try
    try:
        # valida os dados do corpo da requisição
        result = schema.load(request_data)
        # salva no formato Json
        data_now_json_str = dumps(result)
        # adiciona relatorios na lista de relatorios
        response_data = cadastrarRelatorio(data_now_json_str)
    # tratamento de erro, caso dê errado
    except ValidationError as err:
        return jsonify(err.messages), 400 # retorna a mensagem de erro
    

    return jsonify(response_data), 200 # retorna os dados de response_data
