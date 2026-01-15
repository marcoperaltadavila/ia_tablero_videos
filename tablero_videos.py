from flask import Flask, render_template_string
import pandas as pd
from sklearn.linear_model import LinearRegression
import random

app = Flask(__name__)

# ------------------------------
# 1️⃣ Preparar el modelo
# ------------------------------
df = pd.read_csv("videos.csv")
df["tipo"] = df["tipo"].map({"corto": 0, "largo": 1})
df["plataforma"] = df["plataforma"].map({"TikTok": 0, "YouTube": 1})
df["dia"] = df["dia"].map({
    "lunes": 0, "martes": 1, "miercoles": 2,
    "jueves": 3, "viernes": 4, "sabado": 5, "domingo": 6
})

X = df[["duracion_seg", "tipo", "plataforma", "dia"]]
y = df["vistas"]
modelo = LinearRegression()
modelo.fit(X, y)

# ------------------------------
# 2️⃣ Función para predecir y monetizar
# ------------------------------
def predecir_video(duracion, tipo, plataforma, dia):
    tipo_num = 0 if tipo == "corto" else 1
    plataforma_num = 0 if plataforma.lower() == "tiktok" else 1
    dia_map = {
        "lunes": 0, "martes": 1, "miercoles": 2,
        "jueves": 3, "viernes": 4, "sabado": 5, "domingo": 6
    }
    dia_num = dia_map[dia.lower()]
    nuevo_video_df = pd.DataFrame([[duracion, tipo_num, plataforma_num, dia_num]],
                                  columns=["duracion_seg", "tipo", "plataforma", "dia"])
    vistas_estimadas = modelo.predict(nuevo_video_df)[0]

    if plataforma_num == 1:  # YouTube
        cpm = 2
    else:  # TikTok
        cpm = 0.5
    ingreso_estimado = (vistas_estimadas / 1000) * cpm
    decision = "GRABAR" if ingreso_estimado >= 5 else "NO GRABAR"
    return int(vistas_estimadas), round(ingreso_estimado, 2), decision

# ------------------------------
# 3️⃣ Ruta principal
# ------------------------------
@app.route("/")
def index():
    # Generar 20 videos simulados
    tipos = ["corto", "largo"]
    plataformas = ["YouTube", "TikTok"]
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

    simulaciones = []
    for _ in range(20):
        duracion = random.randint(20, 600)
        tipo = random.choice(tipos)
        plataforma = random.choice(plataformas)
        dia = random.choice(dias)
        vistas, ingreso, decision = predecir_video(duracion, tipo, plataforma, dia)
        simulaciones.append({
            "duracion": duracion,
            "tipo": tipo,
            "plataforma": plataforma,
            "dia": dia,
            "vistas_estimadas": vistas,
            "ingreso_estimado": ingreso,
            "decision": decision
        })

    df_sim = pd.DataFrame(simulaciones)

    # ------------------------------
    # 4️⃣ HTML para mostrar tabla
    # ------------------------------
    html = """
    <!doctype html>
    <title>Tablero de Ideas de Video</title>
    <h2>Tablero de Ideas de Video Simuladas</h2>
    <table border="1" cellpadding="5">
    <tr>
        <th>Duración</th><th>Tipo</th><th>Plataforma</th><th>Día</th>
        <th>Vistas Estimadas</th><th>Ingreso Estimado</th><th>Decisión</th>
    </tr>
    {% for row in datos %}
    <tr>
        <td>{{ row.duracion }}</td>
        <td>{{ row.tipo }}</td>
        <td>{{ row.plataforma }}</td>
        <td>{{ row.dia }}</td>
        <td>{{ row.vistas_estimadas }}</td>
        <td>${{ row.ingreso_estimado }}</td>
        <td>{{ row.decision }}</td>
    </tr>
    {% endfor %}
    </table>
    """
    return render_template_string(html, datos=df_sim.to_dict(orient="records"))

# ------------------------------
# 5️⃣ Arrancar Flask
# ------------------------------
import os

if __name__ == "__main__":
    app.run()


