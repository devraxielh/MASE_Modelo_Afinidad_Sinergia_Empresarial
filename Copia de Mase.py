import pandas as pd
from itertools import combinations
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    return df

# Calcular la coincidencia entre dos empresas
def calcular_match_completo(emp1, emp2, tipo="afinidad"):
    objetivos_cols = ['crear_nuevos_modelos_negocio', 'generar_eficiencias', 
                      'fidelizar_mercado_actual', 'diversificar_mercado']
    obj1 = emp1[objetivos_cols].values
    obj2 = emp2[objetivos_cols].values

    if tipo == "afinidad":
        match_score = sum(obj1 == obj2)
    elif tipo == "sinergia":
        match_score = sum((obj1 == 1) & (obj2 == 0)) + sum((obj1 == 0) & (obj2 == 1))
    else:
        match_score = 0
    # Factor de coincidencia por empleados
    empleados_diff = abs(emp1["total_empleados"] - emp2["total_empleados"])
    empleados_score = 1 / (1 + empleados_diff)  # Normalización inversa
    # Coincidencia de ciudad
    ciudad_score = 1 if emp1["ciudad"] == emp2["ciudad"] else 0
    # Score total ponderado
    match_total = match_score + empleados_score + ciudad_score
    return match_total

def generar_matching(df):
    df["total_empleados"] = df["num_empleados_directos"] + df["num_empleados_indirectos"]
    matches = []
    
    for (i, row1), (j, row2) in combinations(df.iterrows(), 2):
        match_afinidad = calcular_match_completo(row1, row2, tipo="afinidad")
        match_sinergia = calcular_match_completo(row1, row2, tipo="sinergia")
        
        matches.append({
            "Empresa 1": row1["razonsocial"],
            "Empresa 2": row2["razonsocial"],
            "Ciudad 1": row1["ciudad"],
            "Ciudad 2": row2["ciudad"],
            "Match Afinidad": match_afinidad,
            "Match Sinergia": match_sinergia,
            "Total Empleados 1": row1["total_empleados"],
            "Total Empleados 2": row2["total_empleados"],
            "Diferencia Empleados": abs(row1["total_empleados"] - row2["total_empleados"])
        })
    
    df_matches = pd.DataFrame(matches)
    df_matches = df_matches.sort_values(by=["Match Afinidad", "Match Sinergia"], ascending=False)
    return df_matches

file_path = "data.xlsx"
df = load_data(file_path)
df_matches = generar_matching(df)
df_matches.to_excel('Matches.xlsx')