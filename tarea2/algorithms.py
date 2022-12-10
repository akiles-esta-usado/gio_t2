import numpy as np
from numpy.typing import NDArray
from pprint import pprint

def simplex_normalization(A: NDArray, entra: int, sale: int):
  A = A.copy()
  
  view_columna = A[:, entra]
  view_fila    = A[sale, :]


  view_fila /= A[sale, entra]
  
  AD = np.ones(shape=A.shape)

  escala = -view_columna
  for idx, value in enumerate(escala):
    AD[idx, :] = value*view_fila

  AD[sale, :] = 0 # Evita los cambios en fila donde está A[sale, entra]

  A = A + AD
  return A


def north_west_heuristic(oferta_i: NDArray, demanda_j: NDArray, costos_ij: NDArray):
  if oferta_i.sum() != demanda_j.sum():
    raise ValueError("Oferta != Demanda")
  
  oferta_i = oferta_i.copy()
  demanda_j = demanda_j.copy()

  factores_ij = np.zeros(shape=costos_ij.shape)

  i = 0
  j = 0

  while True:

    oferta_actual = oferta_i[i,0]
    demanda_actual = demanda_j[j,0]

    # print(f"{   oferta_actual = }")
    # print(f"{   demanda_actual = }")

    if oferta_actual == demanda_actual:
      # print("   - iguales")
      factores_ij[i,j] = oferta_actual
      
      oferta_i[i,0] -= oferta_actual
      demanda_j[j,0] -= oferta_actual

      di = 1
      dj = 1
      
    elif oferta_actual >= demanda_actual:
      # print("   - demanda_actual es menor")
      factores_ij[i,j]=demanda_actual

      oferta_i[i,0]  -= demanda_actual
      demanda_j[j,0] -= demanda_actual

      di = 0
      dj = 1


    elif oferta_actual <= demanda_actual:
      # print("   - oferta_actual es menor")
      factores_ij[i,j]=oferta_actual

      oferta_i[i,0]  -= oferta_actual
      demanda_j[j,0] -= oferta_actual

      di = 1
      dj = 0

    if oferta_i[i,0] == 0 and demanda_j[j,0] == 0:
      # print("Se llega al equilibrio")
      return factores_ij
    
    # print(oferta_i)
    # print(demanda_j)
    i += di
    j += dj

    # print()





def es_factible(X_B):
  return (X_B >= 0).all()

def es_optimo(cr):

  if (cr >= 0).all():
    print("Tenemos un óptimo")

    if (cr == 0).any():
      print("Son múltiples óptimos")
    else:
      print("Es único")

    return True

  return False

def direccion_costo_reducido(X: NDArray, A: NDArray, B:NDArray, NB: NDArray, c: NDArray, NB_i: int) -> NDArray:
  d = np.zeros(shape=X.shape)
  d_B = - np.dot(
    np.linalg.inv(A[:,B]),
    A[:, NB_i]
  )

  np.put(d, NB_i, 1)
  np.put(d, B, d_B)


  cr = c[NB_i] + np.dot(c[B].T, d[B])

  # i, d, cr
  return NB_i, d, cr.flatten()

def costos_reducidos(A: NDArray, c: NDArray, B: NDArray, NB: NDArray, DEBUG: bool=False) -> NDArray:
  
  C_AB_ANB = np.linalg.multi_dot([
    c[B].T,
    np.linalg.inv(A[:,B]),
    A[:, NB]]
  )

  X_cr = c[NB].ravel() - C_AB_ANB.ravel()

  if DEBUG:

    print("\nCostos reducidos:")

    print("  c[NB] es:")
    pprint(c[NB])

    print("  c[B] es:")
    pprint(c[B])

    print("  A[:, B] es:")
    pprint(A[:, B])

    print("  A[:, B]^-1 es:")
    pprint(np.linalg.inv(A[:, B]))

    print("  A[:, NB] es:")
    pprint(A[:, NB])

    print("  C_AB_ANB es:")
    pprint(C_AB_ANB)

    print("  X_cr es:")
    pprint(X_cr)

  return X_cr


