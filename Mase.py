import pandas as pd
from itertools import combinations

def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    if "codigo_ciiu" in df.columns:
        df["codigo_ciiu"] = df["codigo_ciiu"].astype(str)
        df["codigo_ciiu"] = df["codigo_ciiu"].apply(
            lambda x: x.zfill(4) if len(x) == 3 else x
        )
    return df

def load_sector_matrix(file_path):
    matriz = pd.read_excel(file_path, index_col=0)
    matriz.index = matriz.index.astype(str)
    nuevo_index = []
    for idx in matriz.index:
        if len(idx) == 3:
            idx = idx.zfill(4)
        nuevo_index.append(idx)
    matriz.index = nuevo_index
    matriz_dict = matriz.to_dict()
    return matriz, matriz_dict

def calcular_match_mase(emp1, emp2, sector_matrix_dict):
    objetivos = [
        'crear_nuevos_modelos_negocio', 'generar_eficiencias',
        'fidelizar_mercado_actual', 'diversificar_mercado'
    ]
    intereses = [
        'incremento_ventas', 'llegar_nuevos_mercados', 'lanzamiento_nuevos_productos',
        'mejoramiento_productividad', 'incremento_capacidad_productiva',
        'desarrollo_nuevos_canales', 'implementacion_ti',
        'infraestructura_fisica', 'compra_maquinaria_equipos'
    ]
    estrategia_cols = objetivos + intereses
    s1 = emp1[estrategia_cols].values
    s2 = emp2[estrategia_cols].values
    match_afinidad = sum(s1 == s2)
    match_sinergia = sum((s1 == 1) & (s2 == 0)) + sum((s1 == 0) & (s2 == 1))
    e1 = emp1["num_empleados_directos"] + emp1["num_empleados_indirectos"]
    e2 = emp2["num_empleados_directos"] + emp2["num_empleados_indirectos"]
    diferencia_emp = abs(e1 - e2)
    match_empleados = 1 / (1 + diferencia_emp)
    match_ciudad = 1 if emp1["ciudad"] == emp2["ciudad"] else 0
    match_tamaño = 1 if emp1["tamaño"] == emp2["tamaño"] else 0
    codigo1 = str(emp1["codigo_ciiu"])
    codigo2 = str(emp2["codigo_ciiu"])
    if (codigo1 in sector_matrix_dict) and (codigo2 in sector_matrix_dict[codigo1]):
        match_sector = sector_matrix_dict[codigo1][codigo2]
    else:
        match_sector = 0
    match_total = (
        match_afinidad
        + match_sinergia
        + match_empleados
        + match_ciudad
        + match_tamaño
        + match_sector
    )
    if match_afinidad > 0:
        exp_afinidad = f"Coinciden en {match_afinidad} objetivos/intereses."
    else:
        exp_afinidad = "No comparten objetivos/intereses."
    if match_sinergia > 0:
        exp_sinergia = f"Tienen sinergia en {match_sinergia} objetivo(s)/interés(es)."
    else:
        exp_sinergia = "No presentan sinergia estratégica."
    if diferencia_emp == 0:
        exp_empleados = (
            f"Misma cantidad de empleados ({e1}). "
            f"Contribuye {match_empleados:.2f} al puntaje."
        )
    else:
        if match_empleados > 0.0:
            exp_empleados = (
                f"Diferencia de empleados: {diferencia_emp}, "
                f"contribuye {match_empleados:.2f} al puntaje."
            )
        else:
            exp_empleados = (
                f"Diferencia de empleados muy alta ({diferencia_emp}), "
                f"no aporta puntaje."
            )
    exp_ciudad = (
        "Coinciden en la misma ciudad."
        if match_ciudad == 1 else "No coinciden en la ciudad."
    )
    exp_tamaño = (
        "Mismo tamaño empresarial."
        if match_tamaño == 1 else "Diferente tamaño empresarial."
    )
    if match_sector > 0:
        exp_sector = f"Compatibilidad sectorial de {match_sector:.2f}."
    else:
        exp_sector = "Sin coincidencia sectorial."
    desc_ciiu_1 = ""
    if "descripcion_ciiu" in emp1:
        desc_ciiu_1 = str(emp1["descripcion_ciiu"])
    desc_ciiu_2 = ""
    if "descripcion_ciiu" in emp2:
        desc_ciiu_2 = str(emp2["descripcion_ciiu"])
    return {
        "NIT 1": emp1["nit"],
        "Razón Social 1": emp1["razonsocial"],
        "Empresa 1": emp1["nombrecomercial"],
        "CIIU 1": codigo1,
        "Descripción CIIU 1": desc_ciiu_1,
        "NIT 2": emp2["nit"],
        "Razón Social 2": emp2["razonsocial"],
        "Empresa 2": emp2["nombrecomercial"],
        "CIIU 2": codigo2,
        "Descripción CIIU 2": desc_ciiu_2,
        "Ciudad 1": emp1["ciudad"],
        "Ciudad 2": emp2["ciudad"],
        "Tamaño 1": emp1["tamaño"],
        "Tamaño 2": emp2["tamaño"],
        "Match Afinidad": match_afinidad,
        "Match Sinergia": match_sinergia,
        "Total Empleados 1": e1,
        "Total Empleados 2": e2,
        "Diferencia Empleados": diferencia_emp,
        "Match Ciudad": match_ciudad,
        "Match Tamaño": match_tamaño,
        "Match Sector": match_sector,
        "Puntaje Total": match_total,
        "Exp Afinidad": exp_afinidad,
        "Exp Sinergia": exp_sinergia,
        "Exp Empleados": exp_empleados,
        "Exp Ciudad": exp_ciudad,
        "Exp Tamaño": exp_tamaño,
        "Exp Sector": exp_sector
    }

def generar_matching_mase(df_empresas, sector_matrix_dict):
    matches = []
    for (i, emp1), (j, emp2) in combinations(df_empresas.iterrows(), 2):
        match_info = calcular_match_mase(emp1, emp2, sector_matrix_dict)
        matches.append(match_info)
    df_matches = pd.DataFrame(matches)
    df_matches.sort_values(by="Puntaje Total", ascending=False, inplace=True)
    return df_matches

if __name__ == "__main__":
    file_path = "data.xlsx"
    file_path_sector = "matriz.xlsx"
    df_empresas = load_data(file_path)
    matriz_sector, dict_sector = load_sector_matrix(file_path_sector)
    df_matches = generar_matching_mase(df_empresas, dict_sector)
    df_matches.to_excel("Emparejamientos.xlsx", index=False)
    print("Emparejamientos generados y guardados")
