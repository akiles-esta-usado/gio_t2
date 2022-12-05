#CONJUNTOS

set I:{1..20};	#ORIGEN
set J:{1..30};	#DESTINO

#PARAM
param alpha{I};	#OFERTA

param beta{J};	#DEMANDA

param a{I}{J};	#COSTO

# VAR
var x1;
var x2;

###############
# FUNCION OBJETIVO
###############
minimize Function_value: