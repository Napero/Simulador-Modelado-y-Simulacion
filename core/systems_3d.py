"""
Módulo para sistemas dinámicos 3D (como Lorenz).
"""

import numpy as np
from scipy.integrate import solve_ivp
from utils.expression_parser import ExpressionParser


class System3D:
    """Sistema dinámico 3D genérico."""
    
    def __init__(self, dx_expr, dy_expr, dz_expr):
        """
        Args:
            dx_expr: Expresión para dx/dt
            dy_expr: Expresión para dy/dt
            dz_expr: Expresión para dz/dt
        """
        self.dx_expr = dx_expr
        self.dy_expr = dy_expr
        self.dz_expr = dz_expr
        
        # Compilar expresiones
        self.dx_func = ExpressionParser.create_numpy_function(dx_expr, ['x', 'y', 'z'])
        self.dy_func = ExpressionParser.create_numpy_function(dy_expr, ['x', 'y', 'z'])
        self.dz_func = ExpressionParser.create_numpy_function(dz_expr, ['x', 'y', 'z'])
    
    def derivatives(self, t, state):
        """Calcula las derivadas."""
        x, y, z = state
        
        dx = self.dx_func(x, y, z)
        dy = self.dy_func(x, y, z)
        dz = self.dz_func(x, y, z)
        
        return [dx, dy, dz]
    
    def solve(self, initial_condition, t_span, t_eval=None):
        """
        Resuelve el sistema.
        
        Args:
            initial_condition: (x0, y0, z0)
            t_span: (t_start, t_end)
            t_eval: Puntos de tiempo donde evaluar
        
        Returns:
            Objeto solution de solve_ivp
        """
        if t_eval is None:
            t_eval = np.linspace(t_span[0], t_span[1], 5000)
        
        sol = solve_ivp(
            self.derivatives,
            t_span,
            initial_condition,
            t_eval=t_eval,
            method='RK45',
            dense_output=True,
            max_step=0.01
        )
        
        return sol


class LorenzSystem(System3D):
    """Sistema de Lorenz clásico."""
    
    def __init__(self, sigma=10, rho=28, beta=8/3):
        """
        Sistema de Lorenz:
            dx/dt = σ(y - x)
            dy/dt = x(ρ - z) - y
            dz/dt = xy - βz
        
        Args:
            sigma: Parámetro σ (razón de Prandtl)
            rho: Parámetro ρ (número de Rayleigh)
            beta: Parámetro β (relacionado con geometría)
        """
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        
        # No usar ExpressionParser para Lorenz (más eficiente directo)
        self.dx_expr = f"{sigma}*(y - x)"
        self.dy_expr = f"x*({rho} - z) - y"
        self.dz_expr = f"x*y - {beta}*z"
    
    def derivatives(self, t, state):
        """Calcula las derivadas del sistema de Lorenz."""
        x, y, z = state
        
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        
        return [dx, dy, dz]
    
    def find_equilibria(self):
        """
        Encuentra puntos de equilibrio del sistema de Lorenz.
        
        Returns:
            Lista de tuplas (x, y, z) con los equilibrios
        """
        equilibria = []
        
        # Equilibrio trivial en el origen
        equilibria.append((0, 0, 0))
        
        # Equilibrios no triviales (si ρ > 1)
        if self.rho > 1:
            val = np.sqrt(self.beta * (self.rho - 1))
            equilibria.append((val, val, self.rho - 1))
            equilibria.append((-val, -val, self.rho - 1))
        
        return equilibria


def render_3d_trajectory(system, initial_conditions, t_span, ax, log_callback=None):
    """
    Renderiza trayectorias 3D.
    
    Args:
        system: Sistema 3D
        initial_conditions: Lista de tuplas (x0, y0, z0)
        t_span: (t_start, t_end)
        ax: Axes 3D de matplotlib
        log_callback: Función para logging
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(initial_conditions)))
    
    for idx, ic in enumerate(initial_conditions):
        try:
            sol = system.solve(ic, t_span)
            
            if sol.success:
                x, y, z = sol.y
                ax.plot(x, y, z, color=colors[idx], alpha=0.7, linewidth=0.8)
                
                # Marcar punto inicial
                ax.scatter(*ic, color=colors[idx], s=50, marker='o', 
                          edgecolors='black', linewidths=1, zorder=10)
        except Exception as e:
            if log_callback:
                log_callback(f"Error en trayectoria desde {ic}: {e}")
    
    ax.set_xlabel('X', fontsize=10, fontweight='bold')
    ax.set_ylabel('Y', fontsize=10, fontweight='bold')
    ax.set_zlabel('Z', fontsize=10, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Estilo
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('gray')
    ax.yaxis.pane.set_edgecolor('gray')
    ax.zaxis.pane.set_edgecolor('gray')


class RosslerSystem(System3D):
    """Sistema de Rössler (atractor caótico)."""
    
    def __init__(self, a=0.2, b=0.2, c=5.7):
        self.a = a
        self.b = b
        self.c = c
        
        dx_expr = f"-y - z"
        dy_expr = f"x + {a}*y"
        dz_expr = f"{b} + z*(x - {c})"
        
        super().__init__(dx_expr, dy_expr, dz_expr)
    
    def find_equilibria(self):
        """Encuentra equilibrios del sistema de Rössler."""
        a, b, c = self.a, self.b, self.c
        
        # Equilibrio: x* = (c ± √(c²-4ab))/2
        discriminant = c**2 - 4*a*b
        
        equilibria = []
        if discriminant >= 0:
            x1 = (c + np.sqrt(discriminant)) / 2
            y1 = -x1 / a
            z1 = -x1 / a
            equilibria.append((x1, y1, z1))
            
            if discriminant > 0:
                x2 = (c - np.sqrt(discriminant)) / 2
                y2 = -x2 / a
                z2 = -x2 / a
                equilibria.append((x2, y2, z2))
        
        return equilibria


class ChuaSystem(System3D):
    """Sistema de Chua (circuito caótico)."""
    
    def __init__(self, alpha=15.6, beta=28, m0=-1.143, m1=-0.714):
        self.alpha = alpha
        self.beta = beta
        self.m0 = m0
        self.m1 = m1
        
        # Chua usa una función no lineal especial
        dx_expr = "custom"
        dy_expr = "custom"
        dz_expr = "custom"
        
        super().__init__(dx_expr, dy_expr, dz_expr)
    
    def h_function(self, x):
        """Función no lineal de Chua: h(x) = m1*x + 0.5*(m0-m1)*(|x+1|-|x-1|)"""
        return self.m1 * x + 0.5 * (self.m0 - self.m1) * (np.abs(x + 1) - np.abs(x - 1))
    
    def derivatives(self, t, state):
        """Derivadas del sistema de Chua."""
        x, y, z = state
        
        dx = self.alpha * (y - x - self.h_function(x))
        dy = x - y + z
        dz = -self.beta * y
        
        return [dx, dy, dz]
    
    def find_equilibria(self):
        """Solo el origen es equilibrio para parámetros típicos."""
        return [(0, 0, 0)]


class SprottSystem(System3D):
    """Sistema de Sprott (caos simple)."""
    
    def __init__(self, system_type='B'):
        """
        Args:
            system_type: 'A', 'B', 'C', etc. (diferentes sistemas de Sprott)
        """
        self.system_type = system_type
        
        # Sistema Sprott B (uno de los más simples)
        if system_type == 'B':
            dx_expr = "y*z"
            dy_expr = "x - y"
            dz_expr = "1 - x*y"
        elif system_type == 'C':
            dx_expr = "y*z"
            dy_expr = "x - y"
            dz_expr = "1 - x**2"
        elif system_type == 'D':
            dx_expr = "-y"
            dy_expr = "x + z"
            dz_expr = "x*z + 3*y**2"
        else:  # Default a B
            dx_expr = "y*z"
            dy_expr = "x - y"
            dz_expr = "1 - x*y"
        
        super().__init__(dx_expr, dy_expr, dz_expr)
    
    def find_equilibria(self):
        """Equilibrios dependen del tipo de sistema."""
        if self.system_type == 'B':
            return [(1, 1, 1)]
        elif self.system_type == 'C':
            return [(1, 1, 0), (-1, -1, 0)]
        else:
            return [(0, 0, 0)]
