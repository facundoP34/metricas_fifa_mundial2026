import time
import pandas as pd
import numpy as np
from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

print("====================================================")
print("  INICIANDO EXTRACTOR AUTOMATIZADO DE PLAYERS FIFA WORLD CUP 2026")
print("====================================================")

  # 1. Prepación de webdriver para el scraping asistido
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

try:  # 2. Carga del sitio con las estadísticas de Opta
    url = "https://theanalyst.com/competition/fifa-world-cup/stats"
    driver.get(url)
    
    print("Cargando la página web...")
    wait = WebDriverWait(driver, 20)
    
    # 3. Seleccionar 'Players'
    print("Configurando filtro: Seleccionando pestaña 'Players'...")
    boton_players = wait.until(EC.element_to_be_clickable((By.ID, "players")))
    boton_players.click()
    time.sleep(1.5)
    
    # 4. Abrir menú de categorías
    print("Configurando filtro: Abriendo menú de categorías...")
    desplegable_categoria = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='SelectDropdown-module_react-select']"))
    )
    desplegable_categoria.click()
    time.sleep(0.5)
    
    # 5. Seleccionar 'Attacking'
    print("Configurando filtro: Seleccionando 'Attacking'...")
    opcion_attacking = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'SelectDropdown-module_react-select__option') and contains(text(), 'Attacking')]"))
    )
    driver.execute_script("arguments[0].click();", opcion_attacking)
    
    print("Esperando a que la tabla cargue las métricas de ataque por jugador...")
    time.sleep(3)
    
    todas_las_paginas = []
    total_paginas = 14
    
    print("\nArrancando la extracción cíclica de datos...")
    for pagina in range(1, total_paginas + 1):
        print(f" -> Procesando página {pagina} de {total_paginas}...")
        time.sleep(2)
        
        html_actual = driver.page_source
        
        # --- Paso Clave: EXTRACCIÓN DE BANDERA/LOGOS CON BEAUTIFULSOUP ---
        soup = BeautifulSoup(html_actual, 'lxml')
        # Buscamos todas las filas de la tabla (ajustar etiqueta si la estructura varía)
        filas_html = soup.find_all('tr')
        
        ids_equipos = []
        # Recorremos las filas para extraer los IDs de las imágenes
        for fila in filas_html:
            # Buscamos si la fila tiene un encabezado (th) en lugar de datos (td) para ignorarla
            if fila.find('th'):
                continue
                
            img = fila.find('img')
            if img and 'id=' in img.get('src', ''):
                # Cortamos la URL para quedarnos solo con el código final del ID
                team_id = img['src'].split('id=')[-1]
                ids_equipos.append(team_id)
            else:
                ids_equipos.append("N/A")
        # -------------------------------------------------------------------
        
        # Extraemos la tabla numérica con Pandas de forma normal
        tablas_actuales = pd.read_html(StringIO(html_actual))
        
        if tablas_actuales:
            df_pagina = tablas_actuales[0]
            if isinstance(df_pagina.columns, pd.MultiIndex):
                df_pagina.columns = df_pagina.columns.droplevel(0)
            
            # Si la cantidad de IDs coincide con las filas de la tabla, los acoplamos
            if len(ids_equipos) == len(df_pagina):
                df_pagina['Team_ID'] = ids_equipos
                
            todas_las_paginas.append(df_pagina)
        
        if pagina < total_paginas:
            boton_siguiente = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='>']")))
            driver.execute_script("arguments[0].click();", boton_siguiente)
            
    print("\nUnificando las tablas extraídas...")
    df_final = pd.concat(todas_las_paginas, ignore_index=True)
    df_final = df_final.drop_duplicates()
    
    nombre_salida = "estadisticas_ataque_fifa_con_jugadores.xlsx"
    #df_final.to_excel(nombre_salida, index=False)
    
    print("\n====================================================")
    print(f" 🎉 ¡PROCESO EXITOSO! Archivo guardado: {nombre_salida}")
    print("====================================================")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando el navegador... ")
    driver.quit()


print("====================================================")
print("  INICIANDO EXTRACTOR AUTOMATIZADO DE TEAMS ATTACKING FIFA WORLD CUP 2026")
print("====================================================")

options_teams = webdriver.ChromeOptions()
options_teams.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options_teams)

