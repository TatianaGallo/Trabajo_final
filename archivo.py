# -*- coding: utf-8 -*-
"""
Created on Tue May 28 20:30:45 2024

@author: tatia
"""

# INTEGRANTES DEL GRUPO:
    # VALENTINA RESTREPO
    # JENIFER TATIANA GALLO
    
    
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import errorcode


def conectar():
    """ Esta funcion hace la conexion con la base de datos con los parametros indicados.
    Retorna: 
        conexion: objeto de conexion si la conexion es exitosa.
        None: si ocurre un error en la conexion. """
    
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="informatica1",
            password="bio123",
            database="informatica1"
        )
        if conexion.is_connected():
            return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None

def crear_tablas_y_insertar_datos():
    """ Esta funcion hace la conexion con la base de datos y crea las tablas de:
        
        Medicamentos
        Proveedores
        Ubicaciones
        
        e inserta unos datos iniciales en cada tabla.
        Tiene manejo de errores y de ejecucion en caso de que ocurran
        y manejo de error en caso de que las tablas ya existan en la base de datos """
    
    conexion = conectar()
    if not conexion:
        return

    comando = conexion.cursor()

    try:
        comando.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                codigo INT PRIMARY KEY,
                nombre VARCHAR(100),
                apellido VARCHAR(100),
                documento VARCHAR(20)
            );
        """)
        print("Tabla 'proveedores' creada o ya existe.")
    except mysql.connector.Error as error:
        print(f"Error al crear la tabla 'proveedores': {error}")

    try:
        comando.execute("""
            CREATE TABLE IF NOT EXISTS ubicaciones (
                codigo INT PRIMARY KEY,
                nombre VARCHAR(100),
                telefono VARCHAR(20)
            );
        """)
        print("Tabla 'ubicaciones' creada o ya existe.")
    except mysql.connector.Error as error:
        print(f"Error al crear la tabla 'ubicaciones': {error}")

    try:
        comando.execute("""
            CREATE TABLE IF NOT EXISTS medicamentos (
                lote VARCHAR(50) PRIMARY KEY,
                nombre VARCHAR(100),
                cantidad INT,
                fecha_llegada DATE,
                precio INT,
                codigo_proveedor INT,
                codigo_ubicacion INT,
                FOREIGN KEY (codigo_proveedor) REFERENCES proveedores(codigo),
                FOREIGN KEY (codigo_ubicacion) REFERENCES ubicaciones(codigo)
            );
        """)
        print("Tabla 'medicamentos' creada o ya existe.")
    except mysql.connector.Error as error:
        print(f"Error al crear la tabla 'medicamentos': {error}")

    try:
        comando.execute("""
            INSERT IGNORE INTO proveedores (codigo, nombre, apellido, documento) VALUES
            (101, 'Jorge', 'Camacho', '123456789'),
            (102, 'María', 'Arias', '987654321');
        """)
        conexion.commit()
        print("Datos insertados en 'proveedores'.")
    except mysql.connector.Error as error:
        print(f"Error al insertar datos en 'proveedores': {error}")

    try:
        comando.execute("""
            INSERT IGNORE INTO ubicaciones (codigo, nombre, telefono) VALUES
            (1234, 'Hospital San Vicente', '4441234'),
            (1235, 'Hospital Pablo Tobón Uribe', '4445678');
        """)
        conexion.commit()
        print("Datos insertados en 'ubicaciones'.")
    except mysql.connector.Error as error:
        print(f"Error al insertar datos en 'ubicaciones': {error}")

    try:
        comando.execute("""
            INSERT IGNORE INTO medicamentos (lote, nombre, cantidad, fecha_llegada, precio, codigo_proveedor, codigo_ubicacion) VALUES
            ('L123', 'Paracetamol', 100, '2023-01-01', 1200, 101, 1234),
            ('L124', 'Ibuprofeno', 200, '2023-02-01', 1500, 102, 1235);
        """)
        conexion.commit()
        print("Datos insertados en 'medicamentos'.")
    except mysql.connector.Error as error:
        print(f"Error al insertar datos en 'medicamentos': {error}")

    comando.close()
    conexion.close()

# crear_tablas_y_insertar_datos()
    




def validar_credenciales(usuario, contraseña):
    """ Esta funcion valida las credenciales de un usuario intentando hacer la conexion
    con la bae de datos con los parametros proporcionados.
    
    Argumentos: 
        user: [str] recibe el nombre de usuario de la base de datos
        password: [str] recibe la contraseña de la base de datos
        
    Retorna: 
        True: si las credenciales son validas y se hace la conexion a la base de datos
        False: si las credenciales contienen un error o si no se hace la conexion a la base de datos """
        
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=contraseña,
            database="informatica1"
        )
        if conexion.is_connected():
            conexion.close()
            return True
    except mysql.connector.Error as e:
        print(f"Error al validar credenciales: {e}")
        return False



def gestionar_inicio_sesion():
    """  Esta función muestra una ventana de inicio de sesión para que los usuarios 
    ingresen sus credenciales y accedan al sistema.
    Retorna una interfaz gráfica de usuario para dar la bienvenida e indicar que para acceder debe iniciar sesion. """
    
    ventana_inicio_sesion = tk.Tk()
    ventana_inicio_sesion.title("Bienvenida al Sistema de Gestión de Información")
    ventana_inicio_sesion.geometry("400x200")
    ventana_inicio_sesion.configure(bg="lightblue")

    tk.Label(ventana_inicio_sesion, text="¡Bienvenido al Sistema de Gestión de Información!", bg="lightblue", font=("Arial", 14)).pack(pady=10)
    tk.Label(ventana_inicio_sesion, text="Por favor, inicia sesión para continuar:", bg="lightblue", font=("Arial", 12)).pack()

    boton_iniciar_sesion = tk.Button(ventana_inicio_sesion, text="Iniciar Sesión", command=iniciar_sesion)
    boton_iniciar_sesion.pack(pady=20)

    ventana_inicio_sesion.mainloop()
    

def iniciar_sesion():
    """Esta función crea una ventana de inicio de sesión donde los usuarios
    pueden ingresar su nombre de usuario y contraseña para verificar si son correctos.
    Retorna una ventana gráfica de inicio de sesión. """
    
    def verificar_credenciales():
        """ Esta función verifica las credenciales ingresadas por el usuario (nombre de usuario y contraseña)
        comparándolas con las credenciales almacenadas en la base de datos. 
        Si las credenciales son válidas, muestra un mensaje de inicio de sesión exitoso y cierra la ventana de inicio de sesión.
        De lo contrario, muestra un mensaje de error y no permite el inicio de sesión. """
        # Variables globales necesarias para verificar el estado de la sesión.
        global sesion_iniciada
        usuario = entrada_usuario.get()
        contraseña = entrada_contraseña.get()

        if validar_credenciales(usuario, contraseña):
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
            ventana_inicio_sesion.destroy()
            sesion_iniciada = True
            
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            sesion_iniciada = False
    # Se crea la ventana de inicio de sesión.
    ventana_inicio_sesion = tk.Tk()
    ventana_inicio_sesion.title("Inicio de Sesión")
    ventana_inicio_sesion.geometry("350x250")
    ventana_inicio_sesion.configure(bg="pink")

    tk.Label(ventana_inicio_sesion, text="Usuario:", bg="white").grid(row=0, column=0, padx=5, pady=5)
    entrada_usuario = tk.Entry(ventana_inicio_sesion)
    entrada_usuario.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana_inicio_sesion, text="Contraseña:", bg="white").grid(row=1, column=0, padx=5, pady=5)
    entrada_contraseña = tk.Entry(ventana_inicio_sesion, show="*")
    entrada_contraseña.grid(row=1, column=1, padx=5, pady=5)

    boton_ingresar = tk.Button(ventana_inicio_sesion, text="Ingresar", command=verificar_credenciales)
    boton_ingresar.grid(row=2, columnspan=2, padx=5, pady=5)

    ventana_inicio_sesion.mainloop()



def validar_numero(entrada):
    """Esta función valida si una entrada es un número entero o no.
    Retorna:
        Éxito: Retorna el número entero si la entrada es válida.
        Fracaso: Imprime un mensaje de error y retorna None si la entrada no es un número válido. """
        
    try:
        numero = int(entrada)
        return numero
    except ValueError:
        print("Error: Ingrese un número válido.")
        return None



def ingresar_medicamento():
    """ 
    Esta función permite ingresar un nuevo medicamento en la base de datos. Se solicita al usuario ingresar los siguientes datos del medicamento:
    - Lote
    - Nombre
    - Cantidad
    - Fecha de llegada (en formato YYYY-MM-DD)
    - Precio
    - Código del proveedor
    - Código de la ubicación
    Se intenta ingresar el medicamento en la base de datos y 
    si el ingreso es exitoso se imprime: "Medicamento ingresado exitosamente."
    Si ocurre un error imprime: "Error al ingresar el medicamento"
    Esta función también muestra los proveedores y ubicaciones disponibles antes de hacer la elección de estos. 
    """
    conexion = conectar()
    if not conexion:
        return

    comando = conexion.cursor()

    try:
        lote = input("Lote: ")
        nombre = input("Nombre del medicamento: ")
        
        cantidad = None
        while cantidad is None:
            cantidad = validar_numero(input("Cantidad: "))
        
        fecha_llegada = input("Fecha de llegada (YYYY-MM-DD): ")
        
        precio = None
        while precio is None:
            precio = validar_numero(input("Precio: "))
        
        # Mostrar proveedores disponibles
        comando.execute("SELECT codigo, nombre, apellido FROM proveedores")
        proveedores = comando.fetchall()
        print("Proveedores disponibles:")
        for proveedor in proveedores:
            print(f"Código: {proveedor[0]}, Nombre: {proveedor[1]}, Apellido: {proveedor[2]}")
        
        codigo_proveedor = None
        while codigo_proveedor is None:
            codigo_proveedor = validar_numero(input("Código del proveedor: "))
        
        # Mostrar ubicaciones disponibles
        comando.execute("SELECT codigo, nombre FROM ubicaciones")
        ubicaciones = comando.fetchall()
        print("\nUbicaciones disponibles:")
        for ubicacion in ubicaciones:
            print(f"Código: {ubicacion[0]}, Nombre: {ubicacion[1]}")
        
        codigo_ubicacion = None
        while codigo_ubicacion is None:
            codigo_ubicacion = validar_numero(input("Código de la ubicación: "))

        comando.execute("""
            INSERT INTO medicamentos (lote, nombre, cantidad, fecha_llegada, precio, codigo_proveedor, codigo_ubicacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (lote, nombre, cantidad, fecha_llegada, precio, codigo_proveedor, codigo_ubicacion))
        conexion.commit()
        print("Medicamento ingresado exitosamente.")
    except mysql.connector.Error as error:
        print(f"Error al ingresar el medicamento: {error}")

    comando.close()
    conexion.close()





