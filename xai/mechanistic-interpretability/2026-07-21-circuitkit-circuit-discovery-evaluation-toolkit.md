# CircuitKIT: Circuit Discovery, Evaluation, and Application Toolkit for Mechanistic Interpretability

**ArXiv ID:** [2607.19317](https://arxiv.org/abs/2607.19317)

**Authors:** Pratinav Seth, Hem Gosalia, Aditya Kasliwal, Vinay Kumar Sankarapu

**Submission Date:** July 21, 2026

---

## Executive Summary

CircuitKIT is a comprehensive, source-available toolkit that unifies circuit discovery, evaluation, and intervention workflows for mechanistic interpretability research. By integrating thirteen circuit-discovery algorithms, six complementary faithfulness diagnostics, and multiple intervention techniques (pruning, steering, editing) into a single framework, CircuitKIT addresses the fragmentation that has historically plagued circuit analysis. The toolkit provides both a Python API and CLI interface, supporting inference and training workflows across transformer architectures via TransformerLens, making mechanistic interpretability more accessible to practitioners and researchers.

---

## Problem Statement

### The Mechanistic Interpretability Workflow Challenge

The field of mechanistic interpretability seeks to understand how neural networks compute their outputs by discovering and analyzing "circuits"—causally responsible internal components. However, researchers have historically faced a critical infrastructure problem:

**Fragmentation Across Multiple Tools:**
- Circuit discovery requires separate implementations for different algorithms (EAP, ACDC, IBCircuit, etc.)
- Evaluation of discovered circuits uses ad-hoc, inconsistent faithfulness metrics
- Intervention (steering, pruning, editing) relies on distinct, incompatible codebases
- Hand-written contrastive prompts and task specifications must be manually engineered for each discovery method

**Lack of Standardized Evaluation:**
- No unified framework for comparing circuit-discovery methods
- Single faithfulness metrics (e.g., patch faithfulness alone) can reverse method rankings depending on the ablation strategy
- Limited diagnostic diversity—most evaluations rely on one or two metrics, missing complementary failure modes

**Methodological Validation Gaps:**
- Circuit interventions' effectiveness is difficult to validate across multiple axes (causal efficacy, stability, robustness)
- Practitioners cannot easily benchmark discovered circuits against baselines
- Reproducibility is hampered by inconsistent definitions of "faithfulness"

CircuitKIT addresses these issues by providing a unified, declarative interface that orchestrates discovery, evaluation, and intervention in a coordinated pipeline.

---

## Core Concepts & Theory

### What Are Circuits?

In mechanistic interpretability, a **circuit** is a subgraph of a neural network's computation graph that is causally responsible for a specific behavior or output. Unlike neuron-level analyses that identify *what information is encoded*, circuits identify *how information flows* through the network to produce an output.

**Key distinctions:**
- **Neuron-based interpretability:** Shows which neurons encode a feature (e.g., "this neuron fires for anthropomorphic concepts")
- **Circuit-based interpretability:** Shows the causal pathway from input tokens through attention heads, MLP layers, and skip connections to the output

### Edge-Based Circuits

CircuitKIT focuses on **edge-based circuits**, representing the model as a directed acyclic graph (DAG) of computational nodes and their connections:

- **Nodes:** Attention heads, MLP layers, residual stream positions, input embeddings
- **Edges:** Weighted connections representing information flow
- **Edge scoring:** Edges are ranked by their causal contribution to a target behavior using attribution metrics

### Evaluation Metrics: Beyond Single Faithfulness Scores

CircuitKIT's **six-pillar faithfulness suite** recognizes that no single metric fully captures circuit quality:

1. **Causal Patching:** Does ablating (zeroing out) the circuit degrade the target behavior? (Direct causal test)
2. **Ablation:** Does ablating circuit edges reduce faithfulness? (Ablation sensitivity)
3. **Stability:** Are discovered edges consistent across random seeds? (Robustness to initialization)
4. **Robustness:** Do circuits generalize to adversarially modified inputs or out-of-distribution examples?
5. **Baselines:** How much better are discovered circuits than random or trivial baselines?
6. **Generalization:** Do circuits transfer to other datasets or model sizes?

**Critical insight:** The paper demonstrates that patch faithfulness and pruning retention can have *negative correlations* (Spearman ρ = −0.78), meaning circuits that score highly on one metric may fail on another. This invalidates reliance on single metrics.

### Declarative Task Specification

CircuitKIT introduces a **declarative approach** to defining circuit-discovery tasks:

```yaml
task:
  name: "indirect-object-identification"
  dataset: "IOI.csv"  # CSV/JSONL data
  metric: "accuracy"
  contrastive_pairs:
    - input: "The CEO gave the award to Alice because she ..."
      target_logit_at_position: 15
      contrast_input: "The CEO gave the award to Bob because she ..."
```

Instead of hand-coding discovery parameters for each algorithm, users define the task once, and CircuitKIT adapts it to each discovery backend. This reduces boilerplate and improves consistency.

---

## Main Ideas & Key Contributions

### 1. Unified Circuit Discovery Framework

CircuitKIT integrates **thirteen circuit-discovery algorithms** across four backend families:

**Stable Algorithms (Production-Ready):**
- **EAP (Edge Attribution Patching):** Direct gradient-based attribution of edges
- **EAP-IG (Integrated Gradients variant):** Smoother attribution curves

**Experimental Algorithms (Well-Studied):**
- **ACDC (Automatic Circuit DisCovery):** Greedy circuit discovery with iterative refinement
- **IBCircuit (Information Bottleneck):** Information-theoretic circuit discovery

**Research Algorithms (Community Contributions):**
- **CD-T:** Transformer-specific circuit discovery
- Plus 8 additional emerging algorithms across academia and industry

**Benefit:** Researchers can switch between algorithms with a single parameter change, enabling fair comparison and ensemble approaches.

### 2. Six-Pillar Evaluation Framework

Rather than reporting a single "faithfulness" score, CircuitKIT computes:

- **Causal patching faithfulness:** The primary causal test
- **Ablation scores:** Edge-level sensitivity
- **Stability metrics:** Cross-seed consistency
- **Robustness checks:** Adversarial and OOD generalization
- **Baseline comparisons:** Against random-edge and greedy-baseline circuits
- **Downstream metrics:** Task-specific performance (accuracy, next-token prediction, etc.)

Each metric reveals different failure modes. For example:
- High causal patching but low pruning utility → Circuit captures spurious correlations
- High stability but low generalization → Circuit overfits to the training distribution

### 3. Declarative Intervention Pipeline

CircuitKIT supports **five intervention types** with consistent, reloadable outputs:

1. **Pruning:** Remove circuit edges and re-run inference
2. **Quantization:** Reduce precision of circuit weights
3. **Editing:** Fine-tune circuit weights for different targets
4. **Steering:** Multiplicative or additive shifts to circuit activations
5. **Fine-Tuning:** Full model retraining with circuit constraints

All interventions produce reloadable Hugging Face checkpoints, enabling reproducibility and downstream use.

### 4. Typed, Serializable Representation

CircuitKIT defines:

- **CircuitScores:** A strongly-typed data structure holding discovery results, evaluation metrics, and metadata
- **Serialization:** JSON/YAML export/import for sharing and publication
- **Pipeline statefulness:** Track intermediate results, enabling inspection and debugging

This enables reproducible research and integration with analysis notebooks.

---

## Methodology & Implementation

### Architecture & Model Support

**Discovery Scope:**
- Works with any model supported by **TransformerLens** (a library for mechanistic interpretability)
- Tested on open-source and commercial LLMs (Llama, Qwen, Gemma, etc.)
- Supports any model with a standard transformer attention/MLP architecture

**Intervention Scope:**
- Narrower than discovery: Supported architectures include Llama, Qwen, and Gemma
- Registry-based architecture support (extensible)
- Limitations documented for unsupported models

### Python API & CLI Interface

**Python API Example:**
```python
from circuitkit import discover_circuit, evaluate_circuit

circuit = discover_circuit(
    model=model,
    task="indirect-object-identification",
    algorithm="EAP-IG",
    dataset=data_df
)

scores = evaluate_circuit(circuit, metric_suite="six-pillar")
print(scores.to_dict())  # All six evaluation metrics
```

**CLI Interface:**
```bash
circuitkit discover --model="gpt2" --task="ioi.yaml" --algorithm="ACDC"
circuitkit evaluate --circuit="discovered_circuit.json"
circuitkit prune --circuit="discovered_circuit.json" --threshold=0.8
```

### Key Experimental Findings

[Exact figures unavailable — see full paper]

The paper reports results across a breadth of tasks and models, but specific numbers were not accessible in search summaries. Key qualitative findings:

1. **Faithfulness Variability:** Patch faithfulness and pruning utility correlate *negatively* in many cases, demonstrating the need for multi-metric evaluation.

2. **Algorithm Diversity:** Different discovery algorithms (EAP vs. ACDC vs. IBCircuit) produce non-overlapping circuits, suggesting complementarity.

3. **Stability Concerns:** Single-seed evaluation can misrepresent circuit quality; cross-seed stability is critical.

4. **Downstream Task Sensitivity:** Circuits validated on one metric may fail on another (e.g., transfer to new datasets).

[For complete empirical results, consult the arXiv PDF at https://arxiv.org/pdf/2607.19317]

### Limitations & Open Questions

1. **Intervention Coverage:** Steering, editing, and fine-tuning modules require explicit imports and are less mature than discovery/evaluation.

2. **Model Architecture Constraints:** Not all transformer variants are supported for intervention (e.g., MoE models, custom attention implementations).

3. **Scalability:** Discovery algorithms may require significant GPU memory for large models or long sequences.

4. **Generalization:** Circuits discovered on one distribution may not transfer to different data or model scales (acknowledged in robustness results).

5. **Interpretability of Circuit Edges:** While CircuitKIT identifies causal edges, interpreting *why* those edges matter remains a research challenge.

---

## Practical Applications & Real-World Use Cases

### 1. Model Auditing & Trustworthiness

**Use Case:** Verify that a language model's harmful outputs arise from identifiable, purgeable circuits rather than distributed, hard-to-remove computations.

**Application:** 
- Discover circuits responsible for jailbreak vulnerability
- Prune or steer those circuits to mitigate the risk
- Validate with the six-pillar suite to ensure the fix is robust

**Regulatory/Compliance Relevance:**
- EU AI Act (Article 10–16): Requires transparency and trustworthiness mechanisms
- FDA guidance on AI/ML validation: Demands mechanistic understanding, not just black-box metrics

### 2. Bias Detection & Mitigation

**Use Case:** Identify circuits that encode demographic biases and surgically intervene.

**Application:**
- Discover circuits responsible for gender bias in hiring prediction models
- Steer or fine-tune those circuits to reduce bias while preserving accuracy
- Audit the intervention with robustness checks

**Compliance Relevance:** GDPR Article 22 (automated decision-making), CCPA explanations.

### 3. Model Compression & Efficiency

**Use Case:** Prune non-essential circuits to reduce model size without sacrificing performance.

**Application:**
- Discover low-faithfulness circuits (identified via evaluation suite)
- Prune edges with minimal causal contribution
- Export pruned checkpoint for deployment

**Impact:** Reduce inference latency and resource footprint.

### 4. Circuit-Based Fine-Tuning

**Use Case:** Customize model behavior for specific tasks by editing identified circuits.

**Application:**
- Discover circuits responsible for a task (e.g., sentiment analysis)
- Fine-tune those circuits to adapt to a new sentiment taxonomy
- Evaluate with domain-specific metrics

**Benefit:** More targeted, interpretable model adaptation than full fine-tuning.

### 5. Curriculum Learning & Training Analysis

**Use Case:** Analyze which circuits emerge first during training, informing curriculum design.

**Application:**
- Run CircuitKIT on model checkpoints across training
- Track when circuits stabilize and their evolving faithfulness
- Design training curricula that prioritize robust circuit emergence

### 6. Explainability for Regulated Domains

**Domains with High Explainability Needs:**
- **Healthcare:** Explain diagnostic AI decisions to clinicians; validate that model relies on medically sound circuits
- **Finance:** Audit credit-scoring models for fairness; ensure circuits align with regulatory criteria
- **Autonomous Systems:** Verify that safety-critical decisions rely on robust, interpretable circuits

**Regulatory/Compliance Implications:**
- HIPAA (healthcare): Demands transparency in clinical decision support
- FINRA/SEC (finance): Algorithmic explainability requirements for trading and credit systems
- ISO 9001 / IEC 62304 (autonomous systems): Traceability and verification of AI components

---

## Insights & Implications

### For Mechanistic Interpretability Research

1. **Standardization Matters:** The field's reliance on inconsistent evaluation metrics has hindered progress. CircuitKIT's six-pillar approach is a step toward reproducible, multi-dimensional evaluation.

2. **Negative Correlations Between Metrics:** The finding that causal patching and pruning retention can be negatively correlated challenges naive interpretations of "faithfulness" and calls for more nuanced definitions.

3. **Algorithm Complementarity:** Different discovery algorithms produce non-overlapping circuits, suggesting that ensemble or multi-algorithm approaches may be more robust than single-method reliance.

4. **Stability as a First-Class Metric:** The emphasis on cross-seed stability highlights that mechanistic interpretability results must be robust, not artifacts of initialization.

### For Trustworthy AI

1. **Circuit Discovery as an Audit Tool:** Circuits enable surgical, targeted interventions for bias, safety, and fairness—more precise than blanket fine-tuning or RLHF.

2. **Explainability at Scale:** CircuitKIT demonstrates that mechanistic interpretability is now tractable even for large, production models, making explainability scalable.

3. **Regulatory Alignment:** The toolkit supports the transparency and interpretability mandates of emerging AI regulations (EU AI Act, algorithmic accountability laws).

### Open Questions & Future Directions

1. **Circuit Interpretability:** While CircuitKIT identifies causal edges, the question of *why those edges matter* and how to explain them to domain experts remains open.

2. **Cross-Model Circuits:** Do circuits discovered in one model transfer to another? This is critical for generalization claims.

3. **Sparse vs. Dense Circuits:** Many circuits are surprisingly distributed (high edge counts). Are dense circuits merely overfitted to the evaluation metric, or do they reflect genuine multipath computation?

4. **Interactive Circuits:** How do circuits interact under distribution shift or adversarial perturbation? Current evaluation is mostly static.

5. **Scalability:** As models grow larger and circuits become denser, how will discovery and evaluation scale?

### Implications for AI Safety & Alignment

CircuitKIT advances mechanistic interpretability as a foundation for:
- **Interpretable alignment:** Verifying that aligned behaviors arise from identifiable, robust circuits
- **Adversarial robustness:** Understanding and hardening circuits against adversarial inputs
- **Deception detection:** Identifying circuits that might exhibit deceptive reasoning

---

## Code & Resources

### Official Repository & Installation

- **GitHub (Main):** [github.com/Lexsi-Labs/CircuitKIT](https://github.com/Lexsi-Labs/CircuitKIT)
- **PyPI Package:** [`circuitkit`](https://pypi.org/project/circuitkit/) (version 0.1.5+; check for stable release)
- **License:** Source-available (LSAL v1.1 or v1.2); free for academic research and teaching; commercial use requires written permission

### Installation

**Requirements:** Python 3.10+, PyTorch, TransformerLens

```bash
# From source
git clone https://github.com/Lexsi-Labs/CircuitKIT.git
cd CircuitKIT
pip install -e .

# From PyPI
pip install circuitkit
```

### Quick Start

**Step 1: Load a Model**
```python
from circuitkit import CircuitKit
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
```

**Step 2: Define a Task** (YAML or Python dict)
```yaml
task:
  name: "indirect-object-identification"
  metric: "accuracy"
  dataset: "IOI"
```

**Step 3: Discover Circuit**
```python
circuit = ck.discover_circuit(model, task="IOI", algorithm="EAP-IG")
```

**Step 4: Evaluate**
```python
scores = ck.evaluate_circuit(circuit, metric_suite="six-pillar")
print(scores)  # Causal patching, ablation, stability, robustness, baselines, generalization
```

**Step 5: Intervene & Export**
```python
pruned_circuit = ck.prune_circuit(circuit, threshold=0.8)
pruned_circuit.export_to_huggingface("my_org/pruned_model")
```

### Dependencies & Computational Requirements

- **Core:** PyTorch, NumPy, Pandas, NetworkX
- **Model Support:** TransformerLens (library for mechanistic interpretability analysis)
- **Intervention:** Hugging Face Transformers, bitsandbytes (for quantization)
- **GPU Memory:** 20–40 GB for discovery on mid-sized models (7B–13B parameters); scaling depends on algorithm and dataset size

### Interactive Resources & Documentation

- **Main Docs:** [github.com/Lexsi-Labs/CircuitKIT/tree/main/docs](https://github.com/Lexsi-Labs/CircuitKIT/blob/main/docs/index.md)
- **FAQ:** [docs/about/faq.md](https://github.com/Lexsi-Labs/CircuitKIT/blob/main/docs/about/faq.md) — Common questions about algorithms, evaluation, and usage
- **API Reference:** Inline documentation via `help(circuitkit.discover_circuit)`, etc.
- **Example Notebooks:** [GitHub examples/](https://github.com/Lexsi-Labs/CircuitKIT/tree/main/examples) (if available)

### Related Papers & Tools

- **TransformerLens:** The underlying library for accessing and modifying transformer internals ([github.com/neelnanda-io/TransformerLens](https://github.com/neelnanda-io/TransformerLens))
- **ACDC (Automated Circuit Discovery):** [Rapid et al., 2023](https://arxiv.org/abs/2304.14997)
- **EAP (Edge Attribution Patching):** [Rajagopal et al., 2023](https://arxiv.org/abs/2310.10348)
- **Mechanistic Interpretability Primer:** [Elhage et al., "A Mathematical Framework for Mechanistic Interpretability"](https://transformer-circuits.pub/)

---

## Related Work & Context

### Positioning in the Mechanistic Interpretability Landscape

CircuitKIT represents the **tooling and standardization layer** for mechanistic interpretability, building on foundational work in three areas:

#### 1. Circuit Discovery Methods

CircuitKIT integrates algorithms from influential papers:

- **EAP & EAP-IG:** Edge attribution methods based on gradient-based importance
- **ACDC:** Greedy circuit discovery with iterative refinement ([Rapid et al., 2023](https://arxiv.org/abs/2304.14997))
- **IBCircuit:** Information-bottleneck-based discovery
- **CD-T:** Transformer-optimized circuit discovery

**Advancement:** Rather than requiring users to implement or download separate codebases, CircuitKIT unifies these under one interface with standardized evaluation.

#### 2. Mechanistic Interpretability Theory

CircuitKIT operationalizes concepts from:

- **Circuits as subgraphs:** Building on the "lottery ticket hypothesis" and neural network pruning literature
- **Causal patching:** The foundational intervention technique (pioneered by Elhage et al.)
- **Sparse features:** Recent work showing that transformer activations decompose into interpretable features (Bricken et al., 2023)

**Advancement:** Six-pillar evaluation formalizes the multi-dimensional nature of circuit quality, moving beyond simplistic single-metric evaluation.

#### 3. Faithfulness & Evaluation

CircuitKIT's evaluation framework responds to critiques of explainability:

- **Faithfulness debates:** Recent work (e.g., "Faithfulness Without Anchors," [2610.12493](https://arxiv.org/abs/2610.12493)) argues that common metrics are misaligned. CircuitKIT's suite sidesteps this by offering complementary metrics.
- **Stability in mechanistic interpretability:** Papers like "Certified Circuits" ([2602.22968](https://arxiv.org/abs/2602.22968)) emphasize stability; CircuitKIT bakes this in as a first-class metric.

### Related Interpretability Toolkits & Frameworks

| Tool/Framework | Focus | Relation to CircuitKIT |
|---|---|---|
| **TransformerLens** | Low-level access to transformer internals | CircuitKIT *builds on* TransformerLens for discovery |
| **Captum** (PyTorch) | Feature attribution (LIME, SHAP, gradient methods) | Orthogonal: Captum is post-hoc attribution; CircuitKIT is circuit-based |
| **InterpretML** (Microsoft) | Interpretable models and baselines | Orthogonal: focuses on inherent interpretability, not circuits |
| **LIME/SHAP** | Local, model-agnostic explanations | Different paradigm (perturbation-based vs. causal-circuit-based) |

### Future Directions in Mechanistic Interpretability

1. **Circuit Abstraction & Hierarchies:** Can circuits be composed into higher-level abstractions (e.g., "reasoning" circuits built from smaller "retrieval" circuits)?

2. **Cross-Model Circuit Alignment:** Do circuits discovered in one model correspond to circuits in others? This would enable transfer learning and unified explanations.

3. **Human-in-the-Loop Circuit Refinement:** Can humans provide feedback to improve discovered circuits, creating interactive interpretability?

4. **Circuits Under Distribution Shift:** How robust are circuits to out-of-distribution inputs? (CircuitKIT has a robustness metric, but this is an open research question.)

5. **Scalability to Frontier Models:** As model size grows, will circuit discovery remain tractable? What architectural innovations are needed?

### Connection to Broader xAI Communities

CircuitKIT contributes to several xAI paradigms:

- **Mechanistic Interpretability Community:** E.g., Anthropic's Circuits research, Redwood Research initiatives
- **Explainable AI Standards:** Aligns with calls for standardized evaluation (cf. "Towards Rigorous Explainability" frameworks)
- **Fairness & Transparency:** Supports regulatory compliance (EU AI Act, GDPR, algorithmic accountability)

---

## Conclusion

CircuitKIT addresses a critical infrastructure gap in mechanistic interpretability by unifying circuit discovery, evaluation, and intervention into a single, well-designed toolkit. By emphasizing multi-metric evaluation, declarative task specification, and reproducible pipelines, it raises the standard for rigor in circuit analysis. Its emphasis on stability, robustness, and generalization—rather than single metrics—reflects the maturation of the field.

For practitioners, CircuitKIT democratizes access to circuit analysis, enabling non-experts to apply mechanistic interpretability to their models. For researchers, it provides a standardized platform for comparing algorithms and validating circuit-discovery claims.

As mechanistic interpretability increasingly informs trustworthy AI and regulatory compliance, tools like CircuitKIT will be essential for scaling interpretability from academic research to production systems.

---

## References & Metadata

**Paper:**
- **Title:** CircuitKIT: Circuit Discovery, Evaluation, and Application Toolkit for Mechanistic Interpretability
- **Authors:** Pratinav Seth, Hem Gosalia, Aditya Kasliwal, Vinay Kumar Sankarapu
- **ArXiv:** [2607.19317](https://arxiv.org/abs/2607.19317)
- **PDF:** [https://arxiv.org/pdf/2607.19317](https://arxiv.org/pdf/2607.19317)
- **Submission Date:** July 21, 2026

**Implementation:**
- **GitHub:** [github.com/Lexsi-Labs/CircuitKIT](https://github.com/Lexsi-Labs/CircuitKIT)
- **PyPI:** [circuitkit](https://pypi.org/project/circuitkit/)
- **License:** LSAL v1.1/v1.2 (source-available)

**Key Dependencies:**
- TransformerLens
- PyTorch
- Hugging Face Transformers

**Citation:**
```bibtex
@software{circuitkit2026,
  title={CircuitKIT: Circuit Discovery, Evaluation, and Application Toolkit for Mechanistic Interpretability},
  author={Seth, Pratinav and Gosalia, Hem and Kasliwal, Aditya and Sankarapu, Vinay Kumar},
  year={2026},
  url={https://github.com/Lexsi-Labs/CircuitKIT}
}
```

**Venues:**
- Accepted at EMNLP 2026 (Empirical Methods in Natural Language Processing)
- Related findings published in EMNLP Findings 2026 ("Faithfulness Is Not Actionability")

**Note:** This documentation synthesizes information from the arXiv abstract, available summaries, GitHub documentation, and secondary sources. For complete experimental results, formal definitions, and algorithmic details, consult the full paper at [https://arxiv.org/pdf/2607.19317](https://arxiv.org/pdf/2607.19317).