tabla_teams = []

try:
    url = "https://theanalyst.com/competition/fifa-world-cup/stats"
    driver.get(url)
    
    print("Cargando la página web...")
    wait = WebDriverWait(driver, 20)
    
    # 3. Seleccionamos la variables por equipos 'TEAMS'
    print("Configurando filtro: Seleccionando pestaña 'Teams'...")
    boton_teams = wait.until(EC.element_to_be_clickable((By.ID, "teams")))
    boton_teams.click()
    time.sleep(1.5)

   
    # 4. Abrimos menú de categorías
    print("Configurando filtro: Abriendo menú de categorías...")
    desplegable_categoria_teams = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='SelectDropdown-module_react-select']"))
    )
    desplegable_categoria_teams.click()
    time.sleep(0.5)
    

    
    # 5. Seleccionamos 'Attacking' en TEAMS
    print("Configurando filtro: Seleccionando 'Attacking'...")
    opcion_attacking_teams = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'SelectDropdown-module_react-select__option') and contains(text(), 'Attacking')]"))
    )
    driver.execute_script("arguments[0].click();", opcion_attacking_teams)
    
    print("Esperando a que la tabla cargue las métricas de ataque...")
    time.sleep(3)
    
        
    html_actual_teams = driver.page_source
        
        # --- Paso Clave: EXTRACCIÓN DE BANDERA/LOGOS CON BEAUTIFULSOUP --- 
        # #Paso clave para hacerme de un id que permita ej join entre base players y base teams. el id del logo bandera oficia como id
    soup_teams = BeautifulSoup(html_actual_teams, 'lxml')
        # Buscamos todas las filas de la tabla (ajustar etiqueta si la estructura varía)
    filas_html = soup_teams.find_all('tr')
        
    ids_equipos_teams_teams = []
        # Recorremos las filas para extraer los IDs de las imágenes
    for fila in filas_html:
            # Buscamos si la fila tiene un encabezado (th) en lugar de datos (td) para ignorarla
            if fila.find('th'):
                continue
                
            img = fila.find('img')
            if img and 'id=' in img.get('src', ''):
                # Cortamos la URL para quedarnos solo con el código final del ID
                team_id = img['src'].split('id=')[-1]
                ids_equipos_teams_teams.append(team_id)
            else:
                ids_equipos_teams_teams.append("N/A")
        # -------------------------------------------------------------------
        
        # Extraemos la tabla numérica con Pandas de forma normal
    tablas_actuales_teams = pd.read_html(StringIO(html_actual_teams))
        
    if tablas_actuales_teams:
            df_final_teams = tablas_actuales_teams[0]
            if isinstance(df_final_teams.columns, pd.MultiIndex):
                df_final_teams.columns = df_final_teams.columns.droplevel(0)
            
            # Si la cantidad de IDs coincide con las filas de la tabla, los acoplamos
            if len(ids_equipos_teams_teams) == len(df_final_teams):
                df_final_teams['Team_ID'] = ids_equipos_teams_teams
                
            tabla_teams.append(df_final_teams)
        
            
    print("\nUnificando las tablas extraídas...")
    df_final_teams = pd.concat(tabla_teams, ignore_index=True)
    df_final_teams = df_final_teams.drop_duplicates()
    
    nombre_salida = "estadisticas_ataque_fifa_con_equipos.xlsx"
    #df_final_teams.to_excel(nombre_salida, index=False)
    
    print("\n====================================================")
    print(f" 🎉 ¡PROCESO EXITOSO! Archivo guardado: {nombre_salida}")
    print("====================================================")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando el navegador... ")
    driver.quit()


print("====================================================")
print("  INICIANDO EXTRACTOR AUTOMATIZADO DE TEAM PASSING FIFA WORLD CUP 2026")
print("====================================================")

options_teams = webdriver.ChromeOptions()
options_teams.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options_teams)

tabla_teams = []

