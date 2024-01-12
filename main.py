from tabulate import tabulate 
import pandas as pd 
import csv 
import os.path

print("°°°Bienvenido a empresa fantasma 123.")

def main():
    if os.path.isfile("./productos.csv"): # Si existe el programa, con los headers incluidos
        df = pd.read_csv("productos.csv") # Nada mas hay a hacerlo dataframe 

    else: # pero si no existe aún
        with open("productos.csv", "w", newline="") as file: # lo creamos con los headers
            writer = csv.writer(file)
            writer.writerow(["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"])
        df = pd.read_csv("productos.csv")
    lista_entera, _ =  activador()
    while True:
        i = input(
"1. Ver/Modificar lista de productos\n" 
"2. Finalizar programa\n"
"Indique número: ").strip()              
        if i == "1":
            if not df.empty:
                print("\nLista actual:\n", tabulate(lista_entera, headers="keys", tablefmt="fancy_grid"), sep="")
                while True:
                    que_hacer = input("Desea modificar algo de la lista?\n1. Si\n2. No\nIndique número: ").strip()
                    if que_hacer == "1":
                        modificar_lista()
                        break
                    elif que_hacer == "2":
                        print("Programa finalizado con éxito.")
                        break
                    else: 
                        print("\n\033[91mERROR\033[0m: Indique una de las opciones.")
                        continue
            else:
                print("\nLa lista está vacía aún\n")
                x = input("1. Para agregar un producto \n2. Para salir\nIndique número: ").strip()
                if x == "1":
                    agregar_producto()
                    break
                else:
                    print("Programa finalizado sin cambios.")
                    break
            
        elif i == "2":
            print("Programa finalizado con éxito. ")
        
        else:
            print("\n\033[91mERROR\033[0m: Indique una de las opciones.\n")
            continue
        break

