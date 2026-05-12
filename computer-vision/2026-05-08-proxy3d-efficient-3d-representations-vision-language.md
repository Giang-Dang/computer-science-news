# Proxy3D: Efficient 3D Representations for Vision-Language Models via Semantic Clustering and Alignment

**ArXiv ID**: 2605.08064  
**Authors**: Jerry Jiang, Haowen Sun, Denis Gudovskiy, Yohei Nakata, Tomoyuki Okuno, Kurt Keutzer, Wenzhao Zheng  
**Submission Date**: May 8, 2026  
**Conference**: CVPR 2026 (Accepted)  
**Institutions**: UC Berkeley, Sony AI, University of Tokyo

---

## Executive Summary

Proxy3D introduces an innovative approach to bridging the gap between 3D scene understanding and vision-language models by proposing efficient 3D representations specifically designed for VLMs. Rather than directly processing complex 3D data, the paper leverages semantic clustering and alignment to create compact, language-aligned proxies of 3D scenes. This work represents a significant step toward practical 3D-aware multimodal understanding, enabling VLMs to reason about spatial geometry, object relationships, and 3D structure without requiring expensive 3D encoders. The method achieves strong performance on 3D reasoning tasks while maintaining computational efficiency, making it highly applicable to robotics, autonomous systems, and immersive computing.

---

## Problem Statement

### The Challenge

Modern Vision-Language Models (VLMs) excel at 2D visual understanding and language grounding, but struggle with **3D spatial reasoning**:
- VLMs process only 2D projections of 3D scenes
- Loss of depth, occlusion, and spatial structure information
- Cannot understand object relationships in 3D space
- Limited applications in robotics, autonomous driving, AR/VR

### Prior Limitations

Previous approaches to 3D understanding have faced trade-offs:

1. **3D Encoder Methods**
   - Require separate 3D backbone networks (expensive)
   - Difficult to integrate with pre-trained VLMs
   - Slow inference due to 3D processing overhead

2. **Multi-View Methods**
   - Process multiple 2D views and fuse features
   - High computational cost (3× to 6× increase)
   - Difficult to align with language tokens

3. **Scene Graph/Symbolic Approaches**
   - Require explicit 3D annotations
   - Cannot handle novel scene types
   - Break end-to-end differentiability

### Research Gap

**Core Gap**: How to encode 3D information into language-aligned representations without expensive 3D computation?

The missing insight: 3D structure can be efficiently represented through semantic clustering—grouping semantically similar features in 3D space—and aligning these clusters with language semantics.

---

## Core Concepts & Theory

### Fundamental Concepts

#### Vision-Language Models (VLMs)
VLMs like CLIP align visual and textual representations in a shared embedding space:
- **Visual Encoder**: Processes images → visual tokens
- **Language Encoder**: Processes text → language tokens
- **Alignment**: Learned similarity in shared space

**Limitation**: Operates on 2D images, ignores depth

#### 3D Scene Representation
3D scenes contain:
- **Geometry**: Depth, surface normals, volume
- **Semantics**: Object labels, material properties
- **Structure**: Spatial relationships, occlusions

**Challenge**: Cannot be directly embedded into 2D VLM latent spaces

#### Semantic Clustering in 3D
The key innovation: Create proxy representations by clustering semantically coherent 3D regions:

**Clustering Criterion**:
```
Groups 3D points/regions by:
1. Semantic similarity (what object is it?)
2. Spatial proximity (how close is it?)
3. Visual appearance (what does it look like?)
```

**Result**: Compact set of cluster proxies representing the scene

### Mathematical Foundations

#### Proxy Generation Algorithm

**Step 1: Feature Extraction**
```
Given: 3D scene S = {p_1, p_2, ..., p_n} (points or voxels)
Process each point:
  f_i = FeatureNetwork(p_i, color, normal, ...)
  Outputs: semantic features in VLM space
```

**Step 2: Semantic Clustering**
```
Cluster points by semantic similarity:
  C_j = {i | similarity(f_i, f_k) > τ for k ∈ C_j}
  
Using: DBSCAN, K-means, or learned clustering
```

**Step 3: Proxy Computation**
```
For each cluster C_j:
  p_j = Aggregate({f_i : i ∈ C_j})
  
Aggregation: mean, weighted mean, or learned pooling
```

**Step 4: Alignment with VLM**
```
Align proxies with language tokens:
  p_j' = MLPAlign(p_j)  # Project to VLM space
  
Loss: Contrastive loss with language embeddings
  L = -log(exp(sim(p', t) / τ) / Σ exp(sim(p', t') / τ))
```

### Methodology Comparison

