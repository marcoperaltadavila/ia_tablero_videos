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
# 3️⃣ Ruta principal (herramienta)
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
    <html>
    <head>
        <title>Tablero de Ideas de Video</title>
        <meta name="google-site-verification" content="eNDNIUXalL9G4kRooM9xrerTdntwp2l1-VGwoukLEJw" />
    </head>
    <body>

    <h1>📊 Tablero de Ideas de Video con IA</h1>

    <p>
    Esta herramienta usa inteligencia artificial para estimar cuántas vistas y cuánto ingreso
    podría generar un video antes de grabarlo.
    </p>

    <p>
    Simula distintos tipos de contenido según duración, plataforma y día de publicación,
    para ayudarte a decidir qué videos valen la pena crear.
    </p>

    <table border="1" cellpadding="5">
    <tr>
        <th>Duración</th>
        <th>Tipo</th>
        <th>Plataforma</th>
        <th>Día</th>
        <th>Vistas Estimadas</th>
        <th>Ingreso Estimado</th>
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
        <td>{{ row.decision }}</td>
    </tr>
    {% endfor %}
    </table>

    <p><strong>¿Cómo interpretar estos resultados?</strong></p>
    <ul>
      <li><b>Vistas estimadas:</b> proyección basada en datos históricos simulados.</li>
      <li><b>Ingreso estimado:</b> cálculo aproximado usando CPM promedio.</li>
      <li><b>Decisión:</b> indica si el video tiene potencial económico.</li>
    </ul>

    <p style="font-size:12px;color:gray;">
    Esta herramienta ofrece estimaciones orientativas. Los resultados reales pueden variar según
    calidad del contenido, audiencia y algoritmo de cada plataforma.
    </p>

    <hr>

    <h3>🚀 ¿Qué hacer si un video sale como “GRABAR”?</h3>
    <p>
    Si un video muestra buen potencial, lo ideal es producirlo rápido y con calidad.
    Hoy existen herramientas con inteligencia artificial que permiten crear videos
    profesionales en minutos, incluso sin experiencia previa.
    </p>

    <div style="margin-top:20px;padding:15px;border:1px dashed #999;">
      <strong>🎬 Herramienta recomendada</strong>
      <p>
      Recomendamos usar una herramienta de inteligencia artificial especializada
      en creación de videos para producir contenido de forma rápida y profesional.
      </p>
    </div>

    </body>
    </html>
    """

    return render_template_string(html, datos=df_sim.to_dict(orient="records"))

# ------------------------------
# 4️⃣ Página SEO (contenido)
# ------------------------------
@app.route("/seo")
def seo():
    html = """
    <!doctype html>
    <html>
    <head>
        <title>Cómo saber si un video vale la pena antes de grabarlo</title>
        <meta name="google-site-verification" content="eNDNIUXalL9G4kRooM9xrerTdntwp2l1-VGwoukLEJw" />
    </head>
    <body>

    <h1>Cómo saber si un video vale la pena antes de grabarlo (usando IA)</h1>

    <p>
    Crear videos requiere tiempo, energía y constancia. Uno de los mayores problemas
    para los creadores es no saber si un video tendrá resultados antes de grabarlo.
    </p>

    <h2>Predicción de vistas con inteligencia artificial</h2>
    <p>
    Hoy es posible usar inteligencia artificial para analizar variables como duración,
    plataforma y día de publicación para estimar el potencial de un video.
    </p>

    <h2>Tomar mejores decisiones antes de grabar</h2>
    <p>
    En lugar de grabar a ciegas, una herramienta de predicción permite priorizar ideas
    con mayor probabilidad de éxito.
    </p>

    <h2>Conclusión</h2>
    <p>
    La IA no garantiza resultados exactos, pero sí mejora la toma de decisiones
    para creadores que buscan eficiencia y crecimiento.
    </p>

    <p style="font-size:12px;color:gray;">
    Artículo informativo. No representa promesas de resultados.
    </p>

    </body>
    </html>
    """
    return render_template_string(html)

# ------------------------------
# 5️⃣ Arrancar Flask
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
