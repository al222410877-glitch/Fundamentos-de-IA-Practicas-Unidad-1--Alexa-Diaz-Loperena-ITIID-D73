es_dual = input("¿El alumno es Dual? (si/no): ").lower()

if es_dual == "si":
    print("\nEvaluación de Alumno")
    print("Modalidad: Dual")
    print("El alumno aprobó")
else:
    asistencia = float(input("Ingrese asistencia %: "))
    promedio = float(input("Ingrese promedio: "))
    proyecto = input("Entregó proyecto (si/no): ").lower()

    P = asistencia >= 80
    Q = promedio >= 8
    R = proyecto == "si"

    resultado = P and Q and R

    print("\nEvaluación de Alumno")
    print(f"Asistencia: {P}")
    print(f"Promedio: {Q}")
    print(f"Proyecto: {R}")

    if resultado:
        print("El alumno aprobó")
    else:
        print("El alumno reprobó")