# MASE Modelo de Afinidad y Sinergia Empresarial
## Algoritmo de Matching entre Empresas en un Ecosistema
### Rodrigo García,PhD

## Descripción

Este algoritmo identifica empresas compatibles dentro de un ecosistema empresarial, evaluando cinco criterios fundamentales:
* Objetivos estratégicos
* Intereses estratégicos
* Número total de empleados
* Tamaño de la empresa
* Ubicación geográfica
* Compatibilidad con Sectores economicos (Matriz de compatibilidad de actividades)
El sistema genera emparejamientos entre empresas según:
* **Afinidad:** similitud directa en los objetivos e intereses estratégicos.
* **Sinergia:** complementariedad de estrategias entre empresas.

El objetivo es construir redes empresariales más inteligentes, colaborativas y alineadas estratégicamente, teniendo en cuenta también la cercanía o complementariedad de sus actividades productivas.

## Funcionalidades
1. **Carga de datos** con información empresarial estructurada.
2. **Evaluación de afinidad estratégica** Coincidencia binaria de estrategias (objetivos + intereses).
3.	**Evaluación de sinergia estratégica** Complementariedad entre lo que tiene una empresa y le falta a la otra.
4.	**Comparación por número de empleados**  Favorece similitudes en capacidad operativa.
5.	**Comparación por tamaño empresarial** Micro, pequeña, mediana o grande.
6.	**Evaluación de cercanía geográfica** (ciudad).
7.  **Evaluación de compatibilidad sectorial** Matriz de compatibilidad de sectores.
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
- **Código CIIU**  identificador de actividad economica, para la compatibilidad sectorial. Ejemplo: codigo_ciiu con 4 dígitos (1010, 1050, etc.).

### 2. **Ejecución del Algoritmo**
El código toma los datos y genera un conjunto de emparejamientos evaluados según criterios estratégicos, operacionales, geográficos y sectoriales

### 3. **Cálculo del Matching**

El algoritmo calcula dos tipos de emparejamientos:

#### **a) Matching por Afinidad**
Se define como el número de coincidencias exactas en el vector estratégico (objetivos + intereses):
```math
M_{\text{afinidad}}(A,B) = \sum_{i=1}^{n} \mathbf{1}(S_{Ai} = S_{Bi})
```
Donde:
* $S_{Ai}$ y $S_{Bi}$ son los valores del componente $i$ del vector estratégico de las empresas $A$ y $B$, respectivamente.
* $n$ es el número total de elementos estratégicos (en este modelo, $n = 13$).
* ${1}(\cdot)$ vale 1 si se cumple la igualdad $(S_{Ai} = S_{Bi})$, y 0 si no.

#### **b) Matching por Sinergia**
El matching por sinergia evalúa la complementariedad estratégica entre dos empresas. Es decir, identifica casos en los que una empresa tiene una estrategia que la otra no posee, lo cual representa una oportunidad de cooperación o alianza para cubrir vacíos mutuos.

```math
M_{\text{sinergia}}(A,B) = \sum_{i=1}^{n} \left[ \mathbf{1}(S_{Ai} = 1 \land S_{Bi} = 0) + \mathbf{1}(S_{Ai} = 0 \land S_{Bi} = 1) \right]
```

Donde:
* $S_{Ai}$ y $S_{Bi}$ son los valores binarios del componente estratégico $i$ (objetivo o interés) para las empresas $A$ y $B$.
* $n$ es el número total de estrategias evaluadas (13 en este modelo).
*  ${1}(\cdot)$  es la función indicadora, que vale 1 si la condición es verdadera, y 0 si es falsa.

Un valor alto de $M_{\text{sinergia}}$ sugiere que las empresas tienen capacidades o enfoques que se complementan, lo cual es ideal para construir alianzas, asociaciones o cadenas de valor.

