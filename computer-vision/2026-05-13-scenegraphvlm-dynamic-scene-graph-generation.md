# SceneGraphVLM: Dynamic Scene Graph Generation from Video with Vision-Language Models

**ArXiv ID:** 2605.13667  
**Submitted:** May 13, 2026  
**Authors:** Vladislav Makarov, Mark Gizetdinov, Dmitry Yudin  
**Institutions:** Skoltech, Yandex Research

## Executive Summary

SceneGraphVLM introduces an efficient method for generating structured scene representations (scene graphs) from videos using compact vision-language models, achieving quality comparable to large models while maintaining ~1-second latency per frame. By serializing scene graphs in a token-efficient TOON (Tree-to-Object-Object-Node) format and employing two-stage training with hallucination-aware rewards, SceneGraphVLM demonstrates that small VLMs can generate accurate scene graphs with approximately one-second latency, enabling real-time scene understanding in resource-constrained environments while maintaining high precision and recall.

## Problem Statement

### Problem Addressed
Scene graphs provide compact, structured representations of visual scenes:
- **Objects:** Entities in the scene (person, car, tree)
- **Relationships:** Spatial/semantic connections (person riding bike, sitting on bench)
- **Attributes:** Properties of objects (red car, large tree)

However, existing scene graph generation methods suffer from:
- **Slow inference:** Large models require 5-10 seconds per frame
- **Hallucination:** Models generate objects/relations not present in visual input
- **Limited video understanding:** Most work focuses on single images, not temporal dynamics
- **Memory overhead:** Large models difficult to deploy on edge devices

### Prior Limitations
Previous approaches to scene graph generation:

1. **Graph Neural Networks:** Fast but require explicit feature extraction, limited context understanding

2. **Vision-Language Models (Large):** Strong understanding but too slow (5-10s/frame) for video processing

3. **Object Detection + Relation Prediction:** Modular approaches suffer from cascading errors

4. **Single-Image Methods:** Cannot leverage temporal information across video frames

### Research Gap
The gap exists between **speed** (required for video) and **quality** (required for accurate scene understanding). No existing method achieves both efficient inference AND accurate scene graph generation with small models.

## Core Concepts & Theory

### Fundamental Concepts

#### 1. Scene Graphs as Structured Representations

A scene graph is a directed graph: **G = (O, R, A)** where:
- **O:** Set of object nodes {o₁, o₂, ..., oₙ}
- **R:** Set of directed edges representing relationships {(oᵢ, predicate, oⱼ)}
- **A:** Attributes assigned to each object {(o, attribute, value)}

**Example:**
```
Image: Person sitting on bench in park

Scene Graph:
    person ─── sitting_on ──→ bench
      │                          │
      └─── in ──────────────────┘
      
Attributes:
- person: [age="adult", pose="sitting"]
- bench: [material="wood", color="brown"]
```

#### 2. Token-Efficient Serialization (TOON Format)

Convert graph structure to token sequence efficiently:

```
TOON Format:
<object person> <attr age=adult> <relation sitting_on>
<object bench> <attr material=wood> <relation in>
<object park> </object>
```

Standard token-per-object: 20-30 tokens
TOON token-per-object: 3-4 tokens
**Compression ratio: 6-10x**

#### 3. Hallucination in Vision Models

Models tend to generate plausible but unsupported content:

```
Image: Car on street

Hallucination Types:
- Object hallucination: Invents "pedestrian" not in image
- Relation hallucination: Creates "car parked_by building" when building not visible
- Attribute hallucination: Assigns "red" to grayscale car
```

Hallucination-aware reward penalizes unsupported predictions.

### Mathematical Framework

#### Two-Stage Training Pipeline

**Stage 1: Supervised Fine-Tuning (SFT)**

```
Input: I_t (frame t) or (I_t-1, I_t) (temporal context)
Model: VLM with LoRA adapters
Output: Scene graph in TOON format

Loss_SFT = -∑_t log P(graph_t | image_t; θ)
```

Maps raw visual input to TOON tokens using supervised examples.

**Stage 2: Reinforcement Learning with Hallucination-Aware Rewards**

```
Objective: maximize E_τ[R(τ)]

where τ is a trajectory (scene graph) and reward combines:

R(τ) = w₁ × R_recall(τ)      # Penalize missing objects/relations
     + w₂ × R_precision(τ)    # Penalize hallucinated predictions
     + w₃ × R_coverage(τ)     # Encourage complete scene understanding
     - w₄ × R_hallucination(τ) # Heavy penalty for unsupported content
```

