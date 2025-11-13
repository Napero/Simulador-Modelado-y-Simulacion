"""
Pestaña para el Oscilador de Van der Pol.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.systems_2d import CustomSystem2D, render_phase_plot


class VanDerPolTab(tk.Frame):
    """Pestaña para el Oscilador de Van der Pol."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz."""
        # Layout principal
        left_frame_container = tk.Frame(self, bg=COLORS['bg_primary'], width=450)
        left_frame_container.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_frame_container.pack_propagate(False)
        
        # Canvas con scrollbar para panel izquierdo
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
            text="🔄 Oscilador de Van der Pol\n\n"
                 "Sistema con ciclo límite estable.\n"
                 "Aplicaciones en circuitos eléctricos\n"
                 "y sistemas biológicos",
            bg='#d4edda',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # Ecuaciones
        eq_frame = StyledLabelFrame(left_panel, "📝 Sistema")
        eq_frame.pack(fill=tk.X, pady=(0, 10))
        
        eq_info = tk.Label(
            eq_frame,
            text="dx/dt = y\n"
                 "dy/dt = μ(1 - x²)y - x",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 10),
            justify=tk.LEFT
        )
        eq_info.pack(pady=5)
        
        # Parámetro μ
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetro")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        mu_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        mu_frame.pack(fill=tk.X, pady=5)
        tk.Label(mu_frame, text="μ (mu):", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=8).pack(side=tk.LEFT)
        self.mu = SpinboxDouble(mu_frame, from_=0, to=10, value=1, width=10)
        self.mu.pack(side=tk.LEFT, padx=5)
        
        # Info
        info_frame = tk.Frame(param_frame, bg='#d1ecf1', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(info_frame, text="ℹ️ Comportamiento:",
                bg='#d1ecf1', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• μ = 0: Oscilador armónico",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• μ > 0: Ciclo límite estable",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• μ grande: Oscilaciones de relajación",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos de Visualización")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango X
        x_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        x_frame.pack(fill=tk.X, pady=5)
        tk.Label(x_frame, text="x:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(x_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_min = SpinboxDouble(x_frame, from_=-10, to=10, value=-3, width=8)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-10, to=10, value=3, width=8)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango Y
        y_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        y_frame.pack(fill=tk.X, pady=5)
        tk.Label(y_frame, text="y:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(y_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_min = SpinboxDouble(y_frame, from_=-10, to=10, value=-3, width=8)
        self.y_min.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_max = SpinboxDouble(y_frame, from_=-10, to=10, value=3, width=8)
        self.y_max.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field_var = tk.BooleanVar(value=True)
        self.show_equilibria_var = tk.BooleanVar(value=True)
        self.show_nullclines_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(vis_frame, text="Campo vectorial",
                      variable=self.show_field_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Puntos de equilibrio",
                      variable=self.show_equilibria_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Isoclinas",
                      variable=self.show_nullclines_var,
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
        
        self.console.log("🔄 Oscilador de Van der Pol")
        self.console.log("Sistema con ciclo límite estable")
        self.console.log("Ajusta μ y presiona SIMULAR")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            # Obtener parámetro
            mu = self.mu.get()
            
            self.log("=== OSCILADOR DE VAN DER POL ===")
            self.log(f"Parámetro: μ = {mu}")
            self.log("Ecuaciones:")
            self.log("  dx/dt = y")
            self.log(f"  dy/dt = {mu}*(1 - x²)*y - x")
            self.log("-" * 50)
            
            # Crear sistema
            dx_expr = "y"
            dy_expr = f"{mu}*(1 - x**2)*y - x"
            
            system = CustomSystem2D(dx_expr, dy_expr)
            
            # Encontrar equilibrios
            x_range = (self.x_min.get(), self.x_max.get())
            y_range = (self.y_min.get(), self.y_max.get())
            
            self.log(f"\nBuscando equilibrios en:")
            self.log(f"  x ∈ [{x_range[0]}, {x_range[1]}]")
            self.log(f"  y ∈ [{y_range[0]}, {y_range[1]}]")
            
            equilibria = system.find_equilibria(x_range, y_range)
            
            if equilibria:
                self.log(f"\n✓ Equilibrios encontrados: {len(equilibria)}")
                for eq_info in equilibria:
                    x_eq, y_eq = eq_info['point']
                    eq_type = eq_info['type']
                    stability = eq_info['stability']
                    eigenvalues = eq_info['eigenvalues']
                    
                    self.log(f"\n  Punto: ({x_eq:.4f}, {y_eq:.4f})")
                    self.log(f"  Tipo: {eq_type}")
                    self.log(f"  Estabilidad: {stability}")
                    self.log(f"  Autovalores:")
                    for eigval in eigenvalues:
                        if np.iscomplex(eigval):
                            self.log(f"    λ = {eigval.real:.4f} + {eigval.imag:.4f}i")
                        else:
                            self.log(f"    λ = {np.real(eigval):.4f}")
            else:
                self.log("\n⚠ No se encontraron equilibrios en el rango especificado")
            
            # Generar trayectorias alrededor del origen
            trajectories = []
            n_traj = 8
            radius_values = [0.5, 1.0, 1.5, 2.0]
            
            for radius in radius_values:
                angles = np.linspace(0, 2*np.pi, n_traj, endpoint=False)
                for angle in angles:
                    x0 = radius * np.cos(angle)
                    y0 = radius * np.sin(angle)
                    trajectories.append({
                        'initial_condition': (x0, y0),
                        't_forward': 30,
                        't_backward': 0
                    })
            
            # Configuración de renderizado
            config = {
                'x_range': x_range,
                'y_range': y_range,
                'show_field': self.show_field_var.get(),
                'show_nullclines': self.show_nullclines_var.get(),
                'show_equilibria': self.show_equilibria_var.get(),
                'show_eigenvectors': False,
                'trajectories': trajectories
            }
            
            # Renderizar
            self.log("\n✓ Generando diagrama de fase...")
            render_phase_plot(system, config, self.ax, self.log)
            
            self.ax.set_title(f'Oscilador de Van der Pol (μ = {mu})',
                            fontsize=14, fontweight='bold')
            
            # Interpretación
            self.log(f"\nInterpretación:")
            if abs(mu) < 0.01:
                self.log("  μ ≈ 0 → Comportamiento de oscilador armónico")
            elif mu > 0 and mu < 2:
                self.log("  μ pequeño → Ciclo límite casi circular")
            elif mu >= 2:
                self.log("  μ grande → Oscilaciones de relajación (ciclo límite no circular)")
            
            self.log("\n✓ Simulación completada exitosamente")
            self.canvas.draw()
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error en la simulación:\n{str(e)}")
    
    def clear_all(self):
        """Limpia todo."""
        self.ax.clear()
        self.canvas.draw()
        self.console.clear()
        self.log("Interfaz limpiada")
