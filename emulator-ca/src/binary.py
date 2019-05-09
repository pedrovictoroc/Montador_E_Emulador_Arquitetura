def convert_to_bin(int_value):
  """Retorna um Dictionary contendo uma propriedade cujo o valor é uma
  lista de 0's e 1's e a outra propriedade é uma string de 0's e 1's

  Keyword arguments:
  int_value -- Um número inteiro em base decimal
  """
  bin_arr = []
  leftover = 0
  result = int_value

  while(result >= 1):
    leftover = int(result % 2)
    bin_arr.append(leftover)
    result = int(result / 2)

  while(len(bin_arr) < 8):
    bin_arr.append(0)

  return {
      "bin_arr": bin_arr[::-1],
      "bin_str": "".join(map(str, bin_arr[::-1]))
  }


def convert_to_decimal(bin_value):
	"""Recebe uma string de 0s e 1s e converte o binário para inteiro.
	Retorna o inteiro correspondente ao valor binário em string

	Keyword arguments:
	bin_value -- Uma string de 0s e 1s
	"""
	result = 0
	i = len(bin_value) - 1

	for v in bin_value:
		result += int(v)*(2**i)
		i -= 1

	return result
