# Resolução de Dúvidas - Checklist de Decisões

Este documento ajuda a equipe a responder as dúvidas críticas levantadas durante o onboarding.

**Data de Criação:** Abril 6, 2026  
**Status:** Aguardando respostas da equipe

---

## Dúvidas CRÍTICAS 🔴 (Responder esta semana)

### Dúvida #1: Tamanho e Formato de Input (Crop)

**Pergunta:** Qual é o tamanho típico e formato dos crops recebidos pelo servidor gRPC?

**Por que é importante:**
- Determina `imgsz` nos configs de treinamento
- Afeta performance e latência
- Impacta qualidade do modelo

**Opções prováveis:**
- [ ] 224x224 (ImageNet padrão, rápido)
- [ ] 320x320 (bom balanço)
- [ ] 640x640 (máxima qualidade, mais lento)
- [ ] Variável (receber different sizes)

**Como descobrir:**
```python
# No servidor gRPC, logar tamanho dos crops:
print(f"Crop shape: {crop.shape}")  # Deve ser (H, W, C)
```

**Resposta da equipe:**
```
[ ] Tamanho: ________x________
[ ] Formato: RGB / BGR / Grayscale
[ ] Normalização: 0-1 / 0-255 / Sem normalização
[ ] Nota adicional: _______________
```

---

### Dúvida #2: Pipeline de Processamento

**Pergunta:** Qual é a sequência esperada de processamento?

```
OPÇÃO A: Detectar → Circular → Classificar
Frame completo
    ↓
[YOLO Detect] → Bounding boxes (pessoas/veículos)
    ↓
Extrair crops de cada bbox
    ↓
[YOLO Classify] → Atributos (cor, expressão, etc.)
    ↓
Retornar: [[box1, atributos1], [box2, atributos2], ...]

OPÇÃO B: Direto Classificar (crops já extraídos)
Frame completo
    ↓
[Outro sistema extrai crops]
    ↓
Receber crops no gRPC
    ↓
[YOLO Classify] → Atributos
    ↓
Retornar: [atributos1, atributos2, ...]

OPÇÃO C: Detectar + Classificar (single-stage)
Frame completo
    ↓
[YOLO Multi-task] → Boxes + Atributos (simultân)
    ↓
Retornar resultado combinado
```

**Resposta da equipe:**
```
[ ] Opção A: Detectar → Crop → Classificar
[ ] Opção B: Classificar crops (já extraído)
[ ] Opção C: Single-stage detect + classify
[ ] Outra: _______________

Fluxograma/descri ao adicional:
___________________________________________________
```

---

### Dúvida #3: SLA de Latência

**Pergunta:** Qual é o tempo máximo aceitável por inferência?

**Por que importa:**
- Define se pode usar modelo grande ou deve ser nano
- Afeta throughput (quantos frames/segundo)
- Tipo de otimizações necessárias

**Impactos típicos de latência:**

| Tamanho | Latência (GPU) | Latência (CPU) |
|--------|--------|-----------|
| yolov8n (nano) | ~5ms | ~50ms |
| yolov8s (small) | ~10ms | ~100ms |
| yolov8m (medium) | ~20ms | ~200ms |
| yolov8l (large) | ~30ms | ~300ms |

**Resposta da equipe:**
```
[ ] SLA máximo: _______ ms por crop
[ ] Esperado em GPU ou CPU: GPU / CPU / Ambos
[ ] Throughput esperado: _______ crops/segundo
[ ] Pode usar quantização/pruning? Sim / Não / Talvez
```

---

## Dúvidas ALTAS 🟡 (Responder em 2-3 dias)

### Dúvida #4: Volume e Disponibilidade de Datasets

**Pergunta:** Quantas imagens de veículos e faciais existem nos datasets antigos?

**Dataset de Veículos:**
```
[ ] Cores: Quantas imagens por class?
    - Branco: ______
    - Preto: ______
    - Outro: ______
    
[ ] Tipos: Quantas imagens por class?
    - Sedan: ______
    - SUV: ______
    - Outro: ______

[ ] Total estimado: _______ imagens

[ ] Estado: Anotado / Precisa anotação / Parcial
[ ] Formato atual: YOLO / COCO JSON / XML Pascal / Outro
[ ] Path: ________________________
```

**Dataset Facial:**
```
[ ] Total de pessoas: _______ 
[ ] Imagens por pessoa: _______ (média)
[ ] Atributos anotados: Sim / Não / Parcial
[ ] Quais atributos: ________________________
[ ] Path: ________________________
```

---

### Dúvida #5: Marca/Modelo de Carros

**Pergunta:** Há necessidade de classificar marca/modelo ou só cor/tipo?

**Contexto:** Impacta dimensionalidade do problema