def actualizar_medicamento():
    """ Esta función permite actualizar la información de un medicamento en la base de datos.
    Se solicita al usuario que ingrese el número de lote del medicamento que desea actualizar.
    Luego se muestran los campos del medicamento junto con los valores actuales (si existen)
    y se solicita al usuario que ingrese los nuevos valores.
    Si el medicamento no se encuentra en la base de datos, se muestra un mensaje indicando que no se encontró el medicamento. 
    Finalmente, se realiza la actualización en la base de datos."""
    
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    lote = input("Ingrese el número de lote del medicamento que desea actualizar: ")

    # Verificar si el medicamento existe
    comando.execute("SELECT * FROM medicamentos WHERE lote = %s", (lote,))
    medicamento = comando.fetchone()
    if not medicamento:
        print(f"No se encontró ningún medicamento con el lote {lote}.")
        comando.close()
        conexion.close()
        return

    print("Ingrese los nuevos valores para el medicamento:")

    nombre = input(f"Nombre del medicamento [{medicamento[1]}]: ")

    cantidad = validar_numero(input(f"Cantidad [{medicamento[2]}]: "))
    if cantidad is None:
        print("Cantidad debe ser un número entero.")
        comando.close()
        conexion.close()
        return

    fecha_llegada = input(f"Fecha de llegada (YYYY-MM-DD) [{medicamento[3]}]: ")

    precio = validar_numero(input(f"Precio [{medicamento[4]}]: "))
    if precio is None:
        print("Precio debe ser un número entero.")
        comando.close()
        conexion.close()
        return

    # Mostrar proveedores disponibles
    try:
        comando.execute("SELECT codigo, nombre, apellido FROM proveedores")
        proveedores = comando.fetchall()
        print("Proveedores disponibles:")
        for proveedor in proveedores:
            print(f"Código: {proveedor[0]}, Nombre: {proveedor[1]}, Apellido: {proveedor[2]}")
    except mysql.connector.Error as error:
        print(f"Error al obtener los proveedores: {error}")
        comando.close()
        conexion.close()
        return

    codigo_proveedor = validar_numero(input(f"Código del proveedor [{medicamento[5]}]: "))
    if codigo_proveedor is None:
        print("Código del proveedor debe ser un número entero.")
        comando.close()
        conexion.close()
        return

    # Mostrar ubicaciones disponibles
    try:
        comando.execute("SELECT codigo, nombre FROM ubicaciones")
        ubicaciones = comando.fetchall()
        print("\nUbicaciones disponibles:")
        for ubicacion in ubicaciones:
            print(f"Código: {ubicacion[0]}, Nombre: {ubicacion[1]}")
    except mysql.connector.Error as error:
        print(f"Error al obtener las ubicaciones: {error}")
        comando.close()
        conexion.close()
        return

    codigo_ubicacion = validar_numero(input(f"Código de la ubicación [{medicamento[6]}]: "))
    if codigo_ubicacion is None:
        print("Código de la ubicación debe ser un número entero.")
        comando.close()
        conexion.close()
        return

    try:
        comando.execute("""
            UPDATE medicamentos
            SET nombre = %s, cantidad = %s, fecha_llegada = %s, precio = %s, codigo_proveedor = %s, codigo_ubicacion = %s
            WHERE lote = %s
        """, (nombre, cantidad, fecha_llegada, precio, codigo_proveedor, codigo_ubicacion, lote))
        conexion.commit()
        print("Medicamento actualizado exitosamente.")
    except mysql.connector.Error as error:
        print(f"Error al actualizar el medicamento: {error}")

    comando.close()
    conexion.close()



