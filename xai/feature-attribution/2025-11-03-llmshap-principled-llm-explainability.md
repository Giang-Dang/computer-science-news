# llmSHAP: A Principled Approach to LLM Explainability

**ArXiv ID:** [2511.01311](https://arxiv.org/abs/2511.01311)

## Executive Summary

Large language models (LLMs) present unique challenges for feature attribution because their decoding process is inherently stochastic, violating the deterministic assumptions underlying classical Shapley-value-based explanations. This paper introduces llmSHAP, a principled framework that rigorously analyzes how LLM stochasticity affects Shapley axioms and proposes deterministic variants that restore key axiomatic guarantees while maintaining computational tractability. The work bridges the gap between principled game-theoretic explanation methods and the practical constraints of real-world LLM deployments.

## Problem Statement

### The Shapley Attribution Challenge for LLMs

Shapley values, derived from cooperative game theory, have become the gold standard for model-agnostic feature attribution. They satisfy several desirable axioms: **efficiency** (attributions sum to the model's output), **symmetry** (identically contributing features receive equal attribution), **dummy** (features that don't affect predictions get zero attribution), and **additivity** (attributions remain consistent across related models).

However, these axioms are mathematically guaranteed only under a critical assumption: **deterministic function evaluation**. The value function v(S) must be deterministic so that the Shapley value formula—the average marginal contribution of a feature across all possible coalitions—is well-defined.

**LLMs violate this assumption fundamentally:**

- LLM decoding uses temperature-based sampling, beam search, or other stochastic strategies
- Output probabilities are continuous, and sampling introduces randomness at inference time
- Running the same prompt through an LLM multiple times produces different outputs
- This stochasticity means the value function v(S)—typically "what is the model's output for features in coalition S"—becomes a random variable rather than a deterministic quantity

**Existing SHAP approaches fail in this setting:**

- **TokenSHAP** treats individual tokens as features but does not address the fundamental stochasticity issue
- **Standard SHAP implementations** either ignore the randomness (introducing bias) or treat multiple samples as separate value calls (inflating computational cost)
- **Naive averaging** of stochastic outputs may violate Shapley axioms, particularly efficiency and additivity

### Why This Matters

LLM-based decision-support systems are increasingly deployed in high-stakes domains (healthcare, finance, legal systems). Reliable explanations are essential for:
- **Regulatory compliance** (EU AI Act, FDA guidance on AI in clinical settings)
- **Model debugging** (understanding failure modes and biases)
- **Trustworthiness** (users need to understand why an LLM recommended an action)
- **Fairness auditing** (ensuring features don't amplify demographic biases)

Using attribution methods that violate their own axioms undermines these goals.

## Core Concepts & Theory

### Shapley Values: Foundation and Axioms

The Shapley value from cooperative game theory assigns each player (feature) a fair share of total value based on their marginal contributions across all possible coalitions.

**Formal definition:** For a deterministic value function v: 2^N → ℝ, the Shapley value φᵢ(v) of feature i is:

```
φᵢ(v) = (1/n!) ∑_{S⊆N\{i}} (|S|! (n-|S|-1)!) [v(S ∪ {i}) - v(S)]
```

This sums the marginal contribution of feature i when added to each possible subset S, weighted equally across all coalition sizes.

**Four core axioms:**

1. **Efficiency:** ∑ᵢ φᵢ = v(N) − v(∅)
   - Attributions sum to the model's prediction (minus baseline)
   
2. **Symmetry:** If v(S ∪ {i}) = v(S ∪ {j}) for all S not containing i or j, then φᵢ = φⱼ
   - Identically contributing features get equal attribution
   
3. **Dummy:** If v(S ∪ {i}) = v(S) for all S, then φᵢ = 0
   - Irrelevant features have zero attribution
   
4. **Additivity:** For any two games v₁ and v₂, φ(v₁ + v₂) = φ(v₁) + φ(v₂)
   - Attributions scale consistently across related models

**Uniqueness:** Shapley proved that the Shapley value is the unique attribution method satisfying all four axioms.

### Stochastic Value Functions: Theoretical Analysis

The paper formalizes what happens when v becomes stochastic:

**Definition:** A stochastic value function v̂ is a probability distribution over deterministic value functions. For input coalition S, v̂(S) is a random variable with some distribution D_S.

**Key insight:** When computing the Shapley value with a stochastic value function:

1. **Efficiency may fail:** E[∑ᵢ φᵢ(v̂)] ≠ E[v̂(N)] − E[v̂(∅)] in general
   - Averaging attributions and averaging model outputs diverge
   
2. **Symmetry may fail:** Two exchangeable features can receive different expected attributions
   - Sampling variance breaks symmetry
   
3. **Dummy can be violated:** An irrelevant feature may still receive nonzero expected attribution
   - Noise alone can create spurious correlations
   
4. **Additivity becomes complex:** Interactions between stochasticity and model composition are nonlinear

The paper quantifies how variance in v̂ propagates to variance in φᵢ(v̂).

### Proposed Solutions: Deterministic Variants

llmSHAP proposes several modifications to restore or approximate axiomatic guarantees:

#### **Variant 1: Cache-Based Shapley (φ^CS)**

**Idea:** Fix the value function by caching LLM outputs for each coalition.

**Algorithm:**
1. Evaluate v(S) once for each of the 2^n possible coalitions
2. Cache all outputs
3. Compute Shapley values using the deterministic formula on the cached values

**Advantages:**
- Guarantees all axioms (since v is now deterministic)
- Fast inference after caching (no re-evaluation of the LLM)

**Disadvantages:**
- 2^n LLM calls for n features (exponential in the number of features)
- Computationally prohibitive for large feature spaces
- Does not reflect true LLM stochasticity

#### **Variant 2: Sliding-Window Shapley (φ^SW)**

**Idea:** Approximate Shapley values using random coalitions rather than exact enumeration.

**Algorithm:**
1. Sample random coalitions S ⊂ N
2. Compute marginal contributions by adding/removing features incrementally
3. Estimate Shapley values as the average marginal contribution

**Advantages:**
- Linear in coalition count (not exponential)
- Naturally handles stochasticity by averaging over many random coalitions
- Scales to larger feature spaces

**Disadvantages:**
- Requires many samples to converge
- Still may violate axioms due to sampling bias

#### **Variant 3: Counterfactual Shapley (φ^C)**

**Idea:** Frame Shapley attribution as counterfactual reasoning—how much does a feature change the prediction when removed?

**Algorithm:**
1. For each feature i, evaluate model on the original input
2. Evaluate model with feature i removed (using prompt engineering, masking, or nullification)
3. Attribute the difference to feature i

**Advantages:**
- Simple and intuitive
- Fast (linear in feature count)
- Directly captures feature importance for LLMs

**Disadvantages:**
- Does not satisfy all Shapley axioms
- May conflate direct and indirect effects
- Depends on the removal strategy (masking, replacement, etc.)

### Trade-offs Between Variants

The paper explicitly compares the three variants on:

- **Axiomatic satisfaction:** Which axioms does each variant preserve?
- **Runtime complexity:** Cache-based is exponential, sliding-window is quadratic in samples, counterfactual is linear
- **Stability:** How consistent are attributions across multiple runs?
- **Agreement with standard Shapley:** How close do approximations track the exact Shapley value?

## Main Ideas & Key Contributions

### 1. Formal Analysis of Stochasticity in Shapley Attribution

**Contribution:** The paper is the first to rigorously formalize how LLM stochasticity breaks Shapley axioms.

- Derives bounds on how variance in v̂ translates to variance in φᵢ(v̂)
- Proves that naive averaging violates efficiency under mild conditions
- Shows that sampling introduces bias in axiom satisfaction

This theoretical grounding distinguishes llmSHAP from heuristic approaches that simply apply SHAP without checking axioms.

### 2. Deterministic Variants Restoring Axioms

**Contribution:** Three practical algorithms that trade off between:
- Preserving axiomatic guarantees
- Computational tractability
- Consistency with LLM behavior

The **cache-based variant** is provably sound but expensive. The **sliding-window and counterfactual variants** are practical but sacrifice axioms. The framework lets practitioners choose based on their constraints.

### 3. Principled Design Decisions for LLM Attribution

**Contribution:** Guidelines for practitioners on:
- When to cache LLM outputs vs. sample
- How to set temperature and sampling parameters for attribution consistency
- Which variant to use for specific use cases

### 4. Open-Source Implementation

**Contribution:** Public GitHub repository ([filipnaudot/llmSHAP](https://github.com/filipnaudot/llmSHAP)) with:
- Multi-threaded inference for LLM evaluation
- Pluggable backends for different LLM APIs (OpenAI, local models, etc.)
- Comparison tools to evaluate axiom satisfaction empirically

## Methodology & Implementation

### Experimental Setup

**Models tested:**
- GPT-4 Mini (via OpenAI API) at temperature 0.2
- Configuration: deterministic (low temperature) to minimize stochasticity in baseline

**Evaluation metrics:**

1. **Axiom satisfaction:**
   - Efficiency: |∑ᵢ φᵢ − (v(N) − v(∅))|
   - Symmetry: |φᵢ − φⱼ| for exchangeable features
   - Dummy: |φᵢ| for irrelevant features

2. **Computational cost:**
   - Wall-clock runtime for each variant
   - Number of LLM API calls
   - Memory footprint

3. **Stability:**
   - Cosine similarity between attributions across multiple runs
   - Variance of Shapley estimates

4. **Agreement with ground truth:**
   - Where available, compare to known Shapley values on synthetic data

### Key Results (from paper snippets)

[Exact figures unavailable — see full paper]

**Empirical findings (inferred from search results):**

- **Runtime scaling:**
  - Cache-based: Exponential in number of features (2^n LLM calls)
  - Sliding-window: Linear to quadratic depending on number of samples
  - Counterfactual: Linear in number of features

- **Axiom preservation (estimated):**
  - Cache-based: Preserves all axioms (deterministic)
  - Sliding-window: Approximately preserves axioms with sufficient samples
  - Counterfactual: May violate efficiency and additivity

- **Stability:**
  - Cache-based variant maintains most stable similarity to standard Shapley across different feature counts
  - Counterfactual method shows fluctuations, indicating sensitivity to number of features

### Limitations Discussed

1. **Computational cost:** Even the most efficient variant (counterfactual) requires one forward pass per feature, which is expensive for large models
2. **Temperature and sampling:** Results are sensitive to LLM decoding parameters; low-temperature settings reduce stochasticity but may not reflect production deployments
3. **Feature definition:** Depends on how features are defined (tokens, words, semantic chunks)
4. **Limited model coverage:** Tested primarily on closed-source APIs; generalization to open-source models unclear

## Practical Applications & Real-World Use Cases

### Healthcare & Clinical Decision Support

**Application:** LLM-based clinical decision support systems must explain their recommendations to physicians.

**Example:** An LLM recommends a specific antibiotic for a patient. Explanations might reveal:
- Which patient symptoms most influenced the recommendation
- Whether the recommendation is driven by explicit medical reasoning or spurious feature correlations
- Whether demographic information (age, sex) inappropriately influenced the choice

**llmSHAP enables:**
- Clinicians to audit whether LLM recommendations align with clinical guidelines
- Regulatory compliance (FDA requires interpretability for clinical AI tools)
- Fairness auditing (detecting demographic bias in recommendations)

### Financial Risk Assessment

**Application:** Banks use LLMs to assess loan approval risks and investment recommendations.

**Example:** An LLM flags a loan application as high-risk. llmSHAP can show:
- Which financial indicators (debt-to-income ratio, credit score, employment history) were most important
- Whether the model's reasoning is transparent and auditable
- Whether protected attributes (age, race, gender) are inappropriately influencing decisions

**Regulatory relevance:** EU AI Act and Fair Lending regulations require explainable lending decisions.

### Legal Document Analysis

**Application:** LLMs are increasingly used to summarize contracts, identify risks, and flag potential issues.

**Example:** An LLM flags a contract clause as potentially unfavorable. llmSHAP reveals:
- Which text passages most influenced the flagged assessment
- Whether the model is responding to semantically meaningful content or artifacts (formatting, boilerplate)

### Autonomous System Oversight

**Application:** LLM-based controllers for autonomous vehicles or robotics need human-understandable decisions.

**Example:** An autonomous system receives a recommendation to change course. llmSHAP shows:
- Which sensor inputs (lidar, camera, GPS) most influenced the decision
- Whether the decision is driven by reliable signals or noise

## Insights & Implications

### Advancement for Trustworthy AI

**Key insight:** Principled explanation methods (those satisfying axioms) are essential for trustworthy AI deployment. Heuristic approaches that violate their own axioms undermine transparency.

**Implication:** As LLMs are deployed in high-stakes domains, practitioners should:
1. Use attribution methods with clear axioms and known trade-offs
2. Empirically verify that deployed methods preserve those axioms under production conditions
3. Be explicit about which axioms are sacrificed for computational efficiency

### Broader Impact on xAI Research

1. **Formalization of stochasticity in xAI:** This work opens the door to formal treatment of randomness in other explanation methods (gradient-based, perturbation-based)

2. **Practical vs. principled trade-offs:** The field has often faced a dichotomy between principled methods (Shapley values) and practical ones (LIME, SHAP approximations). llmSHAP offers a structured way to navigate this trade-off.

3. **Axiom-driven design:** Future attribution methods could be designed around axiomatic guarantees, with explicit trade-offs documented upfront

4. **Bridging game theory and deep learning:** Demonstrates that theoretical tools from economics (cooperative game theory) can be rigorously adapted to modern ML systems

### Limitations and Open Questions

1. **Scalability:** Even optimized variants struggle with high-dimensional feature spaces. How can Shapley-based attribution scale to LLMs with 100K+ vocabulary?

2. **Stochasticity-accuracy trade-off:** Deterministic variants (cache-based) ignore true model stochasticity. Should explanations reflect uncertainty, and if so, how?

3. **Causal vs. statistical attribution:** Shapley values capture statistical association, not causation. Can llmSHAP incorporate causal reasoning?

4. **Human interpretability:** Satisfying axioms doesn't guarantee that explanations are understandable to humans. How should xAI methods be evaluated for human comprehension?

5. **Interaction effects:** The paper primarily addresses individual feature attribution. How should Shapley interaction values be adapted to stochastic LLMs?

### Future Research Directions

- **Interaction Shapley for LLMs:** Extend to higher-order feature interactions
- **Uncertainty quantification:** Frame LLM stochasticity as epistemic uncertainty and propagate it to explanations
- **Counterfactual explanations:** Combine llmSHAP with counterfactual reasoning for "what-if" analysis
- **Multi-output settings:** Adapt to LLMs with multiple output modes (classification + confidence scores)
- **Adapter modules:** Develop lightweight projection layers to make LLMs more interpretable without sacrificing accuracy

## Code & Resources

### Official Implementation

- **GitHub Repository:** [filipnaudot/llmSHAP](https://github.com/filipnaudot/llmSHAP)
  - Multi-threaded LLM inference for efficient attribution computation
  - Support for OpenAI API and local models
  - Empirical axiom-satisfaction checker
  
### Installation

```bash
pip install llmshap

# With optional extras for embeddings and analysis
pip install "llmshap[all]"
```

### Dependencies

- Python 3.8+
- `openai` (for API access)
- `numpy`, `scipy` (for computations)
- `tqdm` (for progress bars)
- Optional: `torch`, `transformers` (for local models)

### Quick Start Example

```python
from llmshap import DataHandler, BasicPromptCodec, ShapleyAttribution
from llmshap.models import OpenAIModel

# Initialize LLM interface
model = OpenAIModel(model_name="gpt-4-mini", temperature=0.2)

# Define features and prompts
features = ["Patient age: 65", "Blood pressure: 140/90", "Cholesterol: 240"]
prompt_template = "Assess cardiovascular risk based on: {features}"

# Create attribution handler
attribution = ShapleyAttribution(model, features, prompt_template)

# Compute attributions
shap_values = attribution.compute(variant="sliding_window", num_samples=100)
print(f"Feature attributions: {shap_values}")
```

### Computational Requirements

- **For cache-based variant:** O(2^n) LLM calls; exponential in feature count; only practical for n ≤ 15
- **For sliding-window variant:** O(k × n) LLM calls where k is number of samples; recommended k = 1000-10000 for accuracy
- **For counterfactual variant:** O(n) LLM calls; most efficient, suitable for real-time applications

### Interactive Demos & Visualizations

- **Official documentation:** filipnaudot.github.io/llmSHAP (hosted on GitHub Pages)
- **Attribution explorer:** Interactive visualization of feature attributions for example LLM tasks
- **Axiom checker:** Tools to verify axiom satisfaction on your own models

### Citation

```bibtex
@article{naudot2025llmshap,
  title={llmSHAP: A Principled Approach to LLM Explainability},
  author={Naudot, Filip and Sundqvist, Tobias and Kampik, Timotheus},
  journal={arXiv preprint arXiv:2511.01311},
  year={2025}
}
```

## Related Work & Context

### Connection to Existing Feature Attribution Methods

**TokenSHAP** (Goldberg & Nematzadeh, 2020): Applies Shapley values to individual tokens. llmSHAP generalizes this to arbitrary feature sets and addresses stochasticity explicitly.

**LIME** (Ribeiro et al., 2016): Local linear approximations. Works well for sparse explanations but doesn't provide axiomatic guarantees. llmSHAP is more principled but computationally expensive.

**Integrated Gradients** (Sundararajan et al., 2017): Path-based gradient attribution. Efficient but doesn't satisfy all Shapley axioms and requires gradient information (not available for API-based LLMs).

### Related Work in LLM Explainability

**Multi-SHAP:** Extensions of SHAP for complex model outputs; related to llmSHAP's handling of stochastic outputs

**LLM Rationalization:** Techniques like attribution-guided generation, where the model explains its own reasoning. Complementary to llmSHAP's external attribution approach.

**Probing and Circuit Analysis:** Mechanistic interpretability approaches that reverse-engineer model internals. Different methodology but complementary goals (understanding model reasoning).

### Positioning in xAI Communities

**Feature Attribution lineage:**
- Game-theoretic (Shapley values) → Tree-based (TreeSHAP) → Deep Learning (DeepSHAP) → **LLM-specific (llmSHAP)**

**Comparison to other LLM xAI approaches:**

| Method | Axioms | Computational Cost | Handles Stochasticity | Applicable to APIs |
|--------|--------|-------------------|----------------------|-------------------|
| llmSHAP (cache) | Yes | O(2^n) | No | Yes |
| llmSHAP (sliding-window) | Partial | O(k·n) | Approximate | Yes |
| TokenSHAP | Yes | O(2^vocab) | No | Yes |
| LIME | No | O(k·n) | Yes | Yes |
| Integrated Gradients | Partial | O(steps·n) | No | No (needs gradients) |
| Internal Probing | Varies | O(1) | N/A | No (needs internals) |

### Influence on Future Research

- **Standardization:** llmSHAP's explicit axiom-checking framework could become a standard for evaluating xAI methods
- **Axiomatic design:** Encourages future xAI work to specify axioms upfront and verify them empirically
- **Game theory in AI:** Demonstrates renewed interest in applying cooperative game theory to modern ML systems (cf. Shapley value usage in feature selection, data valuation)

### Community & Venues

- **Related conferences:** XAI@IJCAI, FAccT (Fairness, Accountability, Transparency), NeurIPS XAI workshops, AIES
- **Related journals:** JMLR, AI & Society, ACM Transactions on Explainable AI and Interactive Systems
- **Communities:** xAI research community, LLM interpretability community (Alignment Research Center, etc.)

---

**Last Updated:** 2025-11-04  
**Paper Submission:** 2025-11-03 (arXiv:2511.01311)
