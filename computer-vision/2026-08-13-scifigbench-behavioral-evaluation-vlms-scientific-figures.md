# How Do VLMs Behave When Blind or Misled? Behavioral Evaluation of VLMs on Scientific Figures

**Paper Title:** How Do VLMs Behave When Blind or Misled? Behavioral Evaluation of VLMs on Scientific Figures  
**ArXiv ID:** 2608.13267  
**Submission Date:** August 13, 2026  
**Authors:** Paul Osemudiame Oamen, Owusu-Banahene Osei, Ananya Mukherjee, Christian Greisinger, Steffen Eger, Pius Onobhayedo, Wei Zhao  
**Affiliations:** Aberdeen NLP Research Group, IIIT Hyderabad, University of Technology Nuremberg, University of Southern California  
**Paper Link:** https://arxiv.org/abs/2608.13267

## Executive Summary

This paper introduces SciFigBench, a diagnostic benchmark that evaluates vision-language models (VLMs) on scientific figure understanding with a focus on behavioral reliability under uncertainty. Rather than measuring only perception and reasoning accuracy, SciFigBench assesses how VLMs behave when visual evidence is missing, misleading, or ambiguous. Through 600+ hours of annotation effort, the benchmark identifies systematic failures in VLM behavioral reliability, exposing vulnerabilities that standard accuracy metrics miss.

## Problem Statement

Existing VLM benchmarks emphasize perception and reasoning accuracy—how well models describe and reason about visual content. However, a critical gap exists in evaluating behavioral reliability under uncertainty: How do VLMs behave when visual evidence is absent or misleading? This gap is particularly concerning for scientific applications where models may confidently provide incorrect information when faced with incomplete or corrupted data. The research addresses this by proposing a comprehensive evaluation framework that stress-tests VLM reliability.

## Core Concepts & Theory

### Three Dimensions of VLM Evaluation

SciFigBench evaluates VLMs across three complementary dimensions:

1. **Perception:** Can the model accurately describe visual elements in scientific figures?
2. **Reasoning:** Can the model correctly interpret and synthesize information from figures?
3. **Behavioral Reliability:** Does the model appropriately acknowledge uncertainty, resist misleading context, and make cautious inferences?

### A-R-I Framework: Admittance-Resistance-Inductance

The paper introduces the A-R-I framework to systematically evaluate model behavior under uncertainty:

**Admittance (A):**
- Measures whether models appropriately acknowledge insufficient visual evidence
- Tests model's willingness to say "I cannot determine this from the figure"
- Evaluates confidence calibration when information is missing

**Resistance (R):**
- Measures the model's ability to resist misleading or contradictory context
- Tests robustness to caption biases, incorrect labels, and adversarial prompts
- Assesses whether models blindly follow textual cues over visual evidence

**Inductance (I):**
- Measures cautious inference capabilities
- Tests whether models make claims only supported by available evidence
- Evaluates resistance to hallucination and over-generalization

### Scientific Figure Understanding Task

Scientific figures present unique challenges for VLMs:
- Complex visual elements (plots, diagrams, microscopy images)
- Domain-specific notation and terminology
- Multiple interconnected concepts requiring synthesis
- High consequence for errors in scientific interpretation

## Main Ideas & Contributions

### 1. SciFigBench Dataset

**Composition:**
- **250 scientific figures** from diverse fields (biology, chemistry, physics, engineering)
- **600+ hours of expert annotation** ensuring high-quality labels and evaluation criteria
- **34,000+ evaluation setups** created through systematic augmentation

**Methodology for Dataset Creation:**
1. Collect diverse scientific figures from publications
2. Manual annotation of figure components and interpretations
3. Expert verification of annotation quality
4. Augmentation through controlled transformations

### 2. Systematic Stress Testing

**Image Transformation Strategies:**
- **Selective Blur:** Progressively obscure regions to test graceful degradation
- **Caption Bias Probes:** Introduce misleading or contradictory captions
- **Resistance Tests:** Present visually inconsistent claims
- **Reasoning Queries:** Ask multi-step questions requiring integration of figure elements

**Stress Test Coverage:**
- Missing visual information (blur + degradation)
- Contradictory textual context (caption bias)
- Adversarial conditions (misleading prompts)
- Compositional reasoning (multi-element integration)

### 3. Behavioral Reliability Assessment

**Key Innovation:** Moving beyond accuracy metrics to behavioral evaluation

Traditional Approach: "Did the model give the right answer?"
→ Problem: Doesn't capture whether the model was appropriately uncertain

New Approach (A-R-I): "Did the model behave appropriately given the evidence?"
→ Benefit: Captures both accuracy and appropriate confidence calibration

## Methodology & Implementation

### Experimental Protocol

**Evaluation Workflow:**
1. Present VLM with scientific figure
2. Ask perception question (describe elements)
3. Ask reasoning question (interpret relationships)
4. Apply transformations (blur, bias, degradation)
5. Repeat questions under degraded conditions
6. Score responses using A-R-I framework

### A-R-I Scoring Criteria

