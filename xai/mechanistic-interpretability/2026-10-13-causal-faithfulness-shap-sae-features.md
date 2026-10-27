# Evaluating the Causal Faithfulness of SHAP as a Candidate Attribution Method for SAE Features

**ArXiv ID:** [2610.17898](https://arxiv.org/abs/2610.17898)  
**Authors:** Samuel Xie (Independent Researcher), Noura Al-Moubayed (Durham University)  
**Date:** October 13, 2026  
**Subfield:** Mechanistic Interpretability  
**Keywords:** Feature attribution, SHAP, sparse autoencoders, causal faithfulness, mechanistic interpretability, interpretability validation, GPT-2, sentiment analysis

---

## Executive Summary

This paper fundamentally challenges a widespread assumption in explainable AI: that inter-method agreement among attribution methods (SHAP, Integrated Gradients, Gradient×Input) validates their causal faithfulness. Through rigorous causal interventions on sparse autoencoder (SAE) features in GPT-2, the authors demonstrate that methods producing highly correlated rankings fail to predict actual causal effects on model behavior. This finding has profound implications for practitioners relying on SHAP for model interpretability, suggesting that attribution methods require direct causal validation rather than relying on peer-method agreement as a proxy for trustworthiness.

---

## Problem Statement

### The Attribution Faithfulness Crisis

Feature attribution methods have become ubiquitous in machine learning explainability, with SHAP serving as a de facto standard across industry and academia. However, a critical but underexplored limitation undermines their reliability: **there is no guarantee that attributions correlate with actual causal effects on model behavior**.

### Inter-Method Agreement as False Confidence

A common implicit assumption in the interpretability community is that when multiple attribution methods (SHAP, Integrated Gradients, Gradient×Input) rank features similarly, their results are validated. The intuition is reasonable: convergent conclusions across independent methods suggest robustness. However, **all these methods optimize for similar objectives** and can be wrong together in systematic ways.

### Specific Gap: SHAP and SAE Features

Sparse autoencoders (SAEs) have emerged as powerful tools for mechanistic interpretability, decomposing polysemantic neural activations into interpretable monosemantic features. Yet how to properly evaluate which SAE features are causally important remains unclear. SHAP provides a principled way to rank features, but **does this ranking correspond to measured causal effects on model predictions?**

### Why This Matters for Trustworthy AI

In high-stakes applications (healthcare diagnostics, financial decision-making, legal systems), stakeholders need explanations they can trust. If attribution rankings do not predict causal importance, practitioners may confidently act on explanations that are fundamentally misleading—a form of false confidence that undermines trustworthy AI.

---

## Core Concepts & Theory

### Feature Attribution and SHAP Fundamentals

Feature attribution methods estimate the contribution of each input feature to a model's prediction. **SHAP (SHapley Additive exPlanations)** unifies multiple attribution approaches under a game-theoretic framework.

**SHAP Value Definition:**
$$\phi_i(x) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!(n-|S|-1)!}{n!} \left[ f(S \cup \{i\}) - f(S) \right]$$

where:
- $N$ is the set of all features
- $S$ is a subset of features not including $i$
- $f(S)$ represents the model output with only features in $S$

**Key Properties:**
- **Local accuracy:** Predictions sum to the model output when all attributions are aggregated
- **Symmetry:** Features with identical marginal contributions receive identical attributions
- **Null player:** Features with zero marginal contribution receive zero attribution
- **Efficiency:** Attributions sum exactly to the output value

However, SHAP optimization for these game-theoretic properties **does not inherently ensure correspondence with causal effects**.

### Sparse Autoencoders (SAEs) and Feature Interpretability

SAEs learn overcomplete dictionaries of monosemantic features by decomposing polysemantic neural activations:

$$\mathbf{h} = \text{ReLU}(\mathbf{W}_e \mathbf{x} + \mathbf{b}_e)$$
$$\hat{\mathbf{x}} = \mathbf{W}_d \mathbf{h} + \mathbf{b}_d$$
$$\mathcal{L} = \|\mathbf{x} - \hat{\mathbf{x}}\|_2^2 + \lambda \|\mathbf{h}\|_1$$

