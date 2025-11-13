"""
Pestaña de análisis de sistemas autónomos 2D.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.systems_2d import CustomSystem2D, render_phase_plot
from utils.expression_parser import ExpressionParser


class AutonomousTab2D(tk.Frame):
    """Pestaña para análisis de sistemas autónomos 2D."""
    
    def __init__(self, parent, default_dx="x*(2-x-y)", default_dy="y*(1-x-0.5*y)", title="Sistemas Autónomos 2D"):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.default_dx = default_dx
        self.default_dy = default_dy
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz."""
        # Layout principal: panel izquierdo y derecho
        left_panel = tk.Frame(self, bg=COLORS['bg_primary'], width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(self, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === PANEL IZQUIERDO ===
        
        # Descripción
        desc_label = tk.Label(
            left_panel,
            text=f"🌀 Análisis de {self.title}\n\n"
                 "Analiza sistemas de la forma:\n"
                 "  dx/dt = f(x, y)\n"
                 "  dy/dt = g(x, y)",
            bg='#cfe2ff',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15,
            relief=tk.FLAT
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # GroupBox: Ecuaciones
        eq_frame = StyledLabelFrame(left_panel, "📝 Ecuaciones Diferenciales")
        eq_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(eq_frame, text="dx/dt =", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(anchor=tk.W)
        self.dx_entry = StyledEntry(eq_frame)
        self.dx_entry.insert(0, self.default_dx)
        self.dx_entry.config(fg=COLORS['text_primary'])
        self.dx_entry.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(eq_frame, text="dy/dt =", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(anchor=tk.W)
        self.dy_entry = StyledEntry(eq_frame)
        self.dy_entry.insert(0, self.default_dy)
        self.dy_entry.config(fg=COLORS['text_primary'])
        self.dy_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Botón de ayuda
        help_btn = HelpButton(eq_frame, ExpressionParser.get_help_text())
        help_btn.pack(anchor=tk.E, pady=(5, 0))
        
        # GroupBox: Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos de Visualización")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango X
        x_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        x_frame.pack(fill=tk.X, pady=5)
        tk.Label(x_frame, text="x:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(x_frame, text="[", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        self.x_min = SpinboxDouble(x_frame, from_=-100, to=100, value=-5, width=8)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-100, to=100, value=5, width=8)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # Rango Y
        y_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        y_frame.pack(fill=tk.X, pady=5)
        tk.Label(y_frame, text="y:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(y_frame, text="[", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        self.y_min = SpinboxDouble(y_frame, from_=-100, to=100, value=-5, width=8)
        self.y_min.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text=",", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        self.y_max = SpinboxDouble(y_frame, from_=-100, to=100, value=5, width=8)
        self.y_max.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text="]", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # GroupBox: Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field_var = tk.BooleanVar(value=True)
        self.show_nullclines_var = tk.BooleanVar(value=True)
        self.show_equilibria_var = tk.BooleanVar(value=True)
        self.show_eigenvectors_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(vis_frame, text="Campo vectorial",
                      variable=self.show_field_var,
                      bg=COLORS['bg_primary'],
                      font=('Arial', 10)).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Nullclines (isoclinas)",
                      variable=self.show_nullclines_var,
                      bg=COLORS['bg_primary'],
                      font=('Arial', 10)).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Puntos de equilibrio",
                      variable=self.show_equilibria_var,
                      bg=COLORS['bg_primary'],
                      font=('Arial', 10)).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Autovectores",
                      variable=self.show_eigenvectors_var,
                      bg=COLORS['bg_primary'],
                      font=('Arial', 10)).pack(anchor=tk.W)
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.simulate_btn = StyledButton(
            btn_frame,
            "▶ SIMULAR",
            command=self.run_simulation,
            style='success'
        )
        self.simulate_btn.pack(fill=tk.X, pady=(0, 5))
        
        clear_btn = StyledButton(
            btn_frame,
            "🗑 LIMPIAR",
            command=self.clear_all,
            style='danger'
        )
        clear_btn.pack(fill=tk.X)
        
        # === PANEL DERECHO ===
        
        # PanedWindow para paneles redimensionables
        paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL, sashwidth=5, 
                              sashrelief=tk.RAISED, bg=COLORS['bg_secondary'])
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior: gráfico
        top_panel = tk.Frame(paned, bg=COLORS['bg_white'])
        
        self.fig = Figure(figsize=(10, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=top_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, top_panel)
        toolbar.update()
        
        paned.add(top_panel, minsize=300)
        
        # Panel inferior: consola
        bottom_panel = tk.Frame(paned, bg=COLORS['bg_primary'])
        
        info_label = create_label_with_icon(
            bottom_panel, '📊', 'Resultados:',
            font=('Arial', 10, 'bold')
        )
        info_label.pack(anchor=tk.W, padx=10, pady=(5, 5))
        
        self.console = ConsoleText(bottom_panel, height=15)
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        paned.add(bottom_panel, minsize=200)
        
        # Mensaje inicial
        self.console.log("Bienvenido al simulador de sistemas dinámicos 2D")
        self.console.log("Ingresa las ecuaciones y presiona SIMULAR")
        self.console.log("-" * 50)
    
    def log(self, message):
        """Registra mensaje en consola."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            # Obtener ecuaciones
            dx_expr = self.dx_entry.get_value()
            dy_expr = self.dy_entry.get_value()
            
            if not dx_expr or not dy_expr:
                messagebox.showwarning("Advertencia",
                                      "Por favor, ingresa ambas ecuaciones")
                return
            
            self.log("Iniciando simulación...")
            self.log(f"dx/dt = {dx_expr}")
            self.log(f"dy/dt = {dy_expr}")
            
            # Validar expresiones
            valid_dx, error_dx = ExpressionParser.validate_expression(dx_expr, ['x', 'y'])
            valid_dy, error_dy = ExpressionParser.validate_expression(dy_expr, ['x', 'y'])
            
            if not valid_dx:
                messagebox.showerror("Error", f"Error en dx/dt: {error_dx}")
                return
            
            if not valid_dy:
                messagebox.showerror("Error", f"Error en dy/dt: {error_dy}")
                return
            
            # Obtener rangos
            x_range = (self.x_min.get(), self.x_max.get())
            y_range = (self.y_min.get(), self.y_max.get())
            
            self.log(f"Rango X: [{x_range[0]}, {x_range[1]}]")
            self.log(f"Rango Y: [{y_range[0]}, {y_range[1]}]")
            self.log("-" * 50)
            
            # Crear sistema
            system = CustomSystem2D(dx_expr, dy_expr)
            
            # Buscar equilibrios
            self.log("\n🔍 Buscando puntos de equilibrio...")
            equilibria = system.find_equilibria(x_range, y_range)
            
            if equilibria:
                self.log(f"✓ Se encontraron {len(equilibria)} punto(s) de equilibrio:\n")
                for i, eq_info in enumerate(equilibria, 1):
                    x_eq, y_eq = eq_info['point']
                    eq_type = eq_info['type']
                    stability = eq_info['stability']
                    eigenvalues = eq_info['eigenvalues']
                    
                    self.log(f"  Equilibrio {i}: ({x_eq:.4f}, {y_eq:.4f})")
                    self.log(f"    Tipo: {eq_type}")
                    self.log(f"    Estabilidad: {stability}")
                    
                    if np.iscomplex(eigenvalues[0]):
                        self.log(f"    Autovalores: {eigenvalues[0]:.4f}, {eigenvalues[1]:.4f}")
                    else:
                        self.log(f"    Autovalores: λ₁={np.real(eigenvalues[0]):.4f}, λ₂={np.real(eigenvalues[1]):.4f}")
                    self.log("")
            else:
                self.log("⚠ No se encontraron puntos de equilibrio en el rango especificado\n")
            
            self.log("-" * 50)
            self.log("Generando gráfico...\n")
            
            # Configuración de renderizado
            config = {
                'x_range': x_range,
                'y_range': y_range,
                'show_field': self.show_field_var.get(),
                'show_nullclines': self.show_nullclines_var.get(),
                'show_equilibria': self.show_equilibria_var.get(),
                'show_eigenvectors': self.show_eigenvectors_var.get(),
                'trajectories': self._generate_trajectories(x_range, y_range)
            }
            
            # Renderizar
            render_phase_plot(system, config, self.ax, self.log)
            
            self.ax.set_title('Plano de Fase', fontsize=14, fontweight='bold')
            self.canvas.draw()
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error en la simulación:\n{str(e)}")
    
    def _generate_trajectories(self, x_range, y_range):
        """Genera condiciones iniciales automáticas en las esquinas."""
        trajectories = []
        
        # 4 esquinas
        corners = [
            (x_range[0] * 0.7, y_range[0] * 0.7),  # Inferior izquierda
            (x_range[1] * 0.7, y_range[0] * 0.7),  # Inferior derecha
            (x_range[0] * 0.7, y_range[1] * 0.7),  # Superior izquierda
            (x_range[1] * 0.7, y_range[1] * 0.7),  # Superior derecha
        ]
        
        for x0, y0 in corners:
            trajectories.append({
                'initial_condition': (x0, y0),
                't_forward': 10,
                't_backward': -10
            })
        
        return trajectories
    
    def clear_all(self):
        """Limpia todo."""
        self.dx_entry.delete(0, tk.END)
        self.dy_entry.delete(0, tk.END)
        self.ax.clear()
        self.canvas.draw()
        self.console.clear()
        self.log("Interfaz limpiada")