```
[ ] Só cores (10 classes)
[ ] Cores + tipos (18 classes)
[ ] Cores + tipos + algumas marcas populares (~50 classes)
[ ] Cores + tipos + muitas marcas (>100 classes - muito desafiador)

Se incluir marcas, quais?
[ ] Top 5: ________________________
[ ] Top 10: ________________________
[ ] Top 20: ________________________
[ ] Todas: ________________________

Volume de dados disponível por marca?
- Marca A: _______ imagens
- Marca B: _______ imagens
- Outra: _______ imagens
```

---

### Dúvida #6: Qualidade de Anotação

**Pergunta:** Qual é o limiar de acordo entre anotadores (inter-annotator agreement)?

**Métrica:** Cohen's Kappa ou Fleiss' Kappa

- 0.81-1.00: Excellent
- 0.61-0.80: Substantial
- 0.41-0.60: Moderate
- 0.21-0.40: Fair
- <0.20: Poor

```
[ ] Qual deve ser limiar mínimo? _______

[ ] Como validar:
    [ ] Amostras anotadas por múltiplos anotadores (N=?)
    [ ] Calcular kappa entre pares
    [ ] Manter dados com kappa > limiar

[ ] Quem decidirá discrepâncias: ______________________
```

---

## Dúvidas MÉDIAS 🟢 (Responder na sequência)

### Dúvida #7: Escolha de Ferramenta

**Pergunta:** MLflow ou Weights & Biases?

```
Critérios:

[ ] Self-hosted (MLflow) 
    Vantagens: Controle total, sem cloudvendor lock-in
    Desvantagens: Setup/manutenção própria
    
[ ] Cloud (W&B)
    Vantagens: Sem setup, melhor UX, colaboração
    Desvantagens: Requer account cloud, restrições networking

Recomendação da equipe:
[ ] MLflow (self-hosted)
[ ] W&B (cloud)
[ ] Ambos (para redundância)
[ ] None (continuar com JSON)
```

---

### Dúvida #8: Estratégia Multi-Atributo

**Pergunta:** Para veículos, usar Opção A (3 modelos separados) ou Opção B (single model)?

```
OPÇÃO A: Modelos separados
[ ] Modelo cores (10 classes)
[ ] Modelo tipos (8 classes)
[ ] Modelo marcas (variável)
Vantagem: Modular, balanceado, escalável
Desvantagem: Latência +

OPÇÃO B: Single model multi-classe
[ ] Combinações: cores × tipos = 80 classes
Vantagem: Inferência rápida
Desvantagem: Desbalanceado, difícil manter

Recomendação da equipe:
[ ] Opção A (preferida)
[ ] Opção B
[ ] Hybrid (cores separado, tipos+marca juntos)
```

---

## Como Priorizar Respostas

### Semana 1 (HOJE + próximos dias)
**CRÍTICA:**
1. ✅ Dúvida #1: Tamanho de input
2. ✅ Dúvida #2: Pipeline
3. ✅ Dúvida #3: SLA latência

**ALTA:**
4. Dúvida #4: Volume de datasets
5. Dúvida #6: Inter-annotator agreement

### Semana 2
**ALTA:**
- Dúvida #5: Marcas/modelos incluir

**MÉDIA:**
- Dúvida #7: MLflow vs W&B
- Dúvida #8: Multi-atributo

---

## Processo de Decisão

### Passo 1: Documentar Respostas
```bash
# Editar este arquivo e preencher as boxes [ ]
```

### Passo 2: Validar com Equipe
```bash
# Discutir em reunião e obter aprovação
```

### Passo 3: Documentar nas Configs
```yaml
# Atualizar QUICKSTART.md e TEMPLATE_CONFIGS.md
# com decisões finais
```

### Passo 4: Implementar Treinamentos
```bash
# Usar configs atualizadas para treinar modelos
python -c "from ultralytics import YOLO; \
           m = YOLO('yolov8n.pt'); \
           m.train(data='configs/veiculos-cores-v1.yaml')"
```

---

## Modelo de Resposta (Copiar e preencher)

**RESPONDENTE:**  
**DATA:**  
**ASSINATURA:**

```markdown
## Respostas às Dúvidas - Onboarding IA

### Dúvida #1: Tamanho/Formato Input
[Resposta aqui]

### Dúvida #2: Pipeline
[Resposta aqui]

### Dúvida #3: SLA Latência
[Resposta aqui]

### Dúvida #4: Volume Datasets
[Resposta aqui]

### Observações Adicionais
[Notas não solicitadas que podem ser relevantes]
```

---

## Próximas Ações Após Respostas

1. **Atualizar QUICKSTART.md** com decisões
2. **Criar configs finais** em `experimentos/configs/`
3. **Iniciar treinamento piloto** com dataset COCO128
4. **Testar em dados reais** (quando datasets encontrados)
5. **Documentar resultados** em MLflow/JSON

---

**Este documento será atualizado conforme respostas chegarem.**  
**Última atualização:** Abril 6, 2026
