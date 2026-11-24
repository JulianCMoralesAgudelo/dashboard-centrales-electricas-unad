"""Dashboard de la Tarea 4 sobre el EDA auditado de la Tarea 3."""

from hashlib import sha256
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind
import streamlit as st


BASE = Path(__file__).resolve().parent
CSV = BASE / "global_power_plant_database.csv"
HUELLA = "4b1f93e0fd93664f18684d9b05d0a52ed9658c6a8cf0d21ff2520791379ba7fc"
CAPACIDAD = "capacity_mw"
GENERACION = "generation_gwh_2017"
COMBUSTIBLE = "primary_fuel"
ANIOS = range(2013, 2020)
COLUMNAS_ANUALES = [f"generation_gwh_{anio}" for anio in ANIOS]
FUENTES = {
    "Biomass": "Biomasa", "Coal": "Carbón", "Cogeneration": "Cogeneración",
    "Gas": "Gas", "Geothermal": "Geotérmica", "Hydro": "Hidroeléctrica",
    "Nuclear": "Nuclear", "Oil": "Petróleo", "Other": "Otra",
    "Petcoke": "Coque de petróleo", "Solar": "Solar", "Storage": "Almacenamiento",
    "Waste": "Residuos", "Wave and Tidal": "Olas y mareas", "Wind": "Eólica",
}


@st.cache_data
def cargar_datos():
    """Comprueba que el CSV corresponde a la versión auditada en G3."""
    contenido = CSV.read_bytes()
    if sha256(contenido).hexdigest() != HUELLA:
        raise ValueError("El CSV no coincide con la copia auditada de la Tarea 3.")
    return pd.read_csv(BytesIO(contenido), low_memory=False)


def numero(valor, decimales=2):
    if pd.isna(valor):
        return "Sin datos"
    return f"{valor:,.{decimales}f}".translate(str.maketrans(",.", ".,"))


def barras(datos):
    conteos = datos[COMBUSTIBLE].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(7, max(2.2, len(conteos) * .32 + 1)))
    ax.barh(conteos.index.map(FUENTES), conteos.values, color="#007c78")
    ax.set(xlabel="Número de centrales", title="Centrales por fuente principal de energía")
    fig.tight_layout()
    return fig


def dispersion(datos):
    pares = datos.dropna(subset=[CAPACIDAD, GENERACION])
    if pares.empty:
        st.info("Esta selección no tiene datos de generación reportada en 2017.")
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(pares[CAPACIDAD], pares[GENERACION], s=13, alpha=.3, color="#1c6488")
    ax.set(xlabel="Potencia instalada (MW)", ylabel="Electricidad reportada (GWh)",
           title="Potencia y electricidad generada en 2017")
    fig.tight_layout()
    mostrar(fig)
    st.caption(f"Centrales con ambas cifras: {numero(len(pares), 0)} de {numero(len(datos), 0)}.")


def serie_anual(datos):
    panel = datos.dropna(subset=COLUMNAS_ANUALES)
    if panel.empty:
        st.info("Esta selección no tiene centrales con cifras para los siete años.")
        return
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(list(ANIOS), panel[COLUMNAS_ANUALES].mean().to_numpy(),
            marker="o", color="#007c78")
    ax.set(xticks=list(ANIOS), xlabel="Año", ylabel="GWh por central",
           title="Electricidad media generada de 2013 a 2019")
    fig.tight_layout()
    mostrar(fig)
    st.caption(f"Mismas {numero(len(panel), 0)} centrales durante los siete años.")


def mostrar(fig):
    st.pyplot(fig)
    plt.close(fig)


