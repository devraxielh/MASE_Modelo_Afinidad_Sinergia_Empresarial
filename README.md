# MASE Modelo de Afinidad y Sinergia Empresarial
## Algoritmo de Matching entre Empresas en un Ecosistema
### Rodrigo García,PhD

## Descripción

Este algoritmo identifica empresas compatibles dentro de un ecosistema empresarial, evaluando cinco criterios fundamentales:
	•	Objetivos estratégicos
	•	Intereses estratégicos
	•	Número total de empleados
	•	Tamaño de la empresa
	•	Ubicación geográfica

El sistema genera emparejamientos entre empresas según:
	•	**Afinidad:** similitud directa en los objetivos e intereses estratégicos.
	•	**Sinergia:** complementariedad de estrategias entre empresas.

El objetivo es construir redes empresariales más inteligentes, colaborativas y alineadas estratégicamente.

## Funcionalidades
1. **Carga de datos** con información empresarial estructurada.
2. **Evaluación de afinidad estratégica** Coincidencia binaria de estrategias (objetivos + intereses).
3.	**Evaluación de sinergia estratégica** Complementariedad entre lo que tiene una empresa y le falta a la otra.
4.	**Comparación por número de empleados**  Favorece similitudes en capacidad operativa.
5.	**Comparación por tamaño empresarial** Micro, pequeña, mediana o grande.
6.	**Evaluación de cercanía geográfica** (ciudad).
7.	**Generación de tabla de emparejamientos** ordenada por compatibilidad total.

## Uso
### 1. **Carga de Datos**
La data debe contener las siguientes columnas:
-	**Identificación**:
`nit`,`razonsocial`,`nombrecomercial`
- **Información organizacional**:
`num_empleados_directos`, `num_empleados_indirectos`, `ciudad`, `tamaño`
- **Objetivos estratégicos** (binarios: 1 = sí, 0 = no):
`crear_nuevos_modelos_negocio`,`generar_eficiencias`,`fidelizar_mercado_actual`,`diversificar_mercado`
- **Intereses estratégicos** (también binarios):
`incremento_ventas`,`llegar_nuevos_mercados`,`lanzamiento_nuevos_productos`,`mejoramiento_productividad`,`incremento_capacidad_productiva`,`desarrollo_nuevos_canales`,`implementacion_ti`,`infraestructura_fisica`,`compra_maquinaria_equipos`


### 2. **Ejecución del Algoritmo**
El código toma los datos y genera un conjunto de emparejamientos evaluados según criterios estratégicos, operacionales y geográficos.

### 3. **Cálculo del Matching**

El algoritmo calcula dos tipos de emparejamientos:

#### **a) Matching por Afinidad**
Se define como el número de coincidencias exactas en el vector estratégico (objetivos + intereses):
```math
M_{\text{afinidad}}(A,B) = \sum_{i=1}^{n} \mathbf{1}(S_{Ai} = S_{Bi})
```
Donde:
- $S_{Ai}$ y $S_{Bi}$ son los valores del componente $i$ del vector estratégico de las empresas $A$ y $B$, respectivamente.
- $n$ es el número total de elementos estratégicos (en este modelo, $n = 13$).
- ${1}(\cdot)$ es la función indicadora, definida como:
```math
{1}(P) =
\begin{cases}
1, & \text{si la proposición } P \text{ es verdadera (es decir, } S_{Ai} = S_{Bi} \text{)} \\
0, & \text{si la proposición } P \text{ es falsa}
\end{cases}
```

#### **b) Matching por Sinergia**
El matching por sinergia evalúa la complementariedad estratégica entre dos empresas. Es decir, identifica casos en los que una empresa tiene una estrategia que la otra no posee, lo cual representa una oportunidad de cooperación o alianza para cubrir vacíos mutuos.
```math
M_{\text{sinergia}}(A,B) = \sum_{i=1}^{n} \left[ \mathbf{1}(S_{Ai} = 1 \land S_{Bi} = 0) + \mathbf{1}(S_{Ai} = 0 \land S_{Bi} = 1) \right]
```

Donde:
• $S_{Ai}$ y $S_{Bi}$ son los valores binarios del componente estratégico $i$ (objetivo o interés) para las empresas $A$ y $B$.
•	$n$ es el número total de estrategias evaluadas (13 en este modelo).
•  ${1}(\cdot)$  es la función indicadora, que vale 1 si la condición es verdadera, y 0 si es falsa.

Un valor alto de $M_{\text{sinergia}}$ sugiere que las empresas tienen capacidades o enfoques que se complementan, lo cual es ideal para construir alianzas, asociaciones o cadenas de valor.

#### **c) Diferencia de Empleados**
Se usa una normalización inversa para favorecer empresas con números similares de empleados:
```math
E_1 = E_{directos1} + E_{indirectos1} \\
E_2 = E_{directos2} + E_{indirectos2} \\
M_{empleados} = \frac{1}{1 + |E_1 - E_2|}
```
Donde:
- $E_1$ y $E_2$ son el número total de empleados de cada empresa.

Se suma 1 en el denominador para evitar divisiones por cero.
Empresas con tamaños similares obtienen valores más altos.

