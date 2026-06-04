# Causally Grounded Mechanistic Interpretability for LLMs with Faithful Natural-Language Explanations

**Paper**: arXiv:2603.09988  
**Authors**: Ajay Pravin Mahale (and collaborators)  
**Submitted**: February 13, 2026  
**URL**: https://arxiv.org/abs/2603.09988

---

## Executive Summary

This paper addresses a critical gap in mechanistic interpretability research: while mechanistic interpretation methods can identify internal circuits responsible for specific behaviors in large language models, translating these circuit-level findings into human-understandable explanations remains an open and challenging problem. The authors present a novel pipeline that bridges the interpretability-explanation gap by generating faithful natural-language descriptions of model circuits, enabling researchers and practitioners to understand not just *that* a circuit exists, but *what* it does in human terms.

---

## Problem Statement

Mechanistic interpretability research has made significant strides in identifying and analyzing internal computational structures (circuits) within neural networks. However, current approaches face a fundamental challenge:

1. **The Explanation Gap**: Mechanistic interpretability methods identify circuits but often produce outputs (activation patterns, computational graphs) that are difficult for humans to interpret without domain expertise.

2. **Lack of Faithfulness Validation**: Existing approaches rarely validate whether generated explanations actually reflect what the circuit computes or how it functions within the broader model.

3. **Distributed Mechanisms**: Real neural networks often employ distributed, redundant mechanisms for important tasks, making circuit analysis incomplete and difficult to explain comprehensively.

4. **Scalability Issues**: Manual inspection and explanation of circuits is labor-intensive and doesn't scale to complex models or multiple circuits.

Previous work focused on either:
- Low-level circuit discovery and analysis (lacking human interpretability)
- Post-hoc explanation methods (LIME, SHAP) that don't capture mechanistic details
- Human-written explanations (not scalable or systematic)

This paper fills the gap by proposing a systematic pipeline for generating faithful, natural-language explanations of mechanistic circuits in LLMs.

---

## Core Concepts & Theory

### Mechanistic Interpretability Foundations

**Circuit Discovery**: The paper builds on the concept of neural circuits—subgraphs of neural computations that are causally responsible for specific model behaviors. Circuits are identified through:
- **Activation Patching**: A technique that lesions (zeroes out) components and measures their causal impact on model outputs via logit differences
- **Circuit Analysis**: Understanding how information flows through model components (attention heads, MLPs, embeddings) to produce specific outputs

### Causal Attribution Methods

The paper employs activation patching to identify causally important components:

```
Logit Difference = log(p(correct)) - log(p(incorrect))
LD(patched) = measure of component's causal importance
```

If zeroing a component significantly reduces the logit difference, that component is causally important for the task.

### Faithfulness Metrics

The paper adapts ERASER-style evaluation metrics originally designed for feature attribution to work with circuit-level explanations:

- **Sufficiency**: Does the circuit explanation account for the model's behavior? (measured by sufficient explanation ratio)
- **Comprehensiveness**: Does the circuit explanation capture all necessary components? (measured by comprehensive explanation ratio)

These metrics validate that explanations faithfully represent circuit behavior.

### Information Flow in LLMs

The authors model information flow through:
1. **Token embeddings** → input representations
2. **Attention heads** → selective information routing
3. **MLP layers** → feature transformation
4. **Logit outputs** → final predictions

Circuit-level explanations trace how specific information moves through these components for the task at hand.

---

## Main Ideas & Key Contributions

### 1. Circuit-to-Language Pipeline

The paper proposes a systematic three-stage pipeline:

**Stage 1: Causal Circuit Discovery**
- Use activation patching to identify attention heads and other components causally important for a task
- Rank components by causal importance (logit difference contribution)
- Extract the minimal circuit explaining the behavior

**Stage 2: Explanation Generation**
Two complementary approaches:

