import pandas as pd
df = pd.read_excel("CIIU.xlsx", sheet_name=0)
codigos_ciiu = df["CIIU"].astype(str).unique().tolist()
codigos_ciiu_mod = []
for c in codigos_ciiu:
    if len(c) == 3:
        c = c.zfill(4)
    codigos_ciiu_mod.append(c)
def distancia_ciiu(cod1, cod2):
    max_digits = 4
    max_compare = min(max_digits, len(cod1), len(cod2))
    match_count = 0
    for i in range(max_compare):
        if cod1[i] == cod2[i]:
            match_count += 1
        else:
            break
    dist = max_digits - match_count
    return dist

def compatibilidad_ciiu(cod1, cod2):
    dist = distancia_ciiu(cod1, cod2)
    max_dist = 4
    return 1 - (dist / max_dist)

codigos_final = codigos_ciiu_mod
n = len(codigos_final)
matriz = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        c1 = codigos_final[i]
        c2 = codigos_final[j]
        matriz[i][j] = compatibilidad_ciiu(c1, c2)

matriz_df = pd.DataFrame(matriz,
                        index=codigos_final,
                        columns=codigos_final)

matriz_df.to_excel("matriz.xlsx", index=True)
print("Matriz de Compatibilidad CIIU generada.")
