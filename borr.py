import pandas as pd
from tabulate import tabulate
import os.path

if os.path.isfile("./productos.csv"): # Si existe el programa, con los headers incluidos
    df = pd.read_csv("productos.csv")

else: # Si no existe 
    df = pd.DataFrame(columns=["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"])
    output_file_path = "productos.csv"
    df.to_csv(output_file_path, index=False)


def main():
    print("\033[92mHOME\033[0m")
    df = pd.read_csv("productos.csv")
    lista_entera, solo_articulos = activador(df)
    while True:
        i = input(
"1. Ver/Modificar lista de productos\n" 
"2. Finalizar programa\n"
"Indique número: ").strip()
        chequear_df(df, solo_articulos)
        if i == "1":
            print(tabulate(lista_entera, headers="keys", showindex=False, tablefmt="fancy_grid"))
            while True:
                m = input(
                """
Para editar/agregar
1) Agregar nuevo producto
2) Editar nombre articulo
3) Editar cantidad
4) Editar costo
5) Editar precio
6) Editar observación
7) Eliminar producto
8) Finalizar programa

Su elección: """
).strip()
                try:   
                    if m == "1":
                        nnombre, cantidad, costo, precio_final, observaciones = pedir_producto(solo_articulos)
                        agregar_producto(df, nnombre, cantidad, costo, precio_final, observaciones)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break
                    
                    elif int(m) in range(2,8): # Ahorra el paso de pedirlo en cada caso! 
                        while True:
                            producto = input("Nombre del producto: ").title().strip()
                            if producto not in solo_articulos:
                                print("No esta eso bola")
                                continue
                            break
                    
                    if m == "2":
                        while True:
                            n_nuevo = input("Nombre nuevo: ").title().strip()
                            if n_nuevo == "":
                                print("Introduzca un nombre válido.")
                                continue
                            break
                        editar_nombre(df, producto, n_nuevo)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break

                    elif m == "3":
                        print("Seccion: Editar cantidad")
                        while True:
                            try:
                                n_cant = int(input("Nueva cantidad: "))
                            except ValueError:
                                print("Introduzca un número entero. ")
                            break
                        editar_cantidad(df, producto, n_cant)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break

                    elif m == "4":
                        while True:
                            try:
                                n_costo = float(input("Nuevo costo: "))
                            except ValueError:
                                print(f"Indique numero, con puntos de ser necesario. Valor introducido:{n_costo}")
                                continue
                            break
                        editar_costo(df, producto, n_costo)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break
                    
                    elif m == "5":
                        while True:
                            try:
                                n_precio = float(input("Nuevo precio: "))
                            except ValueError:
                                print("Solo numeros con puntos de ser necesario")
                                continue
                            break
                        editar_precio(df, producto, n_precio)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break
                    
                    elif m == "6":
                        print(producto)
                        n_o = input("Nueva observación (presionando enter elimina la actual si es que hay): ").strip()
                        editar_observacion(df, producto, n_o)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break
                    
                    elif m == "7":
                        eliminar(df, producto)
                        df = pd.read_csv("productos.csv")
                        ifna_fillna(df)
                        lista_entera, solo_articulos = activador(df)
                        break
                    
                    elif m == "8":
                        print("Saliendo")
                        break
                    
                    else:
                        print("Error: Elija una de las opciones dadas.")
                        continue
                except ValueError:
                    print("Please, type in an integer.")
                    continue

                 

        elif i == "2":
            print("Programa finalizado")
            break

        else:
            print("Esriba su eleccion")
            continue
        break
    print(f"Lista actual:\n{tabulate(lista_entera, headers='keys', showindex=False,tablefmt='fancy_grid')}")

def chequear_df(df, solo_articulos):
    if df.empty:
            while True:
                i = input("""
La lista aún está vacia
Desea agregar un producto?
1. Si
2. No
Su elección: """
)
                if i == "1":
                    nnombre, cantidad, costo, precio_final, observaciones = pedir_producto(solo_articulos)
                    agregar_producto(nnombre, cantidad, costo, precio_final, observaciones)
                    df = pd.read_csv("productos.csv")
                    ifna_fillna(df)

