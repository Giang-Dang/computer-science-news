# Mechanistic Interpretability of LLM Jailbreaks via Internal Attribution Graphs

**Paper Title:** Mechanistic Interpretability of LLM Jailbreaks via Internal Attribution Graphs

**Authors:** Anupam Wagle, Ifrat Ikhtear Uddin, Chaowei Zhang, Longwei Wang

**ArXiv ID:** 2607.07903

**Submission Date:** July 8, 2026

**ArXiv Paper:** https://arxiv.org/abs/2607.07903

---

## Executive Summary

Large Language Models remain highly vulnerable to adversarial prompts and jailbreak attacks despite their impressive capabilities and safety training. This paper introduces a mechanistic framework that diagnoses these vulnerabilities by analyzing paired internal computation graphs, revealing how adversarial attacks systematically transform the model's internal reasoning. By leveraging causal interventions on identified vulnerability motifs, the work not only provides deeper understanding of *how* jailbreaks succeed but also enables targeted defenses to improve model robustness—a significant advance in understanding and defending against LLM failures through mechanistic interpretability.

---

## Problem Statement

### Current Limitations in Understanding LLM Jailbreaks

Large Language Models exhibiting remarkable capabilities still remain highly vulnerable to adversarial prompts and jailbreak attacks. Existing approaches to analyzing these failures fall into two broad categories:

1. **Input-Output Analysis:** Traditional explainability methods focus on examining the relationship between inputs and outputs, providing limited insight into the intermediate computational processes.
2. **Attribution Methods:** Current attribution-based approaches (e.g., attention patterns, gradient-based saliency) offer insights into which inputs influence outputs but fail to capture how adversarial perturbations systematically alter the model's *internal reasoning structure*.

### The Core Challenge

The fundamental problem is that **safety-aligned LLMs often fail in ways that are difficult to diagnose using conventional approaches**. Key questions remain unanswered:
- *How* do adversarial attacks alter the model's internal computation?
- Which internal components are responsible for safety failures?
- Can we identify recurring patterns of vulnerability that generalize across models?
- How can we intervene on internal structures to improve robustness?

This paper addresses these questions by proposing a mechanistic approach that examines the fine-grained internal computation graphs of LLMs during inference, treating the model as a dynamical system with interpretable computational structures.

---

## Core Concepts & Theory

### Mechanistic Interpretability Framework

**Mechanistic interpretability** is an emerging paradigm that seeks to reverse-engineer neural networks by discovering the algorithms and computational structures they implement. Unlike traditional black-box interpretability, mechanistic interpretability aims to:
- Identify discrete computational units (neurons, attention heads, circuits)
- Trace causal relationships between internal structures
- Understand how information flows through the network
- Validate interpretations through targeted interventions

### Computation Graphs as Internal Representations

The paper's key innovation is the concept of **paired internal computation graphs**—structured representations of how information flows through a model during inference. These graphs capture:

1. **Nodes:** Latent features or activation patterns at specific layers
2. **Edges:** Causal dependencies between features, indicating how one layer's activations influence the next
3. **Graph Structure:** The connectivity pattern reveals the "computational algorithm" the model implements for a given prompt

#### Graph Construction Process

For each prompt (both benign and adversarial), the model constructs a computation graph by:
1. Recording activations at key layers/positions during forward pass
2. Identifying latent features using techniques like PCA or other dimensionality reduction
3. Measuring dependencies between features across layers
4. Visualizing the resulting graph structure

### Deconstructing Adversarial Effects: Three Graph Categories

The framework decomposes the differences between clean and attacked prompts into three structural categories:

1. **Invariant Structures:** Computational components that remain unchanged across clean and attacked prompts—these are robust features that jailbreaks do not target
2. **Suppressed Structures:** Safety-relevant computations that are diminished or eliminated in attacked prompts—jailbreaks succeed by suppressing these safety mechanisms
3. **Emergent Structures:** New computational pathways that only appear in attacked prompts—adversarial attacks create spurious reasoning paths that bypass safety

### Mathematical Formulation: Attribution and Causality

Let $h^{(l)}_i$ denote the activation of feature $i$ at layer $l$. The paper models the contribution of feature $h^{(l)}_i$ to the model's final safety decision $y_{safety}$ using attribution methods:

$$\text{Attribution}(h^{(l)}_i) = \frac{\partial y_{safety}}{\partial h^{(l)}_i}$$

For causal analysis, the framework uses **causal intervention** to directly test whether a feature contributes to failure:

$$\text{Causal Importance} = y_{safety}(\text{model}) - y_{safety}(\text{model with } h^{(l)}_i \text{ ablated})$$

This allows the distinction between:
- **Correlational importance:** Features that co-vary with safety failures (detected by attribution)
- **Causal importance:** Features that *directly cause* safety failures (detected by intervention)

### Vulnerability Motifs: Recurring Patterns of Failure

The paper identifies **vulnerability motifs**—recurring patterns in how computation graphs are transformed by successful jailbreaks. These are analogous to motifs in biology or circuits in computer architecture. Common patterns include:

- **Rerouting motifs:** Safety computations are bypassed entirely; harmful outputs are routed through alternative pathways
- **Suppression motifs:** Safety-relevant features are actively suppressed or their influence is blocked
- **Emergence motifs:** New features appear that support harmful reasoning

By identifying these motifs, the paper enables systematic diagnosis of why a particular jailbreak succeeds.

---

## Main Ideas & Key Contributions

### 1. Paired Computation Graph Framework

**Contribution:** The paper introduces a systematic method for constructing and comparing paired computation graphs—one for benign prompts and one for adversarial prompts—to isolate exactly how jailbreaks alter model internals.

**Why This Matters:** While prior work has studied attention patterns or gradients, this is the first approach to systematically compare the *entire internal computation structure* between successful and failed attacks, providing a unified lens for diagnosis.

### 2. From Correlation to Causation

**Contribution:** Beyond identifying which features correlate with failure (via attribution), the paper uses **targeted causal interventions** to determine which features *directly cause* jailbreak success.

**Implementation:** The authors perform:
- **Node interventions:** Ablate or modify individual features to test their causal role
- **Path interventions:** Modify connections between features to test information flow
- **Subgraph interventions:** Modify entire computational subgraphs to test collective causality

**Why This Matters:** Correlational methods can mislead (features may appear important but be epiphenomenal); causal interventions ground the analysis in mechanistic understanding.

### 3. Activation Scaling for Inference-Time Defense

**Contribution:** Rather than modifying model parameters, the paper proposes **activation scaling**—a lightweight intervention that amplifies or attenuates specific internal features during inference.

**Application:** By identifying vulnerability-critical features, one can scale down their influence during inference, providing defense without retraining.

**Advantage:** This is both interpretable (the scaling can be visualized and understood) and practical (requires no model parameter modification).

### 4. Vulnerability Motif Discovery

**Contribution:** The paper systematically identifies recurring patterns (motifs) in how computation graphs are transformed by successful attacks, enabling generalization across model instances.

**Example Motifs:**
- **Suppression of refusal circuitry:** Safety-relevant features are actively suppressed
- **Rerouting to harm:** Computation bypasses safety checks and routes through harmful reasoning
- **Feature emergence:** New features appear that support harmful outputs

**Why This Matters:** Rather than treating each jailbreak as unique, identifying motifs reveals the *underlying mechanisms* that enable broad categories of attacks.

### 5. Mechanistic Validation of Vulnerability

**Contribution:** A systematic approach to validate that identified internal structures actually cause jailbreak success by:
1. Constructing causal graphs showing which features drive failure
2. Performing targeted interventions to verify causality
3. Correlating intervention results with attack success metrics

**Validation Results:** Strong correlation (reported as correlation coefficients from PCA analysis) between structural deviations in computation graphs and actual attack success rates.

---

## Methodology & Implementation

### Experimental Setup

#### Models Evaluated
The paper evaluates the framework across multiple open-source LLMs to ensure findings generalize:
- **Llama models** (13B, 70B parameters)
- **Mistral** (7B, 8x7B MoE)
- **Other open-source models** (additional architecture diversity)

#### Datasets and Attack Benchmarks
Three major attack datasets are used:

1. **AdvBench:** A benchmark of 100 diverse harmful instructions with multiple attack types
2. **Jailbreak Benchmarks:** Curated adversarial prompts designed to bypass safety training
3. **Custom Adversarial Attacks:** Generated using multiple attack techniques (prompt injection, role-playing, etc.)