try:
    url = "https://theanalyst.com/competition/fifa-world-cup/stats"
    driver.get(url)
    
    print("Cargando la página web...")
    wait = WebDriverWait(driver, 20)
    
    # 3. Seleccionar 'TEAMS'
    print("Configurando filtro: Seleccionando pestaña 'Teams'...")
    boton_teams = wait.until(EC.element_to_be_clickable((By.ID, "teams")))
    boton_teams.click()
    time.sleep(1.5)

   
    # 4. Abrimos menú de categorías
    print("Configurando filtro: Abriendo menú de categorías...")
    desplegable_categoria_teams = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='SelectDropdown-module_react-select']"))
    )
    desplegable_categoria_teams.click()
    time.sleep(0.5)
    

    
    # 5. Seleccionamos variable 'Passing'
    print("Configurando filtro: Seleccionando 'Passing'...")
    opcion_passing_teams = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'SelectDropdown-module_react-select__option') and contains(text(), 'Passing')]"))
    )
    driver.execute_script("arguments[0].click();", opcion_passing_teams)
    
    print("Esperando a que la tabla cargue las métricas de posesion...")
    time.sleep(3)
    
        
    html_actual_teams = driver.page_source
        
        # --- Paso clave: EXTRACCIÓN DE BANDERA/LOGOS CON BEAUTIFULSOUP ---
    soup_teams_tenencia = BeautifulSoup(html_actual_teams, 'lxml')
        # Buscamos todas las filas de la tabla (ajustar etiqueta si la estructura varía)
    filas_html = soup_teams_tenencia.find_all('tr')
        
    ids_equipos_teams_tenencia = []
        # Recorremos las filas para extraer los IDs de las imágenes
    for fila in filas_html:
            # Buscamos si la fila tiene un encabezado (th) en lugar de datos (td) para ignorarla
            if fila.find('th'):
                continue
                
            img = fila.find('img')
            if img and 'id=' in img.get('src', ''):
                # Cortamos la URL para quedarnos solo con el código final del ID
                team_id = img['src'].split('id=')[-1]
                ids_equipos_teams_tenencia.append(team_id)
            else:
                ids_equipos_teams_tenencia.append("N/A")
        # -------------------------------------------------------------------
        
        # Extraemos la tabla numérica con Pandas de forma normal
    tablas_actuales_teams_tenencia = pd.read_html(StringIO(html_actual_teams))
        
    if tablas_actuales_teams_tenencia:
            df_final_teams_tenencia = tablas_actuales_teams_tenencia[0]
            if isinstance(df_final_teams_tenencia.columns, pd.MultiIndex):
                df_final_teams_tenencia.columns = df_final_teams_tenencia.columns.droplevel(0)
            
            # Si la cantidad de IDs coincide con las filas de la tabla, los acoplamos
            if len(ids_equipos_teams_tenencia) == len(df_final_teams_tenencia):
                df_final_teams_tenencia['Team_ID'] = ids_equipos_teams_tenencia
                
            tabla_teams.append(df_final_teams_tenencia)
        
            
    print("\nUnificando las tablas extraídas...")
    df_final_teams_tenencia = pd.concat(tabla_teams, ignore_index=True)
    df_final_teams_tenencia = df_final_teams_tenencia.drop_duplicates()
    
    nombre_salida = "estadisticas_tenencia_fifa_con_equipos.xlsx"
    #df_final_teams_tenencia.to_excel(nombre_salida, index=False)
    
    print("\n====================================================")
    print(f" 🎉 ¡PROCESO EXITOSO! Archivo guardado: {nombre_salida}")
    print("====================================================")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando el navegador... ")
    driver.quit()

#df_final_teams_tenencia = df_final_teams_tenencia.iloc[: [0,23]] # ojo acá, revisar, traigo id y el primer total

print("====================================================")
print("  INICIANDO Procesamiento y Merge de Jugadores y Equipos")
print("====================================================")

# Obtuvimos variables de ataque del dash de Opta con indice en equipo y jugador 

base_fifa_ataque = df_final.merge( df_final_teams, on = 'Team_ID', how='left').merge( df_final_teams_tenencia, on = 'Team_ID', how='left')

# Generación de tres variables: Incidencia_Jugador, Tiros_Equipo_Promedio y Goles_Equipo_Promedio

base_fifa_ataque ['Tiros_Equipo_Promedio'] = (base_fifa_ataque ['shots_y'] / base_fifa_ataque ['played_x'] *100).round(2)

base_fifa_ataque ['Goles_Equipo_Promedio'] = (base_fifa_ataque ['goals_y'] / base_fifa_ataque ['played_x'] *100).round(2)

