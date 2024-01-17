"""
migrar main.py

"""
from tabulate import tabulate 
import pandas as pd 
import csv 
import os.path

if os.path.isfile("./clientes.csv"): #CORRECTO
    df = pd.read_csv("clientes.csv") 

else: # pero si no existe aún
    with open("clientes.csv", "w", newline="") as file: # lo creamos con los headers
        writer = csv.writer(file)
        writer.writerow(["Cliente", "Razon social", "Cuenta corriente", "Ultima compra", "Observaciones"])
df = pd.read_csv("clientes.csv")



print("Bienvenido a empresa fantasma 1234")

def main(): # igual
    print("\n\033[92mHOME\033[0m\n")
    df = pd.read_csv("clientes.csv") 
    lista_entera, _ =  activador()
    while True:
        i = input(
"1. Ver/Modificar lista de clientes\n" 
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
                while True:
                    x = input("1. Para agregar un cliente \n2. Para salir\nIndique número: ").strip()  
                    if x == "1":
                        agregar_cliente()
                        break
                    elif x == 2:
                        print("Programa finalizado sin cambios.")
                        break
                    else:
                        print("\n\033[91mERROR\033[0m: Indique una de las opciones\n")
                        continue
                    
                
        elif i == "2":
            print("Programa finalizado con éxito. ")
        
        else:
            print("\n\033[91mERROR\033[0m: Indique una de las opciones.\n")
            continue
        break

def activador(): # igual
    solo_clientes = []
    lista_entera = []
    with open("clientes.csv", encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i in reader:
            solo_clientes.append(i['Cliente']) # q pasa si tengo un julian de aca y otro de alla?
            lista_entera.append(i) 
    return lista_entera, solo_clientes

def agregar_cliente(): # igual
    lista_entera, solo_clientes = activador()
    while True:
        cliente = input("Nombre del cliente: ").title().strip()
        if cliente == "":
            print("\n\033[91mERROR\033[0m: Ponga un nombre válido")
            continue
        if cliente in solo_clientes:
            esta = input(f"""
\n\033[91mATENCIÓN\033[0m
{cliente} ya está en la lista.
Para modificar el existente, oprima 1.
Para ir al menú inicial, oprima 2
Para finalizar, oprima cualquier otra tecla

Número: """
).strip()
            if esta == "1":
                modificar_cliente()
                break
            elif esta == "2":
                main()
                break
            else:
                print("Se canceló la operación.")
                break
        razon_social = input("Razon social: ").title().strip()
        cuenta_corriente = 0
        observaciones = input("Escriba observaciones si las hay, si no, enter: ")        
        with open("clientes.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([cliente, razon_social, cuenta_corriente, "", observaciones])
        lista_entera, _ = activador()
        mostrar_lista(lista_entera)
        print("✅ Operación exitosa, good evening")
        break


def modificar_lista(): # igual
    global df 
    print("\nMenu:")
    while True:
        s = input("""
1. Agregar cliente
2. Modificar existente
3. Finalizar programa
Indique número: """
    ).strip()
        if s == "1":
            agregar_cliente()

        elif s == "2":
            modificar_cliente()
       
        elif s == "3":
                print("✅ Operación finalizada con éxito")    

        else:
            print("\n\033[91mERROR\033[0m: Indique una opción válida.")
            continue
        break


def modificar_cliente(): # igual
    _, solo_clientes =  activador()
    while True:
        cliente = input("\nIndique el cliente que quiere modificar (escriba salir si no es necesario): ").strip().title()
        if "salir" in cliente.lower():
            print("Operación finalizada con \033[92méxito\033[0m")
            break 
        if cliente not in solo_clientes: # chequeo que sea un producto existente
            print("\n\033[91mERROR\033[0m: Escriba un cliente de la lista")
            continue
        while True:
            x = input(
                """
1) Cambiar nombre cliente
2) Cambiar razón social
3) Eliminar cliente
4) Editar observación
5) Finalizar programa
\nIndique número: """
).strip()
            if x == "1":
                cambiar_nombre(cliente)                  
                break
            
            elif x == "2":
                cambiar_r_social(cliente)
                break

            elif x == "3":
                eliminar(cliente)            
                break

            elif x == "4": 
                editar_observacion(cliente)
                break
            
            elif x == "5":
                break

            else:
                print("\n\033[91mERROR\033[0m: Elija una de las opciones. Solo numeros.")
                continue
        break


def cambiar_nombre(cliente): # igual
    global df 
    print("\n\033[92mSección\033[0m: cambiar nombre del cliente\n")
    while True:
        cliente_nuevo = input("Nuevo nombre: ").title().strip()
        if cliente_nuevo == "":
            print("\n\033[91mERROR\033[0m: Escriba un nombre válido")
            continue
        break
    df.loc[df["Cliente"] == cliente, "Cliente"] = cliente_nuevo
    df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()

def cambiar_r_social(cliente): # igual
    global df
    print("\n\033[92mSección\033[0m: editar razón social\n")
    while True:
        r_social = input("Nueva razón social: ").title().strip()
        if r_social == "":
            print("\n\033[91mERROR\033[0m: Nombre inválido, reintente")
            continue
        break
    df.loc[df["Cliente"] == cliente, "Razon social"] = r_social
    df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    volver()

def eliminar(cliente): # igual
    global df
    print("\n\033[92mSección\033[0m: eliminar articulo\n")
    i = input("Presione 1 para confirmar elección, tenga en cuenta que no hay vuelta atrás: ").strip()
    if i == "1":
        df = df[df["Cliente"] != cliente]
        df.to_csv("clientes.csv", index=False)    
        lista_entera, _ = activador() # para actualizar la lista y poder escribirla
        mostrar_lista(lista_entera) 
        print("✅ Operación exitosa. Que andes bien. ")
    else:
        print("✅ Se canceló la eliminación.")
    volver()


def editar_observacion(cliente): # igual
    global df
    print("\n\033[92mSección\033[0m: cambiar observación del cliente\n")
    obs = input("Nueva observación (enter para eliminar la actual): ")
    if obs == "":
        df.loc[df["Cliente"] == cliente, "Observaciones"] = None
    else: 
        df.loc[df["Cliente"] == cliente, "Observaciones"] = obs
    df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador() # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
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