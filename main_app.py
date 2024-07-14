import streamlit as st

# Caminho para o arquivo txt
file_path = 'output.txt'

# Função para escrever no arquivo (cria um novo arquivo ou sobrescreve o existente)
def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Função para adicionar conteúdo ao arquivo (adiciona novas linhas sem apagar o existente)
def append_to_file(file_path, new_content):
    with open(file_path, 'a') as file:
        file.write(new_content + '\n')

# Exemplo de uso no Streamlit
st.title('Manipulação de Arquivos TXT')

# Escreve ou sobrescreve o arquivo inicialmente
initial_content = "Exemplo de conteúdo inicial.\n"
write_to_file(file_path, initial_content)

# Lê o conteúdo atual do arquivo para exibir no Streamlit
with open(file_path, 'r') as file:
    current_content = file.read()

st.write('Conteúdo atual do arquivo:')
st.text(current_content)

# Entrada para adicionar conteúdo ao arquivo
st.header('Adicionar ao Arquivo')
new_content = st.text_area('Digite o texto que deseja adicionar:', '')

# Botão para adicionar o novo conteúdo
if st.button('Adicionar ao Arquivo'):
    if new_content.strip():  # Verifica se há texto a ser adicionado
        append_to_file(file_path, new_content)
        st.success('Texto adicionado com sucesso!')
    else:
        st.warning('Por favor, digite um texto para adicionar.')
