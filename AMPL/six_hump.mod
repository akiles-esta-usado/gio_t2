#CONJUNTOS

set I:={1..20};	#ORIGEN
set J:={1..30};	#DESTINO

#PARAM
param alpha{I};	#OFERTA

param beta{J};	#DEMANDA

param a{I,J};	#COSTO

#VAR
var Uij{I,J};	#CUANTO DEBO ENVIAR DE DESDE EL LUGAR ALPHA A LUGAR BETA


# FUNCION OBJETIVO
minimize Function_value:
    sum{i in I, j in J} (Uij[i,j]*a[i,j]);

#RESTRICCIONES


## Naturaleza de Variable: Uij mayor o igual a 0.
subject to R1{i in I, j in J}:
    Uij[i,j] >= 0

subject to R2{j in J}:
	sum{i in I}(Uij[i,j])=beta[j];

subject to R3{i in I}:
	alpha[i]=sum{j in J}(Uij[i,j]);
