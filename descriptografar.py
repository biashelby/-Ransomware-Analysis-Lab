from cryptography.fernet import Fernet
import os

# 1. Carregar a chave (A mesma que foi usada para criptografar)
def carregar_chave():
    # Sem esse arquivo 'chave.key', os dados não podem ser recuperados
    return open("chave.key", "rb").read()

# 2. Descriptografar um único arquivo
def descriptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    
    # Lê os dados encriptados
    with open(arquivo, "rb") as file:
        dados_encriptados = file.read()
    
    # Usa a chave para traduzir os dados
    dados_restaurados = f.decrypt(dados_encriptados)
    
    # Sobrescreve o arquivo com o conteúdo original
    with open(arquivo, "wb") as file:
        file.write(dados_restaurados)

# 3. Encontrar os arquivos que foram afetados
def encontrar_arquivos(diretorio):
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            # Ignora os scripts e a chave para não dar erro
            if nome != "ataque.py" and nome != "descriptografar.py" and not nome.endswith(".key"):
                lista.append(caminho)
    return lista

# 4. Execução Principal
def main():
    chave = carregar_chave()
    # Busca os arquivos na pasta de teste
    arquivos = encontrar_arquivos("test_files")
    
    for arquivo in arquivos:
        descriptografar_arquivo(arquivo, chave)
    
    print("Arquivos restaurados com sucesso!")

if __name__ == "__main__":
    main()