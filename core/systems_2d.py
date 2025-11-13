"""
Motor de simulación para sistemas dinámicos 2D.
Incluye análisis de equilibrio, nullclines, y renderizado de plano de fase.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from abc import ABC, abstractmethod
import warnings

from utils.expression_parser import ExpressionParser


class DynamicSystem2D(ABC):
    """Clase base abstracta para sistemas dinámicos 2D."""
    
    def __init__(self):
        self.equilibria = []
        self.nullclines = None
        
    @abstractmethod
    def f(self, x, y):
        """dx/dt = f(x, y)"""
        pass
    
    @abstractmethod
    def g(self, x, y):
        """dy/dt = g(x, y)"""
        pass
    
    def derivatives(self, t, state):
        """Para solve_ivp: [dx/dt, dy/dt]"""
        x, y = state
        return [self.f(x, y), self.g(x, y)]
    
    def find_equilibria(self, x_range, y_range, n_seeds=20):
        """
        Encuentra puntos de equilibrio donde f=0 y g=0.
        
        Args:
            x_range: (x_min, x_max)
            y_range: (y_min, y_max)
            n_seeds: Número de puntos iniciales para búsqueda
        
        Returns:
            Lista de tuplas (x_eq, y_eq, classification)
        """
        equilibria = []
        found_points = []
        
        # Generar semillas en grid
        x_seeds = np.linspace(x_range[0], x_range[1], int(np.sqrt(n_seeds)))
        y_seeds = np.linspace(y_range[0], y_range[1], int(np.sqrt(n_seeds)))
        
        def system(point):
            x, y = point
            return [self.f(x, y), self.g(x, y)]
        
        for x0 in x_seeds:
            for y0 in y_seeds:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        sol = fsolve(system, [x0, y0], full_output=True)
                        x_eq, y_eq = sol[0]
                        info = sol[1]
                        
                        # Verificar que es solución válida
                        if info['fvec'][0]**2 + info['fvec'][1]**2 < 1e-6:
                            # Evitar duplicados
                            is_duplicate = False
                            for (x_f, y_f, _) in found_points:
                                if abs(x_eq - x_f) < 0.01 and abs(y_eq - y_f) < 0.01:
                                    is_duplicate = True
                                    break
                            
                            if not is_duplicate:
                                classification = self.classify_equilibrium(x_eq, y_eq)
                                found_points.append((x_eq, y_eq, classification))
                                equilibria.append({
                                    'point': (x_eq, y_eq),
                                    'type': classification['type'],
                                    'stability': classification['stability'],
                                    'eigenvalues': classification['eigenvalues']
                                })
                except:
                    continue
        
        self.equilibria = equilibria
        return equilibria
    
    def classify_equilibrium(self, x_eq, y_eq, epsilon=1e-5):
        """
        Clasifica un punto de equilibrio por sus autovalores.
        
        Returns:
            dict con 'type', 'stability', 'eigenvalues', 'eigenvectors'
        """
        # Calcular Jacobiano numéricamente
        J = self.compute_jacobian(x_eq, y_eq, epsilon)
        
        # Autovalores y autovectores
        eigenvalues, eigenvectors = np.linalg.eig(J)
        
        # Clasificación
        lambda1, lambda2 = eigenvalues
        
        # Determinar tipo
        if np.iscomplex(lambda1) or np.iscomplex(lambda2):
            real_part = np.real(lambda1)
            if abs(real_part) < 1e-8:
                eq_type = "Centro"
                stability = "Marginalmente estable"
            elif real_part < 0:
                eq_type = "Foco espiral"
                stability = "Estable"
            else:
                eq_type = "Foco espiral"
                stability = "Inestable"
        else:
            # Autovalores reales
            lambda1, lambda2 = np.real(lambda1), np.real(lambda2)
            
            if lambda1 * lambda2 > 0:
                # Mismo signo -> Nodo
                if lambda1 < 0 and lambda2 < 0:
                    eq_type = "Nodo"
                    stability = "Estable"
                else:
                    eq_type = "Nodo"
                    stability = "Inestable"
            else:
                # Signos opuestos -> Punto de silla
                eq_type = "Punto de silla"
                stability = "Inestable"
        
        return {
            'type': eq_type,
            'stability': stability,
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'jacobian': J
        }
    
    def compute_jacobian(self, x, y, epsilon=1e-5):
        """Calcula el Jacobiano numéricamente."""
        J = np.zeros((2, 2))
        
        # ∂f/∂x
        J[0, 0] = (self.f(x + epsilon, y) - self.f(x - epsilon, y)) / (2 * epsilon)
        # ∂f/∂y
        J[0, 1] = (self.f(x, y + epsilon) - self.f(x, y - epsilon)) / (2 * epsilon)
        # ∂g/∂x
        J[1, 0] = (self.g(x + epsilon, y) - self.g(x - epsilon, y)) / (2 * epsilon)
        # ∂g/∂y
        J[1, 1] = (self.g(x, y + epsilon) - self.g(x, y - epsilon)) / (2 * epsilon)
        
        return J
    
    def compute_nullclines(self, x_range, y_range, n_points=100):
        """
        Calcula nullclines (isoclinas donde dx/dt=0 o dy/dt=0).
        
        Returns:
            dict con 'X', 'Y', 'F', 'G'
        """
        x = np.linspace(x_range[0], x_range[1], n_points)
        y = np.linspace(y_range[0], y_range[1], n_points)
        X, Y = np.meshgrid(x, y)
        
        # Evaluar derivadas en grid
        F = np.zeros_like(X)
        G = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                try:
                    F[i, j] = self.f(X[i, j], Y[i, j])
                    G[i, j] = self.g(X[i, j], Y[i, j])
                except:
                    F[i, j] = np.nan
                    G[i, j] = np.nan
        
        self.nullclines = {'X': X, 'Y': Y, 'F': F, 'G': G}
        return self.nullclines
    
    def simulate_trajectory(self, x0, y0, t_span, method='RK45', 
                          rtol=1e-6, atol=1e-9, n_points=1000):
        """
        Simula una trayectoria desde (x0, y0).
        
        Returns:
            dict con 't', 'x', 'y'
        """
        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        
        try:
            sol = solve_ivp(
                self.derivatives,
                t_span,
                [x0, y0],
                method=method,
                t_eval=t_eval,
                rtol=rtol,
                atol=atol
            )
            
            return {
                't': sol.t,
                'x': sol.y[0],
                'y': sol.y[1],
                'success': sol.success
            }
        except Exception as e:
            print(f"Error en simulación: {e}")
            return {
                't': np.array([t_span[0]]),
                'x': np.array([x0]),
                'y': np.array([y0]),
                'success': False
            }


class CustomSystem2D(DynamicSystem2D):
    """Sistema 2D definido por expresiones matemáticas."""
    
    def __init__(self, f_expr, g_expr):
        """
        Args:
            f_expr: Expresión string para dx/dt
            g_expr: Expresión string para dy/dt
        """
        super().__init__()
        self.f_expr = f_expr
        self.g_expr = g_expr
        
        # Parsear expresiones
        self.f_func = ExpressionParser.create_numpy_function(f_expr, ['x', 'y'])
        self.g_func = ExpressionParser.create_numpy_function(g_expr, ['x', 'y'])
    
    def f(self, x, y):
        """dx/dt"""
        try:
            return float(self.f_func(x, y))
        except:
            return 0.0
    
    def g(self, x, y):
        """dy/dt"""
        try:
            return float(self.g_func(x, y))
        except:
            return 0.0


class LinearSystem2D(DynamicSystem2D):
    """Sistema lineal: X' = A*X + b"""
    
    def __init__(self, A, b=None):
        """
        Args:
            A: Matriz 2x2
            b: Vector 2x1 (opcional, default [0, 0])
        """
        super().__init__()
        self.A = np.array(A, dtype=float)
        self.b = np.array(b if b is not None else [0, 0], dtype=float)
        
        # Calcular autovalores/autovectores
        self.eigenvalues, self.eigenvectors = np.linalg.eig(self.A)
        
        # Punto de equilibrio (si b es constante)
        try:
            self.equilibrium_point = np.linalg.solve(self.A, -self.b)
        except:
            self.equilibrium_point = None
    
    def f(self, x, y):
        """dx/dt"""
        state = np.array([x, y])
        result = self.A[0, :] @ state + self.b[0]
        return float(result)
    
    def g(self, x, y):
        """dy/dt"""
        state = np.array([x, y])
        result = self.A[1, :] @ state + self.b[1]
        return float(result)


