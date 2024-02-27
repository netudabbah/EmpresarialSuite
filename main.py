
from tabulate import tabulate
import pandas as pd
import csv
import os.path
import sys
from datetime import date
import warnings
from email.message import EmailMessage
import smtplib
import ssl
from num2words import num2words

warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.*")

print("Bienvenido a la gestión de clientes y productos")

def main():
    if os.path.isfile("./clientes.csv"):
        clientes_df = pd.read_csv("clientes.csv")
    else:
        with open("clientes.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Cliente", "Razon social", "Cuenta corriente", "Ultima compra", "Observaciones"])
        clientes_df = pd.DataFrame(columns=["Cliente", "Razon social", "Cuenta corriente", "Ultima compra", "Observaciones"])

    if os.path.isfile("./productos.csv"):
        articulos_df = pd.read_csv("productos.csv")
    else:
        with open("productos.csv", "w", newline="") as file2:
            writer = csv.writer(file2)
            writer.writerow(["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"])
        articulos_df = pd.DataFrame(columns=["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"])


    while True:
        lista_clientes, solo_clientes = activador_c(clientes_df)
        lista_articulos, solo_articulos = activador_a(articulos_df)        

        print("\n\033[92mHOME\033[0m\n")
        print(
"""              
1. Gestionar clientes (cargar pedidos/pagos, modificar/crear clientes)
2. Gestionar articulos (cargar articulos nuevos, modificar/eliminar existentes)
3. Finalizar programa
"""        
)
        choice = input("\nIndique número: ").strip()
        if choice == "1":
            if not clientes_df.empty:
                gestionar_clientes(lista_clientes, solo_clientes, clientes_df, lista_articulos, solo_articulos, articulos_df)
                break
            else:
                print("\n\033[91mERROR\033[0m: Aún no hay clientes\n")
                while True:
                    i = input("1. Para crear un nuevo cliente\nPresione cualquier otra tecla para salir\nSu eleccion: ").strip()
                    if i == "1":
                        nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones = pedir_cliente(solo_clientes)
                        agregar_cliente(clientes_df, nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones)
                        print("Lista actualizada: ")
                        clientes_df = pd.read_csv("clientes.csv")
                        mostra_c(clientes=clientes_df)
                        break
                    else:
                        print("Sesion finalizada")
                        sys.exit()
            break

        elif choice == "2":
            gestionar_articulos(articulos_df, solo_articulos, lista_articulos)
            break

        elif choice == "3":
            print("Programa finalizado con éxito.")
            break
        else:
            print("\n\033[91mERROR\033[0m: Indique una de las opciones.\n")
            continue

