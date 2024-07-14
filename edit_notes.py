import streamlit as st
import os

# Caminho para o arquivo txt
file_path = 'output.txt'

# Função para ler o conteúdo atual do arquivo
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()  # Lê todas as linhas do arquivo em uma lista
    return content

# Função para remover uma linha específica do arquivo
def remove_line(file_path, line_to_remove):
    lines = read_file_content(file_path)
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != line_to_remove.strip():
                file.write(line)

# Verifica se estamos na página de edição
query_params = st.experimental_get_query_params()
if query_params.get('page') == ['edit']:
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
                    st.experimental_rerun()  # Recarrega a página para atualizar a lista de notas

    # Botão para voltar à página principal
    if st.button('Voltar'):
        st.experimental_set_query_params()
        st.experimental_rerun()
else:
    st.warning('Acesse esta página através do menu principal.')