def render_phase_plot(system, config, ax, log_callback=None):
    """
    Función centralizada para renderizar plano de fase.
    
    Args:
        system: Instancia de DynamicSystem2D
        config: dict con configuración (ranges, trajectories, etc.)
        ax: matplotlib axes
        log_callback: función para logging
    """
    def log(msg):
        if log_callback:
            log_callback(msg)
    
    x_range = config.get('x_range', (-5, 5))
    y_range = config.get('y_range', (-5, 5))
    show_field = config.get('show_field', True)
    show_nullclines = config.get('show_nullclines', True)
    show_equilibria = config.get('show_equilibria', True)
    show_eigenvectors = config.get('show_eigenvectors', True)
    trajectories = config.get('trajectories', [])
    
    # 1. Campo vectorial
    if show_field:
        log("Graficando campo vectorial...")
        n_arrows = 20
        x = np.linspace(x_range[0], x_range[1], n_arrows)
        y = np.linspace(y_range[0], y_range[1], n_arrows)
        X, Y = np.meshgrid(x, y)
        
        U = np.zeros_like(X)
        V = np.zeros_like(X)
        
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                U[i, j] = system.f(X[i, j], Y[i, j])
                V[i, j] = system.g(X[i, j], Y[i, j])
        
        # Normalizar vectores
        M = np.sqrt(U**2 + V**2)
        M[M == 0] = 1  # Evitar división por cero
        U_norm = U / M
        V_norm = V / M
        
        ax.quiver(X, Y, U_norm, V_norm, M,
                 cmap='gray',
                 alpha=0.6,
                 scale=30,
                 width=0.003)
    
    # 2. Nullclines
    if show_nullclines:
        log("Calculando nullclines...")
        nullclines = system.compute_nullclines(x_range, y_range)
        
        # dx/dt = 0 (roja)
        ax.contour(nullclines['X'], nullclines['Y'], nullclines['F'],
                  levels=[0],
                  colors='red',
                  linewidths=2,
                  linestyles='--',
                  alpha=0.7)
        
        # dy/dt = 0 (azul)
        ax.contour(nullclines['X'], nullclines['Y'], nullclines['G'],
                  levels=[0],
                  colors='blue',
                  linewidths=2,
                  linestyles='--',
                  alpha=0.7)
    
    # 3. Puntos de equilibrio
    if show_equilibria:
        log("Buscando puntos de equilibrio...")
        equilibria = system.find_equilibria(x_range, y_range)
        
        log(f"  Encontrados: {len(equilibria)} equilibrios")
        
        for eq in equilibria:
            x_eq, y_eq = eq['point']
            eq_type = eq['type']
            stability = eq['stability']
            eigenvalues = eq['eigenvalues']
            
            log(f"  ({x_eq:.3f}, {y_eq:.3f}): {eq_type} - {stability}")
            
            # Color según estabilidad
            if 'Estable' in stability and 'Inestable' not in stability:
                color = 'green'
                marker = 'o'
            elif 'silla' in eq_type.lower():
                color = 'orange'
                marker = 's'
            else:
                color = 'red'
                marker = 'o'
            
            ax.scatter(x_eq, y_eq, c=color, s=150, marker=marker,
                      edgecolors='black', linewidths=2, zorder=10)
            
            # 4. Autovectores
            if show_eigenvectors and not np.iscomplex(eigenvalues[0]):
                classification = system.classify_equilibrium(x_eq, y_eq)
                eigvecs = classification['eigenvectors']
                eigvals = classification['eigenvalues']
                
                for i in range(2):
                    if not np.iscomplex(eigvals[i]):
                        eigval = np.real(eigvals[i])
                        eigvec = np.real(eigvecs[:, i])
                        
                        # Escalar autovector
                        scale = 0.3
                        dx = eigvec[0] * scale
                        dy = eigvec[1] * scale
                        
                        # Color según signo del autovalor
                        arrow_color = 'green' if eigval < 0 else 'red'
                        
                        ax.arrow(x_eq, y_eq, dx, dy,
                                head_width=scale*0.1,
                                head_length=scale*0.15,
                                fc=arrow_color,
                                ec=arrow_color,
                                linewidth=2,
                                alpha=0.7,
                                zorder=9)
    
    # 5. Trayectorias
    colors = plt.cm.tab10.colors
    for idx, traj_config in enumerate(trajectories):
        x0, y0 = traj_config['initial_condition']
        t_forward = traj_config.get('t_forward', 10)
        t_backward = traj_config.get('t_backward', -10)
        
        color = colors[idx % len(colors)]
        
        # Trayectoria hacia adelante
        if t_forward > 0:
            traj = system.simulate_trajectory(x0, y0, (0, t_forward))
            if traj['success']:
                ax.plot(traj['x'], traj['y'], color=color,
                       linewidth=2, alpha=0.8)
                
                # Flecha de dirección en punto medio
                mid_idx = len(traj['x']) // 2
                if mid_idx > 0 and mid_idx < len(traj['x']) - 1:
                    x_mid = traj['x'][mid_idx]
                    y_mid = traj['y'][mid_idx]
                    dx = traj['x'][mid_idx + 1] - traj['x'][mid_idx]
                    dy = traj['y'][mid_idx + 1] - traj['y'][mid_idx]
                    
                    ax.arrow(x_mid, y_mid, dx*10, dy*10,
                            head_width=0.15, head_length=0.2,
                            fc=color, ec=color,
                            linewidth=1.5, alpha=0.8)
        
        # Trayectoria hacia atrás
        if t_backward < 0:
            traj = system.simulate_trajectory(x0, y0, (0, t_backward))
            if traj['success']:
                ax.plot(traj['x'], traj['y'], color=color,
                       linewidth=1.5, alpha=0.5, linestyle='--')
        
        # Punto inicial
        ax.scatter(x0, y0, c=color, s=100, marker='o',
                  edgecolors='black', linewidths=1.5, zorder=5)
    
    # Configurar ejes
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    
    log("✓ Simulación completada exitosamente")
