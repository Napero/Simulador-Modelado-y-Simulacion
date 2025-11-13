# Apuntes de Modelado y Simulación (Segunda Parte)

## Clase 7: Sistemas Autónomos Desacoplados

### 1) Sistemas dinámicos (definición y contexto)
Modelos matemáticos que describen cómo cambia el estado de un sistema en el tiempo; pueden ser continuos (EDO) o discretos. Aplicaciones en física, biología, economía e ingeniería.  
**Características**:  
- Evolución temporal.  
- Determinismo (el estado futuro está fijado por el estado actual y las leyes).  
- No linealidad (puede aparecer caos; comportamientos complejos).

[imagen: línea de tiempo histórica con Newton, Euler, Laplace, Poincaré y Lorenz; retratos a los costados]

### 2) Diagramas de fase (conceptos básicos)
Representan trayectorias en el espacio de fases para distintas condiciones iniciales.  
- **Ejes**: variables de estado (por ejemplo posición y velocidad).  
- **Trayectorias**: cómo evoluciona el sistema.  
- **Puntos críticos**: estados de equilibrio (no cambian en el tiempo).  

[imagen: diagrama de fase 2D con ejes x e y; varias curvas solución que se acercan a un punto; flechas indicando orientación temporal]

### 3) Clasificación local de puntos de equilibrio (2D, por espectro de la Jacobiana)
Sea \(J\) la matriz jacobiana evaluada en el equilibrio:
\[
J=
\begin{pmatrix}
\frac{\partial f_1}{\partial x} & \frac{\partial f_1}{\partial y}\\
\frac{\partial f_2}{\partial x} & \frac{\partial f_2}{\partial y}
\end{pmatrix}_{(x^*,y^*)}
\]
- **Silla**: algún autovalor con parte real positiva y otro negativa; inestable.  
- **Nodo estable**: partes reales negativas; atractor.  
- **Nodo inestable**: partes reales positivas; repulsor.  
- **Centro**: autovalores puramente imaginarios; estable en sentido de Lyapunov (no asintótico).  
- **No hiperbólico**: alguna parte real cero; el análisis lineal no concluye.

[imagen: mosaico con cinco paneles; cada panel muestra el campo de direcciones típico de silla, nodo estable, nodo inestable, centro y caso no hiperbólico]

### 4) Estabilidad en 1D y 2D
- **1D**: para \( \dot x=f(x) \), un equilibrio \(x^*\) es estable si \(f'(x^*)<0\); inestable si \(f'(x^*)>0\).  
- **2D**: según los autovalores de \(J\) evaluado en el equilibrio.

### 5) Estabilidad asintótica (idea de Lyapunov)
Un equilibrio \(x^*\) es asintóticamente estable si las trayectorias con condiciones iniciales cercanas no solo permanecen cerca sino que **convergen**:
\[
\lim_{t\to\infty} x(t)=x^*
\]
Interpretación física: estabilidad simple mantiene la cercanía; estabilidad asintótica además retorna al equilibrio después de perturbaciones.

[imagen: gráfico 2D con distancia \(\|x(t)-x^*\|\) decreciendo a cero cuando \(t\) crece]

### 6) Sistemas autónomos
EDO autónoma:
\[
\frac{dx}{dt}=f(x)\quad\text{(no depende explícitamente de \(t\))}
\]
Análisis vía diagramas de fase, equilibrios \(f(x)=0\) y estabilidad.

#### 6.1) Desacoplados 1D
Ejemplo:
\[
\dot x=-kx,\; k>0 \quad\Rightarrow\quad \int\frac{dx}{x}=\int -k\,dt \;\Rightarrow\; x(t)=x_0 e^{-kt}
\]

#### 6.2) Acoplados (mención)
En general el término acoplado aplica a sistemas de varias variables:
\[
\dot x=f(x,y),\quad \dot y=g(x,y)
\]
Puede considerarse acoplar a un parámetro externo \(\lambda\):
\[
\dot x=f(x,\lambda)
\]
(si \(\lambda\) depende del tiempo o de otra ecuación, el sistema aumenta de dimensión).

---

## Clase 8: Bifurcaciones

