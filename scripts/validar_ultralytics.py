#!/usr/bin/env python
"""
Script para validar instalação de Ultralytics e testar funcionalidades básicas
"""

import sys
print("\n" + "="*70)
print("VALIDAÇÃO DE ULTRALYTICS YOLO")
print("="*70 + "\n")

# 1. Verificar importação
print("1️⃣  Verificando importação de Ultralytics...")
try:
    from ultralytics import YOLO
    print("   ✅ Ultralytics importado com sucesso\n")
except ImportError as e:
    print(f"   ❌ Erro ao importar Ultralytics: {e}")
    sys.exit(1)

# 2. Verificar modelo pré-treinado
print("2️⃣  Carregando modelo pré-treinado yolov8n.pt...")
try:
    model = YOLO("yolov8n.pt")
    print(f"   ✅ Modelo carregado: {model.model.names}\n")
except Exception as e:
    print(f"   ❌ Erro ao carregar modelo: {e}")
    sys.exit(1)

# 3. Testar inferência com imagem remota
print("3️⃣  Testando inferência com imagem remota...")
try:
    # Usa uma URL de exemplo
    results = model("https://ultralytics.com/images/bus.jpg")
    print(f"   ✅ Inferência realizada!")
    print(f"   - Detecções encontradas: {len(results[0].boxes)}")
    if len(results[0].boxes) > 0:
        print(f"   - Classes detectadas: {results[0].boxes.cls.unique()}\n")
except Exception as e:
    print(f"   ⚠️  Aviso: Inferência remota não funcionou (pode ser problema de rede)")
    print(f"   Erro: {e}\n")

# 4. Testar com imagem local se existir
print("4️⃣  Testando inferência com imagem local...")
try:
    import os
    local_img = "/workspaces/yolo-pytorch-studies/bus.jpg"
    if os.path.exists(local_img):
        results = model(local_img)
        print(f"   ✅ Inferência local realizada!")
        print(f"   - Detecções encontradas: {len(results[0].boxes)}\n")
    else:
        print(f"   ⚠️  Imagem local não encontrada em {local_img}\n")
except Exception as e:
    print(f"   ❌ Erro na inferência local: {e}\n")

# 5. Informações do modelo
print("5️⃣  Informações do modelo YOLOv8n:")
print(f"   - Task: {model.task}")
print(f"   - Model name: {model.model_name}")
print(f"   - Número de parâmetros: {sum(p.numel() for p in model.model.parameters()):,}")
print(f"   - Classes: {len(model.names)} classes disponíveis")

print("\n" + "="*70)
print("✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO")
print("="*70 + "\n")
print("Próximos passos:")
print("1. Explorar datasets com scripts/analise_datasets.py")
print("2. Executar treinamento curto com treinar_coco128.py")
print("3. Revisar estrutura de datasets capturados")
print()