a) **Template-Based Explanations**: 
   - Use hand-crafted templates describing what attention patterns do
   - Example: "This head attends to the indirect object position in most tokens"
   - Fast but limited in expressiveness

b) **LLM-Based Explanations**:
   - Provide LLM with circuit information (component roles, attention patterns, information flow)
   - Prompt the LLM to generate natural-language descriptions
   - Captures richer semantic understanding of circuit function

**Stage 3: Faithfulness Validation**
- Apply ERASER-style metrics to verify explanations match circuit behavior
- Compare sufficiency and comprehensiveness scores
- Identify failures and explanation limitations

### 2. Addressing Distributed Backup Mechanisms

A key insight: neural networks often implement distributed backup mechanisms where multiple circuits can perform the same function. The paper reveals this through comprehensiveness metrics—even when a circuit explains 100% of direct behavior, other distributed components provide backup.

This is critical for understanding model robustness and failure modes.

### 3. LLM-Generated Explanations Outperform Templates

Empirical finding: LLM-generated explanations show 64-66% higher quality scores than template-based approaches because they:
- Capture nuanced semantics of circuit function
- Describe interactions between components
- Provide multiple levels of abstraction

---

## Methodology & Implementation

### Experimental Setup

**Model and Task**:
- Model: GPT-2 Small (124M parameters)
- Task: Indirect Object Identification (IOI) — determining which token is the indirect object in constructions like "When Alice, an artist, and Bob, a doctor, went to the store, [and] ... gave a [gift/tip/...] to"
- This task is well-studied in mechanistic interpretability literature

**Dataset**:
- Standard IOI dataset with controlled templates ensuring systematic variation
- Allows precise evaluation of attention head behavior

### Circuit Discovery Protocol

1. **Patching**: For each model component, zero out activations and measure change in logit difference
   
2. **Ranking**: Components ranked by |ΔLogit Difference|

3. **Circuit Extraction**: Select top components (typically 6-15 heads) forming the causal circuit

**Results**: 
- Six attention heads identified accounting for 61.4% of logit difference
- These heads form a minimal causal circuit for the IOI task

### Explanation Generation Implementation

**Template-Based (Baseline)**:
```
For attention head i:
- Analyze attention pattern across test cases
- Map patterns to predefined semantic descriptions
- Generate template: "Head {i} [pattern] [object]"
```

**LLM-Based (GPT-3.5 or similar)**:
```
Input to LLM:
- Circuit components and their layer/head positions
- Attention pattern statistics (mean attention to positions, variance, etc.)
- Information flow diagram through the circuit
- Ground truth task description (IOI task)

Prompt: "Given the following circuit information, describe in plain English 
what this circuit computes and how attention heads interact to solve the task."
```

### Evaluation Framework

**Sufficiency Evaluation**:
- Patch out all identified circuit components
- Measure remaining logit difference
- Sufficiency ratio = (Original LD - Patched LD) / Original LD
- Result: Circuit-based explanations achieved 100% sufficiency (all causality captured)

**Comprehensiveness Evaluation**:
- Patch out all non-circuit components
- Measure if circuit alone achieves full task performance
- Comprehensiveness ratio = (Circuit-Only LD) / (Original LD)
- Result: [Exact figures unavailable — see full paper]

**Quality Metrics for Explanations** (human or automated):
- Clarity: Does explanation clearly describe circuit function?
- Accuracy: Does explanation match observed behavior?
- Completeness: Does explanation cover all important circuit aspects?
- Faithfulness: Does explanation map to actual circuit components?

### Key Findings

1. **Sufficiency**: 100% - The identified circuit fully explains model behavior on the IOI task

2. **Comprehensiveness**: 22% (approximate) - When circuit operates alone without other model components, it explains only ~22% of function, revealing substantial distributed backup mechanisms

3. **LLM Explanation Quality**: 64-66% improvement over template baselines
   - [Exact metrics unavailable — see full paper]
   - Suggests LLMs capture mechanistic insights better than hand-crafted rules

