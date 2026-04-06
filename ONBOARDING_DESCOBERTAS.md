# Onboarding IA - Plenus Cloud
## Exploração de Frameworks e Datasets

**Data:** Abril de 2026  
**Status:** Dia 1 - Exploração Inicial  
**Responsável:** Equipe IA

---

## 1. Estrutura Atual dos Datasets

### 1.1 Dataset COCO128 ✅ (Verificado)

**Localização:** `/workspaces/yolo-pytorch-studies/datasets/coco128/`

| Aspecto | Informação |
|--------|-----------|
| **Status** | ✅ Disponível |
| **Propósito** | Detecção de objetos (baseline de testes) |
| **Total de imagens** | 128 |
| **Classes** | 80 (dataset COCO) |
| **Split** | train2017 (128 imagens, sem val separado) |
| **Formato** | `images/train2017/*.jpg` + `labels/train2017/*.txt` |
| **Objetos por imagem** | ~2-5 (média) |
| **Resolução típica** | Variável (485x640 ~ 640x480) |
| **Tamanho total** | ~20 MB |

**Características:**
- Dados públicos do dataset COCO original
- Formato YOLO padrão: `<class_id> <x_center> <y_center> <width> <height>` (normalizado 0-1)
- Adequado para validação rápida de pipeline
- Recomendado para testes: treinamento completo em ~5-10 min (GPU)

---

### 1.2 Dataset de Veículos ⚠️ (Não encontrado)

**Localização esperada:** `/workspaces/datasets/veiculos/`

| Aspecto | Status |
|--------|--------|
| **Encontrado** | ❌ Não |
| **Referência** | YAML config: `veiculos-cor-v1.yaml` |
| **Propósito esperado** | Classificação de cor/tipo/modelo de veículos |
| **Estrutura esperada** | `images/` + `labels/` (YOLO format) |

**Ação requerida:**
- [ ] Localizar dataset atual (pode estar em outro caminho)
- [ ] Validar estrutura
- [ ] Migrar ou criar sym-link

---

### 1.3 Dataset de Atributos Faciais ⚠️ (Não encontrado)

**Localização esperada:** `/workspaces/datasets/facial_attributes/`

| Aspecto | Status |
|--------|--------|
| **Encontrado** | ❌ Não |
| **Propósito esperado** | Classificação de atributos faciais |
| **Possível tamanho** | Desconhecido |

---

## 2. Taxonomia Proposta para Datasets

### 2.1 Dataset de Veículos (Cor, Modelo, Tipo)

#### Opção A: Abordagem Multi-Atributo (Recomendada)
Três modelos YOLO separados, cada um especializado em um atributo:

```
├── Modelo 1: Classificação de COR
│   └── Classes: branco, preto, prata, cinza, vermelho, azul, verde, amarelo, laranja, outro
│
├── Modelo 2: Classificação de TIPO
│   └── Classes: hatch, sedan, SUV, pickup, van, ônibus, caminhão, moto
│
└── Modelo 3: Classificação de MARCA/MODELO (opcional)
    └── Classes: a definir conforme dataset disponível
```

**Vantagens:**
- Cada modelo pode ser otimizado independentemente
- Melhor balanceamento de classes por atributo
- Facilita retreinamento incremental
- Escalabilidade: adicionar marcas sem reajustar cores/tipos

**Desvantagens:**
- Requer 3 inferências por detecção (latência +)
- Maior overhead computacional

#### Opção B: Abordagem Single-Model (Multi-classe)
Um único modelo com todas as combinações:

```
Classes: branco_sedan, branco_suv, preto_sedan, ... (combinatória)
```

**Vantagens:**
- Inferência única (latência -)
- Contexto: modelo aprende correlações (cor frequente com tipo)

**Desvantagens:**
- Explosão combinatória de classes (10 cores × 8 tipos = 80 classes)
- Desbalanceamento: nem todas combinações existem
- Difícil de manter e reajustar

**Recomendação:** ✅ **Opção A** (Multi-Atributo)

---

