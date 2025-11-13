"""
Pestaña para conversión de EDOs de orden superior a sistemas de primer orden.
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np

from gui.widgets import *


class ODEConversionTab(tk.Frame):
    """Pestaña para conversión de EDOs."""
    
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
            text="🔄 Conversión: EDO → Sistema 1er Orden\n\n"
                 "Convierte EDOs de orden superior\n"
                 "a sistemas de primer orden",
            bg='#e7f3ff',
            fg=COLORS['text_primary'],
            font=('Arial', 10),
            justify=tk.LEFT,
            padx=15,
            pady=15
        )
        desc_label.pack(fill=tk.X, pady=(0, 10))
        
        # EDO de segundo orden
        ode_frame = StyledLabelFrame(left_panel, "📝 EDO de Segundo Orden")
        ode_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(ode_frame, text="Forma general:",
                bg=COLORS['bg_primary'], font=('Arial', 9, 'italic')).pack(anchor=tk.W)
        tk.Label(ode_frame, text="y'' + a₁·y' + a₀·y = f(t)",
                bg=COLORS['bg_primary'], font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        # Coeficientes
        coef_frame = tk.Frame(ode_frame, bg=COLORS['bg_primary'])
        coef_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(coef_frame, text="a₀ =", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=6).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.a0_entry = StyledEntry(coef_frame, width=15)
        self.a0_entry.insert(0, "-4")  # Valor por defecto: oscilador armónico
        self.a0_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        tk.Label(coef_frame, text="a₁ =", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=6).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.a1_entry = StyledEntry(coef_frame, width=15)
        self.a1_entry.insert(0, "0")  # Valor por defecto
        self.a1_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        tk.Label(coef_frame, text="f(t) =", bg=COLORS['bg_primary'],
                font=('Arial', 10), width=6).grid(row=2, column=0, sticky=tk.W, pady=3)
        self.f_entry = StyledEntry(coef_frame, width=15)
        self.f_entry.insert(0, "0")  # Valor por defecto: homogéneo
        self.f_entry.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        coef_frame.columnconfigure(1, weight=1)
        
        # Info
        info_frame = tk.Frame(ode_frame, bg='#fff3cd', relief=tk.SOLID, borderwidth=1)
        info_frame.pack(fill=tk.X, pady=(10, 5))
        
        tk.Label(info_frame, text="ℹ️ Ejemplos:",
                bg='#fff3cd', font=('Arial', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=3)
        tk.Label(info_frame, text="• Oscilador armónico: a₀=-4, a₁=0, f(t)=0",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Amortiguado: a₀=-4, a₁=-0.5, f(t)=0",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5)
        tk.Label(info_frame, text="• Forzado: a₀=-4, a₁=0, f(t)=sin(t)",
                bg='#fff3cd', font=('Arial', 8)).pack(anchor=tk.W, padx=5, pady=(0, 3))
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=COLORS['bg_primary'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        StyledButton(btn_frame, "🔄 CONVERTIR",
                    command=self.convert_ode,
                    style='success').pack(fill=tk.X, pady=(0, 5))
        
        StyledButton(btn_frame, "📋 EJEMPLOS",
                    command=self.show_examples,
                    style='primary').pack(fill=tk.X, pady=(0, 5))
        
        StyledButton(btn_frame, "🗑 LIMPIAR",
                    command=self.clear_all,
                    style='danger').pack(fill=tk.X)
        
        # === PANEL DERECHO ===
        
        # Resultado
        result_label = create_label_with_icon(
            right_panel, '📊', 'Sistema Convertido:',
            font=('Arial', 12, 'bold')
        )
        result_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Text area con scrollbar
        self.result_text = scrolledtext.ScrolledText(
            right_panel,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg=COLORS['bg_white'],
            fg=COLORS['text_primary'],
            relief=tk.SOLID,
            borderwidth=1,
            padx=15,
            pady=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Muestra mensaje de bienvenida."""
        msg = """
╔════════════════════════════════════════════════════════════╗
║   CONVERSIÓN DE EDO A SISTEMA DE PRIMER ORDEN             ║
╚════════════════════════════════════════════════════════════╝

Este módulo convierte EDOs de segundo orden a sistemas de
primer orden que pueden ser analizados como sistemas 2D.

CONVERSIÓN:
-----------
La EDO:  y'' + a₁·y' + a₀·y = f(t)

Se convierte en el sistema:
  x₁' = x₂
  x₂' = -a₀·x₁ - a₁·x₂ + f(t)

Donde:
  x₁ = y     (posición)
  x₂ = y'    (velocidad)

EJEMPLO:
--------
Oscilador armónico simple:  y'' + 4y = 0

Se convierte en:
  x₁' = x₂
  x₂' = -4·x₁

Este sistema puede analizarse en la pestaña "Lineal No-Homog."

═══════════════════════════════════════════════════════════

Ingresa los coeficientes y presiona CONVERTIR
"""
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', msg)
    
    def convert_ode(self):
        """Convierte la EDO a sistema."""
        try:
            # Obtener coeficientes
            a0 = float(self.a0_entry.get_value() or "0")
            a1 = float(self.a1_entry.get_value() or "0")
            f_str = self.f_entry.get_value() or "0"
            
            # Construir matriz A
            A = np.array([
                [0, 1],
                [-a0, -a1]
            ])
            
            # Autovalores
            eigenvalues = np.linalg.eigvals(A)
            
            # Clasificación del sistema
            system_type = self.classify_system(eigenvalues, a0, a1)
            
            # Construir resultado
            result = f"""
╔════════════════════════════════════════════════════════════╗
║   RESULTADO DE LA CONVERSIÓN                               ║
╚════════════════════════════════════════════════════════════╝

EDO ORIGINAL:
-------------
  y'' + ({a1})·y' + ({a0})·y = {f_str}

SISTEMA EQUIVALENTE DE PRIMER ORDEN:
------------------------------------
Definiendo:
  x₁ = y      (posición)
  x₂ = y'     (velocidad)

El sistema es:
  x₁' = x₂
  x₂' = {-a0}·x₁ + ({-a1})·x₂ + ({f_str})

FORMA MATRICIAL:
----------------
  X' = A·X + b

Donde:
       [x₁]         [ 0    1  ]        [  0   ]
  X =  [  ]    A =  [         ]   b =  [      ]
       [x₂]         [{-a0} {-a1}]        [{f_str}]

MATRIZ A:
         [ {A[0,0]:7.3f}  {A[0,1]:7.3f} ]
    A =  [                      ]
         [ {A[1,0]:7.3f}  {A[1,1]:7.3f} ]

AUTOVALORES:
-----------"""
            
            for i, eigval in enumerate(eigenvalues):
                if np.iscomplex(eigval):
                    result += f"\n  λ{i+1} = {eigval.real:.4f} + {eigval.imag:.4f}i"
                else:
                    result += f"\n  λ{i+1} = {np.real(eigval):.4f}"
            
            result += f"\n\nCLASIFICACIÓN DEL SISTEMA:\n"
            result += f"--------------------------\n"
            result += f"{system_type}\n"
            
            # Punto de equilibrio
            if f_str == "0":
                result += f"\nPUNTO DE EQUILIBRIO:\n"
                result += f"-------------------\n"
                result += f"  x₁* = 0  (y* = 0)\n"
                result += f"  x₂* = 0  (y'* = 0)\n"
                result += f"\nEl origen es el único punto de equilibrio.\n"
            else:
                result += f"\n⚠ NOTA: Sistema no-homogéneo (f(t) ≠ 0)\n"
                result += f"El punto de equilibrio puede variar con t.\n"
            
            result += f"\n" + "═"*60 + "\n"
            result += f"\n💡 PRÓXIMOS PASOS:\n"
            result += f"\n1. Copia los valores de la matriz A:"
            result += f"\n   a₁₁ = {A[0,0]},  a₁₂ = {A[0,1]}"
            result += f"\n   a₂₁ = {A[1,0]},  a₂₂ = {A[1,1]}"
            result += f"\n"
            result += f"\n2. Vector b:"
            result += f"\n   b₁ = 0"
            result += f"\n   b₂ = {f_str}"
            result += f"\n"
            result += f"\n3. Ve a la pestaña 'Lineal No-Homog.'"
            result += f"\n"
            result += f"\n4. Ingresa estos valores y simula el sistema."
            result += f"\n"
            result += f"\n═"*60 + "\n"
            
            # Mostrar resultado
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', result)
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en valores numéricos:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en la conversión:\n{str(e)}")
    
    def classify_system(self, eigenvalues, a0, a1):
        """Clasifica el tipo de sistema según autovalores."""
        lambda1, lambda2 = eigenvalues
        
        classification = ""
        
        if np.iscomplex(lambda1):
            real_part = lambda1.real
            imag_part = abs(lambda1.imag)
            
            if abs(real_part) < 1e-8:
                classification = "🟢 CENTRO (Oscilador armónico simple)\n"
                classification += f"   Frecuencia: ω = {imag_part:.4f}\n"
                classification += f"   Período: T = {2*np.pi/imag_part:.4f}\n"
                classification += "   Soluciones periódicas, órbitas cerradas."
            elif real_part < 0:
                classification = "🟢 FOCO ESPIRAL ESTABLE (Oscilaciones amortiguadas)\n"
                classification += f"   Las soluciones espiralan hacia el origen.\n"
                classification += f"   Amortiguamiento: α = {-real_part:.4f}"
            else:
                classification = "🔴 FOCO ESPIRAL INESTABLE\n"
                classification += f"   Las soluciones espiralan alejándose del origen.\n"
                classification += f"   Crecimiento: α = {real_part:.4f}"
        else:
            lambda1, lambda2 = np.real(lambda1), np.real(lambda2)
            
            if lambda1 * lambda2 > 0:
                if lambda1 < 0:
                    classification = "🟢 NODO ESTABLE\n"
                    classification += "   Todas las soluciones tienden al origen.\n"
                    classification += "   Sin oscilaciones (sobreamortiguado)."
                else:
                    classification = "🔴 NODO INESTABLE\n"
                    classification += "   Todas las soluciones se alejan del origen."
            else:
                classification = "🟠 PUNTO DE SILLA (INESTABLE)\n"
                classification += "   Trayectorias hiperbólicas.\n"
                classification += "   Sistema inestable."
        
        # Info adicional
        if a1 == 0 and a0 > 0:
            classification += "\n\n📌 INTERPRETACIÓN FÍSICA:\n"
            classification += "   Sistema sin amortiguamiento.\n"
            classification += f"   Frecuencia natural: ω₀ = {np.sqrt(a0):.4f}"
        elif a1 != 0:
            classification += "\n\n📌 INTERPRETACIÓN FÍSICA:\n"
            classification += f"   Coeficiente de amortiguamiento: {a1}\n"
            if a1 > 0:
                classification += "   Amortiguamiento positivo (disipativo)."
            else:
                classification += "   Amortiguamiento negativo (energía añadida)."
        
        return classification
    
    def show_examples(self):
        """Muestra ejemplos predefinidos."""
        examples = """
╔════════════════════════════════════════════════════════════╗
║   EJEMPLOS CLÁSICOS                                        ║
╚════════════════════════════════════════════════════════════╝

1. OSCILADOR ARMÓNICO SIMPLE
   ---------------------------
   EDO: y'' + 4y = 0
   
   Coeficientes:
     a₀ = -4
     a₁ = 0
     f(t) = 0
   
   Resultado: Centro (órbitas circulares)

2. OSCILADOR AMORTIGUADO
   ----------------------
   EDO: y'' + 0.5y' + 4y = 0
   
   Coeficientes:
     a₀ = -4
     a₁ = -0.5
     f(t) = 0
   
   Resultado: Foco espiral estable

3. OSCILADOR SOBRE-AMORTIGUADO
   ----------------------------
   EDO: y'' + 6y' + 5y = 0
   
   Coeficientes:
     a₀ = -5
     a₁ = -6
     f(t) = 0
   
   Resultado: Nodo estable

4. SISTEMA INESTABLE
   ------------------
   EDO: y'' - y = 0
   
   Coeficientes:
     a₀ = 1
     a₁ = 0
     f(t) = 0
   
   Resultado: Punto de silla

5. OSCILADOR FORZADO
   ------------------
   EDO: y'' + 4y = sin(t)
   
   Coeficientes:
     a₀ = -4
     a₁ = 0
     f(t) = sin(t)
   
   Resultado: Centro + forzamiento externo

═══════════════════════════════════════════════════════════

Copia los valores de cualquier ejemplo y presiona CONVERTIR
"""
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', examples)
    
    def clear_all(self):
        """Limpia todo."""
        self.show_welcome_message()
