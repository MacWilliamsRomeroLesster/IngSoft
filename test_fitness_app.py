import unittest
from unittest.mock import patch
import os
import sys
import os
import json  #importar el módulo json

# Obtener la ruta absoluta del directorio de pruebas
tests_dir = os.path.abspath(os.path.dirname(__file__))

# Agregar la ruta del directorio de pruebas a sys.path si no está presente
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)

print(sys.path)  # Imprimir sys.path para verificar si el directorio de pruebas está incluido

# Importa la clase que quieres probar
from fitness_app.fitness_app import FitnessApp

class TestFitnessApp(unittest.TestCase):
    
    def setUp(self):
        # Configura el entorno antes de cada prueba
        self.app = FitnessApp()
    def tearDown(self):
        # Limpia el entorno después de cada prueba
        # Por ejemplo, elimina cualquier archivo creado durante las pruebas
        if os.path.exists("user_info.json"):
            os.remove("user_info.json")

    def test_load_user_info(self):
        # Verifica que los datos del usuario se carguen correctamente
        user_info = self.app.load_user_info()
        self.assertEqual(user_info["nombre"], "")
        self.assertEqual(user_info["edad"], "")
        self.assertEqual(user_info["altura"], "")
        self.assertEqual(user_info["peso"], "")

    def test_save_user_info(self):
        # Simula la entrada del usuario
        self.app.username_entry.insert(0, "John")
        self.app.weight_entry.insert(0, "70")
        self.app.height_entry.insert(0, "175")

        # Ejecuta la función que guarda la información del usuario
        self.app.save_user_info()

        # Verifica que los datos se guarden correctamente en el archivo user_info.json
        with open("user_info.json", "r") as file:
            user_info = json.load(file)
            self.assertEqual(user_info["nombre"], "John", "El nombre no coincide")
            self.assertEqual(user_info["peso"], "70", "El peso no coincide")
            self.assertEqual(user_info["altura"], "175", "La altura no coincide")

        # Puedes continuar agregando más pruebas para otros métodos de la clase FitnessApp

if __name__ == "__main__":
    unittest.main()
