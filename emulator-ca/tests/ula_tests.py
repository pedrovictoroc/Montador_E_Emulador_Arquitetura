# Função de teste da ULA

#Importando o arquivo de /src
import sys
sys.path.insert(0, '../src')
from ULA import ULA

minhaUla = ULA()
minhaUla.set_inputs()
minhaUla.set_instruction(60)

instructions = [24, 20, 26, 44, 60, 61, 57, 53, 63, 54, 59, 12, 28, 16, 49, 50]

for i in instructions:
    minhaUla.set_instruction(i)
    print(minhaUla.execute_instruction())