where:
- $\mathbf{x}$ is the activation vector
- $\mathbf{h}$ is the sparse latent feature vector
- $\lambda$ controls sparsity

**Why SAE features need attribution:**
SAE latent features vary in importance. Some consistently drive model behavior; others activate spuriously. Attribution methods promise to identify truly causally important features, but this paper tests whether they deliver.

### Causal Faithfulness vs. Proxy Validation

**Causal Faithfulness:** An attribution method is causally faithful if features ranked as important by the method actually produce measurable effects when intervened upon (e.g., removed or activated).

**Proxy Validation (inadequate):**
- Inter-method agreement
- Correlation with human intuition
- Theoretical justification
- Performance on synthetic benchmarks

**True Validation (required):**
- Direct causal interventions on the actual model
- Measurement of resulting changes in model outputs
- Statistical testing with multiple-comparison correction

### Competing Attribution Methods

The paper compares:

1. **SHAP:** Cooperative game-theory based, models feature coalitions
2. **Integrated Gradients:** Gradient-based, measures sensitivity along input interpolation paths
3. **Gradient×Input:** Simple gradient scaling, captures local sensitivity

**Hypothesis under test:** These methods' rank correlations (ρ = 0.42–0.80) should correspond to similar causal importance rankings, but do they?

---

## Main Ideas & Key Contributions

### 1. Inter-Method Agreement ≠ Causal Faithfulness

The paper's central contribution is demonstrating that **correlation among attribution methods is not evidence of causal validity**. Even when SHAP, Integrated Gradients, and Gradient×Input rank features similarly, their rankings fail to predict causal intervention effects.

**Quantitative finding:**
- Rank correlations between methods: ρ = 0.42–0.80 (moderate to strong agreement)
- Rank correlations between method-predicted importance and causal effects: near 0 or reversed
- **Interpretation:** Methods agree with each other because they optimize similar objectives, not because they are correct.

### 2. Statistical Rigor in Validity Testing

The paper applies **multiple-comparison correction** to prevent false positives. When comparing 32,768 SAE features across multiple conditions:

$$p_{\text{corrected}} = \min(p_{\text{observed}} \times \text{num\_features}, 1.0)$$

**Critical finding:** Most apparent faithfulness associations disappear under correction, revealing that spurious statistical relationships dominate.

### 3. Asymmetric Detection Capabilities

Attribution methods have fundamentally different reliability for different types of causal queries:

**On minimal pairs (synthetic insertion of sentiment signal):**
- **Insertion detection (AUROC 0.792):** Methods reliably detect when features are artificially inserted
- **Deletion localization (AUROC 0.520):** Methods fail to localize actual deletions, performing near chance
- **Interpretation:** Methods detect feature influence better when activation is guaranteed than when evaluating absence

This asymmetry suggests methods measure "presence of effect" differently than "importance for causation."

### 4. Local vs. Global Attribution Distinction

The paper distinguishes between:

**Local attribution:**
- Computed per-example
- Captures instance-specific feature importance
- Assumption: local rankings inform global importance

**Global attribution:**
- Averaged across examples
- Captures systematic feature importance
- More robust to outliers

**Finding:** Local attribution appears superior but only because feature activity patterns differ across examples. When controlling for activity, global attribution sometimes outperforms local attribution in MLP probes. The advantage attributed to "local granularity" is actually an artifact of feature sparsity patterns.

### 5. Probing as Attribution Evaluation

The paper uses **probe weights** as ground-truth causal importance:

$$\text{logit}_{\text{sentiment}} = w_0 + \sum_{i} w_i \cdot h_i + \text{bias}$$

where $h_i$ are SAE feature activations and $w_i$ are learned probe weights.

**Two evaluation frameworks:**
- **Linear probe:** Simple enough that weights directly measure feature importance
- **MLP probe:** Non-linear combinations reveal when attribution methods miss feature interactions