def buscar_medicamento_por_lote():
    """ Esta función permite buscar un medicamento en la base de datos utilizando su número de lote.
    Se solicita al usuario que ingrese el número de lote del medicamento que desea buscar. 
    Luego, se realiza una consulta a la base de datos para encontrar el medicamento. 
    Si se encuentra el medicamento, se muestra su información. 
    Si no se encuentra ningún medicamento con el número de lote ingresado, se muestra un mensaje indicando que no se encontró ningún medicamento."""
    
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    lote = input("Ingrese el número de lote del medicamento que desea buscar: ")

    
    comando.execute("SELECT * FROM medicamentos WHERE lote = %s", (lote,))
    medicamento = comando.fetchone()
    if not medicamento:
        print(f"No se encontró ningún medicamento con el lote {lote}.")
    else:
        print("Información del medicamento:")
        print(f"Lote: {medicamento[0]}")
        print(f"Nombre: {medicamento[1]}")
        print(f"Cantidad: {medicamento[2]}")
        print(f"Fecha de llegada: {medicamento[3]}")
        print(f"Precio: {medicamento[4]}")
        print(f"Código del proveedor: {medicamento[5]}")
        print(f"Código de la ubicación: {medicamento[6]}")

    comando.close()
    conexion.close()



def ver_todos_los_medicamentos():
    """ Esta función permite ver toda la información de los medicamentos almacenados en la base de datos. 
    Realiza una consulta a la base de datos para obtener todos los medicamentos y luego muestra la información de cada uno de ellos. 
    Retorna:
        Éxito: Si hay medicamentos almacenados en la base de datos. Si no hay medicamentos almacenados, muestra un mensaje indicando que no hay medicamentos.
        Fracaso: Si hay algún problema de conexión con la base de datos al realizar la consulta, muestra un mensaje de error."""
    
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    try:
        comando.execute("""
            SELECT lote, nombre, cantidad, fecha_llegada, precio, codigo_proveedor, codigo_ubicacion
            FROM medicamentos
        """)
        medicamentos = comando.fetchall()
        if not medicamentos:
            print("No hay medicamentos almacenados.")
        else:
            print("Información de todos los medicamentos almacenados:")
            for medicamento in medicamentos:
                print("----------------------------")
                print(f"Lote: {medicamento[0]}")
                print(f"Nombre: {medicamento[1]}")
                print(f"Cantidad: {medicamento[2]}")
                print(f"Fecha de llegada: {medicamento[3]}")
                print(f"Precio: {medicamento[4]}")
                print(f"Código del proveedor: {medicamento[5]}")
                print(f"Código de la ubicación: {medicamento[6]}")
                print("----------------------------")
    except mysql.connector.Error as error:
        print(f"Error al obtener los medicamentos: {error}")

    comando.close()
    conexion.close()



