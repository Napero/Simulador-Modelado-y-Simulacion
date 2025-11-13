"""
Parser de expresiones matemáticas con soporte para lenguaje natural.
Convierte expresiones como 'ln(2*x*pi)' a formato evaluable.
"""

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
    function_exponentiation
)


class ExpressionParser:
    """Parser robusto para expresiones matemáticas."""
    
    # Constantes matemáticas disponibles
    CONSTANTS = {
        'pi': np.pi,
        'e': np.e,
        'tau': 2 * np.pi,
        'inf': np.inf,
        'nan': np.nan
    }
    
    # Funciones matemáticas disponibles
    FUNCTIONS = {
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'arcsin': np.arcsin,
        'arccos': np.arccos,
        'arctan': np.arctan,
        'sinh': np.sinh,
        'cosh': np.cosh,
        'tanh': np.tanh,
        'exp': np.exp,
        'log': np.log,  # logaritmo natural
        'ln': np.log,   # alias para log natural
        'log10': np.log10,
        'sqrt': np.sqrt,
        'abs': np.abs,
        'sign': np.sign,
    }
    
    @staticmethod
    def normalize_expression(expr_str):
        """
        Normaliza una expresión matemática para ser parseada.
        
        Conversiones:
        - 'ln' -> 'log'
        - Espacios innecesarios
        - Multiplicación implícita: '2x' -> '2*x', '2pi' -> '2*pi'
        """
        if not expr_str or not isinstance(expr_str, str):
            return expr_str
            
        expr = expr_str.strip()
        
        # Reemplazar 'ln' por 'log' (ambos se mapean a np.log)
        # pero sympy prefiere 'log'
        expr = expr.replace('ln', 'log')
        
        # Limpiar espacios alrededor de operadores
        for op in ['+', '-', '*', '/', '**', '^']:
            expr = expr.replace(f' {op} ', op)
        
        return expr
    
    @staticmethod
    def parse_to_sympy(expr_str, variables=None):
        """
        Parsea una expresión a sympy con transformaciones avanzadas.
        
        Args:
            expr_str: Expresión matemática como string
            variables: Lista de nombres de variables (ej: ['x', 'y', 't'])
        
        Returns:
            Expresión de sympy
        """
        if not expr_str:
            return None
            
        expr = ExpressionParser.normalize_expression(expr_str)
        
        # Definir variables simbólicas
        if variables:
            local_dict = {var: sp.Symbol(var, real=True) for var in variables}
        else:
            local_dict = {}
        
        # Agregar constantes
        local_dict.update({
            'pi': sp.pi,
            'e': sp.E,
            'I': sp.I,
        })
        
        # Transformaciones para parseo flexible
        transformations = (
            standard_transformations +
            (implicit_multiplication_application,
             convert_xor,
             function_exponentiation)
        )
        
        try:
            sympy_expr = parse_expr(
                expr,
                local_dict=local_dict,
                transformations=transformations,
                evaluate=True
            )
            return sympy_expr
        except Exception as e:
            raise ValueError(f"Error parseando expresión '{expr_str}': {str(e)}")
    
    @staticmethod
    def create_numpy_function(expr_str, variables):
        """
        Crea una función numpy evaluable desde una expresión string.
        
        Args:
            expr_str: Expresión matemática
            variables: Lista de variables ['x', 'y'] o ['x', 't']
        
        Returns:
            Función lambda que acepta arrays numpy
        """
        sympy_expr = ExpressionParser.parse_to_sympy(expr_str, variables)
        
        if sympy_expr is None:
            return lambda *args: np.zeros_like(args[0])
        
        # Convertir símbolos de sympy a objetos Symbol
        syms = [sp.Symbol(v, real=True) for v in variables]
        
        # Lambdify: convierte expresión sympy a función numpy
        numpy_func = sp.lambdify(
            syms,
            sympy_expr,
            modules=['numpy', ExpressionParser.FUNCTIONS]
        )
        
        return numpy_func
    
    @staticmethod
    def create_scalar_function(expr_str, variables):
        """
        Crea función para valores escalares (usado en fsolve, nsolve).
        """
        sympy_expr = ExpressionParser.parse_to_sympy(expr_str, variables)
        
        if sympy_expr is None:
            return lambda *args: 0.0
        
        syms = [sp.Symbol(v, real=True) for v in variables]
        
        scalar_func = sp.lambdify(
            syms,
            sympy_expr,
            modules=['math', {'ln': np.log}]
        )
        
        return scalar_func
    
    @staticmethod
    def validate_expression(expr_str, variables):
        """
        Valida que una expresión sea parseable y evaluable.
        
        Returns:
            (is_valid, error_message)
        """
        try:
            ExpressionParser.parse_to_sympy(expr_str, variables)
            return True, ""
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_help_text():
        """Retorna texto de ayuda para el usuario."""
        return """
Funciones disponibles:
  • Trigonométricas: sin, cos, tan, arcsin, arccos, arctan
  • Hiperbólicas: sinh, cosh, tanh
  • Exponencial/Logaritmo: exp, log, ln, log10
  • Otras: sqrt, abs, sign

Constantes:
  • pi, e, tau

Operadores:
  • Básicos: +, -, *, /
  • Potencia: ** o ^
  • Multiplicación implícita: 2x = 2*x, 2pi = 2*pi

Ejemplos válidos:
  • x**2 - 4
  • sin(2*pi*x)
  • ln(x + 1) - y**2
  • exp(-0.5*x)*cos(pi*t)
  • x*(2-x-y)
"""


def test_parser():
    """Función de testing."""
    parser = ExpressionParser()
    
    test_cases = [
        ("ln(2*x*pi)", ['x']),
        ("sin(pi*x) + cos(2*pi*y)", ['x', 'y']),
        ("x**2 - 4", ['x']),
        ("exp(-t)*sin(2*pi*t)", ['t']),
        ("2x + 3y", ['x', 'y']),
    ]
    
    print("Testing Expression Parser:")
    print("=" * 50)
    
    for expr_str, vars in test_cases:
        print(f"\nExpresión: {expr_str}")
        print(f"Variables: {vars}")
        
        try:
            sympy_expr = parser.parse_to_sympy(expr_str, vars)
            print(f"✓ Sympy: {sympy_expr}")
            
            func = parser.create_numpy_function(expr_str, vars)
            test_vals = [1.0] * len(vars)
            result = func(*test_vals)
            print(f"✓ Evaluación en {test_vals}: {result}")
            
        except Exception as e:
            print(f"✗ Error: {e}")


if __name__ == "__main__":
    test_parser()