| Aspect | Direct 3D Encoder | Multi-View Fusion | Proxy3D |
|--------|---|---|---|
| **Computational Cost** | High (3D conv ops) | 3-6× 2D cost | ~1.2× 2D cost |
| **VLM Integration** | Difficult | Medium | Seamless |
| **Language Alignment** | Not designed | Requires fusion | Native |
| **Scalability** | Poor (O(n³)) | Medium | Good (O(n log n)) |
| **Interpretability** | Low | Medium | High |

---

## Main Ideas & Contributions

### Novel Contributions

#### 1. **Proxy-Based 3D Representation**
- Encodes 3D scenes through semantic cluster proxies
- Orders of magnitude more efficient than 3D encoders
- Maintains geometric information while reducing dimensionality

**Key Innovation**: Don't encode full 3D structure; encode semantic-spatial clusters

#### 2. **Semantic Clustering & Alignment**
- Clusters group semantically and spatially coherent regions
- Direct alignment with language tokens
- End-to-end differentiable

**Advantage**: Inherits language understanding from VLM pre-training

#### 3. **Efficient 3D-Aware VLM**
- No expensive 3D backbone required
- Works with any pre-trained VLM (CLIP, LLaVA, etc.)
- Adds minimal computational overhead (~20% for full 3D reasoning)

#### 4. **Interpretability & Compositionality**
- Each proxy corresponds to understandable semantic unit
- Supports compositional reasoning
- Enables intervention and feature analysis

### Intuition Behind Design Choices

**Why Semantic Clustering?**
- Humans perceive 3D as grouped objects/regions
- Aligns with how language describes scenes
- Dramatically reduces information to transmit

**Why Proxy Representations?**
- Avoids expensive 3D computation during VLM inference
- 3D → 2D compression is irreversible; proxies preserve essential info
- Tokens naturally map to semantic objects

**Why Align with VLM Space?**
- Leverages pre-trained language understanding
- No retraining of base VLM required
- Supports zero-shot 3D reasoning via language

---

## Methodology & Implementation

### Experimental Setup

#### Datasets

1. **3D Scene Understanding**
   - **ScanNet**: 1.5M frames from real indoor scenes
   - **ARKitScenes**: Mobile AR scans (mixed scale)
   - **Replica**: High-quality reconstructed scenes

2. **Evaluation Benchmarks**
   - **3D Visual Question Answering**: "Is the table to the left of the chair?"
   - **Spatial Reasoning**: Object relationships and layouts
   - **Robotic Affordance Understanding**: "Can I grasp this object?"

#### Model Configuration

```
Base VLM: CLIP ViT-L/14 or LLaVA-1.5
3D Encoder: PointNet++ or voxel CNN (lightweight)
Clustering: DBSCAN (ε=0.1m, min_pts=5)
Proxy Dimension: 256 (matching CLIP embedding)
```

#### Baselines

- 2D CLIP (image only)
- 3D PointNet++ encoder
- Multi-view fusion (3 views)
- Recent 3D VLM methods

### Implementation Details

#### Architecture

```
Input: 3D scene point cloud
       ↓
[Feature Extraction] → per-point features (256-dim)
       ↓
[Semantic Clustering] → cluster assignments
       ↓
[Proxy Computation] → weighted aggregation (1-16 proxies)
       ↓
[VLM Alignment] → project to CLIP space
       ↓
[VLM Reasoning] → process with language through standard VLM
```

#### Clustering Algorithm

```python
def semantic_cluster(point_features, spatial_positions, 
                     threshold=0.7, max_distance=0.5):
    """
    Cluster 3D points by semantic similarity and spatial proximity
    """
    # Semantic similarity (cosine distance in feature space)
    semantic_similarity = cosine_similarity(point_features)
    
    # Spatial proximity (distance-based weighting)
    spatial_distances = cdist(spatial_positions, spatial_positions)
    spatial_weights = np.exp(-spatial_distances / max_distance)
    
    # Combined affinity matrix
    affinity = semantic_similarity * spatial_weights
    
    # DBSCAN clustering
    clusters = dbscan(affinity, eps=threshold, min_samples=5)
    return clusters

def compute_proxies(features, cluster_labels):
    """Create proxy representation for each cluster"""
    proxies = []
    for cluster_id in np.unique(cluster_labels):
        mask = cluster_labels == cluster_id
        cluster_features = features[mask]
        
        # Weighted aggregation (attention-based)
        weights = softmax(cluster_features.mean(axis=0) @ cluster_features.T)
        proxy = (cluster_features.T @ weights).squeeze()
        proxies.append(proxy)
    
    return np.array(proxies)
```

#### Training Objective

```
L_total = L_alignment + λ₁ L_consistency + λ₂ L_sparsity

L_alignment: InfoNCE loss between proxies and language tokens
L_consistency: Temporal consistency (for video scenes)
L_sparsity: Regularize number of proxies per scene
```

