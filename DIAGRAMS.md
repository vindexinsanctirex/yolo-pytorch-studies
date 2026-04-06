# Diagrama Visual - Estrutura do Onboarding IA

## 1. Estructura do Projeto (Tree View)

```
Onboarding IA - YOLO/DeepStream
│
├─ 📋 DOCUMENTAÇÃO
│  ├─ 📄 README_INDICE.md          ← ÍNDICE PRINCIPAL (comece aqui!)
│  ├─ 📄 EXECUTIVE_SUMMARY.md      ← Para gerentes
│  ├─ 📄 QUICKSTART.md              ← Para devs
│  ├─ 📄 ONBOARDING_DESCOBERTAS.md  ← Análise detalhada
│  ├─ 📄 DECISION_LOG.md            ← Dúvidas a responder
│  ├─ 📄 TEMPLATE_CONFIGS.md        ← Templates YAML
│  └─ 📄 Este arquivo
│
├─ 📓 NOTEBOOK INTERATIVO
│  └─ 📓 onboarding_ia.ipynb
│     └─ 7 seções: Setup → Inferência → Treinamento → Análise → Experimentos
│
├─ 🐍 SCRIPTS
│  ├─ onboarding_log.py             ← Resumir experimentos
│  ├─ scripts/analise_datasets.py    ← Analisar estrutura
│  └─ scripts/validar_ultralytics.py ← Validar ambiente
│
├─ ⚙️  CONFIGURAÇÕES
│  └─ experimentos/configs/
│     └─ veiculos-cor-v1.yaml       ← Config de referência
│
└─ 📊 DATASETS
   └─ datasets/
      └─ coco128/                    ← ✅ Disponível (128 imagens)
         ├─ images/train2017/
         └─ labels/train2017/
```

---

## 2. Fluxo de Trabalho Esperado

```
FASE 1: EXPLORAÇÃO (✅ COMPLETO)
  ├─ Validar ambiente           ✅
  ├─ Explorar COCO128           ✅
  ├─ Propor taxonomia           ✅
  └─ Documentar descobertas     ✅

FASE 2: DECISÕES (⏳ AGUARDANDO)
  ├─ Responder críticas         ❓
  │  ├─ Input size gRPC         ❓
  │  ├─ Pipeline               ❓
  │  └─ SLA latência            ❓
  ├─ Localizar datasets         ❓
  └─ Decidir estratégia         ❓

FASE 3: SETUP (📅 PRÓXIMO)
  ├─ Setup MLflow              📅
  ├─ Atualizar configs         📅
  ├─ Preparar datasets         📅
  └─ Validar pipeline          📅

FASE 4: TREINAMENTO (🚀 FUTURO)
  ├─ Treinar modelo piloto     🚀
  ├─ Validar resultados        🚀
  └─ Deploy em produção        🚀
```

---

## 3. Pipeline de Inferência (Esperado)

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA ESPERADO                         │
└─────────────────────────────────────────────────────────────┘

    Frame completo
         │
         ▼
    ┌──────────────┐
    │ YOLO Detect  │ ← Detecta veículos/pessoas
    └──────────────┘
         │
         ├─ [Box1 (0.2, 0.3, 0.5, 0.6)]
         ├─ [Box2 (0.6, 0.4, 0.9, 0.8)]
         └─ [BoxN (...)]
         │
         ▼
    ┌──────────────────┐
    │ Extrair Crops    │ ← De cada bounding box
    └──────────────────┘
         │
         ├─ Crop1: 224x224
         ├─ Crop2: 224x224
         └─ CropN: 224x224
         │
         ▼
    ┌──────────────────┐
    │ YOLO Classify    │ ← Classifica atributos
    └──────────────────┘
         │
         ├─ Crop1 → [branco, sedan, sorriso]
         ├─ Crop2 → [preto, pickup, neutral]
         └─ CropN → [...]
         │
         ▼
    ┌──────────────────┐
    │ Retorno gRPC     │ ← [[box1, attr1], [box2, attr2], ...]
    └──────────────────┘
```

---

## 4. Taxonomia Proposta (Visual)

```
🚗 VEÍCULOS (3 Dimensões)
│
├─ 🎨 COR (10 classes)
│  ├─ Branco
│  ├─ Preto
│  ├─ Prata
│  ├─ Cinza
│  ├─ Vermelho
│  ├─ Azul
│  ├─ Verde
│  ├─ Amarelo
│  ├─ Laranja
│  └─ Outro
│
├─ 📦 TIPO (8 classes)
│  ├─ Hatch
│  ├─ Sedan
│  ├─ SUV
│  ├─ Pickup
│  ├─ Van
│  ├─ Ônibus
│  ├─ Caminhão
│  └─ Moto
│
└─ 🏷️  MARCA (Variável)
   └─ [A definir based no volume de dados]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 ATRIBUTOS FACIAIS (Multi-label)
│
├─ 🧔 BARBA
│  ├─ Sem barba (80% típico)
│  ├─ Barba curta
│  ├─ Barba média
│  ├─ Barba longa
│  └─ Cavanhaque
│
├─ 👓 ÓCULOS
│  ├─ Sem óculos (70% típico)
│  ├─ Escuros
│  ├─ Normal
│  └─ Leitura
│
├─ 💇 CABELO
│  ├─ Curto
│  ├─ Médio
│  ├─ Longo
│  └─ Careca
│
├─ 😊 EXPRESSÃO
│  ├─ Neutral
│  ├─ Sorriso
│  ├─ Sério
│  ├─ Triste
│  └─ Surpreso
│
└─ ♀️ GÊNERO (Optional)
   ├─ Feminino
   ├─ Masculino
   └─ Ambiguo