**Admittance Scoring:**
- **High Admittance:** "I cannot determine this from the figure" when evidence is insufficient
- **Low Admittance:** Confident claims despite missing visual information

**Resistance Scoring:**
- **High Resistance:** Prioritizes visual evidence over misleading captions
- **Low Resistance:** Easily influenced by contradictory text

**Inductance Scoring:**
- **High Inductance:** Makes claims only supported by visible evidence
- **Low Inductance:** Hallucinates details or over-generalizes

### Evaluation Metrics

**Per-Dimension Metrics:**
- Admittance Score (0-100): Fraction of appropriate uncertainty acknowledgments
- Resistance Score (0-100): Robustness to misleading context
- Inductance Score (0-100): Constraint to supported inferences

**Composite Score:**
- Overall Behavioral Reliability = (A + R + I) / 3

### Results and Findings

**Key Finding [Exact figures unavailable — see full paper]:**
Analysis across multiple state-of-the-art VLMs reveals significant variation in behavioral reliability, with some models excelling at perception but failing under adversarial conditions.

**Behavioral Patterns Observed:**
1. Models show asymmetric strengths (high reasoning, low uncertainty calibration)
2. Caption bias significantly impacts reliability (estimated >20% performance variance)
3. Selective blur reveals graceless degradation patterns
4. Models struggle with nuanced scientific reasoning even with complete visual information

## Practical Applications & Use Cases

### Scientific Research Support
- Automated figure analysis in literature reviews
- Verification of figure interpretations in papers under review
- Quality control for AI-assisted scientific writing

### Educational Applications
- Teaching tools that assess student understanding of scientific figures
- Verification that figures are correctly interpreted by learning systems
- Interactive learning systems with reliable visual understanding

### Healthcare and Medical Imaging
- Medical report generation from diagnostic images (with appropriate uncertainty quantification)
- Second-opinion systems for image interpretation
- Risk assessment for AI-assisted diagnostic systems

### Industrial Quality Control
- Visual inspection systems that appropriately signal uncertainty
- Defect detection in manufacturing with calibrated confidence
- Safety-critical applications requiring robust uncertainty handling

## Insights & Implications

### Broader Field Impact

The introduction of the A-R-I framework and behavioral evaluation methodology represents a paradigm shift in VLM evaluation. Moving beyond accuracy to behavioral reliability provides a more nuanced and practically relevant assessment of model suitability for real-world applications, especially in domains where inappropriate confidence poses risks.

### State-of-the-Art Advancement

SciFigBench establishes a new standard for VLM evaluation that captures the gap between benchmark accuracy and deployment reliability. This framework will likely influence future VLM development and evaluation practices across the field.

### Limitations and Open Questions

1. **Domain Specificity:** How well do behavioral patterns generalize across different scientific domains?
2. **Model Scale Effects:** Do larger models systematically show better behavioral reliability?
3. **Fine-tuning Impact:** Can behavioral reliability be improved through task-specific fine-tuning?
4. **Human Alignment:** How closely do VLM behavioral patterns align with human expert uncertainty patterns?

### Future Research Directions

- **Cross-Domain Generalization:** Evaluating behavioral patterns across medical imaging, satellite imagery, microscopy
- **Intervention Studies:** Exploring fine-tuning and prompt engineering to improve behavioral reliability
- **Mechanistic Analysis:** Understanding which model components drive admittance, resistance, and inductance
- **Interactive Benchmarking:** Extending to scenarios with human feedback loops
- **Deployment Guidelines:** Creating frameworks for determining model suitability for specific applications

## Code & Resources

**Official Resources:**
- Benchmark Data: SciFigBench (250 figures, 34,000+ evaluation setups)
- Evaluation Protocol: A-R-I framework implementation
- Paper and Supplementary Materials: https://arxiv.org/abs/2608.13267

**Dependencies:**
- VLM inference capability (supports multiple model families)
- Image processing utilities (for transformation and augmentation)
- Evaluation annotation framework

**Compute Requirements:**
- Moderate computational cost (standard GPU for VLM inference)
- Evaluation can run in parallel across figures
- Annotation effort: 600+ hours already completed (included in release)

## Related Work & Context

### Related Benchmarks
- **VLM-RobustBench:** Robustness evaluation of VLMs
- **VLABench:** Language-conditioned visual reasoning tasks
- **SenseBench:** Remote sensing visual perception and description

### Foundational Work
- **Calibration in ML:** Prior work on confidence calibration and uncertainty quantification
- **Adversarial VLM Research:** Studies on robustness and failure modes
- **Scientific Document Understanding:** Related work on scientific text and figure comprehension

### Complementary Research Directions
- **Uncertainty Quantification:** Methods for improving model confidence calibration
- **Adversarial Robustness:** Techniques for improving resistance to misleading context
- **Interpretability:** Understanding VLM decision-making under uncertainty
- **Multimodal Learning:** Joint training with improved behavioral properties

### Impact on Field

This work establishes behavioral reliability as a critical evaluation dimension for VLMs, particularly for applications in science, medicine, and safety-critical domains. It provides both a benchmark and a conceptual framework (A-R-I) that future systems will need to address.
