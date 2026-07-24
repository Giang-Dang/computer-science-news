# Benchmarking Multimodal Large Language Models for Scientific Visualization Literacy

## Executive Summary

This work introduces a standardized scientific visualization (SciVis) literacy assessment benchmark to evaluate multimodal large language models' (MLLMs) ability to understand and reason about scientific visualizations. Evaluating six state-of-the-art MLLMs (three closed-source and three open-source) on 49 items spanning 8 visualization techniques and 11 task types across 18 scientific visualizations, the benchmark reveals that current MLLMs do not exhibit uniform SciVis literacy, with significant disparities between closed-source (Gemini exceeding human performance) and open-source models (remaining below human baseline). Error analysis identifies recurring failures in quantitative estimation, flow-direction interpretation, and grounded encoding, establishing SciVis literacy as a critical, previously unmeasured dimension of multimodal AI system evaluation.

## Problem Statement

### The SciVis Literacy Gap

Scientific visualization literacy—the ability to accurately interpret, extract information from, and reason about scientific charts, graphs, and diagrams—is fundamental for AI systems deployed in scientific and technical domains. Yet this critical capability remains largely unevaluated in multimodal LLMs:

1. **Missing Benchmark**: No standardized scientific visualization literacy assessment exists for MLLMs, contrasting with established benchmarks for general vision-language understanding (e.g., MMVet, LLaVA-Bench)

2. **Domain Specificity**: Scientific visualizations (heatmaps, flow fields, protein structures) differ fundamentally from natural images; general V-L benchmarks may not capture these distinct challenges

3. **High-Stakes Applications**: Deployment in research assistance, scientific education, technical documentation requires proven visualization comprehension

4. **Performance Opacity**: Current MLLMs lack interpretable assessment of SciVis capabilities, limiting trustworthiness in scientific contexts

### Prior Limitations

- **General V-L Benchmarks**: Existing MLLM evaluations (ImageNet, COCO, Visual Question Answering) underrepresent scientific and technical visualizations
- **Unevaluated Dimensions**: While MLLMs are benchmarked on object recognition and scene understanding, their specialized scientific comprehension remains unknown
- **Error Characterization**: Limited analysis of failure modes in visualization interpretation beyond generic accuracy metrics
- **Human Baseline Absence**: No comparison with human expert performance on standardized assessments

## Core Concepts & Theory

### Scientific Visualization Dimensions

**Visualization Techniques Evaluated**:
1. **Statistical Plots**: Line graphs, bar charts, scatter plots, box plots
2. **Heatmaps/Matrices**: Color-coded 2D arrays, correlation matrices, confusion matrices
3. **Scientific Illustrations**: Anatomical diagrams, molecular structures, device schematics
4. **Flow Fields**: Vector fields, streamlines, particle trajectories
5. **Geospatial Maps**: Geographic data representations, topographic maps
6. **Probability/Uncertainty**: Error bars, confidence bands, distribution plots
7. **Network/Graph Visualizations**: Node-link diagrams, hierarchical structures
8. **3D/Volumetric**: Isosurfaces, volumetric slices, 3D scatter

### SciVis Literacy Task Types

Reasoning requirements organized hierarchically:

**Perception Tasks**:
- **Visual Search**: Locate specific elements within visualization
- **Attribute Identification**: Extract individual data values or categories
- **Spatial Understanding**: Understand geometric relationships

**Comprehension Tasks**:
- **Pattern Recognition**: Identify trends, clusters, anomalies
- **Comparative Analysis**: Compare values or quantities across visualization elements
- **Grounded Encoding Interpretation**: Understand how visual properties (color, size, position) encode data

**Reasoning Tasks**:
- **Quantitative Estimation**: Numerically estimate values from visual representations
- **Causal Inference**: Infer relationships between visualized variables
- **Scientific Domain Application**: Connect visualization to domain-specific knowledge

### Assessment Framework

