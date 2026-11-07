# Discovering Transformer Circuits via a Hybrid Attribution and Pruning Framework

**Authors:** Hao Gu, Vibhas Nair, Amrithaa Ashok Kumar, Jayvart Sharma, Ryan Lagasse  
**ArXiv ID:** [2510.03282](https://arxiv.org/abs/2510.03282)  
**Submission Date:** October 3, 2025  
**Affiliation:** Algoverse AI Research  
**Venue:** NeurIPS 2025 Workshop on Mechanistic Interpretability, NeurIPS 2025 Workshop on New Perspectives in Graph Machine Learning

---

## Executive Summary

This paper presents a hybrid attribution and pruning (HAP) framework for efficiently discovering faithful transformer circuits—interpretable subgraphs of neural networks that explain model behavior. By combining fast attribution patching with faithful edge pruning, HAP achieves 46% speedup over baseline circuit discovery methods while maintaining or exceeding their faithfulness. This methodological contribution advances mechanistic interpretability by making circuit extraction scalable and practical for deeper investigation of transformer internals.

---

## Problem Statement

**Current Challenge in Mechanistic Interpretability:**

Circuit discovery—the task of identifying minimal subgraphs that explain model computations—faces a fundamental computational-fidelity tradeoff:

- **Attribution patching methods** (e.g., expectation propagation, EAP) are fast but produce unfaithful circuits because they rely on simplified approximations during the attribution phase. The circuits they identify may miss important causal connections within the model.
- **Edge pruning methods** (e.g., edge pruning, EP) maintain high faithfulness by performing causal intervention on actual model edges, but are computationally expensive. This limits their applicability to larger models or more complex tasks.

**Why This Matters:**

Mechanistic interpretability seeks to understand how transformers solve problems by decomposing them into interpretable circuits. Understanding these circuits is crucial for:
- Debugging and improving model behavior
- Detecting and mitigating adversarial vulnerabilities
- Identifying mechanistic explanations for emergent capabilities
- Developing more controllable and trustworthy AI systems

However, the computational expense of current methods limits their practical use, especially for tasks beyond well-studied benchmarks like Indirect Object Identification (IOI). A method that balances speed and faithfulness is essential for scaling mechanistic interpretability research.

---

## Core Concepts & Theory

### What Are Transformer Circuits?

A **circuit** is a subgraph of a transformer model that encodes a causal explanation for how the model solves a specific task. Circuits consist of:
- **Nodes:** Individual components including tokens, attention heads, and MLP neurons
- **Edges:** Connections representing information flow between components
- **Task:** A specific input-output mapping the circuit is designed to explain

For example, in the IOI task (where a model must identify which name appeared first), a circuit might include specific attention heads that copy information and MLPs that perform logical operations.

### Attribution Patching (Fast but Unfaithful)

**Attribution patching** estimates the importance of a component by:
1. Computing an attribution score for each component
2. Setting components below a threshold to 0 (ablating them)
3. Comparing model output with and without the ablation

**Problem:** The estimated importance can be misleading because:
- Attribution methods (e.g., gradient-based) use simplifications that don't capture true causal effects
- The order of ablations matters, but attribution methods treat components independently
- Correlations between components can inflate importance scores

This leads to circuits that are fast to discover but may include spurious components or miss critical ones.

### Edge Pruning (Faithful but Expensive)

**Edge pruning** uses causal intervention:
1. Remove individual edges (connections) from the model
2. Measure the effect on model output (e.g., KL divergence, logit difference)
3. Retain edges with significant causal impact
4. Iteratively prune edges with minimal impact

**Advantage:** This captures true causal effects because we're directly intervening on the computational graph.

**Disadvantage:** With N possible edges, exhaustive edge pruning requires O(N) forward passes through the full model, which is prohibitively expensive for large transformers.

### The Hybrid Attribution and Pruning (HAP) Framework

**Key Insight:** Use attribution patching to quickly identify a high-potential subgraph, then apply edge pruning only within that subgraph.

**Algorithm:**
1. **Phase 1 (Fast Attribution):** Use attribution patching to compute importance scores for all components
2. **Phase 2 (Targeted Pruning):** Identify the top-k components based on attribution scores (forming a subgraph)
3. **Phase 3 (Faithful Refinement):** Apply edge pruning *only* on edges within this smaller subgraph
4. **Output:** A faithful circuit that is much smaller than the full model

**Why This Works:**
- Attribution patching, though not perfect, provides good signal for identifying likely-important regions
- Focusing edge pruning on this smaller region dramatically reduces computational cost
- The final circuits maintain faithfulness because edge pruning is performed on the selected subgraph
- High-impact components (e.g., S-inhibition heads in IOI) are preserved despite being computationally complex

---

## Main Ideas & Key Contributions

### 1. **Unified Framework for Circuit Discovery**

The HAP framework unifies two previously separate approaches into a coherent pipeline:
- Leverages attribution's computational efficiency
- Combines it with pruning's faithfulness guarantees
- Demonstrates that hybrid approaches can achieve better tradeoffs than pure strategies

### 2. **Significant Efficiency Gains**

**Performance Improvements:**
- **46% speedup** compared to baseline edge pruning methods
- Reduces the number of model forward passes from O(N) to O(1) for attribution + O(k) for pruning on k-sized subgraph
- Practical for exploratory analysis of model circuits

**Computational Impact:**
- For IOI task on GPT-2 Small: HAP identifies circuits in significantly less wall-clock time
- Enables researchers to discover circuits for more complex tasks and larger models

### 3. **Preservation of Cooperative Components**

HAP successfully identifies and preserves components that work cooperatively:
- **S-inhibition heads:** Complex heads that suppress spurious predictions
- **Logit lens behaviors:** Heads that maintain consistent information across layers
- Components that would be missed or pruned by pure attribution methods alone

**This is critical** because mechanistic interpretability specifically aims to understand how components work *together*, not just their individual importance.

### 4. **Comparable Faithfulness to Baseline Methods**

Despite the efficiency gains, HAP maintains:
- **High faithfulness** measured by KL divergence between full model and circuit outputs
- **Comparable logit difference** (difference in model output with and without the circuit)
- **Similar or better sparsity** (fewer edges than baseline EP while maintaining accuracy)

---

## Methodology & Implementation

### Experimental Setup

**Model:** GPT-2 Small (117M parameters)
- Standard benchmark for circuit discovery research
- Well-understood behavior and established baselines

**Task:** Indirect Object Identification (IOI)
- Model must identify which name appeared first in a prompt
- Example: "Alice and Bob went to the store. Alice gave a gift to..."
- The model must recognize that "Alice" should complete the sentence
- Well-studied mechanistic interpretability benchmark

**Baseline Methods:**
1. **EAP (Expectation Propagation):** Fast attribution patching method
2. **EP (Edge Pruning):** Faithful but expensive baseline
3. **Other attribution methods:** Various importance-scoring techniques

### Evaluation Metrics

**Faithfulness Metrics:**
- **KL Divergence:** Measures probability distribution difference between full model and circuit
  - Lower is better; measures information-theoretic distance
- **Logit Difference:** Direct difference in output logits
  - Directly measures task performance
  - Used in IOI specifically as the main task metric

**Efficiency Metrics:**
- **Computational Time:** Wall-clock time for circuit discovery
- **Number of Forward Passes:** Proxy for computational cost
- **Memory Usage:** [Exact figures unavailable — see full paper]

**Sparsity:** Percentage of model edges retained in final circuit

### Key Results

**Performance Comparison (Exact figures unavailable — see full paper):**

1. **Speed:**
   - HAP achieves 46% speedup over EP baseline
   - Attribution phase is O(1) in number of edges
   - Pruning phase operates on small subgraph

2. **Faithfulness:**
   - HAP circuits maintain high faithfulness measured by KL divergence
   - Logit difference comparable to EP circuits
   - EAP circuits show lower faithfulness due to attribution approximation errors

3. **Circuit Quality:**
   - HAP successfully identifies S-inhibition heads critical to IOI performance
   - Preserves multi-head attention patterns that EAP alone would miss
   - Circuits are interpretable and align with prior mechanistic interpretability findings

4. **Sparsity-Fidelity Tradeoff:**
   - At similar sparsity levels, HAP maintains higher faithfulness than EAP
   - At similar faithfulness levels, HAP circuits are sparser than EP
   - Demonstrates genuine improvement in the efficiency-faithfulness frontier

### Limitations

**Task Scope:**
- Evaluation limited to IOI task on GPT-2 Small
- IOI is a relatively simple and well-understood task
- Generalization to other tasks (e.g., arithmetic, factual recall) not demonstrated

**Model Scale:**
- GPT-2 Small (117M) is relatively small by modern standards
- Unclear how method scales to larger models (GPT-3, GPT-4 scale)
- Computational benefits may diminish or disappear for very large models due to different bottlenecks

**Attribution Dependence:**
- Method inherits limitations of the attribution phase
- If attribution scores are systematically biased, subsequent pruning may miss important regions
- Sensitivity to attribution method choice not fully explored

**Interpretation Standardization:**
- Circuits are task and model-specific; limited guidance on generalizing findings
- How to port circuits discovered for one task to different domains unclear

---

## Practical Applications & Real-World Use Cases

### 1. **AI Safety and Alignment**

**Application:** Understanding and controlling model behavior for safety-critical systems

- **Jailbreak Detection:** Identify circuits responsible for safety failures and design interventions
- **Capability Control:** Disable specific capabilities (e.g., toxic language generation) by interrupting key circuits
- **Alignment Verification:** Confirm that models implement intended behaviors by inspecting circuits

**Example:** If a model exhibits an undesired reasoning pattern, mechanistic analysis via circuits could pinpoint the exact computations and heads responsible, enabling targeted fixes.

### 2. **Model Debugging and Improvement**

**Application:** Diagnose why models fail on specific inputs

- **Error Analysis:** When a model produces wrong outputs, circuits show exactly which computational steps failed
- **Adversarial Robustness:** Understand which circuits are vulnerable to adversarial attacks
- **Bias Mitigation:** Identify circuit components responsible for biased predictions

**Example:** A vision classifier misclassifying certain objects could have its failure traced to specific attention or MLP patterns, enabling targeted retraining.

### 3. **Regulatory Compliance and Transparency**

**Application:** Meet regulatory requirements for explainability (GDPR, AI Act, FDA)

- **GDPR Article 22:** Right to explanation for automated decisions
- **EU AI Act:** High-risk AI systems must be "explainable"
- **FDA Guidelines:** Medical AI systems must show reasoning

**Limitation:** Circuit discovery is currently most practical for smaller models and specific tasks. Scaling to large language models and open-ended tasks remains challenging.

### 4. **Research on Emergent Behaviors**

**Application:** Investigate how complex behaviors emerge from transformer computations

- **In-Context Learning:** Understand how models adapt to new tasks within context
- **Multi-step Reasoning:** Decompose chain-of-thought into interpretable sub-circuits
- **Knowledge Representation:** Identify how models store and retrieve factual knowledge

**Example:** Research on how large language models perform arithmetic could use circuit discovery to identify and isolate the mathematical reasoning components.

### 5. **Model Compression and Distillation**

**Application:** Create smaller, more interpretable models from larger ones

- **Circuit-Based Pruning:** Remove entire circuits that contribute minimally to performance
- **Knowledge Distillation Targets:** Use circuit insights to guide which behaviors to preserve
- **Efficient Deployment:** Create models with explicit, interpretable components for resource-constrained environments

---

## Insights & Implications

### 1. **Efficiency-Fidelity Frontier**

HAP demonstrates that hybrid approaches can achieve better efficiency-fidelity tradeoffs than pure strategies:
- Neither pure attribution (fast but unfaithful) nor pure pruning (faithful but slow) dominates
- Strategic combination of both methods yields Pareto improvements
- This principle may apply beyond circuit discovery to other interpretability problems

**Broader Implication:** Interpretability methods should consider complementary approaches rather than optimizing for a single criterion.

### 2. **Scalability of Mechanistic Interpretability**

Current mechanistic interpretability research is limited to:
- Small models (GPT-2 class, ~100M parameters)
- Simple, well-defined tasks (IOI, arithmetic)

HAP's efficiency gains are meaningful but incremental (46% speedup). **Open question:** What fundamental breakthroughs are needed to scale circuit discovery to billion-parameter models and complex, open-ended tasks?

**Possibilities:**
- Hierarchical circuit representations (circuits of circuits)
- Attention-based circuit discovery (focusing on salient regions)
- Learned pruning policies (training a model to propose circuits)
- Compressed representations of circuits for faster evaluation

### 3. **Cooperative Component Discovery**

HAP's success at preserving cooperative components (S-inhibition heads in IOI) suggests:
- Attribution patching alone can miss complex multi-head interactions
- Faithfulness metrics are crucial for validating mechanistic explanations
- The true causal graph may be more complex than single-component attributions suggest

**Research Direction:** How do circuits evolve as models get larger? Do cooperative patterns become more or less important?

### 4. **Limitations of Current Evaluation**

The paper's evaluation on a single task (IOI) raises methodological questions:
- **Task Generalization:** Do circuits discovered for IOI provide insights for other tasks?
- **Circuit Compositionality:** Can circuits be combined or reused across tasks?
- **Benchmark Limitations:** IOI is well-studied but may not be representative of model behavior on harder tasks

**Open Debate:** Should mechanistic interpretability focus on understanding toy tasks deeply (current approach) or sample-diverse real-world tasks shallowly?

### 5. **Connection to Graph Machine Learning**

The paper was accepted to NeurIPS 2025 Workshop on Graph Machine Learning, suggesting:
- Circuit discovery is fundamentally a graph problem (subgraph extraction)
- Graph neural networks and graph algorithms may accelerate circuit discovery
- Methods from graph neural networks (e.g., graph pooling, attention) could improve efficiency

**Potential Synergy:** Graph representation learning could enable learned pruning policies rather than hand-crafted heuristics.

---

## Code & Resources

### Official Implementations
- **ArXiv:** https://arxiv.org/abs/2510.03282
- **ArXiv HTML Version:** https://arxiv.org/html/2510.03282v1
- **ArXiv PDF:** https://arxiv.org/pdf/2510.03282

**Note:** Check the paper for GitHub repository links or supplementary materials. Algoverse AI Research may provide code at their website (contact: ryan@algoverseairesearch.org).

### Dependencies & Requirements

**Python Libraries:**
- PyTorch (for transformer models)
- NumPy/SciPy (for numerical computations)
- [Exact library versions unavailable — see full paper]

**Computational Requirements:**
- GPU recommended (CUDA-capable NVIDIA GPU preferred)
- Minimum GPU Memory: [Figures unavailable — see full paper]
- Approximate Runtime: [Figures unavailable — see full paper]
- Disk Space: [Figures unavailable — see full paper]

### Quick Start

The paper does not provide a publicly available implementation or quick-start guide in the ArXiv abstract. For replication:
1. Obtain the paper code (contact authors or check GitHub)
2. Install dependencies as specified in the paper
3. Download or train a GPT-2 Small model (e.g., from Hugging Face)
4. Run HAP framework on IOI or other benchmark tasks

### Interactive Visualizations & Demos

No interactive visualizations or web demos are mentioned in the abstract. Circuit visualizations typically use:
- Graph layouts showing attention head connections
- Heatmaps of edge importance scores
- Token-by-token attribution traces

---

## Related Work & Context

### Position in the Mechanistic Interpretability Landscape

**Mechanistic Interpretability** is the study of how neural networks compute by decomposing them into interpretable components and their interactions. Key related work includes:

1. **Circuit Discovery Methods:**
   - **Edge Pruning (EP):** Original faithful circuit discovery method (basis for comparison)
   - **Expectation Propagation (EAP):** Fast attribution-based circuit discovery
   - **Causal Tracing:** Early work on localizing model computations
   - **Activation Patching:** General framework for causal intervention

2. **Attribution Methods:**
   - **Gradient-Based:** Saliency maps, integrated gradients (fast, approximate)
   - **Perturbation-Based:** LIME, SHAP (faithful, computationally expensive)
   - **Attention-Based:** Attention flow as proxy for information flow (controversial)

3. **Related Tasks:**
   - **SAE (Sparse Autoencoders):** Extract interpretable features from latent representations
   - **Causal Intervention Studies:** Understand which neurons are necessary for specific behaviors
   - **Superposition Hypothesis:** Multiple concepts encoded in single neurons

### How HAP Builds On and Differs From Prior Work

**Builds On:**
- Attribution patching paradigm (fast but approximate importance estimation)
- Edge pruning methodology (faithful causal intervention)
- IOI benchmark (well-characterized test case)

**Novel Contributions:**
- First hybrid approach combining both attribution and pruning
- Systematic comparison showing efficiency-fidelity tradeoff
- Preservation of cooperative multi-component patterns
- 46% speedup while maintaining faithfulness

**Differs From:**
- Pure attribution methods: achieves better faithfulness
- Pure pruning methods: achieves better efficiency
- Other interpretability work: focuses specifically on causal circuit extraction rather than post-hoc explanations

### Connection to Broader xAI Research

**Mechanistic interpretability vs. Other xAI Approaches:**

| Aspect | Mechanistic Interpretability | Feature Attribution | Concept-Based Explanations |
|--------|------------------------------|-------------------|---------------------------|
| **Focus** | Internal circuits and information flow | Feature importance | High-level semantic concepts |
| **Granularity** | Individual neurons, attention heads | Input features | User-defined concepts |
| **Faithfulness** | High (causal intervention) | Medium (approximation) | Variable (concept quality dependent) |
| **Scalability** | Poor (computationally expensive) | Good (fast) | Medium (concept discovery needed) |
| **Interpretability** | High (for researchers) | High (for users) | High (for domain experts) |

HAP improves mechanistic interpretability's scalability without sacrificing faithfulness, narrowing the gap with faster approaches.

### Future Research Directions

**Short-term Questions:**
1. How does HAP generalize to other tasks beyond IOI?
2. Can the method scale to larger models (GPT-3 scale)?
3. Are there more efficient subgraph selection heuristics?

**Long-term Questions:**
1. Can circuits be discovered hierarchically (multi-level abstractions)?
2. Do circuits transfer across models of different sizes or architectures?
3. How do circuits evolve during model training?
4. Can circuit discovery be used for real-time model steering?

**Integration with Other Research:**
- Connection to mechanistic alignment: circuits as a tool for ensuring aligned behavior
- Integration with adversarial robustness: understanding and defending circuit vulnerabilities
- Application to foundation models: scaling to vision transformers, large language models

---

## Discussion: Open Questions and Limitations

### Why Model Scale Matters

While HAP is 46% faster than baseline EP, absolute runtime for GPT-2 Small circuit discovery is not provided. For larger models:
- Scaling to GPT-2 Medium/Large: How much faster is HAP?
- Scaling to GPT-3 (175B): Is HAP still practical?
- Key bottleneck: Even O(1) attribution may dominate for billion-parameter models

### Generalization Beyond IOI

IOI is celebrated as a "Rosetta Stone" for mechanistic interpretability, but:
- Is IOI representative of tasks transformers solve in practice?
- Do circuits for IOI differ fundamentally from circuits for arithmetic, factual recall, or reasoning?
- **Open Question:** Should the field prioritize depth (understanding simple tasks completely) or breadth (sampling diverse tasks)?

### The Attribution Approximation

HAP's initial phase relies on attribution patching, which is known to have:
- **False positives:** Components marked important that aren't causally critical
- **False negatives:** Components marked unimportant that are causally important
- **Interaction effects:** Correlations can inflate importance

**Sensitivity Analysis Needed:**
- How much does poor initial attribution affect final circuit quality?
- Is there a confidence threshold below which the subsequent pruning step fails?

### Path to Deployment

For real-world use (e.g., debugging models in production):
- **Interpretability Gap:** Circuits show *how* a model computes, but domain experts need to understand *why* that computation is correct or incorrect
- **Generalization:** A circuit discovered for one input distribution may not transfer to out-of-distribution inputs
- **Latency:** Even with HAP's speedup, is circuit discovery fast enough for real-time debugging?

---

## Conclusion

"Discovering Transformer Circuits via a Hybrid Attribution and Pruning Framework" makes a solid methodological contribution to mechanistic interpretability by solving a practical efficiency problem. The 46% speedup over baseline methods, achieved while preserving circuit faithfulness, is meaningful for the research community and opens the door to more extensive circuit discovery experiments.

**Key Takeaways:**
1. **Hybrid approaches can achieve better tradeoffs** than pure strategies in interpretability research
2. **Scaling mechanistic interpretability** from toy tasks to real-world applications remains an open challenge
3. **Circuit discovery is complementary** to other xAI methods (feature attribution, concept-based explanations) and together form a richer picture of model behavior
4. **Cooperative components matter:** Fidelity metrics are essential for capturing interactions between model parts

**For Practitioners:**
- If you need to discover circuits for understanding specific model behaviors, HAP offers a practical speedup
- Consider combining HAP with other interpretability methods for a more complete picture
- Be mindful of task and model size limitations when applying this work

**For Researchers:**
- The efficiency-fidelity frontier deserves more attention across interpretability subfields
- Scaling mechanistic interpretability to larger models and real-world tasks is a high-impact research direction
- Graph learning and circuit discovery have natural synergies worth exploring

---

## References

Gu, H., Nair, V., Kumar, A. A., Sharma, J., & Lagasse, R. (2025). Discovering Transformer Circuits via a Hybrid Attribution and Pruning Framework. *arXiv preprint arXiv:2510.03282*. Accepted to NeurIPS 2025 Workshop on Mechanistic Interpretability and NeurIPS 2025 Workshop on New Perspectives in Graph Machine Learning.

**Citation:**
```bibtex
@article{gu2025discovering,
  title={Discovering Transformer Circuits via a Hybrid Attribution and Pruning Framework},
  author={Gu, Hao and Nair, Vibhas and Kumar, Amrithaa Ashok and Sharma, Jayvart and Lagasse, Ryan},
  journal={arXiv preprint arXiv:2510.03282},
  year={2025}
}
```

---

## Related Papers to Explore

- [Edge Pruning for Circuit Discovery](https://arxiv.org/abs/2406.16778)
- [Hierarchical Sparse Circuit Extraction](https://arxiv.org/abs/2601.12879)
- [Efficient Automated Circuit Discovery via Contextual Decomposition](https://arxiv.org/abs/2407.00886)
- [Causal Tracing for Understanding Model Decisions](https://arxiv.org/abs/2202.05629)
- [Mechanistic Interpretability for Neural Networks: Circuits, Sparse Features and Symbolic Reasoning](https://arxiv.org/abs/2607.07316)
- [CircuitKIT: Circuit Discovery, Evaluation, and Application Toolkit](https://arxiv.org/abs/2607.19317)
- [RACE: Scalable Statistical Estimation of Functional Consistency in LLM Neurons](https://arxiv.org/abs/2608.24758)
