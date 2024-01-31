import pandas as pd
from datetime import date
from tabulate import tabulate


df_productos = pd.read_csv("productos.csv")

df_clientes = pd.read_csv("clientes.csv")

"""
Esta proxima parte, de complementarse el programa a main,
quedarian en vano ya que ya lo hice allá.
"""

# Busco en el df q sea la columna y me la devuelve como lista, con values para sacar el index
lista_productos = df_productos.loc[:,["Articulo", "Precio"]].values


lista_clientes = df_clientes.loc[:, "Cliente"].values


def main():
    while True:
        cliente = input("Cliente: ").title().strip()
        if cliente not in lista_clientes:
            print("Error: Indique un cliente del sistema")
            continue
        break
    while True:
        i = input( """
Que desea hacer?\n 
1. Para cargar un nuevo pedido
2. Para cargar un nuevo pago
3. Para cambiar de cliente
Indique: """
)
        if i == "1":
            cargar_pedido(cliente)
            break
        elif i == "2":
            cargar_pago(cliente)
        elif i == "3":
            print("\nCambiando de cliente")
            continue
        else:
            print("Indique una respuesta válida.")
            continue
        break


def cargar_pedido(cliente):
    print(f"Sección: Cargar pedido al cliente {cliente}\n")

    print(tabulate(lista_productos, headers=["Articulo", "Precio"]))

    while True:
        compra = input("\nArticulo que compra (de a uno por vez): ").title().strip()
        if compra not in lista_productos:
            print(f"{compra} no es un articulo de la lista")
            continue
        elif (df_productos.loc[df_productos["Articulo"] == compra, "Cantidad"] == 0).any():
            print("No hay disponibilidad")
            x = input("""
Para elegir otro producto, presione 1
Para salir, presione cualquier otra tecla.
Indique: """
)
            if x == "1":
                print("Volviendo a home")
                main()
            else:
                print("Sesión cerrada.") 
                break
        else: # esta en la lista y hay stock     
            while True:
                try:
                    cantidad = int(input(f"Cuantos/as {compra} lleva?: "))
                except ValueError:
                    print("ERROR: Ingrese un número válido")
                    continue
                if (df_productos.loc[df_productos["Articulo"] == compra, "Cantidad"] < cantidad).any():
                    print("Stock insuficiente")
                    continue

                restar_cantidad(compra, cantidad)
                sumar_a_razonsocial(compra, cantidad, cliente)
                poner_fecha(cliente)
                print("Pedido cargado con éxito.")
                break
        break

    

def restar_cantidad(compra, cantidad):
    df_productos.loc[df_productos["Articulo"] == compra, "Cantidad"] -= cantidad
    df_productos.to_csv("productos.csv", index=False)

def sumar_a_razonsocial(compra, cantidad, cliente):
    total = df_productos.loc[df_productos["Articulo"] == compra, "Precio"] * cantidad
    df_clientes.loc[df_clientes["Cliente"] == cliente, "Cuenta corriente"] += total.values
    df_clientes.to_csv("clientes.csv", index=False)

def poner_fecha(cliente):
    df_clientes.loc[df_clientes["Cliente"] == cliente, "Ultima compra"] = date.today()
    df_clientes.to_csv("clientes.csv", index=False)


def cargar_pago(cliente):
    print("Sección cargar pago\n")
    cuenta_corriente = df_clientes.loc[df_clientes["Cliente"] == cliente, "Cuenta corriente"].values
    while True:
        print(f"Deuda actual: {cuenta_corriente[0]}") 
        try:
            pago = float(input("Pago: "))
        except ValueError:
            print("\nEspecificar pago en números\n")
            continue
        break
    df_clientes.loc[df_clientes["Cliente"] == cliente, "Cuenta corriente"] -= pago
    df_clientes.to_csv("clientes.csv", index=False, float_format="%.2f")
    cuenta_corriente = df_clientes.loc[df_clientes["Cliente"] == cliente, "Cuenta corriente"].values
    if cuenta_corriente == 0:
        print(f"Cuenta cancelada. Slds")
    
    elif cuenta_corriente < 0:
        print(f"Cuenta cancelada. Con {round(cuenta_corriente[0], 2)} a favor de {cliente}")

    else:
        print(f"A cuenta: {cuenta_corriente[0]}")

    

main()
