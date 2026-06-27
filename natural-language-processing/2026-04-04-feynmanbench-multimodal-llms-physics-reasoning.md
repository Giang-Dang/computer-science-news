# FeynmanBench: Benchmarking Multimodal LLMs on Diagrammatic Physics Reasoning

## Executive Summary

This paper introduces FeynmanBench, the first comprehensive benchmark for evaluating multimodal Large Language Models on Feynman diagram reasoning—a fundamental task in high-energy physics requiring understanding of complex diagrammatic notation, multi-step reasoning about particle interactions, and strict adherence to conservation laws and symmetry constraints. The benchmark contains over 2,000 automatically-generated tasks spanning the Standard Model (electromagnetic, weak, and strong interactions), with rigorous evaluation criteria that verify not just syntactic correctness but physical validity. Evaluation of state-of-the-art multimodal LLMs reveals systematic failure modes: models often ignore conservation law constraints, struggle with topological conditions, and show particular difficulty with diagrams involving higher-order processes. These findings underscore that current multimodal systems, despite strong performance on vision-language tasks, lack the structured reasoning required for physics, with significant implications for scientific AI and domain-specific applications.

## Problem Statement

Multimodal Large Language Models (MLLMs) have achieved remarkable performance on diverse vision-language benchmarks (VQA, image captioning, scene understanding). However, their ability to perform rigorous scientific reasoning on specialized visual domains remains poorly characterized. **Feynman diagrams**—a fundamental notation in particle physics—present a uniquely challenging benchmark for multimodal understanding:

**Challenges unique to Feynman diagram reasoning:**

1. **Strict Symbolic Semantics**: Each line, vertex, and label has precise physical meaning; small notational errors (e.g., confusing particle antiparticle notation) completely change the physics.

2. **Conservation Law Constraints**: Every process must conserve:
   - Electric charge at each vertex
   - Baryon number
   - Lepton number
   - Four-momentum in relativistic systems

3. **Topological Reasoning**: The spatial arrangement of lines (even when not physically specified) determines validity; requires understanding abstract graph topology.

4. **Hierarchical Complexity**: Simple diagrams may represent single-particle decay; complex ones model multi-body scattering with loop corrections, requiring tracking of many interacting elements.

5. **Domain-Specific Background**: Correct reasoning requires knowledge of:
   - Standard Model particle zoo (30+ particles)
   - Quantum field theory principles
   - Interaction rules for electromagnetism, weak force, strong force

Prior multimodal benchmarks (VQA, COCO captions, GQA, CLEVR) emphasize object recognition and counting. Even domain-specific benchmarks (SciQA for science, STEM-OP for optical problems) focus on question-answering about images, not reasoning about complex visual notation systems. This paper is the first to create a benchmark specifically targeting structured scientific reasoning over formal visual languages.

## Core Concepts & Theory

### Feynman Diagrams: Notation and Physics

**Visual Grammar of Feynman Diagrams**:

A Feynman diagram is a graph representing particle interactions:

```
Symbols:
- Straight lines → fermions (electrons, quarks, etc.)
- Wavy lines → bosons (photons, W/Z bosons, gluons)
- Direction of arrows → particle vs. antiparticle
- Vertices → interaction points where particles couple

Example: Electron-positron annihilation to photons
        e-
        ↓
       ╱ \
      X    →  γ (photon)
     ╱ \
    ↑   ↓
   e+   γ

The X represents the interaction vertex where:
  charge is conserved: -1 + 1 = 0 (virtual particle intermediate)
```

**Mathematical Interpretation**:
Each Feynman diagram represents an integral (Feynman integral) in the path integral formulation of quantum mechanics. The diagram encodes:
- Particle types and momenta (labeled on lines)
- Coupling constants (determined by interaction type)
- Integration variables for internal/virtual particles

**Conservation Laws in Detail**:

