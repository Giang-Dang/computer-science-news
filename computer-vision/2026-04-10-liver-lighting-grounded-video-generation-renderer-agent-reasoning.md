# LiVER: Lighting-Grounded Video Generation with Renderer-Based Agent Reasoning

**ArXiv ID:** [2604.07966](https://arxiv.org/abs/2604.07966)  
**Published:** April 10, 2026  
**Authors:** Ziqi Cai, Taoyu Yang, Zheng Chang, Si Li, Han Jiang, Shuchen Weng, Boxin Shi  
**Institutions:** Peking University, Beijing University of Posts and Telecommunications, Beijing Academy of Artificial Intelligence, OpenBayes Information Technology Co., Ltd.  
**Field:** Computer Vision / Generative Models / 3D Vision  

---

## Executive Summary

LiVER introduces a video generation framework that achieves precise, **disentangled control over lighting, object layout, and camera trajectory** in generated videos—properties that are tightly entangled and difficult to control independently in prior diffusion-based video generation models. By rendering control signals from a unified 3D scene representation and using a novel scene agent that translates high-level user instructions into 3D scene parameters, LiVER sets a new standard for controllable video generation. The framework achieves state-of-the-art photorealism and temporal consistency while enabling a wide range of applications including image-to-video synthesis with fully editable underlying 3D scenes.

---

## Problem Statement

Modern video diffusion models (Sora, Kling, Wan, etc.) generate highly realistic videos conditioned on text prompts. However, **fine-grained scene control** remains a fundamental challenge:

1. **Lighting**: Changing the lighting of a scene (sunlight to overcast, day to night, single spotlight) in a controlled way requires training data with diverse lighting conditions and complex conditioning mechanisms.

2. **Layout**: Precisely controlling the position, size, and movement of objects requires spatial conditioning that existing text-based control cannot provide.

3. **Camera trajectory**: While some models support basic camera movements (pan, zoom), specifying precise camera paths for cinematography is impossible with text prompts alone.

Critically, these three properties are **entangled** in current models: changing the lighting also changes shadows (which look like layout changes), and camera movement reveals new scene regions (which interact with lighting and layout). Separately controlling each property while keeping others fixed is not possible with existing approaches.

### Applications Demanding Precise Scene Control

The inability to precisely control lighting, layout, and camera trajectory severely limits video generation for:
- **Film production**: Cinematographers need precise control over lighting and camera
- **Virtual production**: VFX artists need to composite elements with matching lighting
- **Architectural visualization**: Clients want to see their building at different times of day
- **Game development**: Cinematics require precise control over all scene properties

---

## Core Concepts & Theory

### Unified 3D Scene Representation

LiVER's key architectural insight is to use a **unified 3D scene representation** that explicitly encodes:

```
Scene = {
    Objects: [(mesh_i, material_i, position_i)] for each object i
    Lighting: Environment map L (HDR) + local light sources [(type, position, intensity)]
    Camera: [position, orientation, FOV] for each frame
    Background: Implicit neural representation or skybox
}
```

By maintaining this explicit 3D representation, LiVER can:
- Change lighting independently (update L, re-render shadows)
- Move objects independently (update position_i)
- Change camera independently (update camera trajectory)

### Rendering-Based Control Signals

Rather than conditioning the video diffusion model directly on 3D scene parameters (which are high-dimensional and abstract), LiVER renders intermediate **control signal images** from the 3D scene:

| 3D Property | Rendered Control Signal |
|-------------|------------------------|
| Lighting | **Shadow map**: where shadows fall in the scene |
| Lighting | **Specular map**: how objects reflect light |
| Layout | **Normal map**: surface orientation of objects |
| Layout | **Depth map**: depth of each pixel from camera |
| Camera | **Optical flow**: how pixels move between frames |

These rendered control signals are 2D images that the diffusion model can condition on directly, using standard image-conditioning techniques (ControlNet-style).

### Lightweight Conditioning Module

LiVER introduces a **lightweight conditioning module** that injects control signals into the video diffusion backbone:

```python
# Standard video diffusion forward pass:
z_t, features = video_unet(z_t, text_embedding)

# LiVER conditioning:
control_signal = render_from_3d_scene(scene)  # rendered images
control_features = conditioning_module(control_signal)  # lightweight encoder
z_t = z_t + cross_attn(features, control_features)  # inject conditioning
```

The conditioning module is a lightweight convolutional network trained with the rest of the system, not a full UNet. This keeps the computational overhead minimal.

### Progressive Training Strategy

Training a model to simultaneously generate photorealistic video AND follow all three control signals is challenging. LiVER uses a **progressive training strategy**:

1. **Stage 1**: Train on text-to-video only (standard video diffusion training)
2. **Stage 2**: Fine-tune with single control signal (lighting only)
3. **Stage 3**: Fine-tune with all control signals simultaneously

This prevents conflicting gradients from different conditioning signals from destabilizing early training.

### Scene Agent for Natural Language Control

A key usability innovation is the **scene agent**: an LLM-based agent that translates high-level user instructions into 3D scene parameters:

```
User: "Make the lighting dramatic — late afternoon sun from the left"

Scene Agent:
  1. Parse lighting intent: "golden hour, directional"
  2. Set sun position: elevation=15°, azimuth=270° (west)
  3. Set sun color: temperature=3200K (warm)
  4. Reduce ambient: ambient_intensity=0.1
  5. Output: updated lighting parameters → LiVER rendering pipeline
```

The scene agent uses an LLM fine-tuned on (instruction, scene parameter) pairs, enabling non-expert users to control the 3D scene via natural language.

---

## Main Ideas & Key Contributions

### 1. Disentangled Control via 3D Scene Rendering

The first video generation framework to explicitly disentangle and independently control lighting, layout, and camera trajectory via explicit 3D scene representation and rendering.

### 2. Rendering-Based Control Signals

Using physically-based rendering to generate intermediate control signals (shadow maps, normal maps, depth maps, optical flow) that bridge the gap between abstract 3D scene parameters and the 2D inputs of video diffusion models.

### 3. Lightweight Conditioning Module

An efficient architecture for injecting multiple rendered control signals into a pretrained video diffusion backbone without full fine-tuning.

### 4. Scene Agent

An LLM-based agent that democratizes precise 3D scene control by accepting natural language instructions and translating them to scene parameters.

### 5. State-of-the-Art Controllable Video Generation

LiVER achieves SOTA on benchmarks for controllable video generation while maintaining the photorealism of the underlying diffusion model.

---

## Methodology & Implementation

### Architecture Overview

```
User Input (text + optional image)
        ↓
Scene Agent (LLM)
        ↓
3D Scene Parameters
{lighting, layout, camera}
        ↓
Renderer (e.g., Blender, custom rasterizer)
        ↓
Control Signal Images
{shadow map, normal map, depth map, optical flow}
        ↓
Lightweight Conditioning Module
        ↓                                    ↑
Video Diffusion Model ──────────────────────┘
(conditioned on control signals)
        ↓
Generated Video
```

### Dataset

LiVER introduces a new **large-scale dataset** with dense annotations:
- 100K+ video clips
- Each clip annotated with:
  - Camera parameters (position, orientation per frame)
  - Object bounding boxes (3D)
  - Lighting parameters (environment map + local lights)
  - Rendered control signals (shadow, normal, depth, flow)

This dataset fills a critical gap: existing video datasets lack dense 3D annotation.

### Evaluation Metrics

| Metric | Measures |
|--------|----------|
| FVD (Fréchet Video Distance) | Overall video quality |
| CLIP Score | Text-video alignment |
| Lighting Consistency Score | Correctness of shadow/specular rendering |
| Layout Accuracy | Object position accuracy (IoU) |
| Camera Trajectory Error | Camera path following accuracy |

### Baselines

LiVER is compared against:
- ControlNet-based video generation (single-condition)
- CameraCtrl (camera control only)
- LightVideo (lighting control only)
- Wan/Kling/Sora (no explicit control)

LiVER outperforms all on the combined controllability + quality evaluation.

---

## Practical Applications & Real-World Use Cases

### 1. Film and Content Production

Professional filmmakers and content creators can use LiVER to:
- Pre-visualize lighting setups before physically staging a shot
- Generate B-roll footage with precise lighting matching
- Create cinematic footage with specified camera movements

### 2. Virtual Production and VFX

VFX artists compositing CGI elements into live footage need generated content that matches the lighting and camera of the source footage. LiVER's explicit lighting control enables accurate match.

### 3. Architectural and Interior Design

Architects and designers can visualize how a space looks at different times of day (morning sunlight, evening ambiance) without expensive rendering—LiVER generates photorealistic video at a fraction of the cost of traditional 3D rendering software.

### 4. Video Game Cinematics

Game studios can use LiVER to rapidly prototype and generate cinematics with precise scene control before committing to expensive hand-crafted production.

### 5. Training Data Generation for Computer Vision

Computer vision models for depth estimation, surface normal prediction, and optical flow estimation require ground-truth data. LiVER can generate large-scale synthetic data with precise ground truth annotations for these tasks.

---

## Insights & Implications

### 3D Understanding as a Path to Controllable Generation

LiVER demonstrates that **explicit 3D scene representation is the right level of abstraction** for controllable video generation. 2D editing (applying filters, masks) is too superficial. Full neural 3D reconstruction (NeRF, Gaussian Splatting) is too expensive at scale. A lightweight 3D scene parameterization that can be rendered into control signals strikes the right balance.

### The Scene Agent: From Expert to Everyone

By automating the translation from natural language to 3D scene parameters, LiVER makes professional-quality controllable video generation accessible to non-expert users. This is analogous to how Stable Diffusion democratized image generation.

### Towards Physically Accurate Video Generation

LiVER's use of physical rendering (shadows, reflections, material properties) moves video generation closer to physically accurate simulation. This is especially valuable for scientific visualization, engineering applications, and any use case where physical plausibility matters.

### Limitations

- **3D scene estimation for in-the-wild videos**: For video-to-video synthesis, the 3D scene must be estimated from input footage, which is still an open problem for complex scenes
- **Dynamic objects**: The current 3D scene representation handles rigid objects well but struggles with deformable objects (cloth, hair, liquid)
- **Scale**: Large outdoor scenes with complex lighting (multiple bounces, atmospheric scattering) are still challenging

---

## Code & Resources

- **Paper (arXiv)**: [https://arxiv.org/abs/2604.07966](https://arxiv.org/abs/2604.07966)

**Dependencies**:
- PyTorch, HuggingFace diffusers
- Rendering: Blender Python API or custom rasterizer (PyTorch3D / nvdiffrast)
- Scene understanding: Depth estimation (Depth Anything), normal estimation, camera pose estimation (COLMAP)

**Computational Requirements**:
- Training: 8×H100 GPUs, ~1 week
- Inference: 1×A100 GPU, ~30s per video (depends on length and diffusion steps)

---

## Related Work & Context

### Controllable Video Generation
- **CameraCtrl**: Camera trajectory control for video generation
- **ControlNet**: Image control via intermediate representations (base for LiVER's conditioning)
- **IC-Light**: Lighting control for image generation (2D, not 3D)

### 3D-Aware Video Generation
- **Scene Dreamer**: 3D scene generation for video
- **CityRAG** (2604.19741): Spatially-grounded video generation
- **SceneScribe-1M** (2604.07990): Large-scale dataset for 3D scene video understanding

### Future Directions
- Video-to-video re-lighting and re-layout via 3D scene estimation
- Dynamic object support (clothes, hair, liquids)
- Integration with NeRF/Gaussian Splatting for higher fidelity 3D scenes
