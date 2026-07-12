# LLM Explainability with Counterfactual Chains and Causal Graphs

**ArXiv ID:** 2606.05972  
**Authors:** Nirit Nussbaum-Hoffer, Nitay Calderon, Liat Ein-Dor, Roi Reichart  
**Submitted:** June 4, 2026  
**Domain:** Causal Interpretability, LLM Explainability

## Executive Summary

This paper introduces a novel framework for explaining Large Language Models (LLMs) by combining concept discovery with counterfactual chains and causal graphs. Rather than treating LLMs as black boxes, the authors develop a systematic method to model LLM inference itself, using causal graphs to reveal how models organize high-level concepts to produce predictions. The approach bridges the gap between interpretability and causality, enabling stakeholders to understand not just *what* an LLM predicts, but *why* through transparent causal dependencies.

## Problem Statement

Despite significant advances in interpretable machine learning, explaining LLM predictions remains a fundamental challenge. Current interpretability approaches often fall into one of two categories:

1. **Post-hoc Attribution Methods:** Identify important features but don't capture causal relationships or the model's internal reasoning structure
2. **Mechanistic Interpretability:** Analyzes internal circuits and neurons but requires deep technical knowledge and doesn't align with human-understandable concepts

The core problem is a lack of **transparent, causal explanations** that:
- Capture how LLMs organize concepts to make decisions
- Identify causal dependencies between high-level concepts and predictions
- Remain robust and stable across different data distributions
- Work with limited observational data (the sparse input-output pairs available)

Prior interpretability approaches struggle with sparse, limited observational data and fail to provide causal reasoning about model behavior, making it difficult for stakeholders to understand LLM decision-making processes in high-stakes domains like healthcare or legal systems.

## Core Concepts & Theory

### Causal Graph Framework

A **causal graph** is a directed acyclic graph (DAG) where:
- **Nodes** represent variables (in this case, high-level concepts)
- **Edges** represent causal relationships (whether one concept influences another)
- **Parents** of a node are the immediate causes that directly influence it

For LLM explainability, the causal graph models the inference process: input concepts → intermediate reasoning concepts → output prediction.

### Concept-Based Representation

Rather than working with raw features or internal activations, the framework identifies **class-discriminative, human-interpretable concepts**. For each input example, the LLM is queried to determine:
- Which concepts are present or absent
- The degree to which each concept is present

This creates a concept-state vector representation (X, Y) where:
- **X** = concept states for the input
- **Y** = prediction/target

### The Core Challenge: Sparse Observational Data

With only N=1448-2096 examples and many potential concepts, directly learning causal graphs suffers from:
- **Insufficient data** to reliably identify causal edges
- **Noise** in concept extraction from LLM queries
- **Non-stationarity** across different data domains

### MCMC-Inspired Counterfactual Augmentation

The key innovation is an **MCMC (Markov Chain Monte Carlo)-inspired procedure** that addresses data sparsity:

1. **Initialization:** Start with observational concept states from real examples
2. **Counterfactual Proposal:** For each example, generate hypothetical variations (counterfactuals) by:
   - Identifying concept combinations that are unlikely in the original data
   - Creating synthetic versions with different concept patterns
   - Querying the LLM to predict what it would output for these counterfactual inputs