#### **c) Diferencia de Empleados**
Se usa una normalización inversa para favorecer empresas con números similares de empleados:
```math
E_1 = E_{directos1} + E_{indirectos1} \\
E_2 = E_{directos2} + E_{indirectos2} \\
M_{empleados} = \frac{1}{1 + |E_1 - E_2|}
```
Donde:
* $E_1$ y $E_2$ son el número total de empleados de cada empresa.

Empresas con tamaños similares obtienen valores más altos.

#### **d) Coincidencia de Ciudad**
Si ambas empresas están en la misma ciudad:
```math
M_{ciudad}(A,B) =
\begin{cases}
1, & \text{si ciudad(A) = ciudad (B)} \\
0, & \text{si son diferentes}
\end{cases}
```
#### **d) Coincidencia de Tamaño Empresarial**
Evalúa si ambas empresas están en la misma categoría (Micro, Pequeña, Mediana, Grande):
```math
M_{tamaño}(A,B) =
\begin{cases}
1, & \text{si tamaño(A) = tamaño(B)} \\
0, & \text{si son diferentes}
\end{cases}
```

#### **e) Compatibilidad Sector economico**
A continuación se describe un procedimiento genérico para construir la matriz de compatibilidad sectorial usando códigos CIIU de 4 dígitos. Esta matriz tendrá dimensiones $m \times m$, donde m es el número de códigos CIIU distintos que aparecen en el ecosistema de empresas.

1. Recopilación de Códigos CIIU
- Extracción: Se obtuvo de la base de datos la lista de códigos CIIU de todas las empresas, asegurándose de que estén representados en 4 dígitos (por ejemplo, rellenando con ceros si fuera necesario).
- Único: Se eliminan los duplicados para tener un conjunto único $\{c_1, c_2, \dots, c_m\}$ que serán las filas y columnas de la matriz.
2. Definición de la Distancia Entre Códigos
Se define una función $\text{distanciaCiiu}(c_i, c_j)$ que mide qué tan diferentes son dos códigos. Existen diversas maneras de hacerlo, pero una de las más usadas es:
- Comparamos dígito a dígito desde el inicio hasta que detectemos una diferencia.
- Distancia = número de dígitos (sobre 4) que no coinciden en los códigos ejemplo:
	- 1010 vs. 1050 → Coinciden en “10” (2 dígitos) y difieren en el tercero → distancia = 2.
	- 2011 vs. 2012 → Coinciden en “201” (3 dígitos) y difieren en el cuarto → distancia = 1.
	- 1010 vs. 2011 → Difieren en el primer dígito → distancia = 4.
3. Conversión a Compatibilidad (0 a 1)
Para traducir la distancia a un índice de compatibilidad, se emplea:
```math
\text{compatibilidad\_ciiu}(c_i, c_j)
= 1 - \frac{\text{distanciaCiiu}(c_i, c_j)}{\text{distancia\_máxima}}
```
Donde:
* distancia\_máxima = 4 (siempre que use 4 dígitos).
* Cuanto menor sea la distancia, mayor la compatibilidad.
	* 1 significa que ambos códigos son idénticos (distancia = 0).
	* 0 significa que difieren desde el primer dígito (distancia = 4).
4. Construcción de la Matriz
* **Inicializar**: Se crea una matriz $M$ de tamaño $m \times m$, donde cada fila y columna corresponde a uno de los códigos CIIU.
* **Iteración**: Para cada par $(c_i, c_j)$, se calcula:
$M_{ij} = \text{compatibilidad\_ciiu}(c_i, c_j)$.
* **Simetría**: Dado que la compatibilidad es un concepto recíproco $(M_{ij} = M_{ji})$, se rellena la mitad inferior de la matriz con los mismos valores de la superior, o viceversa.
Ejemplo para cuatro códigos $\{1010, 1050, 2011, 2012\}$:

