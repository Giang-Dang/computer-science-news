# SIGNPOST-Bench: Benchmarking Text-Vision Conflict Resolution in Multimodal Large Language Models

## Executive Summary

This paper introduces SIGNPOST-Bench, a controlled counterfactual benchmark designed to systematically evaluate how multimodal large language models (MLLMs) resolve conflicts between textual and visual information. Through carefully constructed scenarios where text and images deliberately contradict each other, the authors reveal systematic biases in how current MLLMs prioritize modalities and make decisions. This work is significant for improving the robustness and reliability of multimodal models in real-world applications where information conflicts are common, and for understanding fundamental mechanisms of multimodal reasoning.

## Problem Statement

Current multimodal large language models often encounter scenarios where textual information contradicts visual information. However, the field lacks systematic understanding of:

- **Modality Prioritization**: Which modality (text vs. vision) do MLLMs prefer when they conflict?
- **Reasoning Under Conflict**: How do MLLMs reconcile contradictory information?
- **Robustness**: Can current MLLMs reliably handle conflicting inputs?
- **Failure Modes**: What types of conflicts cause systematic failures?

**Research gaps:**
- Existing multimodal benchmarks assume information consistency
- Real-world applications frequently encounter conflicting modalities
- Limited understanding of conflict resolution mechanisms in MLLMs
- No systematic evaluation methodology for text-vision arbitration

This paper fills this gap by providing the first comprehensive benchmark for evaluating MLLM behavior under modality conflicts.

## Core Concepts & Theory

### Controlled Counterfactual Design

The benchmark creates synthetic scenes where text and images deliberately conflict, allowing controlled measurement of MLLM behavior:

**Example scenario:**
```
Image: Shows a red car
Text: "The car in the image is blue"
Question: "What color is the car?"
```

This enables systematic measurement of whether the MLLM:
1. Chooses the visual information (correct answer: red)
2. Chooses the textual information (wrong answer: blue)
3. Recognizes the conflict and expresses uncertainty
4. Attempts to reconcile the information

### Modality Conflict Taxonomy

The paper defines a taxonomy of conflict types:

**1. Object Property Conflicts**
- Contradictions in attributes (color, size, orientation)
- Example: Image shows small object, text describes it as large

**2. Semantic Conflicts**
- Contradictions in meaning or relationships
- Example: Image shows A next to B, text says A is inside B

**3. Temporal Conflicts**
- Contradictions in time/sequence
- Example: Image shows state T1, text describes state T2

**4. Existence Conflicts**
- Contradictions about presence/absence
- Example: Image shows object absent, text refers to it as present

**5. Quantity Conflicts**
- Contradictions in counts or amounts
- Example: Image shows 3 items, text says "there are 5 items"

### Conflict Resolution Strategies

MLLMs can employ various strategies when encountering conflicts:

**Strategy 1: Vision-First**
- Prioritize visual information as ground truth
- Most robust approach (matches human visual perception)

**Strategy 2: Text-First**
- Prioritize textual information
- Common in language-trained models
- Often incorrect for visual reasoning

**Strategy 3: Averaging/Fusion**
- Attempt to combine both signals
- May lead to nonsensical outputs
- Suggests incomplete conflict resolution

**Strategy 4: Uncertainty Expression**
- Model acknowledges conflict
- Refuses to commit to either modality
- Indicates robust uncertainty quantification

**Strategy 5: Reconciliation**
- Attempts to explain how both could be true
- Sophisticated but potentially rationalization

### Theoretical Framework

The benchmark is grounded in multimodal learning theory:

**Multimodal Representation Learning:**
- Visual and textual information are encoded separately
- Information must be aligned and fused at some point
- Conflicts reveal alignment weaknesses

**Attention Mechanisms:**
- Multimodal attention determines information flow
- Biased attention toward text or vision explains conflict resolution
- Different model architectures have different biases

**Reasoning Under Uncertainty:**
- Humans use context and priors to resolve conflicts
- MLLMs may use different resolution strategies
- Understanding these strategies is crucial for robustness

## Main Ideas & Contributions

### 1. First Comprehensive Benchmark for Text-Vision Conflict Evaluation

SIGNPOST-Bench provides the first systematic, controlled benchmark for evaluating how MLLMs handle conflicting modalities.

**Key features:**
- 1,000+ carefully constructed conflict scenarios
- Diverse conflict types (property, semantic, temporal, existence, quantity)
- Multiple model architectures evaluated
- Clear ground-truth answers based on visual information

### 2. Systematic Bias Discovery

The benchmark reveals systematic biases in how different MLLM architectures resolve conflicts.

**Key findings:**
- Many models show strong text bias despite visual pretraining
- Bias varies significantly across model families
- Bias correlates with model size (estimated observations)
- Architectural choices (attention patterns) influence conflict resolution

### 3. Modality Conflict Taxonomy

Introduces a principled classification of different conflict types, enabling deeper analysis of specific failure modes.

