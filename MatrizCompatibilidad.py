import pandas as pd
df = pd.read_excel("CIIU.xlsx", sheet_name=0)
codigos_ciiu = df["CIIU"].astype(str).unique().tolist()
codigos_ciiu = [codigo.ljust(4, '0') for codigo in codigos_ciiu]

def distancia_ciiu(cod1, cod2):
    """
    Calcula la 'distancia' entre dos códigos CIIU de 4 dígitos
    en función de cuántos dígitos consecutivos coinciden desde el inicio.
    """
    max_digits = 4
    match_count = 0
    for i in range(max_digits):
        if cod1[i] == cod2[i]:
            match_count += 1
        else:
            break
    dist = max_digits - match_count
    return dist

def compatibilidad_ciiu(cod1, cod2):
    """
    Convierte la distancia CIIU a un valor de 0 a 1,
    donde 1 = misma clasificación (distancia 0) y 0 = distancia máxima (4).
    """
    dist = distancia_ciiu(cod1, cod2)
    max_dist = 4
    return 1 - (dist / max_dist)

n = len(codigos_ciiu)
matriz = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        c1 = codigos_ciiu[i]
        c2 = codigos_ciiu[j]
        matriz[i][j] = compatibilidad_ciiu(c1, c2)
matriz_df = pd.DataFrame(matriz,
                        index=codigos_ciiu,
                        columns=codigos_ciiu)
matriz_df.to_excel("matriz_compatibilidad_ciiu.xlsx", index=True)

print("Matriz de Compatibilidad CIIU Generada")