**Hallucination Penalty:**
```
R_hallucination(τ) = ∑_{o,r ∈ τ} (1 - confidence(o,r|I))
```

Objects/relations must be grounded in visual evidence; low-confidence predictions are penalized.

#### Temporal Consistency for Videos

For video processing, add temporal reward:

```
R_temporal(τ_t) = similarity(graph_t, graph_t-1)
                × (1 - large_scene_changes)
```

Encourages smooth transitions unless scene changes significantly.

### Comparison with Existing Approaches

| Approach | Model Size | Latency/Frame | Accuracy | Hallucination |
|----------|---|---|---|---|
| Faster R-CNN + GCN | Large | 0.3s | 65% | High |
| Full VLM (Qwen14B) | Large | 8s | 85% | Medium |
| SceneGraphVLM (0.8B) | **Small** | **0.9s** | **82%** | **Low** |
| SceneGraphVLM (3.5B) | Small-Med | 1.5s | 84% | Low |

## Main Ideas & Contributions

### Novel Techniques

#### 1. Token-Efficient TOON Serialization

Instead of generating free-form text, serialize scene graphs as structured tokens:

```python
# Standard Text Output (verbose, inefficient)
"In the image, there is a person sitting on a bench. 
The person is in a park. The bench is made of wood..."

# TOON Format (compact, structured)
<obj person> <attr young> <rel sitting_on> 
<obj bench> <attr wood> <rel in> 
<obj park> </obj>
```

Benefits:
- **Compression:** 6-10x fewer tokens
- **Consistency:** Structured format reduces freeform variations
- **Parseability:** Direct conversion to graph structure

#### 2. Hallucination-Aware Reward Function

Standard RL rewards don't penalize hallucination explicitly. GRAM introduces:

```python
def hallucination_penalty(predicted_graph, image):
    penalty = 0
    for obj in predicted_graph.objects:
        if not visually_grounded(obj, image):
            penalty += 1.0  # Heavy penalty
        elif low_confidence(obj, image):
            penalty += 0.5  # Medium penalty
    
    for rel in predicted_graph.relations:
        if both_objects_absent(rel, image):
            penalty += 1.0
    
    return penalty
```

Combines detection confidence scores with visual grounding verification.

#### 3. Temporal Context Integration

For videos, optionally condition each frame on previous graph:

```python
# Without temporal context
graph_t = model(image_t)

# With temporal context
graph_t = model(image_t, prev_graph=graph_t-1)
```

Uses prior predictions as lightweight context without explicit tracking.

### Technical Contributions

1. **Compact Graph Representation:** TOON format reduces token overhead from ~30 to ~3-4 per object

2. **Calibrated Reward Design:** Balances coverage (recall) with precision, explicitly penalizing hallucinations

3. **Video Scene Graph Dataset:** Evaluation on video scene graphs (temporal dynamics) not just images

## Methodology & Implementation

### Architecture Overview

```
Input Frame(s)
       ↓
[Vision Encoder]
    ViT backbone
       ↓
[Compact VLM]
Qwen VLM 0.8B or 3.5B
with LoRA adapters
       ↓
[TOON Decoder]
Generates tokenized scene graph
       ↓
Output: Scene Graph
<obj person> <attr age=adult> <rel sitting_on> ...
```

### Implementation Details

#### Model Architecture
- **Vision Encoder:** ViT-B/32 (frozen weights from original VLM)
- **Language Model:** Qwen-0.8B or Qwen-3.5B
- **Adapter:** LoRA adapters in language model layers (rank=8)
- **Decoder:** TOON token vocabulary (200 object types, 50 relation types)

#### Training Configuration

**Stage 1: Supervised Fine-Tuning**
```python
config_sft = {
    'learning_rate': 2e-4,
    'batch_size': 64,
    'epochs': 3,
    'warmup_steps': 1000,
    'max_grad_norm': 1.0,
    'optimizer': 'AdamW'
}
```

**Stage 2: RL Fine-Tuning**
```python
config_rl = {
    'learning_rate': 1e-5,  # Lower LR for RL
    'batch_size': 32,
    'ppo_epochs': 4,
    'gamma': 0.99,  # Discount factor
    'lambda': 0.95,  # GAE parameter
    'reward_weights': {
        'recall': 1.0,
        'precision': 1.0,
        'coverage': 0.5,
        'hallucination': -2.0  # Strong penalty
    }
}
```

### Experimental Setup

#### Datasets
1. **PSG (Pan-Product Scene Graph):** 150k images with scene graphs
2. **PVSG (Panoptic Video Scene Graph):** 400 videos with temporal annotations
3. **Action Genome:** 10k videos with detailed spatio-temporal scene graphs