base_fifa_ataque ['Incidencia_Jugador'] = (base_fifa_ataque ['goals_x'] / base_fifa_ataque ['goals_y'] *100).round(2)



base_fifa_ataque = base_fifa_ataque [['name_x', 'mins', 'goals_x', 'shots_x', 'conv %_x', 'Incidencia_Jugador', 'name_y', 
                                      'played_x', 'goals_y', 'Goles_Equipo_Promedio', 'shots_y', 'conv %_y', 'total', 
                                      'avg poss', 'Tiros_Equipo_Promedio']]


base_fifa_ataque = base_fifa_ataque.rename (columns = {
    'name_x' : 'Jugador',
    'goals_x' : 'Goles_Jugador',
    'name_y' : 'Equipo',
    'goals_y' : 'Goles_Equipo',
    'mins' : 'Minutos_Jugados',
    'shots_x' : 'Tiros_Jugador',
    'conv %_x' : 'Efectividad_Jugador',
    'played_x' : 'Partidos_Equipo',
    'shots_y' : 'Tiros_Equipo',
    'conv %_y' : 'Efectividad_Equipo',
    'total' : 'Pases_Totales_Equipo',
    'avg poss' : 'Promedio_Tenencia_Equipo'
})

## Corrección de columnas espejadas que en el dash de fuente figuraban con encabezado

base_fifa_columna = base_fifa_ataque['Pases_Totales_Equipo']

base_fifa_columna = pd.DataFrame(base_fifa_columna.values, index=base_fifa_columna.index)

base_fifa_columna = base_fifa_columna[[0]]

base_fifa_columna.rename(columns={0: 'Pases_Totales_Equipo'}, inplace=True)

base_fifa_ataque = base_fifa_ataque.drop(columns=['Pases_Totales_Equipo'])

base_fifa_ataque = pd.concat([base_fifa_ataque, base_fifa_columna], axis=1)


base_fifa_ataque ['Promedio_Pases'] = (base_fifa_ataque ['Pases_Totales_Equipo'] / base_fifa_ataque ['Partidos_Equipo'])



#base_fifa_ataque.to_excel("base_fifa_ataque2.xlsx", index=False)



                                     ## Base de métricas defensiva

print("====================================================")
print("  INICIANDO EXTRACTOR AUTOMATIZADO DE TEAMS defending FIFA WORLD CUP 2026")
print("====================================================")

options_teams_defensa = webdriver.ChromeOptions()
options_teams_defensa.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options_teams_defensa)

tabla_teams_defensa = []

