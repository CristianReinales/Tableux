#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label

def Inorder(f):
    # Imprime una formula como cadena dada una formula como arbol
    # Input: tree, que es una formula de logica proposicional
    # Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def string2Tree(A):
    letrasProposicionales=[chr(x) for x in range(97, 123)]
    Conectivos = ['O','Y','>','=']
    Pila = []
    for c in A:
        if c in letrasProposicionales:
            Pila.append(Tree(c,None,None))
        elif c=='-':
            FormulaAux = Tree(c,None,Pila[-1])
            del Pila[-1]
            Pila.append(FormulaAux)
        elif c in Conectivos:
            FormulaAux = Tree(c,Pila[-1],Pila[-2])
            del Pila[-1]
            del Pila[-1]
            Pila.append(FormulaAux)
        else:
            print(u"Hay un problema: el símbolo " + str(c)+ " no se reconoce")
    return Pila[-1]

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def complemento(l):
    if (l.label == '-'):
        return l.right
    else:
        return Tree('-',None,l)

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False
    for i in l:
        indices = [x for x in l if x != i]
        for j in indices:
            if (Inorder(i) == Inorder(complemento(j))):
                return True
        
    return False

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
    if (f.label == "-"):
        if(f.right.label in letrasProposicionales):
            return True
        elif(f.right.label == "-"):
            if (f.right.right.label in letrasProposicionales):
                return True
        else:
            return False
    if(f.label in letrasProposicionales):
        return True
    return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal

    for i in l:
       if (es_literal(i) == False):
            return i
        
    return None

def clasificacion(l):
    if (l.label == '-'):
        if (l.right.label == '-'):
            return "1alfa"
        elif (l.right.label == 'O'):
            return "3alfa"
        elif (l.right.label == '>'):
            return "4alfa"
        elif (l.right.label == 'Y'):
            return "1beta"
        
    if (l.label == 'Y'):
        return "2alfa"
    
    if (l.label == 'O'):
        return "2beta"
    
    if (l.label == '>'):
        return "3beta"
    return "error"

def clasifica_y_extiende(f, h):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol 
	# Output: no tiene output, pues modifica la variable global listaHojas
    global listaHojas
    tipo = clasificacion(f)
    if (tipo == "1alfa"):
        aux = [x for x in h if x!=f] + [f.right.right]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif (tipo == "2alfa"):
        aux = [x for x in h if x!=f] + [f.left, f.right]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif (tipo == "3alfa"):
        aux = [x for x in h if x!=f] + [Tree('-', None, f.right.right), Tree('-', None, f.right.left)]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif (tipo == "4alfa"):
        aux = [x for x in h if x!=f] + [f.right.left, Tree('-', None, f.right.right)]
        listaHojas.remove(h)
        listaHojas.append(aux)
    elif (tipo == "1beta"):
        aux1 = [x for x in h if x!=f] + [Tree('-', None, f.right.right)]
        aux2 = [x for x in h if x!=f] + [Tree('-', None, f.right.left)]
        listaHojas.remove(h)
        listaHojas.append(aux1)
        listaHojas.append(aux2)
    elif (tipo == "2beta"):
        aux1 = [x for x in h if x!=f] + [f.right.right]
        aux2 = [x for x in h if x!=f] + [f.right.left]
        listaHojas.remove(h)
        listaHojas.append(aux1)
        listaHojas.append(aux2)
    elif (tipo == "3beta"):
        aux1 = [x for x in h if x!=f] + [f.right.right]
        aux2 = [x for x in h if x!=f] + [Tree('-', None, f.right.left)]
        listaHojas.remove(h)
        listaHojas.append(aux1)
        listaHojas.append(aux2)
        

def Tableaux(f):
	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f

    global listaHojas
    global listaInterpsVerdaderas

    A = string2Tree(f)
    listaHojas = [[A]]
    
    i = 0
    while(no_literales(listaHojas[i]) != None):
        clasifica_y_extiende(no_literales(listaHojas[i]), listaHojas[i])
   
        
    for i in listaHojas:
        j = par_complementario(listaHojas[i])
        if (j == False):
            listaInterpsVerdaderas.append([listaHojas[i]])

    return listaInterpsVerdaderas




