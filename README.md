# 📊 Sistema de Inteligencia Deportiva: Pipeline FIFA & Tablero Looker Studio

Este repositorio contiene el desarrollo del pipeline de datos (ETL) en Python enfocado en la limpieza, unificación y cálculo del **Índice de Eficiencia de Dominio (IED)** a partir de microdatos de rendimiento deportivo. Los resultados procesados alimentan de forma automatizada un tablero interactivo en **Looker Studio**.

---

## 🛠️ Arquitectura del Proceso (Pipeline)

El script de Python realiza las siguientes tareas críticas de ingeniería de datos:
1. **Extracción Automatizada (Web Scraping):** extrae los microdatos deportivos directamente desde las fuentes web de origen, automatizando la captura de las estadísticas crudas de rendimiento, ataque y defensa de los jugadores y equipos.
2. **Limpieza Vectorizada:** Normaliza variables clave (como transformar la tenencia de texto `"51.5%"` a formato flotante `0.515`).
3. **Consolidación (Merge):** Cruza bases independientes de ataque y defensa a nivel de jugador/equipo utilizando un identificador único, evitando la pérdida de registros.
4. **Cálculo del IED:** Aplica un modelo matemático con penalización dinámica atenuada por la cantidad de partidos jugados ($PJ$), evitando sesgos por goleadas atípicas (*outliers*).
5. **Tratamiento de Duplicados:** Restringe la granularidad de la métrica a nivel de equipo mediante técnicas de desduplicación antes de reinyectarla al set de jugadores.
6. **Clasificación Cualitativa:** Asigna etiquetas ordinales de rendimiento según la escala final del indicador.

---

## 📈 Estructura del Tablero (Looker Studio)

El tablero está optimizado para tener conocimiento sobre el juego de Argentina y mediante un resumen de un paneo del resto de los equipos del torneo. Con solo 2 pestañas podemos tener un conocimiento certero del desarrollo del campeonato.

