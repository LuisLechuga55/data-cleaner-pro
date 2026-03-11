import pandas as pd

# Creamos datos con errores reales de oficina:
# - Espacios locos
# - Mayúsculas y minúsculas mezcladas
# - Precios con símbolos extraños
# - Duplicados
# - Datos faltantes (NaN)
data = {
    'first_name': [' LUIS', 'MARIA', 'luis', 'JUAN ', 'MARIA', 'Pedro'],
    'last_name': ['lechuga ', ' GARCIA', 'lechuga', ' perez', ' GARCIA', 'Solares'],
    'gender': ['Male', 'Female', 'Male', 'Male', 'Female', 'Male'],
    'price': ['$150.50', '200', '$150.50', '9999.99', '200', 'None'], # El 9999 es la anomalía
    'email': ['LUIS@gmail.com', 'maria@GMAIL.com', 'luis@gmail.com', 'juan@PRO.com', 'maria@GMAIL.com', 'pedro@mail.com']
}

df = pd.DataFrame(data)

# Guardamos el archivo para probar
df.to_excel('PRUEBA_DE_FUEGO.xlsx', index=False)
print("🚀 ¡Archivo 'PRUEBA_DE_FUEGO.xlsx' creado! Súbelo a tu app.")

# . venv/Scripts/activate
# streamlit run app.py