import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import config
import os

# Caminho para o arquivo txt
file_path = 'output.txt'

# Configuração do OAuth
oauth = OAuth2Session(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri=config.REDIRECT_URI,
    scope='openid profile email'
)

authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'

# Função para inicializar o arquivo se não existir
def initialize_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Notas de Livros\n")

# Função para ler o conteúdo atual do arquivo
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
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

def main():
    initialize_file(file_path)

    # Mostra a URL de autorização
    authorization_url, state = oauth.create_authorization_url(authorization_base_url)
    st.write(f'Por favor, faça login [aqui]({authorization_url})')

    # URL de callback
    query_params = st.query_params
    if 'code' in query_params:
        code = query_params['code']
        token = oauth.fetch_token(token_url, authorization_response=f'{config.REDIRECT_URI}?code={code}')
        user_info = oauth.get('https://www.googleapis.com/oauth2/v3/userinfo').json()
        st.write('Usuário autenticado:')
        st.json(user_info)

        # Cria a barra de navegação
        with st.sidebar:
            selected = st.selectbox("Menu", ["Adicionar Notas", "Ver Notas", "Editar Notas", "Download"], index=0)

        if selected == "Adicionar Notas":
            st.title('Notas de Livros')

            # Entrada para adicionar nota de livro
            st.header('Adicionar Nota de Livro')

            # Campos para inserir nome do livro, autor e nota
            book_name = st.text_input('Nome do Livro')
            author = st.text_input('Autor')
            note = st.text_area('Nota (máximo 200 caracteres)', max_chars=200)

            # Botão para adicionar a nota de livro
            if st.button('Adicionar Nota'):
                if book_name.strip() and author.strip() and note.strip():
                    # Determina o próximo ID com base nas entradas atuais no arquivo
                    current_notes = [line for line in read_file_content(file_path) if
                                     line.strip() and line.split(" - ")[0].isdigit()]
                    next_id = len(current_notes) + 1

                    new_entry = f"{next_id} - {book_name}\n{author}\n{note}\n"
                    append_to_file(file_path, new_entry)
                    st.success('Nota adicionada com sucesso!')
                else:
                    st.warning('Por favor, preencha todos os campos para adicionar a nota.')

        elif selected == "Ver Notas":
            st.title('Notas de Livros')

            # Lê o conteúdo atual do arquivo para exibir no Streamlit
            file_content = read_file_content(file_path)
            st.write('Notas atuais:')
            for i, line in enumerate(file_content):
                if line.strip() and i > 0:
                    st.text(line.strip())

        elif selected == "Editar Notas":
            st.title('Editar Notas')

            # Lê o conteúdo atual do arquivo para exibir no Streamlit
            file_content = read_file_content(file_path)
            st.write('Notas atuais:')
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
            st.title('Download das Notas')

            # Lê o conteúdo do arquivo
            file_content = read_file_content(file_path)

            # Junta as linhas em uma única string
            file_content_str = ''.join(file_content)

            # Botão de download
            st.download_button(label='Baixar Notas', data=file_content_str, file_name='output.txt', mime='text/plain')

        else:
            st.warning('Selecione uma opção no menu.')
    else:
        st.warning('Faça login para acessar as notas.')

if __name__ == '__main__':
    main()
