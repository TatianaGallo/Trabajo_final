# -*- coding: utf-8 -*-
"""
Created on Tue May 28 20:45:44 2024

@author: tatia
"""


import archivo as arch

# Se inicia sesión en el sistema
arch.gestionar_inicio_sesion()
# Se verifica si la sesión se inició correctamente por medio de la variable global que toma un valor booleano segun lo que corresponde
if arch.sesion_iniciada:
    # Este es el bucle principal del programa
    while True:
        print("\nMENU PRINCIPAL")
        print("-------------------------")
        print("1. Gestionar medicamentos")
        print("2. Gestionar proveedores")
        print("3. Gestionar ubicaciones")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Menú para gestionar medicamentos
            while True:
                print("\nMENU PARA MEDICAMENTOS")
                print("-------------------------")
                print("1. Ingresar un nuevo medicamento")
                print("2. Actualizar la información de un medicamento (con el lote)")
                print("3. Buscar un medicamento (con el lote)")
                print("4. Ver la información de todos los medicamentos almacenados")
                print("5. Eliminar un medicamento (con el lote)")
                print("6. Volver al menú principal")
                opcion1 = input("Seleccione una opción: ")

                if opcion1 == "1":
                    arch.ingresar_medicamento()
                elif opcion1 == "2":
                    arch.actualizar_medicamento()
                elif opcion1 == "3":
                    arch.buscar_medicamento_por_lote()
                elif opcion1 == "4":
                    arch.ver_todos_los_medicamentos()
                elif opcion1 == "5":
                    arch.eliminar_medicamento()
                elif opcion1 == "6":
                    break  # Volver al menú principal
                else:
                    print("Opción no válida. Intente de nuevo.")
        elif opcion == "2":
            # Menú para gestionar proveedores
            while True:
                print("\nMENU PARA PROVEEDORES")
                print("-------------------------")
                print("1. Ingresar un nuevo proveedor")
                print("2. Actualizar la información de un proveedor")
                print("3. Buscar un proveedor (con el codigo)")
                print("4. Ver la información de todos los proveedores")
                print("5. Eliminar un proveedor (con el codigo)")
                print("6. Volver al menú principal")
                opcion2 = input("Seleccione una opción: ")

                if opcion2 == "1":
                    arch.ingresar_proveedor()
                elif opcion2 == "2":
                    arch.actualizar_proveedor()
                elif opcion2 == "3":
                    arch.buscar_proveedor()
                elif opcion2 == "4":
                    arch.ver_proveedores()
                elif opcion2 == "5":
                    arch.eliminar_proveedor()
                elif opcion2 == "6":
                    break  # Volver al menú principal
                else:
                    print("Opción no válida. Intente de nuevo.")
        elif opcion == "3":
            # Menú para gestionar ubicaciones
            while True:
                print("\nMENU PARA UBICACIONES")
                print("-------------------------")
                print("1. Ingresar una nueva ubicación")
                print("2. Actualizar la ubicación de un medicamento")
                print("3. Buscar una ubicación (con el codigo)")
                print("4. Ver la información de todas las ubicaciones")
                print("5. Eliminar una ubicación (con el codigo)")
                print("6. Volver al menú principal")
                opcion3 = input("Seleccione una opción: ")

                if opcion3 == "1":
                    arch.ingresar_ubicacion()
                elif opcion3 == "2":
                    arch.actualizar_ubicacion()
                elif opcion3 == "3":
                    arch.buscar_ubicacion()
                elif opcion3 == "4":
                    arch.ver_ubicaciones()
                elif opcion3 == "5":
                    arch.eliminar_ubicacion()
                elif opcion3 == "6":
                    break  # Volver al menú principal
                else:
                    print("Opción no válida. Intente de nuevo.")
        elif opcion == "4":
            # Sale del programa
            print("Usted a salido del sistema.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
else:
    # Si la sesión no se inició correctamente, se muestra el mensaje y sale del programa.
    print("Inicio de sesión fallido. Saliendo del programa.")



    
    
    
    
    
    
    
    