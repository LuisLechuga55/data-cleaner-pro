import pandas as pd

def mi_primer_limpiador():
    print("🤖: Hola! Estoy leyendo tu archivo de Mockaroo...")
    df = pd.read_excel('datos_sucios.xlsx')

    df = df.drop_duplicates()

    df['first_name'] = df['first_name'].str.title()
    df['last_name'] = df['last_name'].str.title()

    df = df.dropna(subset=['first_name'])

    df.to_excel('DATOS_LIMPIOS_PRO.xlsx', index=False)
    
    print("✅: ¡Terminé! Revisa tu carpeta, creé un archivo llamado DATOS_LIMPIOS_PRO.xlsx")

if __name__ == "__main__":
    mi_primer_limpiador()