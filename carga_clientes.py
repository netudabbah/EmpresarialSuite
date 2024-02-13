"""
Interactua con clientes.csv, carga nuevos clientes y modifica datos 

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
    lista_entera, solo_clientes =  activador(df)
    while True:
        i = input(
"1. Ver/Modificar lista de clientes\n" 
"2. Finalizar programa\n"
"Indique número: ").strip()              
        if i == "1":
            if not df.empty:
                print("\nLista actual:\n", tabulate(lista_entera, headers="keys", tablefmt="fancy_grid", showindex=False), sep="")
                while True:
                    que_hacer = input("Desea modificar algo de la lista?\n1. Si\n2. No\nIndique número: ").strip()
                    if que_hacer == "1":
                        modificar_lista(df, solo_clientes)
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
                        nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones = pedir_cliente(solo_clientes)
                        agregar_cliente(df, nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones)
                        mostrar_lista(lista_entera)
                        break
                    elif x == "2":
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

def activador(df):
    lista_entera = df.loc[:]
    solo_clientes = df.loc[:, ["Cliente"]].values
    return lista_entera, solo_clientes

def pedir_cliente(solo_clientes): # pide nuevo cliente
    print("\n\033[92mNUEVO CLIENTE\033[0m\n")
    while True:
        nnombre = input("Nombre del cliente: ").title().strip()
        if nnombre == "":
            print("\n\033[91mERROR\033[0m: Ponga un nombre válido\n")
            continue
        if nnombre in solo_clientes:
            esta = input(f"""
\033[91mATENCIÓN\033[0m
{nnombre} ya está en la lista.
1. Para modificar el existente.
2. Para ir al menu inicial.
Para finalizar, cualquier otra tecla.

Número: """
).strip()
            if esta == "1":
                modificar_cliente(df, nnombre)
                break
            elif esta == "2":
                main() 
                break  
            else:
                print("Se canceló la operación.")
                return None
        while True:
            razon_social = input("Razon social: ").title().strip()
            if razon_social == "":
                print("\033[91mERROR\033[0m: Indique una razon social válida.")
                continue
            break
        cuenta_corriente = 0
        observaciones = input("Escriba observaciones si las hay, si no, enter: ")
        if observaciones == "":
            observaciones = "---"
        ultima_compra = "---"
        return nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones
    
def agregar_cliente(df, nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones=None):
    data = pd.DataFrame([[nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones]],
                        columns=["Cliente", "Razon social", "Cuenta corriente", "Ultima compra", "Observaciones"])

    combino = pd.concat([df, data], ignore_index=True)

    combino.to_csv("clientes.csv", index=False)

def modificar_lista(df, solo_clientes): # igual
    print("\n\033[92mSección: Modificar lista de clientes\033[0m")
    while True:
        s = input("""
1. Agregar cliente
2. Modificar existente
3. Finalizar programa
Indique número: """
    ).strip()
        if s == "1":
            nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones = pedir_cliente(solo_clientes)
            agregar_cliente(df, nnombre, razon_social, cuenta_corriente, ultima_compra, observaciones)
            lista_entera, _ = activador(df)
            mostrar_lista(lista_entera)
        elif s == "2":
            modificar_cliente(df)
       
        elif s == "3":
                print("✅ Operación finalizada con éxito")    

        else:
            print("\n\033[91mERROR\033[0m: Indique una opción válida.")
            continue
        break


def modificar_cliente(df, cliente=None): # igual
    _, solo_clientes =  activador(df)
    while True:
        if cliente is None:
            cliente = input("\nIndique el cliente que quiere modificar: ").strip().title()
            if cliente not in solo_clientes: # chequeo que sea un producto existente
                print("\n\033[91mERROR\033[0m: Escriba un cliente de la lista")
                cliente = None
                continue
        while True:
            x = input(
                """
1) Editar nombre cliente
2) Editar razón social
3) Eliminar cliente
4) Editar observación
5) Finalizar programa
\nIndique número: """
).strip()
            if x == "1":
                cambiar_nombre(df, cliente)                  
                break
            
            elif x == "2":
                cambiar_r_social(df, cliente)
                break

            elif x == "3":
                eliminar(df, cliente)            
                break

            elif x == "4": 
                editar_observacion(df, cliente)
                break
            
            elif x == "5":
                break

            else:
                print("\n\033[91mERROR\033[0m: Elija una de las opciones. Solo numeros.")
                continue
        break


def cambiar_nombre(df, cliente): # igual
    print("\n\033[92mSección\033[0m: editar nombre del cliente\n")
    while True:
        cliente_nuevo = input("Nuevo nombre: ").title().strip()
        if cliente_nuevo == "":
            print("\n\033[91mERROR\033[0m: Escriba un nombre válido")
            continue
        break
    if cliente_nuevo != cliente:
            df.loc[df["Cliente"] == cliente, "Cliente"] = cliente_nuevo
            df.to_csv("clientes.csv", index=False)
    else: 
        print("\033[93mAtención\033[0m: El nombre insertado es igual al antiguo, por lo tanto no habrá un cambio efectuado")
    lista_entera, _ = activador(df) # para actualizar la lista y poder mostrarla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    

def cambiar_r_social(df, cliente): # igual
    print("\n\033[92mSección\033[0m: editar razón social\n")
    while True:
        r_social = input("Nueva razón social: ").title().strip()
        if r_social == "":
            print("\n\033[91mERROR\033[0m: Nombre inválido, reintente")
            continue
        break
    df.loc[df["Cliente"] == cliente, "Razon social"] = r_social
    df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador(df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
    

def eliminar(df, cliente): # igual 
    print("\n\033[92mSección\033[0m: eliminar articulo\n")
    i = input("Presione 1 para confirmar elección, tenga en cuenta que no hay vuelta atrás: ").strip()
    if i == "1":
        df = df[df["Cliente"] != cliente]
        df.to_csv("clientes.csv", index=False)    
        lista_entera, _ = activador(df) # para actualizar la lista y poder escribirla
        mostrar_lista(lista_entera) 
        print("✅ Operación exitosa. Que andes bien. ")
    else:
        print("✅ Se canceló la eliminación.")
    


def editar_observacion(df, cliente): # igual
    print("\n\033[92mSección\033[0m: Editar observación del cliente\n")
    obs = input("Nueva observación (enter para eliminar la actual): ")
    if obs == "":
        df.loc[df["Cliente"] == cliente, "Observaciones"] = "---"
    else: 
        df.loc[df["Cliente"] == cliente, "Observaciones"] = obs
    df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador(df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")
 


def mostrar_lista(lista_entera):
    df = pd.read_csv("clientes.csv")
    lista_entera, _ = activador(df)
    print(f"Lista actual:\n{tabulate(lista_entera, headers='keys', tablefmt='fancy_grid', showindex=False)}")


if __name__ == "__main__":
    main()