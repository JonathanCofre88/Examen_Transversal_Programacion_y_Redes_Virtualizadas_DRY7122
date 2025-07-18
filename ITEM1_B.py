#Tipos de VLAN.
vlan = int(input("Número de VLAN: "))

if vlan >= 1 and vlan <= 1005:
    print("Rango normal")
else:
    if vlan >= 1006 and vlan <= 4094:
        print("Rango extendido")
    else:
        print("VLAN no válida")
