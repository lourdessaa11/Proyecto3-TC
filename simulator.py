
class Simulador:
    """
    Clase encargada de simular la ejecucion de una Maquina de Turing
    """

    def __init__(self, maquina_turing):
        """
        Inicializa el simulador con una MT
        """
        self.mt = maquina_turing
        self.descripciones_instantaneas = []
        self.limite_pasos = 10000  # Limite para evitar loops infinitos

    def simular(self, cadena_entrada):
        """
        Simula la ejecucion de la MT sobre una cadena de entrada
        Retorna un diccionario con los resultados de la simulacion
        """
        # Inicializamos la cinta y el estado
        self.mt.inicializar_cinta(cadena_entrada)
        self.descripciones_instantaneas = []

        # Guardamos la descripcion instantanea inicial
        id_inicial = self.mt.cinta.obtener_descripcion_instantanea(self.mt.estado_actual)
        self.descripciones_instantaneas.append(id_inicial)

        pasos = 0
        resultado = None

        # Simulamos paso a paso hasta que no haya transicion aplicable
        while pasos < self.limite_pasos:
            # Leemos el simbolo actual
            simbolo_actual = self.mt.cinta.leer()

            # Buscamos una transicion aplicable
            transicion = self.mt.buscar_transicion(self.mt.estado_actual, simbolo_actual)

            # Si no hay transicion, terminamos
            if transicion is None:
                # Verificamos si estamos en estado de aceptacion
                if self.mt.esta_en_estado_aceptacion():
                    resultado = "ACEPTADA"
                else:
                    resultado = "RECHAZADA"
                break

            # Aplicamos la transicion
            self.mt.cinta.escribir(transicion.simbolo_escribir)
            self.mt.estado_actual = transicion.estado_siguiente

            # Movemos el cabezal
            if transicion.movimiento == 'L':
                self.mt.cinta.mover_izquierda()
            elif transicion.movimiento == 'R':
                self.mt.cinta.mover_derecha()
            # Si es 'S', no movemos el cabezal

            # Guardamos la nueva descripcion instantanea
            id_actual = self.mt.cinta.obtener_descripcion_instantanea(self.mt.estado_actual)
            self.descripciones_instantaneas.append(id_actual)

            pasos += 1

        # Si llegamos al limite de pasos, es un loop infinito
        if pasos >= self.limite_pasos:
            resultado = "LOOP INFINITO DETECTADO"

        # Si terminamos y no habiamos establecido resultado, verificamos estado
        if resultado is None:
            if self.mt.esta_en_estado_aceptacion():
                resultado = "ACEPTADA"
            else:
                resultado = "RECHAZADA"

        # Retornamos los resultados
        return {
            'cadena_entrada': cadena_entrada,
            'resultado': resultado,
            'pasos': pasos,
            'descripciones_instantaneas': self.descripciones_instantaneas,
            'cinta_final': self.mt.cinta.obtener_contenido(),
            'estado_final': self.mt.estado_actual
        }

    def obtener_descripciones(self):
        """
        Retorna la lista de descripciones instantaneas de la ultima simulacion
        """
        return self.descripciones_instantaneas