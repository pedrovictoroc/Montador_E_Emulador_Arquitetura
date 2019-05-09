import os

def get_file_content(file_path):
	"""Ler um arquivo binário e retorna o conteúdo em bytes

	Keyword arguments:
	file_path -- Caminho do arquivo a ser lido
	"""
	chunksize = os.path.getsize(file_path)
	with open(file_path, mode="rb") as f:
		byte = f.read(chunksize)

	if byte:
		return { 'bytes': byte, 'size': chunksize }

	return None
