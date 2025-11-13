"""
Pestaña de análisis de bifurcaciones.
"""

import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from gui.widgets import *
from core.bifurcations import BifurcationAnalyzer1D, plot_bifurcation_diagram, plot_phase_diagrams_at_r
from utils.expression_parser import ExpressionParser


class BifurcationTab(tk.Frame):
    """Pestaña para análisis de bifurcaciones."""
    
    def __init__(self, parent, bifurcation_type='saddle-node'):
        """
        Args:
            bifurcation_type: 'saddle-node', 'pitchfork', 'transcritica'
        """
        super().__init__(parent, bg=COLORS['bg_primary'])
        self.bifurcation_type = bifurcation_type
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
        
        # Descripción según tipo
        descriptions = {
            'saddle-node': (
                "🔵 Bifurcación Saddle-Node\n\n"
                "Aparición o desaparición de equilibrios.\n"
                "Ejemplo: f(x, r) = r + x²"
            ),
            'pitchfork': (
                "🔴 Bifurcación Pitchfork\n\n"
                "Un equilibrio se bifurca en tres.\n"
                "Ejemplo: f(x, r) = r*x - x³"
            ),
            'transcritica': (
                "🟢 Bifurcación Transcrítica\n\n"
                "Dos equilibrios se cruzan e intercambian estabilidad.\n"
                "Ejemplo: f(x, r) = r*x - x²"
            )
        }
        
        # Ejemplos por defecto
        default_exprs = {
            'saddle-node': 'r + x**2',
            'pitchfork': 'r*x - x**3',
            'transcritica': 'r*x - x**2'
        }
        
        colors_desc = {
            'saddle-node': '#d1ecf1',
            'pitchfork': '#f8d7da',
            'transcritica': '#d4edda'
        }
        
        desc_text = descriptions.get(self.bifurcation_type, descriptions['saddle-node'])
        desc_color = colors_desc.get(self.bifurcation_type, '#d1ecf1')
        
        desc_label = tk.Label(
            left_panel,
            text=desc_text,
            bg=desc_color,
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
        
        tk.Label(eq_frame, text="f(x, r) =", bg=COLORS['bg_primary'],
                font=('Arial', 10)).pack(anchor=tk.W)
        
        default_expr = default_exprs.get(self.bifurcation_type, 'r + x**2')
        self.f_entry = StyledEntry(eq_frame)
        self.f_entry.insert(0, default_expr)
        self.f_entry.config(fg=COLORS['text_primary'])
        self.f_entry.pack(fill=tk.X, pady=(0, 5))
        
        help_btn = HelpButton(eq_frame, ExpressionParser.get_help_text())
        help_btn.pack(anchor=tk.E)
        
        # Rangos
        range_frame = StyledLabelFrame(left_panel, "📐 Rangos")
        range_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Rango r
        r_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        r_frame.pack(fill=tk.X, pady=5)
        tk.Label(r_frame, text="r:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(r_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.r_min = SpinboxDouble(r_frame, from_=-20, to=20, value=-2, width=8)
        self.r_min.pack(side=tk.LEFT, padx=5)
        tk.Label(r_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.r_max = SpinboxDouble(r_frame, from_=-20, to=20, value=2, width=8)
        self.r_max.pack(side=tk.LEFT, padx=5)
        tk.Label(r_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Rango x
        x_frame = tk.Frame(range_frame, bg=COLORS['bg_primary'])
        x_frame.pack(fill=tk.X, pady=5)
        tk.Label(x_frame, text="x:", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=3).pack(side=tk.LEFT)
        tk.Label(x_frame, text="[", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_min = SpinboxDouble(x_frame, from_=-20, to=20, value=-3, width=8)
        self.x_min.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text=",", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        self.x_max = SpinboxDouble(x_frame, from_=-20, to=20, value=3, width=8)
        self.x_max.pack(side=tk.LEFT, padx=5)
        tk.Label(x_frame, text="]", bg=COLORS['bg_primary']).pack(side=tk.LEFT)
        
        # Diagramas de fase
        phase_frame = StyledLabelFrame(left_panel, "📊 Diagramas de Fase")
        phase_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(phase_frame, text="Valores de r (separados por comas):",
                bg=COLORS['bg_primary'], font=('Arial', 9)).pack(anchor=tk.W)
        self.r_values_entry = StyledEntry(phase_frame)
        self.r_values_entry.insert(0, "-1, 0, 1")  # Valor por defecto
        self.r_values_entry.config(fg=COLORS['text_primary'])
        self.r_values_entry.pack(fill=tk.X)
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        StyledButton(btn_frame, "▶ ANALIZAR BIFURCACIÓN",
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
        
        # Matplotlib figure
        self.fig = Figure(figsize=(12, 10), dpi=100)
        
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
        
        self.console.log(f"Análisis de bifurcación: {self.bifurcation_type}")
        self.console.log("Ingresa f(x, r) y presiona ANALIZAR")
    
    def log(self, message):
        """Registra mensaje."""
        self.console.log(message)
    
    def run_analysis(self):
        """Ejecuta el análisis de bifurcación."""
        self.console.clear()
        self.fig.clear()
        
        try:
            # Obtener ecuación
            f_expr = self.f_entry.get_value()
            
            if not f_expr:
                messagebox.showwarning("Advertencia", "Ingresa f(x, r)")
                return
            
            self.log("Iniciando análisis de bifurcación...")
            self.log(f"f(x, r) = {f_expr}")
            
            # Validar
            valid, error = ExpressionParser.validate_expression(f_expr, ['x', 'r'])
            if not valid:
                messagebox.showerror("Error", f"Error en la ecuación: {error}")
                return
            
            # Rangos
            r_range = (self.r_min.get(), self.r_max.get())
            x_range = (self.x_min.get(), self.x_max.get())
            
            self.log(f"Rango r: [{r_range[0]}, {r_range[1]}]")
            self.log(f"Rango x: [{x_range[0]}, {x_range[1]}]")
            self.log("-" * 50)
            
            # Crear analizador
            analyzer = BifurcationAnalyzer1D(f_expr, param_name='r')
            
            # Valores de r para diagramas de fase
            r_values_text = self.r_values_entry.get_value()
            if r_values_text:
                try:
                    r_values = [float(r.strip()) for r in r_values_text.split(',')]
                except:
                    r_values = []
            else:
                r_values = []
            
            # Layout de subplots
            if r_values:
                # Diagrama de bifurcación + diagramas de fase
                n_phase = len(r_values)
                n_rows = 2 + (n_phase // 2 + (1 if n_phase % 2 else 0))
                
                # Diagrama de bifurcación (ocupa primeras 2 filas)
                ax_bif = self.fig.add_subplot(n_rows, 2, (1, 4))
                plot_bifurcation_diagram(analyzer, r_range, x_range, ax_bif, self.log)
                
                # Diagramas de fase
                axes_phase = []
                for i in range(n_phase):
                    row = 2 + i // 2
                    col = 1 + i % 2
                    ax = self.fig.add_subplot(n_rows, 2, row * 2 + col)
                    axes_phase.append(ax)
                
                plot_phase_diagrams_at_r(analyzer, r_values, x_range, axes_phase, self.log)
            else:
                # Solo diagrama de bifurcación
                ax_bif = self.fig.add_subplot(111)
                plot_bifurcation_diagram(analyzer, r_range, x_range, ax_bif, self.log)
            
            self.log("\n✓ Análisis completado exitosamente")
            self.fig.tight_layout(pad=3.0)
            self.canvas.draw()
            
        except Exception as e:
            self.log(f"✗ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error en el análisis:\n{str(e)}")
    
    def clear_all(self):
        """Limpia todo."""
        self.fig.clear()
        self.canvas.draw()
        self.console.clear()
        self.log("Interfaz limpiada")
