import mlflow
import mlflow.pytorch
from ultralytics import YOLO
import yaml
from datetime import datetime
import os

class MLflowExperimentTracker:
    """Classe para rastrear experimentos com MLflow"""
    
    def __init__(self, experiment_name, tracking_uri="http://localhost:5000"):
        # Configura MLflow
        mlflow.set_tracking_uri(tracking_uri)
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
        
    def log_params_from_yaml(self, yaml_path):
        """Carrega e loga parâmetros de um arquivo YAML"""
        with open(yaml_path, 'r') as f:
            params = yaml.safe_load(f)
        
        # Flatten nested dictionaries
        def flatten_dict(d, parent_key=''):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key).items())
                else:
                    items.append((new_key, v))
            return dict(items)
        
        flat_params = flatten_dict(params)
        mlflow.log_params(flat_params)
        return flat_params
    
    def log_dataset_info(self, dataset_name, dataset_path, classes, split_stats):
        """Loga informações do dataset"""
        mlflow.log_param("dataset_name", dataset_name)
        mlflow.log_param("dataset_path", dataset_path)
        mlflow.log_param("num_classes", len(classes))
        mlflow.log_param("classes", str(classes))
        
        for split, stats in split_stats.items():
            mlflow.log_param(f"{split}_images", stats.get('images', 0))
            mlflow.log_param(f"{split}_objects", stats.get('objects', 0))
    
    def train(self, model_path, data_config, epochs, imgsz, **kwargs):
        """Executa treinamento com logging automático"""
        
        # Inicia um run do MLflow
        with mlflow.start_run(run_name=f"train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            
            # Loga todos os parâmetros
            mlflow.log_params({
                "model_path": model_path,
                "data_config": data_config,
                "epochs": epochs,
                "imgsz": imgsz,
                **kwargs
            })
            
            # Loga informações do sistema
            mlflow.log_param("device", kwargs.get('device', 'cpu'))
            mlflow.log_param("batch_size", kwargs.get('batch', 16))
            
            # Carrega modelo
            model = YOLO(model_path)
            
            # Cria callback para logar métricas durante treinamento
            class MLflowCallback:
                def __init__(self):
                    self.epoch = 0
                
                def on_train_epoch_end(self, trainer):
                    # Loga métricas após cada época
                    if hasattr(trainer, 'metrics'):
                        metrics = trainer.metrics
                        mlflow.log_metrics({
                            "box_loss": metrics.get('box_loss', 0),
                            "cls_loss": metrics.get('cls_loss', 0),
                            "dfl_loss": metrics.get('dfl_loss', 0),
                            "precision": metrics.get('precision', 0),
                            "recall": metrics.get('recall', 0),
                            "mAP50": metrics.get('mAP50', 0),
                            "mAP50-95": metrics.get('mAP50-95', 0)
                        }, step=self.epoch)
                        self.epoch += 1
            
            # Executa treinamento
            results = model.train(
                data=data_config,
                epochs=epochs,
                imgsz=imgsz,
                **kwargs
            )
            
            # Após treino, loga métricas finais
            if hasattr(results, 'results_dict'):
                final_metrics = results.results_dict
                mlflow.log_metrics({f"final_{k}": v for k, v in final_metrics.items()})
            
            # Loga artefatos importantes
            if results.save_dir:
                # Salva gráficos
                for file in os.listdir(results.save_dir):
                    if file.endswith(('.png', '.jpg', '.csv', '.yaml')):
                        mlflow.log_artifact(os.path.join(results.save_dir, file))
                
                # Salva o melhor modelo
                best_model_path = os.path.join(results.save_dir, 'weights', 'best.pt')
                if os.path.exists(best_model_path):
                    mlflow.pytorch.log_model(
                        model.model,
                        artifact_path="model",
                        registered_model_name=f"{self.experiment_name}_model"
                    )
            
            # Loga tags para organização
            mlflow.set_tags({
                "framework": "ultralytics",
                "model_type": "yolov8",
                "status": "completed"
            })
            
            return results

# ===== USO PRÁTICO =====

def main():
    # Inicializa tracker
    tracker = MLflowExperimentTracker(
        experiment_name="veiculos-cor-classificacao",
        tracking_uri="http://localhost:5000"
    )
    
    # Configuração do experimento
    config = {
        "model_path": "yolov8n.pt",
        "data_config": "datasets/veiculos-cor.yaml",
        "epochs": 50,
        "imgsz": 640,
        "batch": 16,
        "device": "cuda",
        "optimizer": "AdamW",
        "lr0": 0.001,
        "augmentation": {
            "mosaic": 1.0,
            "mixup": 0.2
        }
    }
    
    # Informações do dataset
    dataset_info = {
        "dataset_name": "veiculos-cor-v2",
        "dataset_path": "/workspaces/datasets/veiculos",
        "classes": ["branco", "preto", "prata", "cinza", "vermelho", "azul", "outro"],
        "split_stats": {
            "train": {"images": 5000, "objects": 7200},
            "val": {"images": 1000, "objects": 1450}
        }
    }
    
    # Loga informações do dataset
    tracker.log_dataset_info(**dataset_info)
    
    # Executa treinamento
    results = tracker.train(**config)
    
    print(f"✅ Experimento concluído!")
    print(f"📊 Visualize em: http://localhost:5000")

if __name__ == "__main__":
    main()