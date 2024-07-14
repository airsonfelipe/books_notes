import streamlit as st
import streamlit_authenticator as stauth
import os
import json

# Configurações de autenticação
names = ["User1", "User2"]
usernames = ["user1", "user2"]
passwords = ["password1", "password2"]

hashed_passwords = stauth.Hasher(passwords).generate()

# Criação de um arquivo de configuração de autenticação
auth_config = {
    "credentials": {
        "usernames": {
            usernames[0]: {"name": names[0], "password": hashed_passwords[0]},
            usernames[1]: {"name": names[1], "password": hashed_passwords[1]},
        }
    },
    "cookie": {
        "name": "auth_cookie",
        "key": "random_signature_key",
        "expiry_days": 30,
    },
    "preauthorized": {
        "emails": [
            "user1@example.com",
            "user2@example.com"
        ]
    }
}

# Salva as configurações de autenticação em um arquivo JSON
with open('auth_config.json', 'w') as config_file:
    json.dump(auth_config, config_file)

# Inicializa o autenticador
authenticator = stauth.Authenticate(
    credentials=auth_config['credentials'],
    cookie_name=auth_config['cookie']['name'],
    key=auth_config['cookie']['key'],
    expiry_days=auth_config['cookie']['expiry_days'],
    preauthorized=auth_config['preauthorized']
)

# Login do usuário
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Bem-vindo(a), {name}!')

    # Caminho para o arquivo txt específico do usuário
    user_file_path = f'{username}_notes.txt'


    # Função para inicializar o arquivo se não existir
    def initialize_file(file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("Notas de Livros\n")


    # Função para ler o conteúdo atual do arquivo
    def read_file_content(file_path):
        with open(file_path, 'r') as file:
            content = file.readlines()  # Lê todas as linhas do arquivo em uma lista
        return content


    # Função para adicionar conteúdo ao arquivo (adiciona novas linhas sem apagar o existente)
    def append_to_file(file_path, new_content):
        with open(file_path, 'a') as file:
            file.write(new_content + '\n')


    # Função para remover uma linha específica do arquivo
    def remove_line(file_path, line_to_remove):
        lines = read_file_content(file_path)
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip() != line_to_remove.strip():
                    file.write(line)


    # Inicializa o arquivo se ele não existir
    initialize_file(user_file_path)

    # Lê o conteúdo atual do arquivo para exibir no Streamlit
    file_content = read_file_content(user_file_path)
    st.write('Notas atuais:')
    for i, line in enumerate(file_content):
        if line.strip() and i > 0:  # Ignora a linha inicial e linhas vazias
            col1, col2 = st.columns([9, 1])
            with col1:
                st.text(line.strip())
            with col2:
                if st.button('Excluir', key=f'delete_{i}'):
                    remove_line(user_file_path, line)
                    st.experimental_rerun()  # Recarrega a página para atualizar a lista de notas

    # Entrada para adicionar nota de livro
    st.header('Adicionar Nota de Livro')

    # Campos para inserir nome do livro, autor e nota
    book_name = st.text_input('Nome do Livro')
    author = st.text_input('Autor')
    note = st.text_area('Nota (máximo 200 caracteres)', max_chars=200)

    # Botão para adicionar a nota de livro
    if st.button('Adicionar Nota'):
        if book_name.strip() and author.strip() and note.strip():  # Verifica se há texto a ser adicionado
            new_entry = f"{book_name} - {author}\n{note}\n"
            append_to_file(user_file_path, new_entry)
            st.success('Nota adicionada com sucesso!')
            st.experimental_rerun()  # Recarrega a página para atualizar a lista de notas
        else:
            st.warning('Por favor, preencha todos os campos para adicionar a nota.')

elif authentication_status == False:
    st.error('Usuário ou senha incorretos')
elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')
