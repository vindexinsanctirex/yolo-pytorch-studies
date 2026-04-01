from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # Baixa um modelo pré-treinado pequeno
results = model("https://ultralytics.com/images/bus.jpg")
results[0].show()  # Deve abrir uma janela com a imagem e as detecções