| **Código \ Código** | **1010** | **1050** | **2011** | **2012** |
|:-------------------:|:--------:|:--------:|:--------:|:--------:|
| **1010**            | **1.00** | 0.50     | 0.00     | 0.00     |
| **1050**            | 0.50     | **1.00** | 0.00     | 0.00     |
| **2011**            | 0.00     | 0.00     | **1.00** | 0.75     |
| **2012**            | 0.00     | 0.00     | 0.75     | **1.00** |

$(1010, 1010) = 1.0$ (distancia = 0)
$(1010, 1050) = 0.50$ (distancia = 2 → 1 - 2/4 = 0.5)
$(2011, 2012) = 0.75$ (distancia = 1 → 1 - 1/4 = 0.75)

Una vez construida la matriz M (compatibilidad sectorial), el Modelo MASE la emplea de la siguiente manera:
* Cada empresa E tiene un código CIIU.
* Al comparar dos empresas A y B, se localiza la celda $(c_A, c_B)$ en la matriz, y se obtiene su valor:
$M_{\text{sector}}(A,B) = M[c_A, c_B]$.
* Ese valor (0 a 1) se suma al puntaje total $M_{\text{total}}$ junto con la afinidad, sinergia, empleados, ciudad y tamaño.

#### **f ) Puntaje Total de Matching**
El puntaje total se obtiene combinando todas las métricas anteriores:
```math
M_{total} = M_{afinidad} + M_{sinergia} + M_{empleados} + M_{ciudad} + M_{tamaño} + M_{sector}
```
Cada componente aporta al valor total del emparejamiento:
$M_{\text{afinidad}}$ similitud estratégica directa.
$M_{\text{sinergia}}$ complementariedad en estrategias.
$M_{\text{empleados}}$ similitud en capacidad operativa.
$M_{\text{ciudad}}$ cercanía geográfica.
$M_{\text{tamaño}}$ coincidencia en categoría organizacional.
$M_{\text{sector}}$ mide cuán cercanos son los códigos CIIU (0 a 1) en la matriz de distancias.
$M_{\text{total}}$ permite ordenar y priorizar los emparejamientos posibles dentro del ecosistema empresarial.

Cuanto mayor sea el puntaje total, más recomendable es la conexión entre las dos empresas para alianzas, cooperación o desarrollo conjunto.

### **4. Aplicaciones y Uso**
El Modelo MASE tiene múltiples aplicaciones dentro de ecosistemas empresariales, redes de colaboración, programas de desarrollo económico y estrategias de integración territorial. Estas son algunas de sus principales utilidades:
* **Fomentar asociaciones estratégicas**
Permite identificar empresas que comparten una visión similar en términos de objetivos e intereses estratégicos. Estas empresas pueden formar alianzas para proyectos conjuntos, compartir conocimientos o participar en programas colaborativos.
* **Detectar oportunidades de sinergia**
Al destacar la complementariedad entre empresas, el modelo ayuda a encontrar casos en los que una empresa puede cubrir vacíos estratégicos de otra. Esto es útil para formar consorcios, asociaciones público-privadas o cadenas de valor.
* **Optimizar programas de aceleración, incubación y clústeres**
MASE puede usarse como herramienta de diagnóstico y emparejamiento en programas de emprendimiento, clústeres sectoriales y aceleradoras, ayudando a conectar empresas compatibles dentro del mismo entorno.
* **Fortalecer redes empresariales locales o regionales**
Al incorporar la ubicación geográfica como criterio de matching, se facilita la integración de empresas en ecosistemas locales, lo que impacta positivamente la economía territorial.
* **Apoyar procesos de toma de decisiones en cámaras de comercio, gremios o gobiernos**
El modelo puede alimentar políticas públicas o estrategias de desarrollo productivo que requieran emparejamiento de empresas con base en evidencia estratégica.
* **Identificar brechas de capacidades o focos de inversión**
Al analizar sistemáticamente la afinidad y sinergia en los vectores estratégicos, se pueden identificar áreas estratégicas poco desarrolladas y proponer acciones de fortalecimiento institucional o inversión privada.
