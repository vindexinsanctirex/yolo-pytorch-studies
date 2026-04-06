# 🆘 Troubleshooting & FAQ - Onboarding IA

**Objetivo:** Resolver problemas comuns durante o onboarding  
**Tempo de consulta:** 5-15 minutos  

---

## 🔴 Problemas Críticos

### ❌ "ModuleNotFoundError: No module named 'ultralytics'"

**Causa:** Ambiente não ativado ou Ultralytics não instalado

**Solução:**
```bash
# 1. Ativar venv
source /workspaces/yolo-pytorch-studies/.venv/bin/activate

# 2. Verificar se está ativado (deve mostra .venv no prompt)
which python  # Deve mostrar .venv/bin/python

# 3. Instalar se necessário
pip install ultralytics opencv-python

# 4. Verificar
python -c "from ultralytics import YOLO; print('OK')"
```

**Se persistir:** Executar `configure_python_environment` novamente

---

### ❌ "FileNotFoundError: [Errno 2] No such file or directory"

**Causa:** Path para dataset ou modelo não encontrado

**Solução:**
```bash
# 1. Verificar se caminho existe
ls -la /workspaces/yolo-pytorch-studies/datasets/coco128/

# 2. Se não existe, checar paths alternativos
find /workspaces -name "coco128" -type d

# 3. Se dataset não encontrado, documentar em DECISION_LOG.md
```

---

### ❌ "RuntimeError: CUDA out of memory"

**Causa:** GPU não tem memória suficiente

**Solução:**
```python
# No notebook ou script, mudar para CPU:
model = YOLO("yolov8n.pt")
results = model.train(data="coco128.yaml", device="cpu")  # ← Usar CPU

# Ou, reduzir batch size:
results = model.train(data="coco128.yaml", batch=8, device="cuda")  # ← Menor batch
```

**Alternativa:** Usar modelo menor:
```python
model = YOLO("yolov8n.pt")  # nano (melhor para GPU pequena)
# Não usar: yolov8m.pt, yolov8l.pt (muito grandes)
```

---

### ❌ "Permission denied: '.venv/bin/python'"

**Causa:** Permissões de arquivo

**Solução:**
```bash
# Dar permissão de execução
chmod +x /workspaces/yolo-pytorch-studies/.venv/bin/python

# Ou usar explicitamente
python /caminho/para/script.py  # Python já deve estar no path
```

---

## 🟡 Problemas Comuns

### ⚠️ "Notebook não abre no VS Code"

**Causa:** Jupyter não instalado ou não configurado

**Solução:**
1. [ ] Instalar: `pip install jupyter`
2. [ ] Abrir VS Code Jupyter Extension (deve aparecer ao clicar em .ipynb)
3. [ ] Selecionar kernel: Python 3.12 (ou versão em venv)
4. [ ] Executar primeira célula
5. [ ] Se erro, reiniciar VS Code

**Alternativa - Terminal:**
```bash
jupyter notebook onboarding_ia.ipynb
# Vai abrir em http://localhost:8888
```

---

### ⚠️ "Inferência está muito lenta"

**Causa:** Usando CPU ou modelo grande

**Passo 1 - Verificar device:**
```python
print(torch.cuda.is_available())  # Deve ser True se tiver GPU

# No script
model.train(device="cuda")  # Forçar GPU
```

**Passo 2 - Usar modelo menor:**
```python
model = YOLO("yolov8n.pt")  # nano = mais rápido
# Evitar: yolov8m.pt, yolov8l.pt
```

**Passo 3 - Reduzir imgsz:**
```python
model.train(imgsz=224)  # Menor que 640 = mais rápido
```

---

### ⚠️ "Dataset não encontrado"

**Sintoma:** `FileNotFoundError` ao tentar treinar

**Diagnóstico:**
```bash
# Verificar onde está
ls -la /workspaces/datasets/  # Listar datasets

# Procurar por padrão
find /workspaces -name "*coco*" -o -name "*veic*" -o -name "*facial*"
```

**Solução:**
1. [ ] Confirmar path exato no terminal
2. [ ] Atualizar YAML config com path correto
3. [ ] Testar com script: `python scripts/analise_datasets.py`

---

### ⚠️ "Erro ao ler imagem (PIL/OpenCV)"

**Sintoma:** `IOError` ao abrir JPG/PNG

**Causa:** Arquivo corrompido ou formato invalido

**Solução:**
```bash
# Verificar integridade de imagens
for f in datasets/coco128/images/train2017/*.jpg; do
  python -c "from PIL import Image; Image.open('$f')"
done

# Se erro em arquivo específico, deletar e re-baixar
rm datasets/coco128/images/train2017/000000000009.jpg
```

---

### ⚠️ "Config YAML syntax error"

**Sintoma:** `yaml.YAMLError` ao carregar config

**Causa:** Indentação errada ou caracteres inválidos

**Solução:**
```bash
# Validar YAML
python -c "import yaml; yaml.safe_load(open('experimentos/configs/veiculos-cor-v1.yaml'))"

# Se erro, revisar:
# - Espaços vs tabs (usar only espaços)
# - Quotes em strings com caracteres especiais
# - Indentação consistente (2 ou 4 espaços por nível)
```

**Exemplo correto:**
```yaml
dataset:
  name: "veiculos"  # String com quotes
  path: "/workspaces/datasets/veiculos"
  classes:
    - branco    # Nested list, nice indentation
    - preto
```

---

## 🟢 FAQ

### P: Posso treinar com COCO128 agora ou preciso esperar?