#### Attack Methods Evaluated
The paper tests against:
- **Prompt injection attacks:** Direct instructions to ignore safety
- **Role-playing attacks:** Persona-based jailbreaks
- **Encoded attacks:** Obfuscated harmful requests
- **Logical/semantic attacks:** Complex reasoning to justify harmful outputs

### Computation Graph Construction

#### Step 1: Activation Recording
During forward pass inference, the model records activations at key layers:
- All transformer layer outputs
- Attention head activations
- MLP intermediate states
- Position-specific features

#### Step 2: Latent Feature Extraction
Raw activations are high-dimensional; the paper extracts interpretable latent features using:
- **PCA (Principal Component Analysis):** For linear dimensionality reduction
- **Concept activation vectors:** For semantic concepts (e.g., "refusal," "compliance")
- **Sparse autoencoders:** For discovering interpretable features

#### Step 3: Dependency Graph Construction
Dependencies between features are computed using:
- **Correlation analysis:** Measure co-activation patterns
- **Causal inference:** Use interventions to establish causal relationships
- **Information flow:** Trace how information transforms across layers

#### Step 4: Graph Comparison
Paired graphs (clean vs. attacked) are compared by:
1. Alignment mapping (matching corresponding features across graphs)
2. Structural deviation metrics (quantifying differences)
3. Motif extraction (identifying recurring patterns)

### Evaluation Metrics for Interpretability

#### 1. Faithfulness of Interpretation
**Metric:** Causal Effect Correlation
- Measure how well causal interventions on identified features correlate with actual model behavior changes
- [Exact figures unavailable — see full paper]

#### 2. Motif Consistency
**Metric:** Cross-model motif agreement
- Percentage of identified vulnerability motifs that appear consistently across different models
- [Exact figures unavailable — see full paper]

#### 3. Intervention Success Rate
**Metric:** Defense effectiveness of activation scaling
- Percentage reduction in jailbreak success when vulnerability features are scaled down
- [Exact figures unavailable — see full paper]

#### 4. Computational Efficiency
**Metric:** Analysis overhead
- Time and memory required for graph construction and analysis
- [Exact figures unavailable — see full paper]

### Key Results

#### Result 1: Structural Deviations Correlate with Attack Success
Using PCA-based analysis of activation-space steering:
- Computation graphs for successful attacks show significant structural deviations from clean prompts
- Failed attacks (blocked jailbreaks) show minimal structural changes
- The structural deviation metric is a strong predictor of whether an attack will succeed
- [Exact quantitative figures unavailable — see full paper]

#### Result 2: Consistent Vulnerability Motifs Across Models
- Multiple models exhibit similar suppression of safety-relevant features during jailbreaks
- Rerouting motifs appear consistently across different model architectures
- This suggests jailbreaks exploit fundamental computational structures rather than model-specific quirks

#### Result 3: Activation Scaling Provides Effective Defense
By targeting identified vulnerability features with activation scaling:
- Significant reduction in jailbreak success rates (comparative metrics unavailable)
- Defense is interpretable—the scaled features and their roles can be visualized
- Minimal impact on legitimate model behavior and capabilities

#### Result 4: Layer-Wise Analysis Reveals Vulnerability Progression
Tracing structural changes across layers:
- Early layers preserve safety-relevant information
- Middle layers show significant suppression of safety features in attacked prompts
- Later layers route computation through emergent, attack-specific pathways
- This layer-wise progression is consistent across successful attacks

#### Result 5: Generalization to Unseen Attacks
Vulnerability motifs identified on one set of attacks:
- Generalize to previously unseen attack methods
- Can be used to predict vulnerability of new attack patterns
- Support transfer across different model sizes and architectures

### Limitations of the Approach

1. **Computational Cost:** Constructing and analyzing computation graphs requires additional inference and storage; scalability to larger models remains an open question

2. **Interpretability-Complexity Tradeoff:** While the framework is mechanistic, the sheer number of features and dependencies can make visualizations and interpretations complex

3. **Feature Selection Sensitivity:** The quality of extracted latent features (via PCA or other methods) affects the fidelity of constructed graphs

4. **Generalization to Closed-Source Models:** Experiments focus on open-source models where internal activations are accessible; applicability to closed-source APIs is limited