```

---

## 5. Dataset Situation (Status Atual)

```
┌────────────────┬─────────┬────────────────────────┐
│ Dataset        │ Status  │ Localização            │
├────────────────┼─────────┼────────────────────────┤
│ COCO128        │ ✅      │ datasets/coco128/      │
│ Veículos       │ ❌      │ /workspaces/datasets/  │
│ Facial         │ ❌      │ /workspaces/datasets/  │
│ MLflow         │ ⏳      │ pip install mlflow     │
└────────────────┴─────────┴────────────────────────┘
```

---

## 6. Decisões Críticas (Decision Tree)

```
                    INÍCIO
                      │
                      ▼
        ┌─ Tamanho input: 224x224?
        │
        ▼─── SIM ───────────────────────► Config padrão
Pipeline gRPC?  │
        │       ▼─── NÃO ─────────────► ?
        │
        └─ Detectar + Classificar?
           │
           ▼─── SIM ───────────────────► 2 modelos
        Pipeline
           │
           ▼─── NÃO ─────────────────► 1 modelo

                DECISÕES
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Opção A    Opção B    Opção C
   (Cores     (Single    (Custom)
    separado)  model)
        │          │
        └──────┬───┘
               ▼
        TEMPLATES
        CONFIGS
               │
               ▼
          TREINAMENTO
```

---

## 7. Timeline Proposta (Gantt Chart)

```
SEMANA 1
├─ [██████░] Seg/Ter: Respostas críticas
├─ [██████░] Ter/Qua: Localizar datasets
├─ [████░░░] Qua/Qui: Validar estrutura
└─ [███░░░░] Fri: Setup MLflow

SEMANA 2
├─ [██████░] Seg/Ter: Preparar dados
├─ [████████] Ter/Qua: Primeiro treino
├─ [████░░░] Qua/Qui: Validar resultados
└─ [██░░░░░] Fri: Ajustes

SEMANA 3+
└─ [░░░░░░░] Treinamentos produção
```

---

## 8. Matriz de Responsabilidades

```
┌─────────────────────┬──────┬──────┬──────┬──────┐
│ Atividade           │ Dev  │  PM  │ Arch │ Data │
├─────────────────────┼──────┼──────┼──────┼──────┤
│ Decidir estratégia  │      │  ●●  │  ○   │  ○   │
│ Setup MLflow        │  ●●  │      │      │      │
│ Localizar dados     │  ○   │  ●●  │      │  ●   │
│ Treinar modelos     │  ●●  │      │      │      │
│ Validar pipeline    │  ●   │  ●   │  ●●  │      │
│ Anotar dados        │      │      │      │  ●●  │
└─────────────────────┴──────┴──────┴──────┴──────┘
● = Envolvido
●● = Responsável
```

---

## 9. Risk Matrix

```
                           IMPACTO
               BAIXO    MÉDIO    ALTO
            ┌─────────────────────────┐
    BAIXA   │                  ●      │  ● = MLflow
            │                         │
PROBABILIDADE  MÉDIA   │       ●        │
            │         │         ●      │  Risks:
            │                         │  ● Dataset não encontrado
    ALTA    │    ●    │                 |  ● SLA não atendido
            │         │        ●        |  ● Desbalanceamento extremo
            └─────────────────────────┘
```

---

## 10. Quick Reference Card

```
┌──────────────────────────────────────┐
│      QUICK REFERENCE CARD            │
├──────────────────────────────────────┤
│                                      │
│ 📖 Ler: EXECUTIVE_SUMMARY.md (5m)   │
│ 🚀 Agir: QUICKSTART.md (10m)        │
│ ❓ Decidir: DECISION_LOG.md (30m)   │
│ 💻 Codificar: onboarding_ia.ipynb   │
│ ⚙️  Configurar: TEMPLATE_CONFIGS.md  │
│                                      │
│ 🔗 Índice: README_INDICE.md         │
│                                      │
│ Comandos úteis:                      │
│ • python onboarding_log.py           │
│ • python scripts/analise_datasets.py │
│ • jupyter notebook onboarding_ia.... │
│                                      │
└──────────────────────────────────────┘
```

---

## 11. Legenda de Símbolos

```
✅ = Completo
⏳ = Em progresso / Aguardando
❌ = Não encontrado / Não funcionou
❓ = A determinar
🔴 = Crítico
🟡 = Alto
🟢 = Médio/Baixo
📄 = Documento
🐍 = Script Python
📓 = Jupyter Notebook
⚙️ = Configuração
📊 = Dados/Dataset
```

---

## 12. Status Atual (Dashboard)

```
┌─────────────────────────────────────────────────┐
│           ONBOARDING IA - STATUS                │
├─────────────────────────────────────────────────┤
│                                                 │
│ Exploração de Ambiente      [████████░░] 80%   │
│ Documentação               [██████████] 100%   │
│ Notebook Interativo        [██████████] 100%   │
│ Datasets Localizados       [██░░░░░░░░] 20%   │
│ Decisões Críticas          [░░░░░░░░░░] 0%    │
│ Setup MLflow               [░░░░░░░░░░] 0%    │
│ Primeiro Treinamento       [░░░░░░░░░░] 0%    │
│                                                 │
│ GERAL                      [████░░░░░░] 40%   │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

**Diagrama criado:** Abril 6, 2026  
**Formato:** ASCII Art + Markdown  
**Para:** Visualizar estrutura do onboarding