#### **d) Coincidencia de Ciudad**
Si ambas empresas están en la misma ciudad:
```math
M_{ciudad} = 
\begin{cases} 
1, & \text{si ciudad 1 = ciudad 2} \\
0, & \text{si son diferentes} 
\end{cases}
```

#### **d) Coincidencia de Tamaño Empresarial**
Evalúa si ambas empresas están en la misma categoría (Micro, Pequeña, Mediana, Grande):
```math
M_{tamaño} = 
\begin{cases} 
1, & \text{si tamaño 1 = tamaño 2} \\
0, & \text{si son diferentes} 
\end{cases}
```

#### **e) Puntaje Total de Matching**
El puntaje total se obtiene combinando todas las métricas anteriores:
```math
M_{total} = M_{afinidad} + M_{sinergia} + M_{empleados} + M_{ciudad} + M_{tamaño}
```
Cada componente aporta al valor total del emparejamiento:
$M_{\text{afinidad}}$ similitud estratégica directa.
$M_{\text{sinergia}}$ complementariedad en estrategias.
$M_{\text{empleados}}$ similitud en capacidad operativa.
$M_{\text{ciudad}}$ cercanía geográfica.
$M_{\text{tamaño}}$ coincidencia en categoría organizacional.
$M_{\text{total}}$ permite ordenar y priorizar los emparejamientos posibles dentro del ecosistema empresarial.

Cuanto mayor sea el puntaje total, más recomendable es la conexión entre las dos empresas para alianzas, cooperación o desarrollo conjunto.


### 4. **Interpretación de los Resultados**
La salida consiste en una tabla que presenta los emparejamientos estratégicos más relevantes entre empresas del ecosistema. Cada fila representa una pareja de empresas potencialmente compatibles. Las columnas incluyen:
•	Empresa 1 y Empresa 2: Nombres comerciales de las empresas emparejadas.
•	Ciudad 1 y Ciudad 2: Ubicación geográfica de cada empresa. Se favorecen las coincidencias.
•	Tamaño 1 y Tamaño 2: Clasificación de la empresa según su tamaño (Micro, Pequeña, Mediana, Grande).
•	Match Afinidad: Número de coincidencias exactas en los objetivos e intereses estratégicos entre las dos empresas. Valores más altos indican mayor similitud en sus enfoques empresariales.
•	Match Sinergia: Número de elementos estratégicos que una empresa tiene y la otra no. Refleja la complementariedad: un valor alto sugiere que las empresas pueden beneficiarse mutuamente cubriendo vacíos estratégicos.
•	Total Empleados 1 y Total Empleados 2: Suma de empleados directos e indirectos para cada empresa.
•	Diferencia Empleados: Diferencia absoluta en el número total de empleados entre ambas empresas. Cuanto menor sea esta diferencia, más cercanas están en capacidad operativa.
•	Match Ciudad: Valor binario (1 o 0). Es 1 si ambas empresas están en la misma ciudad, lo que favorece colaboraciones logísticas y presenciales.
•	Match Tamaño: Valor binario (1 o 0). Es 1 si ambas empresas pertenecen a la misma categoría de tamaño empresarial.
•	Puntaje Total: Suma de todas las métricas de compatibilidad:

$M_{total} = M_{afinidad} + M_{sinergia} + M_{empleados} + M_{ciudad} + M_{tamaño}$

Un mayor puntaje total indica una mayor compatibilidad entre las empresas para potenciales alianzas, asociaciones estratégicas o cooperación en proyectos.

### **5. Aplicaciones y Uso**
El Modelo MASE tiene múltiples aplicaciones dentro de ecosistemas empresariales, redes de colaboración, programas de desarrollo económico y estrategias de integración territorial. Estas son algunas de sus principales utilidades:
•	**Fomentar asociaciones estratégicas**
Permite identificar empresas que comparten una visión similar en términos de objetivos e intereses estratégicos. Estas empresas pueden formar alianzas para proyectos conjuntos, compartir conocimientos o participar en programas colaborativos.
•	**Detectar oportunidades de sinergia**
Al destacar la complementariedad entre empresas, el modelo ayuda a encontrar casos en los que una empresa puede cubrir vacíos estratégicos de otra. Esto es útil para formar consorcios, asociaciones público-privadas o cadenas de valor.
•	**Optimizar programas de aceleración, incubación y clústeres**
MASE puede usarse como herramienta de diagnóstico y emparejamiento en programas de emprendimiento, clústeres sectoriales y aceleradoras, ayudando a conectar empresas compatibles dentro del mismo entorno.
•	**Fortalecer redes empresariales locales o regionales**
Al incorporar la ubicación geográfica como criterio de matching, se facilita la integración de empresas en ecosistemas locales, lo que impacta positivamente la economía territorial.
•	**Apoyar procesos de toma de decisiones en cámaras de comercio, gremios o gobiernos**
El modelo puede alimentar políticas públicas o estrategias de desarrollo productivo que requieran emparejamiento de empresas con base en evidencia estratégica.
•	**Identificar brechas de capacidades o focos de inversión**
Al analizar sistemáticamente la afinidad y sinergia en los vectores estratégicos, se pueden identificar áreas estratégicas poco desarrolladas y proponer acciones de fortalecimiento institucional o inversión privada.