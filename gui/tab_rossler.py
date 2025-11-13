"""
Pestaña para el sistema de Rössler.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from gui.widgets import *
from core.systems_3d import RosslerSystem


class RosslerTab(tk.Frame):
    """Pestaña para el sistema de Rössler."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz."""
        left_frame_container = tk.Frame(self, bg=COLORS['bg_primary'], width=450)
        left_frame_container.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_frame_container.pack_propagate(False)
        
        canvas = tk.Canvas(left_frame_container, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(left_frame_container, orient="vertical", command=canvas.yview)
        left_panel = tk.Frame(canvas, bg=COLORS['bg_primary'])
        
        left_panel.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
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
            text="🌀 Sistema de Rössler\n\n"
                 "Atractor caótico con estructura\n"
                 "de banda plegada",
            bg='#e7f3ff',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        eq_frame = StyledLabelFrame(left_panel, "📝 Sistema")
        eq_frame.pack(fill=tk.X, pady=(0, 10))
        
        eq_info = tk.Label(
            eq_frame,
            text="dx/dt = -y - z\n"
                 "dy/dt = x + ay\n"
                 "dz/dt = b + z(x - c)\n\n"
                 "Más simple que Lorenz",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 9),
            justify=tk.LEFT
        )
        eq_info.pack(pady=5)
        
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetros")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        a_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        a_frame.pack(fill=tk.X, pady=5)
        tk.Label(a_frame, text="a:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.a = SpinboxDouble(a_frame, from_=0, to=1, value=0.2, width=10)
        self.a.pack(side=tk.LEFT, padx=5)
        
        b_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        b_frame.pack(fill=tk.X, pady=5)
        tk.Label(b_frame, text="b:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.b = SpinboxDouble(b_frame, from_=0, to=1, value=0.2, width=10)
        self.b.pack(side=tk.LEFT, padx=5)
        
        c_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        c_frame.pack(fill=tk.X, pady=5)
        tk.Label(c_frame, text="c:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.c = SpinboxDouble(c_frame, from_=1, to=10, value=5.7, width=10)
        self.c.pack(side=tk.LEFT, padx=5)
        
        info_frame = tk.Frame(left_panel, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Valores típicos:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• a=0.2, b=0.2, c=5.7: Caos clásico",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Más simple que Lorenz",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Banda plegada visible",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        ic_frame = StyledLabelFrame(left_panel, "🎯 Condición Inicial")
        ic_frame.pack(fill=tk.X, pady=(0, 10))
        
        x0_frame = tk.Frame(ic_frame, bg=COLORS['bg_primary'])
        x0_frame.pack(fill=tk.X, pady=5)
        tk.Label(x0_frame, text="x₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.x0 = SpinboxDouble(x0_frame, from_=-20, to=20, value=0.1, width=10)
        self.x0.pack(side=tk.LEFT, padx=5)
        
        y0_frame = tk.Frame(ic_frame, bg=COLORS['bg_primary'])
        y0_frame.pack(fill=tk.X, pady=5)
        tk.Label(y0_frame, text="y₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.y0 = SpinboxDouble(y0_frame, from_=-20, to=20, value=0, width=10)
        self.y0.pack(side=tk.LEFT, padx=5)
        
        z0_frame = tk.Frame(ic_frame, bg=COLORS['bg_primary'])
        z0_frame.pack(fill=tk.X, pady=5)
        tk.Label(z0_frame, text="z₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.z0 = SpinboxDouble(z0_frame, from_=-20, to=20, value=0, width=10)
        self.z0.pack(side=tk.LEFT, padx=5)
        
        time_frame = StyledLabelFrame(left_panel, "⏱️ Tiempo de Simulación")
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        t_frame = tk.Frame(time_frame, bg=COLORS['bg_primary'])
        t_frame.pack(fill=tk.X, pady=5)
        tk.Label(t_frame, text="Tiempo final:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.t_max = SpinboxDouble(t_frame, from_=10, to=500, value=100, width=10)
        self.t_max.pack(side=tk.LEFT, padx=5)
        
        preset_frame = StyledLabelFrame(left_panel, "⚡ Presets")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(preset_frame, "Caos Clásico (a=0.2, b=0.2, c=5.7)",
                    command=lambda: self.load_preset(0.2, 0.2, 5.7),
                    style='info').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Caos Suave (a=0.1, b=0.1, c=4)",
                    command=lambda: self.load_preset(0.1, 0.1, 4),
                    style='success').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Caos Intenso (a=0.3, b=0.3, c=6)",
                    command=lambda: self.load_preset(0.3, 0.3, 6),
                    style='warning').pack(fill=tk.X, pady=2)
        
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_equilibria_var = tk.BooleanVar(value=True)
        tk.Checkbutton(vis_frame, text="Puntos de equilibrio",
                      variable=self.show_equilibria_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        
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
        
        top_panel = tk.Frame(paned, bg=COLORS['bg_white'])
        paned.add(top_panel, minsize=300)
        
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=top_panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        toolbar = NavigationToolbar2Tk(self.canvas, top_panel)
        toolbar.update()
        
        bottom_panel = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(bottom_panel, minsize=200)
        
        info_label = create_label_with_icon(bottom_panel, '📊', 'Resultados:')
        info_label.pack(anchor=tk.W, pady=(5, 5))
        
        self.console = ConsoleText(bottom_panel, height=15)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        self.console.log("🌀 Sistema de Rössler")
        self.console.log("Ajusta los parámetros y presiona SIMULAR")
    
    def load_preset(self, a, b, c):
        """Carga preset."""
        self.a.set(a)
        self.b.set(b)
        self.c.set(c)
        self.console.log(f"✓ Preset cargado: a={a}, b={b}, c={c}")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            a = self.a.get()
            b = self.b.get()
            c = self.c.get()
            x0 = self.x0.get()
            y0 = self.y0.get()
            z0 = self.z0.get()
            t_max = self.t_max.get()
            
            self.log("=== SISTEMA DE RÖSSLER ===")
            self.log(f"Parámetros: a={a:.3f}, b={b:.3f}, c={c:.3f}")
            self.log(f"Condición inicial: ({x0:.2f}, {y0:.2f}, {z0:.2f})")
            self.log(f"Tiempo: [0, {t_max}]")
            self.log("-" * 50)
            
            system = RosslerSystem(a, b, c)
            
            self.log("\nBuscando equilibrios...")
            equilibria = system.find_equilibria()
            
            if equilibria:
                self.log(f"✓ Equilibrios encontrados: {len(equilibria)}")
                for i, (x_eq, y_eq, z_eq) in enumerate(equilibria):
                    self.log(f"  E{i+1}: ({x_eq:.4f}, {y_eq:.4f}, {z_eq:.4f})")
                    
                    if self.show_equilibria_var.get():
                        self.ax.scatter([x_eq], [y_eq], [z_eq], 
                                      color='red', s=100, marker='o',
                                      edgecolors='black', linewidths=2,
                                      label=f'Equilibrio {i+1}' if i == 0 else '')
            else:
                self.log("✗ No se encontraron equilibrios")
            
            self.log("\n✓ Integrando trayectoria...")
            
            t_span = (0, t_max)
            sol = system.solve((x0, y0, z0), t_span)
            
            if sol.success:
                x, y, z = sol.y
                self.ax.plot(x, y, z, color='blue', alpha=0.8, linewidth=1.2)
                self.ax.scatter([x0], [y0], [z0], color='green', s=100, marker='o',
                              edgecolors='black', linewidths=2, label='Inicio')
            else:
                self.log("✗ Error en la integración")
                return
            
            self.ax.set_xlabel('X', fontsize=11, fontweight='bold')
            self.ax.set_ylabel('Y', fontsize=11, fontweight='bold')
            self.ax.set_zlabel('Z', fontsize=11, fontweight='bold')
            self.ax.set_title(f'Atractor de Rössler (a={a}, b={b}, c={c})',
                            fontsize=12, fontweight='bold')
            
            self.log("\n✓ Simulación completada")
            self.log("\nInterpretación:")
            self.log("  El sistema de Rössler exhibe caos determinista")
            self.log("  con una estructura de 'banda plegada' característica.")
            self.log("  Es más simple que Lorenz pero igualmente caótico.")
            
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