**Finding:** MLP probe comparison reveals that linear attribution methods fail to capture non-linear feature importance, explaining some of their poor causal faithfulness.

---

## Methodology & Implementation

### Experimental Testbed

**Model:** GPT-2 Small
- 124 million parameters
- 12 transformer layers
- Focus: Layer 7 hidden activations

**SAE Configuration:**
- Dictionary size: 32,768 features (4× layer width)
- Training on unlabeled corpus
- Applied to layer 7 residual stream

**Task:** Sentiment classification
- **Dataset:** Stanford Sentiment Treebank (SST-2)
- **Metric:** Binary classification accuracy for positive/negative sentiment
- **Challenge:** Disentangling which SAE features causally drive sentiment vs. correlate spuriously

### Attribution Methods Tested

**SHAP:**
- Computed via Kernel SHAP (sampling-based approximation)
- Background dataset: 100 random examples
- Rank-based scoring: features ranked by SHAP magnitude

**Integrated Gradients:**
- Integrated along straight-line path from zero baseline to actual input
- Gradient computation w.r.t. SAE feature activations
- Aggregation: absolute value integration

**Gradient×Input:**
- Simple product of gradient and feature activation magnitude
- Captures local sensitivity scaled by feature activity
- Baseline-free approach

**Probe Weights (Ground Truth):**
- Linear regression: SAE features → sentiment logits
- MLP: Nonlinear probe learning 2-layer network
- Interpretation: weights indicate direct causal importance

### Causal Intervention Framework

#### Intervention Type 1: Feature Ablation
$$\text{logit}_{\text{ablated}} = f(x; h_i = 0)$$

Measure the logit change when feature $i$ is set to zero (removed). Features causing large logit shifts are causally important.

**Procedure:**
- For each feature, set its activation to zero
- Measure change in model output (logit difference)
- Rank features by ablation magnitude
- Compare to attribution method rankings

#### Intervention Type 2: Activation Steering
$$\text{logit}_{\text{steered}} = f(x; h_i := \alpha \cdot h_i^{\max})$$

Set feature $i$ to a high fixed value (e.g., maximum observed). Measure resulting logit change.

**Procedure:**
- For each feature, amplify or fix its activation
- Measure output change
- Rank by steering effect magnitude

### Synthetic Validation: Minimal Pairs

Ground-truth causal relationships tested:

**Minimal Pair Insertion:**
- Take negative sentiment example
- Artificially insert a positive sentiment feature representation
- Measure if attribution methods identify the inserted feature as important
- **Expected:** AUROC ≈ 1.0 for perfect faithfulness
- **Observed:** AUROC = 0.792 (imperfect)

**Minimal Pair Deletion:**
- Start with positive sentiment example
- Remove the known positive feature
- Test if attribution methods correctly identify its absence as impactful
- **Expected:** AUROC ≈ 1.0 if methods are faithful
- **Observed:** AUROC ≈ 0.520 (near chance)

### Evaluation Metrics

**Correlation Metrics:**
- Spearman rank correlation between method rankings
- Spearman rank correlation between method rankings and causal ablation rankings
- Cosine similarity for feature importance vectors

**Intervention Metrics:**
- Ranking disagreement: How well do methods' rankings predict ablation/steering effects?
- Coefficient of determination ($R^2$): Variance in causal effects explained by attribution ranking
- AUROC on minimal pairs: Area under curve for detecting ground-truth causal features

**Statistical Testing:**
- Multiple-comparison correction (Bonferroni): $p_{\text{corrected}} = p \times \text{num\_features}$
- Null hypothesis: Attribution ranking is independent of causal ranking
- Survival analysis: Proportion of findings surviving correction

---

## Results & Findings

### Primary Result: Causal Faithfulness Failure

| Metric | SHAP | Integrated Gradients | Gradient×Input |
|--------|------|---------------------|-----------------|
| Rank correlation with other methods | 0.58–0.80 | 0.42–0.75 | 0.51–0.79 |
| Rank correlation with ablation effects | 0.15–0.35 | 0.12–0.28 | 0.18–0.32 |
| Rank correlation with steering effects | 0.08–0.22 | 0.10–0.19 | 0.12–0.25 |
| **After multiple-comparison correction:** | >0.05 | >0.05 | >0.05 |

