# MASE Modelo de Afinidad y Sinergia Empresarial


## Algoritmo de Matching entre Empresas en un Ecosistema

## Descripción
Este algoritmo identifica empresas compatibles dentro de un ecosistema empresarial basado en **objetivos estratégicos**, **número de empleados** y **ubicación geográfica**. Se generan emparejamientos según **afinidad** (similitud en objetivos) y **sinergia** (complementariedad de estrategias).

## Funcionalidades
1. **Cargar datos desde un archivo Excel** con información empresarial.
2. **Evaluar afinidad estratégica**: Coincidencia en objetivos empresariales.
3. **Evaluar sinergia estratégica**: Complementariedad entre empresas.
4. **Considerar el número de empleados** para identificar organizaciones con tamaños similares.
5. **Considerar la ciudad** para favorecer asociaciones geográficas cercanas.
6. **Generar una tabla de emparejamientos** ordenada según el mejor match.

## Requisitos
- Python 3.8+
- Pandas
- ace_tools (para visualización de resultados)

## Uso
### 1. **Carga de Datos**
El archivo debe contener las siguientes columnas:
- `nit`: Identificación de la empresa.
- `razonsocial`: Nombre de la empresa.
- `nombrecomercial`: Nombre comercial.
- `num_empleados_directos`: Número de empleados directos.
- `num_empleados_indirectos`: Número de empleados indirectos.
- `ciudad`: Ubicación de la empresa.
- `crear_nuevos_modelos_negocio`, `generar_eficiencias`, `fidelizar_mercado_actual`, `diversificar_mercado`: Columnas binarias (1 para sí, 0 para no) que representan los objetivos estratégicos.

### 2. **Ejecución del Algoritmo**
El código carga los datos y genera un DataFrame con los emparejamientos más relevantes. 

### 3. **Cálculo del Matching**

El algoritmo calcula dos tipos de emparejamientos:

#### **a) Matching por Afinidad**
Se define como el número de coincidencias exactas en los objetivos estratégicos entre dos empresas:
```math
M_{afinidad} = \sum_{i=1}^{n} (O_{1i} = O_{2i})
```
Donde:
- $O_{1i}$ y $O_{2i}$ son los valores de los objetivos estratégicos de las empresas 1 y 2.
- $n$ es el número total de objetivos estratégicos evaluados.
- Se suma 1 por cada objetivo coincidente.

#### **b) Matching por Sinergia**
Evalúa qué tan complementarias son dos empresas, es decir, cuando una tiene un objetivo que la otra no tiene:
```math
M_{sinergia} = \sum_{i=1}^{n} ((O_{1i} = 1) \land (O_{2i} = 0)) + \sum_{i=1}^{n} ((O_{1i} = 0) \land (O_{2i} = 1))
```
Este valor es alto si las empresas tienen estrategias complementarias.

#### **c) Diferencia de Empleados**
Se usa una normalización inversa para favorecer empresas con números similares de empleados:
```math
M_{empleados} = \frac{1}{1 + |E_1 - E_2|}
```
Donde:
- $E_1$ y $E_2$ son el número total de empleados de cada empresa.
- Se suma 1 en el denominador para evitar divisiones por cero.
- Empresas con tamaños similares obtienen valores más altos.

#### **d) Coincidencia de Ciudad**
Si ambas empresas están en la misma ciudad:
```math
M_{ciudad} = \begin{cases} 
1, & \text{si la ciudad es la misma} \\
0, & \text{si son ciudades diferentes} 
\end{cases}
```

#### **e) Puntaje Total de Matching**
El puntaje total se obtiene combinando todas las métricas anteriores:
```math
M_{total} = M_{afinidad} + M_{sinergia} + M_{empleados} + M_{ciudad}
```

### 4. **Interpretación de los Resultados**
La salida consiste en una tabla con:
- `Empresa 1` y `Empresa 2`: Empresas emparejadas.
- `Ciudad 1` y `Ciudad 2`: Ubicación de cada empresa.
- `Match Afinidad`: Puntuación de coincidencia estratégica.
- `Match Sinergia`: Puntuación de complementariedad estratégica.
- `Total Empleados 1` y `Total Empleados 2`: Cantidad total de empleados por empresa.
- `Diferencia Empleados`: Diferencia en número de empleados.

### 5. **Ejemplo de Resultados**

| Empresa 1 | Empresa 2 | Ciudad 1 | Ciudad 2 | Match Afinidad | Match Sinergia | Total Empleados 1 | Total Empleados 2 | Diferencia Empleados |
|-----------|-----------|----------|----------|---------------|---------------|------------------|------------------|------------------|
| Comercializadora de Frutas | Comercializadora de Electrodomésticos | Valledupar | Valledupar | 6 | 2 | 95 | 95 | 0 |
| Transportes del Litoral | Servicios de Jardinería | Riohacha | Riohacha | 6 | 2 | 80 | 80 | 0 |
| Producción de Lácteos | Manufacturas de Madera | Sincelejo | Sincelejo | 6 | 2 | 140 | 140 | 0 |

### **6. Aplicaciones y Uso**
- **Fomentar asociaciones estratégicas**: Empresas con alta afinidad pueden formar **alianzas** para potenciar sus estrategias.
- **Identificar oportunidades de crecimiento**: Empresas con alta sinergia pueden **complementarse** en el mercado.
- **Optimizar ecosistemas empresariales**: Facilita la integración de empresas en zonas geográficas estratégicas.