"""
Ventana principal de la aplicación con sistema de pestañas.
"""

import tkinter as tk
from tkinter import ttk

from gui.widgets import COLORS
from gui.tab_2d_autonomous import AutonomousTab2D
from gui.tab_1d_autonomous import AutonomousTab1D
from gui.tab_bifurcation import BifurcationTab
from gui.tab_2d_linear import LinearNonHomogeneousTab
from gui.tab_ode_conversion import ODEConversionTab
from gui.tab_hopf_2d import HopfBifurcationTab
from gui.tab_lorenz import LorenzTab
from gui.tab_vanderpol import VanDerPolTab
from gui.tab_conservative import ConservativeTab
from gui.tab_romeojulieta import RomeoJulietaTab
from gui.tab_pitchfork_subcritical import PitchforkSubcriticalTab
from gui.tab_oscilador_armonico import OsciladorArmonicoTab
from gui.tab_rossler import RosslerTab
from gui.tab_chua import ChuaTab
from gui.tab_sprott import SprottTab


class SimuladorApp(tk.Tk):
    """Aplicación principal del simulador."""
    
    def __init__(self):
        super().__init__()
        
        self.title("🌀 Simulador de Sistemas Dinámicos - Modelado y Simulación - Equipo 4")
        self.geometry("1400x900")
        self.configure(bg=COLORS['bg_primary'])
        
        # Configurar estilo
        self.setup_style()
        
        # Crear interfaz
        self.create_widgets()
        
        # Centrar ventana
        self.center_window()
    
    def setup_style(self):
        """Configura los estilos de ttk."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Notebook
        style.configure('TNotebook', background=COLORS['bg_primary'])
        style.configure('TNotebook.Tab',
                       background=COLORS['bg_secondary'],
                       foreground=COLORS['text_primary'],
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', COLORS['bg_white'])],
                 foreground=[('selected', COLORS['btn_primary'])])
    
    def create_widgets(self):
        """Crea los widgets principales."""
        # Notebook principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # === PESTAÑA: Análisis 1D ===
        tab_1d = ttk.Frame(self.notebook)
        self.notebook.add(tab_1d, text="� Análisis 1D")
        
        # Sub-notebook para 1D
        notebook_1d = ttk.Notebook(tab_1d)
        notebook_1d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sub-pestañas 1D
        autonomous_1d_tab = AutonomousTab1D(notebook_1d)
        notebook_1d.add(autonomous_1d_tab, text="Autónomo 1D")
        
        # Bifurcaciones
        saddle_node_tab = BifurcationTab(notebook_1d, bifurcation_type='saddle-node')
        notebook_1d.add(saddle_node_tab, text="Bif. Saddle-Node")
        
        pitchfork_tab = BifurcationTab(notebook_1d, bifurcation_type='pitchfork')
        notebook_1d.add(pitchfork_tab, text="Bif. Pitchfork")
        
        pitchfork_subcritical_tab = PitchforkSubcriticalTab(notebook_1d)
        notebook_1d.add(pitchfork_subcritical_tab, text="Bif. Pitchfork Subcrítica")
        
        transcritica_tab = BifurcationTab(notebook_1d, bifurcation_type='transcritica')
        notebook_1d.add(transcritica_tab, text="Bif. Transcrítica")
        
        # Conversión de EDOs
        ode_tab = ODEConversionTab(notebook_1d)
        notebook_1d.add(ode_tab, text="EDO → 1er Orden")
        
        # === PESTAÑA: Análisis 2D ===
        tab_2d = ttk.Frame(self.notebook)
        self.notebook.add(tab_2d, text="📐 Análisis 2D")
        
        # Sub-notebook para 2D
        notebook_2d = ttk.Notebook(tab_2d)
        notebook_2d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sub-pestañas 2D
        autonomous_2d_tab = AutonomousTab2D(notebook_2d)
        notebook_2d.add(autonomous_2d_tab, text="Autónomo 2D")
        
        linear_tab = LinearNonHomogeneousTab(notebook_2d)
        notebook_2d.add(linear_tab, text="Lineal No-Homog.")
        
        nonlinear_tab = AutonomousTab2D(notebook_2d, default_dx="y", default_dy="-sin(x) - 0.5*y", title="Sistemas No-Lineales 2D")
        notebook_2d.add(nonlinear_tab, text="No-Lineal")
        
        hopf_tab = HopfBifurcationTab(notebook_2d)
        notebook_2d.add(hopf_tab, text="Bif. Hopf 2D")
        
        vanderpol_tab = VanDerPolTab(notebook_2d)
        notebook_2d.add(vanderpol_tab, text="Van der Pol")
        
        conservative_tab = ConservativeTab(notebook_2d)
        notebook_2d.add(conservative_tab, text="Conservativo")
        
        romeojulieta_tab = RomeoJulietaTab(notebook_2d)
        notebook_2d.add(romeojulieta_tab, text="Romeo y Julieta")
        
        oscilador_tab = OsciladorArmonicoTab(notebook_2d)
        notebook_2d.add(oscilador_tab, text="Oscilador Armónico")
        
        # === PESTAÑA: Análisis 3D ===
        tab_3d = ttk.Frame(self.notebook)
        self.notebook.add(tab_3d, text="🦋 Análisis 3D")
        
        # Sub-notebook para 3D
        notebook_3d = ttk.Notebook(tab_3d)
        notebook_3d.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sub-pestañas 3D
        lorenz_tab = LorenzTab(notebook_3d)
        notebook_3d.add(lorenz_tab, text="Sistema de Lorenz")
        
        rossler_tab = RosslerTab(notebook_3d)
        notebook_3d.add(rossler_tab, text="Sistema de Rössler")
        
        chua_tab = ChuaTab(notebook_3d)
        notebook_3d.add(chua_tab, text="Circuito de Chua")
        
        sprott_tab = SprottTab(notebook_3d)
        notebook_3d.add(sprott_tab, text="Sistemas de Sprott")
        
        # Barra de estado
        self.status_bar = tk.Label(
            self,
            text="Listo | Simulador de Sistemas Dinámicos v1.0",
            bg=COLORS['bg_secondary'],
            fg=COLORS['text_secondary'],
            font=('Arial', 9),
            anchor=tk.W,
            padx=10
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


def main():
    """Punto de entrada de la aplicación."""
    app = SimuladorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
