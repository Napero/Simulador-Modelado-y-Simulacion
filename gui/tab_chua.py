"""
Pestaña para el circuito de Chua.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from gui.widgets import *
from core.systems_3d import ChuaSystem


class ChuaTab(tk.Frame):
    """Pestaña para el circuito de Chua."""
    
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
            text="⚡ Circuito de Chua\n\n"
                 "Caos en circuito electrónico\n"
                 "Atractor de doble scroll",
            bg='#ffe5cc',
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
            text="dx/dt = α(y - x - h(x))\n"
                 "dy/dt = x - y + z\n"
                 "dz/dt = -βy\n\n"
                 "h(x): función no lineal",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 9),
            justify=tk.LEFT
        )
        eq_info.pack(pady=5)
        
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetros")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        alpha_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        alpha_frame.pack(fill=tk.X, pady=5)
        tk.Label(alpha_frame, text="α:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.alpha = SpinboxDouble(alpha_frame, from_=5, to=25, value=15.6, width=10)
        self.alpha.pack(side=tk.LEFT, padx=5)
        
        beta_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        beta_frame.pack(fill=tk.X, pady=5)
        tk.Label(beta_frame, text="β:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.beta = SpinboxDouble(beta_frame, from_=10, to=40, value=28, width=10)
        self.beta.pack(side=tk.LEFT, padx=5)
        
        m0_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        m0_frame.pack(fill=tk.X, pady=5)
        tk.Label(m0_frame, text="m₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.m0 = SpinboxDouble(m0_frame, from_=-2, to=0, value=-1.143, width=10)
        self.m0.pack(side=tk.LEFT, padx=5)
        
        m1_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        m1_frame.pack(fill=tk.X, pady=5)
        tk.Label(m1_frame, text="m₁:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.m1 = SpinboxDouble(m1_frame, from_=-2, to=0, value=-0.714, width=10)
        self.m1.pack(side=tk.LEFT, padx=5)
        
        info_frame = tk.Frame(left_panel, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Circuito de Chua:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• Primer circuito caótico físico",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Atractor de doble scroll",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• h(x): resistor no lineal",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        ic_frame = StyledLabelFrame(left_panel, "🎯 Condición Inicial")
        ic_frame.pack(fill=tk.X, pady=(0, 10))
        
        x0_frame = tk.Frame(ic_frame, bg=COLORS['bg_primary'])
        x0_frame.pack(fill=tk.X, pady=5)
        tk.Label(x0_frame, text="x₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.x0 = SpinboxDouble(x0_frame, from_=-5, to=5, value=0.1, width=10)
        self.x0.pack(side=tk.LEFT, padx=5)
        
        y0_frame = tk.Frame(ic_frame, bg=COLORS['bg_primary'])
        y0_frame.pack(fill=tk.X, pady=5)
        tk.Label(y0_frame, text="y₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.y0 = SpinboxDouble(y0_frame, from_=-5, to=5, value=0, width=10)
        self.y0.pack(side=tk.LEFT, padx=5)
        
        z0_frame = tk.Frame(ic_frame, bg=COLORS['bg_primary'])
        z0_frame.pack(fill=tk.X, pady=5)
        tk.Label(z0_frame, text="z₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.z0 = SpinboxDouble(z0_frame, from_=-5, to=5, value=0, width=10)
        self.z0.pack(side=tk.LEFT, padx=5)
        
        time_frame = StyledLabelFrame(left_panel, "⏱️ Tiempo de Simulación")
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        t_frame = tk.Frame(time_frame, bg=COLORS['bg_primary'])
        t_frame.pack(fill=tk.X, pady=5)
        tk.Label(t_frame, text="Tiempo final:", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.t_max = SpinboxDouble(t_frame, from_=10, to=500, value=150, width=10)
        self.t_max.pack(side=tk.LEFT, padx=5)
        
        preset_frame = StyledLabelFrame(left_panel, "⚡ Presets")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(preset_frame, "Doble Scroll Clásico",
                    command=lambda: self.load_preset(15.6, 28, -1.143, -0.714),
                    style='info').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Caos Suave",
                    command=lambda: self.load_preset(10, 20, -1.2, -0.7),
                    style='success').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Caos Intenso",
                    command=lambda: self.load_preset(20, 35, -1, -0.6),
                    style='warning').pack(fill=tk.X, pady=2)
        
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
        
        self.console.log("⚡ Circuito de Chua")
        self.console.log("Sistema electrónico caótico real")
    
    def load_preset(self, alpha, beta, m0, m1):
        """Carga preset."""
        self.alpha.set(alpha)
        self.beta.set(beta)
        self.m0.set(m0)
        self.m1.set(m1)
        self.console.log(f"✓ Preset cargado")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            alpha = self.alpha.get()
            beta = self.beta.get()
            m0 = self.m0.get()
            m1 = self.m1.get()
            x0 = self.x0.get()
            y0 = self.y0.get()
            z0 = self.z0.get()
            t_max = self.t_max.get()
            
            self.log("=== CIRCUITO DE CHUA ===")
            self.log(f"Parámetros:")
            self.log(f"  α={alpha:.3f}, β={beta:.3f}")
            self.log(f"  m₀={m0:.3f}, m₁={m1:.3f}")
            self.log(f"Condición inicial: ({x0:.2f}, {y0:.2f}, {z0:.2f})")
            self.log(f"Tiempo: [0, {t_max}]")
            self.log("-" * 50)
            
            system = ChuaSystem(alpha, beta, m0, m1)
            
            self.log("\nEquilibrio:")
            self.log("  Origen (0, 0, 0) - típicamente inestable")
            
            self.log("\n✓ Integrando trayectoria...")
            self.log("  Buscando atractor de doble scroll...")
            
            t_span = (0, t_max)
            sol = system.solve((x0, y0, z0), t_span)
            
            if sol.success:
                x, y, z = sol.y
                self.ax.plot(x, y, z, color='orange', alpha=0.8, linewidth=1.2)
                self.ax.scatter([x0], [y0], [z0], color='green', s=100, marker='o',
                              edgecolors='black', linewidths=2, label='Inicio')
            else:
                self.log("✗ Error en la integración")
                return
            
            self.ax.set_xlabel('X (Voltaje C1)', fontsize=11, fontweight='bold')
            self.ax.set_ylabel('Y (Voltaje C2)', fontsize=11, fontweight='bold')
            self.ax.set_zlabel('Z (Corriente L)', fontsize=11, fontweight='bold')
            self.ax.set_title(f'Atractor de Chua (α={alpha}, β={beta})',
                            fontsize=12, fontweight='bold')
            
            self.log("\n✓ Simulación completada")
            self.log("\nInterpretación:")
            self.log("  El circuito de Chua exhibe un atractor")
            self.log("  de 'doble scroll' - dos lóbulos que")
            self.log("  se entrelazan caóticamente.")
            self.log("  Primer circuito caótico construido físicamente.")
            
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
