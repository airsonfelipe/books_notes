import streamlit as st

# Caminho para o arquivo txt
file_path = 'data_base.txt'

# Função para ler o conteúdo do arquivo
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Exemplo de uso no Streamlit
st.title('Conteúdo do Arquivo TXT')

# Lê o conteúdo do arquivo
file_content = read_text_file(file_path)

# Exibe o conteúdo no Streamlit
st.write('Conteúdo do arquivo:')
st.code(file_content, language='text')
