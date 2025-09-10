#Banco de dados com API
#Importando fastapi para criar a API
from fastapi import FastAPI, HTTPException #HTTP para usar raise
#Importando pydantic para modelar os dados e validação
from pydantic import BaseModel
#Banco SQLite
import sqlite3
#Importando optional e list para tipagem de dados
from typing import Optional, List

#Instância do FastAPI
app = FastAPI(title="CRUD de Jogadores com SQLite")
#Nome do arquivo do banco de dados SQLite
BANCO_DE_DADOS = "jogadores.db"

# 1ºFunção para conectar ao banco e criar a tabela
def conectar_bd():
    conexao = sqlite3.connect(BANCO_DE_DADOS)
    cursor = conexao.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS jogadores (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   idade INTEGER NOT NULL,
                   time TEXT NOT NULL
                   )"""
    )
    conexao.commit()
    return conexao, cursor

#Modelo pydantic para criar um jogador (modelos obrigatórios)
class JogadorCreate(BaseModel):
    nome:str
    idade:int
    time:str

#Modelo pydantic para atualizar um jogador (campos opcionais)
class JogadorUpdate(BaseModel):
    nome: Optional[str] = None
    idade: Optional[int] = None
    time: Optional[str] = None

#Modelo pydantic para representar um jogador completo (com ID)
class Jogador(BaseModel):
    id:int
    nome:str
    idade:int
    time:str

#GET: Listar todos os jogadores
@app.get("/jogadores/", response_model= List[Jogador])
async def listar_jogadores():
    #Conecta ao banco
    conexao, cursor = conectar_bd()
    #Query para selecionar todos os jogadores
    cursor.execute("""
                   SELECT 
                        id, nome, idade, time
                   FROM
                        jogadores
                   """)
    #Traz os dados com todas as linhas de uma vez
    jogadores = cursor.fetchall()
    #Fecha a conexão 
    conexao.close()
    #Retorna uma conversão dos resultados em uma lista de dicionários no formato do modelo do Jogador
    return [ {"id":j[0], "nome":j[1], "idade":j[2], "time":j[3]} for j in jogadores ]

#GET: Pegar um jogador específico pelo ID
@app.get("/jogadores/{jogador_id}", response_model=Jogador)
async def pegar_jogador(jogador_id:int):
    conexao, cursor = conectar_bd()
    cursor.execute("""
        SELECT 
            id, nome, idade, time
        FROM
            jogadores
        WHERE
            id = ?""",
            (jogador_id,)
    )
    #Traz os dados linha por linha
    jogador = cursor.fetchone()
    conexao.close()

    #Verifica se o jogador foi encontrado
    if jogador:
        #Retorna o jogador no formato do modelo Jogador
        return {"id":jogador[0], "nome":jogador[1], "idade":jogador[2], "time":jogador[3]}
    #Se não encontrado, levanta uma exceção HTTP 404
    raise HTTPException(status_code=404, detail="Jogador não encontrado")

#GET: Filtrar jogadores por time
@app.get("/jogadores/time/{time}", response_model=List[Jogador])
async def pegar_jogadores_por_time(time:str):
    conexao, cursor = conectar_bd()
    cursor.execute("""
        SELECT
            id, nome, idade, time
        FROM
            jogadores
        WHERE
            time = ?""",
                   (time,)
    )
    jogadores = cursor.fetchall()
    conexao.close()
    
    if jogadores:
        return [ {"id":j[0], "nome":j[1], "idade":j[2], "time":j[3]} for j in jogadores ]
    raise HTTPException(status_code=404, detail=f"Nenhum jogador encontrado para o time {time}")

#POST: Criar um novo jogador
@app.post("/jogadores/", response_model=Jogador)
async def criar_jogador(jogador: JogadorCreate):
    conexao, cursor = conectar_bd()
    #Insere o novo jogador sem especificar o ID
    cursor.execute("""
    INSERT INTO jogadores
        (nome,idade,time)
    VALUES
        (?,?,?)""",
        (jogador.nome,jogador.idade,jogador.time)
    )

    #Obtém o ID do jogador recém-criado
    novo_id = cursor.lastrowid #lastrowid = última linha
    conexao.commit()
    conexao.close()
    return {"id":novo_id, "nome":jogador.nome, "idade":jogador.idade, "time":jogador.time}

#PUT: Atualizar um jogador existente
@app.put("/jogadores/{jogador_id}", response_model=Jogador)
async def atualizar_jogador(jogador_id:int, jogador_atualizado: JogadorUpdate):
    conexao, cursor = conectar_bd()
    cursor.execute("""
        SELECT
            id, nome, idade, time
        FROM
            jogadores
        WHERE
            id = ?""",
            (jogador_id,)
    )
    jogador_existente = cursor.fetchone()
    #Verifica se o jogador existe
    if not jogador_existente:
        conexao.close()
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    #Usa os valores existentes como padrão se os novos não forem fornecidos
    nome = jogador_atualizado.nome if jogador_atualizado.nome is not None else jogador_existente[1]
    idade = jogador_atualizado.idade if jogador_atualizado.idade is not None else jogador_existente[2]
    time = jogador_atualizado.time if jogador_atualizado.time is not None else jogador_existente[3]
    #Atualiza o jogador no banco
    cursor.execute("""
        UPDATE
            jogadores
        SET
            nome=?, idade=?, time=?
        WHERE
            id = ?""",
            (nome, idade, time, jogador_id)
    )
    conexao.commit()
    conexao.close()
    #Retorna o jogador atualizado
    return {"id":jogador_id, "nome":nome, "idade":idade, "time":time}

#DELETE: Excluir um jogador
@app.delete("/jogadores/{jogador_id}")
async def excluir_jogador(jogador_id:int):
    conexao, cursor = conectar_bd()
    cursor.execute("""
        SELECT
            id
        FROM
            jogadores
        WHERE
            id = ?""",
            (jogador_id,)
    )

    if not cursor.fetchone:
        conexao.close()
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    #Deleta o jogador no banco
    cursor.execute("""
        DELETE
        FROM
            jogadores
        WHERE
            id = ?""",
            (jogador_id,)
    )
    conexao.commit()
    conexao.close()
    #Retorna uma mensagem de sucesso
    return {"mensagem":f"Jogador {jogador_id} excluído com sucesso"}