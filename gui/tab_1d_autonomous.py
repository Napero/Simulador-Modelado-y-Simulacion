"""
Pestaña de análisis de sistemas autónomos 1D.
"""

import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.systems_1d import AutonomousSystem1D, plot_phase_diagram_1d, plot_solutions_1d
from utils.expression_parser import ExpressionParser


class AutonomousTab1D(tk.Frame):
    """Pestaña para análisis de sistemas autónomos 1D."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz."""
        # Layout principal
        left_panel = tk.Frame(self, bg=COLORS['bg_primary'], width=450)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)
        
        right_panel = tk.Frame(self, bg=COLORS['bg_primary'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === PANEL IZQUIERDO ===
        
        desc_label = tk.Label(
            left_panel,
            text="📊 Análisis de Sistemas Autónomos 1D\n\n"
                 "Analiza sistemas de la forma:\n"
                 "  dx/dt = f(x)",
            bg='#d1ecf1',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # Ecuación
        eq_frame = StyledLabelFrame(left_panel, "📝 Ecuación Diferencial")
        eq_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(eq_frame, text="dx/dt =", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(anchor=tk.W)
        self.f_entry = StyledEntry(eq_frame)
        self.f_entry.insert(0, "x**2 - 4")  # Valor por defecto
        self.f_entry.config(fg=COLORS['text_primary'])
        self.f_entry.pack(fill=tk.X, pady=(0, 5))
        
        help_btn = HelpButton(eq_frame, ExpressionParser.get_help_text())
        help_btn.pack(anchor=tk.E)
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango x
        x_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        x_frame.pack(fill=tk.X, pady=5)
        tk.Label(x_frame, text="x:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(x_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_min = SpinboxDouble(x_frame, from_=-100, to=100, value=-5, width=8)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-100, to=100, value=5, width=8)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango t
        t_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        t_frame.pack(fill=tk.X, pady=5)
        tk.Label(t_frame, text="t:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(t_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.t_min = SpinboxDouble(t_frame, from_=0, to=100, value=0, width=8)
        self.t_min.pack(side=tk.LEFT, padx=5)
        tk.Label(t_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.t_max = SpinboxDouble(t_frame, from_=0, to=100, value=10, width=8)
        self.t_max.pack(side=tk.LEFT, padx=5)
        tk.Label(t_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Condiciones iniciales
        ci_frame = StyledLabelFrame(left_panel, "📍 Condiciones Iniciales")
        ci_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(ci_frame, text="Valores de x₀ (separados por comas):",
                bg=COLORS['bg_primary'], font=('Arial', 9)).pack(anchor=tk.W)
        self.ci_entry = StyledEntry(ci_frame)
        self.ci_entry.insert(0, "-3, -1, 0, 1, 3")  # Valor por defecto
        self.ci_entry.config(fg=COLORS['text_primary'])
        self.ci_entry.pack(fill=tk.X)
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        StyledButton(btn_frame, "▶ ANALIZAR",
                    command=self.run_analysis,
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
        
        # Matplotlib figure con 2 subplots
        self.fig = Figure(figsize=(10, 10), dpi=100)
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)
        self.fig.tight_layout(pad=3.0)
        
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
        
        self.console.log("Simulador de sistemas autónomos 1D")
        self.console.log("Ingresa la ecuación dx/dt = f(x) y presiona ANALIZAR")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_analysis(self):
        """Ejecuta el análisis."""
        self.console.clear()
        self.ax1.clear()
        self.ax2.clear()
        
        try:
            # Obtener ecuación
            f_expr = self.f_entry.get_value()
            
            if not f_expr:
                messagebox.showwarning("Advertencia", "Ingresa la ecuación dx/dt")
                return
            
            self.log("Iniciando análisis...")
            self.log(f"dx/dt = {f_expr}")
            
            # Validar
            valid, error = ExpressionParser.validate_expression(f_expr, ['x'])
            if not valid:
                messagebox.showerror("Error", f"Error en la ecuación: {error}")
                return
            
            # Obtener rangos
            x_range = (self.x_min.get(), self.x_max.get())
            t_range = (self.t_min.get(), self.t_max.get())
            
            self.log(f"Rango x: [{x_range[0]}, {x_range[1]}]")
            self.log(f"Rango t: [{t_range[0]}, {t_range[1]}]")
            self.log("-" * 50)
            
            # Crear sistema
            system = AutonomousSystem1D(f_expr)
            
            # Diagrama de fase
            self.log("Analizando equilibrios...")
            plot_phase_diagram_1d(system, x_range, self.ax1, self.log)
            
            # Soluciones temporales
            ci_text = self.ci_entry.get_value()
            if ci_text:
                try:
                    initial_conditions = [float(x.strip()) for x in ci_text.split(',')]
                    self.log(f"\nCondiciones iniciales: {initial_conditions}")
                    
                    plot_solutions_1d(system, initial_conditions, t_range, self.ax2)
                except:
                    self.log("⚠ Error parseando condiciones iniciales, usando valores por defecto")
                    initial_conditions = [-3, -1, 0, 1, 3]
                    plot_solutions_1d(system, initial_conditions, t_range, self.ax2)
            
            self.log("\n✓ Análisis completado exitosamente")
            self.fig.tight_layout(pad=3.0)
            self.canvas.draw()
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"Error en el análisis:\n{str(e)}")
    
    def clear_all(self):
        """Limpia todo."""
        self.f_entry.delete(0, tk.END)
        self.ci_entry.delete(0, tk.END)
        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()
        self.console.clear()
        self.log("Interfaz limpiada")