try:
    url = "https://theanalyst.com/competition/fifa-world-cup/stats"
    driver.get(url)
    
    print("Cargando la página web...")
    wait = WebDriverWait(driver, 20)
    
    # 3. Seleccionar 'TEAMS'
    print("Configurando filtro: Seleccionando pestaña 'Teams'...")
    boton_teams = wait.until(EC.element_to_be_clickable((By.ID, "teams")))
    boton_teams.click()
    time.sleep(1.5)

   
    # 4. Abrir menú de categorías
    print("Configurando filtro: Abriendo menú de categorías...")
    desplegable_categoria_teams = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='SelectDropdown-module_react-select']"))
    )
    desplegable_categoria_teams.click()
    time.sleep(0.5)
    

    
    # 5. Seleccionar 'defending'
    print("Configurando filtro: Seleccionando 'defending'...")
    opcion_defending_teams = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'SelectDropdown-module_react-select__option') and contains(text(), 'Defending')]"))
    )
    driver.execute_script("arguments[0].click();", opcion_defending_teams)
    
    print("Esperando a que la tabla cargue las métricas de defensa...")
    time.sleep(3)
    
        
    html_actual_teams = driver.page_source
        
        # --- NUEVA SECCIÓN: EXTRACCIÓN DE BANDERA/LOGOS CON BEAUTIFULSOUP ---
    soup_teams_defensa = BeautifulSoup(html_actual_teams, 'lxml')
        # Buscamos todas las filas de la tabla (ajustar etiqueta si la estructura varía)
    filas_html = soup_teams_defensa.find_all('tr')
        
    ids_equipos_teams_defensa = []
        # Recorremos las filas para extraer los IDs de las imágenes
    for fila in filas_html:
            # Buscamos si la fila tiene un encabezado (th) en lugar de datos (td) para ignorarla
            if fila.find('th'):
                continue
                
            img = fila.find('img')
            if img and 'id=' in img.get('src', ''):
                # Cortamos la URL para quedarnos solo con el código final del ID
                team_id = img['src'].split('id=')[-1]
                ids_equipos_teams_defensa.append(team_id)
            else:
                ids_equipos_teams_defensa.append("N/A")
        # -------------------------------------------------------------------
        
        # Extraemos la tabla numérica con Pandas de forma normal
    tablas_actuales_teams = pd.read_html(StringIO(html_actual_teams))
        
    if tablas_actuales_teams:
            df_final_teams_defensa = tablas_actuales_teams[0]
            if isinstance(df_final_teams_defensa.columns, pd.MultiIndex):
                df_final_teams_defensa.columns = df_final_teams_defensa.columns.droplevel(0)
            
            # Si la cantidad de IDs coincide con las filas de la tabla, los acoplamos
            if len(ids_equipos_teams_defensa) == len(df_final_teams_defensa):
                df_final_teams_defensa['Team_ID'] = ids_equipos_teams_defensa
                
            tabla_teams_defensa.append(df_final_teams_defensa)
        
            
    print("\nUnificando las tablas extraídas...")
    df_final_teams_defensa = pd.concat(tabla_teams_defensa, ignore_index=True)
    df_final_teams_defensa = df_final_teams_defensa.drop_duplicates()
    
    nombre_salida = "estadisticas_defensa_fifa_con_equipos.xlsx"
    #df_final_teams_defensa.to_excel(nombre_salida, index=False)
    
    print("\n====================================================")
    print(f" 🎉 ¡PROCESO EXITOSO! Archivo guardado: {nombre_salida}")
    print("====================================================")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando el navegador... ")
    driver.quit()

df_final_teams_defensa = df_final_teams_defensa [['name', 'played', 'goals', 'xg', 'goals vs xg', 'sot', 'Team_ID']]
# campos: NAME, played goals (goles recibidos), xg (Goles Potenciales), goals vs xg (goles reales vs goles potenciales), sot (tiros al arco) + 

df_final_teams_defensa  = df_final_teams_defensa. rename (columns = {
     'name' : 'Equipo',
    'played' : 'Partidos_Jugados',
    'goals' : 'Goles_Recibidos',
    'xg' : 'Goles_Potenciales',
    'goals vs xg' : 'Goles_Reales_vs_Potenciales',
    'sot' : 'Tiros_Al_Arco'
})


#df_final_teams_defensa.to_excel("prueba_defensa.xlsx", index=False)

print("====================================================")
print("  INICIANDO EXTRACTOR AUTOMATIZADO DE TEAMS PRESIÓN FIFA WORLD CUP 2026")
print("====================================================")

options_teams_defensa = webdriver.ChromeOptions()
options_teams_defensa.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options_teams_defensa)

tabla_teams_press = []