### 2.2 Dataset de Atributos Faciais

#### Schema Proposto: Multi-Atributo com Labels

```yaml
Atributos:
  Barba:
    - sem_barba (predefinido)
    - barba_curta (< 1 cm)
    - barba_média (1-3 cm)
    - barba_longa (> 3 cm)
    - cavanhaque
    Nota: Usar referência visual com régua (mm)
  
  Óculos:
    - sem_oculos
    - oculos_escuros
    - oculos_normal
    - oculos_leitura
    Nota: Clareza: óculos sobre o rosto
  
  Cabelo:
    - cabelo_curto (< 5 cm)
    - cabelo_medio (5-15 cm)
    - cabelo_longo (> 15 cm)
    - careca
    Nota: Comprimento na parte frontal
  
  Expressão:
    - neutral
    - sorriso
    - serio
    - triste
    - surpreso
  
  Gênero (se necessário):
    - feminino
    - masculino
    - ambiguo (se houver dúvida)
```

**Observações Importantes:**

1. **Desbalanceamento esperado:**
   - "sem_barba" >> outros (80%+ habitual em datasets públicos)
   - "sem_oculos" >> outros (60-70%)
   - Necessário data augmentation ou oversampling

2. **Ambiguidades a evitar:**
   - ❌ "barba_curta vs. cavanhaque" - usar definição visual clara
   - ❌ "óculos_escuros vs oculos_transparente" - exemplos visuais
   - ❌ "cabelo_curto vs cabelo_medio" - usar marcos (orelhao, queixo)

3. **Formato recomendado:** Multi-label (uma face pode ter múltiplos atributos)
   ```
   Exemplo: pessoa.jpg → ["barba_media", "oculos_normal", "cabelo_longo", "sorriso"]
   ```

---

## 3. Estrutura de Configuração

### 3.1 Arquivo de Config Atual

**Localização:** `/workspaces/yolo-pytorch-studies/experimentos/configs/veiculos-cor-v1.yaml`

```yaml
experiment:
  name: veiculos-cor-v1
  task: classify  # ← Classificação (não detecção)
  
dataset:
  name: veiculos-cor-v2
  path: /workspaces/datasets/veiculos
  
model:
  base: yolov8n.pt  # nano - mais rápido
  pretrained: true
  
hyperparams:
  epochs: 50
  batch: 16
  imgsz: 640
  device: cuda  # ← Requer GPU
```

**Observações:**
- Task: `classify` indica modelo YOLOv8 em modo classificação (-C para crop)
- Esperado receber crops já cortados (não frames completos)
- Compatível com pipeline gRPC descrito

---

## 4. Pipeline de Inferência (Contexto)

```
Fluxo esperado no servidor gRPC:
    
    Frame completo
         ↓
    [YOLO Detect] → Bounding boxes de veículos/pessoas
         ↓
    Crop cada detecção
         ↓
    [YOLO Classify] → Atributos (cor, expressão, etc.)
         ↓
    Retornar resultado ao cliente
```

**Implicações:**
- Modelos recebem **crops**, não frames
- Tamanho de input: ~224x224 tipicamente (imgsz em config)
- Latência crítica: cada modelo deve ser rápido

---

## 5. Rastreamento de Experimentos

### 5.1 Status Atual

**Ferramenta:** ❌ Nenhuma ferramenta formal  
**Solução temporária:** Registro manual em JSON

**Arquivo:** `/workspaces/yolo-pytorch-studies/experiments_log.json`

### 5.2 Proposta: MLflow

**Instalação:**
```bash
pip install mlflow
mlflow ui --host 0.0.0.0 --port 5000
# Acessar em: http://localhost:5000
```

**Vantagens:**
- ✅ Dashboard web interativo
- ✅ Comparação entre experimentos
- ✅ Armazenamento automático de modelos
- ✅ Integração com principais frameworks
- ✅ Suporta múltiplos usuários

**Alternativa:** Weights & Biases (W&B)
- Setup: `pip install wandb && wandb login`
- Mais polido, mas requer account cloud
- Melhor para produção/sharing

