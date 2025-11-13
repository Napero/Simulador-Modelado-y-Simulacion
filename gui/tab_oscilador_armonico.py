"""
Pestaña para el Oscilador Armónico.
"""

import tkinter as tk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.systems_2d import CustomSystem2D, render_phase_plot


class OsciladorArmonicoTab(tk.Frame):
    """Pestaña para el Oscilador Armónico."""
    
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
            text="🌊 Oscilador Armónico\n\n"
                 "Sistema fundamental de física\n"
                 "con amortiguamiento",
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
            text="dx/dt = v\n"
                 "dv/dt = -ω²x - γv\n\n"
                 "x: posición\n"
                 "v: velocidad\n"
                 "ω: frecuencia natural\n"
                 "γ: coef. amortiguamiento",
            bg=COLORS['bg_primary'],
            fg=COLORS['text_primary'],
            font=('Courier New', 9),
            justify=tk.LEFT
        )
        eq_info.pack(pady=5)
        
        # Parámetros
        param_frame = StyledLabelFrame(left_panel, "⚙️ Parámetros")
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Omega
        omega_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        omega_frame.pack(fill=tk.X, pady=5)
        tk.Label(omega_frame, text="ω (freq. natural):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.omega = SpinboxDouble(omega_frame, from_=0.1, to=10, value=1, width=10)
        self.omega.pack(side=tk.LEFT, padx=5)
        
        # Gamma
        gamma_frame = tk.Frame(param_frame, bg=COLORS['bg_primary'])
        gamma_frame.pack(fill=tk.X, pady=5)
        tk.Label(gamma_frame, text="γ (amortiguamiento):", bg=COLORS['bg_primary'],
                font=('Arial', 9), width=18).pack(side=tk.LEFT)
        self.gamma = SpinboxDouble(gamma_frame, from_=0, to=5, value=0, width=10)
        self.gamma.pack(side=tk.LEFT, padx=5)
        
        # Info sobre tipos de amortiguamiento
        info_frame = tk.Frame(left_panel, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="ℹ️ Tipos de Amortiguamiento:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(3, 0))
        tk.Label(info_frame, text="• γ = 0: Sin amortiguamiento (órbitas cerradas)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• γ < 2ω: Subamortiguado (espirales)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• γ = 2ω: Críticamente amortiguado",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• γ > 2ω: Sobreamortiguado (nodo estable)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos de Visualización")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango x
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
        
        # Rango v
        v_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        v_frame.pack(fill=tk.X, pady=5)
        tk.Label(v_frame, text="v:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(v_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.v_min = SpinboxDouble(v_frame, from_=-10, to=10, value=-3, width=8)
        self.v_min.pack(side=tk.LEFT, padx=5)
        tk.Label(v_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.v_max = SpinboxDouble(v_frame, from_=-10, to=10, value=3, width=8)
        self.v_max.pack(side=tk.LEFT, padx=5)
        tk.Label(v_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Presets
        preset_frame = StyledLabelFrame(left_panel, "⚡ Presets Rápidos")
        preset_frame.pack(fill=tk.X, pady=(0, 10))
        
        StyledButton(preset_frame, "Sin Amortiguamiento (γ=0)",
                    command=lambda: self.load_preset(1, 0),
                    style='info').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Subamortiguado (γ=0.5)",
                    command=lambda: self.load_preset(1, 0.5),
                    style='success').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Crítico (γ=2ω)",
                    command=lambda: self.load_critical(),
                    style='warning').pack(fill=tk.X, pady=2)
        StyledButton(preset_frame, "Sobreamortiguado (γ=3)",
                    command=lambda: self.load_preset(1, 3),
                    style='danger').pack(fill=tk.X, pady=2)
        
        # Opciones de visualización
        vis_frame = StyledLabelFrame(left_panel, "👁️ Visualización")
        vis_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.show_field_var = tk.BooleanVar(value=True)
        self.show_equilibria_var = tk.BooleanVar(value=True)
        self.show_energy_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(vis_frame, text="Campo vectorial",
                      variable=self.show_field_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Punto de equilibrio",
                      variable=self.show_equilibria_var,
                      bg=COLORS['bg_primary']).pack(anchor=tk.W)
        tk.Checkbutton(vis_frame, text="Niveles de energía (γ=0)",
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
        
        self.console.log("🌊 Oscilador Armónico")
        self.console.log("Ajusta ω y γ para ver diferentes comportamientos")
    
    def load_preset(self, omega, gamma):
        """Carga preset."""
        self.omega.set(omega)
        self.gamma.set(gamma)
        self.console.log(f"✓ Preset cargado: ω={omega}, γ={gamma}")
    
    def load_critical(self):
        """Carga amortiguamiento crítico."""
        omega = self.omega.get()
        gamma_critical = 2 * omega
        self.gamma.set(gamma_critical)
        self.console.log(f"✓ Amortiguamiento crítico: γ=2ω={gamma_critical:.2f}")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def energy(self, x, v, omega):
        """Calcula energía: E = ½v² + ½ω²x²"""
        return 0.5 * v**2 + 0.5 * omega**2 * x**2
    
    def run_simulation(self):
        """Ejecuta la simulación."""
        self.console.clear()
        self.ax.clear()
        
        try:
            omega = self.omega.get()
            gamma = self.gamma.get()
            
            if omega <= 0:
                raise ValueError("ω debe ser mayor que 0")
            
            self.log("=== OSCILADOR ARMÓNICO ===")
            self.log(f"Parámetros:")
            self.log(f"  ω (frecuencia natural) = {omega:.2f}")
            self.log(f"  γ (amortiguamiento) = {gamma:.2f}")
            self.log("\nEcuaciones:")
            self.log(f"  dx/dt = v")
            self.log(f"  dv/dt = -{omega**2:.2f}x - {gamma:.2f}v")
            self.log("-" * 50)
            
            # Clasificar tipo de amortiguamiento
            gamma_critical = 2 * omega
            self.log(f"\nAnálisis de Amortiguamiento:")
            self.log(f"  γ_crítico = 2ω = {gamma_critical:.2f}")
            
            if abs(gamma) < 1e-6:
                damping_type = "SIN AMORTIGUAMIENTO"
                description = "Oscilaciones perpetuas (órbitas cerradas)"
            elif gamma < gamma_critical - 0.01:
                damping_type = "SUBAMORTIGUADO"
                description = "Oscilaciones con decaimiento exponencial"
            elif abs(gamma - gamma_critical) < 0.01:
                damping_type = "CRÍTICAMENTE AMORTIGUADO"
                description = "Retorno más rápido sin oscilación"
            else:
                damping_type = "SOBREAMORTIGUADO"
                description = "Retorno lento sin oscilación"
            
            self.log(f"  Tipo: {damping_type}")
            self.log(f"  {description}")
            
            # Crear sistema
            dx_expr = "y"
            dv_expr = f"-{omega**2}*x - {gamma}*y"
            
            system = CustomSystem2D(dx_expr, dv_expr)
            
            # Analizar punto de equilibrio
            self.log(f"\nPunto de Equilibrio: (0, 0)")
            
            # Autovalores: λ² + γλ + ω² = 0
            discriminant = gamma**2 - 4*omega**2
            
            if discriminant < 0:
                real_part = -gamma / 2
                imag_part = np.sqrt(-discriminant) / 2
                lambda1 = complex(real_part, imag_part)
                lambda2 = complex(real_part, -imag_part)
                self.log(f"  Autovalores complejos:")
                self.log(f"    λ₁ = {real_part:.4f} + {imag_part:.4f}i")
                self.log(f"    λ₂ = {real_part:.4f} - {imag_part:.4f}i")
                
                if abs(real_part) < 1e-6:
                    self.log(f"  Tipo: CENTRO (sin amortiguamiento)")
                elif real_part < 0:
                    self.log(f"  Tipo: FOCO ESTABLE (subamortiguado)")
                else:
                    self.log(f"  Tipo: FOCO INESTABLE")
            else:
                lambda1 = (-gamma + np.sqrt(discriminant)) / 2
                lambda2 = (-gamma - np.sqrt(discriminant)) / 2
                self.log(f"  Autovalores reales:")
                self.log(f"    λ₁ = {lambda1:.4f}")
                self.log(f"    λ₂ = {lambda2:.4f}")
                
                if lambda1 < 0 and lambda2 < 0:
                    self.log(f"  Tipo: NODO ESTABLE")
                else:
                    self.log(f"  Tipo: NODO INESTABLE")
            
            # Rangos
            x_range = (self.x_min.get(), self.x_max.get())
            v_range = (self.v_min.get(), self.v_max.get())
            
            # Generar trayectorias
            trajectories = []
            n_traj = 8
            radius_values = [0.5, 1.0, 1.5, 2.0]
            
            for radius in radius_values:
                angles = np.linspace(0, 2*np.pi, n_traj, endpoint=False)
                for angle in angles:
                    x0 = radius * np.cos(angle)
                    v0 = radius * np.sin(angle)
                    trajectories.append({
                        'initial_condition': (x0, v0),
                        't_forward': 30,
                        't_backward': 0
                    })
            
            # Configuración
            config = {
                'x_range': x_range,
                'y_range': v_range,
                'show_field': self.show_field_var.get(),
                'show_nullclines': False,
                'show_equilibria': self.show_equilibria_var.get(),
                'show_eigenvectors': False,
                'trajectories': trajectories
            }
            
            # Renderizar
            self.log("\n✓ Generando diagrama de fase...")
            render_phase_plot(system, config, self.ax, self.log)
            
            # Añadir niveles de energía si γ=0
            if abs(gamma) < 1e-6 and self.show_energy_var.get():
                x_grid = np.linspace(x_range[0], x_range[1], 100)
                v_grid = np.linspace(v_range[0], v_range[1], 100)
                X, V = np.meshgrid(x_grid, v_grid)
                E = self.energy(X, V, omega)
                
                levels = np.linspace(E.min(), E.max(), 10)
                contours = self.ax.contour(X, V, E, levels=levels, colors='green',
                                          alpha=0.3, linewidths=0.8)
                self.ax.clabel(contours, inline=True, fontsize=8, fmt='E=%.2f')
                self.log("✓ Curvas de energía añadidas (E = ½v² + ½ω²x²)")
            
            # Personalizar etiquetas
            self.ax.set_xlabel('x (posición)', fontsize=11, fontweight='bold')
            self.ax.set_ylabel('v (velocidad)', fontsize=11, fontweight='bold')
            self.ax.set_title(f'Oscilador Armónico: {damping_type}\n(ω={omega}, γ={gamma})',
                            fontsize=12, fontweight='bold')
            
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