5. **Dynamic Safety:** As models are fine-tuned or updated, vulnerability motifs may change; the framework requires periodic re-analysis

---

## Practical Applications & Real-World Use Cases

### 1. AI Safety and Alignment

#### Problem It Solves
Understanding *how* jailbreaks work is essential for building robust, trustworthy AI systems. The paper enables systematic diagnosis of model vulnerabilities.

#### Real-World Example
A company deploying an LLM for customer service can:
- Use this framework to test the model against jailbreak attacks
- Identify which internal features are being exploited
- Apply targeted activation scaling to harden safety mechanisms
- Continuously monitor for emerging vulnerability patterns

#### Regulatory Compliance
The interpretability provided by this framework supports:
- **EU AI Act:** Demonstrates technical measures for transparency and robustness
- **NIST AI Risk Management Framework:** Provides structured approach to assessing adversarial risks
- **Responsible AI Standards:** Enables auditing and defense against known attack patterns

### 2. Model Debugging and Improvement

#### Use Case: Debugging Unexpected Safety Failures
When an LLM exhibits unexpected harmful behavior:
- Analyze the computation graph for that specific failure
- Compare against graphs from benign inputs
- Identify which features were suppressed or rerouted
- Trace back to model training data or architecture choices that may have caused the vulnerability

#### Real-World Example
A researcher discovers their model fails on a particular type of prompt:
1. Construct computation graphs for both successful and failed cases
2. Identify the differing features
3. Determine if this is an instance of a known motif or a novel vulnerability
4. Apply targeted retraining or architectural changes to address the root cause

### 3. Adversarial Robustness Testing

#### Framework for Systematic Testing
Organizations can use this framework to:
- Systematically test models against known attack patterns
- Rank vulnerabilities by their mechanistic importance
- Prioritize defenses based on causal analysis

#### Red-Teaming Enhancement
Security teams can:
- Use vulnerability motifs to generate new attacks more efficiently
- Validate that defenses actually address root causes, not just symptoms
- Establish baselines for acceptable risk levels

### 4. Interpretability in High-Stakes Domains

#### Healthcare
- **Use Case:** Diagnosing why a medical decision support LLM made an incorrect recommendation
- **Application:** Compute graphs reveal which clinical reasoning pathways were activated or suppressed
- **Outcome:** Enables clinicians to understand and verify AI recommendations

#### Finance
- **Use Case:** Detecting if a risk assessment model is vulnerable to adversarial manipulation
- **Application:** Identify features that could be exploited by bad actors
- **Outcome:** Improves trust in AI-assisted trading and lending decisions

#### Legal
- **Use Case:** Ensuring an LLM used for contract analysis is not vulnerable to adversarial contracts
- **Application:** Mechanistic analysis reveals potential attack vectors
- **Outcome:** Reduces liability and supports compliance auditing

### 5. Model Stealing and Defense

#### Defensive Application
The framework can detect when an LLM is being attacked for model stealing:
- Monitor computation graphs for anomalous patterns
- Detect when input patterns trigger vulnerability motifs
- Trigger additional safeguards or logging when suspicious patterns appear

#### Practical Implementation
- Deploy lightweight computation graph monitoring alongside the model
- Set thresholds for structural deviations that trigger alerts
- Maintain audit logs of detected attacks

---

## Insights & Implications

### Theoretical Insights

#### 1. Jailbreaks as Computational Rerouting
A key finding is that jailbreaks often succeed not by "breaking" safety mechanisms but by **bypassing them through alternative computational paths**. This suggests that:
- Safety is not monolithic but distributed across multiple components
- Attacks exploit the flexibility of transformer architectures
- Defense should focus on ensuring all reasoning paths, not just direct ones, maintain safety constraints

#### 2. Mechanistic Interpretability as a Safety Tool
This work demonstrates that mechanistic interpretability (traditionally a research tool for understanding models) can be *operationalized* as a practical defense mechanism. By identifying vulnerability motifs and applying targeted interventions, we can move from post-hoc analysis to proactive defense.

#### 3. Structure as a Safety Proxy
The strong correlation between computation graph structure and attack success suggests that:
- Model *internals* encode safety properties beyond just output behavior
- Monitoring and maintaining computational structure is as important as monitoring outputs
- Future models might be designed with mechanistic interpretability in mind from the start