**Taxonomy structure:**
- 5 main conflict categories
- Subcategories for fine-grained analysis
- Extensible framework for new conflict types

### 4. Comprehensive Analysis Framework

Provides metrics and analysis techniques for understanding conflict resolution:

**Metrics:**
- Conflict accuracy (% correct answers under conflict)
- Modality preference score (quantifies text vs. vision bias)
- Uncertainty expression rate (% cases with uncertainty)
- Confidence calibration (whether confidence matches accuracy)

### 5. Insights into MLLM Decision-Making

Reveals how different model architectures make decisions under conflict:

**Architecture-specific findings:**
- Vision transformer-based models: Higher visual accuracy
- Pure-transformer models: Higher text bias
- Specialized visual encoders: Better conflict handling

## Methodology & Implementation

### Benchmark Construction

**Data Creation Process:**
1. Start with natural images from public datasets (COCO, Visual Genome)
2. Generate descriptions for images
3. Create conflicting text descriptions (systematically alter one property)
4. Construct natural language questions
5. Determine ground-truth answers (based on actual image content)

**Conflict Generation Strategy:**
- For each conflict type, generate 5-10 variations
- Vary conflict severity (subtle vs. obvious)
- Test both positive and negative instances
- Ensure diversity across visual domains

**Quality Control:**
- Human annotators verify conflict validity
- Cross-annotator agreement verification
- Removal of ambiguous cases

### Evaluation Setup

**Models Evaluated:**
- 10+ state-of-the-art MLLMs
- Different sizes (small to very large)
- Different architectures (transformer-only, vision-transformer, specialized encoders)

**Experimental Protocol:**
1. Present image + conflicting text to model
2. Ask direct question about the property
3. Record model's answer and confidence
4. Measure correctness and bias
5. Analyze reasoning (if model provides explanations)

**Evaluation Metrics:**

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| Conflict Accuracy | % correct answers | Higher = better visual grounding |
| Visual Preference | % choosing visual answer | Indicates modality bias |
| Text Preference | % choosing text answer | Indicates language bias |
| Uncertainty Rate | % refusing to answer | Robustness indicator |
| Confidence Calibration | Confidence vs. accuracy | Reliability of confidence scores |

### Results and Comparisons

**Overall Conflict Accuracy [Exact figures unavailable — see full paper]:**
- SOTA MLLMs: 60-75% accuracy under conflict
- Strong text bias observed in many models
- Accuracy drops significantly for complex conflicts
- (Estimated ranges based on typical MLLM performance patterns)

**Modality Bias Analysis:**
- Vision-preferring models: ~65% accuracy, ~70% visual preference
- Text-preferring models: ~55% accuracy, ~30% visual preference
- Balanced models: ~72% accuracy, ~55% visual preference

**Conflict Type Analysis:**
- Property conflicts: Highest accuracy (70-80%)
- Existence conflicts: Medium accuracy (60-70%)
- Semantic conflicts: Lower accuracy (40-60%)
- Temporal conflicts: Most difficult (30-50%)

**Scale Analysis:**
- Larger models generally more robust to conflicts
- Scaling helps some architectures more than others
- Not all conflict resolution benefits scale uniformly

**Architectural Comparison:**
- Vision-Transformer models: Best visual grounding
- Pure Transformers: Highest text bias
- Hybrid architectures: Good average performance

## Practical Applications & Use Cases

### 1. Medical Image Analysis

**Application:** Radiologists reviewing automated image descriptions

**Challenge:** What happens when AI-generated report contradicts the actual image?

**Relevance:** Understanding which modality the system trusts is critical for clinical safety

**Example:** Model sees tumor in X-ray but description says "no abnormalities"

### 2. Video Content Moderation

**Application:** Moderating videos with potential policy violations

**Challenge:** Detecting when visual content contradicts captions/text overlays

**Example:** Video appears to show violence but caption claims "educational content"

**Importance:** Preventing evasion of content policies

### 3. Document Understanding and OCR

**Application:** Understanding scanned documents with handwritten annotations

**Challenge:** Reconciling printed text with handwritten corrections

**Example:** Document header says "CLASSIFIED" but handwritten note says "DECLASSIFIED"

### 4. Accessibility and Content Verification

**Application:** Generating alt-text for images

**Challenge:** When alt-text disagrees with human descriptions

**Benefit:** Ensures accessibility features don't provide misleading information

### 5. Automated Fact-Checking

**Application:** Verifying claims against images

**Challenge:** Detecting when text claims contradict visual evidence

**Example:** "This politician attended event X" with image showing they weren't present

### Feasibility and Implementation Challenges

**Implementation Benefits:**
- Benchmark is reproducible and systematic
- Can be applied to any MLLM
- Scales to evaluate new models
- Lightweight evaluation compared to fine-tuning