def validacion(datos):
    # Conserva el alcance de la prueba original al explorar subconjuntos.
    solar = datos.loc[datos[COMBUSTIBLE].eq("Solar"), CAPACIDAD].dropna()
    carbon = datos.loc[datos[COMBUSTIBLE].eq("Coal"), CAPACIDAD].dropna()
    prueba = ttest_ind(solar, carbon, equal_var=False)
    st.write(
        f"En el registro completo, {numero(len(solar), 0)} centrales solares promedian "
        f"{numero(solar.mean())} MW y {numero(len(carbon), 0)} centrales de carbón "
        f"promedian {numero(carbon.mean())} MW. La diferencia es de "
        f"{numero(carbon.mean() - solar.mean())} MW a favor del grupo de carbón. "
        "La comparación aporta evidencia de que las potencias medias difieren entre "
        "estos grupos. El registro tampoco permite atribuir la diferencia al combustible."
    )
    probabilidad = "p < 0,001" if prueba.pvalue < .001 else f"p = {numero(prueba.pvalue, 3)}"
    st.caption(f"Prueba t de Welch de G3 sobre el registro completo, con filtros desactivados "
               f"para esta sección. t = {numero(prueba.statistic, 4)} · {probabilidad}.")


def main():
    st.set_page_config(page_title="Centrales eléctricas del mundo", layout="wide")
    st.title("Centrales eléctricas del mundo")
    st.write("Capacidad instalada y electricidad generada en la Global Power Plant Database.")
    try:
        datos = cargar_datos()
    except (OSError, ValueError) as error:
        st.error(str(error))
        st.stop()

    with st.sidebar:
        st.header("Filtros")
        fuente = st.selectbox("Fuente principal de energía",
                              ["Todas", *sorted(datos[COMBUSTIBLE].unique(), key=FUENTES.get)],
                              format_func=lambda fuente: FUENTES.get(fuente, fuente),
                              help="Permite ver una tecnología o conservar el registro completo.")
        limites = (float(datos[CAPACIDAD].min()), float(datos[CAPACIDAD].max()))
        inferior, superior = st.slider(
            "Potencia instalada (MW)", *limites, value=limites, step=.1, format="%.1f",
            help="Acota la potencia que puede entregar una central; no es su generación anual.",
        )
    seleccion = datos[CAPACIDAD].between(inferior, superior)
    if fuente != "Todas":
        seleccion &= datos[COMBUSTIBLE].eq(fuente)
    filtrados = datos.loc[seleccion]

    st.header("Exploración de datos")
    fuente_visible = "todas las fuentes" if fuente == "Todas" else FUENTES.get(fuente, fuente)
    st.caption(
        f"Filtros activos: {fuente_visible}; potencia entre {numero(inferior, 1)} y "
        f"{numero(superior, 1)} MW. Estos filtros no modifican la prueba de Welch."
    )
    capacidad = filtrados[CAPACIDAD]
    total, media, dispersion_mw = st.columns(3)
    total.metric("Centrales registradas", numero(len(filtrados), 0))
    media.metric("Potencia media (MW)", numero(capacidad.mean()))
    dispersion_mw.metric("Desviación estándar (MW)", numero(capacidad.std(ddof=1)))
    st.caption("La desviación estándar indica cuánto varía la potencia entre centrales. Requiere al menos dos registros.")
    tabla = filtrados[["name", "country_long", COMBUSTIBLE, CAPACIDAD, GENERACION]].copy()
    tabla[COMBUSTIBLE] = tabla[COMBUSTIBLE].map(FUENTES)
    tabla.columns = ["Central", "País", "Fuente principal", "Potencia (MW)", "Generación 2017 (GWh)"]
    st.dataframe(tabla, hide_index=True)

    st.header("Visualizaciones")
    if filtrados.empty:
        st.info("No hay centrales para esta combinación de filtros.")
    else:
        izquierda, derecha = st.columns(2)
        with izquierda:
            mostrar(barras(filtrados))
        with derecha:
            dispersion(filtrados)
        serie_anual(filtrados)

    st.header("Validación estadística")
    validacion(datos)

    st.header("Hallazgos")
    st.caption("Resultados del registro completo. Los gráficos de esta sección muestran ese mismo universo de referencia.")
    st.markdown((BASE / "narrativa.md").read_text(encoding="utf-8"))
    izquierda, derecha = st.columns(2)
    with izquierda:
        mostrar(barras(datos))
    with derecha:
        dispersion(datos)
    st.caption("[Fuente de datos: World Resources Institute — CC BY 4.0](https://github.com/wri/global-power-plant-database)")


if __name__ == "__main__":
    main()
