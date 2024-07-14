import streamlit as st

# Caminho para o arquivo txt
file_path = 'data_base.txt'

# Função para ler o conteúdo do arquivo
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Função para editar o conteúdo do arquivo
def edit_text_file(file_path, new_content):
    with open(file_path, 'w') as file:
        file.write(new_content)

# Exemplo de uso no Streamlit
st.title('Conteúdo do Arquivo TXT')

# Lê o conteúdo atual do arquivo
file_content = read_text_file(file_path)

# Exibe o conteúdo atual no Streamlit
st.write('Conteúdo do arquivo:')
st.code(file_content, language='text')

# Entrada para editar o arquivo
st.header('Editar Arquivo')
new_content = st.text_area('Edite o conteúdo do arquivo abaixo:', file_content)

# Botão para salvar as alterações
if st.button('Salvar Alterações'):
    edit_text_file(file_path, new_content)
    st.success('Alterações salvas com sucesso!')

