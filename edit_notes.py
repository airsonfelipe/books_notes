import streamlit as st
import os
from main_app import file_path, read_file_content

# Função para remover uma linha específica do arquivo
def remove_line(file_path, line_to_remove):
    lines = read_file_content(file_path)
    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip() != line_to_remove.strip():
                file.write(line)


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