def gestionar_clientes(lista_clientes, solo_clientes, clientes_df, lista_articulos, solo_articulos, articulos_df):
    print("\n\033[92mGestionar clientes\033[0m\n")
    print("\nLista actual:\n", tabulate(lista_clientes, headers="keys", tablefmt="fancy_grid", showindex=False), sep="")
    
    while True: 
        i = input(
"""
1. Para cargar pedidos 
2. Para cargar pagos
3. Para crear un nuevo cliente 
4. Para modificar la lista de clientes
Su eleccion: """

).strip()
        if i in ["1", "2"]: 
            if not articulos_df.empty:
                while True:
                    cliente = input("\nNombre del cliente: ").strip().title()
                    if cliente not in solo_clientes:
                        print("Por favor, indique un cliente válido.")
                        continue
                    break
            else:
                print("\033[91mError\033[0m No hay ningun producto aún")
                p = input(

"""
1. Para agregar un nuevo producto

Enter para finalizar el programa
Eleccion: """
)
                if p == "1":
                    articulo, cantidad, costo, precio_final, observaciones = pedir_articulo()
                    agregar_articulo(articulos_df, articulo, cantidad, costo, precio_final, observaciones)
                    articulos_df = pd.read_csv("productos.csv")
                    mostrar_lista(articulos_df) 
                    break
                else:
                    sys.exit()
        
        if i == "1": # Pedidos
            if not articulos_df.empty:
                while True:
                    print("\nLista actual:\n", tabulate(lista_articulos, headers="keys", tablefmt="fancy_grid", showindex=False), sep="")
                    articulo = input("Articulo que desea comprar: ").strip().title()
                    if articulo not in solo_articulos: 
                        print("Por favor, indique un articulo de la lista")
                        continue
                    elif (articulos_df.loc[articulos_df["Articulo"] == articulo, "Cantidad"] == 0).any():
                        print("Articulo fuera de disponibilidad")
                        while True: 
                            i = input(
                            """
                            1. Para volver a Home
                            2. Para cambiar de cliente o de articulo
                            3. Para finalizar
                            """).strip()

                            if i == "1":
                                print("Volviendo a home")
                                main()
                            elif i == "2":
                                gestionar_clientes(lista_clientes, solo_clientes, clientes_df, lista_articulos, solo_articulos, articulos_df) 
                            elif i == "3": 
                                print("Chau") 
                                sys.exit()

                            break
                    break

                while True:
                    try:
                        cantidad = int(input("Cantidad que desea comprar: "))
                        if (articulos_df.loc[articulos_df["Articulo"] == articulo, "Cantidad"] < cantidad).any():
                            print("Stock insuficiente")
                            continue
                    except ValueError:
                        print("Por favor, inserte un numero entero.")
                        continue
                    break
                cargar_pedido(articulos_df, clientes_df, cliente, articulo, cantidad)

        elif i == "2": # Pagos
            print("\n\033[92mSección cargar pago\n\033[0m")
            cuenta_corriente = clientes_df.loc[clientes_df["Cliente"] == cliente, "Cuenta corriente"].values

            while True:
                if cuenta_corriente > 0:
                    print("Deuda actual:", cuenta_corriente[0])
                try:
                    pago = float(input("Pago: "))
                except ValueError:
                    print("\033[91mERROR\033[0m Especificar pago en números\n")
                    continue
                break
            cargar_pago(cliente, pago, clientes_df)
            cuenta_corriente = clientes_df.loc[clientes_df["Cliente"] == cliente, "Cuenta corriente"].values

            if cuenta_corriente == 0:
                print(f"Cuenta cancelada.")
            elif cuenta_corriente < 0:
                print(f"{round(cuenta_corriente[0], 2)} a favor de {cliente}")
            else:
                print(f"A cuenta: {round(cuenta_corriente[0], 2)}")

        elif i == "3": # Cliente
            nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones = pedir_cliente(solo_clientes)
            agregar_cliente(clientes_df, nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones)
            clientes_df = pd.read_csv("clientes.csv")
            print("Lista de clientes actualizada: ")
            mostra_c(clientes=clientes_df)



        elif i == "4": # Modificar cliente
            while True:
                cliente = input("\nNombre del cliente a modificar: ").strip().title()
                if cliente not in solo_clientes:
                    print("Por favor, indique un cliente válido.")
                    continue
                break
            while True:
                x = input(
"""
1) Editar nombre cliente
2) Editar razón social
3) Eliminar cliente
4) Editar observación
5) Editar numero de teléfono
6) Editar IVA
7) Editar domicilio
8) Editar CUIT
9) Editar mail
10) Finalizar programa 
\nIndique número: """
).strip()
                if x == "1":
                    cambiar_nombre(clientes_df, solo_clientes, cliente)                  
                    break
                
                elif x == "2":
                    cambiar_r_social(clientes_df, cliente)
                    break

                elif x == "3":
                    eliminar(clientes_df, cliente)            
                    break

                elif x == "4": 
                    editar_observacion(clientes_df, cliente)
                    break
                
                elif x == "5":
                    editar_telefono(clientes_df, cliente)
                    break

                elif x == "6": 
                    editar_iva(clientes_df, cliente)
                    break

                elif x == "7":
                    editar_domicilio(clientes_df, cliente)
                    break

                elif x == "8":
                    editar_cuit(clientes_df, cliente)
                    break
                
                elif x == "9":
                    editar_mail(clientes_df, cliente)   
                    break
                elif x == "10":
                    break

                else:
                    print("\n\033[91mERROR\033[0m: Elija una de las opciones. Solo numeros.")
                    continue
        
        else: 
            print("\n\033[91mERROR\033[0m: Indique una opcion valida")
            continue
        break

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
2. Para agregar otro cliente
3. Para ir al menu inicial.
Para finalizar, cualquier otra tecla.

