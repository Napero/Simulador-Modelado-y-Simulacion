"""
Ejemplos predefinidos de sistemas dinámicos para testing.
"""

# Sistemas 2D
EXAMPLES_2D = {
    'lotka_volterra': {
        'name': 'Lotka-Volterra (Presa-Depredador)',
        'dx_dt': 'x*(2-x-y)',
        'dy_dt': 'y*(1-x-0.5*y)',
        'x_range': (-1, 5),
        'y_range': (-1, 5),
        'description': 'Modelo clásico de interacción presa-depredador'
    },
    'pendulo': {
        'name': 'Péndulo Amortiguado',
        'dx_dt': 'y',
        'dy_dt': '-sin(x) - 0.5*y',
        'x_range': (-10, 10),
        'y_range': (-5, 5),
        'description': 'Péndulo con fricción'
    },
    'van_der_pol': {
        'name': 'Oscilador de Van der Pol',
        'dx_dt': 'y',
        'dy_dt': '1*(1-x**2)*y - x',
        'x_range': (-4, 4),
        'y_range': (-4, 4),
        'description': 'Oscilador con amortiguamiento no lineal'
    },
    'competencia': {
        'name': 'Competencia entre Especies',
        'dx_dt': 'x*(3-x-2*y)',
        'dy_dt': 'y*(2-x-y)',
        'x_range': (-1, 5),
        'y_range': (-1, 5),
        'description': 'Dos especies compitiendo por recursos'
    },
    'duffing': {
        'name': 'Ecuación de Duffing',
        'dx_dt': 'y',
        'dy_dt': 'x - x**3',
        'x_range': (-3, 3),
        'y_range': (-3, 3),
        'description': 'Oscilador con resorte no lineal'
    }
}

# Sistemas 1D
EXAMPLES_1D = {
    'cuadratica': {
        'name': 'Ecuación Cuadrática',
        'f': 'x**2 - 4',
        'x_range': (-5, 5),
        'initial_conditions': [-3, -1, 0, 1, 3],
        'description': 'Dos equilibrios estables en x = ±2'
    },
    'logistica': {
        'name': 'Ecuación Logística',
        'f': 'x*(1-x)',
        'x_range': (-1, 2),
        'initial_conditions': [-0.5, 0.2, 0.5, 0.8, 1.5],
        'description': 'Modelo de crecimiento poblacional con capacidad de carga'
    },
    'cubica': {
        'name': 'Ecuación Cúbica',
        'f': 'x**3 - x',
        'x_range': (-2, 2),
        'initial_conditions': [-1.5, -0.5, 0, 0.5, 1.5],
        'description': 'Tres equilibrios: estable-inestable-estable'
    },
    'exponencial': {
        'name': 'Crecimiento Exponencial',
        'f': 'x',
        'x_range': (-3, 3),
        'initial_conditions': [-2, -1, 0, 1, 2],
        'description': 'Crecimiento exponencial simple'
    }
}

# Bifurcaciones
EXAMPLES_BIFURCATION = {
    'saddle_node': {
        'name': 'Bifurcación Saddle-Node',
        'f': 'r + x**2',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Aparición/desaparición de equilibrios en r=0'
    },
    'pitchfork_supercritica': {
        'name': 'Pitchfork Supercrítica',
        'f': 'r*x - x**3',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': '1 equilibrio → 3 equilibrios en r=0'
    },
    'pitchfork_subcritica': {
        'name': 'Pitchfork Subcrítica',
        'f': 'r*x + x**3',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Bifurcación inversa a la supercrítica'
    },
    'transcritica': {
        'name': 'Bifurcación Transcrítica',
        'f': 'r*x - x**2',
        'r_range': (-2, 2),
        'x_range': (-3, 3),
        'r_values': [-1, 0, 1],
        'description': 'Intercambio de estabilidad en r=0'
    }
}


def get_example_2d(key):
    """Obtiene un ejemplo 2D por su clave."""
    return EXAMPLES_2D.get(key, None)


def get_example_1d(key):
    """Obtiene un ejemplo 1D por su clave."""
    return EXAMPLES_1D.get(key, None)


def get_example_bifurcation(key):
    """Obtiene un ejemplo de bifurcación por su clave."""
    return EXAMPLES_BIFURCATION.get(key, None)


def list_examples():
    """Lista todos los ejemplos disponibles."""
    print("=" * 60)
    print("EJEMPLOS DISPONIBLES")
    print("=" * 60)
    
    print("\n📐 SISTEMAS 2D:")
    for key, ex in EXAMPLES_2D.items():
        print(f"  • {key}: {ex['name']}")
    
    print("\n📊 SISTEMAS 1D:")
    for key, ex in EXAMPLES_1D.items():
        print(f"  • {key}: {ex['name']}")
    
    print("\n🔄 BIFURCACIONES:")
    for key, ex in EXAMPLES_BIFURCATION.items():
        print(f"  • {key}: {ex['name']}")
    
    print("=" * 60)


if __name__ == "__main__":
    list_examples()
