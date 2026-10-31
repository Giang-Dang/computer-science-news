# Causal Integrated Gradients: Scalable Feature Attribution Along Causal Paths

## Executive Summary

This paper introduces Causal Integrated Gradients (CIG) and Causal Expected Gradients (CEG), novel methods that extend the popular integrated gradients attribution technique to leverage prior causal structure among input features. By routing attribution computation along causal pathways rather than treating features independently, CIG achieves computational efficiency comparable to standard integrated gradients while providing attributions that better match ground-truth causal effects—particularly valuable in domains like genomics where causal relationships are partially known.

**ArXiv ID:** [2610.22126](https://arxiv.org/abs/2610.22126)

**Authors:** Joran Michiels, Anis Ismail, Maarten De Vos, Alejandro Sifrim

**Submission Date:** October 2026

---

## Problem Statement

### Current Challenges in Feature Attribution

Traditional feature attribution methods (gradient-based and model-agnostic) treat input features as independent when calculating their importance to model predictions. This assumption is problematic in domains where causal relationships among features are known or can be estimated:

1. **Confounding and Causality Confusion**: Standard integrated gradients and SHAP may assign high attribution to downstream variables while ignoring their upstream causal drivers. For example, in genomics, downstream expression markers receive credit that should go to their upstream transcription factors.

2. **Computational Efficiency vs. Causal Accuracy Trade-off**: Causal Shapley values provide theoretically sound causal attribution but are computationally expensive, scaling poorly with feature dimension.

3. **Unstructured Feature Spaces**: Without incorporating domain knowledge about feature relationships, attribution methods cannot distinguish between:
   - **Direct causal effects**: A feature's direct influence on the output
   - **Mediated causal effects**: Effects routed through downstream features
   - **Confounded associations**: Spurious correlations that lack causal meaning

4. **Regulatory and Compliance Gaps**: In regulated industries (healthcare, finance), explainability must be causally valid, not merely associational. Current methods lack formal grounding in causal inference.

---

## Core Concepts & Theory

### Background: Integrated Gradients

**Integrated Gradients (IG)** is a popular gradient-based attribution method that addresses some limitations of raw gradients:

- **Definition**: For a model $f$ and input $\mathbf{x}$, integrated gradients attribute importance by integrating the gradient along a straight-line path from a baseline $\mathbf{x'}$ to the input:
  $$\text{IG}_i(\mathbf{x}) = (x_i - x'_i) \cdot \int_0^1 \frac{\partial f(\mathbf{x'} + t(\mathbf{x} - \mathbf{x'}))}{\partial x_i} dt$$

- **Desirable Properties**:
  - *Completeness*: Attributions sum to the difference between output and baseline
  - *Sensitivity*: Non-zero attribution for features that causally affect output
  - *Implementation Invariance*: Depends only on function behavior, not internal architecture

### Causal Graph Formalism

A **causal graph** (directed acyclic graph, DAG) $G = (V, E)$ represents causal relationships among features:
- Nodes $V$ represent features/variables
- Directed edges $(i \to j)$ indicate that feature $i$ causally influences feature $j$
- No cycles (acyclicity assumption)

**Key causal concepts used in CIG**:
- **Parents** of node $i$: $\text{pa}(i)$ = direct causes of feature $i$
- **Descendants** of node $i$: $\text{de}(i)$ = variables causally downstream of $i$
- **Paths**: Sequences of edges representing causal chains
- **Intervention**: Pearl's *do-calculus* $\text{do}(X=x)$ represents an external manipulation

### Introduction to Causal Integrated Gradients (CIG)

**Core Innovation**: Instead of integrating along a straight path in the original feature space, CIG integrates along a path that respects the causal structure:

1. **Path Construction**: The integration path is constructed by:
   - Setting features to their baseline values initially: $\mathbf{x'} = (x'_1, \ldots, x'_n)$
   - Gradually transitioning to the observed values: $\mathbf{x} = (x_1, \ldots, x_n)$
   - **Respecting causal order**: Features are transitioned only after all their causal parents have been transitioned

2. **Attribution Decomposition**: For each feature $i$, CIG decomposes attribution into:
   - **Direct Effect (DE)**: The feature's direct influence on the output (when it changes while descendants remain at baseline)
   - **Mediated Effects (ME)**: Influence transmitted through descendant features (when descendants change in response to feature $i$ changing)

   $$\text{CIG}_i = \text{DE}_i + \sum_{j \in \text{de}(i)} \text{ME}_{i \to j}$$

3. **Mathematical Formulation**:
   The causal integration path $\mathbf{p}(t)$ over $t \in [0, 1]$ is constructed such that:
   - Feature $i$ at step $t$ is: $p_i(t) = x'_i + t \cdot (x_i - x'_i)$ if all parents have been fully transitioned, else $p_i(t) = x'_i$
   - Causal order ensures no "jumps" that violate the causal structure

4. **Gradient Computation**: Along this causally-respecting path:
   $$\text{CIG}_i(\mathbf{x}) = (x_i - x'_i) \cdot \int_0^1 \frac{\partial f(\mathbf{p}(t))}{\partial x_i} dt$$

### Causal Expected Gradients (CEG)

An extension that approximates CIG by sampling multiple random paths through the causal structure, reducing variance and improving stability:

- Averages gradients over multiple causally-valid paths (not just straight-line paths)
- Provides better finite-sample estimates
- Trade-off: Slightly higher computational cost than CIG but still efficient

### Theoretical Guarantees

Under specified conditions on the causal graph:

1. **Completeness**: CIG attributions sum to the model's output difference (relative to baseline)
2. **Axiomatic Soundness**: CIG satisfies variants of Shapley axioms adapted for causal settings
3. **Causal Validity**: When the causal graph is correct and features are causally sufficient (no unmeasured confounders), CIG attributions correspond to Pearl's causal effects
4. **Efficiency**: Computational complexity is $O(n \cdot p)$ where $n$ = number of integration steps and $p$ = number of features, matching standard integrated gradients

---

## Main Ideas & Key Contributions

### 1. Novel Integration Path Design

**Contribution**: Reformulating integrated gradients to traverse feature space in causal order.

- **Why it Matters**: Standard IG treats all features symmetrically, but causal domains have asymmetry (causes → effects). By respecting this structure, CIG naturally separates causal influences from spurious associations.
- **Intuition**: Imagine explaining a prediction in biology. If you adjust a transcription factor (upstream) and measure its effect on downstream genes, then adjust the downstream genes directly—these are different causal scenarios. CIG handles this correctly; standard IG conflates them.

### 2. Direct Effect vs. Mediated Effect Decomposition

**Contribution**: Decomposing each feature's attribution into how much it directly influences the output vs. how much it works indirectly through downstream features.

- **Practical Value**: In drug discovery, for example, you want to know: "Does this target protein directly affect disease markers, or does it work through secondary pathways?" CIG answers this.
- **Design Insight**: This decomposition naturally emerges from causally-ordered integration—not from post-hoc analysis.

### 3. Computational Efficiency

**Contribution**: Maintaining the scalability of integrated gradients while incorporating causal structure.

- **vs. Causal Shapley**: Achieves similar causal validity but at a fraction of computational cost. CIG requires $O(n \cdot p)$ gradient computations; causal Shapley requires exponential-in-$p$ coalition evaluations.
- **Scalability**: Tested on datasets with thousands of features, making it practical for high-dimensional domains like genomics.

### 4. Axiomatic Framework

**Contribution**: Formalizing CIG within a causal variant of the Shapley axioms (completeness, causality, symmetry).

- **Rigor**: Unlike many heuristic attribution methods, CIG has formal mathematical guarantees under stated assumptions.
- **Limitations Acknowledged**: Axioms assume the causal graph is correct and causally sufficient (no hidden confounders).

---

## Methodology & Implementation

### Experimental Setup

#### Datasets and Models

1. **Synthetic Causal Benchmark**:
   - **Purpose**: Ground-truth evaluation where true causal effects are known
   - **Setup**: Generate data from a known causal model (DAG structure + noise)
   - **Model**: Train simple neural network (2-3 hidden layers) to predict an outcome from synthetic features
   - **Causal Structure**: Explicitly encoded, allowing validation of CIG's causal recovery

2. **Gene Regulatory Network (Dyngen Simulated Data)**:
   - **Purpose**: Semi-realistic biological domain with approximately-known causal structure
   - **Setup**: Simulate single-cell transcriptomics data with known regulatory interactions
   - **Model**: DeepSHAP-compatible neural network for gene expression prediction
   - **Task**: Identify transcription factors driving cell-state transitions
   - **Metrics**: Precision and recall at recovering known regulatory targets

3. **Real Interferon-β Response Data**:
   - **Dataset**: Human immune cells stimulated with interferon-β
   - **Features**: Gene expression (thousands of genes)
   - **Causal Graph**: Approximate (estimated from literature and co-expression patterns)
   - **Task**: Discover transcription factors driving interferon response
   - **Validation**: Compare with known biological knowledge

#### Baseline Methods for Comparison

- **Standard Integrated Gradients (IG)**: Ignores causal structure (upper bound on speedup)
- **DeepSHAP**: Model-agnostic but computationally expensive
- **Conditional SHAP**: Attempts to handle feature dependence but not formally causal
- **Causal Shapley Values**: Causal ground truth (slow, used as accuracy reference)

### Evaluation Metrics for Interpretability

1. **Causal Recovery Accuracy** (Synthetic):
   - Compare CIG attributions to ground-truth causal effects computed via Pearl's do-calculus
   - **Metric**: Mean Absolute Error (MAE) between CIG and ground-truth
   - **Results**: [Exact figures unavailable — see full paper] but reported as "matching causal Shapley accuracy"

2. **Biological Precision** (Dyngen & Real Data):
   - **Metric**: Precision@K — percentage of top-K attributed genes that are known regulatory targets
   - **Results**: [Exact figures unavailable — see full paper]
   - **Performance**: CIG outperformed DeepSHAP and IG across all cell-state transitions

3. **Computational Cost**:
   - **Metric**: Wallclock time for attribution computation
   - **Results** (estimated): CIG achieves results in minutes where causal Shapley took hours; 10-100× speedup depending on feature dimensionality

4. **Path Stability** (proposed novelty metric):
   - **Metric**: Variance of attributions across multiple integration paths
   - **Results**: [Exact figures unavailable — see full paper]
   - **Finding**: CEG (with path sampling) more stable than single-path CIG

### Limitations Discussed

1. **Causal Graph Specification**:
   - Assumes the causal graph is known or estimated with high accuracy
   - Performance degrades with graph misspecification
   - In real data (IFN-β), only approximate causal structure available; results less clean than synthetic

2. **Causal Sufficiency Assumption**:
   - Requires no unmeasured confounders
   - Biological networks often have confounding; CIG cannot recover true causal effects in such settings
   - Methods like instrumental variables would be needed for deeper analysis

3. **Baseline Selection**:
   - Like all integrated gradients variants, results depend on baseline choice
   - Different baselines (e.g., mean vs. zero) can yield different attributions
   - No principled rule for baseline selection in causal setting

4. **Feature Measurement Error**:
   - Assumes features are measured without error
   - Real data (e.g., RNA-seq) has measurement noise; not explicitly handled

---

## Practical Applications & Real-World Use Cases

### 1. Genomics & Drug Discovery

**Use Case**: Identifying drug targets and understanding mechanism of action (MoA)

- **Challenge**: High-dimensional transcriptomics (10,000+ genes); need to prioritize which genes actually drive phenotype vs. which are passengers
- **How CIG Helps**:
  - Attribute cell state changes to upstream transcription factors (causes) rather than downstream effectors (effects)
  - Directly vs. mediated effects reveal whether a gene acts upstream (master regulator) or downstream (executor)
  - Computational efficiency allows genome-wide analysis
- **Regulatory Implication**: FDA's 21 CFR Part 11 requires interpretability of biomarker assays; CIG provides causally grounded explanations

### 2. Healthcare & Clinical Diagnosis

**Use Case**: Understanding disease biomarkers and treatment response

- **Challenge**: Distinguish biomarkers (which indicate disease) from causative factors (which drive disease)
- **How CIG Helps**:
  - Causal structure (e.g., genetics → protein expression → disease phenotype) is encoded
  - CIG correctly attributes disease to upstream genetic variants, not just observable biomarkers
  - Supports precision medicine decisions
- **Regulatory Implication**: GDPR Article 22 (automated decision-making) requires interpretability; causal explanations are more trustworthy than correlational

### 3. Financial Risk Assessment

**Use Case**: Credit scoring, fraud detection, market risk modeling

- **Challenge**: Distinguish true risk drivers from correlated confounders
- **How CIG Helps**:
  - Encode known economic causal relationships (GDP → employment → credit risk)
  - Separate direct effects of policies on risk from indirect effects through market variables
  - Improves regulatory compliance under FCRA and AI Act transparency requirements
- **Example**: A credit model may heavily weight a customer's employment status. CIG distinguishes whether employment *causes* loan default (true risk) or is merely correlated with unobserved factors (debt levels, family situation)

### 4. Natural Language Processing (Future Direction)

**Use Case**: Syntax and semantics in LLM reasoning

- **Challenge**: LLMs have latent causal structure (e.g., syntax trees might causally influence semantic understanding)
- **How CIG Helps** (speculative):
  - If causal structure of token dependencies is known (e.g., from parse trees), CIG could provide causal attribution of model outputs
  - Might improve interpretability of reasoning steps in multi-step problems

### 5. Regulatory & Compliance Contexts

**Use Case**: Explainable AI (XAI) compliance under AI Act, GDPR, HIPAA

- **Why CIG is Valuable**:
  - EU AI Act requires "meaningful information" about decisions for high-risk systems (healthcare, criminal justice)
  - Causal explanations are more meaningful than correlational ones
  - CIG provides "right to explanation" with formal grounding
- **Documentation**: CIG can generate audit trails showing causal reasoning paths
- **Fairness Implications**: Causal attribution helps detect whether model decisions reflect protected attributes vs. legitimate causal factors

---

## Insights & Implications

### Advances in Explainability

1. **Bridging Causality and Scalability**: CIG shows that causal inference and computational efficiency are not mutually exclusive. Prior work assumed expensive (Shapley) or non-causal (IG) methods were the only options.

2. **Moving Beyond "Feature Importance"**: CIG's decomposition of direct vs. mediated effects introduces a richer interpretability vocabulary, closer to how domain experts think about causation.

3. **Formalizing Domain Knowledge**: The framework allows practitioners to encode domain expertise (causal graphs) into attribution computations, making explanations more aligned with scientific understanding.

### Limitations and Open Questions

1. **Causal Graph Estimation**:
   - The method assumes the graph is known, but real causal structures are often uncertain
   - Future work: How should CIG be modified for uncertain causal graphs?
   - Options: Bayesian over graphs, robust attribution across graph variations

2. **Failure Modes**:
   - When the causal graph is misspecified, CIG provides incorrect causal explanations
   - This could be worse than correlational methods (which make no causal claims)
   - Risk of overconfidence in false causal stories

3. **Causal Sufficiency Violations**:
   - Many real systems have hidden confounders (unmeasured variables that affect multiple features)
   - CIG cannot handle these without instrumental variables or other causal identification strategies
   - Needs clear communication of when CIG is and isn't applicable

4. **Interplay with Fairness**:
   - Causal attribution clarifies whether a decision depends on protected attributes
   - But causal graphs themselves encode societal assumptions; poorly specified graphs perpetuate bias
   - How to ensure causal models are equitable remains open

### Future Research Directions

1. **Extending to Uncertain Causal Graphs**: Develop CIG variants that average over or robustify to causal graph uncertainty.

2. **Combining with Causal Discovery**: Use data-driven causal discovery (PC algorithm, GES) to estimate the causal graph, then apply CIG. Quantify sensitivity to discovery errors.

3. **Mechanistic Interpretability Connection**: CIG could be combined with mechanistic interpretability (circuit analysis) to explain neural networks at both the feature and module levels.

4. **Interactive & Iterative Explanations**: Extend CIG to generate explanations conditionally (e.g., "What if we intervene on feature X?"), supporting interactive exploration.

5. **Human-Centered Evaluation**: Conduct user studies on whether causal attributions from CIG improve domain experts' trust and decision-making compared to correlational methods.

6. **Cross-Domain Generalization**: Investigate whether causal structures learned or inferred in one domain transfer to related domains (e.g., causal graph of gene regulation across cell types).

---

## Code & Resources

### Official Implementation

- **Code Repository**: [Not yet released] (Anticipated release on arXiv GitHub or authors' lab page upon publication)
- **Implementation Language**: Python (likely PyTorch or TensorFlow based on model compatibility)
- **Main Dependencies**: (expected)
  - NumPy / SciPy for numerical computations
  - PyTorch or TensorFlow for neural network integration
  - Networkx or similar for causal graph representation
  - Scikit-learn for baseline models (if used)

### Quick Start Guide (Anticipated)

```python
# Pseudocode based on paper description

import causal_ig as cig
import networkx as nx

# Define causal graph
G = nx.DiGraph()
G.add_edges_from([("Feature1", "Feature2"), ("Feature1", "Output")])

# Instantiate CIG method
cig_explainer = cig.CausalIntegratedGradients(
    model=neural_net,
    causal_graph=G,
    baseline=baseline_input
)

# Compute attributions
attributions = cig_explainer.attribute(
    inputs=x,
    target=output_index,
    n_steps=50  # integration steps
)

# Decompose into direct & mediated effects
direct_effects = attributions.direct_effects
mediated_effects = attributions.mediated_effects
```

### Computational Requirements

- **Memory**: Proportional to number of integration steps × feature dimension (similar to standard IG)
- **GPU**: Recommended for large models; CPU feasible for moderate-sized networks
- **Runtime**: Minutes to hours depending on feature count and model complexity (vs. hours to days for causal Shapley)

### Interactive Visualizations (Anticipated)

- Causal graph visualization with attribution flow overlaid
- Stacked bar plots showing direct vs. mediated attribution decomposition
- Sensitivity analysis: how attributions change with different causal graphs

### Related Tools & Frameworks

- **SHAP** (Lundberg & Lee): Industry-standard feature attribution; CIG complements with causal structure
- **Captum** (Meta/PyTorch): PyTorch explanation library; might integrate CIG post-publication
- **Econml** (Microsoft): Causal ML library; potential integration for econometric applications
- **DoWhy** (Microsoft): Causal inference library; could use CIG for explanation tasks

---

## Related Work & Context

### Foundational Connections

1. **Integrated Gradients (Sundararajan et al., 2017)**:
   - Original attribution method that CIG extends
   - Provides axiomatic guarantees and computational efficiency
   - CIG inherits IG's completeness axiom

2. **Shapley Values for Feature Attribution (Lundberg & Lee, SHAP, 2017)**:
   - Game-theoretic foundation for attribution
   - Causal Shapley (Heskes et al., 2020) inspired CIG's causal approach
   - CIG achieves similar causal validity at lower computational cost

3. **Causal Inference Foundations**:
   - Pearl's Causal Hierarchies (2009): Formalism for causal reasoning via do-calculus
   - Potential Outcomes / Rubin Causal Model (Rubin, 1974): Alternative causal framework
   - CIG leverages Pearl's framework for formal definitions

### Related xAI Approaches

1. **Mechanistic Interpretability** (e.g., circuit analysis in transformers):
   - Focuses on internal model mechanisms rather than feature importance
   - Complementary to CIG: Could combine causal feature attribution with mechanistic explanations

2. **Concept-Based Explanations**:
   - Explain models via high-level semantic concepts rather than raw features
   - CIG could be applied to concept spaces (e.g., medical imaging ontologies) if causal relationships among concepts are available

3. **Causal Inference for Interpretability** (e.g., causal graphs of features):
   - Includes interventional explanation (Goyal et al., 2019) and counterfactual explanations
   - CIG formalizes this by tightly integrating causal structure into attribution computation

### Community Context

**xAI Research Areas Where CIG Contributes**:
- Feature Attribution Methods: Advances the state-of-the-art toward causal soundness
- Causality & Interpretability: Bridges the gap between causal inference and explanations
- High-Dimensional Domains: Practical tool for genomics, healthcare, finance where causal structure is partially known
- Regulatory Compliance: Supports AI Act and GDPR by providing principled causal explanations

**Relevant Workshops & Conferences**:
- NeurIPS XAI workshops
- ICML Causal Inference tracks
- AISTATS Interpretability sessions
- Domain-specific conferences (e.g., ISMB for bioinformatics)

### Potential Impact

- **Short-term** (1-2 years): Adoption in genomics and drug discovery where causal networks are well-studied
- **Medium-term** (2-5 years): Integration into explainability frameworks (SHAP, Captum); application expansion to healthcare and finance
- **Long-term** (5+ years): Convergence with mechanistic interpretability; causal explanation as standard for high-stakes AI decisions

---

## Summary

**Causal Integrated Gradients (CIG)** provides a principled, computationally efficient method for feature attribution that respects causal structure among inputs. By decomposing attributions into direct and mediated effects, CIG offers richer insights than correlational methods while maintaining the scalability of integrated gradients. The work advances both causal inference and explainability, with immediate applicability in genomics and potential impact on regulated AI systems. Key contributions include novel integration path design, formal axiomatic grounding, and practical demonstration on synthetic and biological data. Open challenges include handling uncertain or misspecified causal graphs and extending to settings with unmeasured confounders.

---

## References & Links

### Primary Paper
- **ArXiv**: [Causal Integrated Gradients: Scalable Feature Attribution Along Causal Paths (2610.22126)](https://arxiv.org/abs/2610.22126)
- **HTML Version**: https://arxiv.org/html/2610.22126
- **PDF**: https://arxiv.org/pdf/2610.22126

### Cited Foundational Works
- Integrated Gradients: [Axiomatic Attribution for Deep Networks](https://arxiv.org/abs/1703.01365)
- SHAP: [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874)
- Causal Shapley: [Causal Shapley Values](https://arxiv.org/abs/2104.02318)
- Pearl's Causal Model: [The Book of Why: The New Science of Cause and Effect](https://www.pearsonhighered.com/program/Pearl-The-Book-of-Why-The-New-Science-of-Cause-and-Effect/PGM1626455.html)

### Related Recent Papers
- Causal SHAP: [Feature Attribution with Dependency Awareness through Causal Discovery (2509.00846)](https://arxiv.org/abs/2509.00846)
- Position on Causality: [Causality is Key for Interpretability Claims to Generalise (2602.16698)](https://arxiv.org/abs/2602.16698)
- DAG-based Attribution: [Feature Attribution in Directed Acyclic Graphs Using Edge Intervention (2606.15273)](https://arxiv.org/abs/2606.15273)

### Tools & Frameworks
- [SHAP (GitHub)](https://github.com/slundberg/shap)
- [Captum by PyTorch](https://captum.ai/)
- [DoWhy by Microsoft](https://github.com/microsoft/DoWhy)
- [Econml by Microsoft](https://github.com/microsoft/EconML)

---

*Documentation synthesized from arXiv abstract, methodology summaries, and related interpretability literature. For complete mathematical proofs, full experimental results, and implementation details, refer to the full paper.*
