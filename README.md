# ⚽ API REST de Jogadores

[![Python](https://img.shields.io/badge/Python-blue?logo=python&logoColor=white)](https://www.python.org/) 
[![FastAPI](https://img.shields.io/badge/FastAPI-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) 
[![SQLite](https://img.shields.io/badge/SQLite-blue?logo=sqlite&logoColor=white)](https://www.sqlite.org/) 
[![Pandas](https://img.shields.io/badge/Pandas-blue?logo=pandas&logoColor=white)](https://pandas.pydata.org/) 
[![Requests](https://img.shields.io/badge/Requests-black?logo=python&logoColor=white)](https://docs.python-requests.org/en/latest/)  

---

## 🌟 Introdução
Este projeto apresenta uma **API CRUD** desenvolvida em **FastAPI** com integração ao banco de dados **SQLite**.  
Além disso, inclui um **cliente em Python** que consome a API via terminal, utilizando **requests** para requisições HTTP e **pandas** para exibir os resultados em formato de tabela.  

---

## 🎯 Objetivo
O projeto foi criado para **praticar integração entre APIs e bancos de dados** e demonstrar como dados podem ser **armazenados, manipulados e disponibilizados** para análise de forma eficiente.  
O foco está em **disponibilizar informações de jogadores de futebol** de maneira acessível, escalável e organizada.  

---

## 🛠 Tecnologias Utilizadas
- 🐍 **Python** – Linguagem de programação principal  
- ⚡ **FastAPI** – Framework para criação da API  
- 🗄 **SQLite** – Banco de dados relacional local  
- 📦 **Requests** – Consumo de endpoints via HTTP  
- 📊 **Pandas** – Exibição e manipulação de dados em DataFrame  

---

## 🚀 Funcionalidades
A API e o cliente possuem as seguintes funcionalidades:

### Endpoints (FastAPI)
- ➕ Criar jogador (POST)  
- 📋 Listar todos os jogadores (GET)    
- 🏟 Filtrar jogadores por time (GET)  
- ✏️ Atualizar jogador (PUT)  
- ❌ Excluir jogador (DELETE)  

### Cliente no Terminal
- 📊 Exibir jogadores em formato de tabela com **pandas**  
- 🔄 Menu interativo para listar, criar, atualizar, excluir e filtrar jogadores  

---

## 🗂 Estrutura de Arquivos
```text
├── banco_api.py  # Código da API CRUD em FastAPI
├── requisicao_api.py  # Cliente Python para consumir a API via terminal
├── jogadores.db  # Banco de dados SQLite (gerado automaticamente)
└── README.md  # Este arquivo
```

---

## 👨‍💻 Autor do Projeto

Desenvolvido por **[Kaique Gomes]** — estudante de Ciência de Dados e Desenvolvimento de Sistemas.

📫 [LinkedIn](https://www.linkedin.com/in/kaique-gomes-dev)  
🐙 [GitHub](https://github.com/Kaique-Gomes-de-Jesus)  