try:
    url = "https://theanalyst.com/competition/fifa-world-cup/stats"
    driver.get(url)
    
    print("Cargando la página web...")
    wait = WebDriverWait(driver, 20)
    
    # 3. Seleccionar 'TEAMS'
    print("Configurando filtro: Seleccionando pestaña 'Teams'...")
    boton_teams = wait.until(EC.element_to_be_clickable((By.ID, "teams")))
    boton_teams.click()
    time.sleep(1.5)

   
    # 4. Abrir menú de categorías
    print("Configurando filtro: Abriendo menú de categorías...")
    desplegable_categoria_teams = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='SelectDropdown-module_react-select']"))
    )
    desplegable_categoria_teams.click()
    time.sleep(0.5)
    

    
    # 5. Seleccionar 'pressing'
    print("Configurando filtro: Seleccionando 'pressing'...")
    opcion_pressing_teams = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'SelectDropdown-module_react-select__option') and contains(text(), 'Pressing')]"))
    )
    driver.execute_script("arguments[0].click();", opcion_pressing_teams)
    
    print("Esperando a que la tabla cargue las métricas de defensa...")
    time.sleep(3)
    
        
    html_actual_teams = driver.page_source
        
        # --- NUEVA SECCIÓN: EXTRACCIÓN DE BANDERA/LOGOS CON BEAUTIFULSOUP ---
    soup_teams_press = BeautifulSoup(html_actual_teams, 'lxml')
        # Buscamos todas las filas de la tabla (ajustar etiqueta si la estructura varía)
    filas_html = soup_teams_press.find_all('tr')
        
    ids_equipos_teams_press = []
        # Recorremos las filas para extraer los IDs de las imágenes
    for fila in filas_html:
            # Buscamos si la fila tiene un encabezado (th) en lugar de datos (td) para ignorarla
            if fila.find('th'):
                continue
                
            img = fila.find('img')
            if img and 'id=' in img.get('src', ''):
                # Cortamos la URL para quedarnos solo con el código final del ID
                team_id = img['src'].split('id=')[-1]
                ids_equipos_teams_press.append(team_id)
            else:
                ids_equipos_teams_press.append("N/A")
        # -------------------------------------------------------------------
        
        # Extraemos la tabla numérica con Pandas de forma normal
    tablas_actuales_teams = pd.read_html(StringIO(html_actual_teams))
        
    if tablas_actuales_teams:
            df_final_teams_press = tablas_actuales_teams[0]
            if isinstance(df_final_teams_press.columns, pd.MultiIndex):
                df_final_teams_press.columns = df_final_teams_press.columns.droplevel(0)
            
            # Si la cantidad de IDs coincide con las filas de la tabla, los acoplamos
            if len(ids_equipos_teams_press) == len(df_final_teams_press):
                df_final_teams_press['Team_ID'] = ids_equipos_teams_press
                
            tabla_teams_press.append(df_final_teams_press)
        
            
    print("\nUnificando las tablas extraídas...")
    df_final_teams_press = pd.concat(tabla_teams_press, ignore_index=True)
    df_final_teams_press = df_final_teams_press.drop_duplicates()
    
    nombre_salida = "estadisticas_press_fifa_con_equipos.xlsx"
    #df_final_teams_press.to_excel(nombre_salida, index=False)
    
    print("\n====================================================")
    print(f" 🎉 ¡PROCESO EXITOSO! Archivo guardado: {nombre_salida}")
    print("====================================================")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando el navegador... ")
    driver.quit()

df_final_teams_press  = df_final_teams_press [['start distance (m)', 'total' , 'Team_ID']]

df_final_teams_press  =  df_final_teams_press .rename (columns = {
          'start distance (m)': 'Zona_Recuperación (m)',
            'total' : 'Recuperación_Alta (65m)',
     })
    
# Generamos una variable ordinal de acuerdo a la presión en donde recupera la pelota el equipo

limites = [0, 36, 40.9, 46.9, 120]

etiquetas = ['Baja', 'Media_baja', 'Media', 'Media_Alta']

df_final_teams_press['Zona_Recuperación'] = pd.cut(df_final_teams_press['Zona_Recuperación (m)'], 
                                                   bins=limites, 
                                                   labels=etiquetas, 
                                                   include_lowest=True,  # Incluye el límite inferior del primer intervalo (0)
                                                     ordered=True)

#df_final_teams_press.to_excel("prueba_press.xlsx", index=False)

print("====================================================")
print("  INICIANDO EXTRACTOR AUTOMATIZADO DE PLAYERS DEFENSA FIFA WORLD CUP 2026")
print("====================================================")

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

