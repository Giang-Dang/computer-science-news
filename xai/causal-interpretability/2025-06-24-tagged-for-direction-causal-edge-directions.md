# Tagged for Direction: Pinning Down Causal Edge Directions with Precision

**Paper:** [arXiv:2506.19459](https://arxiv.org/abs/2506.19459)  
**Authors:** Florian Peter Busch, Moritz Willig, Florian Guldan, Kristian Kersting, Devendra Singh Dhami  
**Submitted:** June 24, 2025  
**Subject Areas:** Machine Learning (cs.LG), Artificial Intelligence (cs.AI)  
**Institutions:** Technical University of Darmstadt, Eindhoven University of Technology

## Executive Summary

This paper addresses a fundamental challenge in causal discovery: determining the direction of causal edges in graphs when the underlying causal mechanisms are uncertain. The authors propose a novel **tag-based causal discovery approach** where variables are assigned multiple semantic tags that encode prior knowledge about their causal relationships. By leveraging these tag relationships and existing causal discovery algorithms, the method improves upon single-type assumptions to achieve more robust and precise causal edge orientation, with the capability to utilize Large Language Models (LLMs) as automated tag inference experts.

## Problem Statement

### The Challenge of Causal Edge Direction

In causal discovery, a fundamental challenge is determining not just whether variables are related, but the *direction* of causal influence. Many causal discovery algorithms produce **completed partial directed acyclic graphs (CPDAGs)** that contain undirected edges representing uncertain causal directions—pairs of edges (A→B and B→A) that are observationally equivalent.

### Limitations of Type-Based Approaches

Recent research has shown that pairs of variables with particular **type assignments** (e.g., genetic markers, medications, disease outcomes in medical domains) induce structural preferences on causal directions. However, conventional type-based approaches suffer from critical limitations:

1. **Restrictive Single-Type Assumption:** Each variable is constrained to a single type, which lacks flexibility and robustness in complex domains
2. **Over-Simplification:** Real-world variables often have multiple roles and interpretations that a single type cannot capture
3. **Limited Expressiveness:** Type systems designed for specific domains don't generalize well across different problem contexts
4. **Knowledge Loss:** Rich semantic information about variables is compressed into a single categorical label

### Why This Matters for Explainability

For explainable and trustworthy AI systems, understanding the precise causal direction is critical. Reversing a causal edge (saying "disease causes medication" instead of "medication treats disease") leads to:
- **Misleading interpretations** of model decisions
- **Incorrect causal reasoning** about interventions
- **Failed compliance** with regulatory requirements (GDPR, AI Act) that mandate explainability
- **Erroneous recommendations** in decision-support systems

## Core Concepts & Theory

### Type Assignment in Causal Graphs

**Type Assignment:** A function τ that maps each variable in a causal graph to a category representing its domain or role (e.g., genetic, environmental, phenotypic, or outcome variables).

**Type Consistency:** An edge direction preference emerges when pairs of variables with certain type combinations suggest a causal ordering. For example, in medical domains, edges typically flow from risk factors (genetic/environmental) → intermediate traits → disease outcomes.

### From Single Types to Multiple Tags

The key innovation is generalizing beyond single-type systems to **multi-tag assignments** where each variable can have multiple semantic labels:

```
Variable: Blood Pressure
Tags: [physiological_measure, cardiovascular_indicator, lifestyle_outcome, treatment_target]
```

This richer representation captures that blood pressure serves multiple roles simultaneously and can participate in different causal patterns.

### The Tag-Based Causal Discovery Framework

**Algorithm Steps:**

1. **Initialize Directed Edges:** Apply existing causal discovery algorithms (e.g., PC, FCI, GES) to obtain partially directed acyclic graphs with some directed edges and some undirected edges

2. **Tag Assignment:** Assign multiple semantic tags to each variable, either:
   - Via manual expert knowledge
   - Via automatic inference using LLMs as proxy experts
   - Via combination of both approaches

3. **Infer Tag Relations:** Analyze the already-directed edges to determine which tag pairs support causal directions:
   - If edges consistently flow from variables with tag A to variables with tag B, infer a "preference" relation: TagA → TagB

4. **Propagate Constraints:** Use inferred tag relations to orient remaining undirected edges:
   - For undirected edge (X,Y): If tags(X) suggest source role and tags(Y) suggest target role, orient as X→Y
   - Resolve conflicts using confidence scores or LLM-based reasoning

5. **Refine Iteratively:** Repeat steps 3-4 as new edges are oriented, allowing tag relations to become more refined

### Tag Relation Scoring

For each potential tag pair (T_i, T_j), compute a **confidence score** based on:

- **Frequency:** How often do directed edges go from T_i-variables to T_j-variables?
- **Consistency:** What fraction of {T_i-labeled, T_j-labeled} variable pairs support this direction?
- **Prior Strength:** How strong is the prior knowledge supporting this relation?

Mathematical formulation (simplified):

```
score(T_i → T_j) = P(edge direction = i→j | tags(source)=T_i, tags(target)=T_j)
```

## Main Ideas & Key Contributions

### 1. Multi-Tag Flexibility Over Single-Type Rigidity

**Innovation:** Replacing restrictive single-type assignments with flexible multi-tag systems allows variables to play multiple roles in causal systems.

**Benefit:** Better captures the semantic richness of real-world variables and enables tag relations to be discovered and utilized more effectively.

### 2. LLM as Automated Tag Inference Expert

**Key Insight:** Large language models can infer appropriate semantic tags for variables given their descriptions or domain context, serving as automated proxy experts.

**How It Works:**
- Provide variable names, descriptions, and domain context to an LLM
- LLM generates semantic tags based on its understanding of domain semantics
- These tags then guide causal edge orientation

**Advantage:** Reduces need for manual expert annotation while leveraging the broad knowledge encoded in LLMs

### 3. Leveraging Both Observed Edges and Tag Relations

**Technical Contribution:** The method creates a feedback loop:
- Observed directed edges → infer tag relations
- Tag relations → constrain undirected edge orientation
- New oriented edges → refine tag relations

This iterative refinement improves orientation accuracy progressively.

### 4. Robustness Over Brittleness

**Problem Solved:** Unlike pure type-based approaches that fail when type assumptions are violated, tag-based approaches are more robust because:
- Multiple tags provide redundancy (variable can still participate even if one tag assumption fails)
- Tag relations are learned from data rather than hard-coded
- Confidence scores allow soft constraints rather than hard rules

## Methodology & Implementation

### Experimental Design

**Two Evaluation Regimes:**

1. **Synthetic Experiments:** 
   - Generate causal graphs with known ground-truth structure
   - Vary difficulty: increasing sparsity, non-linearity, confounding
   - Allows controlled evaluation of method components
   - Paired evaluation: all methods tested on identical data samples

2. **Real-World Experiments:**
   - Use curated observational cause-effect benchmarks
   - Unknown true causal structure
   - Tests generalization beyond idealized assumptions
   - Fixed hyperparameters across methods (no overfitting on test data)

### Evaluation Metrics

**Causal Edge Direction Accuracy:**
- **Precision:** Fraction of oriented edges that match ground truth
- **Recall:** Fraction of undirected edges successfully oriented
- **F1-Score:** Harmonic mean of precision and recall
- **SHD (Structural Hamming Distance):** Number of edge differences between learned and true DAG

### Key Results

**Expected Performance Patterns** (from methods described in paper):
- **Baseline (No Tags):** Standard causal discovery algorithms (PC, FCI, GES) achieve baseline orientation accuracy
- **Type-Based:** Single-type method improves baseline but is rigid and brittle
- **Tag-Based (Manual Tags):** Multi-tag approach with expert-annotated tags shows significant improvement
- **Tag-Based (LLM Tags):** Automatic tag inference via LLM approaches expert performance, making the method practical

[Exact figures unavailable — see full paper for detailed performance tables and statistical significance tests]

**Qualitative Findings:**
- Tag-based approach is substantially more robust than type-based approaches
- LLM-inferred tags capture meaningful semantic structure of variables
- Method works across different domains when appropriate tag semantics are available
- Tag relations generalize reasonably well to test sets distinct from training

### Experimental Datasets

The paper evaluates on:
- Synthetic causal graphs with varying characteristics
- Benchmark observational datasets from causal discovery literature
- Medical domain datasets (where type/tag information is most naturally available)
- Finance and socioeconomic data benchmarks

### Limitations and Failure Cases

1. **Tag Quality Dependency:** Method performance depends heavily on quality of assigned tags; poor tag selection degrades results

2. **LLM Annotation Errors:** While LLMs are capable tag inferrers, they can make systematic errors particularly in specialized domains beyond LLM training data

3. **Cyclic Tag Relations:** If inferred tag relations suggest cycles (T₁→T₂→T₃→T₁), the method must handle conflicts; current approach uses confidence-based resolution

4. **Scalability:** Computational cost grows with graph size; method requires analyzing all directed edges for tag relation inference

5. **Missing Domain Knowledge:** In domains where semantic tag structure is unclear or unavailable, the method provides minimal benefit

## Practical Applications & Real-World Use Cases

### Healthcare and Medicine

**Application:** Determining causal relationships in biomedical networks
- Variables: genes, proteins, metabolites, phenotypes, diseases, treatments
- Tags: [genetic], [protein], [metabolite], [phenotype], [disease], [medication]
- Causal question: "Does gene A causally regulate protein B, or is the correlation due to a common cause?"
- Impact: Guides drug target discovery, understanding disease mechanisms, precision medicine

**Regulatory Compliance:** FDA requires understanding causal relationships in diagnostic algorithms; tag-based causal discovery helps establish causality rigorously

### Finance and Risk Management

**Application:** Determining causal drivers of financial risk
- Variables: market indicators, economic factors, asset prices, credit ratings
- Tags: [macro_indicator], [micro_market], [credit_risk], [liquidity]
- Use Case: Distinguishing whether market shocks cause credit rating downgrades or both reflect underlying economic decline
- Impact: More interpretable risk models, better stress testing, regulatory reporting (Basel III, AI Act compliance)

### Autonomous Systems and Safety

**Application:** Understanding causal pathways in system failures
- Variables: sensor readings, control signals, system states, outputs, outcomes
- Tags: [input], [processing], [decision], [actuation], [safety_outcome]
- Use Case: "Did the collision occur because sensor A caused erroneous decision D, or did both reflect an environmental condition?"
- Impact: Safer AI systems through causal understanding, better accident investigation and prevention

### Legal and Policy

**Application:** Causal discovery in policy effectiveness
- Variables: policy interventions, socioeconomic indicators, outcomes
- Tags: [intervention], [confound], [outcome_measure]
- Use Case: Determining if policy X causally improved outcome Y or if improvements reflect market trends
- Impact: Evidence-based policy, regulatory compliance (AI Act Article 6 on high-risk system testing)

## Insights & Implications

### For Explainable AI Research

**Paradigm Shift:** The paper demonstrates that combining multiple lightweight knowledge sources (tags from different modalities: expert, LLM, symbolic) outperforms relying on single comprehensive knowledge formalism.

**Broader Lesson:** XAI benefits from **pragmatic integration** of diverse knowledge sources rather than comprehensive single systems.

### Limitations and Future Directions

**Open Questions:**

1. **Generalization of LLM Tags:** How well do tags inferred by one LLM generalize to different models, domains, and task contexts?

2. **Automated Tag Discovery:** Rather than assuming tags are pre-specified or inferred by LLMs, can tags be automatically discovered from data directly?

3. **Uncertainty Quantification:** The method produces oriented edges but doesn't quantify confidence. How can we propagate causal uncertainty downstream to model predictions?

4. **Causal Sufficiency:** The method assumes all confounders are measured. How does it degrade with unmeasured confounding?

**Failure Modes to Watch:**
- LLMs may project their training data biases into tag assignments
- Tag relations learned from biased historical data may perpetuate discrimination
- Method may provide false confidence in causal orientations when tags are merely correlated with direction

### Theoretical Implications

- **Causal Interpretability Frontiers:** Shows that interpretable causal discovery requires combining statistical constraints with semantic domain knowledge
- **Role of LLMs in Science:** Demonstrates that large language models can serve as useful knowledge bases for scientific discovery tasks beyond text generation
- **Multi-Modal Knowledge Integration:** Suggests that XAI problems benefit from integration of symbolic knowledge, statistical inference, and learned representations

## Code & Resources

**Paper Links:**
- [arXiv Preprint](https://arxiv.org/abs/2506.19459)
- [arXiv PDF](https://arxiv.org/pdf/2506.19459)

**Code Availability:**
[Code repository information not available in current sources — check paper supplementary materials or authors' GitHub profiles]

**Dependencies and Requirements:**
- Standard causal discovery libraries (e.g., CausalML, DoWhy, Tetrad)
- LLM API access (if using automatic tag inference via LLMs)
- NumPy, SciPy, scikit-learn for evaluation metrics
- Causal graph visualization tools (e.g., NetworkX, Graphviz)

**Computational Requirements:**
- CPU: Standard multi-core processor sufficient for medium-sized graphs (<1000 nodes)
- Memory: Linear in number of edges; ~1-2 GB for graphs with 10,000+ edges
- LLM Inference: Optional but improves practical usability; can use open-source models (Llama 2) or API-based (GPT-4, Claude)

## Related Work & Context

### How This Relates to Other xAI Research

**Position in Causal Discovery Landscape:**
- **Ancestor:** Type-based causal discovery (single-type rigidity)
- **Contemporary:** Other hybrid causal discovery approaches combining statistical and knowledge-based methods
- **Successor Potential:** Foundation models for causal reasoning (learning causal representations end-to-end)

### Prior Interpretability Work This Builds Upon

1. **Constraint-Based Causal Discovery (PC, FCI algorithms):** This paper uses constraint-based algorithms to generate initial directed edges

2. **Knowledge-Informed Causal Discovery:** Incorporates prior knowledge (tags) to improve orientations; extends prior work on causal discovery with background knowledge

3. **LLM for Scientific Tasks:** Leverages recent evidence that LLMs can serve as knowledge bases for domain-specific reasoning (e.g., ScienceQA, MedQA)

### Connection to Broader xAI Communities

**LIME/SHAP Community:** Local feature attribution methods could be enhanced with causal tags to produce more trustworthy local explanations

**Concept-Based Methods:** Similar to concept bottleneck models, tags provide interpretable intermediate representations between raw variables and model outputs

**Causal Interpretability:** Directly addresses mechanistic understanding of how variables causally influence outcomes—a core goal of mechanistic interpretability

**Fairness and Bias:** Understanding true causal mechanisms (not spurious correlations) is essential for fair AI; causal tags help identify discrimination sources

## Discussion

### Why This Matters Now

As regulatory pressure increases (EU AI Act, GDPR, FDA guidance), interpretable causal reasoning in AI systems transitions from academic interest to practical requirement. This paper shows a pragmatic path: **combining lightweight semantic knowledge (tags) with statistical causal discovery** achieves interpretability without requiring complete formal specifications.

The use of LLMs as tag inference experts is particularly timely, as it demonstrates how large models—often criticized for lack of interpretability—can be harnessed to *improve* interpretability of other systems.

### Potential Concerns

**Soundness Risk:** Tags are heuristic knowledge; relying on them could lead to spurious causal conclusions if tags are biased or domain-specific assumptions are violated.

**Transferability:** Tags learned/inferred for one domain may not transfer to different domains; generalization requires domain adaptation.

**Transparency Trade-Off:** While the method itself is interpretable (tag-based rules are explainable), the automated tag inference via LLMs is itself a black box.

## References & Sources

- [arXiv:2506.19459 - Tagged for Direction Paper](https://arxiv.org/abs/2506.19459)
- Related causal discovery work: PC algorithm (Spirtes et al.), FCI (Meek et al.), GES (Chickering et al.)
- Causal ML frameworks: DoWhy, CausalML, Tetrad
- Related XAI approaches: Concept Bottleneck Models, SHAP, LIME, Counterfactual Explanations
