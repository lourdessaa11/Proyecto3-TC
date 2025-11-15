import yaml


class ParserYAML:
    """
    leer y parsear archivos YAML con la configuracion
    de una Maquina de Turing
    """

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.configuracion = None

    def leer_archivo(self):
        """
        Lee el archivo YAML y carga su contenido
        """
        try:
            with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
                self.configuracion = yaml.safe_load(archivo)
            return True
        except FileNotFoundError:
            print(f"Error: No se encontro el archivo {self.ruta_archivo}")
            return False
        except yaml.YAMLError as e:
            print(f"Error al parsear el archivo YAML: {e}")
            return False
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {e}")
            return False

    def obtener_estados(self):
        """
        Extrae la lista de estados de la MT
        """
        return self.configuracion['mt']['states']

    def obtener_alfabeto_entrada(self):
        """
        Extrae el alfabeto de entrada
        """
        return self.configuracion['mt']['input_alphabet']

    def obtener_alfabeto_cinta(self):
        """
        Extrae el alfabeto de la cinta
        """
        return self.configuracion['mt']['tape_alphabet']

    def obtener_estado_inicial(self):
        """
        Extrae el estado inicial de la MT
        """
        return self.configuracion['mt']['initial_state']

    def obtener_estados_aceptacion(self):
        """
        Extrae los estados de aceptacion
        """
        return self.configuracion['mt']['accept_states']

    def obtener_transiciones(self):
        """
        Extrae las funciones de transicion
        """
        return self.configuracion['mt']['transitions']

    def obtener_inputs(self):
        """
        Extrae las cadenas de entrada a simular
        """
        return self.configuracion['inputs']

    def validar_configuracion(self):
        """
        Valida que la configuracion tenga todos los campos necesarios
        """
        if not self.configuracion:
            print("Error: No hay configuracion cargada")
            return False

        # Verificar que existe la clave 'mt'
        if 'mt' not in self.configuracion:
            print("Error: Falta la clave 'mt' en la configuracion")
            return False

        campos_requeridos = ['states', 'input_alphabet', 'tape_alphabet',
                             'initial_state', 'accept_states', 'transitions']

        mt = self.configuracion.get('mt', {})

        for campo in campos_requeridos:
            if campo not in mt:
                print(f"Error: Falta el campo '{campo}' en la configuracion")
                return False

        if 'inputs' not in self.configuracion:
            print("Error: Falta el campo 'inputs' en la configuracion")
            return False

        if not isinstance(mt['states'], list) or len(mt['states']) == 0:
            print("Error: 'states' debe ser una lista no vacia")
            return False

        if not isinstance(mt['input_alphabet'], list):
            print("Error: 'input_alphabet' debe ser una lista")
            return False

        if not isinstance(mt['tape_alphabet'], list):
            print("Error: 'tape_alphabet' debe ser una lista")
            return False

        if mt['initial_state'] not in mt['states']:
            print("Error: El estado inicial no esta en la lista de estados")
            return False

        for estado in mt['accept_states']:
            if estado not in mt['states']:
                print(f"Error: El estado de aceptacion '{estado}' no esta en la lista de estados")
                return False

        if not isinstance(mt['transitions'], list):
            print("Error: 'transitions' debe ser una lista")
            return False

        for i, trans in enumerate(mt['transitions']):
            campos_trans = ['state', 'read', 'write', 'move', 'next']
            for campo in campos_trans:
                if campo not in trans:
                    print(f"Error: Falta el campo '{campo}' en la transicion {i}")
                    return False

            if trans['state'] not in mt['states']:
                print(f"Error: Estado '{trans['state']}' en transicion {i} no esta en la lista de estados")
                return False

            if trans['next'] not in mt['states']:
                print(f"Error: Estado siguiente '{trans['next']}' en transicion {i} no esta en la lista de estados")
                return False

            if trans['move'] not in ['L', 'R', 'S']:
                print(f"Error: Movimiento '{trans['move']}' invalido en transicion {i}. Debe ser L, R o S")
                return False

        if not isinstance(self.configuracion['inputs'], list):
            print("Error: 'inputs' debe ser una lista")
            return False

        return True
