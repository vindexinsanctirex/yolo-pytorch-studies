# Quick Start - Onboarding IA

## 🚀 Primeiros Passos (5 minutos)

### 1. Abrir o Notebook Interativo
```bash
# No VS Code, abra:
onboarding_ia.ipynb
```

### 2. Executar as células em ordem
- Célula 2: Importa bibliotecas (valida ambiente)
- Célula 4: Carrega modelo YOLOv8
- Célula 5: Testa inferência em imagem local
- Célula 7: Mostra estrutura de COCO128

### 3. Ler o Documento de Descobertas
```
ONBOARDING_DESCOBERTAS.md  ← Documento principal
```

---

## 📊 Descobertas Principais

### ✅ Ambiente Validado
- Python 3.12.3 (venv)
- Ultralytics YOLO disponível
- Dataset COCO128 pronto (128 imagens públicas)

### ⚠️ Pendências
- Dataset de veículos: não encontrado em `/workspaces/datasets/veiculos`
- Dataset facial: não encontrado em `/workspaces/datasets/facial_attributes`
- MLflow: não instalado (opcional, recomendado para futuro)

### 🎯 Próximos Passos
1. **Localizar** e validar datasets reais
2. **Decidir** estratégia: modelos separados (cores/tipos) vs. single-model
3. **Setup** MLflow para rastreamento
4. **Criar** guidelines de anotação

---

## 📁 Arquivos Principais

| Arquivo | Propósito |
|---------|-----------|
| `onboarding_ia.ipynb` | Notebook interativo completo (todas as 7 seções) |
| `ONBOARDING_DESCOBERTAS.md` | Documento de descobertas (ESTE) |
| `treinar_coco128.py` | Script de treinamento rápido |
| `example.py` | Exemplo simples de inferência |
| `experimentos/configs/veiculos-cor-v1.yaml` | Config de experimento |
| `experimentos/mlflow_training.py` | Classe para logging com MLflow |

---

## 🔗 Arquitetura Esperada

```
Imagem completa
      ↓
[YOLO Detect] → Encontra veículos/pessoas
      ↓
Crop cada detecção
      ↓
[YOLO Classify] → Classifica atributos
      ↓
Retorna resultado gRPC
```

**Implicação:** Modelos de classificação recebem **crops**, não frames completos.

---

## 📋 Taxonomia Proposta

### Cores (Veículos)
```
branco, preto, prata, cinza, vermelho, azul, verde, amarelo, laranja, outro
```

### Tipos (Veículos)
```
hatch, sedan, SUV, pickup, van, ônibus, caminhão, moto
```

### Atributos Faciais (Multi-label)
```
Barba: sem, curta, média, longa, cavanhaque
Óculos: sem, escuros, normal, leitura
Cabelo: curto, médio, longo, careca
Expressão: neutral, sorriso, sério, triste, surpreso
Gênero: feminino, masculino, ambiguo
```

⚠️ **Desbalanceamento esperado:** Classes negativas dominam (80%+ "sem barba")

---

## ⚙️ Como Executar Testes

### Teste 1: Validar Ambiente
```bash
cd /workspaces/yolo-pytorch-studies
.venv/bin/python scripts/validar_ultralytics.py
```

### Teste 2: Análise de Dataset
```bash
.venv/bin/python scripts/analise_datasets.py
```

### Teste 3: Treinamento Rápido (5-10 min)
```bash
.venv/bin/python treinar_coco128.py
# Resultados em: runs/detect/train/
```

### Teste 4: Inferência
```bash
.venv/bin/python example.py
```

---

## 🎓 Conceitos-Chave

### Formato YOLO
```
images/train2017/000000000009.jpg
labels/train2017/000000000009.txt

Conteúdo do .txt:
45 0.479492 0.688771 0.955609 0.5955
50 0.637063 0.732938 0.494125 0.510583

Formato: <class_id> <x_center> <y_center> <width> <height>
Valores: normalizados entre 0 e 1
```

### Modos YOLO
- `detect`: Encontra objetos (bounding boxes)
- `classify`: Classifica crops individuais
- `pose`: Detecta pontos de articulação

---

## 💾 Rastreamento de Experimentos

### Opção 1: Simples (JSON)
```python
from experiments import ExperimentTracker

tracker = ExperimentTracker()
tracker.log_experiment(
    name="Baseline",
    dataset="COCO128",
    config={"epochs": 50, "batch": 16},
    results={"mAP50": 0.456}
)
```

### Opção 2: Robusto (MLflow)
```bash
pip install mlflow
mlflow ui --host 0.0.0.0 --port 5000
# Acessar: http://localhost:5000
```

---

## 🔴 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Import Error: `No module named ultralytics` | Ativar venv: `source .venv/bin/activate` |
| CUDA não encontrada | Usar device='cpu' na config |
| Arquivo model `.pt` grande (50+MB) | Usar versão 'nano' (yolov8n.pt) |
| Treinamento lento | Dataset COCO128 é pequeno, normal ser rápido |
| Dataset não encontrado | Verificar path em YAML config |

---

## 📖 Leitura Recomendada

### Dia 1 (Hoje)
- [ ] Este README
- [ ] ONBOARDING_DESCOBERTAS.md

### Dias 2-3
- [ ] https://docs.ultralytics.com (25 min)
- [ ] YOLO Format: https://docs.ultralytics.com/datasets/detect/ (10 min)

### Semana 1
- [ ] DeepStream basics (1h)
- [ ] MLflow tutorial (30 min)

---

## 🆘 Contato e Dúvidas

**Dúvidas pendentes listadas em:** `ONBOARDING_DESCOBERTAS.md` (Seção 6)

**Para discussão com o time:**
1. Tamanho/formato de crops gRPC
2. Pipeline: detecção → classificação
3. Prioridade: cores vs. tipos vs. marcas
4. MLflow ou W&B?

---

**Última atualização:** Abril 6, 2026  
**Status:** ✅ Pronto para uso