def lista_direccion_costos_reducidos(X: NDArray, A: NDArray, c: NDArray, B:NDArray, NB: NDArray) -> NDArray:
  d_cr_list = list()

  for j in NB:
    d = np.zeros(shape=X.shape)
    d_B = - np.dot(
      np.linalg.inv(A[:,B]),
      A[:, j]
    )

    np.put(d, j, 1)
    np.put(d, B, d_B)


    cr = c[j] + np.dot(c[B].T, d[B])

    d_cr_list.append((j, d, cr[0][0]))

  return d_cr_list


#################
def simplex(A, b, c, B, NB, DEBUG=False):
  X = np.zeros(shape=c.shape)

  for _ in range(1000):
    if DEBUG:
      print("A:")
      pprint(A)

      print("b:")
      pprint(b)

      print("c:")
      pprint(c)

      print("B:")
      pprint(B)

      print("A[B]:")
      pprint(A[:,B])

      print("NB:")
      pprint(NB)

      print("A[NB]:")
      pprint(A[:,NB])


    X[B] = np.dot(np.linalg.inv(A[:,B]), b)
    X[NB] = 0

    if DEBUG:
      print("X:")
      pprint(X)

      print("X[B]:")
      pprint(X[B])

      print("X[NB]:")
      pprint(X[NB])

    print("\nX es solución:")
    if (X >= 0).all():
      print("- básica factible ")
    else:
      print("- no es solución básica factible. Termino de Simplex")
      return np.zeros(shape=X.shape)

    if (X[B] == 0).any():
      print("- degenerada")
      pprint(lista_direccion_costos_reducidos(X, A, c, B, NB))
      return X


    X_cr = costos_reducidos(A, c, B, NB, DEBUG)


    if (X_cr >= 0).all():
      print(f"- óptima de valor {X * c}")

      if (X_cr == 0).any():
        print("- Hay múltiples óptimos")
      else:
        print("- Es óptimo único")

      return X

    else:
      print("- no es óptima")


    # DETERMINAR DIRECCIONES Y COSTOS REDUCIDOS
    ###########################################

    # Lo más sensato es empezar con una solución básica factible
    # Luego derivar la base, no-base y seguir.
    d_cr_list = lista_direccion_costos_reducidos(X, A, c, B, NB)

    if DEBUG:
      print("\nLista de direcciones y costos reducidos: ")
      pprint(d_cr_list)


    # ENCONTRAR DIRECCIÓN Y PASO
    ############################

    if DEBUG:
      print("\nCosto básico solución básica X_B: ")
      pprint(c[B])

    # Determinar dirección con menor costo reducido
    # (NB_i, d, cr)
    d_cr_min = min(d_cr_list, key=lambda x: x[2])

    if DEBUG:
      print("\nDirección de menor costo reducido: ")
      pprint(d_cr_min)

    # Obtener componentes de la dirección de menor costo reducido que:
    # - Pertenezcan a la base.
    # - Sean menores a cero.

    B_menores_a_cero = [B[i] for i, d_i in enumerate( d_cr_min[1][B] ) if d_i < 0]

    if DEBUG:
      print(f"{B_menores_a_cero = }")

    if len(B_menores_a_cero) == 0:
      print("El salto se hace infinito")
      print("El costo óptimo está indeterminado y se termina el algoritmo")
      break

    # Obtener la lista de coeficientes de desplazamientos posibles
    phi_list = [(- X[i] / d_cr_min[1][i], i) for i in B_menores_a_cero]

    # Quedarse con el menor, y determinar su índice (El que sale)
    phi, B_sale = min(phi_list)

    if DEBUG:
      print(f"{phi_list = }")
      print(f"{phi = }")


    # ACTUALIZAR BASE Y NO_BASE
    ########################################

    NB_entra = d_cr_min[0]
    B_sale_row =   np.where(B == B_sale)[0][0]
    NB_entra_row = np.where(NB == NB_entra)[0][0]

    if DEBUG:
      print()
      print(f"Entra a la base: {NB_entra}")
      print(f"Sale de la base: {B_sale}")

    B.put(B_sale_row, NB_entra)
    NB.put(NB_entra_row, B_sale)

    if DEBUG:
      print()
      print("B actualizado:")
      pprint(B)
      print("NB actualizado:")
      pprint(NB)

      print()
      print()
      print()
      print()
  
  print("Entonces esto no terminó bien :(")
  return X