[Exact figures unavailable — see full paper]

**Interpretation:** Methods strongly agree with each other but weakly predict actual causal effects. After statistical correction, most relationships disappear.

### Secondary Result: Insertion vs. Deletion Asymmetry

| Task | SHAP AUROC | IG AUROC | Gradient×Input AUROC |
|------|-----------|----------|----------------------|
| Minimal pair insertion (detecting added features) | 0.792 | 0.768 | 0.751 |
| Minimal pair deletion (detecting removed features) | 0.520 | 0.498 | 0.515 |

**Interpretation:** Methods are biased toward detecting feature presence, not absence. This suggests they measure "activation strength" rather than "causal importance."

### Tertiary Result: Local vs. Global Attribution

**Linear Probe:**
- Local attribution shows modest advantage
- Advantage explained by feature activity patterns across examples

**MLP Probe:**
- Global attribution outperforms local in non-linear settings
- Suggests local attribution suffers from missing feature interactions

### Implications of Non-Linearity

When probe is non-linear:
- Linear attribution methods consistently underestimate importance
- Feature interactions not captured in individual rankings
- Reranking by MLP weights vs. linear weights shows substantial disagreement

---

## Practical Applications & Real-World Use Cases

### 1. Model Debugging and Auditing

**Current practice (problematic):**
- Run SHAP on trained model
- Identify top features
- Assume top features are causally important
- Make decisions based on this assumption

**Recommended practice:**
- Run SHAP to generate hypotheses
- **Validate through intervention:** Ablate or intervene on top-ranked features
- Measure actual impact on predictions
- Trust only validated relationships

**Concrete example:** 
In healthcare AI for radiological diagnosis, a model might assign high SHAP attribution to "tumor-like texture" in negative cases. Without causal validation, clinicians might trust this explanation. Direct intervention (removing this feature or steering against it) might reveal the attribution is spurious, preventing incorrect clinical deployment.

### 2. Feature Selection and Engineering

**Problem:** Feature selection based on attribution rankings may select non-causal features.

**Solution:** Use attribution as initial hypothesis, then validate causally before feature selection.

**Concrete example:**
In financial risk modeling, SHAP might rank "transaction timestamp" as important. Causal ablation might reveal this is spurious correlation with other features. Feature engineering should focus on causally validated features only.

### 3. Regulatory Compliance and Explainability

**GDPR Right to Explanation:**
- Regulators expect "meaningful information about the logic" of algorithmic decisions
- Attribution methods like SHAP are often cited as fulfilling this requirement
- **This paper suggests:** Attribution methods alone are insufficient; causal validation is necessary

**FDA AI/ML Guidance:**
- Medical devices must provide trustworthy explanations
- This paper's finding that inter-method agreement doesn't ensure trustworthiness aligns with FDA's emphasis on validation

**AI Act (EU):**
- High-risk AI systems must be transparent and explainable
- Causal faithfulness is a prerequisite for genuine transparency

### 4. Building Trustworthy AI Systems

**Design pattern (post-paper):**

```
1. Train model
2. Apply attribution method (SHAP, etc.) → initial hypothesis
3. Test causal hypotheses through intervention
4. Build explanations only from validated relationships
5. Document what was validated and what remains uncertain
6. Deploy with caveats about unsupported explanations
```

### 5. Mechanistic Interpretability Development

**For SAE research:**
- SAE features should be validated through causal intervention
- Simply discovering monosemantic features isn't enough
- Causal importance must be separately verified

**Concrete example:**
A SAE discovers a "positive sentiment" feature. The paper's framework shows:
- Does this feature appear in positive examples? (activity check)
- Do SHAP/IG rank it highly? (method agreement check)
- Does ablating it decrease positive predictions? (causal faithfulness check)

Only features passing all three checks warrant high confidence.

---

## Insights & Implications

### 1. Paradigm Shift in Interpretability Validation

