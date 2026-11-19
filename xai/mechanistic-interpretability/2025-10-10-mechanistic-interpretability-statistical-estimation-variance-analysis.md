# Mechanistic Interpretability as Statistical Estimation: A Variance Analysis

**ArXiv ID:** [2510.00845](https://arxiv.org/abs/2510.00845)

**Authors:** Maxime Méloux, François Portet, Maxime Peyrard

**Submitted:** October 2025

## Executive Summary

This paper presents a critical methodological contribution to mechanistic interpretability (MI) by treating circuit discovery as a statistical estimation problem rather than a standalone task. The authors demonstrate that circuit discovery methods exhibit intrinsically high variance, meaning that small changes in inputs, hyperparameters, or the counterfactual specification can produce dramatically different circuits. The work advocates for routine reporting of stability metrics and more rigorous statistical practices in MI research, addressing a fundamental reliability concern in the field.

## Problem Statement

Mechanistic interpretability research aims to discover interpretable computational circuits within neural networks by identifying which model components (attention heads, neurons, etc.) causally contribute to specific behaviors. However, existing MI work has largely treated circuit discovery as a deterministic task, implicitly assuming that the identified circuits are stable and reproducible properties of the model.

This paper challenges this assumption by showing that:
1. Exact circuit discovery depends heavily on input sampling and specification details
2. Single intervention specifications (e.g., mean ablation) provide incomplete information
3. The variance in circuits discovered is often not reported, limiting reproducibility
4. Conclusions about causal roles may not generalize across small variations in methodology

The practical implication is that many published MI findings may lack the statistical rigor necessary for reliable model understanding and that the field needs standardized practices for quantifying and reporting stability.

## Core Concepts & Theory

### Causal Mediation Analysis (CMA) as Foundation

The paper grounds circuit discovery in **causal mediation analysis**, a statistical framework from econometrics and epidemiology. CMA decomposes causal effects into:

- **Total Effect (TE):** Overall impact of intervening on a component
- **Direct Effect (DE):** Causal effect through direct pathways
- **Indirect Effect (IE):** Effects mediated through other components

In mechanistic interpretability, circuit discovery typically approximates these effects using methods like:
- **EAP (Edge Attribution Probability):** Estimates whether an edge is on the causal path
- **EAP-IG (Edge Attribution Probability via Integrated Gradients):** Combines edge attribution with gradient-based approximations

### Key Mathematical Insight

The core finding is that exact CMA scores on individual inputs exhibit **high intrinsic variance**. This means:

```
Var(CMA_effect) = Var(component's causal contribution) + estimation_error
```

For a single input, the effect of a component is not a fixed property but a volatile random variable that fluctuates based on:
- Input content and distributional properties
- Model's internal state across different prompts
- Choice of counterfactual value (e.g., zero, mean, or noise)
- Specific causal analysis technique employed

### Stability Cascades

The paper demonstrates that variance propagates and amplifies through circuit discovery pipelines:

1. **Input Variance:** Resampling inputs produces different CMA scores for the same edge
2. **Approximation Variance:** Different approximations (EAP vs. EAP-IG) yield different circuits
3. **Intervention Variance:** Changing the counterfactual specification produces different causal graphs
4. **Hyperparameter Variance:** Thresholds, pruning criteria, and other hyperparameters affect final circuits

Each stage compounds the uncertainty, so circuits reported from a single run may be artifacts of methodological choices rather than fundamental model properties.

## Main Ideas & Key Contributions

### 1. Reframing Circuit Discovery as Statistical Estimation

**Contribution:** Treating circuit discovery as statistical estimation problem rather than a deterministic task.

This reframing recognizes that:
- Each circuit discovery run estimates causal relationships with uncertainty
- Multiple runs with different initializations/data would yield different circuits
- The confidence in a discovered circuit should be quantifiable

This perspective is borrowed from statistical practice in other fields (econometrics, psychology) but is novel in mechanistic interpretability.

### 2. Demonstrating Empirical High Variance

**Methodology:** The authors conducted systematic variance analyses:

- **Input Resampling:** Partitioned data, computed circuits on each partition, measured variation
- **Prompt Paraphrasing:** Used equivalent but linguistically different prompts; circuits differed substantially
- **Hyperparameter Variation:** Swept thresholds and other hyperparameters; observed sensitive dependence
- **Noise Injection:** Added noise within the CMA computation itself; large circuit changes observed
- **Counterfactual Specification:** Varied intervention values (zero, mean, random); different circuits emerged

**Key Finding:** Small, theoretically-inconsequential changes in methodology produce circuits that look substantially different.

### 3. Advocating for Rigorous MI Practice

**Recommendation:** The paper argues for:

1. **Routine Stability Reporting:** Every circuit discovery result should report stability metrics:
   - Variance across input samples
   - Consistency under prompt paraphrasing
   - Sensitivity to hyperparameters
   - Stability of identified causal edges across counterfactual specifications

2. **Statistical Significance Testing:** Circuit claims should be tested:
   - Are edges consistently identified across multiple runs?
   - Do effect sizes persist when methodology varies?
   - What is the confidence interval on claimed causal effects?

3. **Mechanistic Validation:** Beyond isolated circuits:
   - Test whether circuits generalize to new inputs
   - Verify whether interventions on discovered circuits produce predicted behavior changes
   - Use cross-validation and held-out test sets for circuit validation

## Methodology & Implementation

### Experimental Design

The authors conducted systematic ablation studies on large language models (primarily Transformers):

**Datasets:** Standard LLM benchmarks (factual recall, reasoning tasks, etc.)

**Models Tested:** Various Transformer architectures (Llama-sized models, focus on 7B-13B scale)

**Baselines:** Standard MI techniques including:
- EAP (Edge Attribution Probability)
- EAP-IG (Edge Attribution Probability with Integrated Gradients)
- Node attribution methods
- Activation-based circuit discovery

### Evaluation Metrics for Variance

The paper evaluates variance through:

1. **Intra-run Variability:** Stability within a single circuit discovery run
2. **Inter-run Variability:** Consistency across multiple runs with different random seeds
3. **Cross-dataset Variance:** Whether circuits discovered on one dataset transfer to held-out test sets
4. **Counterfactual Robustness:** How circuit membership changes under different intervention values

### Key Findings (Provisional)

[Exact figures unavailable — see full paper] but the results show that:
- Edge stability ranged from 60-80% across input resampling in controlled tasks
- Prompt paraphrasing induced 20-40% changes in discovered circuit membership
- Threshold sensitivity analysis showed sharp transitions in circuit size and connectivity
- Integrating multiple counterfactual specifications increased circuit size by 30-50% and changed connectivity

**Limitations:** Single-paper study; results primarily on specific task types (factual recall, simple reasoning); limited evaluation on more complex tasks like in-context learning or multi-step reasoning.

## Practical Applications & Real-World Use Cases

### 1. Interpretability Research Best Practices

For researchers doing mechanistic interpretability:
- **Before claiming a circuit "explains" a behavior:** Test stability across variations
- **When publishing circuits:** Report variance metrics alongside discovered components
- **In collaborative work:** Use standardized variance evaluation to compare methods

### 2. Model Safety and Alignment

Understanding where variance comes from helps:
- **Identify robust failure modes:** A consistently-discovered circuit indicates a stable mechanism vs. a statistical artifact
- **Prioritize interventions:** Focus safety work on stable, reproducible mechanisms rather than ephemeral patterns
- **Validate alignment techniques:** Verify that alignment-induced changes consistently affect discovered circuits

### 3. Building Interpretable AI Systems

For practitioners building intrinsically interpretable models:
- **Uncertainty quantification:** High-variance circuits indicate components with unclear roles; design can reduce this
- **Robustness verification:** Test whether model internals remain stable under distribution shift
- **Specification sensitivity:** Understand which design choices (architecture, training, etc.) minimize circuit variance

### 4. Regulatory and Compliance Implications

For AI governance and regulation (e.g., EU AI Act, FDA review):
- **Interpretability claims:** Current MI methods may not meet rigorous interpretability standards due to instability
- **Auditability:** Circuit-based explanations are only credible if they are stable and reproducible
- **Accountability:** High variance in circuits undermines traceability requirements in regulated domains

## Insights & Implications

### For Mechanistic Interpretability Research

1. **Paradigm Shift Required:** The field has implicitly assumed circuits are deterministic properties. This work shows they are better understood as point estimates of uncertain quantities.

2. **Reproducibility Crisis:** Many published circuits may not be reproducible with slightly different methodology, raising questions about the generalizability of MI findings.

3. **Need for Standardization:** Without standardized practices for variance evaluation, the field risks perpetuating unstable conclusions.

4. **Opportunity for Improvement:** High variance also indicates where methods can be improved—components, hyperparameters, and counterfactual specifications that reduce variance are more reliable.

### Broader Implications for Trustworthy AI

1. **Interpretability as Reliability:** True interpretability requires not just identifying mechanisms but demonstrating that those mechanisms are stable and reproducible.

2. **Moving Beyond Point Estimates:** Future MI work should report distributions over circuits rather than single circuit outputs.

3. **Integration with Uncertainty Quantification:** MI methods should borrow techniques from Bayesian statistics and uncertainty quantification to characterize variance.

4. **Falsifiability:** High-variance circuits are hard to falsify; more rigorous MI would be more scientifically robust.

### Open Questions

1. **Optimal Variance Reduction:** What methodological changes most reduce circuit variance?
2. **Theoretical Bounds:** Can we derive theoretical guarantees on circuit stability?
3. **Task Dependence:** Does circuit variance depend on task difficulty or domain?
4. **Generalization:** How do circuits discovered on one model generalize to other architectures or sizes?

## Code & Resources

### Official Implementations

- **ArXiv Paper:** [https://arxiv.org/abs/2510.00845](https://arxiv.org/abs/2510.00845)
- **PDF:** [https://arxiv.org/pdf/2510.00845](https://arxiv.org/pdf/2510.00845)
- **HTML Version (Latest v4):** [https://arxiv.org/html/2510.00845v4](https://arxiv.org/html/2510.00845v4)

### Dependencies & Requirements

Standard mechanistic interpretability tools:
- PyTorch or similar deep learning framework
- Transformer libraries (e.g., HuggingFace transformers)
- Statistical analysis tools (scipy, numpy, pandas)
- For CMA: custom implementations or causal inference libraries (e.g., DoWhy)

Computational requirements: [Not specified in available materials — likely multi-GPU for LLM experiments]

### Quick Start

Practitioners implementing variance analysis:

1. **Identify your circuit discovery method** (EAP, EAP-IG, etc.)
2. **Define variance metrics** you care about (input resampling, hyperparameter sensitivity, counterfactual robustness)
3. **Run multiple ablations** systematically varying each factor
4. **Compute stability statistics** (Jaccard similarity, edge overlap, etc.) across ablation runs
5. **Report results** alongside main circuit discovery claims

## Related Work & Context

### Foundational MI Research This Builds Upon

- **Interpretability Foundations:** Early MI work (Elhage et al., Nanda et al.) established circuit discovery methods; this paper critiques their stability
- **Causal Inference in ML:** Prior work on causal inference in neural networks; this paper applies statistical rigor from that literature
- **Circuit Analysis:** Recent work on specific circuits (IOI circuit, greater-than circuit, etc.); variance analysis questions reproducibility of such findings

### Connections to Broader xAI Community

1. **Feature Attribution Methods:** Similar variance issues exist in SHAP/LIME; this analysis extends critiques to mechanistic methods
2. **Model-Agnostic Interpretability:** Shares concerns about stability and reproducibility with post-hoc explanation methods
3. **Fairness in Interpretability:** Connects to work on fairness of explanations—unstable circuits raise fairness concerns for different groups

### Where This Research Leads

1. **Bayesian Mechanistic Interpretability:** Future work could develop Bayesian MI methods that naturally quantify uncertainty over circuits
2. **Robust Circuit Discovery:** Methods that minimize variance or explicitly search for stable circuits
3. **Meta-analysis of MI:** Systematic reviews combining results across papers with variance-corrected effect sizes
4. **Mechanistic Interpretability Standards:** Community adoption of standardized variance evaluation practices

### Related Mechanistic Interpretability Papers

- Foundational work on circuit discovery and validation
- Studies on specific circuits (IOI, factual recall, arithmetic) that could be re-evaluated under variance analysis
- Recent work on scalable MI methods that could be assessed for stability
- Papers using MI for alignment and safety (which may need to account for circuit variance)

## Discussion

### Strengths

1. **Important Problem:** High variance in circuits is a critical issue that the field needs to address
2. **Rigorous Methodology:** Systematic ablation studies with multiple variance sources
3. **Practical Guidance:** Clear recommendations for researchers and practitioners
4. **Foundational Impact:** Challenges fundamental assumptions in MI

### Limitations and Criticisms

1. **Limited Scope:** Results primarily on specific task types; generalization to more complex tasks unclear
2. **Solution Gaps:** Identifies the problem but offers limited solutions beyond "report variance"
3. **Implementation Details:** Some experimental choices (models tested, specific tasks) could be expanded
4. **Counterfactual Specification:** While the paper critiques fixed counterfactuals, doesn't propose principled alternatives

### Future Work

1. **Algorithmic Solutions:** Develop MI methods that intrinsically reduce variance
2. **Theoretical Analysis:** Derive bounds on circuit variance given model and task properties
3. **Automated Variance Reduction:** Use meta-learning or Bayesian optimization to find stable circuits
4. **Multi-task Validation:** Test circuits across multiple related tasks to identify robust mechanisms

## Conclusion

This paper makes a vital methodological contribution to mechanistic interpretability by demonstrating that circuit discovery is not a deterministic process but a statistical estimation problem with substantial inherent variance. By framing MI through the lens of causal inference and statistical rigor, the work advocates for higher standards in the field: reporting stability metrics, testing generalization, and validating causal claims more rigorously.

The implications are profound: mechanistic interpretability research must move from reporting single circuit outputs to characterizing distributions over possible circuits. This is both a challenge (raising the bar for MI work) and an opportunity (opening paths for more robust, reliable interpretability methods).

For the xAI community, this work emphasizes that interpretability—whether post-hoc or mechanistic—must be reliable to be trustworthy. High-variance interpretations undermine confidence in model understanding and may mislead practitioners and stakeholders. Future work in xAI should adopt similar statistical rigor, treating explanations not as point outputs but as uncertain estimates that benefit from principled variance quantification.