**R:** Pode treinar! COCO128 é excelente para validar o pipeline. Quando obtiver dados reais, retreine.

```python
# Teste rápido (3 épocas)
model = YOLO("yolov8n.pt")
results = model.train(data="coco128.yaml", epochs=3, device="cuda")
```

---

### P: Qual é o tempo estimado para treinar?

**R:** Depende de: **modelo + hardware + dataset + épocas**

| Cenário | Tempo Estimado |
|---------|--------|
| COCO128, nano, 3 epochs, GPU | 5-10 min |
| COCO128, nano, 100 epochs, GPU | 2-3h |
| Veículos cores, nano, 100 epochs, GPU | 1-2h |
| YOLO detect (full train), GPU | 24h+ |
| Qualquer coisa, CPU only | 10x mais lento |

---

### P: Como salvo o modelo treinado?

**R:** Ultralytics salva automaticamente em `runs/detect/train/weights/`

```python
results = model.train(...)

# Modelo melhor:
best_model = results.save_dir / "weights" / "best.pt"

# Modelo arquivo
last_model = results.save_dir / "weights" / "last.pt"

# Usar modelo salvo depois:
model = YOLO("runs/detect/train/weights/best.pt")
```

---

### P: Como faço export do modelo?

**R:** Use `export()` método

```python
model = YOLO("best.pt")  # Seu modelo treinado

# Para ONNX (universal)
model.export(format="onnx")

# Para TensorRT (GPU NVIDIA)
model.export(format="engine", device=0)

# Para outros formatos
model.export(format="torchscript")  # .torchscript
model.export(format="pb")            # TensorFlow
model.export(format="tflite")        # Mobile
```

---

### P: O que é desbalanceamento de dados?

**R:** Quando uma classe tem muito mais exemplos que outras.

**Exemplo:**
```
Barba dataset:
- sem_barba: 8000 imagens (80%)  ← Dominante
- com_barba: 2000 imagens (20%)

Problema: Modelo aprende a prever "sem_barba" todo o tempo
Solução: Oversampling ou class weights
```

---

### P: Como balancear dataset?

**R:** Três técnicas

```python
# 1. Class Weights (no YAML)
model.train(data="config.yaml", class_weights=True)

# 2. Oversampling (mais imagens da classe rara)
from imblearn.over_sampling import RandomOverSampler
# ... usar em pré-processamento

# 3. Data Augmentation (transformar imagens)
# - Já feito pela Ultralytics automaticamente
```

---

### P: Como monitoro treinamento?

**R:** Usar MLflow (recomendado) ou loss plots do Ultralytics

```python
# Automático - Ultralytics cria plots
model.train(...)
# Gera: runs/detect/train/results.png

# Com MLflow
import mlflow
mlflow.set_experiment("meu-treino")
with mlflow.start_run():
    model.train(...)
    mlflow.log_artifact("runs/detect/train/results.png")
```

---

## 📋 Tabela de Troubleshooting Rápida

| Erro | Causa Provável | Fix |
|------|--------|-----|
| ModuleNotFoundError | Venv não ativada | `source .venv/bin/activate` |
| FileNotFoundError | Path inválido | `find /workspaces -name dataset` |
| CUDA out of memory | GPU pequena | Usar `device="cpu"` ou batch menor |
| Slow training | GPU não sendo usada | Verificar `torch.cuda.is_available()` |
| Imagem não abre | Arquivo corrompido | Deletar e re-download |
| YAML error | Indentação errada | Validar com `yaml.safe_load()` |
| Modelo não converge | Learning rate errado | Tentar `lr0=0.001` → `0.0001` |

---

## 🔧 Dicas de Debug

### Debug Tip 1: Sempre imprimir versões

```python
import torch
import ultralytics
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Ultralytics: {ultralytics.__version__}")
```

### Debug Tip 2: Verificar device

```python
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
```

### Debug Tip 3: Validar dataset antes de treinar

```bash
python scripts/analise_datasets.py
# Isso mostra todos os problemas potenciais
```

### Debug Tip 4: Teste com dataset pequeno

```python
# Antes de 100 epochs, tente com 3
model.train(epochs=3, batch=4)  # Teste rápido
# Se OK, scale up: epochs=100, batch=32
```

---

## 📞 Quando Pedir Ajuda

**Você NÃO pode resolver = Pergunte a:**

| Problema | Quem Perguntar |
|----------|--------|
| Dados/Dataset missing | Data Team / PM |
| Hardware/GPU issues | DevOps / Tech Lead |
| Decisão de arquitetura | Tech Lead / Architect |
| Timeout de servidor | DevOps |
| Dúvidas sobre produção | Architecture Lead |

---

## 🔗 Referências Úteis

- **Ultralytics Docs:** https://docs.ultralytics.com/guides/
- **PyTorch Docs:** https://pytorch.org/docs/stable/
- **YAML Validator:** https://www.yamllint.com
- **GitHub Issues:** https://github.com/ultralytics/yolov5/issues

---

## 📝 Como Reportar Bugs

Se encontrar um problema genuíno:

```markdown
**Title:** [Descrição breve]

**Reprodução:**
1. Step 1
2. Step 2
3. Step 3

**Expected:** O que deveria acontecer
**Actual:** O que está acontecendo

**Environment:**
- Python version: 3.12
- Ultralytics version: X.X.X
- GPU: yes/no
- OS: Linux/Mac/Windows

**Logs/Errors:**
[Paste stack trace]
```

---

**Última atualização:** Abril 6, 2026  
**Se não encontrou resposta:** Documentar em DECISION_LOG.md para próxima reunião
