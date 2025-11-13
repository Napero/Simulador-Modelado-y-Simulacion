# 🌀 Simulador de Sistemas Dinámicos

Herramienta completa para análisis de sistemas dinámicos 1D, 2D y 3D con interfaz gráfica desarrollada en Python y Tkinter.

---

## 🚀 Instalación y Ejecución

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```
### Paso 2: Ejecutar el Simulador

```bash
python main.py
```

---

## 📚 Sistemas Disponibles

### 📊 Sistemas 1D (6 tipos)
1. **Autónomo 1D** - Análisis de dx/dt = f(x)
2. **Bifurcación Saddle-Node** - Colisión y aniquilación de equilibrios
3. **Bifurcación Pitchfork Supercrítica** - Bifurcación simétrica
4. **Bifurcación Pitchfork Subcrítica** - Con histéresis y saltos bruscos
5. **Bifurcación Transcrítica** - Intercambio de estabilidad
6. **Conversión EDO → 1er Orden** - Reducción de orden de ecuaciones

### 📐 Sistemas 2D (8 tipos)
1. **Autónomo 2D** - Sistemas dx/dt = f(x,y), dy/dt = g(x,y)
2. **Lineal No Homogéneo** - Sistemas lineales con forzamiento
3. **No Lineal 2D** - Péndulo y otros sistemas no lineales
4. **Bifurcación de Hopf 2D** - Nacimiento de ciclos límite
5. **Oscilador de Van der Pol** - Ciclo límite autosostenido
6. **Sistema Conservativo (Doble Pozo)** - Hamiltoniano constante
7. **Romeo y Julieta** - Modelo de dinámica romántica (Strogatz)
8. **Oscilador Armónico** - Con amortiguamiento variable

### 🦋 Sistemas 3D (4 tipos)
1. **Sistema de Lorenz** - Atractor caótico clásico
2. **Sistema de Rössler** - Caos con banda plegada
3. **Circuito de Chua** - Atractor de doble scroll
4. **Sistemas de Sprott** - Los sistemas caóticos más simples

**Total: 18 sistemas diferentes** ✨

---

## 🛠️ Requisitos

- Python 3.8+
- NumPy
- Matplotlib
- SciPy
- SymPy
- Tkinter (incluido con Python)

---

## 📖 Uso Básico

1. Ejecuta el programa
2. Selecciona una pestaña (1D, 2D o 3D)
3. Elige el tipo de sistema que deseas simular
4. Ajusta los parámetros
5. Presiona **SIMULAR**
6. Observa el diagrama de fase y el análisis en la consola

---

## 👥 Créditos

Desarrollado para el curso de Modelado y Simulación por:
- Francisco Eduardo Nappa
- Rodrigo Alcorta
- Camila Ibar
- Matias Rapaport
- Gabriel Cayo
- Maximo Rosso