### 1) Definición
Pequeños cambios en parámetros provocan cambios cualitativos en la dinámica: aparición o desaparición de equilibrios, ciclos límite, o cambios de estabilidad.

### 2) Bifurcaciones locales (ejemplos típicos)
- **Silla–nodo**:
  \[
  \dot x=r+x^2
  \]
  Dos equilibrios (uno estable y otro inestable) colisionan y desaparecen al variar \(r\).

  [imagen: diagrama \(x\) vs \(r\) con ramas que se tocan formando una parábola abierta; ramas con estilos de línea distintos para estable e inestable]

- **Pitchfork supercrítica**:
  \[
  \dot x=r\,x - x^3
  \]
  Para \(r<0\): único equilibrio estable en \(x=0\). Para \(r>0\): el origen se vuelve inestable y emergen dos equilibrios estables en \(x=\pm\sqrt{r}\).

  [imagen: diagrama de bifurcación con rama central que pierde estabilidad en \(r=0\) y dos ramas simétricas estables que emergen]

- **Pitchfork subcrítica**:
  \[
  \dot x=r\,x + x^3
  \]
  Para \(r<0\): tres equilibrios (origen estable; dos inestables). En \(r=0\) los inestables colisionan con el origen; el origen cambia su naturaleza.

  [imagen: diagrama con rama central estable para \(r<0\) que se vuelve inestable en \(r=0\); ramas inestables se fusionan en el origen]

- **Pitchfork con histeresis**:
  \[
  \dot x=r\,x + x^3 - x^5
  \]
  Estructura más rica; puede coexistir concilios de estabilidad y regiones con silla–nodo para \(r\) negativos pequeños.

  [imagen: diagrama con forma de tridente ancho; ventanas de multies­tabilidad y flechas que indican saltos de histeresis]

- **Transcrítica**:
  Intercambio de estabilidad entre dos equilibrios cuando \(r\) pasa por el valor crítico.

  [imagen: dos ramas que se cruzan en \(r=0\); la estabilidad se intercambia en el cruce]

### 3) Bifurcaciones globales
Cambios topológicos que involucran órbitas y conjuntos invariantes no locales; por ejemplo conexiones **homoclínicas** y **heteroclínicas**.

[imagen: retrato de fase con separatrices que conectan sillas; flechas mostrando conexiones mono y heteroclínicas]

### 4) Bifurcación de Hopf
Autovalores complejos cruzan el eje imaginario; aparece un ciclo límite. Ejemplo genérico:
\[
\begin{cases}
\dot x = r\,y - x\\
\dot y = -r\,x - y + x^2 + y^2\,y
\end{cases}
\quad\text{Hopf en } r=1
\]

[imagen: retrato de fase 2D; foco estable que al variar \(r\) genera un ciclo límite]

**Modelo radial**:
\[
\begin{cases}
\dot x = y - x\,(r - x^2 - y^2)\\
\dot y = -x + y\,(r - x^2 - y^2)
\end{cases}
\]
- \(r<0\): foco estable.  
- \(r=0\): Hopf.  
- \(r>0\): ciclo límite de radio \(r\).

[imagen: tres paneles con \(r<0,=0,>0\); espirales al centro, transición, y anillo ciclo]

### 5) Sistema de Lorenz (mención a regímenes)
\[
\dot x=\sigma(y-x),\quad
\dot y=x(\rho - z)-y,\quad
\dot z=xy - \beta z
\]
- \(\rho=10\): equilibrio estable; converge.  
- \(\rho=24.74\): Hopf; aparecen oscilaciones.  
- \(\rho=28\): régimen caótico; atractor extraño.

[imagen: atractor de Lorenz con forma de mariposa; dos lóbulos; trayectoria que nunca se repite]

---

## Clase 11: Sistemas Dinámicos No Lineales

### 1) Formulación general en el plano
\[
\dot x=f(x,y),\qquad \dot y=g(x,y)
\]
Puntos críticos resolviendo \(f(x,y)=0\) y \(g(x,y)=0\). Linealización con:
\[
J(x,y)=
\begin{pmatrix}
\partial f/\partial x & \partial f/\partial y\\
\partial g/\partial x & \partial g/\partial y
\end{pmatrix}_{(x^*,y^*)}
\]
Si el equilibrio es hiperbólico (partes reales no nulas), vale Hartman–Grobman.

