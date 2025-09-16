# 👨‍💼 Cadastro de Funcionário com Python / PostgreSQL

Aplicativo simples para **inserção, exclusão, atualização e listagem** de funcionários, com interface gráfica feita em **Flet** e banco de dados **PostgreSQL**.

---

## 📌 Visão Geral

Este sistema permite que o usuário gerencie colaboradores de forma intuitiva, com:

- Interface gráfica com Flet para facilitar a interação.
- Operações CRUD completas: **Create**, **Read**, **Update**, **Delete**.
- Integração segura com banco PostgreSQL para persistência de dados.
- Formatação automática de CPF e valores monetários para melhor usabilidade.

---

## 🧰 Funcionalidades Principais

| Funcionalidade | Descrição |
|----------------|-----------|
| Inserir Funcionário | Registro de novo funcionário, verificando se o ID já existe. |
| Excluir Funcionário | Remoção de funcionário pelo ID. |
| Atualizar Funcionário | Alterar campo específico (nome, cargo, nacionalidade, cpf ou salário). |
| Listar Funcionários | Exibir todos os funcionários cadastrados, com dados completos. |
| Validação / Formatação | CPF formatado, salário com vírgulas e separadores, validação de campos obrigatórios. |

---

## 💻 Tecnologias

- **Linguagem**: Python  
- **Interface Gráfica**: Flet 📱  
- **Banco de Dados**: PostgreSQL  
- **Driver de conexão**: `psycopg2`  

---