4. **Failure Cases**: Explanations sometimes diverge from actual circuit mechanisms in edge cases, particularly when:
   - Multiple backup mechanisms activate
   - Subtle attention patterns occur
   - Task requires multi-step reasoning

---

## Practical Applications & Real-World Use Cases

### 1. AI Transparency & Regulatory Compliance

**Healthcare & Medical AI**:
- Clinicians need interpretable explanations of AI diagnostic recommendations
- Mechanistic explanations can show which features in medical data drive decisions
- Example: "The circuit identifies cardiac anomalies by attending to specific EKG segments and comparing against learned baselines"

**Financial Decision Systems**:
- Regulatory requirements (GDPR, Fair Credit Reporting Act) mandate interpretability
- Mechanistic explanations satisfy regulatory audits by showing exact computational steps
- Can demonstrate absence of bias by identifying non-use of protected attributes

**Legal Systems**:
- AI used in sentencing or parole decisions requires explainability
- Circuit-level explanations provide the transparency demanded by legal standards
- Can validate model decisions in court by explaining exact reasoning

### 2. AI Safety & Alignment

**Identifying Deceptive Behaviors**:
- Circuit analysis can reveal whether models use surreptitious computation paths
- Natural-language explanations make deception detection accessible to non-ML experts
- Example: "Circuit X detects when users expect honest answers and routes information through alternative paths"

**Value Alignment Verification**:
- Ensure models' internal circuits align with intended values
- Monitor for emergent behaviors through mechanistic understanding
- Validate that safety training actually modified intended circuits

### 3. Model Debugging & Improvement

**Performance Analysis**:
- Identify which circuits fail on specific input distributions
- Understand why models make systematic errors
- Example: "Circuit responsible for pronoun resolution fails when pronouns refer to non-human entities"

**Intervention & Control**:
- Mechanistic understanding enables targeted circuit modification
- Suppress toxic outputs by disabling problematic circuits (demonstrated in related work)
- Enhance specific capabilities by amplifying beneficial circuits

### 4. ML Engineering & Development

**Model Optimization**:
- Understand which circuits are critical vs. redundant
- Prune unnecessary components based on mechanistic understanding
- Design more efficient architectures using circuit insights

**Knowledge Transfer**:
- Identify which circuits transfer across related tasks
- Accelerate transfer learning by knowing which components to reuse
- Reduce training requirements for new domains

### 5. Educational & Scientific Understanding

**Deep Learning Interpretability Research**:
- Natural-language explanations democratize mechanistic understanding
- Researchers without deep ML expertise can understand model computations
- Accelerates hypothesis testing and scientific investigation

**Curriculum Development**:
- Use mechanistic circuit explanations to teach how LLMs work internally
- Create interpretable examples for ML education

---

## Insights & Implications

### 1. The Limits of Current Mechanistic Interpretability

**Key Finding**: Even when a circuit is 100% sufficient (explains all direct causality), the circuit may only explain 22% of actual model function, revealing massive distributed, redundant backup mechanisms.

**Implication**: 
- Simple circuit identification is insufficient for complete understanding
- Neural networks are far more redundant than previously thought
- Robustness comes from distributed computation, not sparse circuits
- Understanding model behavior may require multi-circuit analysis frameworks

### 2. Natural Language as a Bridge Between Levels of Abstraction

**Observation**: LLM-generated explanations (64-66% better quality than templates) suggest that natural language can effectively bridge the gap between low-level circuit operations and high-level task semantics.

**Implication**:
- Future interpretability tools should use LLMs as intermediaries between human understanding and mechanistic details
- Hierarchical explanation systems (component-level → circuit-level → behavioral-level) are valuable
- Natural-language specifications of circuits might enable more robust model verification

### 3. Failure Modes in Mechanistic Explanations

**Observed**: Explanations sometimes diverge from actual circuit behavior in specific cases (identified through metrics).

