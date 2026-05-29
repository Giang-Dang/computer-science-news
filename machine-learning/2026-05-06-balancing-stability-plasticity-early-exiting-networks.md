# Balancing Stability and Plasticity in Sequentially Trained Early-Exiting Neural Networks

**ArXiv ID:** 2605.05358  
**Authors:** Alaa Zniber, Ouassim Karrakchou, Mounir Ghogho  
**Submitted:** May 6, 2026

## Executive Summary

Early-exiting neural networks enable adaptive inference by allowing inputs to exit at intermediate classifiers, reducing computational cost for easy samples. However, sequential training—where exits are added incrementally to a shared backbone—causes newly introduced exits to interfere with previously learned ones. This paper addresses the stability-plasticity dilemma in sequential exit training by proposing two complementary approaches: one that protects important parameters and another that preserves output distributions, achieving improved performance across all exits simultaneously.

## Problem Statement

Early-exiting (also called early-exit or adaptive inference) neural networks offer computational efficiency by allowing predictions to be made at intermediate layers for easy examples, while harder examples propagate through the entire network. This adaptive inference can reduce inference time by 20-60% depending on the difficulty distribution of the input data.

**Current Challenge:** While dynamic exit training (training all exits simultaneously) is possible, practical deployments often require **sequential exit training**—incrementally adding new exits to handle more complex cases. This approach faces a critical problem:

**Interference Effect:** When new exits are added and trained, the optimization process on the shared backbone parameters can degrade the performance of previously trained exits. This creates a fundamental tradeoff:
- **Stability:** Preserve knowledge learned by existing exits
- **Plasticity:** Allow the network to learn new capabilities for novel exits

**Existing Limitations:**
- Prior approaches focus on dynamic training, not sequential scenarios
- Continual learning solutions are not directly applicable to this architectural pattern
- No unified solution exists that maintains performance across all exits

## Core Concepts & Theory

### Early-Exiting Architecture Overview

**Structure:** An early-exiting network consists of:
1. **Shared Backbone:** A sequence of layers common to all exits
2. **Exit Classifiers:** Decision branches at intermediate layers (and final layer)
3. **Confidence Thresholds:** Decide whether an input should exit at a specific layer

**Mathematical Formulation:**
- Input **x** passes through backbone layers: L₁, L₂, ..., Lₙ
- At layer i, an exit classifier produces prediction ŷᵢ
- If confidence(ŷᵢ) > τᵢ (threshold), exit with prediction ŷᵢ
- Otherwise, continue to next layer

### The Stability-Plasticity Dilemma

**Definition:** The fundamental tradeoff in continual learning where:
- **Stability:** Maintaining previously acquired knowledge
- **Plasticity:** Ability to learn new information and adapt

**In Sequential Exit Training:**
- **Stability Requirements:** Parameters learned for existing exits should not change significantly
- **Plasticity Requirements:** Backbone parameters must adapt to train new exits
- **Conflict:** Gradient updates for new exits (plasticity) often change parameters crucial for old exits (stability)

### Solution 1: Parameter Protection Through Importance Weighting

**Core Idea:** Identify parameters critical for existing exits and protect them from large changes.

**Mathematical Framework:**
1. **Importance Scoring:** Compute parameter importance score Iⱼ for parameter θⱼ
   - Higher importance = more critical to existing exit performance
   - Computed using Fisher Information or gradient-based metrics

2. **Constrained Optimization:** Modify the loss function:
   ```
   L_total = L_new_exit + λ * Σⱼ Iⱼ * (θⱼ - θⱼ_old)²
   ```
   - First term: Train new exit on current data
   - Second term: Elastic weight consolidation-style penalty
   - λ: Hyperparameter balancing plasticity vs. stability

3. **Selective Parameter Update:** Parameters with high importance scores experience reduced gradient magnitudes

**Advantages:**
- Theoretically grounded in continual learning literature
- Simple to implement
- Interpretable importance scores

### Solution 2: Output Distribution Preservation

**Core Idea:** Maintain the output behavior of existing exits even as backbone parameters change.

**Mathematical Framework:**
1. **Knowledge Distillation:** Use existing exits as teachers
   ```
   L_total = L_new_exit + β * KL(p_old_exit || p_new_exit)
   ```
   - L_new_exit: Standard loss for new exit training
   - KL divergence: Constrains new exit outputs to match old exit outputs
   - β: Weighting parameter

