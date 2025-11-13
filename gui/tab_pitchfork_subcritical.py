"""
Pestaña para la Bifurcación Pitchfork Subcrítica.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *


class PitchforkSubcriticalTab(tk.Frame):
    """Pestaña para bifurcación Pitchfork Subcrítica."""
    
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
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        right_panel = tk.Frame(self, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === PANEL IZQUIERDO ===
        
        desc_label = tk.Label(
            left_panel,
            text="⚡ Bifurcación Pitchfork Subcrítica\n\n"
                 "dx/dt = rx + αx³ - x⁵\n"
                 "(α < 0 para subcrítica)",
            bg='#d1ecf1',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # Parámetros
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetros")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Alpha
        alpha_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        alpha_frame.pack(fill=tk.X, pady=5)
        tk.Label(alpha_frame, text="α (coef. cúbico):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.alpha = SpinboxDouble(alpha_frame, from_=-5, to=5, value=-1, width=10)
        self.alpha.pack(side=tk.LEFT, padx=5)
        
        # Rango de r
        r_range_frame = StyledLabelFrame(left_panel, "📊 Rango del Parámetro r")
        r_range_frame.pack(fill=tk.X, pady=(0, 10))
        
        r_min_frame = tk.Frame(r_range_frame, bg=COLORS['bg_primary'])
        r_min_frame.pack(fill=tk.X, pady=5)
        tk.Label(r_min_frame, text="r mínimo:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.r_min = SpinboxDouble(r_min_frame, from_=-5, to=5, value=-1, width=10)
        self.r_min.pack(side=tk.LEFT, padx=5)
        
        r_max_frame = tk.Frame(r_range_frame, bg=COLORS['bg_primary'])
        r_max_frame.pack(fill=tk.X, pady=5)
        tk.Label(r_max_frame, text="r máximo:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.r_max = SpinboxDouble(r_max_frame, from_=-5, to=5, value=1, width=10)
        self.r_max.pack(side=tk.LEFT, padx=5)
        
        # Número de valores
        n_frame = tk.Frame(r_range_frame, bg=COLORS['bg_primary'])
        n_frame.pack(fill=tk.X, pady=5)
        tk.Label(n_frame, text="Num. puntos:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.n_points = SpinboxDouble(n_frame, from_=10, to=500, value=100, width=10)
        self.n_points.pack(side=tk.LEFT, padx=5)
        
        # Info sobre la bifurcación
        info_frame = tk.Frame(left_panel, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Pitchfork Subcrítica:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• r < 0: Solo x*=0 estable",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• r = 0: Bifurcación pitchfork subcrítica",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• r > 0: x*=0 inestable con ciclo límite",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Aparece histéresis (saltos bruscos)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Presets
        preset_frame = StyledLabelFrame(left_panel, "⚡ Presets")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(preset_frame, "Subcrítica Clásica (α=-1)",
                    command=lambda: self.load_preset(-1),
                    style='info').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Histéresis Fuerte (α=-2)",
                    command=lambda: self.load_preset(-2),
                    style='warning').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Supercrítica (α=1)",
                    command=lambda: self.load_preset(1),
                    style='success').pack(fill=tk.X, pady=2)
        
        # Opciones
        opt_frame = StyledLabelFrame(left_panel, "👁️ Opciones")
        opt_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_unstable_var = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Mostrar ramas inestables",
                      variable=self.show_unstable_var,
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
        
        paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL, sashwidth=5,
                               sashrelief=tk.RAISED, bg=COLORS['bg_secondary'])
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior: Gráfico
        top_panel = tk.Frame(paned, bg=COLORS['bg_white'])
        paned.add(top_panel, minsize=300)
        
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
        
        self.console.log("⚡ Bifurcación Pitchfork Subcrítica")
        self.console.log("Ajusta α < 0 para ver histéresis")
    
    def load_preset(self, alpha):
        """Carga preset."""
        self.alpha.set(alpha)
        self.console.log(f"✓ Preset cargado: α={alpha}")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def find_equilibria(self, r, alpha):
        """
        Encuentra equilibrios de: dx/dt = rx + αx³ - x⁵
        Equilibrios: x(r + αx² - x⁴) = 0
        """
        equilibria = [0]  # x=0 siempre es equilibrio
        
        # Resolver: r + αx² - x⁴ = 0 => x⁴ - αx² - r = 0
        # Sustitución: u = x² => u² - αu - r = 0
        discriminant = alpha**2 + 4*r
        
        if discriminant >= 0:
            u1 = (alpha + np.sqrt(discriminant)) / 2
            u2 = (alpha - np.sqrt(discriminant)) / 2
            
            if u1 > 0:
                equilibria.extend([np.sqrt(u1), -np.sqrt(u1)])
            if u2 > 0:
                equilibria.extend([np.sqrt(u2), -np.sqrt(u2)])
        
        return sorted(equilibria)
    
    def stability(self, x, r, alpha):
        """
        Calcula estabilidad: df/dx = r + 3αx² - 5x⁴
        Estable si df/dx < 0
        """
        dfdx = r + 3*alpha*x**2 - 5*x**4
        return dfdx < 0
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            alpha = self.alpha.get()
            r_min = self.r_min.get()
            r_max = self.r_max.get()
            n_points = int(self.n_points.get())
            
            self.log("=== BIFURCACIÓN PITCHFORK SUBCRÍTICA ===")
            self.log(f"Ecuación: dx/dt = rx + {alpha}x³ - x⁵")
            self.log(f"Rango de r: [{r_min}, {r_max}]")
            self.log(f"Puntos: {n_points}")
            self.log("-" * 50)
            
            if alpha >= 0:
                self.log("\n⚠️ ADVERTENCIA: α ≥ 0 produce pitchfork SUPERCRÍTICA")
                self.log("   Para subcrítica, usa α < 0")
            
            # Generar valores de r
            r_values = np.linspace(r_min, r_max, n_points)
            
            # Almacenar equilibrios
            stable_branches = {0: [], 1: [], 2: []}
            unstable_branches = {0: [], 1: [], 2: []}
            
            for r in r_values:
                equilibria = self.find_equilibria(r, alpha)
                
                for i, x_eq in enumerate(equilibria):
                    if i >= 3:
                        break
                    
                    is_stable = self.stability(x_eq, r, alpha)
                    
                    if is_stable:
                        stable_branches[i].append((r, x_eq))
                    else:
                        unstable_branches[i].append((r, x_eq))
            
            # Graficar ramas estables
            colors = ['blue', 'green', 'red']
            for i, branch in stable_branches.items():
                if branch:
                    r_vals, x_vals = zip(*branch)
                    self.ax.plot(r_vals, x_vals, color=colors[i], linewidth=2, 
                               label=f'Estable {i}' if i == 0 else None)
            
            # Graficar ramas inestables
            if self.show_unstable_var.get():
                for i, branch in unstable_branches.items():
                    if branch:
                        r_vals, x_vals = zip(*branch)
                        self.ax.plot(r_vals, x_vals, color=colors[i], linewidth=2,
                                   linestyle='--', label=f'Inestable {i}' if i == 0 else None)
            
            # Marcar bifurcación en r=0
            self.ax.axvline(x=0, color='gray', linestyle=':', alpha=0.5, label='r=0 (bifurcación)')
            self.ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
            
            self.ax.set_xlabel('r (parámetro)', fontsize=11, fontweight='bold')
            self.ax.set_ylabel('x* (equilibrios)', fontsize=11, fontweight='bold')
            self.ax.set_title(f'Pitchfork Subcrítica (α={alpha})', 
                            fontsize=12, fontweight='bold')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            
            # Análisis
            self.log("\n✓ Diagrama de bifurcación generado")
            
            # Puntos críticos
            if alpha < 0:
                r_saddle_node = -alpha**2 / 4
                x_saddle_node = np.sqrt(-alpha / 2) if alpha < 0 else 0
                
                self.log(f"\nPuntos Críticos:")
                self.log(f"  Bifurcación Pitchfork: r = 0")
                self.log(f"  Bifurcaciones Saddle-Node: r ≈ {r_saddle_node:.4f}")
                self.log(f"    en x* ≈ ±{x_saddle_node:.4f}")
                
                self.log(f"\nRegiones de Comportamiento:")
                self.log(f"  r < {r_saddle_node:.3f}: Solo x*=0 estable")
                self.log(f"  {r_saddle_node:.3f} < r < 0: 5 equilibrios")
                self.log(f"  r > 0: 3 equilibrios (histéresis)")
            
            self.log("\n✓ Análisis completado")
            self.canvas.draw()
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error:\n{str(e)}")
    
    def clear_all(self):
        """Limpia todo."""
        self.ax.clear()
        self.canvas.draw()
        self.console.clear()
        self.log("Interfaz limpiada")