Every vertex must conserve:
1. **Electric Charge**: Sum of charges in = sum of charges out
2. **Baryon Number**: Count of quarks - antiquarks conserved
3. **Lepton Number**: Count of leptons - antileptons conserved
4. **Color Charge** (for strong force): SU(3) color quantum number balanced

Example violation (Invalid diagram):
```
    quark (baryon number = +1)
    ↓
   ╱ \
  X    →  electron (baryon number = 0)
 ╱ \
    ↓
  photon (baryon number = 0)

Baryon number NOT conserved: 1 ≠ 0 + 0 + 0
```

### Benchmark Design Principles

**Automatic Generation Framework**:

Rather than manually creating diagrams (infeasible for thousands of examples), FeynmanBench uses a generation pipeline:

1. **Interaction Template Selection**: Choose allowed processes
   - Single-particle decay
   - Two-particle scattering
   - Loop processes (virtual particle pairs)
   - Cascade decays

2. **Particle Assignment**: Randomly select particles from Standard Model, respecting conservation laws
   - Start with valid initial state (e.g., W boson)
   - Sample valid final states (enforce conservation laws)
   - Assign decay mechanisms

3. **Diagram Rendering**: Convert abstract process to visual Feynman diagram
   - Apply standard notational rules
   - Vary visual style (different line thicknesses, vertex positions) to avoid dataset bias

4. **Question Generation**: Create reasoning tasks
   - Identify diagram type and process
   - Verify conservation laws
   - Predict intermediate particles
   - Classify interaction type (electromagnetic, weak, strong)

### Evaluation Metrics

**Multi-Level Correctness**:

Standard accuracy is insufficient; FeynmanBench employs hierarchical correctness:

```
Level 1: Syntactic Correctness
  Question: "Is this diagram valid?"
  Answer must parse as a valid diagram
  Penalty: -1.0 if answer is incoherent

Level 2: Conservation Law Satisfaction
  Question: "Does this process conserve electric charge?"
  Evaluate: Σ(charges in) = Σ(charges out) at each vertex
  Penalty: -0.5 if charge not conserved
  Penalty: -0.3 if only partially verified

Level 3: Topological Correctness
  Question: "How many vertices are in this diagram?"
  Evaluate: Correct count of interaction points
  Penalty: -0.3 if count is off by 1, -0.7 if off by >1

Level 4: Physical Validity
  Question: "Is this process allowed in the Standard Model?"
  Evaluate: Process obeys known coupling selection rules
  Penalty: -0.2 if coupling is forbidden (e.g., 3-photon vertex doesn't exist)

Final Score = sum of level scores / number of levels
```

### Task Categories

**Electromagnetic Processes** (QED):
- Electron-positron pair production
- Compton scattering
- Bremsstrahlung (photon radiation)

**Weak Force Processes** (Electroweak):
- Beta decay
- W/Z boson scattering
- Higgs production

**Strong Force Processes** (QCD):
- Quark-gluon interactions
- Jet production
- Hadronization

**Complex Processes**:
- Loop diagrams (virtual particle pairs)
- Cascade decays (many sequential steps)
- Rare processes (CP violation, rare decays)

## Methodology & Implementation

### Benchmark Statistics

**Scale**:
- **Total tasks**: 2,017 questions
- **Diagrams**: 1,200+ unique Feynman diagrams
- **Task types**: 5 main categories (identify process, verify conservation, predict particles, classify interaction, evaluate validity)
- **Difficulty levels**: Beginner (single vertex), Intermediate (2-3 vertices), Advanced (loops, rare processes)

**Distribution**:

| Process Type | Count | Avg. Complexity |
|---|---|---|
| Electromagnetic | 450 | 1.8 vertices |
| Weak Force | 380 | 2.1 vertices |
| Strong Force | 320 | 2.3 vertices |
| Mixed Interactions | 280 | 2.9 vertices |
| Loop Processes | 187 | 3.5 vertices |
| **Total** | **1,617** | **2.3** |

