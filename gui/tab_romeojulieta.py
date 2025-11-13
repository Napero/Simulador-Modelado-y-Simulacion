"""
Pestaña para el modelo de Romeo y Julieta (Strogatz).
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.systems_2d import CustomSystem2D, render_phase_plot


class RomeoJulietaTab(tk.Frame):
    """Pestaña para el modelo de Romeo y Julieta."""
    
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
            text="💕 Romeo y Julieta (Strogatz)\n\n"
                 "Modelo de dinámica romántica\n"
                 "basado en personalidades",
            bg='#f8d7da',
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
            text="dR/dt = aR + bJ\n"
                 "dJ/dt = cR + dJ\n\n"
                 "R: sentimiento de Romeo\n"
                 "J: sentimiento de Julieta",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 9),
            justify=tk.LEFT
        )
        eq_info.pack(pady=5)
        
        # Parámetros de Romeo
        romeo_frame = StyledLabelFrame(left_panel, "🎭 Parámetros de Romeo")
        romeo_frame.pack(fill=tk.X, pady=(0, 10))
        
        a_frame = tk.Frame(romeo_frame, bg=COLORS['bg_primary'])
        a_frame.pack(fill=tk.X, pady=5)
        tk.Label(a_frame, text="a (autoexcitación):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.a = SpinboxDouble(a_frame, from_=-5, to=5, value=0, width=10)
        self.a.pack(side=tk.LEFT, padx=5)
        
        b_frame = tk.Frame(romeo_frame, bg=COLORS['bg_primary'])
        b_frame.pack(fill=tk.X, pady=5)
        tk.Label(b_frame, text="b (respuesta a J):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.b = SpinboxDouble(b_frame, from_=-5, to=5, value=1, width=10)
        self.b.pack(side=tk.LEFT, padx=5)
        
        # Parámetros de Julieta
        julieta_frame = StyledLabelFrame(left_panel, "💃 Parámetros de Julieta")
        julieta_frame.pack(fill=tk.X, pady=(0, 10))
        
        c_frame = tk.Frame(julieta_frame, bg=COLORS['bg_primary'])
        c_frame.pack(fill=tk.X, pady=5)
        tk.Label(c_frame, text="c (respuesta a R):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.c = SpinboxDouble(c_frame, from_=-5, to=5, value=-1, width=10)
        self.c.pack(side=tk.LEFT, padx=5)
        
        d_frame = tk.Frame(julieta_frame, bg=COLORS['bg_primary'])
        d_frame.pack(fill=tk.X, pady=5)
        tk.Label(d_frame, text="d (autoexcitación):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.d = SpinboxDouble(d_frame, from_=-5, to=5, value=0, width=10)
        self.d.pack(side=tk.LEFT, padx=5)
        
        # Info sobre personalidades
        info_frame = tk.Frame(left_panel, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Tipos de Personalidad:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• a,d > 0: Apasionado (se autoexcita)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• a,d < 0: Evasivo (se enfría solo)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• b,c > 0: Dependiente (le gusta ser amado)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• b,c < 0: Contradictorio (huye del amor)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos de Visualización")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango R
        r_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        r_frame.pack(fill=tk.X, pady=5)
        tk.Label(r_frame, text="R:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(r_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.r_min = SpinboxDouble(r_frame, from_=-10, to=10, value=-3, width=8)
        self.r_min.pack(side=tk.LEFT, padx=5)
        tk.Label(r_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.r_max = SpinboxDouble(r_frame, from_=-10, to=10, value=3, width=8)
        self.r_max.pack(side=tk.LEFT, padx=5)
        tk.Label(r_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango J
        j_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        j_frame.pack(fill=tk.X, pady=5)
        tk.Label(j_frame, text="J:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(j_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.j_min = SpinboxDouble(j_frame, from_=-10, to=10, value=-3, width=8)
        self.j_min.pack(side=tk.LEFT, padx=5)
        tk.Label(j_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.j_max = SpinboxDouble(j_frame, from_=-10, to=10, value=3, width=8)
        self.j_max.pack(side=tk.LEFT, padx=5)
        tk.Label(j_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Presets
        preset_frame = StyledLabelFrame(left_panel, "⚡ Presets Rápidos")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(preset_frame, "Centro (a=0, b=1, c=-1, d=0)",
                    command=lambda: self.load_preset(0, 1, -1, 0),
                    style='info').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Espiral (a=-0.2, b=1, c=-1, d=-0.2)",
                    command=lambda: self.load_preset(-0.2, 1, -1, -0.2),
                    style='warning').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Ciclo Límite (a=0.1, b=-1, c=1, d=0.1)",
                    command=lambda: self.load_preset(0.1, -1, 1, 0.1),
                    style='success').pack(fill=tk.X, pady=2)
        
        # Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field_var = tk.BooleanVar(value=True)
        self.show_equilibria_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(vis_frame, text="Campo vectorial",
                      variable=self.show_field_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Puntos de equilibrio",
                      variable=self.show_equilibria_var,
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
        
        self.console.log("💕 Modelo de Romeo y Julieta")
        self.console.log("Ajusta los parámetros de personalidad y presiona SIMULAR")
    
    def load_preset(self, a, b, c, d):
        """Carga un preset de parámetros."""
        self.a.set(a)
        self.b.set(b)
        self.c.set(c)
        self.d.set(d)
        self.console.log(f"✓ Preset cargado: a={a}, b={b}, c={c}, d={d}")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def classify_personality(self, param, name):
        """Clasifica el tipo de personalidad."""
        if param > 0.01:
            return f"{name} > 0: Apasionado/Dependiente"
        elif param < -0.01:
            return f"{name} < 0: Evasivo/Contradictorio"
        else:
            return f"{name} ≈ 0: Neutral"
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            # Obtener parámetros
            a = self.a.get()
            b = self.b.get()
            c = self.c.get()
            d = self.d.get()
            
            self.log("=== ROMEO Y JULIETA (STROGATZ) ===")
            self.log(f"Parámetros:")
            self.log(f"  Romeo: a={a:.2f}, b={b:.2f}")
            self.log(f"  Julieta: c={c:.2f}, d={d:.2f}")
            self.log("\nEcuaciones:")
            self.log(f"  dR/dt = {a}R + {b}J")
            self.log(f"  dJ/dt = {c}R + {d}J")
            self.log("-" * 50)
            
            # Análisis de personalidades
            self.log("\nAnálisis de Personalidades:")
            self.log(f"  Romeo (a={a:.2f}): {self.classify_personality(a, 'a')}")
            self.log(f"  Romeo hacia J (b={b:.2f}): {self.classify_personality(b, 'b')}")
            self.log(f"  Julieta hacia R (c={c:.2f}): {self.classify_personality(c, 'c')}")
            self.log(f"  Julieta (d={d:.2f}): {self.classify_personality(d, 'd')}")
            
            # Crear sistema
            dx_expr = f"{a}*x + {b}*y"
            dy_expr = f"{c}*x + {d}*y"
            
            # Renombrar x,y a R,J para claridad
            system = CustomSystem2D(dx_expr, dy_expr)
            
            # Encontrar equilibrios
            r_range = (self.r_min.get(), self.r_max.get())
            j_range = (self.j_min.get(), self.j_max.get())
            
            self.log(f"\nBuscando equilibrios...")
            equilibria = system.find_equilibria(r_range, j_range)
            
            if equilibria:
                self.log(f"✓ Equilibrios encontrados: {len(equilibria)}")
                for eq_info in equilibria:
                    r_eq, j_eq = eq_info['point']
                    eq_type = eq_info['type']
                    stability = eq_info['stability']
                    eigenvalues = eq_info['eigenvalues']
                    
                    self.log(f"\n  Punto: (R={r_eq:.4f}, J={j_eq:.4f})")
                    self.log(f"  Tipo: {eq_type}")
                    self.log(f"  Estabilidad: {stability}")
                    self.log(f"  Autovalores:")
                    for eigval in eigenvalues:
                        if np.iscomplex(eigval):
                            self.log(f"    λ = {eigval.real:.4f} + {eigval.imag:.4f}i")
                        else:
                            self.log(f"    λ = {np.real(eigval):.4f}")
            
            # Generar trayectorias
            trajectories = []
            n_traj = 8
            radius_values = [0.5, 1.0, 1.5, 2.0]
            
            for radius in radius_values:
                angles = np.linspace(0, 2*np.pi, n_traj, endpoint=False)
                for angle in angles:
                    r0 = radius * np.cos(angle)
                    j0 = radius * np.sin(angle)
                    trajectories.append({
                        'initial_condition': (r0, j0),
                        't_forward': 20,
                        't_backward': 20
                    })
            
            # Configuración de renderizado
            config = {
                'x_range': r_range,
                'y_range': j_range,
                'show_field': self.show_field_var.get(),
                'show_nullclines': False,
                'show_equilibria': self.show_equilibria_var.get(),
                'show_eigenvectors': False,
                'trajectories': trajectories
            }
            
            # Renderizar
            self.log("\n✓ Generando diagrama de fase...")
            render_phase_plot(system, config, self.ax, self.log)
            
            # Personalizar etiquetas
            self.ax.set_xlabel('R (Romeo)', fontsize=11, fontweight='bold')
            self.ax.set_ylabel('J (Julieta)', fontsize=11, fontweight='bold')
            self.ax.set_title(f'Romeo y Julieta (a={a}, b={b}, c={c}, d={d})',
                            fontsize=12, fontweight='bold')
            
            # Interpretación
            trace = a + d
            det = a*d - b*c
            
            self.log(f"\nAnálisis de Estabilidad:")
            self.log(f"  Traza (a+d) = {trace:.4f}")
            self.log(f"  Determinante (ad-bc) = {det:.4f}")
            
            if abs(trace) < 0.01 and det > 0:
                self.log("\n  → Centro: Amor eterno (órbitas cerradas)")
            elif trace < 0 and det > 0:
                self.log("\n  → Espiral estable: Se estabilizan juntos")
            elif trace > 0 and det > 0:
                self.log("\n  → Espiral inestable: Pasión descontrolada")
            elif det < 0:
                self.log("\n  → Silla: Relación inestable (uno huye, otro persigue)")
            
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
