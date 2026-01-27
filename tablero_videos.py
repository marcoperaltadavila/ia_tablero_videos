from flask import Flask, render_template_string
import pandas as pd
from sklearn.linear_model import LinearRegression
import random
import os

app = Flask(__name__)

# ------------------------------
# 1️⃣ Preparar el modelo
# ------------------------------
df = pd.read_csv("videos.csv")
df["tipo"] = df["tipo"].map({"corto": 0, "largo": 1})
df["plataforma"] = df["plataforma"].map({"TikTok": 0, "YouTube": 1})
df["dia"] = df["dia"].map({
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "domingo": 6
})

X = df[["duracion_seg", "tipo", "plataforma", "dia"]]
y = df["vistas"]

modelo = LinearRegression()
modelo.fit(X, y)

# ------------------------------
# 2️⃣ Función de predicción
# ------------------------------
def predecir_video(duracion, tipo, plataforma, dia):
    tipo_num = 0 if tipo == "corto" else 1
    plataforma_num = 0 if plataforma.lower() == "tiktok" else 1
    dia_map = {
        "lunes": 0, "martes": 1, "miercoles": 2,
        "jueves": 3, "viernes": 4, "sabado": 5, "domingo": 6
    }
    dia_num = dia_map[dia.lower()]

    nuevo_video_df = pd.DataFrame(
        [[duracion, tipo_num, plataforma_num, dia_num]],
        columns=["duracion_seg", "tipo", "plataforma", "dia"]
    )

    vistas_estimadas = modelo.predict(nuevo_video_df)[0]

    cpm = 2 if plataforma_num == 1 else 0.5
    ingreso_estimado = (vistas_estimadas / 1000) * cpm

    decision = "GRABAR" if ingreso_estimado >= 5 else "NO GRABAR"

    return int(vistas_estimadas), round(ingreso_estimado, 2), decision

# ------------------------------
# 3️⃣ Ruta principal
# ------------------------------
@app.route("/")
def index():
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

    html = """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Validador de Videos con IA</title>
    </head>
    <body>

    <h1>📊 Validador de Videos con IA</h1>

    <p>
    Esta herramienta utiliza inteligencia artificial para estimar si un video
    vale la pena grabarse antes de que inviertas tiempo y esfuerzo.
    </p>

    <p>
    Analiza duración, plataforma y día de publicación para proyectar vistas,
    ingresos estimados y darte una recomendación clara.
    </p>

    <table border="1" cellpadding="5">
        <tr>
            <th>Duración (seg)</th>
            <th>Tipo</th>
            <th>Plataforma</th>
            <th>Día</th>
            <th>Vistas estimadas</th>
            <th>Ingreso estimado</th>
            <th>Decisión</th>
        </tr>
        {% for row in datos %}
        <tr>
            <td>{{ row.duracion }}</td>
            <td>{{ row.tipo }}</td>
            <td>{{ row.plataforma }}</td>
            <td>{{ row.dia }}</td>
            <td>{{ row.vistas_estimadas }}</td>
            <td>${{ row.ingreso_estimado }}</td>
            <td><strong>{{ row.decision }}</strong></td>
        </tr>
        {% endfor %}
    </table>

    <hr>

    <h3>📩 ¿Quieres recibir ideas de videos con potencial real?</h3>
    <p>
    Déjanos tu email y te avisaremos cuando detectemos nuevas oportunidades
    con verdadero potencial de vistas e ingresos.
    </p>

    <p>
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSeD2b87xyvneZFkUeLKojScwtQ-cepE85ytLTGjG6Cn6oTiow/viewform"
           target="_blank"
           style="padding:10px 15px; background:#2ecc71; color:white; text-decoration:none; border-radius:5px;">
           Quiero recibir ideas por email
        </a>
    </p>

    <h4>¿Cómo interpretar estos resultados?</h4>
    <ul>
        <li><b>Vistas estimadas:</b> proyección basada en datos históricos simulados.</li>
        <li><b>Ingreso estimado:</b> cálculo aproximado usando CPM promedio.</li>
        <li><b>Decisión:</b> indica si el formato tiene potencial económico.</li>
    </ul>

    <p style="font-size:12px;color:gray;">
    El resultado se basa en proyecciones estadísticas y no garantiza resultados reales,
    pero te acerca a tomar mejores decisiones antes de grabar.
    </p>

    </body>
    </html>
    """

    return render_template_string(html, datos=df_sim.to_dict(orient="records"))

# ------------------------------
# 4️⃣ Arranque para Render
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
