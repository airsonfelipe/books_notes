import streamlit as st

# Caminho para o arquivo txt
file_path = 'data_base.txt'

# Função para ler o conteúdo do arquivo
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Função para adicionar conteúdo ao arquivo
def add_text_file(file_path, new_content):
    with open(file_path, 'a') as file:
        file.write(new_content + '\n')

# Exemplo de uso no Streamlit
st.title('Conteúdo do Arquivo TXT')

# Lê o conteúdo atual do arquivo
file_content = read_text_file(file_path)

# Exibe o conteúdo atual no Streamlit
st.write('Conteúdo do arquivo:')
st.code(file_content, language='text')

# Entrada para adicionar conteúdo ao arquivo
st.header('Adicionar ao Arquivo')
new_content = st.text_area('Digite o texto que deseja adicionar:', '')

# Botão para adicionar o novo conteúdo
if st.button('Adicionar ao Arquivo'):
    if new_content.strip():  # Verifica se há texto a ser adicionado
        add_text_file(file_path, new_content)
        st.success('Texto adicionado com sucesso!')
    else:
        st.warning('Por favor, digite um texto para adicionar.')