def activador():
    solo_articulos = []
    lista_entera = []
    with open("productos.csv", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i in reader:
            # Para poder verificar q el articulo a modificar exista                 
            solo_articulos.append(i['Articulo'])
            # Para mostrar el csv, lo hago lista
            lista_entera.append(i) 
    return lista_entera, solo_articulos

def agregar_producto():
    lista_entera, solo_articulos = activador()
    while True:
        nnombre = input("Nombre del articulo: ").capitalize().strip()
        if nnombre == "":
            print("\n\033[91mERROR\033[0m: Ponga un nombre válido")
            continue
        if nnombre in solo_articulos:
            esta = input(f"""
\n\033[91mATENCIÓN\033[0m
{nnombre} ya está en la lista.
Para modificar el existente, oprima 1.
Para salir, oprima cualquier otra tecla
número: """
).strip()
            if esta == "1":
                modificar_producto()
                break
            else:
                print("Se canceló la operación.")
                break
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
        with open("productos.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([nnombre, cantidad, costo, precio_final, observaciones])
        lista_entera, solo_articulos = activador()
        mostrar_lista(lista_entera)
        print("✅ Operación exitosa, good evening")
        volver()
        break


def modificar_lista():
    global df 
    while True:
        s = input("""\n
1. Agregar producto
2. Modificar existente
3. Finalizar programa
Indique número: """
    ).strip()
        if s not in ["1", "2", "3"]:
            print("\n\033[91mERROR\033[0m: Indique una opción válida.")
            continue
        break

    if s == "1":
        # AGREGA PRODUCTO NUEVO
        agregar_producto()

    elif s == "2":
        modificar_producto()
    elif s == "3":
            print("✅ Operación finalizada con éxito")    
        

def modificar_producto():
    _ , solo_articulos =  activador()
    # MODIFICAR EXISTENTE
    if not df.empty: # Si no esta vacío
        while True:
            articulo = input("\nIndique el artículo que quiere modificar (escriba salir si no es necesario): ").strip().capitalize()
            if "salir" in articulo.lower():
                print("Operación finalizada con \033[92méxito\033[0m")
                break 
            if articulo not in solo_articulos: # chequeo que sea un producto existente
                print("\n\033[91mERROR\033[0m: Escriba un producto de la lista")
                continue
            while True:
                x = input(
                """
1) Cambiar nombre articulo
2) Cambiar cantidad
3) Cambiar costo
4) Editar precio final
5) Eliminar producto
6) Editar observación
7) Finalizar programa
\nIndique número: """
).strip()
                if x == "1":
                    cambiar_nombre(articulo)
                    break
                
                elif x == "2":
                    cambiar_cantidad(articulo)
                    break

                elif x == "3":
                    cambiar_costo(articulo)
                    break
                
                elif x == "4":
                    editar_precio(articulo)
                    break                

                elif x == "5":
                    eliminar(articulo)            
                    break
                elif x == "6": 
                    editar_observacion(articulo)
                    break
                elif x == "7":
                    break

                else:
                    print("\n\033[91mERROR\033[0m: Elija una de las opciones. Solo numeros.")
                    continue
            break

    else:
        print("\n\033[91mERROR\033[0m: No hay articulos en la lista aún")

def cambiar_nombre(articulo):
    global df 
    while True:
        articulo_nuevo = input("Nuevo nombre: ").capitalize().strip()
        if articulo_nuevo == "":
            print("\n\033[91mERROR\033[0m: Escriba un nombre válido")
            continue
        break
    df.loc[df["Articulo"] == articulo, "Articulo"] = articulo_nuevo
    df.to_csv("productos.csv", index=False)
    lista_entera, solo_articulos = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()


def cambiar_cantidad(articulo):
    global df
    while True:
        try:
            n_cant = int(input("Cantidad nueva: "))
        except ValueError:
            print("\n\033[91mERROR\033[0m: Ingrese un numero válido")
            continue
        break
    df.loc[df["Articulo"] == articulo, "Cantidad"] = n_cant
    df.to_csv("productos.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()


def cambiar_costo(articulo):
    global df 
    while True:
        try:
            n_costo = int(input("Costo nuevo: "))
        except ValueError:
            print("\n\033[91mERROR\033[0m: Ingrese un numero válido")
            continue
        break

    df.loc[df["Articulo"] == articulo, "Costo"] = n_costo
    df.to_csv("productos.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()

def editar_precio(articulo):
    global df
    while True:
        try:
            precio_n = float(input("Nuevo precio: "))
        except ValueError:
            print("\n\033[91mERROR\033[0m: Solo números y puntos admitidos.")
            continue
        break
    df.loc[df["Articulo"] == articulo, "Precio final"] = precio_n
    df.to_csv("productos.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()

def editar_observacion(articulo):
    global df
    obs = input("Nueva observación (enter para eliminar la actual): ")
    df.loc[df["Articulo"] == articulo, "Observaciones"] = obs
    df.to_csv("productos.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()

def eliminar(articulo): # EDITAR EN CASO Q HAYAN DOS CON MISMO NOMBRE 
                        # (POR EJ: DOS COCA PERO UNO EN OBS DICE 1 LT Y EL OTRO DICE LATA)
    global df
    if input("Presione 1 para confirmar elección, tenga en cuenta que no hay vuelta atrás: ").strip() == "1":
        df = df[df["Articulo"] != articulo]
        df.to_csv("productos.csv", index=False)
        lista_entera, _ = activador() # para actualizar la lista y poder escribirla
        mostrar_lista(lista_entera) 
        print("✅ Operación exitosa. Que andes bien. ")
        volver()

    else:
        print("✅ Se canceló la eliminación.")
        volver()


def mostrar_lista(lista_entera):
    print(tabulate(lista_entera, headers="keys", tablefmt="fancy_grid"))

def volver():
    while True:

        x = input(
"\nDesea hacer algo mas?\n"
"Para ir al menú inicial, oprima 1\n"
"Para finalizar, oprima 2\n"
"Su elección: "
).strip()
        if x == "1":
            main()
            break
        elif x == "2":
            break
        else:
            print("ERROR: Indique una de las opciones")
            continue

if __name__ == "__main__":
    main()