**Visual Variations**:
- Same process rendered in 5 different visual styles
- Rotation/reflection of diagrams (tests invariance)
- Different label positions (tests robustness to label placement)

### Evaluation Setup

**Models Evaluated** (April 2026 state-of-the-art):

| Model | Vision Encoder | Language Model | Publication |
|---|---|---|---|
| GPT-4o | Vision Transformer | GPT-4 | OpenAI 2024 |
| Claude 3.5 Sonnet | Custom ViT | Claude base model | Anthropic 2024 |
| Gemini 2.0 | Multi-encoder | PaLM 2 | Google 2026 |
| LLaVA-1.6 | CLIP + Qwen | Qwen-7B | Open-source 2026 |
| Phi-4-Vision | Phi-3-Vision + ViT | Phi-4 | Microsoft 2025 |

### Experimental Protocol

1. **Task Presentation**: Show diagram image + question
2. **Answer Collection**: Free-form text generation (50 tokens max)
3. **Answer Parsing**: Extract claimed answer (e.g., "Yes, charge is conserved")
4. **Evaluation**: Compare against ground truth using multi-level metric
5. **Error Analysis**: Categorize failure modes

## Main Ideas & Contributions

### 1. First Benchmark for Structured Scientific Reasoning

**Contribution**: FeynmanBench establishes the first benchmark specifically designed for evaluating structured reasoning over formal scientific notation in multimodal systems.

**Prior work gap**: Existing multimodal benchmarks test:
- Object recognition (ImageNet, COCO)
- Question-answering (VQA, GQA)
- Scene understanding (CLEVR)

None test reasoning about abstract formal systems with strict rule enforcement.

**Why this matters**: 
- Scientific AI is critical for drug discovery, materials science, theoretical physics
- Current MLLMs may excel at intuitive vision tasks but fail at formal reasoning
- Highlights capability gap between pattern recognition and symbolic reasoning

### 2. Automatic Generation Framework

**Contribution**: Develops a generative framework for creating unlimited physics-grounded visual reasoning tasks.

**Key innovation**: 
- Ensures all generated diagrams are **physically valid** (conservation laws satisfied)
- Automatically generates diverse **question-answer pairs** with verified ground truth
- Enables creation of **domain-specific benchmarks** for other sciences (chemistry, biology)

**Advantage over manual creation**:
- Thousands of diagrams feasible (vs. hundreds manually)
- Eliminates human bias in question selection
- Enables controlled difficulty progression

### 3. Multi-Level Evaluation Metric

**Contribution**: Introduces hierarchical correctness evaluation that distinguishes:
- Syntactic correctness (can the model produce coherent answers?)
- Conservation law adherence (does the model understand physics constraints?)
- Topological reasoning (can it count and track structures?)
- Domain knowledge (does it know Standard Model specifics?)

**Significance**: Reveals that models may produce plausible-sounding answers that violate fundamental physics. A model claiming "Yes, charge is conserved" without actually verifying numerical conservation should be penalized—but standard accuracy treats it as correct.

### 4. Systematic Failure Mode Analysis

**Contribution**: Identifies consistent failure patterns across models.

**Key findings**:

1. **Conservation Law Ignorance** (60% failure rate on conservation tasks)
   - Models often answer "Yes, charge is conserved" without actually checking sums
   - Suggests language pattern memorization over genuine reasoning
   - Example: Model sees "electron + positron → photon + W boson" and doesn't verify charge balance

2. **Topological Blindness** (45% failure on complex diagrams)
   - Models struggle with loop diagrams and non-planar topologies
   - Spatial relationships in diagram unclear to vision encoders
   - Loop particles (virtual) misidentified as real particles

3. **Domain Knowledge Gaps** (55% on rare processes)
   - Models unfamiliar with electroweak coupling selection rules
   - Weak force processes consistently harder than electromagnetic
   - Errors suggest limited Standard Model knowledge

