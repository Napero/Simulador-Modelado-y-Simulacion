"""
Pestaña para Sistema Conservativo (Doble Pozo).
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.systems_2d import CustomSystem2D, render_phase_plot


class ConservativeTab(tk.Frame):
    """Pestaña para Sistema Conservativo (Doble Pozo)."""
    
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
            text="⚡ Sistema Conservativo\n(Doble Pozo)\n\n"
                 "Sistema Hamiltoniano con\n"
                 "energía constante",
            bg='#e2e3e5',
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
                 "dy/dt = x - x³\n\n"
                 "Hamiltoniano:\n"
                 "H = ½y² - ½x² + ¼x⁴",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 9),
            justify=tk.LEFT
        )
        eq_info.pack(pady=5)
        
        # Potencial
        pot_frame = StyledLabelFrame(left_panel, "📈 Potencial")
        pot_frame.pack(fill=tk.X, pady=(0, 10))
        
        pot_info = tk.Label(
            pot_frame,
            text="V(x) = -½x² + ¼x⁴\n\n"
                 "Dos pozos de potencial en:\n"
                 "  x = ±1 (mínimos)\n"
                 "Barrera en:\n"
                 "  x = 0 (máximo local)",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Arial', 9),
            justify=tk.LEFT
        )
        pot_info.pack(pady=5)
        
        # Info sobre conservación
        info_frame = tk.Frame(left_panel, bg='#d1ecf1', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Propiedades:",
                bg='#d1ecf1', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• Energía constante (dH/dt = 0)",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Órbitas = curvas de nivel H = c",
                bg='#d1ecf1', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Separatriz conecta las sillas",
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
        self.x_min = SpinboxDouble(x_frame, from_=-5, to=5, value=-2, width=8)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-5, to=5, value=2, width=8)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango Y
        y_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        y_frame.pack(fill=tk.X, pady=5)
        tk.Label(y_frame, text="y:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(y_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_min = SpinboxDouble(y_frame, from_=-5, to=5, value=-2, width=8)
        self.y_min.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.y_max = SpinboxDouble(y_frame, from_=-5, to=5, value=2, width=8)
        self.y_max.pack(side=tk.LEFT, padx=5)
        tk.Label(y_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field_var = tk.BooleanVar(value=True)
        self.show_equilibria_var = tk.BooleanVar(value=True)
        self.show_energy_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(vis_frame, text="Campo vectorial",
                      variable=self.show_field_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Puntos de equilibrio",
                      variable=self.show_equilibria_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Curvas de energía (H = c)",
                      variable=self.show_energy_var,
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
        
        self.console.log("⚡ Sistema Conservativo (Doble Pozo)")
        self.console.log("Sistema Hamiltoniano con energía constante")
        self.console.log("Presiona SIMULAR para ver el retrato de fase")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def hamiltonian(self, x, y):
        """Calcula el Hamiltoniano H = ½y² - ½x² + ¼x⁴"""
        return 0.5 * y**2 - 0.5 * x**2 + 0.25 * x**4
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            self.log("=== SISTEMA CONSERVATIVO (DOBLE POZO) ===")
            self.log("Ecuaciones:")
            self.log("  dx/dt = y")
            self.log("  dy/dt = x - x³")
            self.log("\nHamiltoniano:")
            self.log("  H(x,y) = ½y² - ½x² + ¼x⁴")
            self.log("  dH/dt = 0 (energía conservada)")
            self.log("-" * 50)
            
            # Crear sistema
            dx_expr = "y"
            dy_expr = "x - x**3"
            
            system = CustomSystem2D(dx_expr, dy_expr)
            
            # Encontrar equilibrios
            x_range = (self.x_min.get(), self.x_max.get())
            y_range = (self.y_min.get(), self.y_max.get())
            
            self.log(f"\nBuscando equilibrios...")
            equilibria = system.find_equilibria(x_range, y_range)
            
            if equilibria:
                self.log(f"✓ Equilibrios encontrados: {len(equilibria)}")
                for eq_info in equilibria:
                    x_eq, y_eq = eq_info['point']
                    eq_type = eq_info['type']
                    stability = eq_info['stability']
                    eigenvalues = eq_info['eigenvalues']
                    
                    # Calcular energía en el equilibrio
                    H_eq = self.hamiltonian(x_eq, y_eq)
                    
                    self.log(f"\n  Punto: ({x_eq:.4f}, {y_eq:.4f})")
                    self.log(f"  Tipo: {eq_type}")
                    self.log(f"  Estabilidad: {stability}")
                    self.log(f"  Energía: H = {H_eq:.4f}")
                    self.log(f"  Autovalores:")
                    for eigval in eigenvalues:
                        if np.iscomplex(eigval):
                            self.log(f"    λ = {eigval.real:.4f} + {eigval.imag:.4f}i")
                        else:
                            self.log(f"    λ = {np.real(eigval):.4f}")
            
            # Generar trayectorias con diferentes energías
            trajectories = []
            
            # Órbitas alrededor de pozos izquierdo y derecho
            for center_x in [-1, 1]:
                for radius in [0.1, 0.3, 0.5]:
                    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
                    for angle in angles:
                        x0 = center_x + radius * np.cos(angle)
                        y0 = radius * np.sin(angle)
                        trajectories.append({
                            'initial_condition': (x0, y0),
                            't_forward': 20,
                            't_backward': 20
                        })
            
            # Trayectoria cerca de la separatriz
            for y0 in [-0.5, -0.3, 0.3, 0.5]:
                trajectories.append({
                    'initial_condition': (0.0, y0),
                    't_forward': 20,
                    't_backward': 20
                })
            
            # Configuración de renderizado
            config = {
                'x_range': x_range,
                'y_range': y_range,
                'show_field': self.show_field_var.get(),
                'show_nullclines': False,
                'show_equilibria': self.show_equilibria_var.get(),
                'show_eigenvectors': False,
                'trajectories': trajectories
            }
            
            # Renderizar
            self.log("\n✓ Generando retrato de fase...")
            render_phase_plot(system, config, self.ax, self.log)
            
            # Agregar curvas de nivel de energía
            if self.show_energy_var.get():
                x_grid = np.linspace(x_range[0], x_range[1], 300)
                y_grid = np.linspace(y_range[0], y_range[1], 300)
                X, Y = np.meshgrid(x_grid, y_grid)
                H = self.hamiltonian(X, Y)
                
                # Niveles de energía importantes
                energy_levels = [-0.25, -0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.2, 0.4, 0.6]
                
                contours = self.ax.contour(X, Y, H, levels=energy_levels, 
                                          colors='purple', alpha=0.4, linewidths=1.5)
                self.ax.clabel(contours, inline=True, fontsize=8, fmt='H=%.2f')
                
                self.log("\n✓ Curvas de energía H = c agregadas")
            
            self.ax.set_title('Sistema Conservativo (Doble Pozo)',
                            fontsize=14, fontweight='bold')
            
            # Interpretación
            self.log(f"\nInterpretación:")
            self.log("  • Dos pozos de potencial en x = ±1")
            self.log("  • Barrera en x = 0 (silla)")
            self.log("  • Las órbitas son curvas de nivel H = constante")
            self.log("  • La separatriz conecta el punto de silla consigo mismo")
            self.log("  • Dentro de cada pozo: órbitas cerradas (oscilaciones)")
            self.log("  • Energía alta: órbitas que cruzan ambos pozos")
            
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
