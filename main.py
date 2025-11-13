"""
Punto de entrada principal de la aplicación.
Simulador de Sistemas Dinámicos - Modelado y Simulación
"""

import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import main

if __name__ == "__main__":
    print("=" * 60)
    print("🌀 SIMULADOR DE SISTEMAS DINÁMICOS")
    print("   Modelado y Simulación")
    print("=" * 60)
    print("\nIniciando aplicación...")
    print("Asegúrate de tener instaladas las dependencias:")
    print("  pip install -r requirements.txt")
    print("\n" + "=" * 60 + "\n")
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
