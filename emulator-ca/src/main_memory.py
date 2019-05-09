from reader import get_file_content
from binary import convert_to_bin, convert_to_decimal

"""Uma classe representando a memória principal"""
class Main_Memory:
	def __init__(self, size):
		"""Inicializa um objeto Main_Memory. Cria uma memória principal
		e ocupa todas as posições da memória com 0
		
		Keyword arguments:
		size -- Tamanho da memória principal
		"""
		self._memory = [b"\x00"]*size

	"""Retorna o tamanho da memoria
	"""
	def get_memory_size(self): return len(self._memory)

	# Criado para teste.
	def get_memory(self): return self._memory

	# Criado para teste.		
	def get_memory_int(self):
		mem = self._memory
		return list(
			map(lambda elem: int.from_bytes(elem, "little"), mem)
		)
	
	# Criado para teste.	
	def get_memory_str(self):
		int_list = self.get_memory_int()
		return list(
			map(lambda elem: convert_to_bin(elem)["bin_str"], int_list)
		)

	# Criado para teste.	
	def get_memory_arr(self):
		int_list = self.get_memory_int()
		return list(
			map(lambda elem: convert_to_bin(elem)["bin_arr"], int_list)
		)

	def load_memory(self, file_path):
		"""Ler uma informação e escrever na memória partindo da posição 1.
		Retorna True se a operação foi bem sucedida, False caso contrario.
		
		Keyword arguments:
		file_path -- Caminho do arquivo a ser escrito na memória
		"""
		file_content = get_file_content(file_path)

		#Verifica se o conteudo e grande demais para a memoria
		if (file_content["size"] > self.get_memory_size()):
			return False

		#Escreve os 20 bytes de inicializacao a partir da posicao 0
		self.write_memory(file_content["bytes"][4:24], 0)
		#Escreve o restante do programa a partir da posicao 1025
		return self.write_memory(file_content["bytes"][24:], 1025)

	def read_memory(self, position, lines=1):
		"""Ler uma posição ou mais posição de memória.
		Retorna um dicionário com a informação lida em bytes, string e array.

		Keyword arguments:
		position -- Posição inicial de memória a ser lida
		lines -- Número de posições a ser lida a partir de position
		"""
		#Verifica se esta tentando ler mais do que existe na memoria
		if (position >= self.get_memory_size()):
			return None

		#Indicara a posicao a ser lida
		pos = None
		#Converte a posicao para inteiro
		if (type(position) == str):
			pos = convert_to_decimal(position)
		elif (type(position) == bytes):
			pos = int.from_bytes(position, byteorder="little")
		else:
			pos = position

		#Resultado da leitura em bytes
		result_byte = b""

		#Adiciona byte a byte os resultados
		for i in range(0, lines):
			result_byte += self._memory[pos+i]

		#Prepara resultado para ser mostrado em string
		result_str = ''
		for i in range(0, lines):
			int_value = int.from_bytes(self._memory[pos+i], "little")
			result_str += convert_to_bin(int_value)["bin_str"]

		#Prepara resultado para ser mostrado em listas
		result_arr = []
		for i in range(0, lines):
			int_value = int.from_bytes(self._memory[pos+i], "little")
			result_arr += convert_to_bin(int_value)["bin_arr"]

		#Retorna o dicionario da leitura de 3 formas diferentes
		return {
			"byte": result_byte,
			"str": result_str,
			"arr": result_arr
		}

	def write_memory(self, value, position):
		"""Escreve na memória um valor na posição position.
		Retorna True se a operação foi bem sucedida, False caso contrário.
		
		Keyword arguments:
		value -- Valor a ser escrito na memória
		position -- Posição de memória que value será escrito
		"""
		#Indicara a posicao a ser lida
		pos = None
		#Converte a posicao para inteiro
		if(type(position) == str):
			pos = convert_to_decimal(position)
		elif(type(position) == bytes):
			pos = int.from_bytes(position, "little")
		else:
			pos = position

		#Valor a ser escrito na memoria
		result = None
		#Coverte o resultado para bytes
		if (type(value) == str):
			result = convert_to_decimal(value)
		elif (type(value) == bytes):
			result = value
		else:
			result = value.to_bytes(value.bit_length(), "little")
		
		result_size = len(result)

		#Verifica se estamos tentando escrever mais do que a memoria suporta
		if (pos+result_size >= self.get_memory_size()):
			return False

		#Escrete os bytes na memoria
		for i in range(0, result_size):
			self._memory[pos+i] = result[i].to_bytes(1, "little")

		return True

	def fetch(self, position):
		"""Busca um valor na posição position.
		Retorna o valor procurado.
		
		Keyword arguments:
		position -- Posição a ser procurada
		"""
		#Faz uma leitura de apenas 1 byte na posicao espeficicada
		return self.read_memory(position)

