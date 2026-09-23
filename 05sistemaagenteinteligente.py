import tkinter as tk
from tkinter import ttk


def generar_diagnostico(nombre, equipo, problema):
    texto = "\n==============================================================\n"
    texto += "       ASISTENTE INTELIGENTE DE SOPORTE TÉCNICO\n"
    texto += "==============================================================\n\n"
    texto += f"Hola, {nombre}!\n"
    texto += "Voy a ayudarte a identificar el problema de tu equipo.\n"
    texto += "Te haré algunas preguntas y te daré soluciones paso a paso.\n\n"
    texto += f"Equipo seleccionado: {equipo}\n"
    texto += f"Problema: {problema}\n\n"

    if equipo == "Celular":
        texto += "DIAGNÓSTICO DE CELULAR\n\n"
        if problema == "No enciende":
            texto += "DIAGNÓSTICO: EL CELULAR NO ENCIENDE\n"
            texto += "Posibles causas:\n"
            texto += "1. Batería completamente descargada.\n"
            texto += "2. Cable de carga dañado.\n"
            texto += "3. Cargador dañado.\n"
            texto += "4. Puerto de carga sucio o dañado.\n"
            texto += "5. Batería desgastada.\n"
            texto += "6. Falla interna.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Conecta el celular a un cargador que sepas que funciona.\n"
            texto += "2. Utiliza otro cable.\n"
            texto += "3. Prueba otro contacto eléctrico.\n"
            texto += "4. Déjalo conectado durante 20 a 30 minutos.\n"
            texto += "5. Intenta encenderlo nuevamente.\n"
        elif problema == "No carga":
            texto += "DIAGNÓSTICO: PROBLEMA DE CARGA\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Prueba otro cable compatible.\n"
            texto += "2. Prueba otro cargador.\n"
            texto += "3. Prueba otro contacto eléctrico.\n"
            texto += "4. Revisa que el puerto no tenga suciedad visible.\n"
            texto += "5. No introduzcas objetos metálicos en el puerto.\n"
        elif problema == "Sin internet":
            texto += "DIAGNÓSTICO: PROBLEMA DE INTERNET\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Activa y desactiva el modo avión.\n"
            texto += "2. Comprueba que el Wi-Fi esté activado.\n"
            texto += "3. Si utilizas datos móviles, comprueba que estén activos.\n"
            texto += "4. Reinicia el celular.\n"
            texto += "5. Si utilizas Wi-Fi, reinicia el router.\n"
        else:
            texto += "DIAGNÓSTICO: PROBLEMA DE PANTALLA\n\n"
            texto += "Posibles causas:\n"
            texto += "- Pantalla dañada.\n"
            texto += "- Golpe o caída.\n"
            texto += "- Daño por humedad.\n"
            texto += "- Conector interno de pantalla.\n"
            texto += "- Falla del sistema de visualización.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Reinicia el celular.\n"
            texto += "2. Comprueba si la pantalla responde al tacto.\n"
            texto += "3. Observa si existen manchas, líneas o zonas negras.\n"
            texto += "4. Si sufrió una caída recientemente, evita presionarla.\n"

    elif equipo == "Computadora":
        texto += "DIAGNÓSTICO DE COMPUTADORA\n\n"
        if problema == "No enciende":
            texto += "DIAGNÓSTICO: LA COMPUTADORA NO ENCIENDE\n"
            texto += "Posibles causas:\n"
            texto += "- Fuente de poder.\n"
            texto += "- Botón de encendido.\n"
            texto += "- Cable de alimentación.\n"
            texto += "- Tarjeta madre.\n"
            texto += "- Algún componente interno.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Desconecta la computadora.\n"
            texto += "2. Espera aproximadamente un minuto.\n"
            texto += "3. Conecta nuevamente el equipo.\n"
            texto += "4. Verifica que el cable esté firmemente conectado.\n"
            texto += "5. Intenta encenderla.\n"
        elif problema == "Sin imagen":
            texto += "DIAGNÓSTICO: NO HAY IMAGEN\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Comprueba que el monitor esté encendido.\n"
            texto += "2. Desconecta y conecta nuevamente el cable HDMI, VGA o DisplayPort.\n"
            texto += "3. Selecciona la entrada correcta en el monitor.\n"
            texto += "4. Si es posible, prueba otro cable.\n"
            texto += "5. Si tienes otro monitor, prueba la computadora con él.\n"
        elif problema == "Sin internet":
            texto += "DIAGNÓSTICO: SIN INTERNET\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Comprueba que el Wi-Fi esté activado.\n"
            texto += "2. Si utilizas cable de red, vuelve a conectarlo.\n"
            texto += "3. Reinicia la computadora.\n"
            texto += "4. Reinicia el router.\n"
            texto += "5. Espera unos minutos y vuelve a probar.\n"
        else:
            texto += "DIAGNÓSTICO: REVISIÓN GENERAL\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Revisa el cable y la toma eléctrica.\n"
            texto += "2. Verifica la alimentación del equipo.\n"
            texto += "3. Consulta soporte técnico si persiste.\n"

    elif equipo == "Laptop":
        texto += "DIAGNÓSTICO DE LAPTOP\n\n"
        if problema == "No enciende":
            texto += "DIAGNÓSTICO:\n"
            texto += "La laptop no está encendiendo.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Revisa el cable del cargador.\n"
            texto += "2. Prueba otro contacto.\n"
            texto += "3. Comprueba que el adaptador esté conectado.\n"
            texto += "4. Si es posible, prueba un cargador compatible.\n"
        elif problema == "Batería no carga":
            texto += "DIAGNÓSTICO:\n"
            texto += "La laptop funciona pero presenta problemas de carga.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Prueba otro contacto.\n"
            texto += "2. Revisa el cargador.\n"
            texto += "3. Comprueba el puerto de carga.\n"
            texto += "4. Si es posible, utiliza otro cargador compatible.\n"
        else:
            texto += "DIAGNÓSTICO:\n"
            texto += "La laptop enciende pero no muestra imagen.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Reinicia la laptop.\n"
            texto += "2. Comprueba el brillo.\n"
            texto += "3. Si tienes un monitor externo, prueba conectarlo.\n"

    elif equipo == "Televisión":
        texto += "DIAGNÓSTICO DE TELEVISIÓN\n\n"
        if problema == "No enciende":
            texto += "DIAGNÓSTICO:\n"
            texto += "La televisión recibe electricidad pero no enciende.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Cambia las baterías del control.\n"
            texto += "2. Intenta encenderla usando el botón físico.\n"
            texto += "3. Desconecta la televisión.\n"
            texto += "4. Espera aproximadamente un minuto.\n"
            texto += "5. Conéctala nuevamente.\n"
        elif problema == "Sin imagen":
            texto += "DIAGNÓSTICO:\n"
            texto += "La televisión enciende pero no muestra imagen.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Comprueba la entrada HDMI seleccionada.\n"
            texto += "2. Desconecta y conecta nuevamente el HDMI.\n"
            texto += "3. Prueba otro puerto HDMI.\n"
            texto += "4. Prueba otro cable HDMI.\n"
        else:
            texto += "DIAGNÓSTICO:\n"
            texto += "La televisión muestra imagen pero no tiene sonido.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Sube el volumen.\n"
            texto += "2. Comprueba que MUTE esté desactivado.\n"
            texto += "3. Revisa la configuración de salida de audio.\n"

    elif equipo == "Impresora":
        texto += "DIAGNÓSTICO DE IMPRESORA\n\n"
        if problema == "No enciende":
            texto += "DIAGNÓSTICO:\n"
            texto += "La impresora no enciende.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Revisa el cable de alimentación.\n"
            texto += "2. Prueba otro contacto.\n"
            texto += "3. Comprueba el botón de encendido.\n"
            texto += "4. Desconecta y vuelve a conectar la impresora.\n"
        elif problema == "No imprime":
            texto += "DIAGNÓSTICO:\n"
            texto += "La impresora enciende pero no imprime correctamente.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Comprueba que tenga papel.\n"
            texto += "2. Revisa la tinta o tóner.\n"
            texto += "3. Comprueba si existe un atasco.\n"
            texto += "4. Revisa el cable USB o conexión Wi-Fi.\n"
            texto += "5. Cancela trabajos pendientes de impresión.\n"
            texto += "6. Reinicia la impresora.\n"
        else:
            texto += "DIAGNÓSTICO:\n"
            texto += "La impresora está presentando un problema general.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Revisa la conexión USB o Wi-Fi.\n"
            texto += "2. Verifica tinta o tóner.\n"
            texto += "3. Reinicia el equipo.\n"

    elif equipo == "Router / Internet":
        texto += "DIAGNÓSTICO DE INTERNET\n\n"
        if problema == "Sin internet":
            texto += "DIAGNÓSTICO:\n"
            texto += "El router enciende pero no hay conexión a Internet.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Reinicia el router.\n"
            texto += "2. Espera de 3 a 5 minutos.\n"
            texto += "3. Revisa los cables.\n"
            texto += "4. Comprueba las luces del router.\n"
            texto += "5. Prueba otro dispositivo.\n"
        else:
            texto += "DIAGNÓSTICO:\n"
            texto += "El router no está funcionando correctamente.\n\n"
            texto += "SOLUCIÓN:\n"
            texto += "1. Revisa el adaptador de corriente.\n"
            texto += "2. Prueba otro contacto.\n"
            texto += "3. Comprueba que el cable esté conectado.\n"

    else:
        texto += "DIAGNÓSTICO GENERAL\n"
        texto += "El dispositivo no se reconoce en la categoría.\n\n"
        texto += "SOLUCIÓN:\n"
        texto += "1. Revisa el cable de alimentación.\n"
        texto += "2. Prueba otro contacto.\n"
        texto += "3. Consulta el manual del fabricante.\n"

    texto += "\n==============================================================\n"
    texto += "Gracias por utilizar el asistente, " + nombre + "!\n"
    texto += "Espero haberte ayudado a solucionar tu problema.\n"
    texto += "==============================================================\n"
    return texto


