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

# Função para ler o conteúdo atual do arquivo
def read_file_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Exemplo de uso no Streamlit
st.title('Manipulação de Arquivos TXT')

# Escreve ou sobrescreve o arquivo inicialmente
initial_content = "Exemplo de conteúdo inicial.\n"
write_to_file(file_path, initial_content)

# Lê o conteúdo atual do arquivo para exibir no Streamlit
file_content = read_file_content(file_path)
st.write('Conteúdo atual do arquivo:')
st.text(file_content)

# Entrada para adicionar conteúdo ao arquivo
st.header('Adicionar ao Arquivo')
new_content = st.text_area('Digite o texto que deseja adicionar:', '')

# Botão para adicionar o novo conteúdo
if st.button('Adicionar ao Arquivo'):
    if new_content.strip():  # Verifica se há texto a ser adicionado
        append_to_file(file_path, new_content)
        st.success('Texto adicionado com sucesso!')
        # Força o Streamlit a recarregar o conteúdo do arquivo após adicionar
        file_content = read_file_content(file_path)
        st.write('Conteúdo atual do arquivo atualizado:')
        st.text(file_content)
    else:
        st.warning('Por favor, digite um texto para adicionar.')