def eliminar_medicamento():
    """  Esta función permite eliminar un medicamento de la base de datos mediante su número de lote.
    Esta establece una conexión con la base de datos. Despues se solicita que se ingrese el número de lote del medicamento que desea eliminar.
    Se verifica si el medicamento existe en la base de datos. Si existe, se solicita una confirmación al usuario antes de proceder con la eliminación.
    Si la confirmación es "si", se elimina el medicamento. Si la confirmación es "no" o cualquier otro valor, se cancela la operación."""
    
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    lote = input("Ingrese el número de lote del medicamento que desea eliminar: ")

    # Verificar si el medicamento existe
    comando.execute("SELECT * FROM medicamentos WHERE lote = %s", (lote,))
    medicamento = comando.fetchone()
    if not medicamento:
        print(f"No se encontró ningún medicamento con el lote {lote}.")
        comando.close()
        conexion.close()
        return

    confirmacion = input(f"Está seguro que desea eliminar el medicamento con el lote {lote}? (si/no): ").lower()
    if confirmacion == 'si':
        try:
            comando.execute("DELETE FROM medicamentos WHERE lote = %s", (lote,))
            conexion.commit()
            print(f"Medicamento con el lote {lote} eliminado exitosamente.")
        except mysql.connector.Error as error:
            print(f"Error al eliminar el medicamento: {error}")
    else:
        print("Operación cancelada.")

    comando.close()
    conexion.close()


