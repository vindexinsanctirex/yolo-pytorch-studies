#!/usr/bin/env python
"""
Script para análise de datasets YOLO
Explora estrutura, volume e distribuição de classes
"""

import os
import json
from collections import defaultdict, Counter
from pathlib import Path
from PIL import Image
import numpy as np

def analise_dataset_yolo(dataset_path):
    """Analisa um dataset em formato YOLO"""
    
    print(f"\n{'='*70}")
    print(f"ANÁLISE DE DATASET: {dataset_path}")
    print(f"{'='*70}\n")
    
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        print(f"⚠️  Dataset não encontrado em {dataset_path}")
        return None
    
    # Verifica estrutura esperada
    images_dir = dataset_path / "images"
    labels_dir = dataset_path / "labels"
    
    if not images_dir.exists() or not labels_dir.exists():
        print(f"❌ Estrutura inválida. Esperado: images/ e labels/")
        return None
    
    # Coleta informações
    stats = {
        'total_imagens': 0,
        'total_labels': 0,
        'class_distribution': Counter(),
        'resolucoes': [],
        'tamanho_medio_bbox': {'width': [], 'height': []},
        'imagens_por_split': defaultdict(int),
        'labels_por_imagem': defaultdict(int),
    }
    
    # Processa splits (train, val, test)
    for split_dir in images_dir.glob('*'):
        if not split_dir.is_dir():
            continue
        
        split_name = split_dir.name
        print(f"\n📁 Split: {split_name}")
        print("-" * 50)
        
        # Processa imagens
        images = list(split_dir.glob('*.jpg')) + list(split_dir.glob('*.png'))
        num_imagens = len(images)
        stats['total_imagens'] += num_imagens
        stats['imagens_por_split'][split_name] = num_imagens
        
        print(f"  Imagens: {num_imagens}")
        
        for img_path in images:
            # Coleta resolução
            try:
                img = Image.open(img_path)
                stats['resolucoes'].append(img.size)
            except Exception as e:
                print(f"  ⚠️  Erro ao ler {img_path}: {e}")
            
            # Processa labels
            label_path = labels_dir / split_name / img_path.stem
            if label_path.with_suffix('.txt').exists():
                with open(label_path.with_suffix('.txt'), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            class_id = int(parts[0])
                            stats['class_distribution'][class_id] += 1
                            stats['tamanho_medio_bbox']['width'].append(float(parts[3]))
                            stats['tamanho_medio_bbox']['height'].append(float(parts[4]))
                    
                    stats['labels_por_imagem'][split_name] += len(lines)
        
        stats['total_labels'] += stats['labels_por_imagem'][split_name]
    
    # Calcula estatísticas
    print(f"\n📊 RESUMO GERAL")
    print("-" * 50)
    print(f"  Total de imagens: {stats['total_imagens']}")
    print(f"  Total de objetos (labels): {stats['total_labels']}")
    
    if stats['total_imagens'] > 0:
        print(f"  Objetos por imagem (média): {stats['total_labels'] / stats['total_imagens']:.2f}")
    
    # Distribuição por split
    if stats['imagens_por_split']:
        print(f"\n📈 Distribuição por split:")
        for split, count in stats['imagens_por_split'].items():
            pct = (count / stats['total_imagens'] * 100) if stats['total_imagens'] > 0 else 0
            print(f"  - {split}: {count} imagens ({pct:.1f}%)")
    
    # Distribuição de classes
    if stats['class_distribution']:
        print(f"\n🏷️  Distribuição de classes:")
        total_objetos = sum(stats['class_distribution'].values())
        for class_id in sorted(stats['class_distribution'].keys()):
            count = stats['class_distribution'][class_id]
            pct = (count / total_objetos * 100) if total_objetos > 0 else 0
            print(f"  - Classe {class_id}: {count} objetos ({pct:.1f}%)")
    
    # Resoluções
    if stats['resolucoes']:
        resolutions = np.array(stats['resolucoes'])
        print(f"\n📐 Resoluções:")
        print(f"  - Mínima: {resolutions.min(axis=0)}")
        print(f"  - Máxima: {resolutions.max(axis=0)}")
        print(f"  - Média: {resolutions.mean(axis=0)}")
    
    # Tamanho de bboxes
    if stats['tamanho_medio_bbox']['width']:
        widths = np.array(stats['tamanho_medio_bbox']['width'])
        heights = np.array(stats['tamanho_medio_bbox']['height'])
        print(f"\n📦 Tamanho médio de bounding boxes (normalizado):")
        print(f"  - Largura: {widths.mean():.4f} (min: {widths.min():.4f}, max: {widths.max():.4f})")
        print(f"  - Altura: {heights.mean():.4f} (min: {heights.min():.4f}, max: {heights.max():.4f})")
    
    return stats


def main():
    datasets = [
        "/workspaces/yolo-pytorch-studies/datasets/coco128",
    ]
    
    # Verifica se dataset de veículos existe
    veiculos_path = "/workspaces/datasets/veiculos"
    if Path(veiculos_path).exists():
        datasets.append(veiculos_path)
    
    print("\n" + "="*70)
    print("EXPLORAÇÃO DE DATASETS - YOLO PYTORCH STUDIES")
    print("="*70)
    
    for dataset in datasets:
        analise_dataset_yolo(dataset)
    
    print("\n" + "="*70)
    print("Análise concluída!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