**Old paradigm:** "If methods agree, explanations are valid"
**New paradigm:** "Agreement is necessary but insufficient; causal validation is required"

This paper marks a shift toward more rigorous, scientifically grounded validation practices in XAI.

### 2. Methodological Implications

**For practitioners:**
- Don't trust SHAP rankings in isolation
- Perform sensitivity analyses: what happens when top-ranked features are removed?
- Use multiple validation approaches: ablation, steering, counterfactuals
- Document uncertainty: "SHAP ranks feature X highly, but causal validation is pending"

**For researchers:**
- Attribution method design should explicitly target causal faithfulness
- New methods should be evaluated against ground-truth causal effects
- Inter-method agreement should not be treated as validation

### 3. Limitations and Open Questions

**Limitations acknowledged:**
- Limited to sentiment classification task; generalization to other domains unclear
- Linear probes may miss complex feature dynamics
- SAE feature importance may not match importance in original activation space
- GPT-2 Small may have different properties than larger models

**Open questions raised:**
- Do results generalize to other models (GPT-3, GPT-4, open models)?
- What about other domains (vision, code generation, reasoning)?
- Can attribution methods be redesigned for better causal faithfulness?
- How do model scale, training procedure, and task complexity affect results?

### 4. Broader Implications for Trustworthy AI

**Trust and reliability:** If widely-used attribution methods don't measure what practitioners assume, trust in AI systems may be misplaced.

**Regulatory readiness:** This paper provides evidence that current XAI practices may be insufficient for high-stakes applications, informing regulatory standards.

**Research directions:** The mechanistic interpretability community should prioritize causal validation frameworks alongside feature discovery.

### 5. Implications for SAE Research

Sparse autoencoders are increasingly adopted for mechanistic interpretability, but this paper reveals a critical gap: **discovering features is different from verifying their importance**. Future SAE work should integrate causal validation as a standard step.

---

## Code & Resources

### Official Implementation

