# Importar implementações do python
import sys
import time
import os

# Importar classes de módulos do projeto
from Reg import Reg
from ULA import ULA
from control_storage import Control_Storage
from instruction import Instruction
from main_memory import Main_Memory

# Importar funções de módulos do projeto
from binary import convert_to_decimal

"""Função responsável por chamar todas as outras funções e dar inicio ao programa"""
def main():
	# Recebe o nome do arquivo que deve ser carregado na memória principal
	file_path = sys.argv[1]

	# Objeto de Registradores
	registers = Reg()

	# Objeto da ULA
	ula = ULA()

	# Objeto de armazenamento de controle
	cs = Control_Storage()
	instruction = None

	# Objeto da Memória principal
	memory = Main_Memory(100000)
	instruction = None

	print("\t\t\t\tArquivo carregando na memória")

	# Carrega arquivo na memória principal
	if (memory.load_memory(file_path)):
		os.system('cls' if os.name == 'nt' else 'clear')
	else:
		print("Memória não pode ser carregada!")
		return

	while True:
		wait_for_clock()

		####################################### PARTE 1: Decodificar #####################################
		

		# Define a primeira instrução do microprograma a ser executada
		instruction = cs.get_readable_instruction()

		####################################### PARTE 2: Barramentos #####################################
		b = registers.get_register_for_bus_b(instruction["bus_b"])

		###################################### PRINT #####################################################
		print("-----------------------------------------------------------")
		cs.get_instruction().print_instruction()
		print("\nRegistrador B: "+registers.get_register_name_for_bus_b(instruction["bus_b"]))
		print("\nNext Address Antes: "+str(convert_to_decimal(instruction["next_address"])))
		print("\nREGISTRADORES ANTES:\n")
		registers.print_registers()
		####################################### PARTE 3: ULA #############################################

		#Atribui os barramentos A e B da ULA
		ula.set_inputs(registers.get_register_by_name("h"), b)

		InstULA = instruction["ula"]

		# Atribui e executa a instrucao da ULA
		ula.set_instruction(InstULA)

		print(ula.get_instruction_translation())

		ula.execute_instruction()

		####################################### PARTE 4: Registradores ####################################

		C = instruction["bus_c"]
		#Grava o resultado da ULA nos registradores especificados pela parte C da micro instrucao
		registers.set_register_by_inst(C, ula.get_result())

		print(registers.get_registers_names_for_bus_c(C))
		
		####################################### PARTE 5: Memoria ##########################################
		m = instruction["memory"]

		#Realiza o Write na posicao MAR com o valor MDR
		if (m[0] == "1"):
			m_address = registers.get_register_by_name("mar")
			m_data = registers.get_register_by_name("mdr")
			memory.write_memory(m_data, m_address*4)
	
		#Realiza o Read na posicao MAR e grava em MDR
		if (m[1] == "1"):
			m_address = registers.get_register_by_name("mar")
			m_data = memory.read_memory(m_address*4, 4)
			m_data = int.from_bytes(m_data["byte"], "little")
			registers.set_register_by_name("mdr", m_data)

		#Realiza o Fetch na posicao PC e grava na em MBR
		if (m[2] == "1"):
			m_address = registers.get_register_by_name("pc")
			m_data = memory.fetch(m_address)["str"]
			m_data = convert_to_decimal(m_data)
			registers.set_register_by_name("mbr", m_data)

		####################################### PARTE 6: Jumps ############################################
		NextAdress = convert_to_decimal(instruction["next_address"])

		J = instruction["jam"]

		#Realiza o JMPC realizando o OU bit a bit de MBR com NextAdress
		if(J[0] == '1'):
			NextAdress = NextAdress | registers.get_register_by_name("mbr")
		#JAMN e JAMZ abaixo, realizando o OU do nono bit do NextAdress (2^8 = 256) com o valor do bit que indica
		#se a ULA for zero(JAMZ) ou com a negacao desse bit(JAMN)
		if(J[1] == '1' and (not ula.is_zero()) and NextAdress < 256):
			NextAdress += 256
		if(J[2] == '1' and ula.is_zero() and NextAdress < 256):
			NextAdress += 256

		####################################### PARTE 7: NEXT ADDRESS #####################################
		# Vai para a próxima instrução
		cs.next(NextAdress)

		print("\nREGISTRADORES DEPOIS:\n")
		registers.print_registers()
		print("\nNext Address Depois: "+str(NextAdress)+"\n")
		print("-----------------------------------------------------------")

def wait_for_clock():
	""" Entrada: Nada
			Operacao: Pausa o programa ate que a tecla enter seja pressionada,
								utilizada para separar os ciclos do clock durante a execucao das instrucoes
			Saida: Nada """

	input("")

main()
