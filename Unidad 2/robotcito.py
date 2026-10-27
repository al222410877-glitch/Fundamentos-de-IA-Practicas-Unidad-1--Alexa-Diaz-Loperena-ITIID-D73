import itertools
import math
import tkinter as tk
from tkinter import ttk

# Coordenadas exactas definidas
PUNTOS = {
    "Origen (0,0)": (0, 0),
    "Entrega A": (2, 1),
    "Entrega B": (4, 4),
    "Entrega C": (5, 2),
    "Entrega D": (6, 6),
    "Entrega E": (8, 1),
}

# Secuencia base por defecto (modificable según selección)
SECUENCIA_RECORRIDO = [
    "Origen (0,0)",
    "Entrega A",
    "Entrega B",
    "Entrega C",
    "Entrega D",
    "Entrega E",
    "Origen (0,0)",
]

# Paleta de colores del arcoíris incluyendo el ROSA para los 6 tramos del trayecto
COLORES_ARCOIRIS = [
    "#FF0000",  # 1. Origen -> A: Rojo
    "#FF7F00",  # 2. A -> B: Naranja
    "#FF69B4",  # 3. B -> C: Rosa
    "#008000",  # 4. C -> D: Verde
    "#0000FF",  # 5. D -> E: Azul
    "#8B00FF",  # 6. E -> Origen: Violeta
]


