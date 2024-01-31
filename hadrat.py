import pandas as pd
headers = ["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"]

df = pd.DataFrame(columns=headers)

output_file_path = "productos.csv"

df.to_csv(output_file_path, index=False)