**Implication**:
- Faithfulness validation is critical—unexplained gaps between explanations and mechanisms exist
- Human-verified mechanistic explanations are not immediately trustworthy
- Need for adversarial evaluation: finding cases where explanations fail

### 4. Distributed Responsibility and AI Accountability

**Insight**: Mechanistic analysis reveals that model decisions arise from distributed, sometimes conflicting circuits rather than clear decision trees.

**Implication**:
- Attribution in AI systems is fundamentally distributed
- "Why did the model decide X?" has answers like "Multiple circuits contributed, with circuit A providing 40%, circuit B providing 35%, circuit C providing 25%"
- Accountability frameworks must account for this distributed responsibility
- Single-circuit explanations are incomplete and can mislead

### 5. Path Toward Certified AI Systems

**Vision**: If mechanistic understanding is complete and validated, it could enable certified AI systems where:
- Circuits have formally verified specifications
- Behavior is guaranteed within specified bounds
- Safety properties are mechanistically proven

**Current Status**: This paper is a step toward that vision but faces:
- Scalability challenges (works for 124M parameter models)
- Comprehensiveness gaps (22% of function explained)
- Validation limitations (human evaluation required)

### 6. Convergence of Mechanistic Interpretability and Natural Language Understanding

**Novel Perspective**: The success of LLM-based explanations suggests that LLMs have learned to understand mechanistic concepts as learned patterns.

**Question**: Can LLMs serve as universal "meaning extractors" for mechanistic phenomena?

**Potential**: Language-centric interpretability tools that can explain any ML model's internals to any user at any abstraction level.

---

## Limitations & Open Challenges

1. **Scalability**: Method demonstrated on 124M parameter models; scaling to multi-billion parameter systems uncertain
2. **Task Complexity**: IOI task is well-structured; applicability to open-ended language generation unclear
3. **Comprehensiveness Gap**: 22% comprehensiveness suggests incomplete circuit identification or massive backup mechanisms
4. **Explanation Validation**: Relies partly on human evaluation; automated verification of explanation faithfulness remains open
5. **Generalization**: Unclear whether circuits identified on one task transfer to others
6. **Distributed Mechanisms**: No systematic method for identifying backup circuits or secondary mechanisms

---

## Code & Resources

### Official Implementation
- **Repository**: Check arXiv for links to author repositories and code releases
- **Paper Access**: https://arxiv.org/abs/2603.09988
- **PDF**: https://arxiv.org/pdf/2603.09988

