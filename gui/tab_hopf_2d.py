"""
Pestaña para análisis de bifurcación de Hopf en sistemas 2D.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.widgets import *
from core.systems_2d import CustomSystem2D, render_phase_plot
from utils.expression_parser import ExpressionParser


class HopfBifurcationTab(tk.Frame):
    """Pestaña para bifurcación de Hopf 2D."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz."""
        # Layout principal
        left_frame_container = tk.Frame(self, bg=COLORS['bg_primary'], width=450)
        left_frame_container.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_frame_container.pack_propagate(False)
        
        # Canvas con scrollbar
        canvas = tk.Canvas(left_frame_container, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame_container, orient="vertical", command=canvas.yview)
        left_panel = tk.Frame(canvas, bg=COLORS['bg_primary'])
        
        left_panel.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=left_panel, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        right_panel = tk.Frame(self, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === PANEL IZQUIERDO ===
        
        desc_label = tk.Label(
            left_panel,
            text="🌪️ Bifurcación de Hopf 2D\n\n"
                 "Analiza bifurcaciones de Hopf\n"
                 "donde nacen ciclos límite",
            bg='#fff3cd',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # Ecuaciones
        eq_frame = StyledLabelFrame(left_panel, "📝 Sistema Paramétrico")
        eq_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(eq_frame, text="dx/dt =", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(anchor=tk.W)
        self.dx_entry = StyledEntry(eq_frame)
        self.dx_entry.insert(0, "mu*x - y - x*(x**2 + y**2)")
        self.dx_entry.config(fg=COLORS['text_primary'])
        self.dx_entry.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(eq_frame, text="dy/dt =", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(anchor=tk.W)
        self.dy_entry = StyledEntry(eq_frame)
        self.dy_entry.insert(0, "x + mu*y - y*(x**2 + y**2)")
        self.dy_entry.config(fg=COLORS['text_primary'])
        self.dy_entry.pack(fill=tk.X, pady=(0, 5))
        
        help_btn = HelpButton(eq_frame, ExpressionParser.get_help_text())
        help_btn.pack(anchor=tk.E, pady=(5, 0))
        
        # Parámetro
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetro de Bifurcación")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(param_frame, text="Nombre del parámetro:",
                bg=COLORS['bg_primary'], font=('Arial', 9)).pack(anchor=tk.W)
        self.param_name = StyledEntry(param_frame)
        self.param_name.insert(0, "mu")
        self.param_name.config(fg=COLORS['text_primary'])
        self.param_name.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(param_frame, text="Valores para diagramas de fase:",
                bg=COLORS['bg_primary'], font=('Arial', 9)).pack(anchor=tk.W)
        self.param_values = StyledEntry(param_frame)
        self.param_values.insert(0, "-0.5, 0, 0.5, 1")
        self.param_values.config(fg=COLORS['text_primary'])
        self.param_values.pack(fill=tk.X)
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos de Visualización")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango X
        x_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        x_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(x_frame, text="x: [", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_min = SpinboxDouble(x_frame, from_=-10, to=10, value=-2)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-10, to=10, value=2)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango Y
        y_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        y_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(y_frame, text="y: [", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_min = SpinboxDouble(y_frame, from_=-10, to=10, value=-2)
        self.y_min.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_max = SpinboxDouble(y_frame, from_=-10, to=10, value=2)
        self.y_max.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Opciones
        opt_frame = StyledLabelFrame(left_panel, "🎨 Opciones de Visualización")
        opt_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Campo vectorial",
                      variable=self.show_field,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        
        self.show_nullclines = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Isoclinas",
                      variable=self.show_nullclines,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        
        self.show_equilibria = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Puntos de equilibrio",
                      variable=self.show_equilibria,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        
        # Info
        info_frame = tk.Frame(left_panel, bg='#d1ecf1', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(info_frame, text="ℹ️ Bifurcación de Hopf:",
                bg='#d1ecf1', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=3)
        tk.Label(info_frame, text="• μ < 0: Foco estable",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• μ = 0: Bifurcación de Hopf",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• μ > 0: Ciclo límite estable",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        StyledButton(btn_frame, "▶ SIMULAR",
                    command=self.run_simulation,
                    style='success').pack(fill=tk.X, pady=(0, 5))
        
        StyledButton(btn_frame, "🗑 LIMPIAR",
                    command=self.clear_plot,
                    style='danger').pack(fill=tk.X)
        
        # === PANEL DERECHO ===
        
        # PanedWindow para hacer el panel redimensionable
        paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL, sashwidth=5, 
                               sashrelief=tk.RAISED, bg=COLORS['bg_secondary'])
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior: Gráfico
        top_panel = tk.Frame(paned, bg=COLORS['bg_white'])
        paned.add(top_panel, minsize=300)
        
        # Área de gráfico
        self.figure = plt.Figure(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, top_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Panel inferior: Consola
        bottom_panel = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(bottom_panel, minsize=200)
        
        console_label = create_label_with_icon(
            bottom_panel, '📋', 'Consola:',
            font=('Arial', 10, 'bold')
        )
        console_label.pack(anchor=tk.W, pady=(5, 5))
        
        self.console = ConsoleText(bottom_panel, height=15)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.console.log("Sistema listo. Configura las ecuaciones y presiona SIMULAR.")
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        try:
            self.console.clear()
            self.console.log("=== BIFURCACIÓN DE HOPF 2D ===\n")
            
            # Obtener ecuaciones
            dx_expr = self.dx_entry.get()
            dy_expr = self.dy_entry.get()
            param_name = self.param_name.get()
            
            if not dx_expr or not dy_expr or not param_name:
                messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")
                return
            
            # Obtener valores del parámetro
            param_str = self.param_values.get()
            if not param_str:
                messagebox.showwarning("Advertencia", "Ingresa al menos un valor del parámetro.")
                return
            
            param_vals = [float(x.strip()) for x in param_str.split(',')]
            
            self.console.log(f"Ecuaciones:")
            self.console.log(f"  dx/dt = {dx_expr}")
            self.console.log(f"  dy/dt = {dy_expr}")
            self.console.log(f"\nParámetro: {param_name}")
            self.console.log(f"Valores: {param_vals}\n")
            
            # Rangos
            x_range = (self.x_min.get(), self.x_max.get())
            y_range = (self.y_min.get(), self.y_max.get())
            
            # Limpiar figura
            self.figure.clear()
            
            # Crear subplots en grilla
            n_vals = len(param_vals)
            n_cols = min(2, n_vals)
            n_rows = (n_vals + n_cols - 1) // n_cols
            
            # Crear cada subplot
            for idx, param_val in enumerate(param_vals):
                self.console.log(f"--- {param_name} = {param_val} ---")
                
                # Sustituir parámetro en las ecuaciones
                dx_with_param = dx_expr.replace(param_name, str(param_val))
                dy_with_param = dy_expr.replace(param_name, str(param_val))
                
                # Crear sistema
                system = CustomSystem2D(dx_with_param, dy_with_param)
                
                # Detectar equilibrios
                equilibria = system.find_equilibria(x_range, y_range)
                
                if equilibria:
                    self.console.log(f"Equilibrios encontrados: {len(equilibria)}")
                    for eq_info in equilibria:
                        try:
                            x_eq, y_eq = eq_info['point']
                            eq_type = eq_info['type']
                            stability = eq_info['stability']
                            self.console.log(f"  ({x_eq:.3f}, {y_eq:.3f}): {eq_type} - {stability}")
                        except Exception as e:
                            self.console.log(f"  Error al procesar equilibrio: {e}")
                else:
                    self.console.log("No se encontraron equilibrios")
                
                # Crear subplot
                ax = self.figure.add_subplot(n_rows, n_cols, idx + 1)
                
                # Generar trayectorias
                trajectories = []
                n_traj = 6
                theta = np.linspace(0, 2*np.pi, n_traj, endpoint=False)
                radius = 1.5
                
                for t in theta:
                    x0 = radius * np.cos(t)
                    y0 = radius * np.sin(t)
                    trajectories.append({
                        'initial_condition': (x0, y0),
                        't_forward': 10,
                        't_backward': 0
                    })
                
                # Configuración para render
                config = {
                    'x_range': x_range,
                    'y_range': y_range,
                    'trajectories': trajectories,
                    'show_field': self.show_field.get(),
                    'show_nullclines': self.show_nullclines.get(),
                    'show_equilibria': self.show_equilibria.get(),
                    'show_eigenvectors': False
                }
                
                # Renderizar
                render_phase_plot(system, config, ax, log_callback=self.console.log)
                
                ax.set_title(f'{param_name} = {param_val}', fontsize=10, fontweight='bold')
                ax.grid(True, alpha=0.3)
                
                self.console.log("")
            
            self.figure.tight_layout()
            self.canvas.draw()
            
            self.console.log("✓ Simulación completada exitosamente")
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            messagebox.showerror("Error", f"Error en la simulación:\n{str(e)}\n\nTipo: {type(e).__name__}")
            self.console.log(f"\n❌ ERROR: {str(e)}")
            self.console.log(f"Tipo de error: {type(e).__name__}")
            self.console.log(f"Detalle:\n{error_detail}")
    
    def clear_plot(self):
        """Limpia el gráfico."""
        self.figure.clear()
        self.canvas.draw()
        self.console.clear()
        self.console.log("Gráfico limpiado. Listo para nueva simulación.")
