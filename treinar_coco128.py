from ultralytics import YOLO

def main():
    print("Iniciando treinamento de exemplo...")
    
    # Carrega um modelo pré-treinado
    model = YOLO("yolov8n.pt")
    
    # Executa o treinamento
    results = model.train(
        data="coco128.yaml",  # Dataset de exemplo
        epochs=3,              # Número de épocas
        imgsz=640,             # Tamanho das imagens
        batch=16,              # Tamanho do batch (opcional)
        workers=4,             # Workers para loading de dados (opcional)
        device="cpu",          # Use "cuda" se tiver GPU, ou "cpu"
        verbose=True           # Mostra logs detalhados
    )
    
    print(f"\nTreinamento concluído!")
    print(f"Resultados salvos em: {results.save_dir}")

if __name__ == "__main__":
    main()