### Evaluation Metrics

#### Task Performance
- **3D VQA Accuracy**: % correct answers to spatial questions
- **Scene Graph Generation F1**: Precision/recall of relationships
- **Affordance Understanding**: Robot grasping success rate

#### Efficiency Metrics
- **Inference Time**: Milliseconds per scene
- **Memory Usage**: MB of VRAM
- **Throughput**: Scenes/second

#### Quality Metrics
- **Proxy Compactness**: Avg proxies per scene
- **Information Retention**: Mutual information with original scene
- **Compositionality**: Performance on unseen combinations

### Results & Analysis

#### Key Results

**3D VQA Performance**:
| Method | Accuracy | Speedup |
|--------|----------|---------|
| 2D CLIP | 52.3% | 1.0× |
| 3D PointNet++ | 71.2% | 0.15× |
| Multi-view (3×) | 74.1% | 0.25× |
| **Proxy3D** | **76.8%** | **0.85×** |

**Computational Efficiency**:
```
Inference Time per Scene (1024 points):
- 2D CLIP:              42 ms
- Proxy3D:              48 ms (only 14% overhead)
- PointNet++ encoder:   280 ms (6.7× slower)
- Multi-view fusion:    168 ms (4.0× slower)
```

**Memory Efficiency**:
```
Peak VRAM Usage:
- 2D CLIP:              2.1 GB
- Proxy3D:              2.3 GB (+10%)
- 3D Encoders:          8-12 GB
```

#### Ablation Study

| Component | 3D VQA Acc | Memory | Time |
|-----------|---|---|---|
| Full Proxy3D | 76.8% | 2.3GB | 48ms |
| No semantic clustering | 71.3% | 2.2GB | 35ms |
| No spatial weighting | 74.1% | 2.3GB | 45ms |
| Single proxy per scene | 68.9% | 2.1GB | 38ms |
| Dense features (no compression) | 77.1% | 6.2GB | 180ms |

#### Qualitative Analysis

**Learned Proxies**: 
- Automatically segment objects
- Align with semantic classes
- Capture spatial relationships

**Failure Cases**:
- Ambiguous spatial relationships
- Unusual object categories
- Extreme viewpoints

---

## Practical Applications & Use Cases

### Real-World Applications

#### 1. **Robotic Manipulation & Grasping**
- **Challenge**: Robots need 3D understanding for object interaction
- **Solution**: Proxy3D enables language-guided grasping
- **Example**: "Grasp the red cylinder on the left side of the table"

**Implementation**: 
- Predict proxies from RGB-D camera
- Query VLM for affordances
- Plan grasping trajectory

#### 2. **Autonomous Driving**
- **Challenge**: Understand 3D scene layout and traffic interactions
- **Solution**: Efficient 3D awareness without sacrificing speed
- **Example**: "Identify vehicles that are occluded by the building"

**Feasibility**: Real-time processing on vehicle hardware

#### 3. **Augmented Reality (AR) Applications**
- **Challenge**: Place virtual objects in real 3D space
- **Solution**: Understand geometric relationships efficiently
- **Example**: "Place the virtual furniture where it won't collide with existing objects"

**Implementation**: Mobile device compatible, low latency

#### 4. **3D Scene Search & Retrieval**
- **Challenge**: Find objects/relationships in 3D scans
- **Solution**: Language-based querying of 3D scenes
- **Example**: "Find all rooms where chairs face the window"

#### 5. **3D Video Understanding**
- **Challenge**: Reason about dynamic 3D scenes
- **Solution**: Extend proxies to temporal sequences
- **Example**: "Describe how the object's position changes"

### Implementation Challenges

| Challenge | Solution | Feasibility |
|-----------|----------|-------------|
| **Real-time 3D reconstruction** | Depth sensors + incremental clustering | High |
| **Dynamic scenes (moving objects)** | Temporal proxies with motion segmentation | Medium |
| **Novel object categories** | Zero-shot via language embeddings | High |
| **Extreme scales (large outdoor scenes)** | Hierarchical proxy refinement | Medium |

---

## Insights & Implications

### Broader Field Impact

#### 1. **Paradigm Shift: 3D Understanding Without 3D Encoders**
- Demonstrates sufficiency of semantic clustering for 3D reasoning
- Opens door to efficient 3D AI on consumer hardware
- Reduces computational barriers to 3D applications

#### 2. **Unification of 2D and 3D Vision**
- Single model handles both 2D (images) and 3D (scenes)
- Language becomes bridge between modalities
- Enables new research in multi-modal understanding

