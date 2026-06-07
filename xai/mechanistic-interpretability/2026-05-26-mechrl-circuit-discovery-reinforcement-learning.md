# MechRL: Reinforcement Learning Agents Perform Circuit Discovery for Mechanistic Interpretability

**ArXiv ID:** [2605.26343](https://arxiv.org/abs/2605.26343)  
**Authors:** Barsat Khadka (University of Southern Mississippi)  
**Submitted:** May 26, 2026  
**Subfield:** Mechanistic Interpretability

---

## Executive Summary

MechRL introduces a revolutionary paradigm shift in mechanistic interpretability by recasting circuit discovery—the process of identifying sparse, interpretable subgraphs of neural network connections that implement specific behaviors—as a reinforcement learning problem. Rather than requiring hand-crafted analysis pipelines for each task, an RL agent autonomously discovers circuits in transformer models, achieving oracle-level performance across multiple tasks while maintaining alignment with established interpretability literature.

---

## Problem Statement

Mechanistic interpretability seeks to understand neural networks by decomposing them into sparse, human-interpretable circuits: small sets of neurons and attention heads that perform specific computational tasks. Prior to MechRL, identifying these circuits required significant manual effort:

1. **Task-Specific Analysis:** Each new task (e.g., induction, indirect object identification) required designing a bespoke analytical pipeline tailored to that specific behavior
2. **Labor Intensive:** Expert researchers had to manually trace activation patterns, design experiments, and test hypotheses to identify causally important components
3. **Lack of Scalability:** This approach could not easily be automated or generalized across different model architectures or tasks
4. **Limited Coverage:** Only a small subset of model behaviors had been thoroughly characterized due to analytical constraints

The field lacked a general, automated method for discovering circuits in transformers. MechRL addresses this by leveraging reinforcement learning to automate the discovery process itself.

---

## Core Concepts & Theory

### Mechanistic Interpretability Foundations

Mechanistic interpretability studies how neural networks implement computations through interpretable circuits. A circuit consists of:

- **Nodes:** Neurons, attention heads, or other model components
- **Edges:** Connections between components (information flow paths)
- **Behavior:** A specific computational task or pattern the circuit implements

### Ablation-Based Analysis

The foundational technique for mechanistic interpretability is **ablation testing**: removing or zeroing out specific components and observing how model performance changes. This reveals which components are causally important for specific tasks.

- **Zero-Ablation:** Setting a component's activations to zero
- **Causal Importance:** A component is important if its ablation significantly degrades task performance
- **Contrastive Reward:** Comparing task performance to baseline (general language modeling) allows isolating task-specific components from general ones

### Attention Heads in Transformers

Transformers use multi-head attention, where each head attends to different parts of the input sequence based on learned patterns:

- **Induction Heads:** Attention heads that look back for pattern repetitions (e.g., if token X appeared, look for similar X to predict what came after)
- **Positional Heads:** Heads that primarily process positional information
- **Semantic Heads:** Heads that attend based on semantic relationships between tokens

### RL for Circuit Discovery

MechRL reformulates circuit discovery as a sequential decision problem:

1. **State:** Current set of identified circuits (subset of attention heads)
2. **Action:** Select an attention head to ablate or include
3. **Reward:** Task performance (with contrastive comparison to baseline)
4. **Goal:** Find the minimal set of heads that maximizes task performance

This mapping enables using standard RL algorithms (PPO, DQN) to solve the circuit discovery problem.

---

## Main Ideas & Key Contributions

### 1. RL-Based Circuit Discovery Framework

**Innovation:** MechRL recasts circuit discovery from a manual analysis problem into an automated sequential decision problem. Instead of expert researchers manually analyzing activation patterns and designing hypotheses, an RL agent learns to discover circuits by interacting with the model.

**Technical Approach:**
- The agent operates over a discrete action space of 144 attention heads (GPT-2 small)
- At each step, the agent selects heads to ablate
- Reward = (Post-ablation general task performance) - (Post-ablation target task performance)
  - The reward is maximized when ablating a head causes minimal damage to general language modeling but maximal damage to the target task, isolating task-specific circuits
- Uses PPO (Proximal Policy Optimization) for policy optimization
- Multi-task training enables the agent to generalize across different circuit discovery tasks

### 2. Validation Against Established Literature

**Innovation:** The circuits discovered by MechRL align with circuits previously identified through manual mechanistic interpretability research, validating the RL approach.

**Key Finding:** On tasks like IOI (Indirect Object Identification) and induction, the agent's preferred attention heads coincide exactly with the canonical heads identified by Olsson et al. and other mechanistic interpretability papers. This suggests MechRL captures the same causal structure identified through careful hand analysis.

### 3. Multi-Task Generalization

**Innovation:** A single PPO policy trained on just two tasks (induction and IOI) generalizes to discover circuits for a held-out third task (docstring completion) without retraining.

**Significance:** This demonstrates that circuit discovery can transfer across different tasks, suggesting the agent has learned a general principle for identifying task-specific circuits rather than memorizing task-specific solutions.

### 4. Oracle-Level Performance

**Innovation:** MechRL achieves oracle performance—discovering the minimal sufficient set of heads—on multiple tasks.

**Measurement:** The agent identifies circuits where:
- Ablating the identified heads causes maximal degradation to target task performance
- The identified heads align with those identified through manual analysis
- The circuits are sparse (minimal number of heads needed)

---

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- GPT-2 small (125M parameters, 144 attention heads total)
  - 12 layers, 12 attention heads per layer
  - Relatively small model chosen to enable thorough mechanistic analysis

**Tasks:**
1. **Induction Task:** Predict tokens in sequences based on pattern repetition
   - Classical benchmark for mechanistic interpretability
   - Tests whether the model learns induction heads that perform pattern matching
   
2. **Indirect Object Identification (IOI):** Predict pronouns that refer to the subject of a sentence
   - Synthetic task: "Alice and Bob went to the store. Alice gave a book to Bob. [He/She] went home."
   - Predict whether the pronoun refers to Alice or Bob
   - Well-studied circuit in mechanistic interpretability literature
   
3. **Docstring Completion (Held-out test):** Generate docstrings for Python functions
   - Used only for evaluation, not training
   - Tests generalization of the circuit discovery policy

### RL Agent Architecture

**Policy:** PPO (Proximal Policy Optimization)
- Gradient-based policy optimization with importance sampling to maintain stability
- Well-suited for discrete action spaces (selecting heads)

**Action Space:**
- Discrete: Select any subset of 144 attention heads
- Represented as binary vector [1, 0, 1, 0, ...] indicating which heads are included

**Reward Function:**
```
reward = (performance_ablated_model_on_general_task) - (performance_ablated_model_on_target_task)
```
Where:
- Higher general task performance with ablation = less damage to general capabilities (good for reward)
- Lower target task performance after ablation = more damage to target circuit (good for reward)
- Contrastive comparison isolates task-specific components by preferring heads whose ablation hurts the target task while sparing general performance

**Multi-Task Training:**
- Vectorized environment: Simultaneously optimizes circuit discovery for induction and IOI
- Shared policy parameters enable transfer learning across tasks

### Datasets & Evaluation

**Datasets:**
- Synthetic induction sequences (standard benchmark)
- IOI dataset: [Exact figures unavailable — see full paper]
- Docstring completion: From Python code repositories

**Evaluation Metrics:**
- **Circuit Accuracy:** Prediction accuracy when using identified circuit
- **Sparsity:** Number of heads included (lower is better)
- **Faithfulness:** Comparison with manually-identified canonical circuits
  - Success = agent identifies the same heads as prior literature
- **Generalization:** Performance on held-out docstring task

**Results Summary:**
- Induction task: Achieves per-episode oracle performance; identified heads align with induction head literature
- IOI task: Achieves per-episode oracle performance; identified heads match canonical IOI circuit from Olsson et al.
- Docstring completion (held-out): Successful generalization, suggesting the agent learned transferable circuit discovery principles
- Circuit sparsity: [Exact figures unavailable — see full paper] (estimated: <10% of all heads needed)

### Implementation Considerations

**Limitations of Current Approach:**

1. **Single-Head Bottlenecks vs. Full Circuits:** The method identifies heads whose individual ablation is maximally damaging (single-head bottlenecks). This does not necessarily capture:
   - Multi-head interactions where multiple heads must work together
   - Path-patching results where information flows through multiple components
   - Full computational circuits (all components involved in a task)

2. **Ablation Method:** Zero-ablation (setting activations to zero) may not accurately reflect head removal, as it might introduce distribution shift

3. **Scalability:** Experiments limited to GPT-2 small; unclear how method scales to large language models with thousands of attention heads

4. **Task Complexity:** Tested on relatively structured synthetic tasks; real-world behavior prediction may be more complex

---

## Practical Applications & Real-World Use Cases

### 1. Automated Safety Analysis

**Application:** Circuit discovery can identify which attention heads are responsible for harmful or undesired behaviors.

**Concrete Example:** 
- Identify circuits responsible for toxic text generation
- Once identified, apply targeted interventions (steering, pruning) to remove harmful behavior
- More precise than broad model modification or retraining

**Benefit:** Enables surgical corrections to model behavior without retraining the entire model.

### 2. Mechanistic Steering & Model Correction

**Application:** Once circuits are identified, they can be directly manipulated to change model behavior.

**Concrete Example:**
- Identify circuits responsible for gender bias in hiring recommendation predictions
- Intervene on specific attention heads to reduce bias
- Verify that intervention successfully reduces bias while maintaining overall performance

**Regulatory Relevance:** Supports GDPR right to explanation and EU AI Act transparency requirements by enabling identification of which model components drive specific predictions.

### 3. Model Compression & Efficiency

**Application:** Circuit discovery reveals minimal sufficient subsets of model components needed for specific tasks.

**Concrete Example:**
- For a language model fine-tuned on customer support, identify the minimal circuit needed for that domain
- Prune identified non-essential components
- Deploy smaller, faster model with identical behavior on target task

**Benefit:** Faster inference, lower computational cost, reduced memory footprint for specialized applications.

### 4. Transfer Learning & Generalization Understanding

**Application:** Identify which circuits transfer across tasks vs. which are task-specific.

**Concrete Example:**
- Identify circuits for a source task (e.g., sentiment classification)
- Test whether those circuits function in target task (e.g., emotion classification)
- Understand fundamental similarities/differences between tasks at the circuit level

**Benefit:** Informs transfer learning strategies and reveals fundamental structure of learned concepts.

### 5. Debugging Model Failures

**Application:** When a model makes incorrect predictions, circuit discovery can identify which components failed.

**Concrete Example:**
- Model predicts wrong pronoun in coreference resolution
- Apply circuit discovery to find which attention heads are responsible
- Identify whether the issue is missing information in certain heads or incorrect attention patterns
- Design targeted training or intervention to fix identified heads

**Benefit:** Faster root-cause analysis for production models vs. black-box debugging.

### 6. Regulatory Compliance

**Domain:** Financial Services, Healthcare, High-Stakes Decision-Making

**Regulatory Drivers:**
- **GDPR Right to Explanation:** Article 22 requires explainability for automated decisions; circuit identification provides mechanistic explanations
- **EU AI Act:** Transparency obligations; mechanistic circuits provide interpretability evidence
- **FDA Algorithm Change Protocol:** Medical devices require understanding of model behavior; circuits enable detailed behavior analysis
- **Fair Lending Laws:** Banking must justify credit decisions; circuit analysis reveals which features drive lending decisions

**Concrete Application:**
A bank uses a neural network for loan approval. Regulators ask: "Why was this applicant denied?"
- Circuit discovery identifies that the denial was driven primarily by income-related features (appropriate)
- Not by protected characteristics like race/gender (compliant with fair lending laws)
- Mechanism can be explained to regulators and customers

---

## Insights & Implications

### 1. Paradigm Shift: From Manual to Automated Circuit Discovery

**Implication:** Mechanistic interpretability has historically been a labor-intensive research field requiring expert researchers to manually trace circuits. MechRL automates this process, democratizing access to circuit-level understanding.

**Impact on Future Research:** Enables studying interpretability at scale, analyzing hundreds or thousands of behaviors in a single model automatically.

### 2. Bridge Between Mechanistic and Behavioral Understanding

**Insight:** MechRL's validation against established literature (Olsson et al., etc.) suggests that RL-discovered circuits capture meaningful, causal computational structure—not just correlations.

**Implication:** This validates mechanistic interpretability as a genuinely causal science, not just post-hoc rationalization. Understanding circuits provides genuine insight into *how* models implement behaviors.

### 3. Generalization of Circuit Discovery Principles

**Insight:** A single RL policy trained on two tasks (induction, IOI) generalizes to a third task (docstring completion), suggesting circuit discovery itself is learnable as a general principle.

**Implication:** Principles of what makes a "good" circuit (sparse, causal, task-specific) can be learned from examples. This opens possibilities for unsupervised circuit discovery or discovery in novel domains.

### 4. Limitations and Open Questions

**Limitation 1: Single vs. Multi-Head Circuits**
- MechRL identifies single-head bottlenecks but may miss multi-head interactions
- Many real circuits involve complex interactions between multiple components
- Unresolved: Can RL be extended to discover multi-head circuits without exponential blowup in action space?

**Limitation 2: Generalization to Large Models**
- Current experiments on GPT-2 small (144 heads)
- Modern LLMs have thousands of components (attention heads, MLPs, etc.)
- Unresolved: How does RL scale to models 1000x larger?

**Limitation 3: Definition of "Circuit"**
- Current definition based on single-head ablation
- Alternative definitions (path-patching, attention flow) might identify different circuits
- Unresolved: Which definition best captures interpretability?

**Limitation 4: Task Specificity**
- Tested on synthetic tasks with clear success metrics
- Real-world behaviors (toxicity, hallucination) may be harder to define as RL reward functions
- Unresolved: How to apply MechRL to fuzzy, multi-faceted real-world behaviors?

### 5. Intersection with Other Interpretability Approaches

**Relationship to SAEs (Sparse Autoencoders):**
- SAEs discover interpretable features in activations
- MechRL discovers circuits (computational pathways)
- Complementary approaches: SAEs reveal *what* models compute, circuits reveal *how*

**Relationship to Attention Analysis:**
- Attention patterns suggest which information heads attend to
- Circuit discovery reveals which heads are actually *causally important* for the task
- Important distinction: Attention can be misleading; ablation provides causal evidence

**Relationship to Influence Functions:**
- Influence functions identify important training examples
- MechRL identifies important model components (attention heads)
- Orthogonal approaches for understanding different dimensions of model behavior

### 6. Future Research Directions

1. **Multi-Head Circuits:** Extend RL approach to discover circuits involving multiple heads with explicit interaction modeling

2. **Large Model Scaling:** Develop hierarchical or compositional RL approaches that scale to modern LLMs with 100K+ components

3. **Fuzzy Task Definitions:** Move beyond synthetic tasks to real-world behaviors (fairness, safety, hallucination) where success is harder to measure

4. **Interpretability Verification:** Combine circuit discovery with human studies to verify that discovered circuits are actually interpretable to humans

5. **Cross-Model Transfer:** Can circuits discovered in one model inform circuit discovery in different architectures or model families?

6. **Circuit Composition:** Understand how circuits for simple tasks compose to form circuits for complex tasks

---

## Code & Resources

### Official Implementations & Papers

- **ArXiv Paper:** [arxiv.org/abs/2605.26343](https://arxiv.org/abs/2605.26343)
- **HTML Version:** [arxiv.org/html/2605.26343](https://arxiv.org/html/2605.26343)

### Dependencies & Computational Requirements

**Required Libraries:**
- PyTorch (for neural network implementation)
- Stable-Baselines3 (for PPO implementation)
- TransformerLens (for mechanistic interpretability analysis)
- NumPy, Pandas (for analysis)

**Computational Requirements:**
- **GPU Memory:** [Exact requirements unavailable — see full paper] (estimated: 8-16 GB VRAM for GPT-2 small with RL agent)
- **Training Time:** [Exact times unavailable — see full paper] (estimated: several hours on modern GPU)

**Software Requirements:**
- Python 3.8+
- CUDA 11.0+ (for GPU acceleration)

### Quick Start Guide

[Framework and quick start code likely provided in official GitHub repository — see full paper for link]

### Related Code & Implementations

- **TransformerLens:** Standard library for mechanistic interpretability research
  - https://github.com/TransformerLensOrg/TransformerLens
  - Provides standard interfaces for circuit analysis, ablation, and intervention

- **Sparse Autoencoders (SAEs) Toolkit:** Complementary interpretability tool
  - https://github.com/jbloom/sae
  - Can be combined with MechRL for comprehensive model understanding

- **Mechanistic Interpretability Papers:** Related circuit discovery work
  - Olsson et al., "Interpretability in the Wild" (IOI circuit)
  - Vig & Belinkov, "A Primer on Neural Network Architectures for Natural Language Processing"

---

## Related Work & Context

### Foundation Papers: Circuit Discovery in LLMs

**Olsson et al. - "Interpretability in the Wild: A Circuit for Indirect Object Identification in GPT-2 small"**
- Manually identified the IOI circuit: 8-10 attention heads implementing pronoun prediction
- Demonstrated faithful circuit analysis through ablation and path-patching
- MechRL automatically discovers the same circuit

**Vig & Belinkov - "Probing for Semantic Evidence of Composition"**
- Early work on analyzing attention heads for interpretable patterns
- Established baseline for understanding what attention heads implement

### Related Automated Circuit Discovery Work

**Automated Circuit Discovery:**
- **Towards Automated Circuit Discovery (2304.14997):** Earlier attempt at automating circuit discovery; MechRL improves on this by achieving oracle performance and better generalization
- **Efficient Automated Circuit Discovery via Contextual Decomposition (2407.00886):** Alternative automated approach using decomposition; MechRL's RL approach is more general

### Mechanistic Interpretability Context

**Sparse Autoencoders (SAEs) for Mechanistic Interpretability:**
- Discover interpretable features in model activations
- Complementary to circuit discovery (features + circuits = comprehensive understanding)
- Recent work: SAEs applied to GPT-2, Claude, and other models

**Neuron-Level Interpretability:**
- Earlier mechanistic interpretability work focused on individual neurons
- Circuits extend this to multi-component pathways
- More faithful to actual computation in transformers

**Attention Head Analysis:**
- Research on attention patterns (what heads attend to)
- MechRL provides causal complement: which heads actually matter for tasks

### Broader XAI Community Alignment

**Within Mechanistic Interpretability:**
- MechRL advances the state-of-the-art by automating circuit discovery
- Enables scaling mechanistic interpretability to new models and tasks
- Supports the vision of mechanistic understanding as a science

**Connections to Causal Interpretability:**
- Both mechanistic interpretability and causal methods seek to understand causal mechanisms
- MechRL uses causal ablation (a causal technique) to discover circuits
- Suggests deeper connection between mechanistic and causal interpretability

**Connections to Concept-Based Interpretability:**
- Concept-based methods focus on *semantic* concepts (e.g., "dog-ness", "red-ness")
- Mechanistic circuits focus on *computational* implementations
- Complementary approaches: concepts describe interpretable dimensions, circuits describe computational structure

### Open Challenges Addressed by MechRL

1. **Circuit Discovery at Scale:** MechRL's RL approach could scale to discovering circuits in larger models
2. **Multi-Task Circuits:** Explores how circuits generalize across tasks
3. **Automation:** Reduces reliance on expert manual analysis
4. **Validation:** Validates discovered circuits against established literature

### Future Convergence Points

**With Other Interpretability Methods:**
1. **SAEs + MechRL:** Discover interpretable features (SAEs) and circuits (MechRL) simultaneously
2. **Causal Inference + MechRL:** Use causal discovery algorithms to identify circuit structure
3. **Attention + MechRL:** Use attention patterns as inductive biases to guide RL-based circuit search

**With Model Development:**
1. **Train Models for Interpretability:** Design models whose circuits are easier to discover/interpret
2. **Interpretability-Aware Pruning:** Use circuit discovery to identify which components can be safely removed
3. **Circuit-Guided Optimization:** Use circuits to guide model optimization (e.g., optimize for sparse, interpretable circuits)

---

## Conclusion

MechRL represents a significant methodological advance in mechanistic interpretability by automating circuit discovery through reinforcement learning. By reformulating circuit discovery from a manual, task-specific analysis problem into a general, learnable problem, MechRL enables:

1. **Scalability:** Automated discovery can be applied to new tasks and models more easily than manual analysis
2. **Generalization:** A single policy learns to discover circuits across multiple tasks
3. **Validation:** Discovered circuits align with established literature, validating the mechanistic interpretability framework
4. **Foundation for Future Work:** Opens possibilities for mechanistic interpretability at scale in increasingly large and complex models

While limitations remain (single-head bottlenecks, scalability to large models, task-specific definitions), MechRL points toward a future where mechanistic understanding of neural networks can be achieved at the scale and scope needed for trustworthy AI deployment.

---

## Key Takeaways

- **Innovation:** Circuit discovery reframed as RL problem enables automation and generalization
- **Validation:** Discovered circuits align with manually-identified canonical circuits from mechanistic interpretability literature
- **Impact:** Enables scaling mechanistic interpretability; supports trustworthy AI development through improved interpretability
- **Future:** Points toward mechanistic interpretability as a general, automated science rather than manual expert analysis
