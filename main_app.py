import streamlit as st
import os

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

    # Cria a barra de navegação
    with st.sidebar:
        selected = st.selectbox("Menu", ["Adicionar Notas", "Editar Notas"], index=0)

    if selected == "Adicionar Notas":
        st.title('Notas de Livros')

        # Lê o conteúdo atual do arquivo para exibir no Streamlit
        file_content = read_file_content(file_path)
        st.write('Notas atuais:')
        for i, line in enumerate(file_content):
            if line.strip() and i > 0:  # Ignora a linha inicial e linhas vazias
                col1, col2 = st.columns([9, 1])
                with col1:
                    st.text(line.strip())

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
                append_to_file(file_path, new_entry)
                st.success('Nota adicionada com sucesso!')
            else:
                st.warning('Por favor, preencha todos os campos para adicionar a nota.')

    elif selected == "Editar Notas":
        st.title('Editar Notas')

        # Lê o conteúdo atual do arquivo para exibir no Streamlit
        file_content = read_file_content(file_path)
        st.write('Notas atuais:')
        for i, line in enumerate(file_content):
            if line.strip() and i > 0:  # Ignora a linha inicial e linhas vazias
                col1, col2 = st.columns([9, 1])
                with col1:
                    st.text(line.strip())
                with col2:
                    if st.button('Excluir', key=f'delete_{i}'):
                        remove_line(file_path, line)
                        st.success('Nota excluída com sucesso!')

    else:
        st.warning('Selecione uma opção no menu.')

# Executa a função principal
if __name__ == '__main__':
    main()
