from flask import Flask, request, jsonify
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

@app.route("/analisar", methods=["POST"])
def analisar():
    if "image" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"})

    file = request.files["image"]
    img = Image.open(file.stream).convert("RGB")
    img = np.array(img)

    # converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # detectar brilho médio (simples, depois melhora)
    media = np.mean(gray)

    if media > 130:
        sinal = "VERDE"
        explicacao = "Predominância de força compradora"
    else:
        sinal = "VERMELHO"
        explicacao = "Predominância de força vendedora"

    return jsonify({
        "sinal": sinal,
        "explicacao": explicacao
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
