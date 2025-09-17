
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

def zip_com_senha(caminho_zip): ## Deve fazer o teste do arquivo de senhas para encontrar a senha correta
    try:
        with zipfile.ZipFile(caminho_zip, 'r') as zipf:
            zipf.testzip() # Tenta sem senha
            
        return False # Não Precisa de Senha
    
    except RuntimeError:
        return True # Precisa de Senha
    
    
def teste_senha_zip(txt_path: str , pyzipper_module):

    if not txt_path or not os.path.exists(txt_path):
        print("Arquivo de senhas não encontrado") 
        return None

    pasta_destino = "pasta_destino"
    os.makedirs(pasta_destino, exist_ok=True)

    try: 
        with open(txt_path, 'r') as f:
            senhas = [linha.strip() for linha in f if linha.strip()]
            print(f"Total de senhas para teste: {len(senhas)}")

        with pyzipper_module.AES.ZipFile(caminho_zip, 'r') as zipf:
            arquivos = zipf.namelist()
            if not arquivos:
                print("Nenhum arquivo encontrado no ZIP.")
                return None

            for i, senha in enumerate(senhas, 1):
                try:
                    print(f"Testando senha {i}/{len(senhas)}: {senha}")
                    
                    print(f"Senha correta encontrada: {senha}")
                except RuntimeError:
                    continue  # Senha errada, tenta a próxima
                except Exception as e:
                    print(f"Erro ao testar senha {senha}: {e}")
                    continue
    except Exception as e:
        print(f"Erro ao processar o arquivo de senhas: {e}")
        return None

    print("A senha correta não está nesse arquivo.")
    return None
    
if __name__ == "__main__":
    caminho_selecionado = buscar_arquivo(caminho_zip)
    
    if zip_com_senha(caminho_zip):
        print("O arquivo ZIP está protegido por senha.")
        caminho_txt = filedialog.askopenfilename(
            title="Selecione o arquivo de senhas (.txt)",
            filetypes=[("Arquivo de texto", "*.txt")]
        )
        senha_encontrada = teste_senha_zip(caminho_txt)
       