#"""
#==============================================================
#   Primer Gráfico con Matplotlib (Versión Mejorada - Ejemplo Base)
#==============================================================
# Materia: Extracción de Conocimiento en Bases de Datos
#==============================================================
#"""

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import matplotlib.pyplot as plt
import numpy as np

# ==========================================================
# DATOS (Ejemplo original del profesor)
# ==========================================================

meses = [
    "Ene", "Feb", "Mar", "Abr",
    "May", "Jun", "Jul", "Ago",
    "Sep", "Oct", "Nov", "Dic"
]

ventas = [85, 90, 96, 105, 120, 135,
          150, 148, 160, 172, 181, 195]

# ==========================================================
# CONFIGURACIÓN GENERAL DE LA FIGURA 
# ==========================================================

fig, ax = plt.subplots(figsize=(14, 8))

# ==========================================================
# TÍTULOS Y SUBTÍTULOS (Título principal arriba, subtítulo abajo)
# ==========================================================

ax.set_title(
    "Ventas Mensuales de la Empresa EcoMart",
    fontsize=20,
    fontweight="bold",
    pad=25,
    color="#4A4A4A"
)

ax.text(
    0.5, 1.03, 
    "Periodo Enero - Diciembre 2026", 
    transform=ax.transAxes,
    fontsize=12,
    color="#7F8C8D",
    ha="center",
    fontweight="semibold"
)

# ==========================================================
# GRÁFICA PRINCIPAL (Línea en Lila Pastel)
# ==========================================================

linea, = ax.plot(
    meses,
    ventas,
    color="#B19CD9",          # Lila pastel elegante
    linewidth=3.5,
    marker="o",
    markersize=9,
    markerfacecolor="white",
    markeredgewidth=2.5,
    markeredgecolor="#B19CD9",
    label="Ventas mensuales",
    picker=5                  
)

# ==========================================================
# ETIQUETAS EN LOS EJES
# ==========================================================

ax.set_xlabel(
    "Mes",
    fontsize=14,
    fontweight="bold",
    color="#34495E"
)

ax.set_ylabel(
    "Ventas (Miles de pesos)",
    fontsize=14,
    fontweight="bold",
    color="#34495E"
)

# ==========================================================
# CUADRÍCULA
# ==========================================================

ax.grid(
    linestyle="--",
    linewidth=0.7,
    alpha=0.5,
    color="#BDC3C7"
)

# ==========================================================
# LEYENDA 
# ==========================================================

ax.legend(
    fontsize=11,
    loc="upper left",
    frameon=True,
    facecolor="#F9F9F9",
    edgecolor="#BDC3C7"
)

# ==========================================================
# ANOTACIONES ESTÁTICAS (Valores exactos en cada punto)
# ==========================================================

for x, y in zip(meses, ventas):
    ax.text(
        x,
        y + 3,
        str(y),
        fontsize=10,
        ha="center",
        color="#2C3E50",
        fontweight="semibold"
    )

# ==========================================================
# LÍNEA DE PROMEDIO (Rosa Pastel)
# ==========================================================

promedio = np.mean(ventas)

ax.axhline(
    promedio,
    color="#FFB6C1",          # Rosa pastel suave
    linestyle="--",
    linewidth=2.5,
    label="Promedio"
)

ax.text(
    10.1,
    promedio + 3,
    f"Promedio = {promedio:.1f}",
    color="#D87093",          
    fontsize=11,
    fontweight="bold"
)

# ==========================================================
# DESTACAR EL MÁXIMO (Verde Menta Pastel)
# ==========================================================

indice_max = np.argmax(ventas)

ax.scatter(
    meses[indice_max],
    ventas[indice_max],
    color="#98FB98",          # Verde menta pastel
    s=200,
    zorder=5,
    edgecolors="#2E8B57",     
    linewidths=1.5,
    label="Máximo"
)

ax.annotate(
    "Mayor venta del año",
    xy=(meses[indice_max], ventas[indice_max]),
    xytext=(7.5, 185),
    arrowprops=dict(
        arrowstyle="->",
        color="#2E8B57",
        lw=2
    ),
    fontsize=11,
    fontweight="bold",
    color="#2E8B57"
)

# ==========================================================
# CONFIGURACIÓN DE INTERACTIVIDAD (Posicionamiento Inteligente)
# ==========================================================

anotacion_clic = ax.annotate(
    "", xy=(0, 0), xytext=(15, 15),
    textcoords="offset points",
    bbox=dict(boxstyle="round,pad=0.5", fc="#FFF0F5", ec="#B19CD9", lw=1.5),
    arrowprops=dict(arrowstyle="->", color="#B19CD9", lw=1.5),
    fontsize=11,
    fontweight="bold",
    color="#4A4A4A"
)
anotacion_clic.set_visible(False)

def al_hacer_clic(event):
    if isinstance(event.artist, plt.Line2D):
        ind = event.ind[0]
        x_val = meses[ind]
        y_val = ventas[ind]
        
        # Si está en la segunda mitad (derecha), mueve la etiqueta a la izquierda para que no se corte
        if ind >= len(meses) / 2:
            anotacion_clic.set_position((-80, 15))
        else:
            anotacion_clic.set_position((15, 15))
            
        anotacion_clic.xy = (x_val, y_val)
        anotacion_clic.set_text(f"Mes: {x_val}\nVentas: ${y_val}k")
        anotacion_clic.set_visible(True)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('pick_event', al_hacer_clic)

ax.text(
    0.99, 1.03, 
    "Nota: Haz clic en cualquier punto para ver detalles", 
    transform=ax.transAxes,
    fontsize=9,
    color="#B19CD9",
    ha="right",
    fontweight="bold"
)

# ==========================================================
# PIE DE FIGURA
# ==========================================================

fig.text(
    0.01,
    0.01,
    "Conclusión: Estimado de las ventas | Elaboración propia | UTVT",
    fontsize=10,
    color="#7F8C8D"
)

# ==========================================================
# LIMPIEZA DE DISEÑO
# ==========================================================

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#BDC3C7")
ax.spines["bottom"].set_color("#BDC3C7")

# ==========================================================
# AJUSTAR ESPACIOS Y GUARDAR
# ==========================================================

plt.tight_layout()

plt.savefig(
    "Grafica_Profesional_01.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("="*60)
print("Gráfica 1 del profesor mejorada correctamente.")
print("Archivo guardado como: Grafica_Profesional_01.png")
print("="*60)