4. **Length Sensitivity** (accuracy drops 30% for 4+ vertex diagrams)
   - Multi-step reasoning becomes exponentially harder
   - Models lose track of constraints across many vertices
   - Suggests weak compositional reasoning

5. **Notation Brittleness** (15% drop with unfamiliar rendering styles)
   - Models rely on specific visual patterns
   - Poor generalization to diagram variants
   - Indicates superficial visual feature learning

### 5. Practical Implications for Scientific AI

**Benchmark reveals gaps that matter for real applications**:

- **Drug Discovery**: Predicting molecular structures requires strict conservation of electrons and valence—errors can be fatal
- **Materials Science**: Reasoning about crystal symmetries requires understanding topological constraints
- **Theoretical Physics**: Proposing new particle interactions needs rigorous conservation law verification

**Clear message**: Current MLLMs are not reliable tools for autonomous scientific reasoning without human verification.

## Practical Applications & Use Cases

### 1. **Scientific AI Development**

**Use Case**: Training more capable scientific reasoning systems

**Application**:
- Use FeynmanBench as evaluation metric during development
- Identify failure modes in custom multimodal architectures
- Test hypotheses about which components improve physics reasoning

**Example workflow**:
```
Model A: Standard GPT-4o → 42% accuracy
Add physics constraint verification layer → 61% accuracy
Add symbolic reasoning module → 75% accuracy
```

### 2. **Educational AI**

**Use Case**: Interactive physics tutoring system

**Application**:
- Present Feynman diagram problems to students
- Use benchmark to validate whether AI explanations are physically correct
- Generate practice problems of graduated difficulty
- Identify when AI makes common mistakes (e.g., forgetting conservation laws)

**Benefit**: Ensures educational AI doesn't teach incorrect physics.

### 3. **Model Evaluation in Procurement**

**Use Case**: Organizations selecting multimodal models for scientific applications

**Application**:
- Test candidate models on FeynmanBench
- Compare performance across reasoning categories
- Identify specific weaknesses (e.g., one model is bad at QCD, another at electroweak)
- Make informed trade-offs (e.g., GPT-4o strong on conservation laws but weak on rare processes)

### 4. **Curriculum Learning for LLMs**

**Use Case**: Improving model capabilities through structured training

**Application**:
- Use FeynmanBench to identify which processes the model struggles with most
- Create targeted training data emphasizing weak areas
- Evaluate improvement incrementally

### 5. **Physics-Informed Model Architecture Design**

**Use Case**: Designing specialized multimodal architectures

**Application**:
- Use benchmark to evaluate architectural innovations:
  - Specialized attention mechanisms for graph-structured content
  - Symbolic reasoning modules alongside neural components
  - Physics-aware loss functions during pretraining
  
**Example hypothesis testing**:
- "Does adding a graph neural network layer improve Feynman diagram reasoning?" → Test on benchmark
- "Does physics-aware pretraining help?" → Evaluate before/after

## Insights & Implications

### Broader Field Impact

1. **Establishes Rigor Standards for Scientific AI**
   - Before: Scientific AI benchmarks tested factual recall or simple pattern matching
   - After: Scientific benchmarks now require formal reasoning and constraint satisfaction
   - Likely to reshape how we evaluate AI in other STEM domains (chemistry, biology, mathematics)

2. **Challenges "Good Performance on VQA Means Reasoning" Assumption**
   - Many papers claim progress based on VQA benchmark improvements
   - FeynmanBench shows that strong VQA performance doesn't guarantee domain reasoning capability
   - Implies ML community needs more targeted benchmarks for specific reasoning types

3. **Motivates Physics-Aware AI Research**
   - Results suggest generic architectures have fundamental limits for physics reasoning
   - Likely to inspire work on:
     - Symbolic-neural hybrid architectures
     - Physics-informed neural networks
     - Constraint satisfaction in generative models

4. **Implications for Scientific Applications**
   - Organizations considering MLLMs for drug discovery or materials science should demand physics-grounded reasoning
   - Highlights need for human-in-the-loop validation in real scientific applications

