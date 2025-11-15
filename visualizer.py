class Visualizador:
    """
    Clase encargada de mostrar los resultados de la simulacion
    de forma clara y organizada
    """

    def __init__(self):
        """
        Inicializa el visualizador
        """
        pass

    def mostrar_configuracion_mt(self, info_mt):
        """
        Muestra la configuracion de la Maquina de Turing
        """
        print("=" * 70)
        print("CONFIGURACION DE LA MAQUINA DE TURING")
        print("=" * 70)
        print(f"Estados: {', '.join(info_mt['estados'])}")
        print(f"Alfabeto de entrada: {', '.join(info_mt['alfabeto_entrada'])}")
        print(f"Alfabeto de cinta: {', '.join(info_mt['alfabeto_cinta'])}")
        print(f"Estado inicial: {info_mt['estado_inicial']}")
        print(f"Estados de aceptacion: {', '.join(info_mt['estados_aceptacion'])}")
        print(f"Numero de transiciones: {info_mt['num_transiciones']}")
        print("=" * 70)
        print()

    def mostrar_transiciones(self, transiciones):
        """
        Muestra las funciones de transicion de la MT
        """
        print("FUNCIONES DE TRANSICION:")
        print("-" * 70)
        trans_ordenadas = sorted(transiciones.values(),
                                 key=lambda t: (t.estado_actual, t.simbolo_leido))
        for trans in trans_ordenadas:
            print(f"  {trans}")
        print()

    def mostrar_resultado_simulacion(self, resultado):
        """
        Muestra el resultado completo de una simulacion
        """
        print("=" * 70)
        print(f"SIMULACION DE LA CADENA: '{resultado['cadena_entrada']}'")
        print("=" * 70)
        print()

        print("DESCRIPCIONES INSTANTANEAS:")
        print("-" * 70)

        # Mostramos cada descripcion instantanea numerada
        for i, id_actual in enumerate(resultado['descripciones_instantaneas']):
            print(f"Paso {i}: {id_actual}")

        print()
        print("-" * 70)
        print(f"Numero de pasos ejecutados: {resultado['pasos']}")
        print(f"Estado final: {resultado['estado_final']}")
        print(f"Contenido final de la cinta: {resultado['cinta_final']}")
        print()

        # Mostramos el resultado con formato destacado
        if resultado['resultado'] == "ACEPTADA":
            print(">>> RESULTADO: CADENA ACEPTADA <<<")
        elif resultado['resultado'] == "RECHAZADA":
            print(">>> RESULTADO: CADENA RECHAZADA <<<")
        else:
            print(f">>> RESULTADO: {resultado['resultado']} <<<")

        print("=" * 70)
        print()

    def mostrar_resumen(self, resultados):
        """
        Muestra un resumen de todas las simulaciones
        """
        print()
        print("=" * 70)
        print("RESUMEN DE SIMULACIONES")
        print("=" * 70)

        aceptadas = 0
        rechazadas = 0
        otros = 0

        for resultado in resultados:
            if resultado['resultado'] == "ACEPTADA":
                aceptadas += 1
            elif resultado['resultado'] == "RECHAZADA":
                rechazadas += 1
            else:
                otros += 1

        print(f"Total de cadenas simuladas: {len(resultados)}")
        print(f"Cadenas aceptadas: {aceptadas}")
        print(f"Cadenas rechazadas: {rechazadas}")
        if otros > 0:
            print(f"Otros resultados: {otros}")

        print()
        print("Detalle por cadena:")
        print("-" * 70)
        for i, resultado in enumerate(resultados, 1):
            estado = "✓" if resultado['resultado'] == "ACEPTADA" else "✗"
            print(f"{i}. '{resultado['cadena_entrada']}' -> {estado} {resultado['resultado']}")

        print("=" * 70)
        print()

    def pausar(self):
        """
        Pausa la ejecucion esperando que el usuario presione Enter
        """
        input("Presione Enter para continuar...")
        print()