try:
    url = "https://theanalyst.com/competition/fifa-world-cup/stats"
    driver.get(url)
    
    print("Cargando la página web...")
    wait = WebDriverWait(driver, 20)
    
    # 3. Seleccionar 'Players'
    print("Configurando filtro: Seleccionando pestaña 'Players'...")
    boton_players_def = wait.until(EC.element_to_be_clickable((By.ID, "players")))
    boton_players_def.click()
    time.sleep(1.5)
    
    # 4. Abrir menú de categorías
    print("Configurando filtro: Abriendo menú de categorías...")
    desplegable_categoria = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[class*='SelectDropdown-module_react-select']"))
    )
    desplegable_categoria.click()
    time.sleep(0.5)
    
    # 5. Seleccionar 'Defending'
    print("Configurando filtro: Seleccionando 'Defending'...")
    opcion_defending = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'SelectDropdown-module_react-select__option') and contains(text(), 'Defending')]"))
    )
    driver.execute_script("arguments[0].click();", opcion_defending)
    
    print("Esperando a que la tabla cargue las métricas de defensa por jugador...")
    time.sleep(3)
    
    todas_las_paginas_defensa = []
    total_paginas = 14
    
    print("\nArrancando la extracción cíclica de datos...")
    for pagina in range(1, total_paginas + 1):
        print(f" -> Procesando página {pagina} de {total_paginas}...")
        time.sleep(2)
        
        html_actual = driver.page_source
        
        # --- NUEVA SECCIÓN: EXTRACCIÓN DE BANDERA/LOGOS CON BEAUTIFULSOUP ---
        soup = BeautifulSoup(html_actual, 'lxml')
        # Buscamos todas las filas de la tabla (ajustar etiqueta si la estructura varía)
        filas_html = soup.find_all('tr')
        
        ids_equipos = []
        # Recorremos las filas para extraer los IDs de las imágenes
        for fila in filas_html:
            # Buscamos si la fila tiene un encabezado (th) en lugar de datos (td) para ignorarla
            if fila.find('th'):
                continue
                
            img = fila.find('img')
            if img and 'id=' in img.get('src', ''):
                # Cortamos la URL para quedarnos solo con el código final del ID
                team_id = img['src'].split('id=')[-1]
                ids_equipos.append(team_id)
            else:
                ids_equipos.append("N/A")
        # -------------------------------------------------------------------
        
        # Extraemos la tabla numérica con Pandas de forma normal
        tablas_actuales = pd.read_html(StringIO(html_actual))
        
        if tablas_actuales:
            df_pagina = tablas_actuales[0]
            if isinstance(df_pagina.columns, pd.MultiIndex):
                df_pagina.columns = df_pagina.columns.droplevel(0)
            
            # Si la cantidad de IDs coincide con las filas de la tabla, los acoplamos
            if len(ids_equipos) == len(df_pagina):
                df_pagina['Team_ID'] = ids_equipos
                
            todas_las_paginas_defensa.append(df_pagina)
        
        if pagina < total_paginas:
            boton_siguiente = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='>']")))
            driver.execute_script("arguments[0].click();", boton_siguiente)
            
    print("\nUnificando las tablas extraídas...")
    df_final_defensa = pd.concat(todas_las_paginas_defensa, ignore_index=True)
    df_final_defensa = df_final_defensa.drop_duplicates()
    
    nombre_salida = "estadisticas_defensa_fifa_con_jugadores.xlsx"
    #df_final.to_excel(nombre_salida, index=False)
    
    print("\n====================================================")
    print(f" 🎉 ¡PROCESO EXITOSO! Archivo guardado: {nombre_salida}")
    print("====================================================")

except Exception as e:
    print(f"\n❌ Ocurrió un error inesperado: {e}")

finally:
    print("Cerrando el navegador... ")
    driver.quit()


df_final_defensa = df_final_defensa.loc[:, [df_final_defensa.columns[8], df_final_defensa.columns[10], 'name','Team_ID', 'pos won']]

base_fifa_defensa = df_final_defensa.merge( df_final_teams_press, on = 'Team_ID', how='left').merge( df_final_teams_defensa, on = 'Team_ID', how='left')

#indice_eliminar = [1, 3, 5]

#base_fifa_defensa = base_fifa_defensa.drop(base_fifa_defensa.columns[indice_eliminar], axis=1)

base_fifa_defensa = base_fifa_defensa.rename(columns={
    'name': 'Jugador',
    'pos won': 'Recuperaciones_Jugador',
    'Zona_Recuperación (m)': 'Zona_Recuperación_m_Equipo',
    'Recuperación_Alta (65m)': 'Recuperación_Alta_65m_Equipo',
    'Partidos_Jugados': 'Partidos_Jugados_Equipo'
})

nuevo_orden = [4, 10, 5, 0, 1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 14, 15]

base_fifa_defensa = base_fifa_defensa.iloc [:, nuevo_orden]

# Agregación de campos : promedio tiros y goles recibidos

