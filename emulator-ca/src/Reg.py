from binary import convert_to_decimal

class Reg:

	def __init__(self):
		"""Inicializa um objeto Reg que armazenará todos os registradores"""
		self.dict = {
			"h": 0,
			"opc": 0,
			"tos": 0,
			"cpp": 0,
			"lv": 0,
			"sp": 0,
			"pc": 0,
			"mdr": 0,
			"mar": 0,
			"mbr": 0
		}

	def get_register_by_name(self, register_name):
		"""Retorna o valor do registrador especificado pelo nome
		
		Keyword arguments:
		register_name -- o nome do registrador desejado(string)
		"""

		#Caso de escape, talvez nao seja necessario
		#if(register_name == "none"): return 0

		return self.dict[register_name]

	def set_register_by_name(self, register_name, value):
		"""Altera o valor do registrador especificado pelo nome
		
		Keyword arguments:
		register_name -- o nome do registrador desejado (string)
		value -- o valor a ser atribuido ao registrador (int)
		"""

		self.dict[register_name] = value


	def set_register_by_inst(self, instruction_string, value):
		"""Grava o valor recebido nos registradores, especificados atraves da 
		parte C da instrucao recebida
		
		Keyword arguments:
		instruction_string -- a string que representa a parte C da instrucao (string)
		value -- o valor a ser atribuido aos registradores (int)
		"""

		for i in range(0, len(instruction_string)):
		 if(instruction_string[i] == '1'):
				self.dict[list(self.dict.keys())[i]] = value
		
	def get_registers_names_for_bus_c(self, instruction_string):
		"""Mostra para um estudante de arquitetura de computadores quais registradores estão sendo
		gravadas pela parte C do comando 
		
		Keyword arguments:
		instruction_string -- a string que representa a parte C da instrucao (string)
		"""

		str_result = "\nRegistradores gravados pela ULA: "

		for i in range(0, len(instruction_string)):
		 if(instruction_string[i] == '1'):
			 	str_result += (list(self.dict.keys())[i]+"     ").upper()
		return str_result


	def get_register_for_bus_b(self, instruction_string):
		"""Retorna o valor que o barramento B recebera atraves da parte B 
		da instrucao em forma de string
		
		Keyword arguments:
		instruction_string -- a string que representa a parte B da instrucao (string)
		"""

		#Talvez seja necessario inverter a string
		#inv_reg = instruction_string[::-1]
		intRegister = convert_to_decimal(instruction_string)

		reg_names_for_b = ["mdr", "pc", "mbr", "mbr", "sp", "lv", "cpp", "tos", "opc"]

		reg_value = self.dict[reg_names_for_b[intRegister]]

		#Retorna o valor de MBR com sinal
		if(intRegister == 2 and reg_value > 256):
			reg_value = reg_value | (0b111111111111111111111111 << 8)

		return reg_value

	def get_register_name_for_bus_b(self, instruction_string):
		"""Retorna o nome do registrador acessado pelo barramento B atraves da parte B 
		da instrucao em forma de string
		
		Keyword arguments:
		instruction_string -- a string que representa a parte B da instrucao (string)
		"""

		intRegister = convert_to_decimal(instruction_string)

		reg_names_for_b = ["mdr", "pc", "signed mbr", "unsigned mbr", "sp", "lv", "cpp", "tos", "opc"]

		return reg_names_for_b[intRegister].upper()


	def print_registers(self):
		"""Imprime na tela os valores de todos os registradores seguidos de seus nomes
		"""
		k = list(self.dict.values())
		arr_print = ["  H : ", "OPC : ", "TOS : ", "CPP : ", " LV : ", " SP : ", " PC : ", "MDR : ", "MAR : ", "MBR : "]

		for i in range(0, len(arr_print)):
			print(arr_print[i]+str(k[i]))
