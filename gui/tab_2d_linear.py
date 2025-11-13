"""
Pestaña de análisis de sistemas lineales no homogéneos 2D.
Sistema: X' = AX + b
"""

import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np

from gui.widgets import *
from core.systems_2d import LinearSystem2D, render_phase_plot


class LinearNonHomogeneousTab(tk.Frame):
    """Pestaña para sistemas lineales no homogéneos 2D."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz."""
        # Layout principal
        left_panel = tk.Frame(self, bg=COLORS['bg_primary'], width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(self, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === PANEL IZQUIERDO ===
        
        desc_label = tk.Label(
            left_panel,
            text="📐 Sistema Lineal No-Homogéneo\n\n"
                 "Analiza sistemas de la forma:\n"
                 "  X' = AX + b\n"
                 "donde A es matriz 2x2 y b es vector",
            bg='#fff3cd',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # Matriz A
        matrix_frame = StyledLabelFrame(left_panel, "📝 Matriz A (2×2)")
        matrix_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para matriz
        grid_frame = tk.Frame(matrix_frame, bg=COLORS['bg_primary'])
        grid_frame.pack(pady=5)
        
        tk.Label(grid_frame, text="A =", bg=COLORS['bg_primary'],
                font=('Arial', 11)).grid(row=0, column=0, rowspan=2, padx=5)
        
        tk.Label(grid_frame, text="[", bg=COLORS['bg_primary'],
                font=('Arial', 14)).grid(row=0, column=1, rowspan=2)
        
        # Entradas de matriz con valores por defecto
        self.a11 = StyledEntry(grid_frame, width=8)
        self.a11.insert(0, "0")  # Valor por defecto
        self.a11.grid(row=0, column=2, padx=3, pady=2)
        
        self.a12 = StyledEntry(grid_frame, width=8)
        self.a12.insert(0, "1")  # Valor por defecto
        self.a12.grid(row=0, column=3, padx=3, pady=2)
        
        self.a21 = StyledEntry(grid_frame, width=8)
        self.a21.insert(0, "-2")  # Valor por defecto
        self.a21.grid(row=1, column=2, padx=3, pady=2)
        
        self.a22 = StyledEntry(grid_frame, width=8)
        self.a22.insert(0, "-1")  # Valor por defecto
        self.a22.grid(row=1, column=3, padx=3, pady=2)
        
        tk.Label(grid_frame, text="]", bg=COLORS['bg_primary'],
                font=('Arial', 14)).grid(row=0, column=4, rowspan=2)
        
        # Vector b
        vector_frame = StyledLabelFrame(left_panel, "📊 Vector b (término constante)")
        vector_frame.pack(fill=tk.X, pady=(0, 10))
        
        b_grid = tk.Frame(vector_frame, bg=COLORS['bg_primary'])
        b_grid.pack(pady=5)
        
        tk.Label(b_grid, text="b =", bg=COLORS['bg_primary'],
                font=('Arial', 11)).grid(row=0, column=0, rowspan=2, padx=5)
        
        tk.Label(b_grid, text="[", bg=COLORS['bg_primary'],
                font=('Arial', 14)).grid(row=0, column=1, rowspan=2)
        
        self.b1 = StyledEntry(b_grid, width=10)
        self.b1.insert(0, "1")  # Valor por defecto
        self.b1.grid(row=0, column=2, padx=3, pady=2)
        
        self.b2 = StyledEntry(b_grid, width=10)
        self.b2.insert(0, "0")  # Valor por defecto
        self.b2.grid(row=1, column=2, padx=3, pady=2)
        
        tk.Label(b_grid, text="]", bg=COLORS['bg_primary'],
                font=('Arial', 14)).grid(row=0, column=3, rowspan=2)
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos de Visualización")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango X
        x_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        x_frame.pack(fill=tk.X, pady=5)
        tk.Label(x_frame, text="x:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(x_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_min = SpinboxDouble(x_frame, from_=-100, to=100, value=-3, width=8)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-100, to=100, value=3, width=8)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango Y
        y_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        y_frame.pack(fill=tk.X, pady=5)
        tk.Label(y_frame, text="y:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(y_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_min = SpinboxDouble(y_frame, from_=-100, to=100, value=-3, width=8)
        self.y_min.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_max = SpinboxDouble(y_frame, from_=-100, to=100, value=3, width=8)
        self.y_max.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field_var = tk.BooleanVar(value=True)
        self.show_equilibria_var = tk.BooleanVar(value=True)
        self.show_eigenvectors_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(vis_frame, text="Campo vectorial",
                      variable=self.show_field_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Punto de equilibrio",
                      variable=self.show_equilibria_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Autovectores",
                      variable=self.show_eigenvectors_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        StyledButton(btn_frame, "▶ SIMULAR",
                    command=self.run_simulation,
                    style='success').pack(fill=tk.X, pady=(0, 5))
        
        StyledButton(btn_frame, "🗑 LIMPIAR",
                    command=self.clear_all,
                    style='danger').pack(fill=tk.X)
        
        # === PANEL DERECHO ===
        
        # PanedWindow para hacer el panel redimensionable
        paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL, sashwidth=5, 
                               sashrelief=tk.RAISED, bg=COLORS['bg_secondary'])
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior: Gráfico
        top_panel = tk.Frame(paned, bg=COLORS['bg_white'])
        paned.add(top_panel, minsize=300)
        
        # Matplotlib figure
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=top_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.canvas, top_panel)
        toolbar.update()
        
        # Panel inferior: Consola
        bottom_panel = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(bottom_panel, minsize=200)
        
        info_label = create_label_with_icon(bottom_panel, '📊', 'Resultados:')
        info_label.pack(anchor=tk.W, pady=(5, 5))
        
        self.console = ConsoleText(bottom_panel, height=15)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.console.log("Sistema Lineal No-Homogéneo: X' = AX + b")
        self.console.log("Ingresa matriz A y vector b, luego presiona SIMULAR")
    
    def log(self, message):
        """Registra mensaje en consola."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            # Obtener valores de matriz A
            A = np.array([
                [float(self.a11.get_value() or "0"), float(self.a12.get_value() or "0")],
                [float(self.a21.get_value() or "0"), float(self.a22.get_value() or "0")]
            ])
            
            # Obtener vector b
            b = np.array([
                float(self.b1.get_value() or "0"),
                float(self.b2.get_value() or "0")
            ])
            
            self.log("Iniciando simulación de sistema lineal no-homogéneo...")
            self.log(f"Matriz A:")
            self.log(f"  [{A[0,0]:.3f}  {A[0,1]:.3f}]")
            self.log(f"  [{A[1,0]:.3f}  {A[1,1]:.3f}]")
            self.log(f"Vector b: [{b[0]:.3f}, {b[1]:.3f}]")
            self.log("-" * 50)
            
            # Crear sistema
            system = LinearSystem2D(A, b)
            
            # Calcular y mostrar información
            eigenvalues = system.eigenvalues
            self.log(f"\nAutovalores de A:")
            for i, eigval in enumerate(eigenvalues):
                if np.iscomplex(eigval):
                    self.log(f"  λ{i+1} = {eigval.real:.4f} + {eigval.imag:.4f}i")
                else:
                    self.log(f"  λ{i+1} = {np.real(eigval):.4f}")
            
            # Punto de equilibrio
            if system.equilibrium_point is not None:
                eq_point = system.equilibrium_point
                self.log(f"\nPunto de equilibrio: ({eq_point[0]:.4f}, {eq_point[1]:.4f})")
            else:
                self.log("\n⚠ No existe punto de equilibrio único (det(A) = 0)")
            
            # Rangos
            x_range = (self.x_min.get(), self.x_max.get())
            y_range = (self.y_min.get(), self.y_max.get())
            
            self.log(f"Rango X: [{x_range[0]}, {x_range[1]}]")
            self.log(f"Rango Y: [{y_range[0]}, {y_range[1]}]")
            self.log("-" * 50)
            
            # Generar trayectorias alrededor del equilibrio
            trajectories = []
            if system.equilibrium_point is not None:
                eq_x, eq_y = system.equilibrium_point
                
                # 8 puntos alrededor del equilibrio
                radius = min(abs(x_range[1] - x_range[0]), abs(y_range[1] - y_range[0])) * 0.3
                angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
                
                for angle in angles:
                    x0 = eq_x + radius * np.cos(angle)
                    y0 = eq_y + radius * np.sin(angle)
                    trajectories.append({
                        'initial_condition': (x0, y0),
                        't_forward': 5,
                        't_backward': -5
                    })
            else:
                # Sin equilibrio, usar corners
                corners = [
                    (x_range[0] * 0.7, y_range[0] * 0.7),
                    (x_range[1] * 0.7, y_range[0] * 0.7),
                    (x_range[0] * 0.7, y_range[1] * 0.7),
                    (x_range[1] * 0.7, y_range[1] * 0.7),
                ]
                
                for x0, y0 in corners:
                    trajectories.append({
                        'initial_condition': (x0, y0),
                        't_forward': 5,
                        't_backward': -5
                    })
            
            # Configuración de renderizado
            config = {
                'x_range': x_range,
                'y_range': y_range,
                'show_field': self.show_field_var.get(),
                'show_nullclines': False,  # No aplica para sistemas lineales
                'show_equilibria': self.show_equilibria_var.get(),
                'show_eigenvectors': self.show_eigenvectors_var.get(),
                'trajectories': trajectories
            }
            
            # Renderizar
            render_phase_plot(system, config, self.ax, self.log)
            
            self.ax.set_title('Sistema Lineal No-Homogéneo: X\' = AX + b',
                            fontsize=14, fontweight='bold')
            self.canvas.draw()
            
        except ValueError as e:
            self.log(f"✗ Error en valores numéricos: {str(e)}")
            messagebox.showerror("Error", f"Error en valores:\n{str(e)}")
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error en la simulación:\n{str(e)}")
    
    def clear_all(self):
        """Limpia todo."""
        self.ax.clear()
        self.canvas.draw()
        self.console.clear()
        self.log("Interfaz limpiada")
