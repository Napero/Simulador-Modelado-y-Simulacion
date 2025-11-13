"""
Paquete core: Núcleo de simulación de sistemas dinámicos.
"""

from .systems_2d import DynamicSystem2D, CustomSystem2D, LinearSystem2D, render_phase_plot
from .systems_1d import AutonomousSystem1D, plot_phase_diagram_1d, plot_solutions_1d
from .bifurcations import BifurcationAnalyzer1D, plot_bifurcation_diagram

__all__ = [
    'DynamicSystem2D',
    'CustomSystem2D',
    'LinearSystem2D',
    'render_phase_plot',
    'AutonomousSystem1D',
    'plot_phase_diagram_1d',
    'plot_solutions_1d',
    'BifurcationAnalyzer1D',
    'plot_bifurcation_diagram',
]
