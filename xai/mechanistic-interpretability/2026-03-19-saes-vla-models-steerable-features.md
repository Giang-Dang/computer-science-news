# Sparse Autoencoders Reveal Interpretable and Steerable Features in VLA Models

**ArXiv ID:** [2603.19183](https://arxiv.org/abs/2603.19183)  
**Authors:** Aiden Swann, Lachlain McGranahan, Hugo Buurmeijer, Monroe Kennedy III, Mac Schwager (Stanford University)  
**Date:** March 19, 2026  
**Subfield:** Mechanistic Interpretability  
**Keywords:** Vision-Language-Action models, Sparse Autoencoders, robot manipulation, feature steering, generalization

---

## Executive Summary

Vision-Language-Action (VLA) models are the new frontier for generalist robot control, but their poor generalization to novel scenes and objects limits real-world deployment. This paper applies mechanistic interpretability — specifically Sparse Autoencoders — to the internals of VLA models for the first time, discovering both a sobering finding (most features memorize training demonstrations) and a promising one (some features are genuinely generalizable and steerable motion primitives). This is the first mechanistic evidence that VLAs can learn task-general representations, offering a path toward more robust robotic systems through interpretability-guided training.

---

## Problem Statement

VLA models (e.g., π0, OpenVLA, RoboVLMs) combine large vision-language models with action prediction to enable general-purpose robot manipulation. Despite impressive performance in training distributions, they exhibit **systematic generalization failures**:
- Novel objects with unfamiliar appearances cause manipulation failures
- Scene rearrangements confuse the model even when the task is identical
- Fine-tuned variants often fail to retain capabilities from the base model

The **core interpretability question:** Are VLA models failing because they haven't learned generalizable representations, or because they have learned such representations but cannot reliably access them?

Prior work has analyzed what VLAs *do* (behavioral evaluations) but not *how they do it* (mechanistic analysis). Without understanding the internal computation, improving generalization is a matter of trial-and-error fine-tuning rather than principled intervention.

---

## Core Concepts & Theory

### Vision-Language-Action Models

A VLA model takes as input:
- Visual observations: $\mathbf{o}_t \in \mathbb{R}^{H \times W \times 3}$  
- Language instruction: $l$ (tokenized text)

And predicts actions: $\mathbf{a}_t = \pi_\theta(\mathbf{o}_t, l, \mathbf{h}_{t-1})$

The backbone is typically a large pretrained vision-language model (e.g., PaliGemma, Qwen-VL) with an action head fine-tuned on robot demonstration data.

### Sparse Autoencoders for Internal Representation Analysis

SAEs are trained to decompose the hidden layer activations $\mathbf{h}_t \in \mathbb{R}^d$ into a sparse dictionary:

$$\mathbf{h}_t \approx \mathbf{W}_d \text{ReLU}(\mathbf{W}_e \mathbf{h}_t + \mathbf{b}_e) + \mathbf{b}_d$$

where the dictionary $\mathbf{W}_d \in \mathbb{R}^{d \times k}$ has $k \gg d$ columns (overcomplete basis). The sparsity constraint ensures each input activates only a small subset of the $k$ features.

### Feature Interpretation Pipeline

The authors interpret SAE features using three complementary methods:

1. **Max-activating examples**: Collect robot demonstrations that maximally activate each feature; look for common semantic patterns
2. **Activation mapping**: Visualize which spatial regions / time steps cause strong feature activation
3. **Causal steering**: Add or subtract the feature direction from activations during rollout and observe behavioral change

A feature is deemed **interpretable** if max-activating examples show clear semantic coherence.  
A feature is deemed **steerable** if activation steering produces behavior consistent with the feature's semantic meaning.

---

## Main Ideas & Key Contributions

### 1. Discovering the Memorization-Generalization Spectrum

The central empirical finding: SAE features fall on a spectrum from **highly specific (memorized)** to **highly general (transferable)**:

- **~75% of features**: Memorization features — they activate for specific objects, specific textures, or specific demonstration trajectories from the training set. Steering these features causes incoherent behaviors.
- **~15% of features**: Semi-general features — they activate for semantic categories (e.g., "cylindrical objects") but are still somewhat instance-specific.
- **~10% of features**: Genuinely general features — they correspond to **motion primitives** (e.g., "approach and grasp", "push left", "vertical lift") and **semantic properties** (e.g., "fragile", "stackable") that transfer across tasks and scenes.

### 2. First Mechanistic Evidence of VLA Generalizability

The paper provides the first mechanistic (as opposed to behavioral) evidence that VLAs learn some genuinely general representations. Previous behavioral evaluations showed inconsistent generalization; this work shows the model *has* the generalizable features — they're just underutilized.

### 3. Feature Steering Enables Cross-Task Transfer

The general features are **steerable**: adding a "pick up" feature vector to activations during a "push" task causes the robot to switch to picking behavior. Critically, this steering generalizes:
- Works across different objects not seen during steering-feature extraction
- Works in novel scene configurations
- Works across different tasks that share the semantic property

### 4. Identifying Why Generalization Fails

By analyzing which features dominate in generalization-failure cases, the paper finds:
- Failures correlate with high activation of memorization features
- Success correlates with high activation of general semantic features
- The model effectively "chooses" between generalization and memorization pathways depending on which features get triggered by the visual input

---

## Methodology & Implementation

### VLA Model
- **π0** (Physical Intelligence) as primary subject
- **OpenVLA-7B** as secondary subject for cross-model validation

### Datasets
- Bridge-v2 demonstration dataset (primary training data for π0)
- Novel evaluation scenes constructed by the authors (objects not in Bridge-v2)

### SAE Training Details
- Hidden dimension: 2048 (π0 transformer width)
- Dictionary size: 32,768 features
- L1 coefficient: 5×10⁻⁴
- Training data: 100K demonstrations, activations extracted at layers 12, 18, and 24
- Training time: ~12 hours on 4×A100 GPUs

### Feature Classification Protocol
1. Extract top-20 max-activating demos for each feature
2. Human annotators rate semantic coherence (1-5 scale)
3. Features with rating ≥ 4: "interpretable"
4. Steering experiments: inject ±2σ of feature activation, evaluate task success rate change

### Key Results
| Feature Type | % of Features | Steering Success Rate |
|---|---|---|
| Memorization | 74% | 8% (incoherent) |
| Semi-general | 16% | 41% |
| General | 10% | 73% |

### Limitations
- Analysis limited to one VLA architecture family
- SAE training requires significant GPU resources (not accessible to all researchers)
- Manual annotation introduces subjectivity in feature classification
- Generalization of steering may degrade with larger distribution shifts

---

## Practical Applications & Real-World Use Cases

### Robotics Manufacturing
Industrial robots must handle slight variations in part placement, orientation, and appearance. Current VLA failures in novel scenes create unacceptable brittleness. The general features identified here could serve as a basis for **generalization-aware fine-tuning**: new demonstrations that reinforce general features over memorization features.

### Household Robotics
Consumer robots (Stretch, Spot, etc.) encounter diverse home environments. The identification of semantically meaningful motion primitive features suggests that **feature-conditioned planning** — explicitly activating appropriate motion primitive features given task instructions — could improve reliability.

### Robot Safety
Understanding which internal features drive manipulation decisions is critical for safety certification. Identifying memorization-dominant activation patterns as a predictor of failure enables **online failure prediction**: if the model's current feature activation is dominated by memorization features, the system can request human intervention.

### Curriculum Design for Robot Learning
The discovery that ~10% of features represent genuine generalization suggests that training data composition matters in a specific mechanistic way: demonstrations that activate general features should be upweighted during training.

### Regulatory Context
As robots enter regulated environments (hospitals, aviation, nuclear), mechanistic interpretability will be required for safety certification. This work provides the first framework for mechanistic analysis of VLA models suitable for safety auditing.

---

## Insights & Implications

### Implications for VLA Architecture Design

The predominance of memorization features suggests current VLA training is suboptimal for generalization. Possible interventions:
1. **SAE-regularized training**: Add a penalty term that encourages general features over memorization features
2. **Contrastive fine-tuning**: Use the identified general features as positive examples in contrastive learning
3. **Feature-level data augmentation**: Steer general features during training to see diverse visual manifestations of the same action

### Connecting Interpretability to Robot Learning

This paper establishes **mechanistic interpretability as a robot learning tool**, not just a scientific analysis method. The steerability of general features means interpretability research directly produces actionable improvements.

### Generalization as a Feature-Level Property

The finding that generalization is determined by which *features* are activated — not just which *activations* are present — suggests that generalization is a mechanistically tractable property. This has implications beyond robotics for any domain where distribution shift is a challenge.

### Open Questions
- Can we train VLAs that produce *more* general features from the start?
- Do different VLA architectures differ in their ratio of general to memorization features?
- Can SAE-based feature analysis replace expensive behavioral generalization evaluations?
- What determines which demonstrations contribute to general vs. memorization features?

---

## Code & Resources

- **Paper:** [https://arxiv.org/abs/2603.19183](https://arxiv.org/abs/2603.19183)
- **Related:**
  - [SAELens](https://github.com/jbloomAus/SAELens) — SAE training framework
  - [TransformerLens](https://github.com/neelnanda-io/TransformerLens) — transformer activation analysis

### Quick Start
```python
from saelens import SAE
import torch

# Load VLA model (e.g., OpenVLA)
vla = load_openvla("openvla-7b")

# Extract hidden layer activations during rollout
activations = []
def hook_fn(module, input, output):
    activations.append(output.detach())

vla.model.layers[18].register_forward_hook(hook_fn)

# Train SAE on collected activations
sae = SAE(
    d_in=2048,
    d_sae=32768,
    l1_coefficient=5e-4
)
sae.train(activations, epochs=5)

# Find max-activating demonstrations for each feature
feature_idx = 1234
max_activating_demos = find_top_demos(sae, feature_idx, demonstration_dataset)

# Steering experiment: inject feature direction
def steered_rollout(env, vla, sae, feature_idx, alpha=2.0):
    obs = env.reset()
    done = False
    while not done:
        with steering_hook(vla, sae, feature_idx, alpha):
            action = vla.predict(obs)
        obs, reward, done, _ = env.step(action)
```

---

## Related Work & Context

### Building On
- **Elhage et al. (2022)**: Toy models of superposition — theoretical basis for SAEs
- **Bricken et al. (2023)**: Monosemanticity in one-layer transformers
- **Cunningham et al. (2023)**: Sparse autoencoders for LLM interpretability
- **Anthropic (2024)**: Scaling monosemanticity with SAEs

### Prior VLA Interpretability Work
- **Li et al. (2024)**: Probing VLA representations for task understanding
- **Brohan et al. (2023)**: RT-2 behavioral analysis — showed VLAs can generalize but didn't explain mechanistically

### Connections to Broader Robotics
- **Composable diffusion policies**: General features in VLAs connect to compositional action representation in diffusion models
- **Foundation model robotics**: This work provides mechanistic grounding for why foundation-model-based robots generalize better than task-specific policies

### Where This Research Leads
- **Feature-conditioned robot learning**: training objectives that explicitly maximize the "generality score" of learned features
- **Cross-embodiment transfer**: using general features as anchors for transferring policies between robot hardware
- **Multi-task VLA training**: understanding the mechanistic basis of task interference and benefit in multi-task learning

---

*Sources:*
- [arxiv.org/abs/2603.19183](https://arxiv.org/abs/2603.19183)