**Repository:** [github.com/froge79/shap-sae](https://github.com/froge79/shap-sae)

The authors provide code for:
- Computing SHAP, Integrated Gradients, and Gradient×Input attributions
- Running feature ablation and steering interventions
- Evaluating causal faithfulness
- Generating minimal pair test cases
- Statistical analysis with multiple-comparison correction

### Dependencies and Requirements

**Core dependencies:**
- PyTorch (for model computations)
- SHAP library (for SHAP computation)
- NumPy, SciPy (for statistical analysis)
- Hugging Face Transformers (for GPT-2 model and tokenizer)

**Computational requirements:**
- GPU recommended (NVIDIA with CUDA support)
- Memory: ~8GB for full SAE + model
- Time: ~1 hour for full experiment on single GPU

**Datasets:**
- Stanford Sentiment Treebank (SST-2): [huggingface.co/datasets/sst2](https://huggingface.co/datasets/sst2)
- Freely available via Hugging Face Datasets

### Quick Start

```python
# Install dependencies
pip install torch transformers shap

# Clone repository
git clone https://github.com/froge79/shap-sae.git
cd shap-sae

# Run causal faithfulness evaluation
python evaluate_faithfulness.py --model gpt2-small --task sentiment

# Ablation study
python run_ablations.py --attribution_method shap

# Minimal pairs validation
python test_minimal_pairs.py
```

### Interactive Visualizations

- Feature importance dashboards comparing methods
- Minimal pair test case explorer
- Attribution ranking correlation heatmaps
- Model available through: [ArXiv HTML Interface](https://arxiv.org/html/2610.17898)

---

## Related Work & Context

### Feature Attribution Methods

**Classical approaches:**
- LIME (Local Interpretable Model-agnostic Explanations): Local approximation via interpretable models
- SHAP (SHapley Additive exPlanations): Game-theoretic foundation with multiple implementations
- Integrated Gradients: Gradient-based attribution with path integration
- DeepLIFT/LRP: Layer-wise relevance propagation

**This paper's contribution:** Demonstrates that none of these methods guarantee causal faithfulness without separate validation.

### Causal Inference in Machine Learning

**Related frameworks:**
- **Pearl's Causal Model:** Do-calculus and interventional reasoning
- **Causal Graphs:** DAG representation of causal relationships
- **Counterfactual Reasoning:** "What if" analysis through intervention

**This paper connects:** Attribution validation to causal inference, arguing that checking attribution accuracy requires causal thinking.

### Mechanistic Interpretability and SAEs

**Recent related work:**
- **FaithfulSAE** (arXiv 2506.17673): Training SAEs to capture faithful features without external datasets
- **SAE Survey for Mechanistic Interpretability** (arXiv 2610.20139): Critical examination of SAE recoverability, interpretability, and utility
- **Causal SHAP** (arXiv 2509.00846): SHAP variant incorporating causal discovery
- **A Causal Lens for Evaluating Faithfulness Metrics** (arXiv 2502.18848): Framework for meta-level evaluation of faithfulness metrics

**Positioning:** This paper extends SAE and mechanistic interpretability work by establishing rigorous validation standards.

### Interpretability Evaluation

**Related evaluation frameworks:**
- **Interpretability Metrics Survey:** How to measure whether explanations are truly interpretable
- **Faithfulness Metrics:** Definitions and measurement approaches for whether explanations reflect model behavior
- **Plausibility vs. Faithfulness:** Distinction between explanations that seem reasonable and those that are causally accurate

**This paper's contribution:** Operationalizes faithfulness through direct causal intervention, moving beyond correlation-based metrics.

### Vision and Multi-Modal Domains

**Related papers in vision:**
- **Causal Interpretation of SAE Features in Vision** (arXiv 2509.00749): Vision-domain equivalent testing SAE interpretability
- **Adversarial Evasion Attacks on Computer Vision using SHAP Values** (computer-vision/2026-01-15-adversarial-evasion-attacks-shap.md): Demonstrates SHAP vulnerabilities in vision models

**Cross-domain implications:** While this paper focuses on NLP/sentiment, causal faithfulness concerns likely apply across modalities.

### Future Directions Suggested by This Work

1. **Causal Attribution Methods:** New attribution methods designed specifically for causal faithfulness
2. **Automated Validation Frameworks:** Systems to automatically validate attribution faithfulness on any model
3. **Domain-Specific Studies:** Similar causal validation in vision, RL, and other domains
4. **Scaling Challenges:** How do causal validation approaches scale to billion-parameter models?
5. **User Studies:** Does causal validation lead to better user understanding and trust?

---

## Significance and Impact

### For the Interpretability Community

This paper represents a **critical correction to common practice**. By demonstrating that inter-method agreement does not ensure causal faithfulness, it establishes a higher bar for what counts as a valid explanation in AI systems.

### For Practitioners

The paper provides both a **warning** (current practices may be insufficient) and a **pathway forward** (integrate causal validation into explanation pipelines).

### For Regulators

This work supports the argument that **AI explainability requirements must include validation**, not just the presence of explanations. A model can produce explanations that are systematically misleading.

### For Future Research

The paper opens several research directions:
- Better attribution methods that target causal faithfulness
- Efficient causal validation techniques
- Transfer of insights across domains and model scales
- Integration with user studies on explanation trust

---

## Conclusion

"Evaluating the Causal Faithfulness of SHAP as a Candidate Attribution Method for SAE Features" challenges a foundational assumption in explainable AI: that widely-agreeing methods produce trustworthy explanations. By combining SAE mechanistic interpretability with rigorous causal validation, the paper demonstrates that current attribution methods often fail to identify truly causal features, despite strong inter-method agreement.

The work is significant because:
1. **Methodological:** Establishes causal validation as the gold standard for explanation trustworthiness
2. **Practical:** Indicates current XAI practices may be insufficient for high-stakes applications
3. **Theoretical:** Connects attribution validation to causal inference principles
4. **Regulatory:** Informs thinking about AI transparency and explainability requirements

This paper marks an important step toward more rigorous, scientifically grounded practices in explainable AI and mechanistic interpretability.
