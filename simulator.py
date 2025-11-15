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
        self.limite_pasos = 10000  #limite

    def simular(self, cadena_entrada):
        """
        Simula la ejecucion de la MT sobre una cadena de entrada
        """
        self.mt.inicializar_cinta(cadena_entrada)
        self.descripciones_instantaneas = []

        id_inicial = self.mt.cinta.obtener_descripcion_instantanea(self.mt.estado_actual)
        self.descripciones_instantaneas.append(id_inicial)

        pasos = 0
        resultado = None

        while pasos < self.limite_pasos:
            simbolo_actual = self.mt.cinta.leer()

            transicion = self.mt.buscar_transicion(self.mt.estado_actual, simbolo_actual)

            if transicion is None:
                if self.mt.esta_en_estado_aceptacion():
                    resultado = "ACEPTADA"
                else:
                    resultado = "RECHAZADA"
                break

            self.mt.cinta.escribir(transicion.simbolo_escribir)
            self.mt.estado_actual = transicion.estado_siguiente

            if transicion.movimiento == 'L':
                self.mt.cinta.mover_izquierda()
            elif transicion.movimiento == 'R':
                self.mt.cinta.mover_derecha()

            id_actual = self.mt.cinta.obtener_descripcion_instantanea(self.mt.estado_actual)
            self.descripciones_instantaneas.append(id_actual)

            pasos += 1

        if pasos >= self.limite_pasos:
            resultado = "Loop infinito"

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