### 2) Ejemplos clásicos
- **Lotka–Volterra** (presas–depredadores):
  \[
  \dot x=\alpha x-\beta xy,\qquad \dot y=\delta xy-\gamma y
  \]
  Equilibrios en \((0,0)\) y \((\gamma/\delta,\;\alpha/\beta)\); órbitas cerradas alrededor del segundo (centro; requiere análisis no lineal).

  [imagen: retrato de fase con ciclos cerrados alrededor del equilibrio positivo; flechas indicando sentido horario]

- **Van der Pol**:
  \[
  \dot x=y,\qquad \dot y=\mu(1-x^2)y - x
  \]
  Para \(\mu>0\) hay ciclo límite estable.

  [imagen: retrato de fase con ciclo límite único; trayectorias internas y externas convergiendo al ciclo]

- **Normal form tipo Hopf**:
  \[
  \begin{cases}
  \dot x = y - x(\mu - x^2 - y^2)\\
  \dot y = -x + y(\mu - x^2 - y^2)
  \end{cases}
  \]
  \(\mu<0\) estable en el origen; \(\mu>0\) aparece ciclo límite.

### 3) Teoremas útiles
- **Existencia y unicidad (Picard–Lindelöf)**: continuidad en \(t\) y condición de Lipschitz en \(x\) garantizan solución local única (las trayectorias no se cruzan).  
- **Hartman–Grobman**: cerca de un equilibrio hiperbólico, la dinámica es topológicamente conjugada a la linealización.  
- **Lyapunov (directo)**: si \(V>0\) y \(\dot V<0\) en vecindad, el equilibrio es asintóticamente estable; si \(\dot V\le 0\), estable; si \(\dot V>0\), inestable.  
- **Poincaré–Bendixson (2D)**: en regiones cerradas y acotadas sin puntos fijos, el \(\omega\)-límite es un punto fijo, un ciclo límite, o una unión finita de órbitas y puntos fijos conectados; descarta caos en 2D continuo.  
- **LaSalle (principio de invariancia)**: generaliza Lyapunov para deducir convergencia al mayor conjunto donde \(\dot V=0\).

### 4) Ejemplos de análisis con Jacobiana
- \(\dot x=xy-2y,\; \dot y=xy-2x\): equilibrios en \((0,0)\) silla y \((2,2)\) nodo fuente.  
- \(\dot x=y,\; \dot y=x^2+y^2-1\): centro en \((-1,0)\) (linealización no concluye); silla en \((1,0)\).  
- \(\dot x=xy,\; \dot y=x^2+y^2-1\): cuatro equilibrios; combinación de nodo estable, nodo inestable y dos sillas.

[imagen: cuatro pequeños retratos de fase, cada uno con el tipo de equilibrio marcado con colores distintos]

---

## Clase 12: Aplicaciones de Sistemas No Lineales

### 1) Romeo y Julieta (Strogatz)
\[
\begin{cases}
\dot R=aR+bJ\\
\dot J=cR+dJ
\end{cases}
\]
**Estilos según signos**:  
- Apasionado (a>0, b>0) (autoexcitación y respuesta positiva al otro).  
- Contradictorio (a>0, b<0).  
- Dependiente (a<0, b>0).  
- Evasivo (a<0, b<0).  
Análogo para \(c,d\) del lado de Julieta.

**Caso 1**: \(\dot R=-J,\; \dot J=R\) (R evasivo; J dependiente). Matriz en el origen:
\(\begin{pmatrix}0&-1\\1&0\end{pmatrix}\).

**Condición de espiral** para lineales \(A=\begin{pmatrix}a&b\\c&d\end{pmatrix}\):  
\(\operatorname{tr}A\ne 0,\; \Delta=ad-bc>0,\; \operatorname{tr}A^2-4\Delta<0\).

**Ciclo límite romántico** (modelo radial):
\[
\dot R=R(1-R^2-J^2),\quad \dot J=-J(1-R^2-J^2)
\]
Círculo de radio 1 separa dinámicas.

[imagen: tres retratos de fase; centro puro, espiral estable, y ciclo límite alrededor del origen]

