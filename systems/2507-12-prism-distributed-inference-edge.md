# PRISM: Distributed Inference for Foundation Models at Edge

## Executive Summary

PRISM is a communication-efficient and compute-aware strategy for distributed Transformer inference on edge devices. By leveraging a Segment Means representation to approximate intermediate output features, PRISM drastically reduces inter-device communication (up to 99.2% for BERT) while maintaining accuracy, enabling practical deployment of large foundation models on resource-constrained edge networks.

## Problem Statement

Distributing Transformer inference across edge devices faces critical challenges:

- **Communication Bottleneck**: Intermediate activations between layers can be massive; transmitting them between edge nodes creates severe latency and bandwidth constraints
- **Computational Heterogeneity**: Edge devices have vastly different computational capabilities and network connectivity
- **Model Size**: Foundation models often exceed single device memory; must be partitioned across multiple devices
- **Latency Requirements**: Edge applications demand real-time inference, incompatible with high communication overhead

Previous approaches either:
- Centralized inference (privacy/latency issues)
- Naive distributed computation (excessive communication)
- Quantization (accuracy loss)
- Model compression (significant capability reduction)

PRISM addresses these by compressing intermediate features rather than reducing model capability.

## Core Concepts & Theory

### Segment Means Representation

The core innovation is replacing full intermediate layer outputs with compressed "segment means":

**Standard approach**: Pass all intermediate activations `H ∈ R^(batch_size × sequence_length × hidden_dim)`

**PRISM approach**: 
1. Divide sequence into K segments
2. Compute mean vector for each segment: `segment_mean = mean(H[i:j, :])` 
3. Transmit only segment means instead of full activations
4. Reconstruct approximation at receiving device

**Information preservation**: While segment means lose fine-grained positional information, they preserve:
- Overall feature statistics
- High-level semantic content
- Token-to-token interactions at coarser granularity

### Compression Rate and Reconstruction

Let `sequence_length = L`, `compression_rate = CR = L/K` (segments per token):

- **Communication reduction**: `1/CR` of original size
- **Reconstruction**: Linear interpolation for missing tokens within segments
- **Quality trade-off**: Increases with larger CR values

### Mathematical Foundation

For layer output `H_l^out` at layer l:
```
Compressed representation: H_l^compressed = {mean(H_l^out[seg_i]) | i ∈ 1...K}

Reconstructed input: H_{l+1}^in = interpolate(H_l^compressed, L)

Error bound: ||H_{l+1}^in - H_l^out|| ≤ δ(CR, L, hidden_dim)
```

The error bounds are provably tighter for longer sequences and larger compression rates.

## Main Ideas & Contributions

### 1. Segment Means Representation for Compression

**Key Insight**: Transformer layers aggregate information; exact token-by-token activation details aren't essential for downstream layers to compute meaningful outputs.

**Contribution**: Proposes segment means as the right abstraction level for edge communication:
- Preserves semantic information
- Dramatically reduces communication (99.2% for BERT)
- Minimal accuracy degradation (1-3%)

### 2. Compute-Aware Partitioning

Different edge devices have different compute capabilities. PRISM's strategy:

1. **Profile each device**: Measure compute speed and memory
2. **Assign layers** based on capability:
   - Fast devices: computational layers (self-attention, FFN)
   - Slow devices: embedding/output layers
3. **Optimize segment sizes** based on network bandwidth

### 3. Dynamic Adaptation

PRISM adapts to network conditions:
- **High bandwidth**: Larger CR (less compression)
- **Low bandwidth**: Smaller CR (more compression)
- **Variable latency**: Adjust segment sizes dynamically

This enables robust performance across diverse edge scenarios.

## Methodology & Implementation

### Experimental Setup

**Models Evaluated**:
- BERT (110M parameters)
- RoBERTa (355M parameters)
- DistilBERT (66M parameters)
- Small Vision Transformer (ViT-Small)

**Edge Network Configurations**:
1. **LAN**: High-bandwidth, low-latency (100 Mbps, 5ms)
2. **Wireless**: Medium bandwidth (50 Mbps, 20ms)
3. **Long-range**: Low bandwidth (10 Mbps, 100ms)

**Datasets**:
- GLUE benchmark for NLP tasks
- ImageNet for vision tasks
- Synthetic workloads for stress testing

### System Architecture

**Components**:
1. **Layer Partitioner**: Assigns layers to devices
2. **Compression Module**: Implements segment means
3. **Communication Runtime**: Handles synchronized layer-to-layer passing
4. **Reconstruction Engine**: Interpolates received segments

**Communication Protocol**:
```
Device A (layers 1-6):
  1. Forward pass on layers 1-6
  2. Compute segment means of output
  3. Send compressed output to Device B
  
Device B (layers 7-12):
  1. Receive segment means from Device A
  2. Reconstruct full-resolution input
  3. Forward pass on layers 7-12
  4. Send results to Device C (or output)
```

### Training Configuration

**Fine-tuning**: Models fine-tuned on task-specific data with full-resolution training, then deployed with PRISM compression

**Inference Only**: No retraining required; compression applied during inference only

## Results, Metrics & Benchmarks

### Communication Overhead Reduction

| Model | Compression Rate | Communication Reduction | Accuracy Loss |
|-------|------------------|------------------------|----------------|
| BERT | CR=32 | 96.9% | 0.8% |
| BERT | CR=64 | 98.4% | 1.5% |
| BERT | CR=128 | 99.2% | 2.1% |
| RoBERTa | CR=64 | 98.1% | 1.2% |
| DistilBERT | CR=128 | 99.1% | 1.8% |

### Computation Efficiency

Per-device computation reduction with optimal partitioning:

