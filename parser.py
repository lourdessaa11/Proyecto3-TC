import yaml

class ParserYAML:
    """
    Clase encargada de leer y parsear archivos YAML con la configuracion
    de una Maquina de Turing
    """

    def __init__(self, ruta_archivo):
        """
        Inicializa el parser con la ruta del archivo YAML
        """
        self.ruta_archivo = ruta_archivo
        self.configuracion = None

    def leer_archivo(self):
        """
        Lee el archivo YAML y carga su contenido
        Retorna True si tuvo exito, False en caso contrario
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
        Retorna una lista de diccionarios con cada transicion
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

        return True