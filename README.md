# 📊 Sistema de Inteligencia Deportiva: Pipeline FIFA & Tablero Looker Studio

Este repositorio contiene el desarrollo del pipeline de datos (ETL) en Python enfocado en la limpieza, unificación y cálculo del **Índice de Eficiencia de Dominio (IED)** a partir de microdatos de rendimiento deportivo. Los resultados procesados alimentan de forma automatizada un tablero interactivo en **Looker Studio**.

---

## 🛠️ Arquitectura del Proceso (Pipeline)

El script de Python realiza las siguientes tareas críticas de ingeniería de datos:
1. **🕸️ Extracción Automatizada (Web Scraping):** extrae los microdatos deportivos directamente desde las fuentes web de origen, automatizando la captura de las estadísticas crudas de rendimiento, ataque y defensa de los jugadores y equipos.
2. **🧹 Limpieza Vectorizada:** Normaliza variables clave (como transformar la tenencia de texto `"51.5%"` a formato flotante `0.515`).
3. **🔀 Consolidación (Merge):** Cruza bases independientes de ataque y defensa a nivel de jugador/equipo utilizando un identificador único, evitando la pérdida de registros.
4. **🧮 Cálculo del IED:** Aplica un modelo matemático con penalización dinámica atenuada por la cantidad de partidos jugados ($PJ$), evitando sesgos por goleadas atípicas (*outliers*).
5. **🗂️ Tratamiento de Duplicados:** Restringe la granularidad de la métrica a nivel de equipo mediante técnicas de desduplicación antes de reinyectarla al set de jugadores.
6. **🏷️ Clasificación Cualitativa:** Asigna etiquetas ordinales de rendimiento según la escala final del indicador.

---

## 📈 Estructura del Tablero (Looker Studio)

El tablero está optimizado para tener conocimiento sobre el juego de Argentina y mediante un resumen de un paneo del resto de los equipos del torneo. Con solo 2 pestañas podemos tener un conocimiento certero del desarrollo del campeonato.
### 🇦🇷 Componente 1: Ficha Técnica ( Argentina)
Módulo descriptivo enfocado en el diagnóstico y auditoría del rendimiento de la Selección Nacional:
* **Métricas de Control de Juego:** Monitorización de la tenencia promedio de balón y volumen de circulación.
* **KPIs de Conversión y Solidez:** Análisis de efectividad en área rival frente al volumen de contención en área propia.
* **Data Labeling Status:** Posicionamiento cualitativo de la selección dentro del esquema jerárquico del IED.

### 🏆 Componente 2: Resumen del Torneo 
Panel analítico cross-torneo para el análisis comparativo del campeonato mediante rankings y matrices de dispersión:
* **⚽ Scoring Goleador:** Top de máximos artilleros e indicadores de efectividad individual.
* **🛡️ Defensive Performance:** Matriz de rendimiento de defensores clave y vallas menos vencidas.
* **🎛️ Possession Ranking:** Distribución de control de juego indexada por club.
* **🥇 Elite Performance (Top IED):** Clasificación de equipos líderes bajo la métrica del indicador ponderado.
* **🎯 Shooting Volume:** Balance neto de disparos (Tiros a Favor vs. Tiros en Contra) desagregado por institución.

* ## 📐 Especificación del Modelo Matemático: IED

El **Índice de Eficiencia de Dominio (IED)** evalúa de forma multivariable la relación entre el control del balón y la verticalidad ofensiva/defensiva. Aplicando una penalización dinámica según el el equipo tenga diferencia de gol favorable/neutra o negativa.



🔗 **[Accedé aquí al Tablero de Control Interactivo | Looker Studio](https://datastudio.google.com/reporting/53ab282a-c94e-4eee-b718-384c8fffabe9/page/O3F2F)**
