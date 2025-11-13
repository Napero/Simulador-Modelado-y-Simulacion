"""
Análisis de sistemas autónomos 1D: dx/dt = f(x)
"""

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

from utils.expression_parser import ExpressionParser


class AutonomousSystem1D:
    """Sistema autónomo 1D: dx/dt = f(x)"""
    
    def __init__(self, f_expr):
        """
        Args:
            f_expr: Expresión string para dx/dt = f(x)
        """
        self.f_expr = f_expr
        
        # Parsear a sympy
        self.f_sympy = ExpressionParser.parse_to_sympy(f_expr, ['x'])
        self.x_symbol = sp.Symbol('x', real=True)
        
        # Crear función numpy
        self.f_func = ExpressionParser.create_numpy_function(f_expr, ['x'])
        
        # Derivada df/dx (para estabilidad)
        self.df_dx_sympy = sp.diff(self.f_sympy, self.x_symbol)
        self.df_dx_func = sp.lambdify(self.x_symbol, self.df_dx_sympy, 'numpy')
        
        self.equilibria = []
    
    def f(self, x):
        """Evalúa f(x)"""
        try:
            result = self.f_func(x)
            if isinstance(result, np.ndarray):
                return result
            return float(result)
        except:
            return 0.0
    
    def df_dx(self, x):
        """Evalúa df/dx en x"""
        try:
            result = self.df_dx_func(x)
            if isinstance(result, np.ndarray):
                return result
            return float(result)
        except:
            return 0.0
    
    def find_equilibria(self, x_range, n_seeds=20):
        """
        Encuentra puntos de equilibrio donde f(x) = 0.
        
        Returns:
            Lista de dict con 'x', 'stability', 'derivative'
        """
        equilibria = []
        found_x = []
        
        x_seeds = np.linspace(x_range[0], x_range[1], n_seeds)
        
        for x0 in x_seeds:
            try:
                x_eq = fsolve(self.f, x0)[0]
                
                # Verificar que es solución
                if abs(self.f(x_eq)) < 1e-6:
                    # Evitar duplicados
                    is_duplicate = any(abs(x_eq - x_f) < 0.01 for x_f in found_x)
                    
                    if not is_duplicate and x_range[0] <= x_eq <= x_range[1]:
                        df = self.df_dx(x_eq)
                        
                        if df < -1e-8:
                            stability = "Estable"
                        elif df > 1e-8:
                            stability = "Inestable"
                        else:
                            stability = "Marginalmente estable"
                        
                        equilibria.append({
                            'x': x_eq,
                            'stability': stability,
                            'derivative': df
                        })
                        found_x.append(x_eq)
            except:
                continue
        
        # Ordenar por x
        equilibria.sort(key=lambda e: e['x'])
        self.equilibria = equilibria
        return equilibria
    
    def solve(self, x0, t_span, n_points=500):
        """
        Resuelve el sistema desde x0.
        
        Returns:
            dict con 't', 'x'
        """
        def derivatives(t, state):
            return [self.f(state[0])]
        
        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        
        try:
            sol = solve_ivp(
                derivatives,
                t_span,
                [x0],
                t_eval=t_eval,
                method='RK45'
            )
            
            return {
                't': sol.t,
                'x': sol.y[0],
                'success': sol.success
            }
        except:
            return {
                't': np.array([t_span[0]]),
                'x': np.array([x0]),
                'success': False
            }


def plot_phase_diagram_1d(system, x_range, ax, log_callback=None):
    """
    Dibuja diagrama de fase 1D: f(x) vs x con equilibrios y flujo.
    """
    def log(msg):
        if log_callback:
            log_callback(msg)
    
    # Curva f(x)
    x = np.linspace(x_range[0], x_range[1], 500)
    
    try:
        y = system.f(x)
    except:
        y = np.array([system.f(xi) for xi in x])
    
    ax.plot(x, y, 'k-', linewidth=2, label='f(x)')
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--', alpha=0.7)
    ax.axvline(0, color='gray', linewidth=0.8, linestyle='--', alpha=0.7)
    
    # Equilibrios
    equilibria = system.find_equilibria(x_range)
    
    log(f"Encontrados {len(equilibria)} equilibrios:")
    
    for eq in equilibria:
        x_eq = eq['x']
        stability = eq['stability']
        derivative = eq['derivative']
        
        log(f"  x = {x_eq:.4f}: {stability} (f'(x) = {derivative:.4f})")
        
        if stability == "Estable":
            ax.scatter(x_eq, 0, c='green', s=200, marker='o',
                      edgecolors='black', linewidths=2, zorder=10,
                      label='Estable' if eq == equilibria[0] else '')
        else:
            ax.scatter(x_eq, 0, c='red', s=200, marker='o',
                      facecolors='none', edgecolors='red',
                      linewidths=2, zorder=10,
                      label='Inestable' if eq == equilibria[0] else '')
    
    # Flechas de flujo en eje x
    arrow_x = np.linspace(x_range[0], x_range[1], 15)
    for xi in arrow_x:
        f_val = system.f(xi)
        
        if abs(f_val) > 0.01:  # No dibujar cerca de equilibrios
            direction = 1 if f_val > 0 else -1
            dx = 0.15 * direction
            
            ax.arrow(xi, -0.05, dx, 0,
                    head_width=0.05, head_length=0.08,
                    fc='blue', ec='blue',
                    linewidth=1.5, alpha=0.6)
    
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('dx/dt = f(x)', fontsize=12)
    ax.set_title('Diagrama de Fase 1D', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.legend()


def plot_solutions_1d(system, initial_conditions, t_range, ax):
    """
    Grafica soluciones x(t) vs t para múltiples condiciones iniciales.
    """
    colors = plt.cm.tab10.colors
    
    for idx, x0 in enumerate(initial_conditions):
        sol = system.solve(x0, t_range)
        
        if sol['success']:
            color = colors[idx % len(colors)]
            ax.plot(sol['t'], sol['x'], color=color,
                   linewidth=2, alpha=0.8,
                   label=f'x₀ = {x0:.2f}')
    
    ax.set_xlabel('t', fontsize=12)
    ax.set_ylabel('x(t)', fontsize=12)
    ax.set_title('Soluciones x(t)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.legend()