**Recomendação:** ✅ **MLflow** (auto-hospedado, controle total)

---

## 6. Dúvidas e Pontos de Decisão

### Clarificações Necessárias

| # | Pergunta | Impacto | Prioridade |
|----|----------|--------|-----------|
| 1 | Qual é tamanho de input esperado (crop)? | Arquitetura do modelo | 🔴 Alta |
| 2 | Pipeline: YOLO det → classif, ou direto classif? | Organização dados | 🔴 Alta |
| 3 | Há datasets antigos/privados a reintegrar? | Volume de trabalho | 🟡 Média |
| 4 | SLA de latência? (ms) | Otimizações necessárias | 🟡 Média |
| 5 | Modelo multi-task vs. modelos separados? | Design de treinamento | 🟡 Média |
| 6 | Será usado MLflow ou W&B? | Setup inicial | 🟢 Baixa |
| 7 | Quantas marcas/modelos incluir? | Viabilidade dataset | 🟡 Média |
| 8 | Validação inter-anotador: qual threshold? | QA do dataset | 🔴 Alta |

---

## 7. Scripts e Utilitários Criados

### 7.1 Notebook Interativo

**Arquivo:** `onboarding_ia.ipynb`

Células incluem:
1. ✅ Setup de ambiente e importações
2. ✅ Inferência local com YOLO
3. ✅ Validação do pipeline de treinamento
4. ✅ Exemplos de exportação (ONNX, TensorRT)
5. ✅ Análise de datasets
6. ✅ Schema de atributos faciais
7. ✅ Sistema de rastreamento de experimentos

---

## 8. Checklist Ação para Próximas Etapas

### Dia 1 (Hoje)
- [ ] Revisar este documento com equipe
- [ ] Confirmar que tamanho/formato de inputs gRPC
- [ ] Executar: `python treinar_coco128.py` (validar setup)
- [ ] Explorar saídas em `/workspaces/yolo-pytorch-studies/runs/`

### Dias 2-3
- [ ] Localizar/validar dataset de veículos
- [ ] Localizar/validar dataset de atributos faciais
- [ ] Documentar estrutura atual real
- [ ] Propor ajustes na taxonomia baseado em dados reais

### Semana 1
- [ ] Decidir: Opção A ou B para veículos (discutir)
- [ ] Decdir: MLflow vs W&B (setup)
- [ ] Criar guidelines de anotação (PDF com imagens)
- [ ] Planejar coleta adicional se necessário

### Semana 2+
- [ ] Iniciar treinamentos pilotos
- [ ] Validar performance em cenários reais
- [ ] Refinar hiperparâmetros

---

## 9. Referências e Documentação

| Recurso | Link |
|---------|------|
| **Ultralytics Docs** | https://docs.ultralytics.com |
| **YOLO Format** | https://docs.ultralytics.com/datasets/detect/ |
| **DeepStream Dev Guide** | https://docs.nvidia.com/metropolis/deepstream/dev-guide/ |
| **MLflow** | https://mlflow.org/docs/ |
| **CelebA Dataset** | http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html |
| **VeRi-776** | https://github.com/JDAI-CV/VeRi |
| **CompCars Dataset** | http://mmlab.ie.cuhk.edu.hk/datasets/comp_cars/index.html |

---

## Anexo: Comandos Úteis

```bash
# Executar notebook
jupyter notebook onboarding_ia.ipynb

# Treinar COCO128
python treinar_coco128.py

# MLflow UI (quando setup)
mlflow ui --host 0.0.0.0 --port 5000

# Exportar modelo
python -c "from ultralytics import YOLO; m = YOLO('best.pt'); m.export(format='onnx')"

# Análise de dataset
python scripts/analise_datasets.py

# Validar Ultralytics
python scripts/validar_ultralytics.py
```

---

**Documento preparado para:** Onboarding Equipe IA  
**Versão:** 1.0  
**Próxima revisão:** Próxima reunião de alinhamento
