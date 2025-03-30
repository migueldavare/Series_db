# Series_db

### Instrucciones
Descargar el repositorio en VSCode y escribir en el terminal:
<pre>
<code>
    git clone https://github.com/migueldavare/Series_db.git
  </code>
</pre>


Una vez descargado el repositorio se debe instalar el ambiente virtual en VSCode, se deben seguir los siguientes pasos en la terminal:

- Forzar la ejecucion del ambiente virtual 
<code>
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
  </code>

- Crear el ambiente virtual 
  <code>
    python -m venv .venv
  </code>

- Ejecutar el ambiente 
<code>
    .\venv\Scripts\activate
  </code>

Una vez creado el ambiente virtual se debe instalar las librerias con el siguiente comando en la terminal.

<code>
    pip install -r requirements.txt
  </code>

### Ejecución

Una vez instalado el ambiente y librerias se procede a ejecutar el código que extrae los datos desde la API y los almacena en un JSON en la ubicación /src/json_output/output_raw_data.json. 

Para ejecutar el primer código se escribe la siguiente linea de código en el terminal:

<code>
    python .\1_api_extract.py
  </code>

Al terminar aparecerá un mensaje : DataFrame successfully saved to: src/json_output/output_raw_data.json

### profiling

El Archivo que contiene el profiling de los datos se encuentra en src\profiling\profiling.html junto con algunos análisis.

### Datos curados

Los datos curados resultado del paso anterior se encuentran en el path src\data\output_data.parquet

### DB

El archivo de la db en sqllite3 se encuentra en la ubicacion  src\db\sqllite.ipynb

y los pasos para el query en src\db\sql.txt

### Modelo de datos

Los datos curados resultado del paso anterior se encuentran en el path src\model\Modelo_datos.jpg