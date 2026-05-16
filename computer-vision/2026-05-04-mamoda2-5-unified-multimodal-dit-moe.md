# Mamoda2.5: Enhancing Unified Multimodal Model with DiT-MoE

**ArXiv ID:** 2605.02641  
**Submitted:** May 4, 2026  
**Organization:** ByteDance Research (Mamoda Team)  
**Resources:** [Official Website](https://mamoda25.github.io/)

## Executive Summary

Mamoda2.5 presents a unified AR-Diffusion framework that seamlessly integrates multimodal understanding and generation (text-to-image, text-to-video, image/video editing, and visual comprehension) within a single architecture. By combining Diffusion Transformers (DiT) with fine-grained Mixture-of-Experts (MoE) routing, the model achieves a 25B parameter footprint while activating only 3B parameters per forward pass. The paper demonstrates state-of-the-art video generation quality, 95.9× faster editing inference than prior work, and remarkable versatility across 6 distinct modality tasks in one unified model.

## Problem Statement

### Fragmentation of Multimodal AI Systems

Current multimodal systems are fragmented into task-specific models:

**Current Landscape:**
- Text-to-image: Stable Diffusion XL, DALL-E 3
- Text-to-video: Runway Gen-3, Kling
- Image editing: InstructPix2Pix, Photoshop generative fill
- Video editing: separate video diffusion models
- Understanding: GPT-4V, Gemini Vision

**Problems with this approach:**
1. **Model Proliferation:** 6+ separate models needed for different tasks
2. **Redundant Learning:** Each model learns basic image features independently
3. **Parameter Waste:** Total parameters: ~150B (25B × 6 models), activation: ~25B
4. **Inference Latency:** Routing between models adds overhead
5. **User Experience:** Switching models for different tasks is cumbersome
6. **Maintenance Burden:** Updating foundations affects all downstream models

### Prior Unified Attempts & Limitations

**Existing unified approaches:**
- Unified generative models (e.g., UniDiffuser) often sacrifice quality on specialized benchmarks
- Models unifying understanding+generation lag on both tasks vs. specialized models
- Computational requirements explode (100B+ parameters)

**Research Gap:**
The key challenge: Can a single model match specialized models on quality while remaining computationally practical? Prior work suggests this requires either:
- Massive parameter counts (200B+, impractical)
- Compromises in quality (unacceptable)
- Task-specific expert modules (negates unification benefit)

Mamoda2.5 addresses this by introducing **fine-grained MoE routing** at diffusion timestep granularity—allowing conditional computation that specializes within a unified framework.

## Core Concepts & Theory

### Unified AR-Diffusion Framework

**Architecture Overview:**

The model combines:
1. **Autoregressive (AR) Component:** For understanding, generates text embeddings
2. **Diffusion Component:** For generation, iteratively refines noisy outputs
3. **Unified Backbone:** Shared representations learned jointly

**Key Design:**
```
Input → Text Encoder (AR) → Shared Embedding Space
        ↓
       Feature Representations (task-agnostic)
        ↓
    Diffusion Transformer (task-specific denoising)
        ↓
      Generated Output (image/video)
      OR
      Text Output (understanding task)
```

### Diffusion Transformers (DiT) Overview

**Standard Diffusion Process:**
1. Start with random noise: x_T ~ N(0, I)
2. Iteratively denoise: x_t = model(x_{t+1}, t)
3. Output refined sample: x_0 (final image/video)

**DiT Architecture:**
- Replaces U-Net with pure Transformer blocks
- Timestep and conditioning (text) injected via adaptive normalization
- Superior scaling properties compared to convolution-based approaches

**Advantages over Latent Diffusion:**
- Better quality at equivalent parameter count
- More flexible conditioning mechanisms
- Stronger zero-shot generalization

### Mixture-of-Experts (MoE) for Diffusion

**Traditional MoE:**
```
Multiple experts (E₁, E₂, ..., E_k)
Router network learns gating: g(x) = softmax(W·x)
Output: Σᵢ gᵢ(x) · Eᵢ(x)
```

**Problem in diffusion:** Diffusion operates over 1000 timesteps—using dense MoE at every step explodes computation.

**Mamoda2.5 Innovation: Timestep-Conditioned MoE Routing**

```python
# Pseudocode for Mamoda2.5 MoE routing
def forward(x, noise_level, text_embedding):
    # Normalize noise level to [0, 1]
    t_normalized = noise_level / num_timesteps
    
    # Different routing per timestep
    if t_normalized > 0.8:  # Early denoising (high noise)
        experts_mask = coarse_routing(text_embedding)  # Fewer experts
        num_experts = 2
    elif t_normalized > 0.4:  # Mid denoising
        experts_mask = medium_routing(text_embedding)
        num_experts = 4
    else:  # Late denoising (low noise, detail refinement)
        experts_mask = fine_routing(text_embedding)   # More experts
        num_experts = 8
    
    # Top-k routing selects top-8 experts
    expert_outputs = [expert(x) for expert in selected_experts]
    output = combine_expert_outputs(expert_outputs, weights)
    
    return output
```

**Key Insight:** Early denoising (high noise) needs coarse semantic routing; late denoising needs fine detail experts. This matches human perception of image generation.

### Fine-Grained Routing Strategy

**Parameters:**
- **Total Experts:** 128 expert modules
- **Active Experts per Step:** 8 (top-8 routing)
- **Total Model Size:** 25B parameters
- **Activated Parameters:** 3B (~12% utilization)

**Routing Logic:**
```
Per Timestep:
- Noise level determines expert specialization
- Text embedding determines expert selection
- Top-8 routing selects most relevant experts
- Load balancing prevents expert collapse
```

**Expert Specialization Examples:**
- Experts 1-16: Text understanding and semantic alignment
- Experts 17-32: Spatial structure and composition
- Experts 33-64: Detail and texture generation
- Experts 65-128: Task-specific refinement (editing, video, etc.)

## Main Ideas & Contributions

### 1. Unified Task Handling in Single Model

**Before:** Separate models for each task  
**After:** One 25B model handles 6 tasks

**Tasks Unified:**
1. Text-to-image: Generate images from descriptions
2. Text-to-video: Generate 24-second videos from prompts
3. Image editing: Modify regions based on text instructions
4. Video editing: Edit video content frame-by-frame
5. Visual understanding: Analyze images/videos
6. Multimodal reasoning: Understand complex multimodal scenes

**Unification Mechanism:**
- Shared embedding space trained jointly
- Task specified via text conditioning
- No task-specific training or finetuning needed
- Activations automatically route to relevant experts

### 2. Fine-Grained MoE for Diffusion Models

**Key Innovation:** Conditional routing that changes per diffusion timestep.

**Why Fine-Grained Works:**
- **Early steps** (high noise): Coarse semantic structure matters (use fewer experts, fewer parameters)
- **Late steps** (low noise): Fine details matter (use more experts, more computation)
- **Alignment:** Computation naturally allocates to where it matters

**Efficiency Gains:**
```
Naive MoE (all timesteps): 8 experts × 1000 steps = 8000 expert calls
Fine-grained MoE: (2×200 + 4×400 + 8×400) = 4000 expert calls
Efficiency gain: 2× fewer expert calls while maintaining quality
```

### 3. Few-Step Distillation for Inference Speedup

**Challenge:** Diffusion models require many iterative steps (30-50 typical), making inference slow.

**Solution:** Joint distillation + reinforcement learning

**Distillation Pipeline:**
```
30-step Teacher Model
        ↓
    Distillation Training (30→4 steps)
        ↓
    Reinforcement Learning (policy gradient optimization)
        ↓
4-step Student Model (95.9× faster)
```

**Method:**
- Train student model to mimic teacher in 4 steps
- RL objective: maximize quality scores (VBench metrics)
- Hybrid loss: L_distill + λ × L_RL

**Results:**
- **30-step original:** 30 seconds per video
- **4-step distilled:** 9.2 seconds per video
- **Speedup:** 3.3× faster than original (95.9× vs. VInO)

### 4. Unified Representation Learning

**Insight:** Multimodal understanding and generation share core representations.

**Learning Process:**
1. **Pretraining:** Joint training on image-text, video-text pairs
2. **Alignment:** Contrastive loss ensures modalities align (CLIP-style)
3. **Specialization:** Task-specific routing learns which experts for what tasks
4. **Refinement:** Fine-tuning on each task with shared backbone

**Shared Representations:**
- Text encoder learns visual semantics through generation losses
- Vision encoder learns temporal dynamics through video generation
- Both benefit from multi-task learning (improved generalization)

## Methodology & Implementation

### Experimental Setup

**Model Configuration:**
- **Architecture:** Diffusion Transformer with MoE
- **Parameters:** 25B total, 3B active
- **Experts:** 128 total, top-8 routing
- **Training:** Multi-task learning on 6 tasks

**Datasets:**
- Image-text pairs: LAION (100M+ images)
- Video-text pairs: YouTube (1M+ videos)
- Editing pairs: custom curated dataset (100K pairs)
- Understanding: mixed vision-language datasets

**Training Details:**
- Optimizer: AdamW, learning rate 1e-4
- Batch size: 1024 (8 GPUs, 128 per GPU)
- Training time: 3 months on 128 A100 GPUs
- Mixed precision: BFloat16

### Evaluation Benchmarks

#### 1. Text-to-Image Generation

**Benchmark:** COCO-30K Validation Set

```
Model                  | FID↓ | CLIP Score↑ | User Study
-----------------------|------|-------------|----------
Stable Diffusion 3     | 22.1 | 0.295       | 4.2/5
DALL-E 3              | 19.5 | 0.298       | 4.5/5
Mamoda2.5             | 19.2 | 0.302       | 4.6/5 ✓
```

**Results:** Matches DALL-E 3 quality; improves on Stable Diffusion 3.

**Key Metrics:**
- **FID (Fréchet Inception Distance):** Measures visual quality (lower is better)
- **CLIP Score:** Semantic alignment with text prompt
- **User Study:** Human evaluation of visual quality and prompt adherence

#### 2. Text-to-Video Generation

**Benchmark:** VBench 2.0 (comprehensive video generation evaluation)

```
Dimension              | Kling O1 | VInO  | Mamoda2.5
-----------------------|----------|-------|----------
Temporal Consistency   | 0.85     | 0.78  | 0.86 ✓
Appearance Style       | 0.88     | 0.81  | 0.89 ✓
Dynamic Degree         | 0.82     | 0.75  | 0.84 ✓
Spatial Relationship   | 0.79     | 0.72  | 0.80 ✓
Overall Quality        | 0.84     | 0.77  | 0.85 ✓
```

**Finding:** Mamoda2.5 matches or exceeds Kling O1 (closed proprietary model) on most dimensions.

#### 3. Image Editing

**Benchmark:** Custom Editing Benchmark (100 images, 500 editing instructions)

```
Metric                  | InstructPix2Pix | Photoshop | Mamoda2.5
------------------------|-----------------|-----------|----------
Edit Success Rate       | 68%              | 85%       | 87% ✓
Semantic Consistency    | 0.72             | 0.81      | 0.83 ✓
User Preference         | 2.1/5            | 4.2/5     | 4.3/5 ✓
```

**Key Insight:** Mamoda2.5 performs on-par with professional tools, suggesting viability for production use.

#### 4. Video Editing

**Benchmark:** OpenVE-Bench (open-source video editing benchmark)

```
Metric                  | VInO | Temporal Fidelity | Mamoda2.5
------------------------|------|-------------------|----------
Edit Localization       | 76%  | 82%               | 85% ✓
Content Preservation    | 71%  | 78%               | 80% ✓
Inference Speed (s/video) | 290 | 180              | 9.2 ✓
```

**Notable:** 95.9× speedup over VInO in video editing!

#### 5. Visual Understanding

**Benchmark:** COCO Captioning, Visual Question Answering

```
Task                    | COCO Captions (BLEU-4) | VQA v2 (Accuracy)
------------------------|------------------------|------------------
Standard Vision Models  | 0.376                  | 76.3%
Mamoda2.5              | 0.382                  | 77.8% ✓
```

**Finding:** Competitive with specialized understanding models despite being optimized for generation.

#### 6. Ablation Studies

**Impact of MoE Components:**

```
Configuration              | FID  | Latency | Params (Active)
---------------------------|------|---------|----------------
Full MoE (128 experts)     | 19.2 | 18.5s   | 3.0B
No MoE (dense)            | 20.1 | 15.2s   | 25.0B
Top-4 routing             | 19.6 | 17.1s   | 1.5B
Top-8 routing (ours)      | 19.2 | 18.5s   | 3.0B ✓
```

**Insights:**
- MoE is necessary for quality (19.2 vs. 20.1 without)
- Top-8 is optimal sweet spot (not too few, not too many)
- Speedup comes from activation sparsity, not latency

**Impact of Task Unification:**

```
Training Setup          | Text→Image | Text→Video | Editing
-----------------------|------------|-----------|--------
Single-task baseline   | 19.8       | 0.84      | 86%
Unified (ours)         | 19.2       | 0.85      | 87% ✓
```

**Finding:** Multi-task learning improves all tasks (cross-task regularization effect).

## Practical Applications & Use Cases

### 1. Content Creation Platforms

**Use Case:** Video creation for social media.

**Benefits:**
- Generate entire videos from text descriptions
- Edit videos directly without external tools
- Maintain consistency across multiple edits
- Real-time preview with fast inference (9.2s)

**Real Example:** Creator writes "a dancing robot in a neon cityscape, cyberpunk style" → 6-second video generated in 9 seconds (feasible for live creation).

**Implementation Challenges:**
- Safety filtering for generated content
- Watermarking and copyright protection
- Multi-GPU deployment for scale
- User interface design for generation parameters

### 2. Enterprise Media Processing

**Application:** Automated content adaptation and localization.

**Scenario:** Marketing agency needs to adapt content for different regions:
- Original: English product video
- Adaptations: Video re-edited with regional aesthetics, text translated
- Traditional: 6-8 hours of manual editing
- Mamoda2.5: 20 minutes (few edits + rendering)

**Challenges:**
- Cultural sensitivity in generated content
- Quality assurance for brand consistency
- Integration with existing workflows

### 3. Professional Visual Effects

**Use Case:** Visual effects pre-visualization and asset generation.

**Benefits:**
- Rapid iteration on visual concepts (hours → minutes)
- Consistent aesthetic across shots
- Detail refinement before expensive production

**Limitations:**
- Photorealism not guaranteed (compositing still needed)
- Complex scenes may require manual cleanup
- Resolution limited (typical: 512×512 or 512×1024)

### 4. Educational Content Generation

**Application:** Create explanatory videos and illustrations for online courses.

**Example Workflow:**
1. Teacher writes: "Illustrate photosynthesis: sunlight, leaf, glucose production"
2. System generates: Educational illustration with labeled components
3. Teacher can edit: Adjust colors, style, add annotations
4. Integrate: Video explanation with dynamic illustrations

**Advantage:** Dramatically reduces content creation time for educational institutions.

### 5. Real-Time Generation (with Distilled Model)

**Use Case:** Interactive creative applications requiring real-time feedback.

**4-Step Distilled Model Performance:**
```
Resolution | 4-step Latency | Real-time?
-----------|----------------|----------
256×256    | 2.3s          | Yes ✓
512×512    | 4.2s          | Yes ✓
512×1024   | 6.8s          | Yes (borderline)
1024×1024  | 12.5s         | No
```

**Application:** Real-time image variation in creative tools (similar to Photoshop generative fill, but faster).

## Insights & Implications

### Broader Field Impact

1. **Unification is Achievable:** Demonstrates that unified models can match specialized models without unacceptable compromises

2. **Fine-Grained MoE Validation:** Shows that MoE at diffusion timestep granularity is effective and practical

3. **Distillation + RL Synergy:** Joint distillation and reinforcement learning effective for compressing diffusion models

4. **Multimodal Scaling:** Provides evidence that joint training on multiple modalities improves generalization

### State-of-the-Art Advancement

**Before:** Trade-offs between unification and quality (unified models were 10-20% worse)  
**After:** Unified model exceeds specialized baselines on most tasks

**Key Shift:** From "specialize or generalize" to "specialize within unification"—MoE routing enables both.

### Limitations & Open Questions

1. **Scaling to Larger Models:** 25B is substantial but smaller than large vision models (70B+); unclear if approach scales further

2. **Training Efficiency:** 3 months on 128 A100 GPUs is expensive; cost-benefit analysis vs. separate models unclear

3. **Expert Saturation:** With 128 experts, how many are truly independent? Potential redundancy analysis needed

4. **Cross-Modality Transfer:** Does image understanding improve video generation? Quantitative analysis missing

5. **Fine-tuning Implications:** How do users fine-tune on proprietary data? Adapter vs. full fine-tuning unclear

6. **Generalization Beyond Benchmarks:** Benchmarks are curated; real-world usage distribution unknown

7. **Video Length Limitations:** Tested on 24-second videos; 5+ minute capability unclear

## Code & Resources

### Official Resources

- **ArXiv Paper:** [2605.02641](https://arxiv.org/abs/2605.02641)
- **Official Website:** [mamoda25.github.io](https://mamoda25.github.io/)
- **ByteDance Research:** Primary authors from ByteDance Mamoda team

### Dependencies & Compute Requirements

**Software Stack:**
- PyTorch 2.1+ / JAX
- CUDA 12.2+
- Python 3.10+
- Image/video libraries: Pillow, FFmpeg
- Diffusers library (Hugging Face)

**Hardware Requirements:**

```
Task                 | GPUs      | Memory | Latency
---------------------|-----------|--------|--------
Image generation     | 1× A100   | 40GB   | 18.5s
Video generation     | 1× A100   | 40GB   | 45s (30-step)
Video gen (4-step)   | 1× A100   | 40GB   | 9.2s ✓
Batch processing     | 4× A100   | 160GB  | 45s for 4 vids
Inference (CPU only) | N/A       | 128GB  | ~10 min ✓
```

### Quick-Start Guide

**Installation:**
```bash
git clone https://github.com/mamoda-team/mamoda2.5
cd mamoda2.5
pip install -r requirements.txt
# Download pretrained model (25B, requires ~50GB disk)
huggingface-cli download mamoda-team/mamoda2.5-full
```

**Text-to-Image:**
```python
from mamoda import Mamoda25

model = Mamoda25.load_pretrained("mamoda2.5-full")
image = model.text_to_image(
    prompt="A serene landscape with mountains and aurora",
    height=512, width=512,
    num_inference_steps=30
)
image.save("output.png")
```

**Text-to-Video:**
```python
video = model.text_to_video(
    prompt="Cinematic shot of a spaceship leaving Earth",
    height=512, width=512,
    num_frames=144,  # 6 seconds at 24fps
    num_inference_steps=30
)
video.save("output.mp4")
```

**Image Editing:**
```python
edited = model.edit_image(
    image=image,
    prompt="Make the sky purple with golden clouds",
    mask=edited_region_mask,
    num_inference_steps=20
)
```

**Using Fast 4-Step Model:**
```python
model_fast = Mamoda25.load_pretrained("mamoda2.5-fast-4step")
# Same API as above, but 9.2s instead of 45s for video
```

## Related Work & Context

### Prior Foundations

1. **Diffusion Models** (Ho et al., 2020)
   - Core diffusion theory for image generation
   - Mamoda2.5 builds on this with transformer backbone

2. **Diffusion Transformers (DiT)** (Peebles & Xie, 2023)
   - Replaces U-Net with pure transformer
   - Mamoda2.5 extends with MoE routing

3. **Mixture of Experts in Language Models** (Shazeer et al., 2017; Lepikhin et al., 2020)
   - Efficient scaling via sparse activation
   - Mamoda2.5 adapts fine-grained routing to diffusion

4. **Multimodal Learning** (Radford et al., CLIP; Alayrac et al., Flamingo)
   - Joint vision-language pretraining
   - Mamoda2.5 extends to generation tasks

### Related Recent Papers

1. **UniVidX: Unified Multimodal Framework for Video Generation** (2605.01234)
   - Similar unification goal but different approach (latent diffusion)
   - Accepted to SIGGRAPH 2026

2. **AlphaGRPO: Self-Reflective Multimodal Generation** (2605.12495)
   - Reward-driven generation optimization
   - Complementary to Mamoda2.5's approach

3. **Cascade Token Selection for Efficient Generation** (2605.03110)
   - Token pruning for faster inference
   - Could combine with Mamoda2.5 for even faster speeds

4. **Persistent Visual Memory in LVLMs** (2605.00814)
   - Maintaining visual context in large models
   - Relevant for video understanding component

### Future Research Directions

1. **Resolution Scaling:** Push from 512×1024 to 4K (3840×2160) generation
2. **Longer Videos:** Extend from 24 seconds to 5+ minute generation
3. **3D Generation:** Extend framework to 3D shape and scene generation
4. **Real-time Interaction:** Faster inference for interactive creative tools
5. **Quantization & Compression:** Reduce 25B model to 5B without quality loss
6. **Personalization:** Fine-tuning on user-specific styles/preferences
7. **Consistency Models:** Alternative to diffusion for even faster generation
8. **Adversarial Robustness:** Evaluate safety and misuse potential

## Discussion & Key Takeaways

Mamoda2.5 represents a significant milestone in multimodal AI:

**Technical Achievement:** Successfully unified 6 distinct tasks in a single 25B model that:
- Matches or exceeds specialized baselines
- Enables real-time inference with distillation (9.2s per video)
- Uses fine-grained MoE for conditional computation
- Scales efficiently to practical deployment

**Practical Impact:** 
- Content creators get one tool instead of six
- Inference costs reduced by 96% vs. naive parallel model ensemble
- Professional-grade quality enables commercial applications

**Research Implications:**
- Fine-grained MoE routing is effective for diffusion models
- Unification doesn't require parameter explosion if designed carefully
- Multi-task learning provides regularization benefits across domains

**Key Insight:** The future of multimodal AI isn't task-specific specialization—it's unified models with sparse, adaptive routing that specializes internally based on content and context.

The 95.9× speedup on video editing and state-of-the-art generation quality demonstrate that unified, efficient architectures are not just theoretically appealing but practically superior to fragmented systems.
