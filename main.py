import sys
import os
from parser import ParserYAML
from turing_machine import MaquinaTuring, Transicion
from simulator import Simulador
from visualizer import Visualizador


def construir_maquina_turing(parser):
    """
    Construye una Maquina de Turing a partir de la configuracion parseada
    """
    # Obtenemos los componentes basicos
    estados = parser.obtener_estados()
    alfabeto_entrada = parser.obtener_alfabeto_entrada()
    alfabeto_cinta = parser.obtener_alfabeto_cinta()
    estado_inicial = parser.obtener_estado_inicial()
    estados_aceptacion = parser.obtener_estados_aceptacion()

    # Creamos la MT
    mt = MaquinaTuring(estados, alfabeto_entrada, alfabeto_cinta,
                       estado_inicial, estados_aceptacion)

    # Agregamos las transiciones
    transiciones_config = parser.obtener_transiciones()

    for trans in transiciones_config:
        estado = trans['state']
        simbolos_leer = trans['read']
        simbolos_escribir = trans['write']
        movimiento = trans['move']
        siguiente = trans['next']

        # Según el ejemplo del PDF:
        # read: [a, B] significa leer 'a' de la cinta
        # write: [a, B] significa escribir 'a' en la cinta
        # Es una sola transición, donde el primer elemento es para la cinta
        # (En MT de una cinta, solo usamos el primer elemento)

        simbolo_leer = simbolos_leer[0] if isinstance(simbolos_leer, list) else simbolos_leer
        simbolo_escribir = simbolos_escribir[0] if isinstance(simbolos_escribir, list) else simbolos_escribir

        transicion = Transicion(estado, simbolo_leer, siguiente,
                                simbolo_escribir, movimiento)
        mt.agregar_transicion(transicion)

    return mt


def listar_archivos_yaml(directorio="ejemplos"):
    """
    Lista todos los archivos YAML en el directorio especificado
    Retorna una lista de rutas de archivos
    """
    if not os.path.exists(directorio):
        return []

    archivos = []
    for archivo in os.listdir(directorio):
        if archivo.endswith('.yaml') or archivo.endswith('.yml'):
            archivos.append(os.path.join(directorio, archivo))

    return archivos


def mostrar_menu_archivos():
    """
    Muestra un menu para seleccionar un archivo YAML
    Retorna la ruta del archivo seleccionado o None
    """
    print()
    print("=" * 70)
    print("SELECCION DE ARCHIVO DE CONFIGURACION")
    print("=" * 70)
    print()

    archivos = listar_archivos_yaml("ejemplos")

    if not archivos:
        print("No se encontraron archivos YAML en la carpeta 'ejemplos/'")
        print()
        # Opción para ingresar ruta manualmente
        print("Opciones:")
        print("1. Ingresar ruta manualmente")
        print("2. Salir")
        print()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo YAML: ").strip()
            if os.path.exists(ruta):
                return ruta
            else:
                print(f"Error: El archivo '{ruta}' no existe.")
                return None
        else:
            return None

    print("Archivos disponibles:")
    print()
    for i, archivo in enumerate(archivos, 1):
        nombre = os.path.basename(archivo)
        print(f"{i}. {nombre}")

    print(f"{len(archivos) + 1}. Ingresar ruta manualmente")
    print(f"{len(archivos) + 2}. Salir")
    print()

    while True:
        try:
            opcion = input("Seleccione un archivo (número): ").strip()
            opcion_num = int(opcion)

            if 1 <= opcion_num <= len(archivos):
                return archivos[opcion_num - 1]
            elif opcion_num == len(archivos) + 1:
                ruta = input("Ingrese la ruta del archivo YAML: ").strip()
                if os.path.exists(ruta):
                    return ruta
                else:
                    print(f"Error: El archivo '{ruta}' no existe.")
                    print()
            elif opcion_num == len(archivos) + 2:
                return None
            else:
                print("Opción inválida. Intente nuevamente.")
                print()
        except ValueError:
            print("Por favor ingrese un número válido.")
            print()


def ejecutar_simulacion(archivo_yaml):
    """
    Ejecuta la simulacion completa para un archivo YAML
    """
    print()
    print("=" * 70)
    print("SIMULADOR DE MAQUINA DE TURING")
    print("=" * 70)
    print()

    # Creamos el parser y leemos el archivo
    print(f"Leyendo archivo: {archivo_yaml}")
    parser = ParserYAML(archivo_yaml)

    if not parser.leer_archivo():
        print("Error al leer el archivo.")
        return False

    if not parser.validar_configuracion():
        print("Error en la configuracion.")
        return False

    print("Archivo leido correctamente.")
    print()

    # Construimos la Maquina de Turing
    print("Construyendo Maquina de Turing...")
    mt = construir_maquina_turing(parser)
    print("Maquina de Turing construida exitosamente.")
    print()

    # Creamos el visualizador
    visualizador = Visualizador()

    # Mostramos la configuracion de la MT
    visualizador.mostrar_configuracion_mt(mt.obtener_info())
    visualizador.mostrar_transiciones(mt.transiciones)

    # Creamos el simulador
    simulador = Simulador(mt)

    # Obtenemos las cadenas de entrada
    inputs = parser.obtener_inputs()

    print(f"Se simularan {len(inputs)} cadenas de entrada.")
    print()
    visualizador.pausar()

    # Simulamos cada cadena
    resultados = []
    for cadena in inputs:
        resultado = simulador.simular(cadena)
        resultados.append(resultado)
        visualizador.mostrar_resultado_simulacion(resultado)

        # Pausa entre simulaciones (excepto en la ultima)
        if cadena != inputs[-1]:
            visualizador.pausar()

    # Mostramos resumen final
    visualizador.mostrar_resumen(resultados)

    print("Simulacion completada.")
    print()

    return True


def menu_principal():
    """
    Menu principal del programa
    """
    while True:
        print()
        print("=" * 70)
        print("SIMULADOR DE MAQUINA DE TURING - MENU PRINCIPAL")
        print("=" * 70)
        print()
        print("1. Ejecutar simulación desde archivo YAML")
        print("2. Salir")
        print()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            archivo = mostrar_menu_archivos()
            if archivo:
                ejecutar_simulacion(archivo)
                input("\nPresione Enter para volver al menú principal...")
            else:
                print("No se seleccionó ningún archivo.")
        elif opcion == "2":
            print()
            print("¡Gracias por usar el simulador!")
            print()
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def main():
    """
    Funcion principal del programa
    """
    # Si se proporciona un archivo como argumento, usarlo directamente
    if len(sys.argv) >= 2:
        archivo_yaml = sys.argv[1]
        ejecutar_simulacion(archivo_yaml)
    else:
        # Si no hay argumentos, mostrar el menú
        menu_principal()


if __name__ == "__main__":
    main()
