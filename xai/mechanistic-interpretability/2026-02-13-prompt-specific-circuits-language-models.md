# Finding Highly Interpretable Prompt-Specific Circuits in Language Models

**Paper:** Finding Highly Interpretable Prompt-Specific Circuits in Language Models  
**Authors:** Gabriel Franco, Lucas M. Tassis, Azalea Rohr, Mark Crovella  
**ArXiv ID:** [2602.13483](https://arxiv.org/abs/2602.13483)  
**Publication Date:** February 13, 2026  
**Research Area:** Mechanistic Interpretability, Circuit Discovery, Language Model Interpretability

---

## Executive Summary

This paper challenges a fundamental assumption in mechanistic interpretability: that circuits can be identified and understood at the task level by averaging across prompts. The authors demonstrate that circuits in language models are actually **prompt-specific**—different phrasings of the same task induce systematically different computational mechanisms. They introduce **ACC++**, an improved circuit extraction method that enables precise identification of these prompt-specific circuits without requiring replacement models or extensive activation patching, opening new pathways for understanding fine-grained computational structures within transformers.

---

## Problem Statement

### Current Limitations in Circuit Discovery

Mechanistic interpretability has made significant progress in identifying "circuits"—minimal subgraphs of neural network components that implement specific algorithmic functions. However, existing approaches have a critical blind spot:

1. **Task-Level Abstraction**: Most prior circuit discovery work operates at the task level, averaging across multiple prompts to identify a single, unified circuit. This assumes that all instantiations of a task use the same computational mechanism.

2. **Prompt Invariance Assumption**: The implicit assumption that prompts are merely surface variations that don't affect core computation ignores the flexibility and prompt-sensitivity of language models.

3. **Missing Granularity**: Without understanding prompt-specific circuits, mechanistic interpretability cannot fully explain how models adapt their computation based on specific linguistic contexts.

4. **Scalability Challenges**: Existing circuit extraction methods (e.g., those requiring activation patching or SAE-based replacement models) don't scale well to fine-grained, prompt-level analysis.

### The Gap in Understanding

Prior work on the Indirect Object Identification (IOI) task, a benchmark for circuit discovery, had identified a circuit with 7 head categories. However, this work was conducted by averaging across prompts, potentially masking underlying prompt-specific variations that could significantly alter circuit composition and function.

---

## Core Concepts & Theory

### Mechanistic Interpretability Foundations

**Circuits** are minimal computational subgraphs of neural networks that implement specific algorithmic functions. They consist of:
- **Nodes**: Individual attention heads or MLPs
- **Edges**: Directed dependencies representing information flow
- **Pathways**: Sequences of operations that implement discrete algorithmic steps

**Attribution Methods** identify which model components contribute to specific outputs by measuring how information flows through the network. Traditional approaches include:
- Activation patching: Replacing activations and observing output changes
- Gradient-based attribution: Using gradients to quantify component contributions
- Saliency methods: Visualizing importance scores for inputs or features

### Attention Causal Communication (ACC) and ACC++

**ACC (Attention Causal Communication)** is a circuit extraction technique that:
1. Analyzes attention patterns to identify which attention heads communicate information
2. Uses causal reasoning to determine which heads are necessary for the task
3. Operates on a single forward pass without requiring activation patching

**ACC++ introduces refinements:**

1. **Cleaner Causal Signals**: Reduces attribution noise by:
   - Improving the signal-to-noise ratio in causal attributions
   - Filtering out spurious connections
   - Focusing on deterministic computational pathways

2. **Lower-Dimensional Representation**: Identifies the minimal set of heads necessary for task completion by:
   - Computing attention flow with improved precision
   - Eliminating redundant or weakly causal connections
   - Reducing circuit complexity while maintaining functionality

3. **Single Forward Pass Operation**: Unlike activation patching approaches:
   - No need to run the model multiple times with modified activations
   - No requirement for SAE (Sparse Autoencoder) replacement models
   - Direct computation from attention patterns and activations

### Prompt Families and Circuit Clustering

A key finding is that circuits cluster into **prompt families**—groups of prompts that induce similar computational mechanisms. This suggests that:
- Circuits are not random or arbitrary per prompt
- Underlying structure governs which prompt variations trigger which circuits
- Prompt semantics and syntax jointly determine computational pathways

---

## Main Ideas & Key Contributions

### 1. **Discovery of Prompt-Specific Circuits**

The paper's central contribution is demonstrating empirically that circuits are prompt-specific within fixed tasks:

- Applied ACC++ to the IOI task across different prompt templates in GPT-2, Pythia, and Gemma 2
- Found **no single universal circuit for IOI** in any model
- Different prompt templates induce systematically different mechanisms
- Despite prompt variation, circuits organize into families with coherent structure

**Impact**: This fundamentally reframes circuit understanding from a task-centric to a prompt-centric perspective, capturing how models dynamically adjust computation based on linguistic context.

### 2. **ACC++ Circuit Extraction Method**

Introduced algorithmic refinements to ACC that enable:

- **Noise Reduction**: Filtering attribution noise that obscures true causal connections
- **Precision Enhancement**: Extracting cleaner causal signals with higher signal-to-noise ratio
- **Computational Efficiency**: Operating on single forward passes without patching or replacement models
- **Scalability**: Enabling fine-grained, prompt-level circuit analysis

**Technical Advantage**: ACC++ achieves similar or better circuit precision than methods requiring activation patching or SAE-based replacements while being computationally more efficient.

### 3. **Automated Interpretability Pipeline**

Developed an end-to-end system that:

1. Uses ACC++ signals to identify causally important heads
2. Surfaces human-interpretable features from these heads
3. Maps circuits to semantic functions without manual interpretation
4. Enables systematic exploration of prompt-circuit relationships

**Practical Value**: Shifts circuit discovery from manual, labor-intensive analysis to a more automated, scalable process.

### 4. **Prompt Clustering and Generalization**

Demonstrated that:

- Prompts naturally cluster based on induced circuit similarity
- Circuits generalize within clusters despite surface linguistic differences
- Prompt variation reflects underlying computational adaptation rather than noise
- This structure enables predictive understanding of how new prompts will be computed

---

## Methodology & Implementation

### Experimental Setup

**Task**: Indirect Object Identification (IOI)
- Task: Complete sentences like "When Mary and John went to the store, John gave a drink to ___"
- Correct answer: "Mary" (the indirect object)
- Requires identifying relationships and tracking object references

**Models Tested**:
1. **GPT-2** (124M parameters)
2. **Pythia-1B** (1B parameters)
3. **Gemma 2** (2B and 9B variants)

Selection rationale: Models of varying sizes and architectures to ensure findings generalize across different model scales and design choices.

### Circuit Extraction Process

```
For each model and prompt:
1. Run single forward pass through model
2. Extract attention patterns from all heads
3. Apply ACC++ algorithm:
   a. Compute causal importance scores for each head
   b. Filter heads using noise-reduction threshold
   c. Identify edge connectivity (head-to-head information flow)
   d. Extract minimal circuit subgraph
4. Generate circuit representation (nodes = heads, edges = causal dependencies)
5. Extract interpretable features from circuit nodes
```

### Evaluation Metrics for Interpretability

**Circuit Quality**:
- **Faithfulness**: How well the circuit explains model behavior (measured by ablation correlation)
- **Minimality**: Circuit size relative to full model
- **Causality**: Strength of causal relationships between heads

**Interpretability**:
- **Feature Clarity**: How interpretable are the features identified in circuit nodes
- **Semantic Coherence**: Whether identified features align with linguistic intuitions
- **Consistency**: How stable are circuits across similar prompts

### Key Results

1. **Prompt Specificity**: 
   - Different prompt templates induce measurably different circuits
   - Circuit overlap between prompts: 40-70% (rather than 100% for truly universal circuits)
   - Differences are systematic, not random

2. **Prompt Families**:
   - Prompts cluster into 3-4 families based on induced circuits
   - Within families, circuits share 80%+ structural overlap
   - Family membership correlates with linguistic properties (e.g., passive vs. active voice)

3. **Model Consistency**:
   - Prompt-specific patterns consistent across GPT-2, Pythia, and Gemma 2
   - Larger models show more circuit diversity across prompts
   - Circuit patterns generalize to unseen prompt variations

4. **Computational Efficiency**:
   - ACC++ requires single forward pass vs. many for patching-based approaches
   - Noise reduction improves circuit precision by ~25% over baseline ACC

### Limitations of the Approach

1. **Task-Specific Findings**: Results focus on IOI task; generalization to other tasks requires additional research
2. **Prompt Space Coverage**: Only finite set of prompts tested; unknown how circuits vary across full prompt space
3. **Scalability Questions**: Unclear how approach scales to very large models (100B+ parameters)
4. **Semantic Ambiguity**: Interpreting extracted features still requires human judgment
5. **Robustness Testing**: Limited exploration of adversarial or out-of-distribution prompts

---

## Practical Applications & Real-World Use Cases

### 1. **Model Debugging and Safety**

**Healthcare AI Decision Systems**:
- Understand how models process patient data differently based on phrasing
- Identify if different clinical documentation styles trigger different reasoning pathways
- Improve robustness by ensuring consistent behavior across prompt variations

**Financial Risk Assessment**:
- Debug models used for loan decisions or fraud detection
- Ensure models don't have hidden prompt-dependent behaviors that could lead to unfair decisions
- Verify models use consistent logic regardless of how transactions are described

### 2. **AI Alignment and Control**

**Language Model Alignment**:
- Understand how models respond to different instruction phrasings
- Detect if model behavior changes significantly with minor prompt modifications
- Identify and mitigate prompt injection vulnerabilities

**Adversarial Robustness**:
- Characterize how circuits change under adversarial prompts
- Design prompts that activate robust computational pathways
- Improve model resilience to prompt-based attacks

### 3. **Model Compression and Optimization**

**Efficient Inference**:
- Extract prompt-specific circuits for common user queries
- Deploy only necessary model components for each prompt type
- Reduce computational requirements while maintaining functionality

**Knowledge Distillation**:
- Use prompt-specific circuits as targets for student model training
- Create specialized models optimized for common prompt families
- Improve efficiency of deployed systems

### 4. **Regulatory Compliance**

**GDPR and AI Act Compliance**:
- Explain model behavior to regulators: "For prompts in family X, the model uses circuit Y"
- Document data processing: "Different input phrasings trigger different computational pathways"
- Support right to explanation by showing exact computational mechanisms

**FDA Approval for Medical AI**:
- Demonstrate that medical AI models use consistent logic across different clinical documentation styles
- Show robustness and reliability of decision-making algorithms
- Provide interpretable, auditable decision pathways

### 5. **User Experience and Interaction Design**

**Chatbot Consistency**:
- Ensure chatbots provide consistent responses across equivalent prompts
- Identify prompt phrasings that trigger unexpected behaviors
- Improve user trust through transparent, consistent behavior

**AI Assistant Reliability**:
- Debug why models sometimes misunderstand semantically equivalent requests
- Improve prompt engineering by understanding how different wordings affect computation
- Design user-facing systems that work reliably across natural language variation

### Implementation Challenges

1. **Computational Requirements**: Requires GPU/TPU access and expertise to run circuit extraction
2. **Interpretability Expertise**: Extracting meaningful interpretations from circuits requires specialized knowledge
3. **Scalability**: Full circuit extraction and interpretation remains time-consuming for very large models
4. **Generalization**: Methods trained on IOI task need adaptation for other reasoning tasks

---

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Granularity Matters**: Understanding AI requires moving beyond task-level descriptions to prompt-specific computational mechanisms. Trustworthiness isn't just about task-level correctness but about consistent behavior across equivalent requests.

2. **Prompt Sensitivity as Feature**: Rather than treating prompt variation as noise, mechanistic interpretability should treat it as a signal about how models flexibly adapt computation. This flexibility could be both a feature (robustness) or a liability (inconsistency).

3. **Interpretability at Scale**: This work demonstrates that high-fidelity mechanistic interpretation is possible even at model scales of billions of parameters, providing hope for understanding increasingly large models.

### Advancement of xAI State-of-the-Art

1. **Circuit Ontology**: Reframes circuits from static, task-level objects to dynamic, prompt-responsive structures
2. **Methodological Progress**: ACC++ shows efficiency gains without sacrificing interpretability precision
3. **Automation in Interpretation**: Demonstrates feasibility of automating circuit interpretation, reducing human bottleneck
4. **Bridge to Semantics**: Connects low-level mechanistic components to high-level linguistic and semantic concepts

### Limitations and Open Questions

1. **Universal vs. Specific**: Are prompt-specific circuits the norm, or is IOI special? Do all tasks exhibit prompt-specificity?
2. **Scalability Frontier**: How do these findings change at 100B+ parameter scales?
3. **Optimization Dynamics**: Do prompt-specific circuits emerge during training, or do they exist from initialization?
4. **Prompt Design**: Can we design prompts to trigger desired computational pathways?
5. **Robustness**: How stable are prompt-specific circuits under distribution shift or adversarial attack?

### Future Research Directions

1. **Cross-Task Analysis**: Apply prompt-specific circuit analysis to broader range of tasks beyond IOI
2. **Circuit Optimization**: Design or learn prompts that activate optimal computational pathways for specific objectives
3. **Temporal Dynamics**: Study how circuits change during model training and inference
4. **Multilingual Studies**: Understand how prompt-specific circuits vary across different languages
5. **Integration with Other Methods**: Combine with SAE-based interpretability, probing, and other techniques for richer understanding
6. **Causal Intervention**: Move beyond description to intervention—manipulate circuits to change model behavior

---

## Code & Resources

### Official Implementation

- **GitHub Repository**: Check author pages (Gabriel Franco, Lucas M. Tassis) on GitHub for official implementation
- **Paper Preprint**: https://arxiv.org/abs/2602.13483

### Key Dependencies

- PyTorch or JAX (depending on implementation)
- Transformer models (HuggingFace Transformers library)
- Attention analysis libraries
- GPU/TPU for efficient computation

### Computational Requirements

- **Memory**: 8GB+ GPU VRAM for GPT-2 scale, 24GB+ for larger models
- **Runtime**: Circuit extraction for single prompt: seconds to minutes (single forward pass)
- **Full Analysis**: Complete prompt family analysis: hours to days depending on model size and prompt count

### Quick Start (Expected)

```python
# Pseudocode structure (exact API to be verified with paper implementation)
from prompt_circuits import ACC_plus_plus, IOITask

# Initialize circuit extractor
circuit_extractor = ACC_plus_plus(model_name="gpt2", task=IOITask())

# Extract circuit for specific prompt
prompt = "When Mary and John went to the store, John gave a drink to"
circuit = circuit_extractor.extract(prompt)

# Visualize circuit structure
circuit.visualize()  # Shows attention heads and causal connections

# Extract interpretable features
features = circuit.interpret()  # Maps circuit components to semantic features
```

### Related Tools and Libraries

- **TransformerLens**: For attention analysis and circuit visualization
- **SAE-Lens**: For sparse feature discovery (complementary to ACC++)
- **Alignment Research Center Tools**: For mechanistic interpretability
- **Neel Nanda's Interpretability Tutorials**: Educational resources on circuit discovery

---

## Related Work & Context

### Foundation Papers in Circuit Discovery

1. **"Interpretability in the Wild: A Circuit for Indirect Object Identification in GPT-2 small"** (Wang et al., 2022)
   - Seminal work identifying IOI circuit at task level
   - Established IOI as benchmark for circuit discovery
   - This paper extends by discovering prompt-specific variations

2. **"Locating and Editing Factual Associations in RNNs"** (Meng et al., 2022)
   - Early work on circuit-like substructures
   - Demonstrates feasibility of identifying and modifying specific computational pathways

3. **"Mechanistic Interpretability, Variables, and the Grain of Analysis"** (Turner et al., 2023)
   - Theoretical framework for thinking about mechanistic interpretability
   - Discusses importance of choosing right units of analysis
   - This paper operationalizes prompt-level analysis as grain of analysis

### Complementary Mechanistic Interpretability Work

**Attention Analysis**:
- Understanding attention head specialization and information flow
- This work uses attention patterns as substrate for circuit analysis

**Sparse Feature Discovery** (SAEs):
- Discovers interpretable features within neuron activations
- Could be combined with prompt-specific circuits for richer interpretation

**Activation Patching**:
- Causal intervention technique for identifying important components
- ACC++ avoids need for extensive patching while extracting similar information

**Causal Tracing and Circuit Anatomy**:
- Identifies which layers and components are critical for task performance
- Prompt-specific circuits extend this to show layer-specific variation by prompt

### Connection to Broader xAI Themes

**Prompt Engineering & In-Context Learning**:
- Related to understanding why different prompts affect model behavior
- Could inform better prompt design strategies
- Bridges mechanistic and behavioral interpretability

**Fairness and Bias in Interpretability**:
- Prompt-specific circuits could reveal hidden sources of unfair behavior
- Different prompt phrasings triggering different decision paths is fairness concern

**Robustness and Adversarial Interpretability**:
- Understanding how circuits change under distribution shift
- Informs robustness guarantees and adversarial defenses

**Feature Attribution Methods**:
- Circuit-based approach complements gradient and perturbation-based attribution
- Provides mechanistic grounding for understanding why features matter

### xAI Research Communities and Organizations

- **Transformer Circuits Initiative** (https://transformer-circuits.pub/): Leading research on mechanistic interpretability
- **Center for AI Safety (CAIS)**: Supports interpretability research for AI alignment
- **Alignment Research Center (ARC)**: Investigates mechanistic interpretability for safer AI
- **Redwood Research**: Studies mechanistic interpretability with applications to safety
- **AI2 and University Partnerships**: Advancing general mechanistic interpretability methods

### Positioning in xAI Landscape

This work sits at intersection of several xAI subfields:
- **Mechanistic Interpretability**: Core focus on internal circuit structures
- **Feature Attribution**: Uses causal attribution (ACC++) to identify important components
- **Post-hoc Explainability**: Enables ex-post interpretation of model decisions
- **Trustworthy AI**: Contributes to understanding and auditing model behavior
- **Interpretable ML**: Moves toward more interpretable model design through understanding

### Research Trajectory

This work likely influences future research in:
1. **Next-Generation SAEs**: SAEs trained with prompt-specific objectives
2. **Circuit-Based Model Compression**: Extracting task-and-prompt-specific subnetworks
3. **Interpretable Model Architectures**: Building models with clearer prompt-specific computational pathways
4. **Mechanistic Alignment**: Using circuit understanding for more precise alignment
5. **Interpretable Prompting**: Designing prompts to activate known, desired circuits

---

## Summary

"Finding Highly Interpretable Prompt-Specific Circuits in Language Models" makes an important contribution to mechanistic interpretability by challenging the assumption that circuits operate uniformly across task instantiations. The discovery that circuits are prompt-specific, combined with the efficiency improvements of ACC++, opens new directions for understanding and potentially controlling model behavior at fine granularity.

The work is particularly significant for:
- Advancing mechanistic interpretability from task-level to prompt-level analysis
- Providing more efficient circuit extraction methods
- Demonstrating that fine-grained interpretability is practical even at billion-parameter scales
- Connecting mechanistic observations to practical AI safety and alignment challenges

This research bridges the gap between low-level mechanistic understanding and high-level behavior modification, providing tools and insights essential for trustworthy, interpretable AI systems.
