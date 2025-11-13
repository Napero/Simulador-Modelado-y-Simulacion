"""
Análisis de bifurcaciones 1D con sympy.
Tipos: Saddle-Node, Pitchfork, Transcrítica
"""

import numpy as np
import sympy as sp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

from utils.expression_parser import ExpressionParser


class BifurcationAnalyzer1D:
    """Analizador de bifurcaciones para sistemas 1D: dx/dt = f(x, r)"""
    
    def __init__(self, f_expr, param_name='r'):
        """
        Args:
            f_expr: Expresión string f(x, r)
            param_name: Nombre del parámetro de bifurcación
        """
        self.f_expr = f_expr
        self.param_name = param_name
        
        # Parsear expresión
        self.f_sympy = ExpressionParser.parse_to_sympy(f_expr, ['x', param_name])
        self.x_symbol = sp.Symbol('x', real=True)
        self.r_symbol = sp.Symbol(param_name, real=True)
        
        # Derivada respecto a x (para estabilidad)
        self.df_dx_sympy = sp.diff(self.f_sympy, self.x_symbol)
        
        # Crear funciones numéricas
        self.f_func = sp.lambdify((self.x_symbol, self.r_symbol),
                                  self.f_sympy, 'numpy')
        self.df_dx_func = sp.lambdify((self.x_symbol, self.r_symbol),
                                      self.df_dx_sympy, 'numpy')
        
        self.branches = []
        self.bifurcation_points = []
    
    def f(self, x, r):
        """Evalúa f(x, r)"""
        try:
            return float(self.f_func(x, r))
        except:
            return 0.0
    
    def df_dx(self, x, r):
        """Evalúa df/dx en (x, r)"""
        try:
            return float(self.df_dx_func(x, r))
        except:
            return 0.0
    
    def find_equilibria_at_r(self, r_value, x_range, n_seeds=30):
        """
        Encuentra equilibrios para un valor fijo de r.
        
        Returns:
            Lista de dict con 'x', 'stability', 'derivative'
        """
        equilibria = []
        found_x = []
        
        x_seeds = np.linspace(x_range[0], x_range[1], n_seeds)
        
        def equation(x):
            return self.f(x, r_value)
        
        for x0 in x_seeds:
            try:
                x_eq = fsolve(equation, x0)[0]
                
                if abs(equation(x_eq)) < 1e-6:
                    is_duplicate = any(abs(x_eq - x_f) < 0.05 for x_f in found_x)
                    
                    if not is_duplicate and x_range[0] <= x_eq <= x_range[1]:
                        df = self.df_dx(x_eq, r_value)
                        
                        if df < -1e-8:
                            stability = "stable"
                        elif df > 1e-8:
                            stability = "unstable"
                        else:
                            stability = "marginal"
                        
                        equilibria.append({
                            'x': x_eq,
                            'stability': stability,
                            'derivative': df
                        })
                        found_x.append(x_eq)
            except:
                continue
        
        return equilibria
    
    def compute_bifurcation_diagram(self, r_range, x_range, n_points=200):
        """
        Calcula diagrama de bifurcación completo.
        
        Returns:
            Lista de ramas (branches), cada una con:
            - 'r_values': array de r
            - 'x_values': array de x
            - 'stability': 'stable' o 'unstable'
        """
        r_values = np.linspace(r_range[0], r_range[1], n_points)
        
        # Estructura para almacenar ramas
        all_equilibria = []
        
        for r in r_values:
            eq_at_r = self.find_equilibria_at_r(r, x_range)
            for eq in eq_at_r:
                all_equilibria.append({
                    'r': r,
                    'x': eq['x'],
                    'stability': eq['stability']
                })
        
        # Agrupar en ramas continuas
        branches = self._track_branches(all_equilibria, r_values)
        self.branches = branches
        
        return branches
    
    def _track_branches(self, equilibria, r_values):
        """
        Agrupa equilibrios en ramas continuas.
        """
        if not equilibria:
            return []
        
        # Organizar por r
        eq_by_r = {}
        for eq in equilibria:
            r = eq['r']
            if r not in eq_by_r:
                eq_by_r[r] = []
            eq_by_r[r].append(eq)
        
        # Ordenar cada lista por x
        for r in eq_by_r:
            eq_by_r[r].sort(key=lambda e: e['x'])
        
        # Inicializar ramas
        branches = []
        used = set()
        
        for r in sorted(eq_by_r.keys()):
            for eq in eq_by_r[r]:
                if (r, eq['x']) in used:
                    continue
                
                # Nueva rama
                branch = {
                    'r_values': [r],
                    'x_values': [eq['x']],
                    'stability': eq['stability']
                }
                used.add((r, eq['x']))
                
                # Extender rama hacia adelante
                current_x = eq['x']
                for r_next in sorted([rn for rn in eq_by_r.keys() if rn > r]):
                    # Buscar equilibrio más cercano
                    candidates = eq_by_r[r_next]
                    if not candidates:
                        break
                    
                    closest = min(candidates, key=lambda e: abs(e['x'] - current_x))
                    
                    # Si está muy lejos, terminar rama
                    if abs(closest['x'] - current_x) > 0.5:
                        break
                    
                    if (r_next, closest['x']) not in used:
                        branch['r_values'].append(r_next)
                        branch['x_values'].append(closest['x'])
                        used.add((r_next, closest['x']))
                        current_x = closest['x']
                
                if len(branch['r_values']) > 1:
                    branches.append(branch)
        
        return branches
    
    def detect_bifurcations(self, r_range, x_range):
        """
        Detecta puntos de bifurcación y clasifica el tipo.
        
        Returns:
            Lista de dict con 'r', 'type', 'description'
        """
        r_values = np.linspace(r_range[0], r_range[1], 100)
        
        bifurcations = []
        prev_n_eq = None
        
        for r in r_values:
            eq = self.find_equilibria_at_r(r, x_range)
            n_eq = len(eq)
            
            if prev_n_eq is not None and n_eq != prev_n_eq:
                # Cambio en número de equilibrios -> bifurcación
                
                if prev_n_eq < n_eq:
                    # Aparecen equilibrios
                    if n_eq - prev_n_eq == 2:
                        bif_type = "Saddle-Node"
                        description = f"Aparecen {n_eq - prev_n_eq} equilibrios"
                    elif prev_n_eq == 1 and n_eq == 3:
                        bif_type = "Pitchfork"
                        description = "1 equilibrio → 3 equilibrios"
                    else:
                        bif_type = "Desconocido"
                        description = f"{prev_n_eq} → {n_eq} equilibrios"
                else:
                    # Desaparecen equilibrios
                    if prev_n_eq - n_eq == 2:
                        bif_type = "Saddle-Node"
                        description = f"Desaparecen {prev_n_eq - n_eq} equilibrios"
                    elif prev_n_eq == 3 and n_eq == 1:
                        bif_type = "Pitchfork"
                        description = "3 equilibrios → 1 equilibrio"
                    else:
                        bif_type = "Desconocido"
                        description = f"{prev_n_eq} → {n_eq} equilibrios"
                
                bifurcations.append({
                    'r': r,
                    'type': bif_type,
                    'description': description,
                    'prev_n_eq': prev_n_eq,
                    'n_eq': n_eq
                })
            
            prev_n_eq = n_eq
        
        self.bifurcation_points = bifurcations
        return bifurcations


