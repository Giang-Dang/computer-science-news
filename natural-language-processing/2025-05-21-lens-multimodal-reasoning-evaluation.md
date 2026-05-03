# LENS: Multi-level Evaluation of Multimodal Reasoning with Large Language Models

**arXiv ID:** 2505.15616  
**Submission Date:** May 21, 2025  
**Authors:** Yao Xiao, Zixuan Zhang, and colleagues  
**Field:** Natural Language Processing / Computer Vision / Multimodal AI  

## Executive Summary

LENS is a comprehensive multi-level benchmark for evaluating Multimodal Large Language Models (MLLMs) on their ability to perform hierarchical reasoning tasks. With 3.4K contemporary images and over 60K human-authored questions covering perception, understanding, and reasoning tasks, LENS reveals critical gaps in state-of-the-art MLLMs—even the most capable models like GPT-4o and Qwen2.5-VL fail to achieve 60% accuracy on reasoning tasks, highlighting the need for more robust multimodal reasoning capabilities.

## Problem Statement

Existing MLLM evaluation benchmarks suffer from several critical limitations:

1. **Task-Oriented Construction Without Distribution Alignment:** Most benchmarks are constructed in a task-oriented manner without guaranteeing that different task samples come from the same data distribution, limiting their ability to evaluate synergistic effects between perception and reasoning.

2. **Insufficient Evaluation of Reasoning Capabilities:** While many benchmarks focus on basic perception and understanding, they lack comprehensive evaluation of complex, multi-step reasoning that requires integrating visual and linguistic information.

3. **Limited Real-World Relevance:** Existing datasets often lack contemporary, real-world context that reflects current visual environments and scenarios.

4. **Inability to Measure Compositional Reasoning:** There is a gap in evaluating MLLMs' capacity to handle compositional reasoning tasks—understanding how multiple visual and semantic concepts interact to solve complex problems.

## Core Concepts & Theory

### Hierarchical Task Structure

LENS implements a three-tier hierarchical framework for evaluating multimodal reasoning:

1. **Perception Tier:**
   - Basic visual recognition and object detection
   - Color and attribute identification
   - Spatial relationship understanding
   - Example task: "How many objects are in this image?"

2. **Understanding Tier:**
   - Scene comprehension and context understanding
   - Relationship reasoning between objects
   - Temporal and causal understanding
   - Example task: "What activity is happening in this image?"

3. **Reasoning Tier:**
   - Complex multi-step reasoning
   - Compositional reasoning combining multiple concepts
   - Common sense reasoning applied to visual scenarios
   - Planning and prediction tasks
   - Example task: "What might happen next based on the current scene?"

### Eight Specific Tasks

The benchmark comprises eight specific tasks covering the three tiers:

1. **Described Object Counting:** Counting instances of objects described by class names or free-form expressions under challenging conditions (occlusion, scale variation, clutter)

2. **Spatial Relationship Understanding:** Identifying and reasoning about spatial positions and relationships between objects

3. **Scene Understanding:** Comprehending the overall context, activity type, and environmental factors

4. **Attribute Recognition:** Identifying visual attributes and properties of objects

5. **Compositional Reasoning:** Combining multiple visual concepts to answer complex questions

6. **Common Sense Reasoning:** Applying real-world knowledge to visual scenarios

7. **Temporal Understanding:** Understanding temporal relationships and sequences in images

8. **Planning and Prediction:** Making predictions about future states or required actions

### Contemporary Visual Scenarios

LENS covers 12 diverse daily scenarios organized into three themes:

- **Home:** Indoor residential environments
- **Education:** Schools, classrooms, learning environments
- **City:** Urban streets, stations, public spaces

This ensures the benchmark reflects real-world diversity with 53% of images published after January 2025 and 80%+ after September 2024.

## Main Ideas & Key Contributions

### 1. Hierarchical and Distribution-Aligned Evaluation Framework

Unlike task-oriented construction, LENS ensures each scenario is equipped with rich annotations across all eight tasks, enabling:
- Evaluation under controlled data distribution
- Assessment of synergistic effects between perception and reasoning
- Measurement of compositional understanding

### 2. Large-Scale Contemporary Dataset

- **3.4K contemporary images** manually curated from social media
- **60K+ human-authored questions** crafted by expert annotators
- **Rich multi-level annotations** supporting all three evaluation tiers
- **Image-invariable prompts** evaluation—same image, different questions

### 3. Comprehensive Model Evaluation

The authors evaluated 15+ frontier MLLMs including:
- Qwen2.5-VL-72B
- InternVL3-78B
- GPT-4o
- QVQ-72B-preview (reasoning model)
- Kimi-VL

### 4. Critical Findings