### 2) Lotka–Volterra (repaso aplicado)
\[
\dot x=ax-bxy,\quad \dot y=cxy-dy
\]
Tabla de parámetros y efectos:
- \(a\): crecimiento natural de presas.  
- \(b\): eficiencia de caza (reduce presas por interacción).  
- \(c\): conversión en nuevos depredadores.  
- \(d\): mortalidad del depredador.

[imagen: gráfico tiempo-serie con oscilaciones desfasadas de presas y depredadores; y retrato de fase con ciclo]

### 3) Problema del cohete (Tsiolkovsky)
\[
m(t)\frac{dv}{dt}=-u\frac{dm}{dt}
\quad\Rightarrow\quad
v(t)=v_0+u\ln\frac{m_0}{m(t)}
\]
Variables: \(m(t)\) masa, \(v(t)\) velocidad, \(u\) velocidad de eyección (constante), \(\dot m<0\).

[imagen: esquema de cohete expulsando masa; flechas mostrando \(u\) y variación de \(m\)]

### 4) Oscilador armónico sin fricción
\[
\ddot x+\omega^2 x=0,\quad \omega=\sqrt{k/m}
\]
[imagen: fase \(x\)-\(\dot x\) como elipses; solución sinusoidal en tiempo]

### 5) Péndulo simple (formulación en 2D)
\[
\dot\theta=v,\quad \dot v=\sin\theta
\]
Jacobianos en \((0,0)\) y \((\pm\pi,0)\).

[imagen: retrato de fase con órbitas cerradas alrededor de \((0,0)\) y separatrices pasando por \((\pm\pi,0)\)]

### 6) Sistema conservativo de doble pozo
\[
\ddot x=-(dV/dx),\quad V(x)=-\tfrac12 x^2+\tfrac14 x^4
\;\Rightarrow\; \ddot x=x-x^3
\]
Forma de sistema:
\[
\dot x=y,\quad \dot y=x-x^3
\]
**Hamiltoniano**:
\[
H(x,y)=\tfrac12 y^2+\tfrac12 x^2+\tfrac14 x^4,\quad \dot H=0
\]

[imagen: curvas de nivel \(H=c\) en el plano \(x\)-\(y\); lóbulos alrededor de los pozos; separatriz en el origen]

---

## Clase 13: Parametrización de Sistemas Dinámicos

### 1) Idea general
Para sistemas autónomos:
\[
\frac{d\mathbf{x}}{dt}=\mathbf{F}(\mathbf{x}),\;\; \mathbf{x}=(x,y)^\top
\]
Buscar \(x(t),y(t)\) que parametrizan las trayectorias en el plano \((x,y)\); o eliminar \(t\) para obtener \(y=f(x)\).

**Para qué sirve**: entender el movimiento, graficar trayectorias, estudiar energía y oscilaciones, clasificar órbitas.

### 2) Métodos
1. **Solución explícita en \(t\)** (ideal si es lineal o desacoplado).  
2. **Eliminación de \(t\)** con \(\dfrac{dy}{dx}=\dfrac{\dot y}{\dot x}=\dfrac{g(x,y)}{f(x,y)}\) (curvas de dirección).  
3. **Curvas de nivel** \(H(x,y)=c\) en sistemas conservativos (energía constante).  
4. **Coordenadas polares** \(x=r\cos\theta,\; y=r\sin\theta\) con
\[
\dot r=\frac{x\dot x+y\dot y}{r},\quad
\dot\theta=\frac{x\dot y - y\dot x}{r^2}
\]
(útil en trayectorias radiales o espirales).

[imagen: tres paneles con ejemplos de: solución parametrizada en tiempo; campo de direcciones y curva \(y(x)\); y curvas de nivel \(H=c\)]

### 3) Caso no autónomo
\[
\dot x=f(x,y,t),\quad \dot y=g(x,y,t)
\]
El tiempo actúa como variable externa. Estrategia: resolver para \(x(t),y(t)\); o visualizar en espacio extendido \((x,y,t)\).