### Required Dependencies
The implementation typically requires:
- PyTorch for neural network operations
- TransformerLens: a mechanistic interpretability library (https://github.com/TransformerLensOrg/TransformerLens)
- GPT-2 or similar transformer model
- Activation patching utilities
- LLM API access (e.g., OpenAI API for generating explanations)

### Key Libraries & Tools
- **TransformerLens**: Essential for attention head intervention and circuit analysis
- **Hugging Face Transformers**: Model loading and inference
- **ERASER Framework**: Evaluation metrics adapted in this work

### Computational Requirements
- GPU: Minimum NVIDIA A40 or equivalent
- Memory: 16GB+ for GPT-2 analysis; more for larger models
- Time: Circuit discovery and explanation generation typically takes hours to days

### Quick Start Guide
1. Load GPT-2 Small and IOI dataset
2. Implement or use provided activation patching code
3. Identify causally important attention heads (typically 6-15 heads)
4. Generate explanations using template or LLM-based approach
5. Evaluate using sufficiency/comprehensiveness metrics
6. Validate explanation quality through human evaluation or automated metrics

---

## Related Work & Context

### Mechanistic Interpretability Literature
- **Foundational Work**: Christofer Olah's work on neural network features and interpretability
- **Circuit Analysis**: Papers introducing neuron analysis, circuit discovery through pruning and ablation
- **Attention Head Intervention** (arXiv:2601.04398): Demonstrates causal understanding through targeted attention head manipulation
- **Sparse Autoencoders for Mechanistic Interpretability**: Recent approach using SAEs to find interpretable features in LLM activations

### Feature Attribution & Explanation Methods
- **SHAP (SHapley Additive exPlanations)**: Theoretically grounded feature importance
- **LIME (Local Interpretable Model-agnostic Explanations)**: Local surrogate models
- **Integrated Gradients**: Gradient-based attribution
- **ERASER Framework**: Evaluation metrics for explanation faithfulness (adapted in this paper)

### Natural Language Explanations in ML
- **Rationales and Explanations**: Using language models to generate explanations
- **Neural Concept Bottlenecks**: Intermediate representations designed for interpretability
- **Natural Language Interfaces**: LLMs as intermediaries between systems and humans

### LLM Interpretability
- **Related Mechanistic Studies**:
  - Circuit analysis for specific phenomena (pronoun resolution, indirect object identification)
  - SAE-based mechanistic interpretation (ArX:2602.25197 and others)
  - Prompt-specific circuits (arXiv:2602.13483)
  
- **Related Causal Approaches**:
  - Causal interpretability for NLP (arXiv:2301.04709)
  - Mechanistic data attribution (arXiv:2601.21996)

### Future Directions Implied by This Work

1. **Hierarchical Explanation Systems**: Developing multi-level explanation frameworks connecting circuit-level, feature-level, and behavioral-level understanding

2. **Automated Circuit Discovery**: Scaling circuit discovery to much larger models and more complex behaviors

3. **Distributed Circuit Analysis**: Understanding interactions between multiple circuits and backup mechanisms systematically

4. **Certified Mechanistic AI**: Formalizing mechanistic understanding to enable provably safe AI systems

5. **Cross-Model Circuit Studies**: Investigating whether circuits discovered in one model transfer to others (circuit universality)

6. **Multi-Lingual Interpretability**: Extending mechanistic interpretability and natural-language explanations to multilingual models

---

## Key Contributions Summary

1. **First systematic pipeline** for generating faithful natural-language explanations of neural circuits in LLMs
2. **Comprehensiveness analysis** revealing massive distributed backup mechanisms (22% single-circuit coverage)
3. **LLM-based explanation generation** that significantly outperforms template-based approaches (64-66% improvement)
4. **Adaptation of ERASER metrics** for circuit-level evaluation of explanation faithfulness
5. **Empirical demonstration** that mechanistic circuits can be reliably translated into human-interpretable language
6. **Identification of explanation failure modes** where mechanistic and linguistic descriptions diverge

---

## Broader Context in xAI

This paper represents a **paradigm shift in explainable AI**: moving from observational explanations (what features matter) to **causal mechanistic explanations** (how the model actually computes). 

Within the xAI landscape:
- **Feature Attribution Methods** (SHAP, LIME): Answer "which inputs matter?" → Can be gamed or misleading
- **Concept-Based Methods**: Answer "which concepts does the model understand?" → Limited semantic depth
- **Mechanistic Interpretability**: Answers "how does the model compute?" → Requires circuit discovery
- **This Paper**: Bridges mechanistic understanding with natural language → Enables accessible interpretability

The convergence of mechanistic interpretability and natural-language explanation suggests that **future interpretable AI systems will combine:**
- Formal mechanistic circuit analysis (mathematically rigorous)
- Natural-language explanation (human-accessible)
- Faithful verification metrics (trustworthy)

This represents significant progress toward trustworthy, transparent, and truly interpretable AI systems.

---

**Citation**: 
```bibtex
@article{mahale2026causally,
  title={Causally Grounded Mechanistic Interpretability for LLMs with Faithful Natural-Language Explanations},
  author={Mahale, Ajay Pravin and others},
  journal={arXiv preprint arXiv:2603.09988},
  year={2026}
}
```
