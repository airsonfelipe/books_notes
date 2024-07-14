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

# Função para inicializar o arquivo se não existir
def initialize_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("Notas de Livros\n")

# Inicializa o arquivo se ele não existir
initialize_file(file_path)

# Exemplo de uso no Streamlit
st.title('Notas de Livros')

# Lê o conteúdo atual do arquivo para exibir no Streamlit
file_content = read_file_content(file_path)
st.write('Notas atuais:')
st.text(file_content)

# Entrada para adicionar nota de livro
st.header('Adicionar Nota de Livro')
book_note = st.text_area('Digite a nota de livro que deseja adicionar:', '')

# Botão para adicionar a nota de livro
if st.button('Adicionar Nota'):
    if book_note.strip():  # Verifica se há texto a ser adicionado
        append_to_file(file_path, book_note)
        st.success('Nota adicionada com sucesso!')
        # Força o Streamlit a recarregar o conteúdo do arquivo após adicionar
        file_content = read_file_content(file_path)
        st.write('Notas atualizadas:')
        st.text(file_content)
    else:
        st.warning('Por favor, digite uma nota para adicionar.')
