class Transicion:
    """
    Representa una funcion de transicion de la MT
    """

    def __init__(self, estado_actual, simbolo_leido, estado_siguiente,
                 simbolo_escribir, movimiento):
        """
        Inicializa una transicion
        estado_actual: estado desde donde se aplica la transicion
        simbolo_leido: simbolo que debe leer en la cinta
        estado_siguiente: estado al que se mueve
        simbolo_escribir: simbolo que escribe en la cinta
        movimiento: 'L' (izquierda), 'R' (derecha), 'S' (stay/quieto)
        """
        self.estado_actual = estado_actual
        self.simbolo_leido = simbolo_leido
        self.estado_siguiente = estado_siguiente
        self.simbolo_escribir = simbolo_escribir
        self.movimiento = movimiento

    def __str__(self):
        return f"δ({self.estado_actual}, {self.simbolo_leido}) = ({self.estado_siguiente}, {self.simbolo_escribir}, {self.movimiento})"


class Cinta:
    """
    Representa la cinta de la Maquina de Turing
    """

    def __init__(self, cadena_inicial, simbolo_blanco='B'):
        """
        Inicializa la cinta con una cadena
        cadena_inicial: cadena de entrada
        simbolo_blanco: simbolo que representa espacios vacios
        """
        self.simbolo_blanco = simbolo_blanco
        if cadena_inicial:
            self.cinta = list(cadena_inicial)
        else:
            self.cinta = []

        self.posicion_cabezal = 0

        self.cinta.insert(0, simbolo_blanco)
        self.cinta.append(simbolo_blanco)
        self.posicion_cabezal = 1

    def leer(self):
        """
        Lee el simbolo en la posicion actual del cabezal
        """
        return self.cinta[self.posicion_cabezal]

    def escribir(self, simbolo):
        """
        Escribe un simbolo en la posicion actual del cabezal
        """
        self.cinta[self.posicion_cabezal] = simbolo

    def mover_izquierda(self):
        """
        Mueve el cabezal una posicion a la izquierda
        Si llega al borde, agrega un blanco
        """
        self.posicion_cabezal -= 1
        if self.posicion_cabezal < 0:
            self.cinta.insert(0, self.simbolo_blanco)
            self.posicion_cabezal = 0

    def mover_derecha(self):
        """
        Mueve el cabezal una posicion a la derecha
        Si llega al borde, agrega un blanco
        """
        self.posicion_cabezal += 1
        if self.posicion_cabezal >= len(self.cinta):
            self.cinta.append(self.simbolo_blanco)

    def obtener_contenido(self):
        """
        Retorna el contenido de la cinta como string
        """
        return ''.join(self.cinta)

    def obtener_descripcion_instantanea(self, estado_actual):
        """
        Retorna la descripcion instantanea (ID) de la MT
        Formato: contenido_izquierda + estado + contenido_derecha

        """
        izquierda = ''.join(self.cinta[:self.posicion_cabezal])
        derecha = ''.join(self.cinta[self.posicion_cabezal:])
        return f"{izquierda}{estado_actual}{derecha}"


class MaquinaTuring:
    """
    Representa una Maquina de Turing completa
    """

    def __init__(self, estados, alfabeto_entrada, alfabeto_cinta,
                 estado_inicial, estados_aceptacion):
        """
        Inicializa la Maquina de Turing con sus componentes basicos
        """
        self.estados = estados
        self.alfabeto_entrada = alfabeto_entrada
        self.alfabeto_cinta = alfabeto_cinta
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.transiciones = {}  # Diccionario para buscar transiciones rapidamente
        self.estado_actual = estado_inicial
        self.cinta = None

    def agregar_transicion(self, transicion):
        """
        Agrega una transicion al conjunto de transiciones
        (estado_actual, simbolo_leido)
        """
        clave = (transicion.estado_actual, transicion.simbolo_leido)
        self.transiciones[clave] = transicion

    def buscar_transicion(self, estado, simbolo):
        """
        Busca una transicion aplicable dado un estado y simbolo
        """
        clave = (estado, simbolo)
        return self.transiciones.get(clave, None)

    def inicializar_cinta(self, cadena_entrada):
        """
        Inicializa la cinta con una cadena de entrada
        """
        simbolo_blanco = 'B'
        if 'B' in self.alfabeto_cinta:
            simbolo_blanco = 'B'
        elif '_' in self.alfabeto_cinta:
            simbolo_blanco = '_'
        elif ' ' in self.alfabeto_cinta:
            simbolo_blanco = ' '

        self.cinta = Cinta(cadena_entrada, simbolo_blanco)
        self.estado_actual = self.estado_inicial

    def esta_en_estado_aceptacion(self):
        """
        Verifica si el estado actual es un estado de aceptacion
        """
        return self.estado_actual in self.estados_aceptacion

    def obtener_info(self):
        """
        Retorna un diccionario con la informacion de la MT
        """
        return {
            'estados': self.estados,
            'alfabeto_entrada': self.alfabeto_entrada,
            'alfabeto_cinta': self.alfabeto_cinta,
            'estado_inicial': self.estado_inicial,
            'estados_aceptacion': self.estados_aceptacion,
            'num_transiciones': len(self.transiciones)
        }