#### Evaluation Metrics

**Graph-Level Metrics:**
- **Recall@K:** % of true objects/relations in top-K predictions
- **Precision@K:** % of predicted objects/relations that are correct
- **F1 Score:** Harmonic mean of precision/recall

**Hallucination Metrics:**
- **Hallucination Rate:** % of generated elements not in ground truth
- **Confidence Calibration:** Alignment between model confidence and accuracy

**Timing:**
- **Latency per frame:** Wall-clock time to generate graph
- **FPS:** Frames per second in video mode

#### Baselines Compared
1. Faster R-CNN + Graph Convolution Network (GCN)
2. Full VLM (Qwen-14B)
3. SceneGraphVLM (0.8B)
4. SceneGraphVLM (3.5B)

### Results

#### Image Scene Graph Generation (PSG Dataset)

| Model | Size | Recall@50 | Precision@50 | F1 | Latency |
|-------|------|----------|-------------|-----|---------|
| Faster R-CNN + GCN | Large | 68.2% | 61.4% | 64.6% | 0.3s |
| Qwen-14B (baseline) | 14B | 82.3% | 78.9% | 80.5% | 8.2s |
| SceneGraphVLM | 0.8B | 78.1% | 79.2% | **78.6%** | **0.9s** |
| SceneGraphVLM-Large | 3.5B | 81.6% | 80.4% | **81.0%** | 1.5s |

**Key Finding:** SceneGraphVLM-0.8B achieves 98% of full VLM quality at 9x faster inference.

#### Video Scene Graph Generation (PVSG Dataset)

| Model | F1 Score | Hallucination Rate | Temporal Consistency |
|-------|----------|---|---|
| Single-Frame SG × frames | 76.2% | 18.4% | N/A |
| Qwen-14B | 77.8% | 15.2% | 0.72 |
| SceneGraphVLM (temporal) | **79.3%** | **8.1%** | **0.85** |

**Key Finding:** Temporal conditioning reduces hallucination rate by half while improving temporal consistency.

#### Ablation Study

| Component | F1 Score | Hallucination |
|-----------|----------|---|
| SFT only (no RL) | 76.4% | 14.2% |
| + Standard RL reward | 77.9% | 11.3% |
| + Hallucination penalty | **79.3%** | **8.1%** |
| + Temporal conditioning | 79.8% | 7.9% |

Hallucination penalty accounts for 4-5% absolute improvement in F1.

## Practical Applications & Use Cases

### Applicable Domains

1. **Video Understanding & Indexing**
   - Real-world: YouTube, TikTok content recommendation
   - Challenge: Process billions of video hours efficiently
   - Solution: SceneGraphVLM enables structured understanding on edge devices

2. **Autonomous Driving**
   - Real-world: Real-time scene understanding for decision making
   - Challenge: 1-2s latency requirement for safety-critical decisions
   - Solution: 0.9s per frame enables integration into driving pipeline

3. **Robotics & Embodied AI**
   - Real-world: Mobile robots navigating complex environments
   - Challenge: Limited compute; need scene understanding for navigation
   - Solution: Small model size allows on-robot inference

4. **Smart Surveillance & Security**
   - Real-world: Real-time monitoring of public spaces
   - Challenge: Privacy concerns, cost of human monitoring
   - Solution: Efficient video understanding for anomaly detection

5. **Content Moderation**
   - Real-world: Platforms need rapid content classification
   - Challenge: Screen enormous volumes of video
   - Solution: Fast, structured representations enable content classification

### Concrete Examples

**Example 1: Autonomous Driving**
```
Input: Dashcam video frame
SceneGraphVLM output:
  Objects: [car, pedestrian, traffic_light, road]
  Relations: 
    - pedestrian crossing_near car
    - traffic_light above road
    - car approaching traffic_light
  
Decision: Brake predicted due to pedestrian crossing_near
Processing time: 0.8s → Safe for real-time driving
```

**Example 2: Smart Home Monitoring**
```
Input: Security camera feed
SceneGraphVLM output:
  Objects: [person, backpack, window]
  Relations:
    - person near window
    - backpack in_hand person
    - window open
  
Alerts: Potential break-in (person near open window)
Edge execution: Runs on home hub device, no cloud needed
```

**Example 3: Video Content Search**
```
Query: "Find videos where person is sitting on bench"
SceneGraphVLM processes video library:
  - Generates scene graphs for all videos
  - Indexes objects and relationships
  - Query matches videos with sitting_on(person, bench)
  
Result: Fast retrieval across large video collection
```

## Insights & Implications

### Broader Field Impact

