# Template de Configuração para Datasets

Este arquivo contém templates de configuração YAML para diferentes cenários de treinamento.

## 1. Template: Classificação de Cor (Veículos)

Arquivo: `experimentos/configs/veiculos-cores.yaml`

```yaml
# Experimento: Classificação de Cores de Veículos
experiment:
  name: "veiculos-cores-v1"
  description: "Classificação de cor de veículos com YOLOv8n"
  owner: "equipe-ia"
  priority: "high"
  created: "2026-04-06"

# Dataset
dataset:
  name: "veiculos-cores"
  path: "/workspaces/datasets/veiculos"
  task: "classify"  # Em vez de 'detect'
  splits:
    train: 0.7
    val: 0.2
    test: 0.1
  classes:
    - branco
    - preto
    - prata
    - cinza
    - vermelho
    - azul
    - verde
    - amarelo
    - laranja
    - outro

# Modelo
model:
  base: "yolov8n.pt"  # nano - rápido, 3.2M parâmetros
  task: "classify"
  pretrained: true
  # Alternativas: yolov8s.pt (11.2M), yolov8m.pt (25.9M)

# Hiperparâmetros
hyperparams:
  epochs: 100
  batch: 32
  imgsz: 224  # Tamanho padrão para classificação
  patience: 20  # Early stopping
  device: "cuda"  # GPU
  optimizer: "SGD"      # ou "AdamW"
  lr0: 0.001
  lrf: 0.01
  momentum: 0.937
  weight_decay: 0.0005
  warmup_epochs: 3
  warmup_momentum: 0.8
  warmup_bias_lr: 0.1

# Data Augmentation
augmentation:
  hsv_h: 0.015      # Hue
  hsv_s: 0.7        # Saturation (importante para cores!)
  hsv_v: 0.4        # Value
  rotate: 0.0
  translate: 0.1
  scale: 0.5
  flipud: 0.0       # Não flipar cores verticalmente
  fliplr: 0.5       # Sim, horizontalmente
  mosaic: 1.0       # Mosaic augmentation
  mixup: 0.0        # Sem mixup (pode confundir cores)
  copy_paste: 0.0

# Validação
validation:
  split: "val"
  conf_threshold: 0.5
  iou_threshold: 0.6  # Não aplicável para classify, mas compatível
  max_det: 300

# Early Stopping
early_stopping:
  patience: 20
  min_delta: 0.001
```

---

## 2. Template: Classificação de Tipo (Veículos)

Arquivo: `experimentos/configs/veiculos-tipos.yaml`

```yaml
# Experimento: Classificação de Tipo de Veículos
experiment:
  name: "veiculos-tipos-v1"
  description: "Classificação de tipo de veículos (sedan, SUV, etc.)"
  owner: "equipe-ia"

dataset:
  name: "veiculos-tipos"
  path: "/workspaces/datasets/veiculos"
  classes:
    - hatch
    - sedan
    - suv
    - pickup
    - van
    - onibus
    - caminhao
    - moto

model:
  base: "yolov8n.pt"
  pretrained: true

hyperparams:
  epochs: 100
  batch: 32
  imgsz: 224
  lr0: 0.001
  weight_decay: 0.0005

augmentation:
  fliplr: 0.5
  hsv_s: 0.3  # Menos importante que para cores
  scale: 0.5
```

---

## 3. Template: Multi-Atributos Faciais

Arquivo: `experimentos/configs/atributos-faciais.yaml`

```yaml
# Experimento: Classificação de Atributos Faciais (Multi-label)
experiment:
  name: "atributos-faciais-v1"
  description: "Multi-label classification: barba, óculos, cabelo, expressão"
  owner: "equipe-ia"
  multi_label: true  # IMPORTANTE: múltiplos atributos por imagem

dataset:
  name: "facial-attributes"
  path: "/workspaces/datasets/facial_attributes"
  task: "multi-label-classify"  # Extensão do Ultralytics
  
  # Schema: cada atributo como sub-classificação
  attributes:
    barba:
      classes: ["sem_barba", "barba_curta", "barba_media", "barba_longa", "cavanhaque"]
      required: true
    oculos:
      classes: ["sem_oculos", "oculos_escuros", "oculos_normal", "oculos_leitura"]
      required: true
    cabelo:
      classes: ["cabelo_curto", "cabelo_medio", "cabelo_longo", "careca"]
      required: true
    expressao:
      classes: ["neutral", "sorriso", "serio", "triste", "surpreso"]
      required: false
    genero:
      classes: ["feminino", "masculino", "ambiguo"]
      required: false

model:
  base: "yolov8m.pt"  # Médio para maior capacidade
  pretrained: true

# Importante: balanceamento via ponderação de classes
hyperparams:
  epochs: 100
  batch: 16
  imgsz: 224
  lr0: 0.0001  # Learning rate menor para datasets balanceados
  class_weights: true  # Usar pesos para classes minoritárias
  
  # Pesos manuais (exemplo)
  # barba_longa: 2.0  # Overweight classes raras
  # cavanhaque: 2.0
  # oculos_escuros: 1.5

augmentation:
  fliplr: 0.5
  flipud: 0.0  # Não flipar rosto verticalmente
  hsv_h: 0.1
  rotate: 15  # Pequena rotação
  brightness: 0.2
  contrast: 0.2
  saturation: 0.2

data_balancing:
  strategy: "oversampling"  # ou "undersampling"
  target_ratio: 0.5  # 50% min class ratio target
  random_seed: 42

validation:
  f1_weighted: true  # F1 ponderado para multi-label
```