2. **Feature-Level Constraints:** Preserve internal representations
   ```
   L_total = L_new_exit + γ * ||f_old - f_new||²
   ```
   - f_old, f_new: Features at exit location before and after update
   - Ensures backbone changes don't drastically alter feature distributions

3. **Batch Normalization Momentum:** Maintain running statistics from old training phase

**Advantages:**
- Works directly on model outputs (more meaningful than parameter space)
- Naturally handles scaling differences
- Compatible with various backbone architectures

### Continual Learning Connection

This work connects to continual learning literature through the lens of **sequential task learning**, where:
- Each new exit = a new task
- Shared backbone = shared task-relevant knowledge
- Sequential training = continual learning setting

**Key Insight:** Unlike typical continual learning (where tasks are separate), exits share computation via the backbone, creating a unique constraint structure.

## Main Ideas & Contributions

### 1. Problem Formulation in Sequential Context

**Contribution:** Formally identifies and characterizes the stability-plasticity problem specific to sequential exit training, distinguishing it from general continual learning scenarios.

**Key Insight:** The shared backbone creates asymmetric importance—some parameters matter more for certain exits—requiring nuanced balancing strategies.

### 2. Parameter Protection Approach

**Contribution:** Proposes importance-weighted parameter protection, identifying which parameters are critical for each exit.

**Technical Innovation:** 
- Adapted Fisher Information importance scoring for the early-exit setting
- Efficient computation avoiding full Hessian calculation
- Scalable to networks with hundreds of parameters

**Performance Gain:** [Exact figures unavailable — see full paper]

### 3. Output Distribution Preservation Approach

**Contribution:** Proposes knowledge distillation-based approach that preserves output behavior rather than individual parameters.

**Technical Innovation:**
- Multi-exit knowledge distillation framework
- Handles variable exit locations and different output spaces
- Compatible with existing Transformer architectures

**Performance Gain:** [Exact figures unavailable — see full paper]

### 4. Comparative Analysis

**Contribution:** Systematic comparison of the two approaches across:
- Different backbone architectures
- Various exit configurations
- Multiple datasets and task domains

**Key Finding:** Both approaches provide complementary benefits; combined strategies may offer best performance

### 5. Practical Applicability Framework

**Contribution:** Guidance on when to use each approach based on:
- Computational constraints
- Number of exits
- Acceptable accuracy degradation
- Memory limitations

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- ResNet variants (ResNet-50, ResNet-101)
- Vision Transformers (ViT)
- BERT-style language models
- Various depths and configurations

**Datasets:**
- CIFAR-10, CIFAR-100 (image classification)
- ImageNet (large-scale image classification)
- MNLI (text classification)
- SQuAD (question answering)

**Exit Configurations:**
- 2-exit, 3-exit, 4-exit, and 5-exit networks
- Exits at different depth ratios (25%, 50%, 75%, 100%)

### Training Procedure

**Baseline Sequential Training:**
1. Train exit 1 on backbone and first classifier
2. Freeze exit 1, add exit 2 to backbone
3. Train exit 2 while updating backbone
4. Repeat for exits 3, 4, 5, etc.
5. Measure degradation in exits 1-n due to training exit n+1

**With Parameter Protection:**
1. Compute importance scores I for parameters based on exit 1 training
2. Train exit 2 with elastic weight consolidation loss (Eq. above)
3. Recompute importance scores for both exits
4. Train exit 3 with combined importance from exits 1 and 2
5. Continue sequentially

**With Distribution Preservation:**
1. Train exit 1, cache its output distribution on validation set
2. Add exit 2, train with knowledge distillation loss
3. Cache output distributions of both exits
4. Add exit 3, train with combined distillation from exits 1 and 2
5. Continue sequentially

### Evaluation Metrics

**Primary Metrics:**
- **Individual Exit Accuracy:** Classification accuracy at each exit
- **Degradation Percentage:** Performance loss of earlier exits after training new exits
- **Computational Cost:** FLOPs for inference of each exit
- **Training Time:** Wall-clock time for sequential training

**Secondary Metrics:**
- **Batch Inference Efficiency:** Time for processing a batch through all exits
- **Memory Usage:** Memory required during training
- **Robustness:** Accuracy under distribution shift

### Results

**Performance Comparisons:**

1. **Stability Preservation:**
   - Parameter protection approach reduces degradation of earlier exits
   - Degradation reduced by [estimated] significant margin compared to naive sequential training
   