### State-of-the-Art Advancement

**Before**: Multimodal systems evaluated on general vision-language tasks; physics-specific capabilities assumed rather than verified.

**After**: Clear empirical evidence that state-of-the-art multimodal LLMs (GPT-4o, Claude 3.5, Gemini 2.0) struggle with structured scientific reasoning, even on tasks that should be solvable with their training data (Standard Model is well-documented).

**Open question**: Will this spur development of specialized scientific ML models, or will general models improve sufficiently to handle physics reasoning?

### Limitations and Open Questions

1. **Limited to Feynman Diagrams**
   - Findings specific to particle physics notation
   - Results may not generalize to other scientific domains (chemistry, materials science)
   - Need similar benchmarks for other STEM fields

2. **Static Diagrams Only**
   - Real physics often involves animations, simulations, time-dependent processes
   - Benchmark doesn't test dynamic reasoning

3. **No Interactive Element**
   - Students/researchers often ask follow-up questions, refine reasoning iteratively
   - Benchmark tests single-turn reasoning only

4. **Limited to Standard Model**
   - Doesn't test reasoning about beyond-Standard-Model physics (supersymmetry, extra dimensions, etc.)
   - Could be extended to test model-agnostic reasoning frameworks

5. **Assumption: Ground Truth is Physics**
   - Benchmark assumes current physics is correct
   - Doesn't test creative reasoning or novel process prediction
   - Might penalize models that propose new, speculative physics

6. **Language Bias**
   - All benchmarks in English
   - Multilingual evaluation would be valuable for scientific AI accessibility

## Code & Resources

### Official Paper & Benchmark
- **ArXiv**: https://arxiv.org/abs/2604.03893
- **PDF**: https://arxiv.org/pdf/2604.03893
- **HTML**: https://arxiv.org/html/2604.03893
- **Publication Date**: April 4, 2026
- **Venue**: KDD 2026

### Benchmark Access

**Main Repository**: https://github.com/feynmanbench/feynmanbench
- Benchmark dataset (2,017 tasks with ground truth)
- Evaluation code
- Baseline results for state-of-the-art models
- Leaderboard tracking model performance over time

**Hosted Evaluation**: https://feynmanbench.org/
- Browse benchmark tasks
- Submit model predictions
- View detailed error analysis
- Compare model performance

### Dependencies and Setup

**Requirements**:
- Python 3.8+
- PyTorch (for diagram rendering)
- Hugging Face Transformers (for evaluating open-source models)
- OpenAI/Anthropic/Google API keys (for proprietary models)

**Installation**:
```bash
git clone https://github.com/feynmanbench/feynmanbench.git
cd feynmanbench
pip install -r requirements.txt

# Download benchmark
python scripts/download_benchmark.py

# Run baseline evaluation
python eval/evaluate_model.py --model gpt-4o --benchmark feynmanbench
```

### Quick-Start Guide for Using the Benchmark

1. **Explore the Benchmark**:
   ```bash
   python scripts/browse_benchmark.py
   # View sample diagrams and questions
   # Inspect error patterns across models
   ```

2. **Evaluate Your Model**:
   ```bash
   python eval/evaluate_model.py \
     --model your_model_id \
     --benchmark feynmanbench \
     --output results/your_model.json
   ```

3. **Analyze Results**:
   ```bash
   python analysis/analyze_errors.py \
     --results results/your_model.json \
     --output_dir analysis/your_model
   # Generates error categorization, confusion matrices, etc.
   ```

4. **Understand Failure Modes**:
   ```bash
   python analysis/failure_analysis.py \
     --model your_model_id \
     --process_type weak_force  # Focus on specific process type
     --complexity advanced       # Filter by difficulty
   ```

### Compute Requirements

- **Storage**: ~10GB for full benchmark + rendered diagrams
- **Inference**: Varies by model
  - GPT-4o: ~$5-10 per full benchmark evaluation (API pricing)
  - Local models (LLaVA): ~30 mins on A100 GPU
  - Desktop evaluation: Feasible with quantized models

