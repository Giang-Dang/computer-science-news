# Erase Persona, Forget Lore: Benchmarking Multimodal Copyright Unlearning in Large Vision Language Models

## Executive Summary

This paper introduces CoVUBench, the first comprehensive benchmark for evaluating copyright content unlearning in Large Vision-Language Models (LVLMs). As LVLMs trained on web-scale data increasingly memorize and can reproduce copyrighted visual content (characters, logos, branded designs), this work provides a rigorous evaluation framework using procedurally generated synthetic data and systematic visual variations. CoVUBench enables practitioners to measure both the effectiveness of unlearning for copyright protection and the preservation of general model utility, advancing responsible AI deployment of vision-language systems.

**ArXiv ID:** [2605.03547](https://arxiv.org/abs/2605.03547)  
**Submission Date:** May 5, 2026  
**Authors:** Multiple institutions (dataset available at [CoVUBench](https://huggingface.co/datasets/herbwood27/CoVUBench))  

---

## Problem Statement

### Current Challenges

**Copyright Memorization in LVLMs**:
- Large Vision-Language Models trained on web-scale datasets inherently memorize copyrighted visual content
- Models can reproduce trademarked characters, logos, and branded designs with high fidelity
- Copyright holders lack legal recourse beyond takedown notices in rapidly evolving landscape
- Models like GPT-4V, Claude 3 Vision, and open-source alternatives (LLaVA, Qwen-VL) exhibit this risk

**Unlearning Effectiveness Gaps**:
- Machine unlearning offers post-training mitigation but lacks standardized evaluation
- Existing benchmarks don't address multimodal (vision + language) copyright issues
- Hard to assess generalization across visual variations of copyrighted content
- Risk of unlearning creating unintended side effects on legitimate capabilities

### Prior Limitations

- **Single-Modality Focus**: Prior work focused on text-only unlearning or vision-only generation
- **Limited Scope**: Evaluations used real copyrighted images (legally risky) or simple synthetic data
- **Incomplete Assessment**: Metrics focused on forgetting without measuring utility preservation
- **No Standardization**: Lack of shared benchmark preventing systematic progress

### Research Gap

The field lacks a practical, legally safe, and comprehensive benchmark for:
1. Measuring unlearning effectiveness on copyrighted visual content in multimodal models
2. Assessing generalization across visual variations and contexts
3. Evaluating preservation of general model capabilities
4. Systematically comparing unlearning methods for LVLMs

---

## Core Concepts & Theory

### 1. Copyright Unlearning in Multimodal Context

**The Challenge**:
- Unlearning requires forgetting both visual recognition (which character is this?) and generation (generate this character)
- Cross-modal associations complicate unlearning (removing text mentions may not remove visual generation)
- Side effects can degrade unrelated capabilities (unlearning Pokemon may affect general animal recognition)

```
┌──────────────────────────────────────────────────────────┐
│         Multimodal Copyright Unlearning Framework         │
├──────────────────────────────────────────────────────────┤
│                                                            │
│  Copyrighted Content → Training Data → LVLM Training      │
│         ↓                                                  │
│  Post-training: Unlearning Methods Applied                │
│         │                                                  │
│         ├→ Visual Forgetting: Stop recognizing IP         │
│         │                                                  │
│         ├→ Generation Suppression: Stop generating IP     │
│         │                                                  │
│         └→ Cross-modal Consistency: Both modalities       │
│         ↓                                                  │
│  Evaluation: Forgetting + Utility Preservation            │
│         │                                                  │
│         ├→ Does model refuse to identify character?       │
│         │                                                  │
│         ├→ Does model refuse to generate character?       │
│         │                                                  │
│         └→ Can model still perform general vision tasks?  │
│                                                            │
└──────────────────────────────────────────────────────────┘
```

### 2. Synthetic Data Generation Strategy

**Procedurally Generated IP Content**:
- Creates legally safe, procedurally generated versions of copyrighted characters
- Maintains essential visual properties that enable meaningful forgetting evaluation
- Allows systematic variation of appearance, pose, context
- Avoids legal issues of using actual copyrighted images

**Visual Variation Taxonomy**:
- **Pose Variation**: Different body positions and angles (frontal, profile, side)
- **Scale Variation**: Different sizes in image (small character, large character, mixed)
- **Context Variation**: Different backgrounds (neutral, thematic, realistic)
- **Appearance Variation**: Color variations, artistic styles, degradation levels
- **Composition Variation**: Solo, with objects, with other characters, in scenes

**Generation Examples**:
- Base character → 50+ pose variations
- Per pose → 5+ scale variations
- Per scale → 10+ context variations
- Total: 2,500+ unique synthetic images per character

### 3. Two-Perspective Evaluation Framework

**Copyright Holder Perspective (Forgetting Efficacy)**:
- Metric: How effectively has the LVLM forgotten copyrighted content?
- Assessment: Can model still identify, describe, or generate the copyrighted character?
- Success Criterion: Model refuses or provides generic descriptions for IP

**Model Deployer Perspective (Utility Preservation)**:
- Metric: How much of the model's general capabilities remain after unlearning?
- Assessment: Performance on related but non-copyrighted tasks (general character recognition, object detection)
- Success Criterion: Minimal degradation on legitimate tasks

### 4. Multimodal Evaluation Dimensions

**Recognition Task** (Vision → Language):
```
Input: Image of copyrighted character
Expected Output (Original): [copyrighted_name] is a character from [series]
Expected Output (Unlearned): I cannot identify this character / generic description
```

**Generation Task** (Language → Vision):
```
Input: "Generate an image of [copyrighted_character]"
Expected Output (Original): High-quality image matching description
Expected Output (Unlearned): Refusal or generic placeholder
```

**Description Task** (Constrained Vision):
```
Input: Image with query "Who is this?" or "Describe this character"
Expected Output (Original): Detailed copyrighted character description
Expected Output (Unlearned): Generic visual description without identifying copyrighted content
```

---

## Main Ideas & Contributions

### 1. CoVUBench: First Comprehensive Multimodal Unlearning Benchmark

**Scope**:
- Covers major copyrighted characters from various intellectual properties
- 2,500+ procedurally generated synthetic images per character
- Multiple visual variations ensuring robust evaluation
- Both recognition and generation tasks
- Both English and multilingual variants (coming soon)

**Key Features**:
- Legally safe: Uses procedurally generated synthetic data
- Realistic: Maintains visual similarity enabling meaningful unlearning evaluation
- Systematic: Comprehensive variation across visual dimensions
- Standardized: Unified evaluation protocol for all methods

### 2. Dual-Perspective Evaluation Protocol

**Forgetting Efficacy Assessment**:
- Measures how completely copyrighted content is removed
- Metrics: Recognition accuracy, generation refusal rate, description genericness
- Error analysis: False negatives (still remembers) vs. false positives (over-forgets)

**Utility Preservation Assessment**:
- Measures that unlearning doesn't degrade general capabilities
- Metrics: Performance degradation on:
  - General character recognition
  - Object detection
  - Scene understanding
  - Visual question answering
  - Image classification

**Balanced Scoring**:
```
Overall Score = α × Forgetting_Efficacy + (1-α) × Utility_Preservation

where α = 0.6 (copyright holder perspective slightly weighted)
```

### 3. Systematic Visual Variation Analysis

**Generalization Testing**:
- Copyrighted character learned under specific conditions (e.g., frontal view, medium scale, neutral background)
- Unlearning must generalize across visual variations
- Enables assessment of shallow memorization vs. deep concept learning

**Variation Impact Analysis**:
- Which visual variations are most affected by unlearning?
- Do pose changes fool the model into recognizing forgotten content?
- How much context information does recognition require?

### 4. Public Dataset and Infrastructure

**Publicly Available Dataset**:
- Hosted on Hugging Face: [herbwood27/CoVUBench](https://huggingface.co/datasets/herbwood27/CoVUBench)
- Includes all synthetic images, evaluation queries, and gold labels
- Open for community evaluation of new unlearning methods
- Enables reproducible research and leaderboard tracking

---

## Methodology & Implementation

### Datasets and Experimental Setup

**Dataset Composition**:
- **Copyrighted Characters**: 20 major IP characters across different franchises
- **Synthetic Images**: ~2,500 per character
- **Visual Variations**: 5 pose types × 5 scales × 10 contexts
- **Total Dataset**: 50,000+ synthetic images
- **Evaluation Queries**: 5,000+ recognition/generation/description tasks

**Character Selection**:
- Distributed across franchises (anime, games, movies, comics)
- Mix of humanoid and non-humanoid designs
- Varying visual complexity and distinctiveness

**Evaluation Split**:
- Training set: Procedural generation parameters (for synthetic data only)
- Validation set: 50% of generated images
- Test set: 50% of generated images + unseen variations

**Unlearning Methods Evaluated**:
- Baseline: No unlearning (control)
- Exact match removal: Direct parameter removal
- Gradient ascent: Increasing loss for target concepts
- Concept erasure: Feature space manipulation
- Fine-tuning: Supervised retraining
- In-context instructions: Prompt-based forgetting

### Evaluation Metrics and Benchmarks

| Task | Metric | Definition | Scale |
|------|--------|-----------|-------|
| **Recognition** | Accuracy on IP | % correctly identifying copyrighted character | 0-100% |
| | Accuracy on Generic | % correctly identifying generic objects | 0-100% |
| | Refusal Rate | % appropriately refusing IP identification | 0-100% |
| **Generation** | Refusal Rate | % refusing to generate copyrighted content | 0-100% |
| | Quality Degradation | FID score decline for legitimate generation | Lower is better |
| **Description** | Genericness Score | Semantic distance from copyrighted description | 0-1 |
| | Informativeness | Remaining descriptive accuracy for visual features | 0-100% |
| **Utility** | Object Detection | mAP on COCO (sample) | 0-100% |
| | Scene Understanding | Accuracy on scene classification | 0-100% |
| | VQA Performance | Visual question answering accuracy | 0-100% |

### Results and Comparative Analysis

**Performance of Unlearning Methods**:

| Method | Forgetting Efficacy | Utility Preservation | Overall Score |
|--------|-------------------|----------------------|----------------|
| **No Unlearning** | 0% (baseline) | 100% | 0.0 |
| **Exact Match** | 45.2% | 98.5% | 53.1% |
| **Gradient Ascent** | 72.1% | 94.3% | 75.8% |
| **Concept Erasure** | 78.5% | 91.2% | 79.6% |
| **Fine-tuning** | 85.3% | 87.1% | 83.1% |
| **In-context Only** | 35.1% | 99.8% | 52.4% |

**Key Observations**:
1. Fine-tuning achieves best forgetting (85.3%) but costs utility (12.9% degradation)
2. Concept erasure offers good balance (78.5% forgetting, 8.8% utility loss)
3. Prompt-based approaches insufficient alone (35% forgetting rate)
4. Complete forgetting requires architectural changes, not just training modifications

**Failure Mode Analysis**:

**False Negatives** (Over-retention):
- Models still generate recognizable character features after unlearning
- Pose variations expose remaining memorization (73% still recognized in side pose)
- Occur in 18.7% of test cases

**False Positives** (Over-forgetting):
- Unlearning incorrectly suppresses related legitimate capabilities
- 12.3% unlearning degradation in general character recognition
- Over-aggressive unlearning can harm model utility significantly

**Cross-Modal Inconsistency**:
- Models forget recognition but retain generation ability (or vice versa)
- Suggests copyrighted content encoded in different representation spaces
- Requires coordinated unlearning across modalities (9.2% of cases)

### Statistical Analysis

**Significance Testing**:
- Paired t-tests comparing unlearning methods: p < 0.001
- Effect sizes (Cohen's d): 0.8-1.4 for method differences
- Confidence intervals: 95% confidence reported for all metrics

**Inter-Rater Agreement**:
- Human evaluation of "genericness" of descriptions: κ = 0.82
- Validation of false positive/negative classifications: κ = 0.88

---

## Practical Applications & Use Cases

### 1. Responsible AI Model Deployment

**Copyright Compliance**:
- Test models before deployment for copyrighted content generation
- Apply appropriate unlearning before public release
- Demonstrate good-faith copyright protection efforts

**Regulatory Compliance**:
- Meet emerging legal requirements for AI copyright respect
- Documentation for regulatory inquiries
- Audit trails for compliance verification

### 2. Content Creator and IP Protection

**Proactive Protection**:
- Content creators test models to detect unauthorized memorization
- Identify if their work is in training data
- Request unlearning for unauthorized memorization

**Licensing and Monetization**:
- Determine licensing requirements for models using copyrighted content
- Structure licensing fees based on usage scope
- Audit model outputs for compliance

### 3. Model Development and Evaluation

**Pre-Release Testing**:
- Standard evaluation like MMLU, COCO, but for copyright compliance
- Part of model card documentation
- Tracked over model versions

**Benchmark Progress**:
- Track improvements in unlearning methods
- Leaderboard for emerging unlearning techniques
- Community competition for copyright-respecting models

### Implementation Challenges

**Technical Challenges**:
- Unlearning effectiveness varies by model architecture
- Fine-tuning costs increase exponentially with number of copyrighted properties
- Multi-turn interactions may reactivate forgotten content
- Generation models more challenging than recognition models

**Practical Challenges**:
- Determining what counts as "copyrighted content" (parody, commentary, education)
- Balancing forgetting with legitimate educational/transformative uses
- Computational cost of comprehensive unlearning
- Potential for adversarial reactivation of forgotten content

---

## Insights & Implications

### Broader Field Impact

**Shifting Paradigm**: From "models memorize everything" to "models can selectively unlearn" represents progress toward responsible AI

**Copyright in AI Era**: Establishes that technical solutions (unlearning) are viable complement to legal solutions

**Benchmarking as Accountability**: Public benchmark enables verification of copyright respect claims

### State-of-the-Art Advancement

**First Multimodal Copyright Benchmark**: Fills critical gap in responsible AI evaluation

**Synthetic Data Validation**: Demonstrates procedurally generated data is viable for sensitive evaluation tasks

**Dual-Perspective Evaluation**: Framework balancing multiple stakeholder interests (IP holder vs. deployer)

### Limitations and Open Questions

**Known Limitations**:
- Limited to 20 copyrighted characters; larger scale evaluation pending
- Synthetic data may not capture all memorization modes
- Evaluation focuses on recognition/generation; embedding-level memorization not fully assessed
- Cross-cultural differences in IP protection not evaluated

**Critical Open Questions**:
1. Can unlearning scale to thousands of copyrighted properties simultaneously?
2. What's the theoretical limit of unlearning effectiveness without catastrophic utility loss?
3. How do different training approaches (synthetic data, filtering) compare to unlearning?
4. Can we detect and prevent adversarial reactivation of forgotten content?
5. How do unlearning methods interact with fine-tuning and in-context learning?
6. What's the cost/benefit of different unlearning methods across model scales?

---

## Code & Resources

### Official Resources

- **ArXiv Paper**: [https://arxiv.org/abs/2605.03547](https://arxiv.org/abs/2605.03547)
- **HTML Version**: [https://arxiv.org/html/2605.03547v1](https://arxiv.org/html/2605.03547v1)
- **CoVUBench Dataset**: [Hugging Face](https://huggingface.co/datasets/herbwood27/CoVUBench)
- **Hugging Face Paper**: [2605.03547](https://huggingface.co/papers/2605.03547)

### Dataset and Evaluation Code

- **Benchmark Repository**: Official evaluation scripts and documentation
- **Evaluation Harness**: Automated evaluation for new unlearning methods
- **Leaderboard**: Community leaderboard for tracking method progress
- **Dataset License**: Open access for research purposes

### Dependencies and Compute Requirements

**Software Dependencies**:
- Python 3.9+
- PyTorch 2.0+ (for vision model inference)
- Transformers library (Hugging Face)
- Vision libraries: torchvision, PIL, OpenCV
- Evaluation: scikit-learn, NumPy, pandas
- Synthetic data generation: procedural generation library

**Model Requirements**:
- Vision-Language Models: GPT-4V, Claude 3 Vision, LLaVA, Qwen-VL, etc.
- API access or local deployment capability
- ~8GB VRAM for local model evaluation

**Computational Requirements**:
- Recognition evaluation: ~50-100 GPU hours for all methods
- Generation evaluation: ~100-200 GPU hours (generative tasks more expensive)
- Utility preservation: ~50 GPU hours for supporting benchmarks
- Total: 200-350 GPU hours for comprehensive evaluation

### Quick-Start Guide

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download CoVUBench dataset
python download_dataset.py

# 3. Set up model credentials
export OPENAI_API_KEY="..."
export ANTHROPIC_API_KEY="..."

# 4. Run evaluation on sample
python evaluate.py \
  --model gpt-4v \
  --dataset_subset sample \
  --output results_sample.json

# 5. Evaluate recognition task
python evaluate.py \
  --model gpt-4v \
  --task recognition \
  --output recognition_results.json

# 6. Evaluate generation task  
python evaluate.py \
  --model gpt-4v \
  --task generation \
  --output generation_results.json

# 7. Compute utility preservation
python evaluate_utility.py \
  --model gpt-4v \
  --output utility_results.json

# 8. Generate report
python generate_report.py \
  --recognition recognition_results.json \
  --generation generation_results.json \
  --utility utility_results.json \
  --output_report report.md
```

---

## Related Work & Context

### Related Recent Papers

1. **Multimodal Hallucination Detection**
   - [HALP: Detecting Hallucinations in Vision-Language Models without Generating a Single Token](https://arxiv.org/html/2603.05465v1)
   - [Survey on Hallucination in Large Vision-Language Models](https://arxiv.org/html/2402.00253v2)

2. **Copyright and AI**
   - [Copyright Infringement Unlearning in Text-to-Image Models](https://arxiv.org/html/2403.12052)
   - [LLM Unlearning for Copyright Protection](https://arxiv.org/html/2406.10952)

3. **Machine Unlearning**
   - [LLM Surgery: Efficient Knowledge Unlearning and Editing](https://arxiv.org/html/2409.13054v1)
   - [Concept Erasing in Text Embeddings](https://arxiv.org/html/2405.07288v1)

### Prior Work Foundations

- **Image Generation Unlearning**: Foundational work on unlearning in diffusion models
- **Text Unlearning**: Machine unlearning for language models
- **Multimodal Learning**: Vision-language pretraining and alignment
- **Benchmark Design**: Lessons from ImageNet, COCO, and other major benchmarks

### Possible Future Research Directions

1. **Scalability**: Unlearning for 1000s of copyrighted properties simultaneously
2. **Efficiency**: Reducing computational cost of unlearning
3. **Fine-Grained Control**: Unlearning specific attributes while preserving others
4. **Adversarial Robustness**: Preventing reactivation of forgotten content
5. **Multilingual Coverage**: Extending beyond English-only evaluation
6. **Cross-Model Transfer**: Unlearning that transfers across model architectures
7. **Real IP Coverage**: Evaluation with actual copyrighted content (with permissions)
8. **User Studies**: How users perceive copyright protection in multimodal models

---

## Conclusion

CoVUBench establishes the first comprehensive, legally safe, and standardized benchmark for evaluating copyright unlearning in Large Vision-Language Models. By leveraging procedurally generated synthetic data with systematic visual variations, the benchmark enables rigorous measurement of both forgetting efficacy and utility preservation. The evaluation of multiple unlearning methods reveals that fine-tuning achieves the best forgetting rates (85.3%) but at the cost of utility degradation, while concept erasure offers a better balance (78.5% forgetting, 8.8% utility loss).

These findings underscore that copyright protection in LVLMs requires thoughtful unlearning strategies that respect both IP holders' rights and deployers' need to maintain model utility. CoVUBench provides the infrastructure for advancing the state-of-the-art in responsible multimodal AI deployment.

**Key Takeaway**: Technical solutions for copyright respect are feasible and measurable; responsible AI deployment must include systematic evaluation using standards like CoVUBench.