| Task | Single Device | PRISM 2-Device | Reduction |
|------|---------------|----------------|-----------|
| BERT on GLUE | 100% | 51.24% | 48.8% |
| RoBERTa | 100% | 54.2% | 45.8% |
| ViT inference | 100% | 52.1% | 47.9% |

### End-to-End Latency

On wireless network (50 Mbps, 20ms RTT):

| Approach | Latency (ms) | Communication Time | Compute Time |
|----------|-------------|-------------------|--------------|
| Single device | 250 | 0 | 250 |
| Naive distribution | 450 | 280 | 170 |
| PRISM (CR=64) | 195 | 15 | 180 |

**Finding**: PRISM provides 1.28x speedup despite slower individual devices due to parallelization and reduced communication.

### Accuracy on Downstream Tasks

Tested on GLUE benchmark (averaged across 8 tasks):

- **BERT (Full)**: 80.5% accuracy
- **BERT (PRISM, CR=64)**: 79.3% accuracy (1.2% drop)
- **BERT (Quantized, INT8)**: 77.1% accuracy (3.4% drop)

PRISM outperforms quantization while being simpler to implement.

### Robustness to Network Conditions

Tested with variable bandwidth and latency:

```
Bandwidth: 10 Mbps - 100 Mbps
Latency: 5 ms - 200 ms
Packet loss: 0% - 5%

PRISM maintains <2% accuracy drop across all configurations
while adapting compression rate dynamically
```

## Practical Applications & Use Cases

### 1. Mobile Inference
- Smartphone with cloud co-processor
- Split inference between device and edge server
- Reduced bandwidth enables faster response times
- Privacy-preserving (raw data stays on device)

### 2. IoT Edge Networks
- Sensor networks with limited bandwidth
- Distributed processing across IoT hubs
- Real-time inferencing for industrial applications
- Energy-efficient multi-hop networks

### 3. Federated Learning
- Train models while keeping data distributed
- Use PRISM for efficient gradient communication
- Reduced communication in federated inference

### 4. Automotive Edge Computing
- Vehicle-to-vehicle communication
- Vehicle-to-infrastructure (V2I) collaboration
- Real-time autonomous driving with edge inference

### 5. Medical Edge Devices
- Hospital sensor networks
- Privacy-preserving patient monitoring
- Real-time diagnostic assistance
- Telemedicine with local processing

## Implementation Considerations

### Challenges

1. **Reconstruction Accuracy**: Finding optimal segment sizes for different model architectures
2. **Dynamic Adjustment**: Adapting compression rate based on network measurements
3. **Heterogeneous Devices**: Balancing partitioning across devices with different capabilities
4. **Synchronization**: Ensuring all distributed components stay synchronized

### Performance Trade-offs

- **Communication vs. Accuracy**: Higher compression = more latency savings but accuracy loss
- **Device Heterogeneity**: More capable devices can do more computation but communication dominates
- **Model Architecture**: Transformers benefit most; CNNs benefit less from this approach

## Insights & Implications

### Broader Field Impact

- **Communication is the bottleneck**: More important than computation in many edge scenarios
- **Feature approximation works**: Segment means successfully capture essential information
- **Practical edge inference is achievable**: Can deploy large models on small networks

### State-of-the-Art Advancement

- First work to achieve 99.2% communication reduction on practical models
- Outperforms quantization on communication-limited scenarios
- Enables real-time inference for large models on edge networks

### Limitations and Open Questions

1. **Architecture specificity**: Does segment means work for all Transformer variants (e.g., sparse attention)?
2. **Very low bandwidth**: How does PRISM perform on sub-1 Mbps networks?
3. **Dynamic sequences**: Variable input length optimization needed
4. **Streaming inference**: How to handle continuous streaming scenarios?

## Code & Resources

### Implementation

Paper introduces PRISM framework with reference implementation

### Dependencies

- **PyTorch**: Deep learning framework
- **PyTorch Distributed**: Multi-device communication
- **Network Measurement**: Bandwidth/latency profiling tools

### Quick-Start Guide

1. **Profile network**: Measure bandwidth and latency between devices
2. **Partition model**: Assign layers based on device capabilities
3. **Set compression rate**: Based on network characteristics and accuracy requirements
4. **Run inference**: Distributed forward pass with automatic compression

## Related Work & Context

### Related Recent Papers

- **Model Parallelism**: Prior distributed inference approaches (Pipeline Parallelism)
- **Knowledge Distillation**: Alternative approach to reducing model size
- **Neural Network Compression**: Quantization, pruning, and other compression techniques
- **Edge AI Systems**: Systems-level approaches to edge inference

### Prior Work Foundations

- **Transformer Architecture**: Basis for models being distributed
- **Distributed Deep Learning**: Foundations of multi-device coordination
- **Network Optimization**: Compression and communication patterns

### Possible Future Research Directions

1. **Adaptive Compression**: Learning to adjust segment size based on input
2. **Cross-layer Optimization**: Co-optimize partitioning and compression jointly
3. **Heterogeneous Architectures**: Support non-Transformer models
4. **Wireless Protocols**: Integration with 5G/6G edge computing frameworks
5. **Privacy-Aware Distribution**: Formal privacy guarantees for distributed inference

## Paper Metadata

- **ArXiv ID**: 2507.12145
- **Authors**: Muhammad Azlan Qazi, Alexandros Iosifidis, Qi Zhang
- **Submission Date**: July 16, 2025
- **Subject Areas**: Machine Learning (cs.LG), Artificial Intelligence (cs.AI), Computer Vision and Pattern Recognition (cs.CV)
- **Citation**: https://arxiv.org/abs/2507.12145
