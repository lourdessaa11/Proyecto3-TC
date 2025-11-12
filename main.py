import sys
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

        # Creamos una transicion por cada combinacion de simbolos
        # El formato del YAML puede tener multiples simbolos en read/write
        # Asumimos que son del mismo largo y se corresponden por posicion
        for i in range(len(simbolos_leer)):
            simbolo_leer = simbolos_leer[i]
            simbolo_escribir = simbolos_escribir[i]

            transicion = Transicion(estado, simbolo_leer, siguiente,
                                    simbolo_escribir, movimiento)
            mt.agregar_transicion(transicion)

    return mt


def main():
    """
    Funcion principal del programa
    """
    print()
    print("=" * 70)
    print("SIMULADOR DE MAQUINA DE TURING")
    print("=" * 70)
    print()

    # Verificamos que se proporciono un archivo
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo.yaml>")
        print("Ejemplo: python main.py ejemplos/reconocedor_anbn.yaml")
        return

    archivo_yaml = sys.argv[1]

    # Creamos el parser y leemos el archivo
    print(f"Leyendo archivo: {archivo_yaml}")
    parser = ParserYAML(archivo_yaml)

    if not parser.leer_archivo():
        print("Error al leer el archivo. Terminando programa.")
        return

    if not parser.validar_configuracion():
        print("Error en la configuracion. Terminando programa.")
        return

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


if __name__ == "__main__":
    main()