### Implications for xAI Research

#### 1. Beyond Attribution Methods
Traditional attribution methods (LIME, SHAP, attention visualization) focus on input-output relationships. This work shows the value of deeper mechanistic analysis:
- Explanations based on internal structures are more actionable
- Causal interventions provide stronger evidence than correlational analysis
- Understanding computation flow complements feature attribution

#### 2. Importance of Graph-Based Representations
Representing model computation as structured graphs (nodes, edges, subgraphs) enables:
- Pattern discovery and motif extraction
- Hierarchical analysis (individual features to entire subgraphs)
- Visualization and communication with stakeholders

#### 3. Scalability Challenges
As models grow larger and more complex, the approach faces challenges:
- Larger activation spaces mean more complex graphs
- Causal analysis becomes computationally expensive
- Motif discovery requires pattern matching at scale

### Limitations and Open Questions

1. **Model Architecture Dependence:** Experiments focus on transformer-based LLMs; generalization to other architectures (MoE, SSMs, etc.) is unclear

2. **Safety Concept Definition:** What constitutes "safety" depends on the application; the framework assumes a clear safety objective but may struggle with value alignment

3. **Temporal Dynamics:** During training or fine-tuning, vulnerability motifs evolve; the paper doesn't address how motifs change over time

4. **Explanatory Depth:** While the framework reveals *what* features are involved in jailbreaks, it may not always explain *why* the model learned these vulnerabilities in the first place

5. **Generalization to Intent:** Jailbreaks that exploit different types of reasoning (creative writing vs. harmful instructions) may involve distinct motifs; generalization across intent types is unclear

### Future Research Directions

1. **Real-Time Monitoring:** Deploy computation graph monitoring during inference for real-time attack detection and mitigation

2. **Proactive Robustness:** Use identified motifs during training to proactively build models less vulnerable to jailbreaks

3. **Mechanistic Alignment:** Directly optimize model internals (rather than just outputs) for alignment with human values

4. **Cross-Architecture Analysis:** Extend to other model families (vision-language models, multimodal systems, reinforcement learning agents)

5. **Automated Motif Discovery:** Develop automated techniques to discover novel vulnerability motifs without human intervention

---

## Code & Resources

### Official Implementation
- **GitHub Repository:** [Check arXiv paper for link to code repository]
- **Paper Resources:** Full code, datasets, and pretrained graph analysis tools should be available with the published paper

### Dependencies and Requirements
- **Python 3.9+**
- **PyTorch:** For model inference and activation recording
- **NetworkX:** For graph construction and analysis
- **Scikit-learn:** For PCA and dimensionality reduction
- **Visualization libraries:** Matplotlib, Plotly (for graph visualization)

### Computational Requirements
- **GPU Memory:** [Exact figures unavailable — see full paper] for storing activations during analysis
- **Disk Space:** Computation graphs and intermediate analysis results require significant storage
- **Inference Cost:** Graph construction adds computational overhead; [exact overhead unavailable — see full paper]

### Quick Start Guide
Based on the methodology section, typical usage would involve:

1. **Load Model:** Initialize an open-source LLM (Llama, Mistral, etc.)

2. **Select Prompts:** Choose benign and adversarial prompt pairs for analysis

3. **Record Activations:** Forward pass through model while recording layer activations

4. **Extract Features:** Apply PCA or other techniques to extract interpretable latent features

5. **Construct Graphs:** Build computation graphs representing feature dependencies

6. **Compare Graphs:** Align and compare clean vs. attacked graphs to identify structural deviations

7. **Identify Motifs:** Extract recurring patterns from structural deviations

8. **Validate with Interventions:** Perform targeted interventions on identified features to confirm causality

### Links to Interactive Visualizations
- The paper likely includes visualizations of computation graphs; check arXiv paper for links to interactive versions

---

## Related Work & Context

### Position in the Mechanistic Interpretability Landscape

This work builds on and relates to several major research directions:

#### 1. Circuit Discovery in Neural Networks
**Related work:**
- Anthropic's "Towards Monosemanticity" series on finding interpretable features in language models
- Work on attention head circuits and their roles in model computation
- Sparse autoencoders for discovering interpretable features