1. **Efficient Multimodal Understanding:** Demonstrates that compact VLMs can achieve near-SOTA performance on structured understanding tasks

2. **Edge AI Deployment:** Makes sophisticated scene understanding feasible on mobile/embedded devices

3. **Structured Output from VLMs:** TOON serialization provides a template for other structured tasks (knowledge graphs, entity relations, etc.)

### State-of-the-Art Advancement

SceneGraphVLM achieves several notable results:
- **Fastest accurate scene graph generation:** 0.9s/frame (competitive with 2020 fast methods, with better accuracy)
- **Highest accuracy on video scene graphs:** 79.3% F1 on PVSG (first VLM-based approach to exceed GCN baselines on video)
- **Lowest hallucination rate:** 8.1% (state-of-the-art, vs. 15% for full VLMs)

### Limitations and Open Questions

1. **Object Type Coverage:** Limited to 200 object categories; extension to open-vocabulary detection is needed

2. **Fine-Grained Relationships:** Struggles with abstract relationships (metaphorical, counterfactual); focus is on observable spatial relations

3. **Multi-Scale Understanding:** Less effective on scenes with large spatial variation (aerial views, panoramas)

4. **Temporal Reasoning:** Current temporal model is simple (previous frame conditioning); deeper temporal modeling could help

5. **Zero-Shot Transfer:** Limited evaluation on out-of-distribution scenes; generalization to new environments unclear

## Code & Resources

### Official Repository
- **Paper:** https://arxiv.org/abs/2605.13667
- **Code:** Available upon request (authors working on release)
- **Project Website:** https://github.com/vllab/SceneGraphVLM (expected June 2026)

### Dependencies
- Python 3.10+
- PyTorch 2.0+
- HuggingFace Transformers
- Qwen VLM (0.8B or 3.5B)
- LoRA library for efficient fine-tuning

### Compute Requirements
- **Training:** 1× GPU (A100) for full fine-tuning, 8× GPUs for RL stage
- **Inference:** CPU inference possible with quantization; GPU recommended for real-time
- **Memory:** 4-8GB for inference with 0.8B model, 16GB for 3.5B model
- **Latency:** ~0.9s per 1080p frame on V100, ~0.5s on A100

### Quick Start

```python
from scenegraphvlm import SceneGraphVLM

# Load pre-trained model
model = SceneGraphVLM.from_pretrained(
    "scenegraphvlm-0.8b-finetuned"
)

# Single image inference
from PIL import Image
image = Image.open("scene.jpg")
graph = model.generate(image)

print("Objects:", graph.objects)
print("Relations:", graph.relations)

# Video inference with temporal conditioning
import cv2
cap = cv2.VideoCapture("video.mp4")
prev_graph = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Generate graph with temporal context
    graph = model.generate(
        frame, 
        prev_graph=prev_graph,
        use_temporal=True
    )
    
    print(f"Frame: {graph}")
    prev_graph = graph
```

### Visualization

```python
# Visualize scene graph
from scenegraphvlm import visualize_graph

graph_image = visualize_graph(
    image,
    graph,
    show_attributes=True,
    highlight_hallucinations=True
)

graph_image.save("scene_graph_viz.png")
```

## Related Work & Context

### Prior Work Foundations

1. **Scene Graph Generation:** Earlier work (Johnson et al., 2015)
   - SGVLM advance: Uses VLMs for joint object detection and relationship understanding

2. **Vision-Language Models:** CLIP, ALBEF, Qwen
   - Contribution: Applies VLMs to structured graph generation, not just classification

3. **Efficient Transformers:** LoRA, adapters, quantization
   - Usage: Enables small model fine-tuning without full model updates

### Recent Related Papers

- "GraphVLM: Benchmarking Vision Language Models for Multimodal Graph Learning" (2603.13370)
- "Scene Graphs from Images with Vision-Language Models" (2404.xxxxx): Earlier VLM work
- "Fast Scene Understanding with Generative Models" (2502.xxxxx): Concurrent work on efficient generation

### Future Research Directions

1. **Open-Vocabulary Scene Graphs:** Support arbitrary object types and relationships (not limited to 200 categories)

2. **3D Scene Graphs:** Extend from 2D to 3D scene understanding for robotics applications

3. **Temporal Reasoning:** Deeper modeling of object interactions and state changes across time

4. **Interactive Scene Graphs:** Generate graphs conditioned on queries ("what does person see?", "where can person sit?")

5. **Uncertainty Quantification:** Estimate confidence in generated graphs for safety-critical applications

---

**Paper Link:** https://arxiv.org/abs/2605.13667
