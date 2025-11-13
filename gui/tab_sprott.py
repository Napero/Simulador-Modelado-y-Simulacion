"""
Pestaña para sistemas de Sprott.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

from gui.widgets import *
from core.systems_3d import SprottSystem


class SprottTab(tk.Frame):
    """Pestaña para sistemas de Sprott."""
    
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
            text="🔮 Sistemas de Sprott\n\n"
                 "Los sistemas caóticos\n"
                 "más simples posibles",
            bg='#e8f5e9',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        type_frame = StyledLabelFrame(left_panel, "🔤 Tipo de Sistema")
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.system_type = tk.StringVar(value='B')
        
        tk.Radiobutton(type_frame, text="Sprott B (yz, x-y, 1-xy)",
                      variable=self.system_type, value='B',
                      bg=COLORS['bg_primary'],
                      command=self.update_equations).pack(anchor=tk.W, padx=5, pady=2)
        
        tk.Radiobutton(type_frame, text="Sprott C (yz, x-y, 1-x²)",
                      variable=self.system_type, value='C',
                      bg=COLORS['bg_primary'],
                      command=self.update_equations).pack(anchor=tk.W, padx=5, pady=2)
        
        tk.Radiobutton(type_frame, text="Sprott D (-y, x+z, xz+3y²)",
                      variable=self.system_type, value='D',
                      bg=COLORS['bg_primary'],
                      command=self.update_equations).pack(anchor=tk.W, padx=5, pady=2)
        
        self.eq_frame = StyledLabelFrame(left_panel, "📝 Ecuaciones")
        self.eq_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.eq_label = tk.Label(
            self.eq_frame,
            text="dx/dt = yz\n"
                 "dy/dt = x - y\n"
                 "dz/dt = 1 - xy\n\n"
                 "Solo 5 términos cuadráticos",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 9),
            justify=tk.LEFT
        )
        self.eq_label.pack(pady=5)
        
        info_frame = tk.Frame(left_panel, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Sprott Systems:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• Los sistemas caóticos más simples",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Solo términos cuadráticos",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• 19 sistemas catalogados (A-S)",
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
        self.t_max = SpinboxDouble(t_frame, from_=10, to=500, value=100, width=10)
        self.t_max.pack(side=tk.LEFT, padx=5)
        
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
        
        self.console.log("🔮 Sistemas de Sprott")
        self.console.log("Caos con ecuaciones minimalistas")
    
    def update_equations(self):
        """Actualiza las ecuaciones mostradas."""
        system_type = self.system_type.get()
        
        if system_type == 'B':
            text = "dx/dt = yz\n" \
                   "dy/dt = x - y\n" \
                   "dz/dt = 1 - xy\n\n" \
                   "Solo 5 términos cuadráticos"
        elif system_type == 'C':
            text = "dx/dt = yz\n" \
                   "dy/dt = x - y\n" \
                   "dz/dt = 1 - x²\n\n" \
                   "Variante con x² en vez de xy"
        elif system_type == 'D':
            text = "dx/dt = -y\n" \
                   "dy/dt = x + z\n" \
                   "dz/dt = xz + 3y²\n\n" \
                   "Versión con término cúbico"
        
        self.eq_label.config(text=text)
        self.console.log(f"✓ Sistema cambiado a Sprott {system_type}")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            system_type = self.system_type.get()
            x0 = self.x0.get()
            y0 = self.y0.get()
            z0 = self.z0.get()
            t_max = self.t_max.get()
            
            self.log(f"=== SISTEMA DE SPROTT {system_type} ===")
            self.log(f"Condición inicial: ({x0:.2f}, {y0:.2f}, {z0:.2f})")
            self.log(f"Tiempo: [0, {t_max}]")
            self.log("-" * 50)
            
            system = SprottSystem(system_type)
            
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
            
            self.log("\n✓ Integrando trayectoria...")
            
            t_span = (0, t_max)
            sol = system.solve((x0, y0, z0), t_span)
            
            if sol.success:
                x, y, z = sol.y
                self.ax.plot(x, y, z, color='purple', alpha=0.8, linewidth=1.2)
                self.ax.scatter([x0], [y0], [z0], color='green', s=100, marker='o',
                              edgecolors='black', linewidths=2, label='Inicio')
            else:
                self.log("✗ Error en la integración")
                return
            
            self.ax.set_xlabel('X', fontsize=11, fontweight='bold')
            self.ax.set_ylabel('Y', fontsize=11, fontweight='bold')
            self.ax.set_zlabel('Z', fontsize=11, fontweight='bold')
            self.ax.set_title(f'Atractor de Sprott {system_type}',
                            fontsize=12, fontweight='bold')
            
            self.log("\n✓ Simulación completada")
            self.log("\nInterpretación:")
            self.log(f"  Sistema Sprott {system_type}: uno de los")
            self.log("  sistemas caóticos más simples conocidos.")
            self.log("  Requiere muy pocos términos para exhibir caos.")
            
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