def plot_bifurcation_diagram(analyzer, r_range, x_range, ax, log_callback=None):
    """
    Dibuja diagrama de bifurcación.
    """
    def log(msg):
        if log_callback:
            log_callback(msg)
    
    log("Calculando diagrama de bifurcación...")
    
    # Calcular ramas
    branches = analyzer.compute_bifurcation_diagram(r_range, x_range)
    
    # Dibujar cada rama
    for branch in branches:
        r_vals = np.array(branch['r_values'])
        x_vals = np.array(branch['x_values'])
        stability = branch['stability']
        
        if stability == "stable":
            ax.plot(r_vals, x_vals,
                   linestyle='solid',
                   linewidth=2.0,
                   color='blue',
                   alpha=0.8)
        else:
            ax.plot(r_vals, x_vals,
                   linestyle='dotted',
                   linewidth=2.0,
                   color='red',
                   alpha=0.8)
    
    # Detectar y marcar bifurcaciones
    log("Detectando bifurcaciones...")
    bifurcations = analyzer.detect_bifurcations(r_range, x_range)
    
    log(f"Encontradas {len(bifurcations)} bifurcaciones:")
    
    for bif in bifurcations:
        r_bif = bif['r']
        bif_type = bif['type']
        description = bif['description']
        
        log(f"  r ≈ {r_bif:.3f}: {bif_type} - {description}")
        
        ax.axvline(r_bif, color='orange', linestyle='--',
                  alpha=0.7, linewidth=2)
        
        # Etiqueta
        y_pos = (x_range[0] + x_range[1]) / 2
        ax.text(r_bif, y_pos, f'r≈{r_bif:.2f}\n{bif_type}',
               bbox=dict(boxstyle='round,pad=0.3',
                        facecolor='orange', alpha=0.7),
               fontsize=9, ha='center')
    
    ax.set_xlabel(f'{analyzer.param_name}', fontsize=12)
    ax.set_ylabel('x*', fontsize=12)
    ax.set_title('Diagrama de Bifurcación', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    
    # Leyenda
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='blue', linewidth=2, label='Estable'),
        Line2D([0], [0], color='red', linewidth=2, linestyle=':', label='Inestable'),
        Line2D([0], [0], color='orange', linewidth=2, linestyle='--', label='Bifurcación')
    ]
    ax.legend(handles=legend_elements, loc='best')


def plot_phase_diagrams_at_r(analyzer, r_values, x_range, axes, log_callback=None):
    """
    Dibuja diagramas de fase para valores específicos de r.
    
    Args:
        r_values: Lista de valores de r
        axes: Lista de matplotlib axes (uno por cada r)
    """
    from core.systems_1d import AutonomousSystem1D, plot_phase_diagram_1d
    
    for idx, r_val in enumerate(r_values):
        if idx >= len(axes):
            break
        
        ax = axes[idx]
        
        # Crear expresión con r fijo
        f_expr_at_r = str(analyzer.f_sympy.subs(analyzer.r_symbol, r_val))
        
        # Crear sistema 1D
        system = AutonomousSystem1D(f_expr_at_r)
        
        # Dibujar diagrama de fase
        plot_phase_diagram_1d(system, x_range, ax, log_callback)
        ax.set_title(f'Diagrama de Fase (r = {r_val:.2f})',
                    fontsize=12, fontweight='bold')