**Ejemplo**:  
\(\dot x=x+t\). Reescritura \(\dot x - x = t\). Factor integrante \(\mu(t)=e^{-t}\):
\[
\frac{d}{dt}\!\big(xe^{-t}\big)=t e^{-t}
\;\Rightarrow\;
x(t)=e^{t}\!\int t e^{-t}\,dt=-t-1+C_1 e^{t}
\]
\(\dot y=-y+\cos t\). Factor integrante \(\mu(t)=e^{t}\):
\[
\frac{d}{dt}\!\big(ye^{t}\big)=e^{t}\cos t
\;\Rightarrow\;
y(t)=\tfrac12\sin t+\tfrac12\cos t + C_2 e^{-t}
\]

[imagen: dos gráficos tiempo-serie \(x(t)\) y \(y(t)\); curvas exponenciales y senoidales superpuestas]

### 4) Ejemplo tipo Hopf (parámetro \(\mu\))
\[
\begin{cases}
\dot x=\mu x - y - x(x^2+y^2)\\
\dot y=x + \mu y - y(x^2+y^2)
\end{cases}
\quad\Rightarrow\quad
J(0,0)=\begin{pmatrix}\mu & -1\\ 1 & \mu\end{pmatrix}
\]
Autovalores \(\lambda=\mu\pm i\).  
- \(\mu<0\): espirales que decaen.  
- \(\mu=0\): centro puro.  
- \(\mu>0\): espirales que crecen; ciclo límite por no linealidad.

[imagen: retrato de fase con transición de foco estable a ciclo límite al cruzar \(\mu=0\)]

### 5) Soluciones explícitas lineales y eliminación de parámetro
Sistema:
\[
\dot X = A X,\quad
A=\begin{pmatrix}\lambda&-1\\[2pt]1&\lambda\end{pmatrix},\quad
X(t)=e^{\lambda t}\begin{pmatrix}
x_0\cos t - y_0\sin t\\
x_0\sin t + y_0\cos t
\end{pmatrix}
\]
Interpretación de \(\lambda\):  
- \(\lambda<0\) espiral que decae; \(\lambda=0\) órbitas cerradas; \(\lambda>0\) espiral que crece.

**Curvas sin \(t\)**: si \(x(t)=a e^{2t},\; y(t)=b e^{t}\), entonces \(e^{t}=y/b\) y
\[
x(t)=a\Big(\frac{y}{b}\Big)^2
\quad\Rightarrow\quad x=\frac{a}{b^2}y^2 \; \text{(parábolas)}
\]
Otro caso \(X(t)=a e^{t}v_1 + b e^{-t}v_2\) puede dar familias de **hipérbolas**.

[imagen: familia de parábolas en el plano \(x\)-\(y\); otra figura con hipérbolas simétricas respecto a ejes]

### 6) Estructura orbital y conjuntos límite
- **Variedades estable e inestable**; **separatrices**; **ciclos límite**.  
- Conjuntos \(\omega(x_0)\) y \(\alpha(x_0)\):
\[
\omega(x_0)=\{y:\exists t_n\to+\infty \text{ tal que } \phi(t_n,x_0)\to y\},\quad
\alpha(x_0)=\{y:\exists t_n\to-\infty \text{ tal que } \phi(t_n,x_0)\to y\}
\]

**Ejemplo nodo degenerado**  
\(\dot x=-x+y,\; \dot y=-y\) con \(X(t)=e^{-t}\big(c_1(1,0)^\top+c_2(0,1)^\top + t(1,0)^\top\big)\).  
Para \(x_0=y_0=1\): \(x(t)=(t+1)e^{-t}\to 0\), \(y(t)=e^{-t}\to 0\) cuando \(t\to+\infty\); la órbita tiende al origen; hacia atrás crece sin cota.

[imagen: retrato de fase con abanico típico de nodo degenerado; trayectorias entrando tangentes a una dirección preferente]

---

### Notas sobre imágenes
Donde indiqué `[imagen: ...]` podés reemplazar por la figura correspondiente. Si preferís, puedo listar cada placeholder en una checklist para que pegues las imágenes exactas más adelante.

---

**Fuentes consultadas**:  
9. Sistemas Autonomos desacoplados 1d.pdf; 10.Bifurcaciones.pdf; 13.sistemas_dinamicos_no_lineales.pdf; 13.sistemas_dinamicos_no_lineales 1.pdf; 14.sistemas_dinamicos_no_lineales_aplicaciones.pdf; 15.Parametrizacion_sistemas_dinamicos.pdf.