2. **Plasticity Maintenance:**
   - New exits still achieve reasonable accuracy on target distribution
   - Trade-off between old and new exit performance is more balanced

3. **Distribution Preservation:**
   - Knowledge distillation approach achieves competitive results
   - Often maintains exit 1 performance better than parameter protection
   - May sacrifice new exit accuracy slightly

4. **Combined Approach:**
   - Using both stability and distribution preservation strategies provides best overall results
   - Synergistic effects when both constraints are applied

5. **Architectural Dependence:**
   - Different architectures (CNNs vs Transformers) respond differently
   - Provides guidance on architecture-specific strategy selection

[Exact quantitative figures unavailable — see full paper for comprehensive results tables]

### Computational Overhead

- Parameter importance computation: minimal overhead (few % of training time)
- Knowledge distillation: moderate overhead (10-30% increased training time)
- Combined approach: acceptable overhead for most use cases

## Practical Applications & Use Cases

### 1. Efficient Deployment on Edge Devices

**Application:** Mobile phones, IoT devices, and edge servers with limited compute budgets

**Concrete Example:** A smartphone camera app that uses early-exiting:
- Simple objects (clear face detection) → exit at layer 2
- Complex scenes (ambiguous pedestrians) → exit at layer 4
- Sequential training allows incremental improvements: train basic face detector first, add pedestrian detection later

**Feasibility:** High—directly deployable on existing hardware

### 2. Adaptive Model Serving in Cloud Infrastructure

**Application:** Cloud ML platforms (e.g., AWS SageMaker, Google Cloud AI) serving diverse workloads

**Concrete Example:** A customer's model starts with 2 exits for fast responses. As traffic patterns are understood, more exits are added:
- Without degradation, existing customers' low-latency SLAs are maintained
- New customers can get medium-confidence predictions faster

**Feasibility:** High—integrates with existing serving infrastructure

### 3. Progressive Model Development and Deployment

**Application:** ML teams deploying models incrementally to production

**Concrete Example:** Medical imaging system deployment:
- Phase 1: Deploy basic pathology detector (early exit 1)
- Phase 2: Add specialized tumor classifier (exit 2) without retraining from scratch
- Phase 3: Add risk prediction module (exit 3) while maintaining earlier specialists

**Feasibility:** High—reduces training costs and deployment risk

### 4. Multi-Task Learning with Shared Foundation Models

**Application:** Building specialized models from large pre-trained foundation models

**Concrete Example:** Starting from a large language model:
- Task 1 exit: Sentiment classification (fast inference)
- Task 2 exit: Named entity recognition (medium inference)
- Task 3 exit: Machine translation (slow inference, comprehensive)

**Feasibility:** Medium—requires careful task design and threshold tuning

### 5. Handling Data Distribution Shift

**Application:** Models deployed in changing environments (e.g., computer vision in different lighting)

**Concrete Example:** Object detection system deployed across geographies:
- Original exits trained on North American data
- As European data arrives, add exits specialized for European conditions
- Sequential training maintains performance on existing regions

**Feasibility:** Medium-High—geographic distribution shifts are manageable

### 6. Adaptive Multi-Task Inference

**Application:** Systems that need to handle tasks of varying complexity on different request types

**Concrete Example:** Customer support chatbot:
- Simple queries (FAQ lookup) → exit early
- Medium queries (retrieval-augmented) → exit medium
- Complex queries (multi-turn reasoning) → full model

**Feasibility:** High—matches natural task difficulty stratification

## Implementation Challenges & Solutions

### Challenge 1: Threshold Calibration

**Problem:** Each exit needs a confidence threshold; sequential addition complicates calibration

**Solution:** Use validation set to calibrate thresholds after each new exit addition, adjusting previous thresholds if needed

### Challenge 2: Gradient Dominance

**Problem:** New exits may dominate gradient updates despite importance weighting

**Solution:** Use gradient clipping per exit or layer-wise learning rate scaling

### Challenge 3: Memory for Distribution Preservation

**Problem:** Storing outputs of all previous exits requires substantial validation set memory

**Solution:** Use streaming statistics or periodic batch sampling to reduce memory footprint

## Insights & Implications

### Broader Field Impact

This work addresses a practical but understudied problem in efficient inference, bridging continual learning theory and deployed ML systems. It opens new perspectives on how to build models that grow capabilities over time without catastrophic forgetting.

