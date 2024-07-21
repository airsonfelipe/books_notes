import streamlit as st
import os
import json
import firebase_admin
from firebase_admin import credentials, auth
import streamlit_authenticator as stauth

# Inicializar Firebase
cred = credentials.Certificate("path/to/your/firebase_credentials.json")
firebase_admin.initialize_app(cred)

# Caminho para o arquivo txt
file_path = 'output.txt'


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


# Função principal do aplicativo
def main():
    initialize_file(file_path)

    st.title("Sistema de Notas de Livros")

    # Autenticação
    credentials = {
        "usernames": {
            "user1": {"name": "User One", "password": "password"},
            "user2": {"name": "User Two", "password": "password"}
        }
    }

    authenticator = stauth.Authenticate(credentials, "notas_de_livros", "abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        st.write(f"Bem-vindo, {name}!")
        with st.sidebar:
            selected = st.selectbox("Menu", ["Adicionar Notas", "Ver Notas", "Editar Notas", "Download"], index=0)

        if selected == "Adicionar Notas":
            st.header('Adicionar Nota de Livro')
            book_name = st.text_input('Nome do Livro')
            author = st.text_input('Autor')
            note = st.text_area('Nota (máximo 200 caracteres)', max_chars=200)
            if st.button('Adicionar Nota'):
                if book_name.strip() and author.strip() and note.strip():
                    current_notes = [line for line in read_file_content(file_path) if
                                     line.strip() and line.split(" - ")[0].isdigit()]
                    next_id = len(current_notes) + 1
                    new_entry = f"{next_id} - {book_name}\n{author}\n{note}\n"
                    append_to_file(file_path, new_entry)
                    st.success('Nota adicionada com sucesso!')
                else:
                    st.warning('Por favor, preencha todos os campos para adicionar a nota.')

        elif selected == "Ver Notas":
            st.write('Notas atuais:')
            file_content = read_file_content(file_path)
            for i, line in enumerate(file_content):
                if line.strip() and i > 0:
                    st.text(line.strip())

        elif selected == "Editar Notas":
            st.write('Notas atuais:')
            file_content = read_file_content(file_path)
            for i, line in enumerate(file_content):
                if line.strip() and i > 0:
                    col1, col2 = st.columns([9, 1])
                    with col1:
                        st.text(line.strip())
                    with col2:
                        if st.button('Excluir', key=f'delete_{i}'):
                            remove_line(file_path, line)
                            st.success('Nota excluída com sucesso!')

        elif selected == "Download":
            st.write('Download das Notas')
            file_content = read_file_content(file_path)
            file_content_str = ''.join(file_content)
            st.download_button(label='Baixar Notas', data=file_content_str, file_name='output.txt', mime='text/plain')

        else:
            st.warning('Selecione uma opção no menu.')

    elif authentication_status == False:
        st.error('Usuário ou senha incorretos')
    elif authentication_status == None:
        st.warning('Por favor, insira seu usuário e senha')


if __name__ == '__main__':
    main()
