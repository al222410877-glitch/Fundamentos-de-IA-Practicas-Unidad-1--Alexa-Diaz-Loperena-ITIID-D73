#"""
#==============================================================
#   Galería Interactiva con Menú Desplegable de Paletas
#==============================================================
# Materia: Extracción de Conocimiento en Bases de Datos
#==============================================================
#"""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import seaborn as sns
import numpy as np

# ==========================================================
# CONFIGURACIÓN Y DATOS
# ==========================================================

plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
np.random.seed(42)

x = np.arange(1, 11)
y = np.random.randint(20, 90, 10)

# Lista de paletas a explorar
paletas = [
    "deep", "muted", "bright", "pastel", "dark", "colorblind",
    "Blues", "Greens", "Reds", "Purples",
    "viridis", "plasma", "inferno", "magma", "cividis"
]

# ==========================================================
# CREACIÓN DE LA FIGURA Y DISEÑO TIPO PANEL
# ==========================================================

fig, ax = plt.subplots(figsize=(13, 7))

# Ajustar los espacios para dejar el panel izquierdo libre y separar más la parte superior
plt.subplots_adjust(left=0.32, bottom=0.15, top=0.84, right=0.95)

# Título principal de la interfaz
fig.suptitle(
    "Explorador Interactivo de Paletas Profesionales",
    fontsize=18,
    fontweight="bold",
    color="#2C3E50",
    y=0.93
)

# ==========================================================
# FUNCIÓN PARA DIBUJAR LA GRÁFICA ACTIVA
# ==========================================================

def actualizar_grafica(nombre_paleta):
    ax.clear()
    
    # Generar colores de la paleta seleccionada
    colores = sns.color_palette(nombre_paleta, len(x))
    
    # Dibujar barras con diseño estilizado
    ax.bar(
        x, y,
        color=colores,
        edgecolor="#34495E",
        linewidth=1.2,
        alpha=0.85
    )
    
    # Estética de la gráfica con mayor separación (pad=15)
    ax.set_title(
        f"Paleta Activa: {nombre_paleta.upper()}",
        fontsize=14,
        fontweight="bold",
        color="#2980B9",
        pad=15
    )
    ax.set_xlabel("Categorías del Sistema", fontsize=11, fontweight="bold", color="#34495E", labelpad=8)
    ax.set_ylabel("Valores Métrica", fontsize=11, fontweight="bold", color="#34495E", labelpad=8)
    ax.set_xticks(x)
    ax.grid(linestyle="--", linewidth=0.6, alpha=0.5, color="#BDC3C7")
    
    # Limpieza de marcos
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#BDC3C7")
    ax.spines["bottom"].set_color("#BDC3C7")
    
    fig.canvas.draw_idle()

# Dibujar la primera paleta por defecto al abrir
actualizar_grafica(paletas[0])

# ==========================================================
# CREACIÓN DEL MENÚ INTERACTIVO LATERAL (RADIO BUTTONS)
# ==========================================================

# Área para el cuadro de selección a la izquierda
ax_menu = plt.axes([0.05, 0.15, 0.22, 0.70], facecolor="#F8F9F9")
ax_menu.set_title("Menú de Paletas", fontsize=11, fontweight="bold", color="#2C3E50", pad=8)

# Crear los botones de radio interactivos
radio = RadioButtons(ax_menu, paletas, active=0, activecolor="#2980B9")

# Estilizar el texto del menú lateral
for label in radio.labels:
    label.set_fontsize(10)
    label.set_color("#34495E")
    label.set_fontweight("semibold")

# Conectar el evento de selección del menú con la función de actualización
def al_seleccionar(label):
    actualizar_grafica(label)

radio.on_clicked(al_seleccionar)

# ==========================================================
# PIE DE FIGURA Y EJECUCIÓN
# ==========================================================

fig.text(
    0.32, 0.02,
    "Selecciona una paleta en el panel izquierdo para visualizarla en tiempo real | UTVT",
    fontsize=10,
    color="#7F8C8D",
    fontweight="semibold"
)

plt.show()

print("="*60)
print("Interfaz interactiva ajustada con mejor separación visual.")
print("="*60)