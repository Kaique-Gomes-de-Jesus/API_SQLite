import requests
import pandas as pd
from typing import Dict, Any, Optional

BASE_URL = "http://127.0.0.1:8000/jogadores/"

#Função auxiliar para chamar a API
def chamar_api(metodo:str, 
               endpoint:str="", 
               dados:Optional[Dict]=None) -> Optional[Any]  : #Apontar a variável Any para optional (exclusivo api via terminal)
    #Fazer a requisição http(get, post, put, delete)
    url = f"{BASE_URL}{endpoint}"
    #Variável headers {tipo aplicação JSON}
    headers = {"Content-Type":"application/json"}
    try:
        #Verificar método
        if metodo =="GET":
            response = requests.get(url)

        elif metodo == "POST":
            response = requests.post(url, json=dados, headers=headers) #Enviar os dados ao servidor

        elif metodo == "PUT":
            response = requests.put(url, json=dados, headers=headers) #Enviar os dados ao servidor

        elif metodo == "DELETE":
            response = requests.delete(url)

        else:
            raise ValueError(f"Método inválido: {metodo}")

        #Levantar exceção para códigos de erro HTTP
        response.raise_for_status()

        return response.json()
    
    except requests.exceptions.RequestException as erro:
        print(f"ERRO ao chamar a API: {erro}")

#Função listar todos os jogadores no terminal
def listar_jogadores():
    #Listar todos os jogadores via tabela usando o pandas
    print("Lista de todos os jogadores: \n")
    #Chamar API GET
    jogadores = chamar_api("GET")
    if jogadores:
        try:
            df = pd.DataFrame(jogadores)
            #Pega tabela do banco de dados em texto e joga no terminal
            #Sem o index da ordem
            print(df.to_string(index=False)) 

        except ImportError:
            #Caso o pandas não esteja instalado, exibir como lista
            for i in jogadores:
                print(f"""
                    ID:{i["id"]}
                    Nome:{i["nome"]}
                    Idade:{i["idade"]}
                    Time:{i["time"]}
                """)
    else:
        print("Nenhum jogador encontrado ou erro na API.")

#Função listar jogadores por time
def buscar_pelo_time():
    time = str(input("Digite o time para saber os jogadores: "))
    print(f"Jogadores do time: {time}")

    buscar_jogadores_time = chamar_api("GET", str(f"time/{time}"))

    if buscar_jogadores_time:
        for jogador in buscar_jogadores_time:
            print(jogador)

    else:
        print(f"Nenhum jogador para o time {time}")
        

#Função criar jogador via terminal
def criar_jogador():
    print("Criar um novo jogador: \n")
    nome = str(input("Digite o nome do jogador: "))
    idade = int(input("Digite a idade do jogador: "))
    time = str(input("Digite o time do jogador: "))
    #Criar um dicionário para passar os dados para API
    dados = {"nome":nome, "idade":idade, "time":time}
    novo_jogador = chamar_api("POST", dados = dados)
    if novo_jogador:
        print(f"Jogador criado com sucesso: {novo_jogador['nome']}")
    else:
        print("Falha ao criar o jogador.")

#Função atualizar o jogador
def atualizar_jogador():
    jogador_id = int(input("Digite o ID do jogador para atualizar: "))
    print(f"Atualizar o jogador ID {jogador_id}")

    #Input para atualizar
    atualizacao = int(input("""
                        O que deseja atualizar ? 
                        1 - Nome
                        2 - Idade 
                        3 - Time: 
                            """))
    #Dicionário vazio
    dados = {}
    #Verificar o que deseja atualizar e #if para cada dado: nome, idade, time
    if atualizacao == 1:
        novo_nome = str(input("Digite o novo nome: "))
        if novo_nome:
            dados["nome"] = novo_nome

    elif atualizacao == 2:
        nova_idade = int(input("Digite a nova idade: "))
        if nova_idade:
            dados["idade"] = nova_idade

    elif atualizacao == 3:
        novo_time = str(input("Digite o novo time: "))
        if novo_time:
            dados["time"] = novo_time
    
    if not dados:
        print("Nenhum dado encontrado para atualizar.")
        return
    
    #Chama api para fazer o post
    jogador_atualizado = chamar_api("PUT", str(jogador_id), dados = dados)
    if jogador_atualizado:
        print("Jogador atualizado")
    else:
        print("Falha ao atualizar o jogador.")

#Função deletar o jogador
def deletar_jogador():
    jogador_id = int(input("Digite o ID do jogador para deletar: "))
    print(f"Excluir jogador ID {jogador_id}")
    resultado = chamar_api("DELETE",str(jogador_id))
    if resultado:
        print("Jogador deletado.")
    else:
        print("Falha para deletar o jogador.")

def main():
    while True:
        print("""
        MENU DE ESCOLHA:
        1 - Listar jogadores.
        2 - Criar jogador (Nome, idade, time).
        3 - Atualizar jogador.
        4 - Deletar jogador.
        5 - Listar jogadores por time.
        0 - Sair do programa.
        """)
        escolha = int(input("Digite a sua escolha: "))

        if escolha == 1:
            listar_jogadores()

        elif escolha == 2:
            criar_jogador()
        
        elif escolha == 3:
            atualizar_jogador()
        
        elif escolha == 4:
            deletar_jogador()

        elif escolha == 5:
            buscar_pelo_time()

        elif escolha == 0:
            print("Saindo do sistema...")
            break

if __name__ == "__main__":
    main()
