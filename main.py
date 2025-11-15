import sys
import os
from parser import ParserYAML
from turing_machine import MaquinaTuring, Transicion
from simulator import Simulador
from visualizer import Visualizador


def construir_maquina_turing(parser):
    """
    Maquina de Turing a partir de la configuracion parseada
    """
    estados = parser.obtener_estados()
    alfabeto_entrada = parser.obtener_alfabeto_entrada()
    alfabeto_cinta = parser.obtener_alfabeto_cinta()
    estado_inicial = parser.obtener_estado_inicial()
    estados_aceptacion = parser.obtener_estados_aceptacion()

    mt = MaquinaTuring(estados, alfabeto_entrada, alfabeto_cinta,
                       estado_inicial, estados_aceptacion)

    transiciones_config = parser.obtener_transiciones()

    for trans in transiciones_config:
        estado = trans['state']
        simbolos_leer = trans['read']
        simbolos_escribir = trans['write']
        movimiento = trans['move']
        siguiente = trans['next']

        simbolo_leer = simbolos_leer[0] if isinstance(simbolos_leer, list) else simbolos_leer
        simbolo_escribir = simbolos_escribir[0] if isinstance(simbolos_escribir, list) else simbolos_escribir

        transicion = Transicion(estado, simbolo_leer, siguiente,
                                simbolo_escribir, movimiento)
        mt.agregar_transicion(transicion)

    return mt


def listar_archivos_yaml(directorio="."):
    """
    Lista todos los archivos YAML
    """
    try:
        archivos = []
        directorio_absoluto = os.path.abspath(directorio)

        for archivo in os.listdir(directorio):
            # Verificar extensiones .yaml, .yml y .yalm (por si acaso)
            if (archivo.lower().endswith('.yaml') or
                    archivo.lower().endswith('.yml') or
                    archivo.lower().endswith('.yalm')):
                archivos.append(archivo)

        return sorted(archivos)
    except Exception as e:
        print(f"Error al listar archivos: {e}")
        return []


def mostrar_menu_archivos():
    """
    Muestra un menu para seleccionar un archivo YAML
    """
    print()
    print("=" * 70)
    print("SELECCION DE ARCHIVO")
    print("=" * 70)
    print()

    archivos = listar_archivos_yaml(".")

    if not archivos:
        print("No se encontraron archivos YAML en el directorio actual")
        print()
        print("Opciones:")
        print("1. Ingresar nombre de archivo manualmente")
        print("2. Salir")
        print()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            archivo = input("Ingrese el nombre del archivo YAML: ").strip()
            if os.path.exists(archivo):
                return archivo
            else:
                print(f"Error: El archivo '{archivo}' no existe.")
                return None
        else:
            return None

    print("Archivos disponibles:")
    print()
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    print(f"{len(archivos) + 1}. Ingresar nombre manualmente")
    print(f"{len(archivos) + 2}. Salir")
    print()

    while True:
        try:
            opcion = input("Seleccione un archivo (numero): ").strip()
            opcion_num = int(opcion)

            if 1 <= opcion_num <= len(archivos):
                return archivos[opcion_num - 1]
            elif opcion_num == len(archivos) + 1:
                archivo = input("Ingrese el nombre del archivo YAML: ").strip()
                if os.path.exists(archivo):
                    return archivo
                else:
                    print(f"Error: El archivo '{archivo}' no existe.")
                    print()
            elif opcion_num == len(archivos) + 2:
                return None
            else:
                print("Opcion invalida. Intente nuevamente.")
                print()
        except ValueError:
            print("Por favor ingrese un numero valido.")
            print()


def ejecutar_simulacion(archivo_yaml):
    """
    Ejecuta la simulacion
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
    print("¡Maquina de Turing construida!")
    print()

    visualizador = Visualizador()

    visualizador.mostrar_configuracion_mt(mt.obtener_info())
    visualizador.mostrar_transiciones(mt.transiciones)

    simulador = Simulador(mt)

    inputs = parser.obtener_inputs()

    print(f"Se simularan {len(inputs)} cadenas de entrada.")
    print()
    visualizador.pausar()

    resultados = []
    for cadena in inputs:
        resultado = simulador.simular(cadena)
        resultados.append(resultado)
        visualizador.mostrar_resultado_simulacion(resultado)

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
        print("SIMULADOR DE MAQUINA DE TURING")
        print("=" * 70)
        print()
        print("1. Ejecutar simulacion")
        print("2. Salir")
        print()

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            archivo = mostrar_menu_archivos()
            if archivo:
                ejecutar_simulacion(archivo)
                input("\nPresione Enter para volver al menu principal...")
            else:
                print("No se selecciono ningun archivo.")
        elif opcion == "2":
            print()
            print("¡Feliz dia!")
            print()
            break
        else:
            print("Opcion invalida. Intente nuevamente.")


def main():
    if len(sys.argv) >= 2:
        archivo_yaml = sys.argv[1]
        ejecutar_simulacion(archivo_yaml)
    else:
        menu_principal()


if __name__ == "__main__":
    main()