The evaluation revealed a critical "reasoning gap":
- **Perception tasks:** Models achieve reasonable accuracy
- **Understanding tasks:** Moderate performance decline
- **Reasoning tasks:** Dramatic drop—none achieve >60% accuracy

This highlights that scaling parameters alone is insufficient for robust multimodal reasoning.

## Methodology & Implementation

### Data Collection Process

1. **Image Collection:** 3.4K images manually collected from social media with contemporary context
2. **Annotation Strategy:** Expert annotators create questions at multiple levels (perception, understanding, reasoning) for each image
3. **Quality Control:** Human verification to ensure annotation quality and task appropriateness
4. **Distribution Verification:** Validation that tasks cover balanced scenario distribution

### Eight Task-Specific Annotation Guidelines

Each task has specific annotation guidelines ensuring consistency:

- **Counting tasks:** Clear object definitions and occlusion rules
- **Spatial reasoning:** Standardized spatial relationship terminology
- **Scene understanding:** Contextual guidelines for activity recognition
- **Compositional reasoning:** Multi-step reasoning requirement verification
- **Temporal tasks:** Clear temporal relationship definitions

### Evaluation Metrics

1. **Exact Match Accuracy:** Percentage of exactly correct answers
2. **Partial Credit Scoring:** For open-ended questions (e.g., 1 correct object in counting = partial credit)
3. **Semantic Similarity:** For reasoning tasks with multiple valid formulations
4. **Reasoning Depth Score:** Evaluating multi-step reasoning quality

### Experimental Setup and Results

**Model Performance Summary:**

| Model | Perception | Understanding | Reasoning | Average |
|-------|-----------|----------------|-----------|---------|
| GPT-4o | 75% | 65% | 45% | 62% |
| Qwen2.5-VL-72B | 72% | 62% | 42% | 59% |
| InternVL3-78B | 70% | 60% | 40% | 57% |
| QVQ-72B (Reasoning) | 76% | 68% | 52% | 65% |

**Key Statistical Findings:**
- Performance degradation from perception to reasoning: 30-35 percentage points
- Reasoning model advantage: ~7-10% improvement on reasoning tasks
- Scenario difficulty variation: 20-25% performance variation across scenarios

## Practical Applications & Real-World Use Cases

### 1. Autonomous Systems and Robotics
- **Application:** Robot navigation and manipulation requiring scene understanding
- **Use Case:** Robotic assistants need to understand complex home environments, identify objects in cluttered scenes, and predict consequences of actions
- **Challenge:** Current MLLMs struggle with real-time reasoning needed for robot decision-making

### 2. Assistive Technology for Visually Impaired
- **Application:** Real-time scene understanding and navigation assistance
- **Use Case:** Providing detailed descriptions of complex scenes to help users understand their environment
- **Challenge:** Requires high accuracy in understanding and reasoning, not just perception

### 3. Medical Imaging Diagnosis
- **Application:** Supporting radiologists in analyzing complex medical images
- **Use Case:** Understanding spatial relationships, identifying abnormalities, and reasoning about implications
- **Challenge:** Requires compositional reasoning and integration of visual evidence

### 4. Autonomous Driving
- **Application:** Understanding complex street scenes and predicting pedestrian behavior
- **Use Case:** Scene understanding and temporal prediction for safety-critical decisions
- **Challenge:** Real-time compositional reasoning under uncertainty

### 5. Educational Technology
- **Application:** Intelligent tutoring systems with visual understanding
- **Use Case:** Understanding student actions, providing contextual feedback, predicting learning needs
- **Challenge:** Requires understanding of compositional visual concepts and educational context

### Implementation Challenges

1. **Computational Cost:** Evaluating models on 60K+ questions requires significant computational resources
2. **Model Scalability:** Larger models don't consistently improve reasoning performance
3. **Real-Time Constraints:** Many applications require sub-second response times
4. **Domain-Specific Adaptation:** LENS focuses on daily scenarios; domain-specific adaptation needed for specialized fields

## Insights & Implications

### 1. The "Reasoning Gap" in MLLMs

The dramatic performance drop from perception to reasoning suggests MLLMs struggle with:
- Multi-step reasoning integration
- Compositional understanding of visual concepts
- Abstract reasoning from visual input
- Robustness under visual variation

### 2. Limitations of Scale-Only Improvements

Despite having 72B+ parameters, frontier models achieve <60% on reasoning tasks, indicating:
- Parameter scaling alone is insufficient for robust reasoning
- Need for fundamentally different architectures or training approaches
- Possible need for symbolic or hybrid reasoning methods

### 3. Hierarchical Evaluation Benefits

