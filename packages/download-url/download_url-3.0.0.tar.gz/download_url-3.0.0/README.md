**Download_url** é uma simples função que faz o download de arquivos através de URLs informadas.

## Funções

"""
	A função receberá uma url, referente ao arquivo pdf que se quer fazer o download, o
	caminho (diretorio) onde se quer salvar o arquivo e o nome do arquivo que se deseja
	nomear.

	Entradas
		download_url   : (string)                Url do arquivo alvo
		path_download  : (string)                Caminho (diretório) onde se armazenará o arquivo
		file_name      : (string)                Nome do arquivo 

	Saídas

		(True, filename) : tupla (bool,string)   Retorno sucesso. "Filename = path_download + file_name"
		(-1, traceback)  : tupla (int,string)    Retorno Erro. Falha ao formar o path completo do arquivo
		(-2, traceback)  : tupla (int,string)    Retorno Erro. Falha ao fazer o download do arquivo alvo

"""