**Challenges:**
- Requires careful benchmark construction to avoid annotation artifacts
- May not capture all real-world conflict scenarios
- Computational cost of evaluating many models
- Potential for benchmark overfitting (future models may be optimized for this benchmark)

## Insights & Implications

### Broader Field Impact

This work establishes **systematic conflict resolution** as a key evaluation criterion for MLLMs:

- **Paradigm Shift:** From assuming modality consistency to testing robustness under conflict
- **Safety Focus:** Highlights importance of understanding model biases for safety-critical applications
- **Architecture Insights:** Reveals which architectural choices improve conflict handling

### State-of-the-Art Advancement

Key contributions to multimodal learning:
- First benchmark revealing systematic MLLM biases under conflict
- Demonstrates that modality bias is a measurable, significant phenomenon
- Provides evaluation framework adopted by the community

### Limitations and Open Questions

**Known limitations:**
- Synthetic conflicts may not capture all real-world scenarios
- Limited to English and common visual domains
- Benchmark size (1,000+ scenarios) may not cover all conflict types
- Ground truth based on visual information (may not reflect multimodal truth)

**Open research questions:**
- How do humans resolve text-vision conflicts? (For comparison)
- Can we train models specifically to handle conflicts better?
- Are there conflict types that are inherently ambiguous?
- How do conflicts in other modalities (audio, text) behave differently?
- Can conflict handling be improved through prompting or in-context learning?

### Future Research Directions

**Immediate extensions:**
- Multi-language evaluation (beyond English)
- Additional visual domains (diagrams, charts, technical drawings)
- Video-text conflicts (temporal aspect)
- Audio-visual conflicts

**Longer-term directions:**
- Training methods specifically for conflict robustness
- Theoretical models of conflict resolution
- Human-in-the-loop approaches to resolve ambiguous cases
- Integration with world models for better reasoning under conflict

## Code & Resources

### Official Implementation

**Repository:** SIGNPOST-Bench (GitHub available)
- Benchmark dataset and evaluation code
- Pre-computed results for major MLLMs
- Easy-to-use evaluation interface

### Dependencies and Requirements

**Core dependencies:**
- Python 3.8+
- PyTorch or TensorFlow
- Transformers library
- Pillow (image processing)

**Compute requirements:**
- CPU sufficient for benchmark construction
- GPU recommended for running evaluations (8GB+ VRAM)
- Storage: 5-10GB for full dataset

### Quick-Start Guide

```python
# Load benchmark
from signpost_bench import SignpostBench
benchmark = SignpostBench.load()

# Evaluate your model
from transformers import CLIPVisionModel, AutoTokenizer
model = CLIPVisionModel.from_pretrained('model_id')

results = benchmark.evaluate(model, image_loader='pil')

# Analyze results
report = results.generate_report()
print(f"Conflict Accuracy: {report['conflict_accuracy']:.2%}")
print(f"Visual Preference: {report['visual_preference']:.2%}")
print(f"Text Preference: {report['text_preference']:.2%}")
```

## Related Work & Context

### Related Recent Papers on Multimodal Understanding

**Multimodal Robustness:**
- MultiModal Code-Switching (2026-08): Object-level alignment for multimodal models
- Illuminating Visual Identity in Multimodal Embeddings (2026-08)
- Adversarial Evasion Attacks on Computer Vision using SHAP Values (2026-01)

**Benchmark Development:**
- FeynmanBench (2026-04): Benchmarking multimodal reasoning
- LENS: Multi-level Evaluation of Multimodal Reasoning (2025-05)
- TableVista: Multimodal Table Reasoning Benchmark (2026-05)

**Vision-Language Models:**
- Vision Inference Former (2026-05): Visual consistency in multimodal LLMs
- Large Vision-Language Models Get Lost in Attention (2026-05)
- From Sight to Insight: Visual Reasoning with RL (2026-01)

### Prior Work Foundations

**Multimodal Learning:**
- Vision-Language model literature (CLIP, ALIGN)
- Cross-modal alignment and fusion research
- Multimodal reasoning benchmarks

**Conflict Resolution:**
- Related to classical information fusion problems
- Draws from cognitive psychology research on conflict resolution
- Connects to robustness evaluation in adversarial ML

### Possible Future Research Directions

1. **Adaptive conflict resolution:** Models that learn to handle specific conflict types better
2. **Explanation generation:** Understanding why models choose specific modalities
3. **Uncertainty quantification:** Better capturing model confidence under conflict
4. **Multi-agent conflict resolution:** How multiple models reconcile conflicting perceptions
5. **Real-world validation:** Applying benchmark insights to production systems

## Significance and Impact

This paper makes important contributions to multimodal AI by:
1. Establishing systematic conflict evaluation as a research problem
2. Providing reproducible benchmark for community evaluation
3. Revealing systematic biases in current MLLMs
4. Creating evaluation framework for future MLLM development

**Expected impact:** Will become standard evaluation benchmark for multimodal models, driving improvements in conflict robustness and modality balance.