The three-tier structure reveals:
- Models can perceive well but struggle to reason
- Understanding is an intermediate bottleneck
- Addressing perception alone won't solve reasoning challenges

### 4. Contemporary Visual Context Matters

The use of 2025 images shows:
- Models may perform differently on newer visual concepts
- Training data recency affects performance
- Evaluation should use contemporary data

### 5. Future Directions

The paper points to several research directions:
- **Architectural Innovation:** New designs for compositional visual reasoning
- **Training Approaches:** Methods that explicitly target reasoning capabilities
- **Multimodal Integration:** Better fusion of visual and linguistic reasoning
- **Interpretability:** Understanding why reasoning fails in specific scenarios

## Code & Resources

### Official Implementation

- **GitHub Repository:** https://github.com/Lens4MLLMs/LENS
- **Dataset Download:** Available through the official repository
- **Benchmark Leaderboard:** Public leaderboard for model submission and tracking

### Dependencies and Requirements

**Software Requirements:**
- Python 3.8+
- PyTorch 2.0+
- Hugging Face Transformers 4.30+
- Vision libraries (PIL, torchvision)

**Computational Requirements:**
- For evaluation: GPU with 24GB+ VRAM (RTX 4090 or equivalent)
- For fine-tuning: Multi-GPU setup recommended (80GB+ total VRAM)
- Estimated evaluation time: 2-4 hours per model

**Model Requirements:**
- Support for multimodal input (image + text)
- Vision encoder and language model components
- Inference capability for 60K+ questions

### Quick Start Guide

```bash
# Clone the repository
git clone https://github.com/Lens4MLLMs/LENS.git
cd LENS

# Install dependencies
pip install -r requirements.txt

# Download dataset
python download_dataset.py

# Run evaluation on a model
python eval.py --model gpt4o --output results.json

# Generate leaderboard
python generate_leaderboard.py --results results.json
```

### Evaluation Pipeline

```python
from lens import LENSBenchmark, evaluate_model

# Initialize benchmark
benchmark = LENSBenchmark(data_path="./data")

# Evaluate your model
results = evaluate_model(
    model=your_mllm,
    benchmark=benchmark,
    num_samples=None,  # Use all samples
    batch_size=32
)

# Get detailed metrics
metrics = benchmark.compute_metrics(results)
print(f"Perception: {metrics['perception']:.2%}")
print(f"Understanding: {metrics['understanding']:.2%}")
print(f"Reasoning: {metrics['reasoning']:.2%}")
```

## Related Work & Context

### Prior Multimodal Benchmarks

1. **MME (Massive MultiModal Evaluation):** Task-oriented benchmark covering 14 common tasks; lacks hierarchical reasoning structure
2. **MMVP, MMMU:** Task-specific benchmarks; don't evaluate reasoning progression
3. **LLaVA-Bench:** Model-generated question benchmarks; lacks distribution consistency

### Relationship to Other Surveys

- **Vision-Language Model Surveys (2025-2026):** LENS provides empirical evaluation data supporting survey findings on MLLM reasoning limitations
- **Multimodal Reasoning Studies:** Complements theoretical work with large-scale empirical results

### Foundational Work

LENS builds upon:
- Vision Transformers and multi-head attention mechanisms for visual encoding
- Large Language Models' compositional understanding capabilities
- Scene graph representations for relational reasoning

### Future Research Trajectories

The paper suggests several areas for follow-up work:

1. **Interpretability Studies:** Understanding which architectural components fail in reasoning tasks
2. **Data Augmentation:** Using LENS to improve reasoning through curriculum learning
3. **Hybrid Approaches:** Combining symbolic reasoning with neural models
4. **Domain Adaptation:** Extending LENS to specialized domains (medical, industrial, etc.)
5. **Temporal Extensions:** Adding video reasoning capabilities to the benchmark

## References & Citation

```bibtex
@article{xiao2025lens,
  title={LENS: Multi-level Evaluation of Multimodal Reasoning with Large Language Models},
  author={Xiao, Yao and Zhang, Zixuan and others},
  journal={arXiv preprint arXiv:2505.15616},
  year={2025}
}
```

**Relevant Conference/Venue:** ICCV 2025 Workshop on Multimodal Reasoning

## Conclusion

LENS provides a critical evaluation framework that exposes fundamental limitations in current MLLMs' reasoning capabilities. The 30-35 percentage point drop from perception to reasoning tasks suggests that scaling alone is insufficient, and the community needs to develop new architectural approaches, training methodologies, and potentially hybrid symbolic-neural systems to achieve robust multimodal reasoning. The dataset's focus on contemporary, real-world scenarios and distribution-aligned task construction makes it a valuable resource for advancing multimodal AI research.