def activador(df):
    lista_entera = df.loc[:]
    solo_articulos = df.loc[:, ["Articulo"]].values
    return lista_entera, solo_articulos

def pedir_producto(solo_articulos): # pide nuevo producto
    print("\n\033[92mNUEVO PRODUCTO\033[0m\n")
    while True:
        nnombre = input("Nombre del articulo: ").title().strip()
        if nnombre == "":
            print("\n\033[91mERROR\033[0m: Ponga un nombre válido\n")
            continue
        if nnombre in solo_articulos:
            esta = input(f"""
\033[91mATENCIÓN\033[0m
{nnombre} ya está en la lista.

Para modificar el existente, oprima 1.
Para ir al menu inicial, oprima 2
Para finalizar, cualquier otra tecla

Número: """
).strip()
            if esta == "1":
                print("Modificar")
                break
            elif esta == "2":
                main() 
                break  
            else:
                print("Se canceló la operación.")
                return None

        while True:
            try:
                cantidad = int(input("Cantidad: "))
            except ValueError:
                print("\n\033[91mERROR\033[0m: Solo números admitidos.")
                continue
            break
        while True:
            try:
                costo = float(input("Costo p/u: "))
            except ValueError:
                print("\n\033[91mERROR\033[0m: Solo números y puntos admitidos.")
                continue
            break
        while True:
            try:
                precio_final = float(input("Precio final: "))
            except ValueError:
                print("\n\033[91mERROR\033[0m: Solo números y puntos admitidos.")
                continue
            break
        observaciones = input("Escriba observaciones si las hay, si no, enter: ")
        return nnombre, cantidad, costo, precio_final, observaciones

def agregar_producto(df, nnombre, cantidad, costo, precio_final, observaciones=None):
    data = pd.DataFrame([[nnombre, cantidad, costo, precio_final, observaciones]],
                        columns=["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"])
    
    combino = pd.concat([df, data], ignore_index=True)
    combino.to_csv("productos.csv", index=False)

def ifna_fillna(df):
    if df.loc[:, "Observaciones"].isna().any():
        df.fillna("---", inplace=True)
        df.to_csv("productos.csv", index=False)


def editar_nombre(df, viejo, nuevo):
    print("\n\033[92mSección\033[0m: cambiar nombre del articulo\n")
    df.loc[df["Articulo"] == viejo, "Articulo"] = nuevo
    df.to_csv("productos.csv", index=False)

def editar_cantidad(df, producto, n_cant):
    print("\n\033[92mSección\033[0m: editar cantidad del articulo\n")
    df.loc[df["Articulo"] == producto, "Cantidad"] = n_cant
    df.to_csv("productos.csv", index=False)

def editar_costo(df, producto, n_costo):
    print("\n\033[92mSección\033[0m: editar costo del articulo\n")
    df.loc[df["Articulo"] == producto, "Costo"] = n_costo
    df.to_csv("productos.csv", index=False)

def editar_precio(df, producto, n_precio):
    print("\n\033[92mSección\033[0m: editar precio del articulo\n")
    print(f"Precio actual: {df.loc[df['Articulo'] == producto, 'Costo']}")
    df.loc[df["Articulo"] == producto, "Precio"] = n_precio
    df.to_csv("productos.csv", index=False)

def editar_observacion(df, producto, n_o):
    print("\n\033[92mSección\033[0m: editar observación del articulo\n")
    print(f"Observacion actual: {df.loc[df['Articulo'] == producto, 'Observaciones']}")
    df.loc[df['Articulo'] == producto, 'Observaciones'] = n_o
    df.to_csv("productos.csv", index=False)

def eliminar(df, producto):
    print("\n\033[92mSección\033[0m: eliminar articulo\n")
    if input("Presione 1 para confirmar elección, tenga en cuenta que no hay vuelta atrás: ").strip() == "1":
        df = df[df["Articulo"] != producto]
        df.to_csv("productos.csv", index=False)
    else:
        print("Accion cancelada.")


main()