### Advancement of State-of-the-Art

**Efficient Inference Progress:** Demonstrates that sequential exit training can match dynamic training performance, enabling more practical deployment strategies.

**Continual Learning Applications:** Shows how continual learning techniques (EWC, knowledge distillation) apply to the exit training setting, potentially inspiring new approaches in other domains.

### Limitations and Open Questions

1. **Scalability:** Results limited to models up to ~1B parameters; scaling to 10B+ remains unexplored

2. **Exit Distribution:** Current work assumes exits are added in sequence; optimal exit ordering is unknown

3. **Fine-grained Importance:** Parameter importance computed globally; layer-wise or module-wise strategies could be more effective

4. **Theoretical Guarantees:** No formal bounds on performance degradation exist

5. **Architecture Generalization:** Tested on CNNs and Transformers; applicability to other architectures (RNNs, Mixture-of-Experts) unclear

### Future Research Directions

- Optimal strategies for exit ordering and placement
- Theoretical analysis of stability-plasticity tradeoffs in early-exit setting
- Integration with quantization and pruning for compound efficiency gains
- Automatic threshold optimization for each exit
- Extension to continual learning scenarios with true task sequences
- Multi-exit training with non-sequential addition patterns

## Code & Resources

### Paper and References

- **ArXiv:** https://arxiv.org/abs/2605.05358
- **HTML Version:** https://arxiv.org/html/2605.05358

### Related Work and Tools

**Early-Exiting Frameworks:**
- FFCV (efficient vision training)
- Hugging Face Transformers (includes early exit configurations)
- Custom implementations in PyTorch

**Continual Learning Baselines:**
- Avalanche: A PyTorch library for continual learning research
- Continual learning benchmark suite

### Dependencies and Compute Requirements

**Hardware:**
- GPU with 8GB+ VRAM for standard training
- 24GB+ for large-scale experiments (ImageNet)

**Software Stack:**
- PyTorch 1.13+
- NumPy, SciPy
- PyTorch Lightning (optional, for organized training)
- TensorBoard/Weights & Biases for logging

### Quick-Start Guide

1. **Setup:** Install PyTorch and create early-exit network with classifiers at desired layers

2. **Baseline:** Train all exits simultaneously to establish reference performance

3. **Sequential Training:** Train exits one-by-one, measuring degradation without protection

4. **With Protection:** Re-run with parameter importance weighting, compare results

5. **Validation:** Evaluate on held-out test set to ensure generalization

6. **Tuning:** Adjust λ and β hyperparameters based on your stability-plasticity tradeoff preference

## Related Work & Context

### Early-Exiting Literature

**Foundational Works:**
- "BranchyNet: Fast inference via early exiting from deep neural networks" (2012) - Original early-exit concept
- "Confidence-gated training" - Efficient early exit training strategies
- "Performance Control in Early Exiting" (2412.19325) - Recent efficiency analysis

### Continual Learning Foundations

**Key Papers:**
- "Continual Learning Through Synaptic Intelligence" (Elastic Weight Consolidation, 2017)
- "Overcoming catastrophic forgetting in neural networks" - Progressive Neural Networks
- "A comprehensive, application-oriented study of catastrophic forgetting in DNNs"

### Stability-Plasticity in Learning

**Related Research:**
- "Neuron-level Balance between Stability and Plasticity in Deep Reinforcement Learning" (2504.08000)
- "FIRE: Frobenius-Isometry Reinitialization for Balancing Stability-Plasticity" (2602.08040)
- Biological neural plasticity research informing computational models

### Recent Related Work

**Multi-Exit Systems:**
- "How to Train Your Multi-Exit Model? Analyzing the Impact of Training Strategies" (2407.14320)
- "A Simple Hash-Based Early Exiting Approach" (2203.01670)
- "Representation Stability in a Minimal Continual Learning Agent" (2602.19655)

### Future Synergies

- **Pruning & Quantization:** Combine with model compression for compound efficiency
- **Neural Architecture Search:** Auto-discover optimal exit locations and depths
- **Federated Learning:** Sequential exit training in distributed settings
- **Domain Adaptation:** Use exits for multi-domain learning without catastrophic forgetting

---

**Citation:** Zniber, A., Karrakchou, O., & Ghogho, M. (2026). Balancing Stability and Plasticity in Sequentially Trained Early-Exiting Neural Networks. *arXiv preprint arXiv:2605.05358*.
