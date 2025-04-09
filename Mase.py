
import pandas as pd
from itertools import combinations

# Cargar los datos desde un archivo Excel
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    return df

# Calcular el match completo entre dos empresas según el modelo MASE
def calcular_match_mase(emp1, emp2):
    # Objetivos estratégicos
    objetivos = [
        'crear_nuevos_modelos_negocio', 'generar_eficiencias',
        'fidelizar_mercado_actual', 'diversificar_mercado'
    ]

    # Intereses estratégicos
    intereses = [
        'incremento_ventas', 'llegar_nuevos_mercados', 'lanzamiento_nuevos_productos',
        'mejoramiento_productividad', 'incremento_capacidad_productiva',
        'desarrollo_nuevos_canales', 'implementacion_ti',
        'infraestructura_fisica', 'compra_maquinaria_equipos'
    ]

    estrategia_cols = objetivos + intereses

    s1 = emp1[estrategia_cols].values
    s2 = emp2[estrategia_cols].values

    # 1. Afinidad estratégica
    match_afinidad = sum(s1 == s2)

    # 2. Sinergia estratégica
    match_sinergia = sum((s1 == 1) & (s2 == 0)) + sum((s1 == 0) & (s2 == 1))

    # 3. Empleados
    e1 = emp1["num_empleados_directos"] + emp1["num_empleados_indirectos"]
    e2 = emp2["num_empleados_directos"] + emp2["num_empleados_indirectos"]
    match_empleados = 1 / (1 + abs(e1 - e2))

    # 4. Ciudad
    match_ciudad = 1 if emp1["ciudad"] == emp2["ciudad"] else 0

    # 5. Tamaño
    match_tamaño = 1 if emp1["tamaño"] == emp2["tamaño"] else 0

    # 6. Puntaje total
    match_total = match_afinidad + match_sinergia + match_empleados + match_ciudad + match_tamaño

    return {
        "Empresa 1": emp1["nombrecomercial"],
        "Empresa 2": emp2["nombrecomercial"],
        "Ciudad 1": emp1["ciudad"],
        "Ciudad 2": emp2["ciudad"],
        "Tamaño 1": emp1["tamaño"],
        "Tamaño 2": emp2["tamaño"],
        "Match Afinidad": match_afinidad,
        "Match Sinergia": match_sinergia,
        "Total Empleados 1": e1,
        "Total Empleados 2": e2,
        "Diferencia Empleados": abs(e1 - e2),
        "Match Ciudad": match_ciudad,
        "Match Tamaño": match_tamaño,
        "Puntaje Total": match_total
    }

# Generar tabla con los mejores emparejamientos
def generar_matching_mase(df):
    matches = []
    for (i, emp1), (j, emp2) in combinations(df.iterrows(), 2):
        match = calcular_match_mase(emp1, emp2)
        matches.append(match)

    df_matches = pd.DataFrame(matches)
    df_matches = df_matches.sort_values(by="Puntaje Total", ascending=False)
    return df_matches

# Uso
if __name__ == "__main__":
    file_path = "datos_prueba_finales_corrected nuevas columnas intereses.xlsx"
    df = load_data(file_path)
    df_matches = generar_matching_mase(df)

    # Guardar resultados
    df_matches.to_excel("Emparejamientos_MASE.xlsx", index=False)
    print("Emparejamientos generados y guardados en 'Emparejamientos_MASE.xlsx'")