def diagnosticar():
    nombre = nombre_var.get().strip()
    equipo = equipo_var.get()
    problema = problema_var.get()

    if not nombre:
        salida.delete("1.0", tk.END)
        salida.insert(tk.END, "Escribe tu nombre antes de continuar.")
        return

    texto = generar_diagnostico(nombre, equipo, problema)
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, texto)


root = tk.Tk()
root.title("Asistente técnico")
root.geometry("860x560")
root.configure(bg="#dfeeff")
root.resizable(False, False)
root.option_add("*Font", "Arial 10")

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground="#ffffff", background="#1f6feb", foreground="#123a5b", borderwidth=1)
style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")])
style.configure("TButton", background="#1f6feb", foreground="white", font=("Arial", 11, "bold"), padding=(12, 8))
style.map("TButton", background=[("active", "#184fa5")], foreground=[("active", "white")])

frame = tk.Frame(root, bg="#dfeeff", padx=28, pady=22)
frame.pack(fill="both", expand=True)

header = tk.Label(
    frame,
    text="ASISTENTE DE DIAGNÓSTICO",
    font=("Arial", 22, "bold"),
    fg="#123a5b",
    bg="#dfeeff",
    pady=6,
)
header.pack(pady=(0, 18))

panel = tk.LabelFrame(
    frame,
    text="Datos del problema",
    padx=14,
    pady=14,
    bg="#ffffff",
    fg="#1b4d72",
    font=("Arial", 10, "bold"),
    highlightbackground="#b7d7ff",
    highlightthickness=2,
)
panel.pack(fill="x", pady=(0, 12))

