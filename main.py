import zipfile
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()

# Para quando iniciar a interface
print("Selecione o arquivo ZIP")
caminho_zip = filedialog.askopenfilename(
    title="Selecione um arquivo ZIP",
    filetypes=[("Arquivo Zip", "*.zip")]
)


def buscar_arquivo(caminho_zip):
 
    if not caminho_zip:
        print("Nenhum arquivo selecionado.")
        return None
    
    
    print(f"Arquivo selecionado:" )
    try: 
        with zipfile.ZipFile(caminho_zip, 'r') as zipf:
            print("Conteúdos do arquivo ZIP:")
            for arquivo in zipf.namelist():
                print(f" - {arquivo}")
    except zipfile.BadZipFile:
        print("Erro: O arquivo não é um ZIP válido.")
    except RuntimeError:
        print("Erro: O arquivo ZIP está protegido por senha.")
    

# def listar_conteudo_zip(): ## Lista o conteudo do arquivo zip antes de extrair
#     if caminho_zip:
#         print(f"Arquivo selecionado: {caminho_zip}")
#         try:
#             # Abre o arquivo ZIP e lista os conteúdos
#             with zipfile.ZipFile(caminho_zip, 'r') as zipf:
#                 print("Conteúdos do arquivo ZIP:")
#                 for arquivo in zipf.namelist():
#                     print(arquivo)
#         except zipfile.BadZipFile:
#             print("Erro: O arquivo não é um ZIP válido.")
#     else:
#         print("Nenhum arquivo selecionado.")





def zip_com_senha(caminho_zip): ## Deve fazer o teste do arquivo de senhas para encontrar a senha correta
    try:
        with zipfile.ZipFile(caminho_zip, 'r') as zipf:
            zipf.testzip() # Tenta sem senha
        return False # Não Precisa de Senha
    except RuntimeError:
        return True # Precisa de Senha
    


    
def teste_senha_zip(txt_path):
    ## Faz o teste de um arquivo txt para descobrir a senha
    if not txt_path or not os.path.exists(txt_path):
        print("Arquivo de senhas não encontrado") 
        return None
    
    try:
        with open(caminho_txt, 'r', encoding='utf-8') as f:

            senhas = [linha.strip() for linha in f if linha.strip()] 
            print(f"Total de senhas para teste: {len(senhas)}")

            pasta_destino = os.path.join(os.path.dirname(caminho_zip), "Extraido")
            os.makedirs(pasta_destino, exist_ok=True)
    
        with zipfile.ZipFile(caminho_zip, 'r') as zipf: 
            arquivos = zipf.namelist()

        if not arquivos:
                    print("Nenhum arquivo encontrado no ZIP.")
                    return None
        for i, senha in enumerate(senhas, 1):
            try:
                print(f"Testando senha {i}/{len(senhas)}: {senha}")
                zipf.setpassword(senha.encode('utf-8'))
                zipf.extract(arquivos[0], pasta_destino)  # Testa com o primeiro arquivo
                print(f"Senha correta encontrada: {senha}")
                zipf.extractall(pasta_destino)  # Extrai tudo se a senha for válida
                return senha
            except (RuntimeError, zipfile.BadZipFile):
                continue  # Tenta a próxima senha
            except Exception as e:
                print(f"Erro ao testar senha {senha}: {e}")
                break
    except Exception as e:
        print(f"A senha correta não está nesse arquivo: {e}")
        return None
    
    ## TESTE ANTERIOR DA PARTE DE SENHA
# def teste_senha_zip(txt_path):  # Recebe uma senha como parâmetro
#     if not os.path.exists(caminho_zip):
#         print("Arquivo de senhas não encontrado.")
#         return None
    
#     with open(txt_path, 'r') as file:
#         for linha in file:
#             senha = linha.strip()
#             if teste_senha_zip(senha):  # Testa a senha
#                 print("Senha correta encontrada:", senha)
#                 return senha
#     print("A senha correta não está nesse arquivo.")
#     return None


if __name__ == "__main__":
    caminho_selecionado = buscar_arquivo(caminho_zip)
    
    if zip_com_senha(caminho_zip):
        print("O arquivo ZIP está protegido por senha.")
        caminho_txt = filedialog.askopenfilename(
            title="Selecione o arquivo de senhas (.txt)",
            filetypes=[("Arquivo de texto", "*.txt")]
        )
        senha_encontrada = teste_senha_zip(caminho_txt)
        if senha_encontrada:
            print(f"Extração concluida! Usando a senha: {senha_encontrada}")
    else:
        print("O arquivo ZIP não está protegido por senha.")
        

    


# if caminho_zip:
#     print(f"Arquivo selecionado: {caminho_zip}")
#     try:
#         # Abre o arquivo ZIP e lista os conteúdos
#         with zipfile.ZipFile(caminho_zip, 'r') as zipf:
#             print("Conteúdos do arquivo ZIP:")
#             for arquivo in zipf.namelist():
#                 print(arquivo)
#     except zipfile.BadZipFile:
#         print("Erro: O arquivo não é um ZIP válido.")
#     else:
#     print("Nenhum arquivo selecionado.")


# # Extrair um ZIP com senha
# with zipfile.ZipFile('arquivo_protegido.zip', 'r') as zipf:
#     zipf.setpassword(b'senha123')
#     zipf.extractall('pasta_destino')