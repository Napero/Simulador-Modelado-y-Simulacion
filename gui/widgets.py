"""
Widgets personalizados y utilidades para la interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk


# Paleta de colores
COLORS = {
    'bg_primary': '#f8f9fa',
    'bg_secondary': '#e9ecef',
    'bg_white': '#ffffff',
    'border': '#6c757d',
    'border_focus': '#4a90e2',
    'text_primary': '#212529',
    'text_secondary': '#495057',
    'btn_primary': '#4a90e2',
    'btn_success': '#28a745',
    'btn_danger': '#dc3545',
    'btn_warning': '#ffc107',
    'console_bg': '#212529',
    'console_fg': '#e9ecef',
}


class StyledButton(tk.Button):
    """Botón con estilo personalizado."""
    
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        """
        Args:
            style: 'primary', 'success', 'danger', 'warning'
        """
        color_map = {
            'primary': COLORS['btn_primary'],
            'success': COLORS['btn_success'],
            'danger': COLORS['btn_danger'],
            'warning': COLORS['btn_warning'],
        }
        
        bg_color = color_map.get(style, COLORS['btn_primary'])
        
        default_config = {
            'bg': bg_color,
            'fg': 'white',
            'font': ('Arial', 11, 'bold'),
            'relief': tk.FLAT,
            'borderwidth': 0,
            'cursor': 'hand2',
            'padx': 20,
            'pady': 10,
        }
        
        default_config.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **default_config)
        
        # Hover effects
        self.bind('<Enter>', lambda e: self.config(bg=self._lighten_color(bg_color)))
        self.bind('<Leave>', lambda e: self.config(bg=bg_color))
    
    def _lighten_color(self, color):
        """Aclara un color hex para efecto hover."""
        # Simple lightening: aumentar valores RGB
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = min(255, int(r * 1.1))
            g = min(255, int(g * 1.1))
            b = min(255, int(b * 1.1))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color


class StyledLabelFrame(tk.LabelFrame):
    """LabelFrame con estilo personalizado."""
    
    def __init__(self, parent, text, **kwargs):
        default_config = {
            'text': text,
            'font': ('Arial', 11, 'bold'),
            'fg': COLORS['text_secondary'],
            'bg': COLORS['bg_primary'],
            'relief': tk.GROOVE,
            'borderwidth': 2,
            'padx': 10,
            'pady': 10,
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)


class StyledEntry(tk.Entry):
    """Entry con estilo personalizado."""
    
    def __init__(self, parent, placeholder='', **kwargs):
        default_config = {
            'font': ('Arial', 10),
            'relief': tk.SOLID,
            'borderwidth': 2,
            'bg': COLORS['bg_white'],
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)
        
        self.placeholder = placeholder
        self.placeholder_active = False
        
        if placeholder:
            self.insert(0, placeholder)
            self.config(fg='gray')
            self.placeholder_active = True
            
            self.bind('<FocusIn>', self._on_focus_in)
            self.bind('<FocusOut>', self._on_focus_out)
        
        # Cambiar color de borde en focus
        self.bind('<FocusIn>', self._on_focus_in_border, add='+')
        self.bind('<FocusOut>', self._on_focus_out_border, add='+')
    
    def _on_focus_in(self, event):
        if self.placeholder_active:
            self.delete(0, tk.END)
            self.config(fg=COLORS['text_primary'])
            self.placeholder_active = False
    
    def _on_focus_out(self, event):
        if not self.get() and self.placeholder:
            self.insert(0, self.placeholder)
            self.config(fg='gray')
            self.placeholder_active = True
    
    def _on_focus_in_border(self, event):
        self.config(highlightbackground=COLORS['border_focus'],
                   highlightcolor=COLORS['border_focus'],
                   highlightthickness=2)
    
    def _on_focus_out_border(self, event):
        self.config(highlightthickness=0)
    
    def get_value(self):
        """Obtiene el valor, retorna '' si es placeholder."""
        if self.placeholder_active:
            return ''
        return self.get()


class ConsoleText(tk.Text):
    """Text widget estilo consola con autoscroll."""
    
    def __init__(self, parent, **kwargs):
        default_config = {
            'bg': COLORS['console_bg'],
            'fg': COLORS['console_fg'],
            'font': ('Consolas', 10),
            'relief': tk.FLAT,
            'borderwidth': 0,
            'padx': 10,
            'pady': 10,
            'wrap': tk.WORD,
            'state': tk.DISABLED,
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(parent, command=self.yview)
        self.config(yscrollcommand=scrollbar.set)
        
    def log(self, message, tag=None):
        """Agrega un mensaje a la consola."""
        self.config(state=tk.NORMAL)
        self.insert(tk.END, message + '\n', tag)
        self.see(tk.END)
        self.config(state=tk.DISABLED)
    
    def clear(self):
        """Limpia la consola."""
        self.config(state=tk.NORMAL)
        self.delete('1.0', tk.END)
        self.config(state=tk.DISABLED)


class SpinboxDouble(tk.Frame):
    """Spinbox para números decimales."""
    
    def __init__(self, parent, from_=-100, to=100, value=0, increment=0.1, **kwargs):
        super().__init__(parent, bg=COLORS['bg_primary'])
        
        self.var = tk.DoubleVar(value=value)
        
        self.spinbox = tk.Spinbox(
            self,
            from_=from_,
            to=to,
            increment=increment,
            textvariable=self.var,
            font=('Arial', 10),
            relief=tk.SOLID,
            borderwidth=1,
            **kwargs
        )
        self.spinbox.pack(fill=tk.BOTH, expand=True)
    
    def get(self):
        """Obtiene el valor actual."""
        return self.var.get()
    
    def set(self, value):
        """Establece el valor."""
        self.var.set(value)


class HelpButton(tk.Button):
    """Botón de ayuda con tooltip."""
    
    def __init__(self, parent, help_text, **kwargs):
        super().__init__(
            parent,
            text='?',
            font=('Arial', 10, 'bold'),
            bg=COLORS['btn_primary'],
            fg='white',
            relief=tk.FLAT,
            width=2,
            height=1,
            cursor='hand2',
            **kwargs
        )
        
        self.help_text = help_text
        self.tooltip = None
        
        self.bind('<Enter>', self._show_tooltip)
        self.bind('<Leave>', self._hide_tooltip)
    
    def _show_tooltip(self, event):
        x, y, _, _ = self.bbox("insert")
        x += self.winfo_rootx() + 25
        y += self.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip,
            text=self.help_text,
            justify=tk.LEFT,
            background='#ffffcc',
            relief=tk.SOLID,
            borderwidth=1,
            font=('Arial', 9),
            padx=10,
            pady=5
        )
        label.pack()
    
    def _hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def create_label_with_icon(parent, icon, text, **kwargs):
    """Crea un label con icono emoji."""
    default_config = {
        'font': ('Arial', 11),
        'fg': COLORS['text_primary'],
        'bg': COLORS['bg_primary'],
    }
    default_config.update(kwargs)
    
    label = tk.Label(parent, text=f"{icon} {text}", **default_config)
    return label


def create_info_panel(parent, title):
    """Crea un panel de información con título."""
    frame = tk.Frame(parent, bg=COLORS['bg_primary'])
    
    # Título
    title_label = create_label_with_icon(
        frame, '📊', title,
        font=('Arial', 11, 'bold')
    )
    title_label.pack(anchor=tk.W, pady=(0, 5))
    
    return frame