lbl_nombre = tk.Label(panel, text="Nombre:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#1b4d72")
lbl_nombre.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=8)

nombre_var = tk.StringVar(value="Cliente")
entry_nombre = tk.Entry(panel, textvariable=nombre_var, width=28, font=("Arial", 10), bd=2, bg="#f8fbff", fg="#123a5b", highlightbackground="#b7d7ff", highlightcolor="#1f6feb")
entry_nombre.grid(row=0, column=1, sticky="w", pady=8)

lbl_equipo = tk.Label(panel, text="Equipo:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#1b4d72")
lbl_equipo.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)

equipo_var = tk.StringVar(value="Celular")
combo_equipo = ttk.Combobox(
    panel,
    textvariable=equipo_var,
    values=["Celular", "Computadora", "Laptop", "Televisión", "Impresora", "Router / Internet", "Otro dispositivo"],
    state="readonly",
    width=28,
    font=("Arial", 10),
)
combo_equipo.grid(row=1, column=1, sticky="w", pady=8)

lbl_problema = tk.Label(panel, text="Problema:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#1b4d72")
lbl_problema.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)

problema_var = tk.StringVar(value="No enciende")
combo_problema = ttk.Combobox(
    panel,
    textvariable=problema_var,
    values=["No enciende", "No carga", "Sin imagen", "Sin internet", "No imprime", "Batería no carga", "Otro problema"],
    state="readonly",
    width=28,
    font=("Arial", 10),
)
combo_problema.grid(row=2, column=1, sticky="w", pady=8)

btn = tk.Button(
    frame,
    text="Diagnosticar",
    command=diagnosticar,
    width=20,
    height=2,
    bg="#1f6feb",
    fg="white",
    font=("Arial", 11, "bold"),
    activebackground="#184fa5",
    activeforeground="white",
    relief="flat",
    bd=0,
    highlightthickness=0,
)
btn.pack(pady=(6, 12))

resultado = tk.LabelFrame(
    frame,
    text="Resultado",
    padx=12,
    pady=12,
    bg="#ffffff",
    fg="#1b4d72",
    font=("Arial", 10, "bold"),
    highlightbackground="#b7d7ff",
    highlightthickness=2,
)
resultado.pack(fill="both", expand=True)

salida = tk.Text(
    resultado,
    height=15,
    width=94,
    font=("Consolas", 10),
    bg="#f8fbff",
    fg="#14324a",
    wrap="word",
    relief="solid",
    bd=1,
    highlightbackground="#b7d7ff",
    highlightthickness=1,
)
salida.pack(fill="both", expand=True)

salida.insert(tk.END, "Selecciona un equipo y problema para ver el diagnóstico.\n")

root.mainloop()