#Proveedores

def ingresar_proveedor():
    """
    Esta función permite ingresar un nuevo proveedor en la base de datos.

    Solicita al usuario que ingrese el código, nombre, apellido y documento del proveedor.
    Luego intenta insertar estos datos en la tabla 'proveedores'.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    
    conexion = conectar()
    comando = conexion.cursor()
    
    while True:
        codigo = input("Ingrese el código del proveedor: ")
        codigo_validado = validar_numero(codigo)
        if codigo_validado is not None:
            break
        else:
            print("Error: El código debe ser un número.")

    nombre = input("Ingrese el nombre del proveedor: ")
    apellido = input("Ingrese el apellido del proveedor: ")
    
    while True:
        documento = input("Ingrese el número de documento del proveedor: ")
        documento_validado = validar_numero(documento)
        if documento_validado is not None:
            break
        else:
            print("Error: El documento debe ser un número.")

    comando.execute("""
        INSERT INTO proveedores (codigo, nombre, apellido, documento)
        VALUES (%s, %s, %s, %s)
    """, (codigo_validado, nombre, apellido, documento_validado))
    
    conexion.commit()
    comando.close()
    conexion.close()
    print("Proveedor ingresado exitosamente.")






def actualizar_proveedor():
    """
    Esta función permite actualizar la información de un proveedor existente en la base de datos.

    Solicita al usuario que ingrese el código del proveedor que desea actualizar.
    Luego muestra los detalles del proveedor y solicita los nuevos valores para nombre, apellido y documento.
    Finalmente, actualiza los datos del proveedor en la tabla 'proveedores'.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    while True:
        codigo = validar_numero(input("Ingrese el código del proveedor a actualizar: "))
        if codigo is None:
            print("El código del proveedor debe ser un número entero.")
        else:
            # Verificar si el proveedor existe
            comando.execute("SELECT * FROM proveedores WHERE codigo = %s", (codigo,))
            proveedor = comando.fetchone()
            if not proveedor:
                print(f"No se encontró ningún proveedor con el código {codigo}.")
                comando.close()
                conexion.close()
                return
            else:
                break

    print("Ingrese los nuevos valores para el proveedor:")

    nombre = input(f"Nombre del proveedor [{proveedor[1]}]: ")
    apellido = input(f"Apellido del proveedor [{proveedor[2]}]: ")

    while True:
        documento = validar_numero(input(f"Número de documento del proveedor [{proveedor[3]}]: "))
        if documento is None:
            print("El número de documento debe ser un número entero.")
        else:
            break

    try:
        comando.execute("""
            UPDATE proveedores
            SET nombre = %s, apellido = %s, documento = %s
            WHERE codigo = %s
        """, (nombre, apellido, documento, codigo))
        conexion.commit()
        print("Proveedor actualizado exitosamente.")
    except mysql.connector.Error as error:
        print(f"Error al actualizar el proveedor: {error}")

    comando.close()
    conexion.close()