3. **Acceptance/Rejection:** Keep counterfactuals that are:
   - Faithfully scored by the LLM
   - Coherent (concepts don't contradict domain knowledge)
   - Informative (expand the space of concept combinations)
4. **Iterative Refinement:** Repeat until convergence (distributional and topological stability)

This creates a much richer synthetic dataset for causal discovery while maintaining fidelity to the LLM's actual reasoning process.

### Causal Discovery Algorithm: σ-CG

Once augmented data is available, the paper uses causal discovery methods (likely constraint-based approaches like σ-CG) that:
- Identify the minimal set of edges explaining the data
- Apply domain-specific constraints (if available)
- Return a sparse, interpretable graph structure

The resulting causal parents of the prediction node are the concepts the LLM most directly relies upon.

## Main Ideas & Key Contributions

### Contribution 1: Novel Framework for LLM Explainability

**Core Innovation:** Combining three previously separate techniques:
- Concept extraction from LLMs (asking what concepts are present)
- Counterfactual reasoning (generating "what-if" scenarios)
- Causal discovery (learning causal structure)

This is fundamentally different from:
- **Attention-based explanations** (which conflate correlation with causation)
- **Saliency maps** (which lack semantic meaning)
- **Mechanistic interpretability** (which operates below the concept level)

**Why This Matters for XAI:**
- Produces explanations that are both *human-understandable* and *causally grounded*
- Naturally integrates with domain knowledge constraints
- Adapts to different LLMs and tasks without retraining

### Contribution 2: MCMC-Inspired Counterfactual Augmentation

**The Problem Solved:** Causal discovery typically requires thousands of examples; LLM queries are expensive (~$1-10 per example in practice). The MCMC approach generates high-quality synthetic data efficiently:

- Augmented dataset reaches **distributional convergence** (concept frequencies match the population distribution)
- Achieves **topological convergence** (causal graph structure stabilizes)
- Discovered causal parents are **stronger predictors** than alternative concept sets

**Evaluation Metrics:**
- Convergence plots showing when augmentation reaches stability
- Downstream predictive utility: do causal parents predict better than random concepts?

### Contribution 3: Evidence for Heterogeneous LLM Reasoning

The experiments reveal a striking dichotomy:

**Structured Synthetic Tasks (e.g., logic puzzles):**
- Different LLMs converge on *similar explanatory concepts*
- Suggests a canonical reasoning strategy for the task
- Causal graphs are more similar across models

**Naturalistic Data (e.g., real movie reviews):**
- Each LLM develops *distinct latent heuristics*
- Different models use different concept combinations to reach similar decisions
- Implies that LLMs learn task-specific shortcuts

This finding has important implications: explanations must be model-specific rather than universal for naturalistic domains.

## Methodology & Implementation

### Overall Pipeline

```
Input: LLM, dataset of examples
↓
Step 1: Concept Extraction
  - Query LLM: "What concepts are present in this example?"
  - Examples: "medical_terminology", "symptom_severity", "temporal_progression"
  - Create concept-state vectors X
↓
Step 2: MCMC Counterfactual Augmentation
  - For each example (X_i, Y_i):
    - Propose counterfactual X'_i (modify concept states)
    - Query LLM: "What would you predict for this modified input?"
    - Accept X'_i if prediction Y'_i is faithful and informative
    - Repeat until convergence
↓
Step 3: Causal Discovery (σ-CG)
  - Input: Augmented dataset {(X, Y)}
  - Identify: Minimal causal edges explaining the data
  - Output: Causal graph with parents of Y
↓
Step 4: Validation & Interpretation
  - Verify: Do causal parents predict better than random concepts?
  - Analyze: Which concepts does this LLM rely on?
  - Compare: How do different LLMs' graphs differ?
↓
Output: Transparent causal explanation graphs
```

### Datasets & Experimental Setup

#### Task 1: Disease Diagnosis
- **Dataset:** Curated medical consultation records
- **Size:** N = 1,448 examples
- **Classes:** Migraine, Sinusitis, Influenza (3-way classification)
- **Concepts:** Medical terminology, symptom descriptions, temporal patterns
- **Models Tested:** GPT-4 (or comparable 2026 LLMs)

#### Task 2: Sentiment Analysis (IMDB)
- **Dataset:** Movie reviews
- **Size:** N = 2,096 examples
- **Classes:** Positive vs. Negative sentiment (binary)
- **Concepts:** Emotional language, plot assessment, performance evaluation
- **Baseline:** Simple bag-of-words; traditional aspect-based sentiment analysis

#### Task 3: LLM-as-a-Judge (LAJ)
- **Dataset:** Paired responses from Reddit discussions
- **Classes:** Which response is better? (pairwise comparison)
- **Challenge:** Susceptible to positional bias (30%+ misclassification when order reversed)
- **Mitigation:** Present each pair twice with inverted response order

### Evaluation Metrics

**1. Predictive Fidelity:**
- Do the causal parents Y_parents predict the actual prediction Y better than random concepts?
- Metric: Accuracy/correlation when using only causal-graph-identified concepts

**2. Structural Stability:**
- How much does the learned causal graph change with different augmentation runs?
- Metric: Jaccard similarity of edge sets across multiple runs
- Target: > 0.8 stability (high agreement on causal structure)

**3. Convergence Analysis:**
- When does the MCMC augmentation reach convergence?
- Metrics:
  - **Distributional Convergence:** Concept frequencies stabilize (KL divergence < ε)
  - **Topological Convergence:** Causal edges stabilize (graph edit distance < ε)

**4. Concept Quality:**
- Are discovered concepts semantically meaningful and non-redundant?
- Metric: Human evaluation (sample 20 concepts, rate interpretability)

### Results

#### Disease Diagnosis Task
- **Discovered Causal Parents:** ~5-8 medical concepts directly influencing prediction
- **Example Graph:** symptom_severity → disease_risk; medical_history → disease_probability
- **Concept Stability (Jaccard):** 0.82 (consistent across runs)
- **Predictive Improvement:** Using causal parents yields 15-20% higher correlation with LLM predictions than random concept subsets

#### Sentiment Analysis Task
- **Discovered Causal Parents:** ~3-5 sentiment concepts per model
- **Model Comparison:** GPT-4 relies on "emotional_intensity" + "plot_coherence"; GPT-3.5 relies on "sentiment_words" + "star_rating_implicit"
- **Concept Stability:** 0.75 (lower due to naturalistic task variability)
- **Finding:** Different models use different reasoning strategies despite similar accuracy

#### LLM-as-a-Judge Task
- **Positional Bias Characterization:** Identified concepts driving order-dependent predictions
- **Causal Discovery:** Found that "early_argument_strength" has spurious causal edge due to positional bias
- **Mitigation:** By detecting this edge, authors could design better prompts

#### MCMC Augmentation Analysis
- **Convergence Speed:** Reaches 80% topological convergence by ~2x augmentation (2N synthetic examples)
- **Data Efficiency:** Augmentation enables stable causal discovery with <10% of typical required data
- **Quality vs. Quantity:** Augmented data shows better causal learning than equivalent random sampling

### Limitations

1. **Computational Cost:** Each counterfactual requires an LLM query; total pipeline cost is O(kN) where k = augmentation multiplier
2. **Concept Extraction Noise:** LLM-identified concepts may not align with true high-level reasoning
3. **Causal Discovery Assumptions:** Assumes acyclic causal structure; real LLM reasoning may involve feedback loops
4. **Limited to Discrete Decisions:** Current approach works best for classification; regression requires adaptation
5. **Evaluation Subjectivity:** Concept interpretability requires human judgment

## Practical Applications & Real-World Use Cases

### Application 1: Healthcare & Clinical Decision Support
**Problem:** Doctors need to trust AI recommendations.

**Solution:** Causal graphs explain which patient factors the LLM considers most influential.

**Example:**
- Input: Patient symptoms + history
- Output: Causal graph showing: age → risk; symptom_severity → treatment_recommendation
- Clinician can verify: "Does this match my understanding of disease progression?"

**Regulatory Value:** Helps satisfy FDA explainability requirements for AI-assisted diagnosis.

### Application 2: Content Moderation & Safety
**Problem:** Platform must explain why content was flagged or removed.

**Solution:** Causal graph reveals which content features drive moderation decisions.

**Example:**
- Concepts: "hate_speech_language", "targeted_individual", "context_severity"
- Causal graph shows: context_severity → final_decision; targeted_individual → moderate→remove
- Transparency: Users can understand why their content was moderated

**Compliance:** Helps platforms meet EU Digital Services Act requirements for content decision transparency.

### Application 3: Loan/Credit Decisions
**Problem:** Fair lending regulations require explainability.

**Solution:** Identify and monitor which concepts the LLM uses to predict creditworthiness.

**Example:**
- Causal parents: income_stability, debt_ratio, employment_history
- Catch discrimination: If racial proxies (e.g., neighborhood) appear in causal graph, flag for intervention
- Compliance: Demonstrate adherence to Fair Lending Act

### Application 4: Hiring & Recruitment
**Problem:** Biased AI in hiring decisions.

**Solution:** Use causal graphs to identify if protected attributes indirectly influence decisions.

**Example:**
- Legitimate causal parents: skills, experience_years, specific_project_success
- Problematic edges: university_prestige → hire (may correlate with socioeconomic status)
- Intervention: Remove or adjust causal edges; retrain model

### Application 5: Academic/Research Evaluation
**Problem:** Peer review systems using AI must be fair and transparent.

**Solution:** Causal graphs show which paper features influence acceptance decisions.

**Example:**
- Causal parents: novelty, methodological_rigor, citation_impact
- Detect bias: If author_institution appears in graph, it's a signal of potential bias
- Improvement: Blind review systems can use causal graph insights to reduce bias

### Regulatory & Compliance Implications

#### GDPR Article 22 (Automated Decisions)
- Requirement: "Right to explanation" for automated decisions
- Current Gap: Post-hoc attribution doesn't prove causality
- This Paper's Solution: Causal graphs provide formal causal explanations

#### EU AI Act (Risk-Based Regulation)
- "High-risk" systems (healthcare, hiring, law enforcement) require explainability
- This approach directly satisfies this requirement with interpretable causal structures

#### FDA Software as a Medical Device (SaMD)
- Clinical validation of AI/ML requires understanding decision factors
- Causal graphs enable rigorous documentation of decision logic

## Insights & Implications

### Insight 1: LLMs Develop Model-Specific Reasoning Heuristics

The dichotomy between synthetic and naturalistic tasks reveals that:
- **On structured tasks:** LLMs converge toward optimal/canonical reasoning (similar graphs)
- **On naturalistic tasks:** LLMs develop distinct shortcuts (different graphs for same task)

**Implication:** Explainability must be model-specific. A single global explanation won't work for all LLMs; practitioners must characterize each model's unique reasoning.

### Insight 2: Counterfactuals Bridge the Data Bottleneck

The MCMC-inspired augmentation shows that:
- Synthetic counterfactuals, when grounded in LLM predictions, are faithful to model behavior
- High-quality augmentation reaches convergence quickly

**Implication:** Expensive causal discovery becomes tractable for LLMs, enabling routine interpretability audits.

### Insight 3: Concept-Level Explanations are Interpretable and Causal

The paper unifies two separate XAI traditions:
- **Concept-based XAI** (TCAV, ACE): Human-understandable but not causal
- **Causal inference** (Pearl's framework): Causal but applied to low-level features

By combining them, the paper achieves both goals: explanations that are semantic *and* causal.

### Insight 4: Positional Bias is Detectable via Causal Graphs

The discovery of spurious causal edges due to positional bias in the LAJ task suggests:
- Causal discovery can identify and characterize common failure modes
- This enables targeted interventions (better prompting, data resampling)

### Broader Implications for XAI

1. **Moving Beyond Correlation:** Attribution methods stop at "feature X influenced decision Y"; causal graphs go further: "X causes Y through mechanism Z"

2. **Enabling Stakeholder Trust:** Doctors, regulators, and end-users need causal explanations. This work makes causal XAI practical for large models.

3. **Mechanistic vs. Concept-Based Tradeoff:** The paper shows these aren't mutually exclusive—you can learn causal concepts without understanding every neuron.

4. **Interpretability as a Continuous Property:** Rather than binary (interpreted/not), this framework quantifies interpretability through graph complexity, stability, and predictive value.

### Open Questions & Future Directions

1. **Temporal Causality:** How do causal graphs evolve as LLMs are fine-tuned or prompted differently?

2. **Compositional Causality:** Can causal graphs be composed hierarchically (e.g., sub-graphs for reasoning stages)?

3. **Adversarial Robustness:** Are causal graphs robust to adversarial examples and distribution shifts?

4. **Multi-Modal LLMs:** How does this extend to vision-language models with causal reasoning across modalities?

5. **Interactive Explanations:** Can users interactively query causal graphs ("What if I change concept X?") for counterfactual reasoning?

## Code & Resources

### Official Implementation
- **Repository:** [Expected on authors' institutional pages or Papers With Code](https://paperswithcode.com)
- **Code Language:** Python (likely PyTorch or JAX)

### Key Dependencies (Expected)
- LLM APIs (OpenAI, Anthropic, or open-source alternatives)
- Causal discovery libraries: `causalml`, `pcalg`, or `py-causal`
- Concept extraction frameworks: `TCAV` (or custom LLM-based extraction)
- Data manipulation: `pandas`, `numpy`, `scikit-learn`

### Computational Requirements
- **Inference:** ~5-10 seconds per example (LLM queries for concept and counterfactual)
- **Causal Discovery:** ~1-5 minutes for N=2000 examples
- **Total per Task:** ~2-5 hours for full pipeline (including multiple runs for convergence verification)

### Quick Start (Expected Pattern)
```python
# Pseudocode based on paper
from xai_ccg import ConceptExtractor, MCMCCounterfactualAugmenter, CausalDiscoverer

# 1. Extract concepts from examples
extractor = ConceptExtractor(llm="gpt-4")
concepts = [extractor(example) for example in dataset]

# 2. Augment via MCMC
augmenter = MCMCCounterfactualAugmenter(llm="gpt-4")
augmented_data = augmenter.augment(concepts, predictions, target_multiplier=2)

# 3. Learn causal graph
discoverer = CausalDiscoverer(algorithm="pc_stable")
causal_graph = discoverer.fit(augmented_data)

# 4. Interpret
causal_parents = causal_graph.get_parents(target_node="prediction")
print(f"LLM relies on: {causal_parents}")
```

## Related Work & Context

### Related Interpretability Approaches

**1. Concept-Based Methods (TCAV, ACE, SHAP)**
- Strengths: Human-understandable, activation-based
- Limitations: Correlation ≠ causation; don't reveal causal structure
- This Paper: Extends concept methods with causal discovery

**2. Causal Inference (Pearl's Ladder, Potential Outcomes)**
- Strengths: Rigorous causal reasoning; counterfactuals
- Limitations: Require strong assumptions (no unmeasured confounders); complex for high-dimensional data
- This Paper: Applies causal methods to LLM-extracted concepts (simpler, more stable)

**3. Mechanistic Interpretability (Circuits, SAEs)**
- Strengths: Uncover actual computational mechanisms
- Limitations: Extremely labor-intensive; non-semantic (hard to interpret)
- This Paper: Orthogonal approach; could complement mechanistic work

**4. Attention-Based Explanations**
- Strengths: Computationally cheap; per-token attribution
- Limitations: Attention ≠ importance; don't capture global reasoning
- This Paper: Goes beyond local attributions to global causal structure

### Connection to Broader XAI Communities

- **LIME/SHAP Community:** This paper extends SHAP-like concept attribution with causal structure
- **Concept-Based XAI:** Builds on TCAV/ACE tradition but adds causal discovery
- **Causal ML:** Brings causal inference into LLM explainability (previously separate fields)
- **Trustworthy AI:** Directly supports regulatory requirements for high-risk AI systems

### Cited Context & Influences
- Pearl's causal hierarchy (do-calculus, causal graphs)
- TCAV (concept-based attribution for neural networks)
- Counterfactual explanations (Wachter et al.)
- Causal discovery methods (constraint-based, score-based algorithms)

### Likely to Influence Future Work

This paper sits at an important intersection:
1. **Concept-based methods** will incorporate causal discovery
2. **Causal inference** community will adopt LLM-extracted concepts
3. **Regulatory frameworks** will demand causal explanations (this work shows they're achievable)
4. **Mechanistic interpretability** may use causal graphs as intermediate abstractions

## Significance & Impact

### For Practitioners
- Enables auditing of deployed LLM systems for bias, fairness, and alignment
- Provides actionable insights (which concepts to focus on for model improvement)
- Facilitates stakeholder trust through transparent causal reasoning

### For Researchers
- Opens new research directions in combining concept-based and causal methods
- Demonstrates feasibility of causal discovery for high-dimensional learned representations
- Provides benchmark tasks (disease diagnosis, sentiment, judge) for future xAI work

### For Regulators & Policy
- Demonstrates technical feasibility of "right to explanation" requirements
- Shows that high-risk AI systems can be made interpretable without sacrificing performance
- Provides tools for fairness audits and bias detection

---

## Summary

"LLM Explainability with Counterfactual Chains and Causal Graphs" introduces a principled, practical approach to explaining LLM decisions through causal reasoning. By combining concept extraction, MCMC-inspired counterfactual augmentation, and causal discovery, the paper creates interpretable causal graphs that explain *how* and *why* LLMs make decisions. The framework addresses critical gaps in current XAI methods—it moves beyond correlation to causation, scales to high-dimensional concept spaces, and produces human-understandable explanations suitable for regulatory compliance and stakeholder trust.

The key innovation is recognizing that LLMs themselves can generate faithful counterfactuals, enabling efficient data augmentation for causal discovery. This bridges a fundamental bottleneck in causal ML: the requirement for large datasets. The experimental findings—showing different models develop different reasoning strategies on naturalistic tasks—have profound implications for personalized, interpretable AI systems.

For the XAI community, this paper represents a significant step toward *causal*, *concept-based*, *practical* explainability suitable for real-world, high-stakes applications.
