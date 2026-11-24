# Centrales eléctricas del mundo

Este dashboard comunica los resultados de la Tarea 3 de Programación para el análisis de datos. Permite explorar cuántas centrales registra cada tecnología, la diferencia entre potencia y electricidad generada, y la evolución de la generación reportada por las mismas centrales de 2013 a 2019.

Se emplea la Global Power Plant Database del World Resources Institute (WRI), con 34.936 centrales y 36 variables. El CSV conserva la huella de la copia auditada en G3. Su cobertura permite examinar tecnologías y países en una base común, con límites derivados de la disponibilidad de registros históricos.

## Hallazgos del EDA

- Solar tiene 10.665 centrales registradas y carbón tiene 2.330.
- La potencia media es de 17,66 MW en solar y 843,58 MW en carbón. La prueba t de Welch compara esas medias en el registro completo.
- Entre 9.500 centrales con ambos datos, una potencia mayor tiende a acompañarse de mayor generación en 2017 (Pearson r = 0,8437).
- El panel histórico de 6.030 centrales con datos en los siete años pasó de 574,70 GWh por central en 2013 a 608,50 GWh en 2019.

## Ejecución local

1. Abra una terminal en la carpeta que contiene `app.py`. Use Python 3.12.
2. Cree y active el entorno virtual en Fedora con `python3.12 -m venv .venv` y `source .venv/bin/activate`.
3. Instale las dependencias con `python -m pip install -r requirements.txt`.
4. Inicie con `streamlit run app.py`. Abra [la aplicación local](http://localhost:8501) en Microsoft Edge.

Con Docker Compose, ejecute `docker compose -p pad-g4 up --build -d` desde esta carpeta y abra la misma dirección.

## Publicación y captura

Pendientes hasta verificar el despliegue en Streamlit Community Cloud y capturar el dashboard funcionando en Microsoft Edge.

## Datos y autor

Datos de [World Resources Institute](https://github.com/wri/global-power-plant-database), licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Se redistribuye el CSV íntegro utilizado en G3.

Julian Camilo Morales Agudelo · Grupo 14 · Programación para el análisis de datos (203008069) · UNAD · Noviembre de 2026.