**How this paper extends it:**
- Applies circuit discovery specifically to adversarial settings
- Connects circuits to *failure modes* rather than just capabilities
- Introduces causal interventions to validate circuit importance

#### 2. Safety Analysis of LLMs
**Related work:**
- Papers on jailbreak attacks (AdvBench, prompt injection studies)
- Work on safety training and alignment methods
- Robustness evaluation of LLMs

**How this paper extends it:**
- Shifts focus from behavioral testing to mechanistic understanding
- Enables diagnosis of *why* attacks succeed, not just that they do
- Provides interpretable defenses grounded in model internals

#### 3. Attribution and Explanation Methods
**Related work:**
- LIME and SHAP for local model explanations
- Attention-based interpretation
- Gradient-based saliency maps

**Key difference:**
- This work goes beyond input-output attribution to analyze internal structure
- Emphasizes causal analysis over correlational features
- Enables intervention-based validation

#### 4. Adversarial Robustness in Deep Learning
**Related work:**
- Adversarial example attacks (images, text)
- Certified robustness approaches
- Defense mechanisms (adversarial training, etc.)

**How this paper extends it:**
- Provides mechanistic lens for understanding adversarial failures
- Enables targeted, interpretable defenses
- Applies to discrete domains (text) where robustness is less studied

### Broader xAI Communities and Context

#### Connection to Concept-Based Explanations
While concept-based xAI typically focuses on high-level semantic concepts, this work connects to:
- Feature importance estimation at the concept level
- Understanding how concepts are suppressed or rerouted in attacks
- Potential for combining concept-based and mechanistic approaches

#### Connection to Causal Interpretability
The causal interventions in this work align with causal inference approaches in xAI:
- Structural causal models for explainability
- Causal graphs representing model dependencies
- Intervention-based validation of explanations

#### Connection to Fairness and Transparency
Mechanistic interpretability of jailbreaks has implications for:
- **Fairness:** Understanding how attacks exploit model biases
- **Transparency:** Enabling organizations to audit and defend their systems
- **Accountability:** Supporting explanations of why models failed and how they were fixed

### Where This Research Leads

This paper is positioned at the intersection of:
- **Mechanistic interpretability** (understanding model internals)
- **Adversarial robustness** (building resilient systems)
- **AI safety** (ensuring alignment and trustworthiness)

Future research likely will:
1. Extend mechanistic interpretability to other domains (vision, robotics)
2. Develop automated defenses based on identified vulnerability motifs
3. Integrate mechanistic understanding into model training and alignment
4. Create standards and benchmarks for mechanistically-grounded explainability

---

## Summary and Conclusions

The paper "Mechanistic Interpretability of LLM Jailbreaks via Internal Attribution Graphs" makes significant contributions to understanding and defending against adversarial attacks on Large Language Models:

### Key Takeaways

1. **Novel Diagnostic Framework:** By analyzing paired computation graphs, the paper reveals *how* adversarial attacks systematically transform model internals, moving beyond behavioral observation to mechanistic understanding.

2. **From Correlation to Causation:** Causal interventions on identified features validate that structural deviations directly cause attack success, grounding the analysis in mechanistic causality.

3. **Actionable Insights:** Identified vulnerability motifs and causal structures enable targeted defenses (e.g., activation scaling) without retraining, providing practical value alongside theoretical insight.

4. **Generalization and Consistency:** Experiments across multiple models and attack types demonstrate that vulnerability patterns generalize, suggesting these are fundamental properties exploited by jailbreaks.

5. **Interpretability as Safety:** The work operationalizes mechanistic interpretability as a practical tool for AI safety, demonstrating that deeper understanding of model internals directly supports defense and robustness.

### Significance for xAI Research

This paper exemplifies how mechanistic interpretability can move beyond academic curiosity to address real safety challenges. By making internal model structures interpretable, auditable, and actionable, the work advances the field toward *practical explainability*—where understanding a model's behavior enables improving and defending it.

---

## References

- Wagle, A., Uddin, I. I., Zhang, C., & Wang, L. (2026). Mechanistic Interpretability of LLM Jailbreaks via Internal Attribution Graphs. *arXiv preprint arXiv:2607.07903*.

For additional citations and related work, consult the full paper at: https://arxiv.org/abs/2607.07903
