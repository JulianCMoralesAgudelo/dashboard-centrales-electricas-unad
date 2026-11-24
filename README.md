# Dashboard interactivo de centrales eléctricas del mundo

## Descripción de la actividad

Este repositorio contiene el producto desarrollado para la **Tarea 4: Comunicación de resultados mediante dashboard interactivo** del curso **Programación para el análisis de datos (203008069)** de la Universidad Nacional Abierta y a Distancia (UNAD). La actividad corresponde al momento final del curso y tiene como propósito transformar el análisis exploratorio realizado en la Tarea 3 en una aplicación publicada, comprensible para personas que no tienen formación especializada en estadística.

El dashboard no plantea un análisis diferente al de la actividad anterior. Retoma el mismo conjunto de datos, los gráficos principales, la comparación estadística entre centrales solares y de carbón y las conclusiones ya verificadas. El cambio está en la forma de comunicar los resultados: la información se presenta mediante filtros, métricas y gráficos que permiten explorar los datos sin modificar el alcance del estudio original.

## Objetivo del proyecto

Comunicar de manera clara los principales resultados del análisis de las centrales eléctricas registradas en la **Global Power Plant Database**, diferenciando tres aspectos que no deben interpretarse como equivalentes:

- La cantidad de centrales registradas por fuente de energía.
- La potencia instalada de cada central, expresada en megavatios (MW).
- La electricidad reportada durante un año, expresada en gigavatios-hora (GWh).

La aplicación está dirigida a tomadores de decisiones y usuarios no técnicos. Por esta razón, incluye explicaciones en lenguaje común y evita presentar asociaciones estadísticas como relaciones de causa y efecto.

## Conjunto de datos

Se utiliza la **Global Power Plant Database** del World Resources Institute (WRI). La copia analizada contiene **34.936 centrales y 36 variables**. El archivo CSV publicado en este repositorio es el mismo empleado y auditado en la Tarea 3; su integridad se comprueba desde la aplicación mediante una huella SHA-256.

La base reúne información sobre ubicación, fuente principal de energía, potencia instalada y generación reportada para distintos años. No todas las centrales tienen información histórica completa, por lo que el dashboard informa la cantidad de registros disponibles en cada comparación y conserva los valores faltantes sin reemplazarlos por cero.

## Funcionalidades del dashboard

La aplicación fue construida con Streamlit e incluye:

- Un filtro por fuente principal de energía.
- Un filtro por rango de potencia instalada.
- Una tabla que se actualiza con los filtros seleccionados.
- Métricas de cantidad de registros, potencia media y desviación estándar.
- Un gráfico de centrales por fuente de energía.
- Una gráfica de potencia instalada frente a generación reportada en 2017.
- Una serie de generación media entre 2013 y 2019 para las mismas centrales con datos completos.
- La prueba t de Welch de la Tarea 3, calculada sobre el registro completo y sin alterarse por los filtros exploratorios.
- Una narrativa organizada en cuatro preguntas: qué se analizó, qué se encontró, qué significa y qué se recomendaría.
- Mensajes claros cuando una selección no contiene registros o no tiene datos suficientes para un gráfico.

## Principales hallazgos

- La base registra **10.665 centrales solares** y **2.330 centrales de carbón**.
- La potencia media es de **17,66 MW** en las centrales solares y de **843,58 MW** en las de carbón. La prueba t de Welch confirma una diferencia entre las medias del registro analizado, pero no demuestra que el combustible sea su causa.
- Entre **9.500 centrales** con datos de potencia y generación en 2017, una mayor potencia tiende a estar acompañada de una mayor generación reportada. La correlación de Pearson es **0,8437** y no debe interpretarse como causalidad.
- El panel de **6.030 centrales** con información disponible durante los siete años pasó de **574,70 GWh por central en 2013** a **608,50 GWh en 2019**.

## Estructura del repositorio

| Archivo | Descripción |
| --- | --- |
| `app.py` | Código principal del dashboard en Streamlit. |
| `global_power_plant_database.csv` | Copia íntegra del conjunto de datos utilizado en la Tarea 3. |
| `narrativa.md` | Texto de hallazgos presentado dentro del dashboard. |
| `requirements.txt` | Versiones de las librerías necesarias. |
| `Dockerfile` | Imagen reproducible para ejecutar la aplicación. |
| `compose.yaml` | Configuración local del servicio y del puerto 8501. |

## Instrucciones de uso

### Opción 1: ejecución con Python

1. Clone el repositorio y entre en su directorio:

   ```bash
   git clone https://github.com/JulianCMoralesAgudelo/dashboard-centrales-electricas-unad.git
   cd dashboard-centrales-electricas-unad
   ```

2. Cree un entorno virtual con Python 3.12:

   ```bash
   python3.12 -m venv .venv
   ```

3. Active el entorno en Fedora o en otra distribución Linux:

   ```bash
   source .venv/bin/activate
   ```

   En Windows PowerShell use:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

4. Instale las dependencias:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Inicie el dashboard:

   ```bash
   streamlit run app.py
   ```

6. Abra `http://localhost:8501` en Microsoft Edge.

### Opción 2: ejecución con Docker Compose

1. Compruebe que Docker esté activo.
2. Desde la raíz del repositorio ejecute:

   ```bash
   docker compose -p pad-g4 up --build -d
   ```

3. Verifique el servicio:

   ```bash
   docker compose -p pad-g4 ps
   curl -fsS http://127.0.0.1:8501/_stcore/health
   ```

4. Abra `http://localhost:8501` en Microsoft Edge.

5. Para detener la aplicación ejecute:

   ```bash
   docker compose -p pad-g4 down
   ```

## Dashboard publicado

La URL de Streamlit Community Cloud y la captura de la aplicación publicada se incorporarán después de verificar el despliegue en Microsoft Edge.

## Fuente y licencia de los datos

Los datos provienen del [World Resources Institute](https://github.com/wri/global-power-plant-database) y se distribuyen bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Autor y contexto académico

**Julian Camilo Morales Agudelo**  
Grupo 14  
Programación para el análisis de datos — 203008069  
Universidad Nacional Abierta y a Distancia — UNAD  
Noviembre de 2026
