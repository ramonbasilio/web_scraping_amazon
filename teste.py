import re
texto = '145-160 de 1 resultados'
partes = texto.split('-')
print(partes)

numero1 = int(partes[0].strip())
numero2 = int(partes[1].split()[0].strip())
c = 1 + numero2 - numero1

print(c)



