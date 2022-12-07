#CONJUNTOS

set I:={1..20};	#ORIGEN
set J:={1..30};	#DESTINO

#PARAM
param alpha{I};	#OFERTA

param beta{J};	#DEMANDA

param a{I}{J};	#COSTO;

#VAR
var Uij{I}{J};	#CUANTO DEBO ENVIAR DE DESDE EL LUGAR ALPHA A LUGAR BETA


# FUNCION OBJETIVO
minimize Function_value: sum{i in I, j in J}(Uji[i,j]*a[i,j]);

#RESTRICCIONES

subject to R1{j in J}:
	sum{i in I}(Uij[i,j])=beta[j];
	
subject to R2{i in I}:
	alpha[i]=sum{j in J}(Uij[i,j]);
	