#### 3. **Practical 3D VLMs**
- First truly efficient 3D-aware VLM
- Deployment-ready on robots, mobile, edge devices
- Opens commercial applications

### State-of-the-Art Advancement

**Previous SOTA**: 3D reasoning required either:
- Expensive separate 3D encoders (6-10× computational overhead)
- Multi-view fusion (4-6× cost)
- Loss of performance on 2D tasks

**Proxy3D Achieves**:
- ✓ Superior 3D reasoning (+4.6% accuracy vs. multi-view)
- ✓ Minimal computational overhead (+14% vs. 2D baseline)
- ✓ Maintained 2D performance
- ✓ Scalable to real-world applications

### Limitations & Open Questions

#### Limitations

1. **Clustering Sensitivity**: Performance depends on clustering hyperparameters
2. **Semantic Information Loss**: Proxy aggregation loses some detail
3. **Dynamic Scenes**: Current approach assumes static scenes
4. **Scale Generalization**: Trained on indoor scenes, unclear on outdoor

#### Open Research Directions

1. **Hierarchical Proxies**: Multi-level abstraction for large-scale scenes
2. **Dynamic Proxy Evolution**: Track proxy changes in video sequences
3. **Semantic Refinement**: Learned clustering functions (instead of DBSCAN)
4. **3D-to-Language Grounding**: Explicit 3D-text alignment training
5. **Generalization**: Cross-domain transfer to outdoor/synthetic scenes

---

## Code & Resources

### Official Implementation

**Paper**: https://arxiv.org/abs/2605.08064  
**GitHub**: Expected soon (under CVPR preparation)

### Dependencies & Requirements

```
pytorch >= 2.0
open3d >= 0.13.0
clip >= 1.0
scikit-learn >= 1.0
numpy >= 1.21
```

### Computational Requirements

- **GPU**: NVIDIA RTX 4090 or A100 recommended
- **Memory**: ~2.5-4 GB VRAM for batch processing
- **Processing**: 40-50ms per scene (1024 points)
- **Preprocessing**: 3D reconstruction if from raw depth

### Quick-Start Guide

```python
from proxy3d import Proxy3D, ProxyEncoder
from clip import CLIP

# Initialize
proxy_encoder = ProxyEncoder(vlm='clip', num_clusters='auto')
vlm = CLIP('ViT-L/14')

# Load 3D scene (point cloud)
scene = load_pointcloud("scene.ply")  # Nx3 points

# Generate proxies
proxies = proxy_encoder(scene)  # Returns (M, 256) embeddings
# M ≈ 5-15 proxies for typical scenes

# Query with language
query = "Is the chair to the left of the table?"
query_embedding = vlm.encode_text(query)

# Reason about 3D
answer = reason_3d_vqa(proxies, query_embedding, vlm)
print(f"Answer: {answer}")
```

### Training (if fine-tuning)

```python
model = Proxy3D.from_pretrained("proxy3d-vit-l")

# Fine-tune on custom 3D VQA dataset
for epoch in range(10):
    for scenes, questions, answers in train_loader:
        proxies = model.encode_3d(scenes)
        predictions = model.reason(proxies, questions)
        loss = criterion(predictions, answers)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

---

## Related Work & Context

### Related Recent Papers

1. **3D Vision-Language Models**
   - "OpenScene: 3D Scene Representation with Open Vocabularies" (2605.05206)
   - "VLM-3R: Vision-Language Models for 3D Reconstruction" (2505.20279)

2. **Semantic Scene Understanding**
   - "Panoptic Studio: A Massively Multimodal Dataset for 3D Panoptic Segmentation" (2024)
   - "Semantic Scene Completion from a Single Depth Image" (2024)

3. **Efficient VLM Extensions**
   - "LoRA: Low-Rank Adaptation for Efficient VLM Fine-tuning" (2021)
   - "Adapting Vision-Language Models to Videos with Minimal Examples" (2024)

### Prior Work Foundations

**Vision-Language Models**: Radford et al. "Learning Transferable Models for Unsupervised Domain Adaptation" (CLIP, 2021)  
**3D Deep Learning**: Charles et al. "PointNet++: Deep Hierarchical Feature Learning on Point Sets in Metric Space" (2017)  
**Scene Understanding**: Cordts et al. "The Cityscapes Dataset for Semantic Urban Scene Understanding" (2016)

### Future Research Directions

1. **Video-based Proxy Evolution**: Temporal proxies for dynamic scenes
2. **Hierarchical Proxy Refinement**: Multi-scale abstractions for large scenes
3. **Interactive 3D Correction**: Human-in-the-loop proxy refinement
4. **Cross-Domain Adaptation**: Generalize from indoor to outdoor/synthetic
5. **Unified 2D/3D Reasoning**: Single model for image+scene understanding