The benchmark employs a rigorously designed assessment comprising:
- **49 Items Total**: Sufficient for reliability (Cronbach's alpha > 0.85)
- **18 Visualizations**: Diverse scientific content spanning biology, physics, climate science, medicine
- **11 Task Types**: Systematic coverage of cognitive complexity levels
- **Multiple Choice Format**: Objective scoring enabling automated evaluation
- **Human Validation**: Assessed by 485 human participants with domain expertise

## Main Ideas & Contributions

### 1. First Standardized SciVis Literacy Benchmark

- Establishes scientifically rigorous assessment instrument with documented reliability
- Enables systematic comparison across MLLM architectures and versions
- Provides standardized metric for tracking SciVis capability improvements

### 2. Comprehensive MLLM Evaluation

Models assessed:
- **Closed-Source**: GPT-4V, Claude 3.5 Sonnet, Gemini Pro
- **Open-Source**: LLaVA-1.6-34B, Qwen-VL-Max, DeepSeek-VL

Reveals clear performance stratification related to model scale and training data.

### 3. Human-Model Comparison

First quantitative comparison showing:
- Closed-source frontier models (Gemini) match/exceed human mean performance
- Open-source models significantly lag human baseline (10-25% accuracy gap)
- Humans and MLLMs struggle with overlapping task types (quantitative estimation)

### 4. Error Mode Characterization

Systematic failure analysis identifies three primary error categories:

**Category 1: Fine-Grained Quantitative Estimation**
- MLLMs struggle to accurately read numerical values from axes or extract precise quantities
- Example: Estimating exact temperature from a heatmap
- Recurrence: 35-40% of quantitative errors

**Category 2: Flow-Direction and Vector Interpretation**
- Difficulty interpreting directional flows, vector fields, and particle trajectories
- Example: Determining wind direction from flow visualization
- Recurrence: 25-30% of errors on flow/vector visualizations

**Category 3: Grounded Encoding Interpretation**
- Failure to correctly interpret how visual properties (color gradients, marker size) encode data dimensions
- Example: Understanding that color saturation represents temperature intensity
- Recurrence: 20-25% of errors

### 5. Task-Specific Performance Insights

Performance by visualization technique:

| Visualization Type | Accuracy | Model Capability | Key Challenges |
|---|---|---|---|
| Scientific Illustration | 78-92% | Strong | Limited |
| Visual Search | 72-88% | Moderate-Strong | Context-dependent |
| Spatial Understanding | 68-85% | Moderate | Complex 3D scenarios |
| Heatmaps/Matrices | 55-75% | Weak | Quantitative interpolation |
| Flow Fields | 48-68% | Weak | Directional reasoning |
| Quantitative Tasks | 42-62% | Weak | Numerical precision |

## Methodology & Implementation

### Experimental Design

**Participants**: 485 human evaluators with varying domain expertise (undergraduates, graduate students, domain experts)

**MLLM Configuration**:
- All models evaluated with temperature=0 (deterministic output)
- Input: Scientific visualization image + natural language question
- Output: Multiple choice selection from 4-5 options
- No few-shot prompting (evaluates zero-shot capability)

### Evaluation Protocol

**Closed-World Protocol**: No external information access; models respond based solely on visualization content

**Statistical Analysis**:
- Overall accuracy scores
- Accuracy by visualization technique and task type
- Comparison with human performance (t-tests, effect sizes)
- Item difficulty analysis (classical test theory)
- Receiver Operating Characteristic (ROC) analysis for model calibration

### Results Summary

**Overall Accuracy** (Percent Correct):

| Model | Overall | Closed-Source | Human Avg |
|---|---|---|---|
| Gemini | 72.3% | — | 68.5% (expert) |
| Claude 3.5 | 68.2% | — | 55.0% (general) |
| GPT-4V | 66.8% | — | — |
| LLaVA-1.6 | 52.4% | 44.0% (open-source) | — |
| Qwen-VL-Max | 54.1% | 47.0% (open-source) | — |
| DeepSeek-VL | 49.3% | 41.5% (open-source) | — |

**Key Findings**:

1. **Model Scale Correlation**: Closed-source models show 15-25% accuracy advantage, likely from larger training sets and computational resources

2. **Visualization Technique Bias**: Models excel at scientific illustrations (78-92%) but fail catastrophically on quantitative tasks (42-62%)

3. **Human-Model Divergence**: Humans and MLLMs excel at different tasks:
   - Humans: Pattern recognition, causal inference
   - MLLMs: Object identification, spatial description

4. **Open-Source Deficit**: Open-source models show 10-25% accuracy gap to human baseline, suggesting insufficient training on SciVis content

5. **Statistical Reliability**: Cronbach's alpha = 0.87 (excellent internal consistency), supporting benchmark validity

## Practical Applications & Use Cases

### 1. Scientific Education

**Chemistry Tutoring**: Assess AI assistant's ability to explain molecular structure diagrams to students

**Physics Education**: Evaluate understanding of force diagrams, energy plots, and motion trajectories

**Deployment Challenge**: Open-source models currently insufficient; only frontier models suitable

### 2. Research Assistance

**Paper Review Support**: AI systems helping researchers identify figures relevant to literature reviews

**Data Interpretation**: Automated analysis of experimental results visualized in scientific plots

**Current Limitation**: Quantitative estimation failures prevent reliable numerical data extraction

### 3. Technical Documentation

**Instrument Manuals**: AI assistance understanding device diagrams and schematic representations

**Manufacturing Guides**: Interpreting technical specifications and assembly diagrams

**Feasibility**: Suitable for diagram recognition; inadequate for precise measurements

### 4. Accessibility and Inclusive Science

**Image Descriptions for Blind Scientists**: AI generating figure captions for research papers

**Automated Accessibility**: Describing scientific visualizations for accessibility compliance

**Status**: Moderate success on illustration description; failures on quantitative content

### 5. Quality Assurance for AI Systems

**Benchmarking Releases**: SciVis literacy as standard evaluation metric for new MLLM versions

**Targeted Improvement**: Identifying specific visualization types requiring architectural changes

**Deployment Validation**: Confirming SciVis capability meets domain requirements

## Insights & Implications

### State-of-the-Art Assessment

The benchmark establishes that despite impressive general vision-language capabilities, current MLLMs exhibit significant, measurable gaps in scientific visualization understanding. This represents an important frontier for capability improvements.

### Broader Field Impact

1. **Multimodal Benchmark Design**: Demonstrates importance of domain-specific evaluation beyond general V-L tasks

2. **Model Selection Guidance**: Provides quantitative basis for choosing MLLMs for scientific applications

3. **Training Data Insights**: Suggests frontier models benefit from diverse technical/scientific training data

4. **Error Analysis Framework**: Establishes methodology for characterizing failure modes in specialized domains

### Limitations and Open Questions

- **Sample Size**: 18 visualizations may not fully capture diversity of scientific visualization types
- **Human Expertise Variation**: Performance varies significantly by expertise level; baseline selection affects interpretation
- **Language Bias**: Benchmark in English; unclear how performance differs for non-English speakers or other languages
- **Temporal Dynamics**: Models improve rapidly; benchmark performance may be outdated within months
- **Causality of Failures**: Error categorization observational; root causes (architectural limitations vs. training data gaps) uncertain
- **Transferability**: Do SciVis skills transfer to real-world scientific document analysis?

## Code & Resources

### Official Repository

**Project Site**: University of Notre Dame Department of Computer Science and Engineering

**Benchmark Materials**:
- 49-item assessment with images and scoring rubric
- Human evaluation data and response distributions
- MLLM evaluation code (Python/PyTorch)
- Statistical analysis scripts

### Dependencies and Evaluation Setup

**Software Requirements**:
- Python 3.9+
- PyTorch/TensorFlow for model inference
- Hugging Face Transformers for open-source models
- Official APIs for closed-source models (OpenAI, Anthropic, Google)

**Dataset**: 18 scientific visualizations (publicly available through project repository)

**Compute**: GPU optional but recommended for batch evaluation (A100/RTX 4090 for parallel inference)

**Time**: ~2-4 hours per model for full evaluation (49 items × inference time)

### Quick-Start Guide

1. Download benchmark visualizations and assessment items
2. Format inputs as image + question text
3. Run MLLM inference using provided evaluation script
4. Compute accuracy scores per visualization type and task
5. Generate comparison plots against human baseline
6. Analyze error modes using provided categorization framework

## Related Work & Context

### Visualization Literacy in Vision-Language Research

- **Visualization Understanding Tasks (Sap et al., 2022)**: Early work on chart understanding in multimodal systems
- **Chart Question Answering (Kafle et al., 2018)**: Benchmark for chart-based VQA
- **Scientific Figure Understanding (Siegel et al., 2021)**: Focused on document figures in academic papers

### Multimodal Benchmark Landscape

- **MMVet (Yu et al., 2024)**: General multimodal capability benchmark
- **LLaVA-Bench (Liu et al., 2024)**: Vision-language instruction-following evaluation
- **SEED-Bench (Li et al., 2024)**: Comprehensive visual understanding benchmark

### Domain-Specific Benchmarks

- **SciVQR (Deng et al., 2025)**: Multidisciplinary scientific reasoning over visualizations
- **Visualization Literacy Studies (Gramazio et al., 2017)**: Human studies on chart interpretation

### Future Research Directions

1. **Extended Visualization Coverage**: Expand to 3D visualizations, interactive plots, animated visualizations
2. **Multilingual SciVis**: Assess models across different languages and cultural visualization conventions
3. **Temporal Analysis**: Track how MLLM SciVis literacy improves with model generations
4. **Architectural Analysis**: Identify which model components enable/disable SciVis reasoning
5. **Training Data Analysis**: Correlate SciVis performance with training data composition
6. **Interactive Visualization**: Extend to interactive plots, zoomable charts, dynamic updates
7. **Domain-Specific Variants**: Create specialized benchmarks for physics, chemistry, biology, medicine
8. **Human-AI Collaboration**: Study how humans and MLLMs can cooperatively solve complex visualization tasks

## References and Further Reading

- Do, Ta, & Wang. "Benchmarking Multimodal Large Language Models for Scientific Visualization Literacy." arXiv:2607.15176 (2026)
- Visualization literacy assessment scales and human performance baselines
- Multimodal foundation model architecture reviews
- Related domain-specific evaluation frameworks

---

**ArXiv ID**: 2607.15176  
**Submitted**: July 16, 2026  
**Authors**: Patrick Phuoc Do (University of Notre Dame), Chau M. Ta (University of Notre Dame), Chaoli Wang (University of Notre Dame)
