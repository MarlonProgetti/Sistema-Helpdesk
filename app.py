from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tha15Ma11#",
        database="helpdesk_tcc"
    )

@app.route('/api/chamados', methods=['GET'])
def listar_chamados():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    # Busca os chamados no banco
    cursor.execute("SELECT * FROM chamados ORDER BY data_abertura DESC")
    meus_chamados = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return jsonify(meus_chamados)

@app.route('/api/chamados', methods=['POST'])
def abrir_chamado():
    dados = request.json 
    
    titulo = dados.get('titulo')
    descricao = dados.get('descricao')
    categoria = dados.get('categoria')
    usuario_id = dados.get('usuario_id') # Meu usuario fixo por enquanto
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Insere no banco de dados
    sql = "INSERT INTO chamados (titulo, descricao, categoria, usuario_id) VALUES (%s, %s, %s, %s)"
    valores = (titulo, descricao, categoria, usuario_id)
    
    cursor.execute(sql, valores)
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
    return jsonify({"mensagem": "Chamado aberto com sucesso!"}), 201

@app.route('/api/chamados/<int:id>', methods=['PUT'])
def atualizar_chamado(id):
    dados = request.json # Pega os dados que o técnico digitou no Front-end
    
    novo_status = dados.get('status')
    nota_resolucao = dados.get('nota_resolucao')
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Atualiza o chamado específico no banco de dados
    sql = "UPDATE chamados SET status = %s, nota_resolucao = %s WHERE id = %s"
    valores = (novo_status, nota_resolucao, id)
    
    cursor.execute(sql, valores)
    conexao.commit() # Salva as alterações
    
    cursor.close()
    conexao.close()
    
    return jsonify({"mensagem": "Chamado atualizado com sucesso!"}), 200

# ROTA 4: Excluir um chamado (DELETE)
@app.route('/api/chamados/<int:id>', methods=['DELETE'])
def excluir_chamado(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Comando SQL para apagar a linha da tabela
    sql = "DELETE FROM chamados WHERE id = %s"
    valores = (id,) # Essa vírgula é obrigatória no Python quando temos apenas 1 valor
    
    cursor.execute(sql, valores)
    conexao.commit() # Salva as alterações no banco
    
    cursor.close()
    conexao.close()
    
    return jsonify({"mensagem": "Chamado excluído com sucesso!"}), 200

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True, port=5000)