---

## 4. Template: Detecção + Classificação (Pipeline)

Arquivo: `experimentos/configs/pipeline-detectar-classificar.yaml`

Estrutura YAML para executar pipeline em sequência:

```yaml
# Pipeline: Detecção (veículos/pessoas) → Classificação (atributos)
pipeline:
  name: "detect-classify-pipeline-v1"
  
  stages:
    - name: "detection"
      type: "detect"
      model: "/path/to/detect_model.pt"
      config:
        conf_threshold: 0.5
        iou_threshold: 0.4
        classes: [2, 5, 7]  # apenas cars, bus, truck
    
    - name: "classification"
      type: "classify"
      model: "/path/to/classify_model.pt"
      config:
        conf_threshold: 0.6
        imgsz: 224
      apply_to: ["detection"]  # Usa outputs do estágio anterior

  # Pós-processamento
  postprocess:
    filter_small_detections: 50  # pixels
    merge_overlapping_crops: true
    iou_merge_threshold: 0.3

  # Saída
  output:
    format: "json"  # ou "protobuf" para gRPC
    include_confidence: true
    include_bbox: true
```

---

## 5. Como Usar Estes Templates

### Passo 1: Copiar template apropriado
```bash
cp experimentos/configs/template_veiculos-cores.yaml \
   experimentos/configs/veiculos-cores-v1.yaml
```

### Passo 2: Editar paths e parâmetros
```yaml
dataset:
  path: "/workspaces/datasets/veiculos"  # Seu dataset
  
hyperparams:
  batch: 32  # Ajustar conforme GPU disponível
  device: "cuda"  # ou "cpu"
```

### Passo 3: Treinar
```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model.train(
    data="experimentos/configs/veiculos-cores-v1.yaml",
    epochs=100,
    batch=32,
    device="cuda"
)
```

---

## 6. Ajustes por Hardware

### GPU de 8GB (NVIDIA Tesla)
```yaml
batch: 32
imgsz: 224
device: "cuda"
workers: 4
```

### GPU de 16GB (NVIDIA RTX 3060)
```yaml
batch: 64
imgsz: 224
device: "cuda"
workers: 8
```

### CPU apenas
```yaml
batch: 8
imgsz: 224
device: "cpu"
workers: 0
epochs: 50  # Menos épocas para acelerar
```

---

## 7. Observações Importantes

### Para Classificação de Cores
- ⚠️ Data augmentation em HSV (Hue, Saturation, Value) é crítica
- ⚠️ Aumentar `hsv_s` para capturar variações
- ✅ Usar imgsz=224 (padrão ImageNet)

### Para Múltiplas Categorias
- ⚠️ Datasets desbalanceados: usar `class_weights=true`
- ⚠️ Multi-label requer formato especial de labels
- ✅ Usar F1-score ponderado para validação

### Para Atributos Faciais
- ⚠️ Evitar flipud (virar rosto de cabeça para baixo)
- ⚠️ Normalizar iluminação em pré-processamento
- ✅ Usar guidelines visuais para anotadores

---

## 8. Checklist Pré-Treinamento

- [ ] Dataset estrutura validada (`images/` + `labels/`)
- [ ] Classes definidas e documentadas
- [ ] Dados balanceados (ou plan de balanceamento)
- [ ] Split train/val/test: 70/15/15 (ou similar)
- [ ] Augmentation: apropriada para tarefa
- [ ] GPU/CPU disponível e testado
- [ ] MLflow ou experiment tracker ativo
- [ ] Hyperparâmetros aprovados por equipe

---

**Versão:** 1.0  
**Última atualização:** Abril 6, 2026