### Extending the Benchmark

**Create Custom Physics Domains**:
```python
from feynmanbench.generators import ProcessGenerator

# Generate new processes beyond Standard Model
gen = ProcessGenerator(process_type="supersymmetry")
diagrams = gen.generate(num_diagrams=500)
benchmark = gen.create_benchmark(diagrams)
```

## Related Work & Context

### Prior Benchmarks

- **VQA 2.0** (Antol et al., 2016): General visual question answering
- **CLEVR** (Johnson et al., 2017): Compositional reasoning over objects
- **SciQA** (Jin et al., 2016): Science question-answering
- **STEM-OP** (Wang et al., 2023): Optics and physics problems (but not formal notation)
- **MathVista** (Lu et al., 2023): Mathematical reasoning with visual content

**Gap**: None of these benchmarks emphasize formal scientific notation with strict rule enforcement.

### Physics and AI

- **Physics-Informed Neural Networks (PINNs)** (Raissi et al., 2019): Embedding physics constraints in neural networks
- **Symbolic Physics Learning** (Udrescu & Tegmark, 2020): Discovering physics from data symbolically
- **Graph Neural Networks for Physics** (Battaglia et al., 2018): Reasoning about systems as graphs

### Particle Physics Background

- **Feynman, R. P.** (1949): Original Feynman diagram formulation (Historical foundation)
- **Peskin & Schroeder** (1995): *An Introduction to Quantum Field Theory* (Standard textbook on QFT and Feynman diagrams)
- **PDG (Particle Data Group)**: https://pdg.lbl.gov/ (Authoritative reference for Standard Model particles and interactions)

### Recent Related Work (2024-2026)

- **Benchmarking Multimodal LLMs on Reasoning Tasks**: Various works evaluating MLLMs on VQA and counting (but not physics-specific)
- **Domain-Specific Generative Models**: Papers on chemistry-specific models suggest domain specificity helps

### Possible Future Research Directions

1. **Beyond Feynman Diagrams**
   - Extend to chemistry (Lewis structures, reaction mechanisms)
   - Extend to biology (metabolic pathways, protein interactions)
   - Create domain-agnostic framework for scientific notation understanding

2. **Interactive Scientific Reasoning**
   - Models that ask clarifying questions about diagrams
   - Iterative refinement of understanding
   - Debugging reasoning steps

3. **Theory-Guided Learning**
   - Use constraint satisfaction solvers as auxiliary teachers
   - Train multimodal models to generate intermediate symbolic representations
   - Combine neural vision with symbolic reasoning modules

4. **Inverse Diagramming**
   - Given textual physics description, generate correct Feynman diagram
   - Evaluates understanding from text→visual direction
   - More challenging reasoning task

5. **Cross-Disciplinary Extensions**
   - Standardized benchmark framework for scientific notation
   - Shared evaluation infrastructure across STEM domains
   - Federated leaderboard for scientific AI

6. **Human Studies**
   - Benchmark performance of physics students and experts
   - Compare human vs. AI reasoning patterns
   - Identify which errors are common across both

## Summary

"FeynmanBench: Benchmarking Multimodal LLMs on Diagrammatic Physics Reasoning" introduces the first comprehensive benchmark for evaluating whether multimodal systems can perform rigorous scientific reasoning. Through analysis of 2,017 physics-grounded tasks, the paper demonstrates that current state-of-the-art models, despite strong general vision-language performance, systematically fail at physics reasoning—often ignoring conservation laws, struggling with topological reasoning, and showing weak domain knowledge. The work has immediate practical value for scientific AI development and broader implications for establishing rigor standards in specialized reasoning tasks. By providing both benchmark and automatic generation framework, FeynmanBench establishes a model for how to evaluate structured reasoning in other scientific domains, likely to influence future work on AI for STEM applications.