base_fifa_defensa ['Tiros_Al_Arco_Promedio'] = (base_fifa_defensa ['Tiros_Al_Arco'] / base_fifa_defensa ['Partidos_Jugados_Equipo'] ).round(2)

base_fifa_defensa ['Goles_Recibidos_Promedio'] = (base_fifa_defensa ['Goles_Recibidos'] / base_fifa_defensa ['Partidos_Jugados_Equipo'] ).round(2)


base_fifa_defensa.to_excel("base_defensa.xlsx", index=False)


print("====================================================")
print("  INICIANDO CREACIÓN DE INDICE DE EFICIENCIA DE DOMINIO")
print("====================================================")

## Creación de indicador INDICE DE EFICIENCIA DE DOMINIOA (IED) evalúa el rendimiento integral de un equipo teniendo en cuenta
## fase ataque y variables defensivas. El indicador mide cuán eficiente es un equipo en base a la posesión de la pelota,
## eficiencia ofensiva y penaliza a los equipos que tienen diferencia de gol negativa. 

# Previo normalizo las columnas extraídas como % del tipo 50.0%, ellas son : 'Promedio_Tenencia_Equipo', 'Efectividad_Equipo', 'Efectividad_Jugador'

if base_fifa_ataque['Promedio_Tenencia_Equipo'].dtype == 'object':
    base_fifa_ataque['Promedio_Tenencia_Equipo'] = base_fifa_ataque['Promedio_Tenencia_Equipo'].str.replace('%', '').astype(float) / 100
else:
    # Si ya era numérica pero en escala 0-100
    base_fifa_ataque['Promedio_Tenencia_Equipo'] = base_fifa_ataque['Promedio_Tenencia_Equipo'] / 100



def calcular_ied_agregado(row):
    pos = row['Promedio_Tenencia_Equipo'] 
    tf, tc = row['Tiros_Equipo_Promedio'], row['Tiros_Al_Arco_Promedio']
    gf, gc = row['Goles_Equipo_Promedio'], row['Goles_Recibidos_Promedio']
    pj = row['Partidos_Equipo']
    
    # 1. Base Normalizada
    ied_base = (pos * ((tf + 1) / (tc + 1)) * ((gf + 1) / (gc + 1))) * 2
    
    # 2. Factor de Penalización Dinámico por Muestra
    if gf < gc and pj > 0:
       fp = np.exp(-(gc - gf) / pj)
    else:
        fp = 1.0
        
    return round(ied_base * fp, 2)

# pasos a seguir, hago un merge entre df defensa y df ataque, activo la función, extraigo luego la función y un id y hago join con ataque

fusion_provisoria = pd.merge(base_fifa_ataque, base_fifa_defensa, on='Equipo', how='left')

fusion_provisoria['IED_Final'] = fusion_provisoria.apply(calcular_ied_agregado, axis=1)


# Creamos un DF ultra limpio que solo tiene el ID y el nuevo KPI
df_ied_limpio = fusion_provisoria[['Equipo', 'IED_Final']].drop_duplicates(subset=['Equipo']).copy()


base_fifa_ataque = pd.merge(base_fifa_ataque, df_ied_limpio, on='Equipo', how='left')

#Normalización de los valores de IED y generación de variable con etiquetado para comprender el sentido de IED

min_ied = base_fifa_ataque['IED_Final'].min()
max_ied = base_fifa_ataque['IED_Final'].max()

# escalamos a base 100

base_fifa_ataque['IED_Centil'] = ((base_fifa_ataque['IED_Final'] - min_ied) / (max_ied - min_ied)) * 100

# funcion para etiquetas de 0 a 100
def etiquetar_ied_cien(nota):   # revisar etiquetas convenientes
    if pd.isna(nota): return "Sin Datos"
    elif nota >= 45:  return "Dominio Sostenido" 
    elif 13 <= nota < 45: return "Rendimiento Eficiente"
    elif 2 <= nota < 13: return "Zona de Paridad"
    elif 1 <= nota < 2: return "Ineficacia Táctica"
    else:                 return "Colapso Táctico"

base_fifa_ataque['IED_Rendimiento'] = base_fifa_ataque['IED_Centil'].apply(etiquetar_ied_cien)

#Descarga
base_fifa_ataque.to_excel("base_ataque.xlsx", index=False)