Número: """
).strip()
            if esta == "1":
                print("Modificar cliente")
                break
            elif esta == "2":
                continue
            elif esta == "3":
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
        while True:
            iva = input("Situacion de IVA: ").strip().title()
            if iva == "":
                print("\nIntentelo de nuevo\n")
                continue
            break
        while True:
            domicilio = input("Domicilio: ").strip().title()
            if domicilio == "":
                print("\nIntentelo de nuevo\n")
                continue
            break
        while True:
            cuit = input("Cuit: ").strip()
            if cuit == "":
                print("\nIntentelo de nuevo\n")
                continue
            break
        telefono = input("Telefono: ").strip()
        cuenta_corriente = 0
        observaciones = input("Escriba observaciones si las hay, si no, enter: ")
        if observaciones == "":
            observaciones = "---"
        while True: # agregar regex!!
            mail = input("E-mail del cliente: ").strip()
            if mail == "":
                print("Por favor, indique un mail valido.")
                continue
            break
        ultima_compra = "---"
        return nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones
    
def agregar_cliente(df, nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones=None):
    data = pd.DataFrame([[nnombre, razon_social, cuenta_corriente, ultima_compra, iva, domicilio, cuit, telefono, mail, observaciones]],
                        columns=["Cliente", "Razon social", "Cuenta corriente", "Ultima compra", "IVA", "Domicilio", "CUIT", "Telefono","Mail", "Observaciones"])
    combino = pd.concat([df, data], ignore_index=True)
    combino.to_csv("clientes.csv", index=False)

def cambiar_nombre(clientes_df, solo_clientes, cliente): 
    print("\n\033[92mSección\033[0m: editar nombre del cliente\n")
    while True:
        cliente_nuevo = input("Nuevo nombre: ").title().strip()
        if cliente_nuevo == "":
            print("\n\033[91mERROR\033[0m: Escriba un nombre válido")
            continue
        elif cliente_nuevo in solo_clientes:
            i = input(
f"""
\n\033[91mERROR: Nombre duplicado\033[0m
El nombre que esta intentando poner, ya esta en la lista. 
1. Para guardarlo como '{cliente_nuevo} 2'
2. Para cambiar el nombre manualmente
3. Para salir
Su eleccion: """
).strip()
            if i == "1":
                cliente_nuevo = f"{cliente_nuevo} 2"
            
            elif i == "2":
                continue

        break
    if cliente_nuevo != cliente:
            clientes_df.loc[clientes_df["Cliente"] == cliente, "Cliente"] = cliente_nuevo
            clientes_df.to_csv("clientes.csv", index=False)
    else: 
        print("\033[93mAtención\033[0m: El nombre insertado es igual al antiguo, por lo tanto no habrá un cambio efectuado")
    lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder mostrarla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")

def cambiar_r_social(clientes_df, cliente): 
    print("\n\033[92mSección\033[0m: editar razón social\n")
    while True:
        r_social = input("Nueva razón social: ").title().strip()
        if r_social == "":
            print("\n\033[91mERROR\033[0m: Nombre inválido, reintente")
            continue
        break
    clientes_df.loc[clientes_df["Cliente"] == cliente, "Razon social"] = r_social
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")

def eliminar(clientes_df, cliente):  
    print("\n\033[92mSección\033[0m: eliminar articulo\n")
    i = input("Presione 1 para confirmar elección, tenga en cuenta que no hay vuelta atrás: ").strip()
    if i == "1":
        clientes_df = clientes_df[clientes_df["Cliente"] != cliente]
        clientes_df.to_csv("clientes.csv", index=False)    
        lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder escribirla
        mostrar_lista(lista_entera) 
        print("✅ Operación exitosa. Que andes bien. ")
    else:
        print("✅ Se canceló la eliminación.")

def editar_observacion(clientes_df, cliente): 
    print("\n\033[92mSección\033[0m: Editar observación del cliente\n")
    obs = input("Nueva observación (enter para eliminar la actual): ")
    if obs == "":
        clientes_df.loc[clientes_df["Cliente"] == cliente, "Observaciones"] = "---"
    else: 
        clientes_df.loc[clientes_df["Cliente"] == cliente, "Observaciones"] = obs
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")

def editar_telefono(clientes_df, cliente): 
    print("\n\033[92mSección\033[0m: editar número de teléfono\n")
    while True:
        tel_nuevo = input("Nuevo teléfono: ").title().strip()
        if tel_nuevo == "":
            print("\n\033[91mERROR\033[0m: Número inválido, reintente")
            continue
        break
    clientes_df.loc[clientes_df["Cliente"] == cliente, "Telefono"] = tel_nuevo
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")

def editar_iva(clientes_df, cliente):
    print("\n\033[92mSección\033[0m: editar IVA\n")
    while True:
        iva_nuevo = input("Nuevo IVA: ").title().strip()
        if iva_nuevo == "":
            print("\n\033[91mERROR\033[0m: Reintente")
            continue
        break
    clientes_df.loc[clientes_df["Cliente"] == cliente, "IVA"] = iva_nuevo
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ") 

def editar_domicilio(clientes_df, cliente):
    print("\n\033[92mSección\033[0m: editar domicilio\n")
    while True:
        dom_nuevo = input("Nuevo domicilio: ").title().strip()
        if dom_nuevo == "":
            print("\n\033[91mERROR\033[0m: Reintente")
            continue
        break
    clientes_df.loc[clientes_df["Cliente"] == cliente, "Domicilio"] = dom_nuevo
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) # para actualizar la lista y poder escribirla
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ")   

def editar_cuit(clientes_df, cliente):
    print("\n\033[92mSección\033[0m: editar cuit\n")
    while True:
        cuit_nuevo = input("Nuevo CUIT: ").title().strip()
        if cuit_nuevo == "":
            print("\n\033[91mERROR\033[0m: Reintente")
            continue
        break
    clientes_df.loc[clientes_df["Cliente"] == cliente, "CUIT"] = cuit_nuevo
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) 
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ") 

def editar_mail(clientes_df, cliente):
    print("\n\033[92mSección\033[0m: editar mail\n")
    while True:
        mail_nuevo = input("Nuevo mail: ").title().strip()
        if mail_nuevo == "":
            print("\n\033[91mERROR\033[0m: Reintente")
            continue
        break
    clientes_df.loc[clientes_df["Cliente"] == cliente, "Mail"] = mail_nuevo
    clientes_df.to_csv("clientes.csv", index=False)
    lista_entera, _ = activador_c(clientes_df) 
    mostrar_lista(lista_entera) 
    print("✅ Operación exitosa. Que andes bien. ") 

def mostrar_lista(lista):
    print(tabulate(lista, headers="keys", tablefmt="fancy_grid", showindex=False))

def mostra_c(clientes=None, art=None, pedidos=None):
    if clientes is not None and not clientes.empty:
        df = pd.read_csv("clientes.csv")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    elif art is not None and not art.empty:
        df = pd.read_csv("productos.csv")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    elif pedidos is not None and not pedidos.empty:
        df = pd.read_csv("pedidos.csv")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
    else:
        print("Please specify one df")
          
def cargar_pago(cliente, pago, clientes_df):
        clientes_df.loc[clientes_df["Cliente"] == cliente, "Cuenta corriente"] -= pago
        clientes_df.to_csv("clientes.csv", index=False, float_format="%.2f")
                  
def cargar_pedido(articulos_df, clientes_df, cliente, articulo, cantidad):
    restar_cantidad(articulos_df, articulo, cantidad)
    sumar_a_cuentacorriente(articulos_df, clientes_df, articulo, cantidad, cliente)
    poner_fecha(cliente, clientes_df)
    precio = articulos_df.loc[articulos_df["Articulo"] == articulo, "Precio"].values[0]
    df_pedido = guardar_pedido(cliente, articulo, cantidad)  
    pedido_num = f"pedido-{cliente}-{date.today()}.csv"
    print("Pedido cargado con éxito.")

    i = input(
"""
Desea mandar un recibo por mail?
1. Si
2. No
Indique su elección: """
)
    if i == "1":
        email_sender = "netudabbah@gmail.com"
        email_pass = "dgyd zxlr jnif poxj"
        email_receiver = clientes_df.loc[clientes_df["Cliente"] == cliente, "Mail"].values[0]
        subject = "Pedido Nº 0358. Randerscraw, Inc."
        pedido_data = {'Articulo': [articulo], 'Cantidad': [cantidad], 'Precio': [precio]}
        df_pedido = pd.DataFrame(pedido_data)
        df_pedido.to_csv(pedido_num, index=False)
        body = f"""
Recibo de compra del dia: {date.today()} 

{tabulate(df_pedido, headers="keys", tablefmt="pretty", showindex="never", colalign=("center", "center", "center"))}

Precio final: {precio} ({num2words(precio, lang="es", to='currency', separator=' y', currency='ARS')})
Gracias por comprar en Randerscraw, Inc. 
Facturado por emsuit
"""
        print("Enviando mail...")
        mail(email_sender, email_pass, email_receiver, subject, body)
        print(f"Mail enviado con éxito a: {email_receiver}")
    else:
        print(f"Se guardó sin enviar. El archivo es: {pedido_num}")

def restar_cantidad(articulos_df, articulo, cantidad):
    articulos_df.loc[articulos_df["Articulo"] == articulo, "Cantidad"] -= cantidad
    articulos_df.to_csv("productos.csv", index=False)

def sumar_a_cuentacorriente(articulos_df, clientes_df, articulo, cantidad, cliente):
    total = articulos_df.loc[articulos_df["Articulo"] == articulo, "Precio"] * cantidad
    clientes_df.loc[clientes_df["Cliente"] == cliente, "Cuenta corriente"] += total.values
    clientes_df.to_csv("clientes.csv", index=False)

def poner_fecha(cliente, clientes_df):
    clientes_df.loc[clientes_df["Cliente"] == cliente, "Ultima compra"] = date.today()
    clientes_df.to_csv("clientes.csv", index=False)

def guardar_pedido(cliente, articulo, cantidad):
    pedido_data = {'Cliente': [cliente], 'Articulo': [articulo], 'Cantidad': [cantidad]}
    df_pedido = pd.DataFrame(pedido_data)
    if not os.path.isfile('pedidos.csv'):
        df_pedido.to_csv('pedidos.csv', index=False)
    else:
        df_pedido.to_csv('pedidos.csv', mode='a', header=False, index=False)
    return df_pedido

def gestionar_articulos(articulos_df, solo_articulos, lista_articulos):
    print("\n\033[92mGestionar articulos\033[0m\n")
    if not articulos_df.empty:
        print("\nLista actual:\n", tabulate(lista_articulos, headers="keys", tablefmt="fancy_grid", showindex=False), sep="")
        x = input(
"""
1. Para agregar un nuevo articulo
2. Para modificar un existente
3. Para salir
Su eleccion: """
)
        if x == "1":
            print("\n\033[92mSeccion\033[0m: Nuevo articulo")
            while True:
                articulo = input("Nombre del articulo: ").strip().title()
                if articulo == "":
                    print("Por favor, indique un nombre valido")
                    continue
                if articulo in solo_articulos:
                    esta = input(f"""
\033[91mATENCIÓN\033[0m
{articulo} ya está en la lista.

1. Para modificar el existente
2. Para ir al menu inicial.
Para finalizar, cualquier otra tecla

Número: """
).strip()
                    if esta == "1":
                        modificar_articulo(articulo, articulos_df)
                        break
                    elif esta == "2":
                        main() 
                        break  
                    else:
                        print("Se canceló la operación.")
                        sys.exit()
                else:
                    articulo, cantidad, costo, precio_final, observaciones = pedir_articulo(articulo)
                    agregar_articulo(articulos_df, articulo, cantidad, costo, precio_final, observaciones)
                break

        elif x == "2":
            print("\n\033[92mSeccion\033[0m: Modificar articulo\n")
            while True:
                articulo = input("Articulo: ").strip().title()
                if articulo not in solo_articulos:
                    print("Por favor indicar un articulo de la lista")
                    continue
                break
            modificar_articulo(articulo, articulos_df)
    else:
        while True:
            i = input("""
La lista aún está vacia
Desea agregar un articulo?
1. Si
2. No
Su elección: """
)
            if i == "1":
                articulo, cantidad, costo, precio_final, observaciones = pedir_articulo()
                agregar_articulo(articulos_df, articulo, cantidad, costo, precio_final, observaciones)
                articulos_df = pd.read_csv("productos.csv")
                mostrar_lista(articulos_df)
            else:
                print("Sesion finalizada")
                sys.exit() 
            
            break 

def modificar_articulo(articulo, articulos_df):
    
    n = input(
"""
1. Editar nombre
2. Editar cantidad
3. Editar costo
4. Editar precio
5. Editar observacion
6. Eliminar articulo

Su eleccion: """
).strip()
    if n == "1":
        print("\n\033[92mEditar nombre\033[0m\n")  
        while True:
            nuevo = input("Nuevo nombre: ").strip().title()
            if nuevo == "":
                print("Por favor, indique un nombre valido")
                continue
            break
        editar_nombre_a(articulos_df, articulo, nuevo)
    elif n == "2":
        print("\n\033[92mEditar cantidad\033[0m\n")
        while True:
            try:
                n_cant = int(input("Nueva cantidad: "))
            except ValueError:
                print("Introduzca un número entero. ")
            break
        editar_cantidad(articulos_df, articulo, n_cant)

    elif n == "3":
        print("\n\033[92mEditar costo\033[0m\n")
        while True:
            try:
                n_costo = float(input("Nuevo costo: "))
            except ValueError:
                print(f"Indique numero, con puntos de ser necesario. Valor introducido:{n_costo}")
                continue
            break
        editar_costo(articulos_df, articulo, n_costo)

    elif n == "4":
        print("\n\033[92mEditar precio\033[0m\n")
        while True:
            try:
                n_precio = float(input("Nuevo precio: "))
            except ValueError:
                print("Solo numeros con puntos de ser necesario")
                continue
            break
        editar_precio(articulos_df, articulo, n_precio)

    elif n == "5":
        print("\n\033[92mEditar observacion\033[0m\n")
        observacio_n = input("Nueva observacion (presione enter para borrar la actual, en caso de haber): ").strip().title()
        if observacio_n == "":
            observacio_n = "---"
        editar_observacion_a(articulos_df, articulo, observacio_n)
    
    elif n == "6":
        print("\n\033[92mEliminar articulo\033[0m\n")
        if input("Presione 1 para confirmar elección, tenga en cuenta que no hay vuelta atrás: ").strip() == "1":
            eliminar_a(articulos_df, articulo)
        else:
            print("Accion cancelada")
    
    print("Lista de articulos actualizada: ")
    mostra_c(art=articulos_df)

def editar_nombre_a(articulos_df, viejo, nuevo):
    articulos_df.loc[articulos_df["Articulo"] == viejo, "Articulo"] = nuevo
    articulos_df.to_csv("productos.csv", index=False)

def editar_cantidad(articulos_df, producto, n_cant):
    articulos_df.loc[articulos_df["Articulo"] == producto, "Cantidad"] = n_cant
    articulos_df.to_csv("productos.csv", index=False)

def editar_costo(articulos_df, articulo, n_costo):
    articulos_df.loc[articulos_df["Articulo"] == articulo, "Costo"] = n_costo
    articulos_df.to_csv("productos.csv", index=False)

def editar_precio(articulos_df, articulo, n_precio):
    articulos_df.loc[articulos_df["Articulo"] == articulo, "Precio"] = n_precio
    articulos_df.to_csv("productos.csv", index=False)

def editar_observacion_a(articulos_df, articulo, obs):
    articulos_df.loc[articulos_df['Articulo'] == articulo, 'Observaciones'] = obs
    articulos_df.to_csv("productos.csv", index=False)

def eliminar_a(articulos_df, articulo): 
    articulos_df = articulos_df[articulos_df["Articulo"] != articulo]
    articulos_df.to_csv("productos.csv", index=False)

def pedir_articulo(articulo=None):
    if articulo == None:
        while True:
            articulo = input("Articulo: ").title().strip()
            if articulo == "":
                print("Por favor, indique un nombre valido")
                continue
            break
    
    while True:
        try:
            cantidad = int(input("Cantidad disponible: "))
        except ValueError:
            print("Por favor, indique un numero valido.")
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
    observaciones = input("Observaciones (de no haber, presionar enter): ")
    if observaciones == "":
        observaciones = "---"
    return articulo, cantidad, costo, precio_final, observaciones

def agregar_articulo(articulos_df, articulo, cantidad, costo, precio_final, observaciones):
    data = pd.DataFrame([[articulo, cantidad, costo, precio_final, observaciones]],
                        columns=["Articulo", "Cantidad", "Costo", "Precio", "Observaciones"])
    
    articulos_df_clean = articulos_df.dropna(how='all')

    combino = pd.concat([articulos_df_clean, data], ignore_index=True)
    combino.to_csv("productos.csv", index=False)

def activador_c(df):
    lista_clientes = df.loc[:]
    solo_clientes = df.loc[:, ["Cliente"]].values
    return lista_clientes, solo_clientes

def activador_a(df):
    lista_articulos = df.loc[:]
    solo_articulos = df.loc[:, ["Articulo"]].values
    return lista_articulos, solo_articulos

def mail(email_sender, email_pass, email_receiver, subject, body):
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

if __name__ == "__main__":
    main()