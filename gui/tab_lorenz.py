"""
Pestaña para el Sistema de Lorenz (3D).
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D

from gui.widgets import *
from core.systems_3d import LorenzSystem, render_3d_trajectory


class LorenzTab(tk.Frame):
    """Pestaña para el Sistema de Lorenz."""
    
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
            text="🦋 Sistema de Lorenz (Caos)\n\n"
                 "Sistema tridimensional que exhibe\n"
                 "comportamiento caótico y atractor extraño",
            bg='#f8d7da',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # Parámetros
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetros del Sistema")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sigma
        sigma_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        sigma_frame.pack(fill=tk.X, pady=5)
        tk.Label(sigma_frame, text="σ (sigma):", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=12).pack(side=tk.LEFT)
        self.sigma = SpinboxDouble(sigma_frame, from_=0.1, to=50, value=10, width=10)
        self.sigma.pack(side=tk.LEFT, padx=5)
        
        # Rho
        rho_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        rho_frame.pack(fill=tk.X, pady=5)
        tk.Label(rho_frame, text="ρ (rho):", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=12).pack(side=tk.LEFT)
        self.rho = SpinboxDouble(rho_frame, from_=0.1, to=50, value=28, width=10)
        self.rho.pack(side=tk.LEFT, padx=5)
        
        # Beta
        beta_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        beta_frame.pack(fill=tk.X, pady=5)
        tk.Label(beta_frame, text="β (beta):", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=12).pack(side=tk.LEFT)
        self.beta = SpinboxDouble(beta_frame, from_=0.1, to=10, value=8/3, width=10)
        self.beta.pack(side=tk.LEFT, padx=5)
        
        # Info de regímenes
        info_frame = tk.Frame(param_frame, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(info_frame, text="Regímenes típicos:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• ρ = 10: Estable",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• ρ = 24.74: Hopf",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• ρ = 28: Caótico (clásico)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Tiempo
        time_frame = StyledLabelFrame(left_panel, "⏱️ Parámetros de Simulación")
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        t_frame = tk.Frame(time_frame, bg=COLORS['bg_primary'])
        t_frame.pack(fill=tk.X, pady=5)
        tk.Label(t_frame, text="Tiempo:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=12).pack(side=tk.LEFT)
        tk.Label(t_frame, text="[0,", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.t_max = SpinboxDouble(t_frame, from_=1, to=200, value=50, width=8)
        self.t_max.pack(side=tk.LEFT, padx=5)
        tk.Label(t_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Condición inicial
        ic_frame = StyledLabelFrame(left_panel, "📍 Condición Inicial")
        ic_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(ic_frame, text="x₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9)).pack(anchor=tk.W)
        self.x0 = StyledEntry(ic_frame)
        self.x0.insert(0, "0.1")
        self.x0.config(fg=COLORS['text_primary'])
        self.x0.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(ic_frame, text="y₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9)).pack(anchor=tk.W)
        self.y0 = StyledEntry(ic_frame)
        self.y0.insert(0, "0")
        self.y0.config(fg=COLORS['text_primary'])
        self.y0.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(ic_frame, text="z₀:", bg=COLORS['bg_primary'],
                font=('Arial', 9)).pack(anchor=tk.W)
        self.z0 = StyledEntry(ic_frame)
        self.z0.insert(0, "0")
        self.z0.config(fg=COLORS['text_primary'])
        self.z0.pack(fill=tk.X)
        
        # Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "🎨 Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_equilibria = tk.BooleanVar(value=True)
        tk.Checkbutton(vis_frame, text="Mostrar equilibrios",
                      variable=self.show_equilibria,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        
        # Presets rápidos
        preset_frame = StyledLabelFrame(left_panel, "⚡ Presets Rápidos")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(preset_frame, "Estable (ρ=10)",
                    command=lambda: self.load_preset(10),
                    style='info').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Hopf (ρ=24.74)",
                    command=lambda: self.load_preset(24.74),
                    style='warning').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Caótico (ρ=28)",
                    command=lambda: self.load_preset(28),
                    style='danger').pack(fill=tk.X, pady=2)
        
        # Botones principales
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
        
        # Panel superior: Gráfico 3D
        top_panel = tk.Frame(paned, bg=COLORS['bg_white'])
        paned.add(top_panel, minsize=350)
        
        # Matplotlib figure 3D
        self.fig = plt.Figure(figsize=(10, 8), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
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
        
        self.console.log("🦋 Sistema de Lorenz")
        self.console.log("El sistema de Lorenz exhibe comportamiento caótico")
        self.console.log("Ajusta los parámetros y presiona SIMULAR")
    
    def load_preset(self, rho_value):
        """Carga un preset rápido."""
        # SpinboxDouble no tiene delete, hay que configurar el valor directamente
        self.rho.set(rho_value)
        self.console.log(f"✓ Preset cargado: ρ = {rho_value}")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            # Obtener parámetros
            sigma = self.sigma.get()
            rho = self.rho.get()
            beta = self.beta.get()
            t_max = self.t_max.get()
            
            self.log("=== SISTEMA DE LORENZ ===")
            self.log(f"Parámetros: σ={sigma}, ρ={rho}, β={beta:.3f}")
            self.log(f"Ecuaciones:")
            self.log(f"  dx/dt = σ(y - x)")
            self.log(f"  dy/dt = x(ρ - z) - y")
            self.log(f"  dz/dt = xy - βz")
            self.log("-" * 50)
            
            # Crear sistema
            system = LorenzSystem(sigma=sigma, rho=rho, beta=beta)
            
            # Encontrar equilibrios
            equilibria = system.find_equilibria()
            self.log(f"\nEquilibrios encontrados: {len(equilibria)}")
            for idx, eq in enumerate(equilibria):
                self.log(f"  E{idx+1}: ({eq[0]:.4f}, {eq[1]:.4f}, {eq[2]:.4f})")
            
            # Condición inicial
            try:
                x0 = float(self.x0.get())
                y0 = float(self.y0.get())
                z0 = float(self.z0.get())
                initial_condition = (x0, y0, z0)
            except:
                initial_condition = (0.1, 0, 0)
                self.log("\n⚠ Usando condición inicial por defecto: (0.1, 0, 0)")
            
            self.log(f"\nCondición inicial: ({initial_condition[0]}, {initial_condition[1]}, {initial_condition[2]})")
            self.log(f"Tiempo de simulación: [0, {t_max}]")
            self.log("\nResolviendo sistema...")
            
            # Resolver
            t_span = (0, t_max)
            sol = system.solve(initial_condition, t_span)
            
            if sol.success:
                x, y, z = sol.y
                
                # Graficar trayectoria
                self.ax.plot(x, y, z, 'b-', alpha=0.7, linewidth=0.8)
                self.ax.scatter(*initial_condition, color='green', s=100, 
                              marker='o', label='Inicio', zorder=10)
                self.ax.scatter(x[-1], y[-1], z[-1], color='red', s=100, 
                              marker='s', label='Final', zorder=10)
                
                # Equilibrios
                if self.show_equilibria.get():
                    for eq in equilibria:
                        self.ax.scatter(*eq, color='black', s=80, marker='*', 
                                      edgecolors='yellow', linewidths=2, zorder=15)
                
                self.ax.set_xlabel('X', fontsize=10, fontweight='bold')
                self.ax.set_ylabel('Y', fontsize=10, fontweight='bold')
                self.ax.set_zlabel('Z', fontsize=10, fontweight='bold')
                self.ax.set_title(f'Atractor de Lorenz (σ={sigma}, ρ={rho}, β={beta:.2f})', 
                                fontsize=12, fontweight='bold')
                self.ax.legend(loc='upper right')
                self.ax.grid(True, alpha=0.3)
                
                # Estadísticas
                self.log(f"\n✓ Simulación completada exitosamente")
                self.log(f"Puntos calculados: {len(sol.t)}")
                self.log(f"Rango X: [{x.min():.2f}, {x.max():.2f}]")
                self.log(f"Rango Y: [{y.min():.2f}, {y.max():.2f}]")
                self.log(f"Rango Z: [{z.min():.2f}, {z.max():.2f}]")
                
                # Interpretación
                if rho < 1:
                    self.log("\nInterpretación: ρ < 1 → Origen estable")
                elif 1 <= rho < 24.74:
                    self.log("\nInterpretación: 1 ≤ ρ < 24.74 → Régimen subcrítico")
                elif abs(rho - 24.74) < 0.5:
                    self.log("\nInterpretación: ρ ≈ 24.74 → Bifurcación de Hopf")
                elif 24.74 <= rho < 30:
                    self.log("\nInterpretación: ρ ≈ 28 → Régimen CAÓTICO (atractor extraño)")
                else:
                    self.log(f"\nInterpretación: ρ = {rho} → Régimen complejo")
                
                self.canvas.draw()
            else:
                self.log("✗ Error: La simulación no convergió")
                messagebox.showerror("Error", "La simulación no convergió")
            
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