def buscar_proveedor():
    """
    Esta función permite buscar un proveedor por su código en la base de datos.

    Solicita al usuario que ingrese el código del proveedor que desea buscar.
    Luego busca el proveedor en la tabla 'proveedores' y muestra sus detalles si se encuentra.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    while True:
        codigo = validar_numero(input("Ingrese el código del proveedor a buscar: "))
        if codigo is None:
            print("El código del proveedor debe ser un número entero.")
        else:
            break

    comando.execute("SELECT * FROM proveedores WHERE codigo = %s", (codigo,))
    proveedor = comando.fetchone()
    if proveedor:
        print("Información del proveedor:")
        print(f"Código: {proveedor[0]}")
        print(f"Nombre: {proveedor[1]}")
        print(f"Apellido: {proveedor[2]}")
        print(f"Documento: {proveedor[3]}")
    else:
        print("Proveedor no encontrado.")
    
    comando.close()
    conexion.close()




def ver_proveedores():
    """
    Muestra la información de todos los proveedores almacenados en la base de datos.

    Recupera y muestra el código, nombre, apellido y documento de todos los proveedores.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    try:
        comando.execute("SELECT * FROM proveedores")
        proveedores = comando.fetchall()
        if not proveedores:
            print("No hay proveedores almacenados.")
        else:
            print("Información de todos los proveedores almacenados:")
            for proveedor in proveedores:
                print("----------------------------")
                print(f"Código: {proveedor[0]}")
                print(f"Nombre: {proveedor[1]}")
                print(f"Apellido: {proveedor[2]}")
                print(f"Documento: {proveedor[3]}")
                print("----------------------------")
    except mysql.connector.Error as error:
        print(f"Error al obtener los proveedores: {error}")

    comando.close()
    conexion.close()


def eliminar_proveedor():
    """
    Esta función permite eliminar un proveedor de la base de datos.

    Solicita al usuario que ingrese el código del proveedor que desea eliminar.
    Luego intenta eliminar el proveedor correspondiente de la tabla 'proveedores'.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    codigo = None
    while codigo is None:
        codigo = validar_numero(input("Ingrese el código del proveedor que desea eliminar: "))

    # Verificar si el proveedor existe
    comando.execute("SELECT * FROM proveedores WHERE codigo = %s", (codigo,))
    proveedor = comando.fetchone()
    if not proveedor:
        print(f"No se encontró ningún proveedor con el código {codigo}.")
        comando.close()
        conexion.close()
        return

    confirmacion = input(f"Está seguro que desea eliminar el proveedor con el código {codigo}? (si/no): ").lower()
    if confirmacion == 'si':
        try:
            comando.execute("DELETE FROM proveedores WHERE codigo = %s", (codigo,))
            conexion.commit()
            print("Proveedor eliminado exitosamente.")
        except mysql.connector.Error as error:
            print(f"Error al eliminar el proveedor: {error}")
    else:
        print("Operación cancelada.")

    comando.close()
    conexion.close()



#Ubicaciones

def ingresar_ubicacion():
    """
    Esta función permite ingresar una nueva ubicación en la base de datos.

    Solicita al usuario que ingrese el código, nombre y teléfono de la ubicación.
    Luego intenta insertar estos datos en la tabla 'ubicaciones'.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()
    
    codigo = None
    while codigo is None:
        codigo = validar_numero(input("Ingrese el código de la ubicación: "))

    nombre = input("Ingrese el nombre de la ubicación: ")
    telefono = validar_numero(input("Ingrese el teléfono de la ubicación: "))

    try:
        comando.execute("""
            INSERT INTO ubicaciones (codigo, nombre, telefono)
            VALUES (%s, %s, %s)
        """, (codigo, nombre, telefono))
        conexion.commit()
        print("Ubicación ingresada exitosamente.")
    except mysql.connector.Error as error:
        print(f"Error al ingresar la ubicación: {error}")

    comando.close()
    conexion.close()
    