class SimuladorRobotOrtogonal:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "Simulador de Robot"
    )
    self.root.geometry("1400x720")
    self.root.config(bg="#FAFAFA")

    self.crear_todas_las_permutaciones()
    self.crear_interfaz()
    self.animacion_en_curso = False

  def crear_todas_las_permutaciones(self):
    """Calcula matemáticamente las 120 combinaciones y sus distancias."""
    entregas = ["Entrega A", "Entrega B", "Entrega C", "Entrega D", "Entrega E"]
    self.lista_permutaciones = []

    for perm in itertools.permutations(entregas):
      ruta_completa = ["Origen (0,0)"] + list(perm) + ["Origen (0,0)"]
      distancia_total = 0
      for i in range(len(ruta_completa) - 1):
        p1 = PUNTOS[ruta_completa[i]]
        p2 = PUNTOS[ruta_completa[i + 1]]
        # Distancia ortogonal (Manhattan)
        distancia_total += abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

      self.lista_permutaciones.append(
          {"ruta": ruta_completa, "distancia": distancia_total}
      )

  def crear_interfaz(self):
    titulo = tk.Label(
        self.root,
        text="🤖 Robot de Entregas",
        font=("Arial", 14, "bold"),
        fg="#333333",
        bg="#FAFAFA",
    )
    titulo.pack(pady=5)

    main_frame = tk.Frame(self.root, bg="#FAFAFA")
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # --- SECCIÓN 1: PANEL IZQUIERDO (TABLA DE LAS 120 POSIBILIDADES) ---
    left_panel = tk.LabelFrame(
        main_frame,
        text=" Las 120 Combinaciones Posibles (5! Permutaciones) ",
        font=("Arial", 10, "bold"),
        fg="#0277BD",
        bg="#FFFFFF",
        relief="groove",
        bd=2,
    )
    left_panel.pack(side="left", fill="both", expand=False, padx=5, ipadx=5)

    table_frame = tk.Frame(left_panel, bg="#FFFFFF")
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)

    self.tree = ttk.Treeview(
        table_frame, columns=("id", "secuencia", "dist"), show="headings", height=25
    )
    self.tree.heading("id", text="#")
    self.tree.heading("secuencia", text="Secuencia de Recorrido")
    self.tree.heading("dist", text="Distancia")

    self.tree.column("id", width=35, anchor="center")
    self.tree.column("secuencia", width=280, anchor="w")
    self.tree.column("dist", width=60, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame, orient="vertical", command=self.tree.yview
    )
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for idx, item in enumerate(self.lista_permutaciones, 1):
      res_str = " ➔ ".join(
          [p.replace("Entrega ", "") for p in item["ruta"]]
      )
      self.tree.insert(
          "",
          "end",
          values=(str(idx), res_str, f"{item['distancia']} u"),
          iid=str(idx - 1),
      )

    self.tree.bind("<<TreeviewSelect>>", self.seleccionar_ruta_tabla)

    # --- SECCIÓN 2: PANEL CENTRAL (PLANO CARTESIANO) ---
    center_panel = tk.LabelFrame(
        main_frame,
        text=" Plano Cartesiano (Movimiento Ortogonal) ",
        font=("Arial", 10, "bold"),
        fg="#0277BD",
        bg="#FFFFFF",
        relief="groove",
        bd=2,
    )
    center_panel.pack(side="left", fill="both", expand=True, padx=5)

    self.canvas_width = 480
    self.canvas_height = 430
    self.canvas = tk.Canvas(
        center_panel,
        width=self.canvas_width,
        height=self.canvas_height,
        bg="#FFFFFF",
        highlightthickness=1,
        highlightbackground="#B0BEC5",
    )
    self.canvas.pack(padx=10, pady=10, fill="both", expand=True)

    btn_frame = tk.Frame(center_panel, bg="#FFFFFF")
    btn_frame.pack(pady=5)

    self.btn_iniciar = tk.Button(
        btn_frame,
        text="▶ Simular Ruta Seleccionada",
        font=("Arial", 9, "bold"),
        bg="#00897B",
        fg="white",
        padx=8,
        pady=4,
        command=self.iniciar_recorrido,
    )
    self.btn_iniciar.pack(side="left", padx=5)

    btn_reiniciar = tk.Button(
        btn_frame,
        text="🔄 Reiniciar",
        font=("Arial", 9, "bold"),
        bg="#E53935",
        fg="white",
        padx=8,
        pady=4,
        command=self.reiniciar_simulacion,
    )
    btn_reiniciar.pack(side="left", padx=5)

    # --- SECCIÓN 3: PANEL DERECHO (PANTALLITA DE BITÁCORA COLORIDA) ---
    right_panel = tk.LabelFrame(
        main_frame,
        text=" Pantallita de Bitácora Colorida ",
        font=("Arial", 10, "bold"),
        fg="#0277BD",
        bg="#FFFFFF",
        relief="groove",
        bd=2,
    )
    right_panel.pack(side="right", fill="both", expand=False, padx=5, ipadx=5)

    self.txt_pantallita = tk.Text(
        right_panel,
        width=38,
        height=24,
        font=("Consolas", 9),
        bg="#F4F6F7",
        fg="#2C3E50",
        relief="flat",
    )
    self.txt_pantallita.pack(padx=10, pady=10, fill="both", expand=True)

    self.txt_pantallita.tag_config(
        "Rojo", foreground="#D32F2F", font=("Consolas", 9, "bold")
    )
    self.txt_pantallita.tag_config(
        "Naranja", foreground="#E65100", font=("Consolas", 9, "bold")
    )
    self.txt_pantallita.tag_config(
        "Rosa", foreground="#E91E63", font=("Consolas", 9, "bold")
    )
    self.txt_pantallita.tag_config(
        "Verde", foreground="#2E7D32", font=("Consolas", 9, "bold")
    )
    self.txt_pantallita.tag_config(
        "Azul", foreground="#1565C0", font=("Consolas", 9, "bold")
    )
    self.txt_pantallita.tag_config(
        "Violeta", foreground="#6A1B9A", font=("Consolas", 9, "bold")
    )
    self.txt_pantallita.tag_config("Info", foreground="#37474F")

    self.log_pantallita("=== SISTEMA DE NAVEGACIÓN ACTIVO ===\n", "Info")
    self.log_pantallita(" Selecciona una ruta de la tabla izq.\n", "Info")
    self.log_pantallita("-----------------------------------\n", "Info")

    self.dibujar_plano_cartesiano()

  def seleccionar_ruta_tabla(self, event):
    if self.animacion_en_curso:
      return
    selected_items = self.tree.selection()
    if selected_items:
      idx = int(selected_items[0])
      global SECUENCIA_RECORRIDO
      SECUENCIA_RECORRIDO = self.lista_permutaciones[idx]["ruta"]
      self.dibujar_plano_cartesiano()
      self.log_pantallita(
          f"\n[SELECCIONADA] Opción #{idx + 1}\nDistancia: {self.lista_permutaciones[idx]['distancia']}u\n",
          "Info",
      )

  def transformar_coordenadas(self, x, y):
    pad_x = 45
    pad_y = 40
    escala_x = (self.canvas_width - 2 * pad_x) / 9.0
    escala_y = (self.canvas_height - 2 * pad_y) / 7.0

    px = pad_x + x * escala_x
    py = self.canvas_height - (pad_y + y * escala_y)
    return px, py

  def dibujar_plano_cartesiano(self):
    self.canvas.delete("all")
    ox, oy = self.transformar_coordenadas(0, 0)

    for x_val in range(10):
      cx, _ = self.transformar_coordenadas(x_val, 0)
      self.canvas.create_line(
          cx, 15, cx, self.canvas_height - 15, fill="#ECEFF1", width=1
      )
      if x_val % 2 == 0:
        self.canvas.create_text(
            cx, oy + 12, text=str(x_val), font=("Arial", 7), fill="#78909C"
        )

    for y_val in range(8):
      _, cy = self.transformar_coordenadas(0, y_val)
      self.canvas.create_line(
          15, cy, self.canvas_width - 15, cy, fill="#ECEFF1", width=1
      )
      if y_val % 2 == 0:
        self.canvas.create_text(
            ox - 12, cy, text=str(y_val), font=("Arial", 7), fill="#78909C"
        )

    self.canvas.create_line(
        20, oy, self.canvas_width - 20, oy, fill="#455A64", width=2
    )
    self.canvas.create_line(
        ox, self.canvas_height - 20, ox, 20, fill="#455A64", width=2
    )

    for nombre, (x, y) in PUNTOS.items():
      px, py = self.transformar_coordenadas(x, y)
      is_origen = "Origen" in nombre
      radio = 8 if is_origen else 6
      color_punto = "#2E7D32" if is_origen else "#3F51B5"

      self.canvas.create_oval(
          px - radio,
          py - radio,
          px + radio,
          py + radio,
          fill=color_punto,
          outline="white",
          width=2,
      )
      self.canvas.create_text(
          px,
          py - 13,
          text=f"{nombre.split()[0]}\n({x},{y})",
          font=("Arial", 7, "bold"),
          fill="#263238",
      )

    orig_x, orig_y = PUNTOS["Origen (0,0)"]
    rpx, rpy = self.transformar_coordenadas(orig_x, orig_y)
    self.robot_id = self.canvas.create_oval(
        rpx - 9,
        rpy - 9,
        rpx + 9,
        rpy + 9,
        fill="#FF7043",
        outline="white",
        width=2,
    )
    self.robot_txt = self.canvas.create_text(
        rpx, rpy, text="🤖", font=("Arial", 8), fill="white"
    )

  def log_pantallita(self, mensaje, tag="Info"):
    self.txt_pantallita.insert(tk.END, mensaje, tag)
    self.txt_pantallita.see(tk.END)

  def iniciar_recorrido(self):
    if self.animacion_en_curso:
      return
    self.animacion_en_curso = True
    self.btn_iniciar.config(state="disabled")
    self.log_pantallita("\n[INICIO] Desplegando ruta seleccionada...\n", "Info")

    self.root.after(300, lambda: self.animar_tramo(0, 0.0))

  def animar_tramo(self, indice_tramo, tiempo_total_acumulado):
    if indice_tramo >= len(SECUENCIA_RECORRIDO) - 1:
      self.log_pantallita(
          "\n[FINALIZADO] ¡Robot de vuelta en la base (0,0)!\n", "Info"
      )
      self.log_pantallita(
          f"⏱ Tiempo Total: {tiempo_total_acumulado:.2f}s\n", "Info"
      )
      self.animacion_en_curso = False
      self.btn_iniciar.config(state="normal")
      return

    p_actual = SECUENCIA_RECORRIDO[indice_tramo]
    p_siguiente = SECUENCIA_RECORRIDO[indice_tramo + 1]

    x1, y1 = PUNTOS[p_actual]
    x2, y2 = PUNTOS[p_siguiente]

    ix, iy = x2, y1
    dist_h = abs(ix - x1)
    dist_v = abs(y2 - iy)
    distancia_total = dist_h + dist_v

    velocidad = 4.0
    tiempo_estimado = (
        distancia_total / velocidad if velocidad > 0 else 1
    )

    color_tramo = COLORES_ARCOIRIS[indice_tramo % len(COLORES_ARCOIRIS)]
    tags_nombres = ["Rojo", "Naranja", "Rosa", "Verde", "Azul", "Violeta"]
    tag_actual = tags_nombres[indice_tramo % len(tags_nombres)]

    nombre_corto_1 = p_actual.split()[0]
    nombre_corto_2 = p_siguiente.split()[0]
    self.log_pantallita(
        f"➔ {nombre_corto_1} ➔ {nombre_corto_2}\n", tag_actual
    )

    self.mover_robot_horizontal(
        x1,
        y1,
        ix,
        iy,
        0,
        12,
        tiempo_estimado * (dist_h / max(1, distancia_total)),
        indice_tramo,
        tiempo_total_acumulado,
        p_siguiente,
        color_tramo,
        tag_actual,
    )

  def mover_robot_horizontal(
      self,
      x1,
      y1,
      x2,
      y2,
      paso,
      total_pasos,
      tiempo_h,
      idx,
      tiempo_acum,
      destino,
      color_linea,
      tag_color,
  ):
    if x1 == x2:
      self.mover_robot_vertical(
          x1,
          y1,
          x2,
          PUNTOS[destino][1],
          0,
          12,
          tiempo_h,
          idx,
          tiempo_acum,
          destino,
          color_linea,
          tag_color,
      )
      return

    if paso <= total_pasos:
      t = paso / total_pasos
      curr_x = x1 + (x2 - x1) * t
      curr_y = y1

      px, py = self.transformar_coordenadas(curr_x, curr_y)
      self.canvas.coords(self.robot_id, px - 9, py - 9, px + 9, py + 9)
      self.canvas.coords(self.robot_txt, px, py)

      delay = int((tiempo_h * 1000) / total_pasos) if total_pasos > 0 else 10
      self.root.after(
          max(10, delay),
          lambda: self.mover_robot_horizontal(
              x1,
              y1,
              x2,
              y2,
              paso + 1,
              total_pasos,
              tiempo_h,
              idx,
              tiempo_acum,
              destino,
              color_linea,
              tag_color,
          ),
      )
    else:
      ox, oy = PUNTOS[SECUENCIA_RECORRIDO[idx]]
      cpx1, cpy1 = self.transformar_coordenadas(ox, oy)
      cpx2, cpy2 = self.transformar_coordenadas(x2, y1)
      self.canvas.create_line(
          cpx1, cpy1, cpx2, cpy2, fill=color_linea, width=3.5
      )

      dest_final_y = PUNTOS[destino][1]
      dist_v = abs(dest_final_y - y1)
      tiempo_v = max(
          0.1,
          (
              abs(PUNTOS[destino][0] - ox) + dist_v
          )
          / 4.0
          * (dist_v / max(1, abs(PUNTOS[destino][0] - ox) + dist_v)),
      )

      self.mover_robot_vertical(
          x2,
          y1,
          x2,
          dest_final_y,
          0,
          12,
          tiempo_v,
          idx,
          tiempo_acum,
          destino,
          color_linea,
          tag_color,
      )

  def mover_robot_vertical(
      self,
      x1,
      y1,
      x2,
      y2,
      paso,
      total_pasos,
      tiempo_v,
      idx,
      tiempo_acum,
      destino,
      color_linea,
      tag_color,
  ):
    if y1 == y2:
      self.finalizar_tramo(idx, tiempo_acum, tiempo_v, destino, tag_color)
      return

    if paso <= total_pasos:
      t = paso / total_pasos
      curr_x = x1
      curr_y = y1 + (y2 - y1) * t

      px, py = self.transformar_coordenadas(curr_x, curr_y)
      self.canvas.coords(self.robot_id, px - 9, py - 9, px + 9, py + 9)
      self.canvas.coords(self.robot_txt, px, py)

      delay = int((tiempo_v * 1000) / total_pasos) if total_pasos > 0 else 10
      self.root.after(
          max(10, delay),
          lambda: self.mover_robot_vertical(
              x1,
              y1,
              x2,
              y2,
              paso + 1,
              total_pasos,
              tiempo_v,
              idx,
              tiempo_acum,
              destino,
              color_linea,
              tag_color,
          ),
      )
    else:
      cpx1, cpy1 = self.transformar_coordenadas(x1, y1)
      cpx2, cpy2 = self.transformar_coordenadas(x2, y2)
      self.canvas.create_line(
          cpx1, cpy1, cpx2, cpy2, fill=color_linea, width=3.5
      )

      tiempo_total_tramo = tiempo_v * 2
      self.finalizar_tramo(
          idx, tiempo_acum, tiempo_total_tramo, destino, tag_color
      )

  def finalizar_tramo(self, idx, tiempo_acum, tiempo_tramo, destino, tag_color):
    tiempo_nuevo = tiempo_acum + tiempo_tramo
    self.log_pantallita(f" ✔ Llegó a {destino.split()[0]}\n", tag_color)
    self.root.after(200, lambda: self.animar_tramo(idx + 1, tiempo_nuevo))

  def reiniciar_simulacion(self):
    self.animacion_en_curso = False
    self.btn_iniciar.config(state="normal")
    self.dibujar_plano_cartesiano()
    self.txt_pantallita.delete("1.0", tk.END)
    self.log_pantallita("=== SISTEMA DE NAVEGACIÓN ACTIVO ===\n", "Info")
    self.log_pantallita(" Estado: Simulación reiniciada.\n", "Info")
    self.log_pantallita("-----------------------------------\n", "Info")


if __name__ == "__main__":
  root = tk.Tk()
  app = SimuladorRobotOrtogonal(root)
  root.mainloop()