def actualizar_ubicacion():
    """
    Esta función permite actualizar la información de una ubicación existente en la base de datos.

    Solicita al usuario que ingrese el código de la ubicación que desea actualizar.
    Luego muestra los detalles de la ubicación y solicita los nuevos valores para nombre y teléfono.
    Finalmente, actualiza los datos de la ubicación en la tabla 'ubicaciones'.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()
    
    codigo = None
    while codigo is None:
        codigo = validar_numero(input("Ingrese el código de la ubicación que desea actualizar: "))

    comando.execute("SELECT * FROM ubicaciones WHERE codigo = %s", (codigo,))
    ubicacion = comando.fetchone()
    if not ubicacion:
        print(f"No se encontró ninguna ubicación con el código {codigo}.")
        return

    print("Ingrese los nuevos valores para la ubicación:")
    nuevo_nombre = input(f"Nombre ({ubicacion[1]}): ")
    nuevo_telefono = input(f"Teléfono ({ubicacion[2]}): ")

    try:
        comando.execute("""
            UPDATE ubicaciones
            SET nombre = %s, telefono = %s
            WHERE codigo = %s
        """, (nuevo_nombre, nuevo_telefono, codigo))
        conexion.commit()
        print("Ubicación actualizada exitosamente.")
    except mysql.connector.Error as error:
        print(f"Error al actualizar la ubicación: {error}")

    comando.close()
    conexion.close()



def buscar_ubicacion():
    """
    Esta función permite buscar una ubicación por su código en la base de datos.

    Solicita al usuario que ingrese el código de la ubicación que desea buscar.
    Luego busca la ubicación en la tabla 'ubicaciones' y muestra sus detalles si se encuentra.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    codigo = None
    while codigo is None:
        codigo = validar_numero(input("Ingrese el código de la ubicación que desea buscar: "))

    # Verificar si la ubicación existe
    comando.execute("SELECT * FROM ubicaciones WHERE codigo = %s", (codigo,))
    ubicacion = comando.fetchone()
    if ubicacion:
        print("Información de la ubicación:")
        print(f"Código: {ubicacion[0]}")
        print(f"Nombre: {ubicacion[1]}")
        print(f"Teléfono: {ubicacion[2]}")
    else:
        print(f"No se encontró ninguna ubicación con el código {codigo}.")

    comando.close()
    conexion.close()


def ver_ubicaciones():
    """
    Muestra la información de todas las ubicaciones almacenadas en la base de datos.

    Recupera y muestra el código, nombre y teléfono de todas las ubicaciones.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    try:
        comando = conexion.cursor()
        comando.execute("SELECT * FROM ubicaciones")
        ubicaciones = comando.fetchall()

        if not ubicaciones:
            print("No hay ubicaciones almacenadas.")
            return

        print("Información de todas las ubicaciones almacenadas:")
        for ubicacion in ubicaciones:
            print("----------------------------")
            print(f"Código: {ubicacion[0]}")
            print(f"Nombre: {ubicacion[1]}")
            print(f"Teléfono: {ubicacion[2]}")
            print("----------------------------")
    except mysql.connector.Error as error:
        print(f"Error al obtener las ubicaciones: {error}")
    finally:
        comando.close()
        conexion.close()


def eliminar_ubicacion():
    """
    Esta función permite eliminar una ubicación de la base de datos.

    Solicita al usuario que ingrese el código de la ubicación que desea eliminar.
    Luego intenta eliminar la ubicación correspondiente de la tabla 'ubicaciones'.

    Retorna:
        None: Esta función no retorna ningún valor directamente.
    """
    conexion = conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos.")
        return

    comando = conexion.cursor()

    codigo = None
    while codigo is None:
        codigo = validar_numero(input("Ingrese el código de la ubicación que desea eliminar: "))

    # Verificar si la ubicación existe
    comando.execute("SELECT * FROM ubicaciones WHERE codigo = %s", (codigo,))
    ubicacion = comando.fetchone()
    if not ubicacion:
        print(f"No se encontró ninguna ubicación con el código {codigo}.")
        comando.close()
        conexion.close()
        return

    confirmacion = input(f"Está seguro que desea eliminar la ubicación con el código {codigo}? (si/no): ").lower()
    if confirmacion == 'si':
        try:
            comando.execute("DELETE FROM ubicaciones WHERE codigo = %s", (codigo,))
            conexion.commit()
            print("Ubicación eliminada exitosamente.")
        except mysql.connector.Error as error:
            print(f"Error al eliminar la ubicación: {error}")
    else:
        print("Operación cancelada.")

    comando.close()
    conexion.close()


    






