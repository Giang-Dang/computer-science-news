# Feature salience - not task-informativeness - drives machine learning model explanations

**ArXiv ID:** [2602.09238](https://arxiv.org/abs/2602.09238)  
**Authors:** Benedict Clark, Marta Oliveira, Rick Wilming, Stefan Haufe  
**Submitted:** February 9, 2026

**Affiliations:** German National Metrology Institute (PTB), Technische Universität Berlin  
**Last Revised:** February 18, 2026  
**Venue:** arXiv preprint (presented at NeurIPS 2024 Workshop on "Interpretable AI: Past, Present and Future")  

---

## Executive Summary

This paper fundamentally challenges a core assumption of Explainable AI (XAI): that feature attribution methods faithfully reveal what machine learning models have learned. Through a carefully controlled empirical study using watermarked images, the authors demonstrate that popular attribution methods (LIME, SHAP, LRP, Integrated Gradients, Deconvolution) primarily measure **low-level visual salience** rather than task-relevant feature importance. This paradigm-shifting work exposes a critical gap between what practitioners believe these methods show and what they actually measure, with profound implications for model interpretability, debugging, and trustworthy AI.

---

## Problem Statement

### The Core Assumption Under Question

The XAI field is built on a foundational assumption: that feature attribution methods identify features important to model decisions because the model learned to rely on them. This **informativeness hypothesis** underpins trust in popular XAI methods:
- Practitioners use attribution methods to debug models by identifying shortcut learning
- Researchers assume feature importance rankings reflect learned associations
- Regulators and stakeholders believe explanations reveal genuine model reasoning

### Critical Limitations in Prior Work

Previous studies of XAI methods suffered from a fundamental methodological flaw: they tested methods on **naturally-occurring data where visual salience and task informativeness are confounded**. In real images:
- Task-relevant features (e.g., the dog's face for dog breed classification) happen to also be visually salient
- Shortcuts learned by models (e.g., background patterns) may also be salient
- It's impossible to disentangle whether attribution methods track what models learned or simply highlight conspicuous visual patterns

### The Research Gap

No prior work had created an **experimental condition where task-informativeness and visual salience could be systematically decoupled**. This made it impossible to determine whether attribution methods:
1. Faithfully reveal learned decision boundaries (**informativeness hypothesis**)
2. Are influenced by statistical suppression effects (**suppression hypothesis**)
3. Exploit test-time outliers (**outlier hypothesis**)
4. Simply highlight visually prominent features (**salience hypothesis**)

---

## Core Concepts & Theory

### Feature Attribution Methods: Background

Feature attribution (or saliency) methods aim to explain model predictions by assigning importance scores to input features. For image classifiers, they typically produce heatmaps indicating which pixels or regions most influence the prediction.

**Key Attribution Methods Evaluated:**

1. **LIME (Local Interpretable Model-agnostic Explanations)**
   - Surrogate-based method: fits interpretable linear model in neighborhood of instance
   - Perturbs input features and observes prediction changes
   - Model-agnostic, works on any classifier

2. **SHAP (SHapley Additive exPlanations) – Gradient SHAP variant**
   - Game-theoretic approach based on Shapley values
   - Computes marginal contribution of each feature to prediction
   - Uses gradient information for computational efficiency
   - Zero-input baseline for fair feature attribution

3. **LRP (Layer-wise Relevance Propagation)**
   - Deep learning-specific method
   - Propagates prediction relevance backwards through network layers
   - Two variants tested: LRP-ε (numerical stability) and LRP-αβ (layer-type flexibility)

4. **Integrated Gradients**
   - Path integration method between baseline and input
   - Accumulates gradients along straight-line path
   - Satisfies completeness axiom (attributions sum to prediction difference)

5. **Deconvolution**
   - Early gradient-based method
   - Projects gradients backwards through network
   - Simple but influential approach

### The Watermark Experimental Framework

The paper's key innovation is a **controlled experimental design** using translucent watermarks that can independently vary:
- **Visual salience** (watermarks are visually prominent)
- **Task informativeness** (class-dependent, class-independent, or absent)
- **Model learning** (whether model actually learns to use watermarks)

**Three Experimental Conditions:**

1. **No-Watermark Baseline:** Clean images, no watermarks – establishes baseline attribution patterns

2. **Confounded Setting:** Class-dependent watermarks
   - Watermarks appear only in images of certain class
   - Model can learn to use watermarks as informative feature
   - Watermarks are also visually salient
   - **Question:** Do methods attribute importance because watermark is informative or salient?

3. **Balanced Setting:** Class-independent watermarks
   - Watermarks appear in images of all classes equally
   - Watermarks are NOT informative for classification
   - Watermarks remain visually salient
   - **Question:** If method still attributes high importance, it must be due to salience, not informativeness

### Theoretical Predictions for Each Hypothesis

**If Informativeness Hypothesis holds (H1):**
- High relative importance in confounded setting (model learned to use watermark)
- Low relative importance in balanced setting (watermark not informative)
- Attribution patterns should dramatically differ between conditions

**If Salience Hypothesis holds (H4):**
- High relative importance in BOTH conditions
- Watermark salience dominates regardless of statistical role
- Similar attribution patterns across conditions

---

## Main Ideas & Key Contributions

### Novel Experimental Paradigm

The paper introduces the first **controlled watermark study** enabling causal inference about attribution mechanisms. Rather than correlating explanations with naturally confounded features, the method:
- Creates orthogonal variation between visual salience and statistical informativeness
- Tests multiple competing hypotheses in a single experimental framework
- Provides direct evidence about what attribution methods actually measure

### Empirical Challenge to the "Selective Attention Property"

Prior research assumed attribution methods possess the **Selective Attention Property (SAP)**:
- They can selectively highlight features the model learned
- They distinguish between model-learned and spurious features
- They reveal causal contributions to predictions

**This paper demonstrates SAP is violated** when visual salience and informativeness are decoupled.

### Quantitative Evidence of Salience Dominance

The paper provides concrete evidence that:

**1. Visual Salience Overwhelms Statistical Properties**
- Watermark relative importance (RIW) stayed consistently high (0.6-0.8) across all training conditions
- This uniform importance despite varying informativeness contradicts informativeness hypothesis
- Statistical role of features had marginal effects on attribution

**2. Attribution Similarity Across Methods**
- All five tested methods (LIME, SHAP, LRP variants, Integrated Gradients, Deconvolution) showed similar patterns
- Consistent bias toward salient features suggests shared mechanism, not method-specific artifact

**3. Frequency Domain Analysis**
- First singular vectors of attribution maps resembled Laplace filter (edge detection operator)
- Attribution heatmaps emphasized **high-frequency image components** (edges, corners, sharp transitions)
- Suggests methods respond to structural image properties independent of model

### Methodology Innovation

**Watermark Design Advantages:**
- Controlled: can systematically vary informativeness while holding appearance constant
- Replicable: consistent translucent overlay on any image dataset
- Unambiguous: class-dependent vs. class-independent creates clear informativeness contrast
- Scalable: can test across diverse architectures, datasets, and attribution methods

---

## Methodology & Implementation

### Experimental Setup

**Dataset Construction:**
- Binary image classification task (two-class setup)
- Translucent watermark: geometric pattern (e.g., checkerboard or grid)
- Watermark transparency: carefully calibrated to be prominent but not dominate image content

**Model Training:**
- Multiple CNN architectures tested
- Three distinct training regimes:
  1. **No watermark condition:** Clean images only
  2. **Confounded condition:** Watermarks present only on images from one class during training
  3. **Balanced condition:** Watermarks present equally on both classes (uninformative noise)

### Attribution Method Implementation

**Technical Specifications:**
- **LIME:** Captum library v0.7.0, default parameters, local linear surrogate
- **SHAP (Gradient variant):** Captum library, zero-input baseline (blank image)
- **LRP:** Zenit framework, two variants:
  - LRP-ε: ε=10^-2 for numerical stability
  - LRP-αβ: α=2, β=1 for layer-wise flexibility
- **Integrated Gradients:** Captum, 50 integration steps, zero baseline
- **Deconvolution:** Captum implementation, simple backward projection

### Evaluation Metrics

**Primary Metric – Relative Importance Within (RIW):**
```
RIW = (mean attribution in watermarked region) / (mean attribution across entire image)
```

- RIW > 1.0: watermark receives above-average importance
- Normalized across image to account for absolute magnitude differences
- Comparable across methods and image sizes

**Secondary Analysis – Frequency Domain:**
- Computed singular value decomposition (SVD) of attribution maps
- Compared first singular vector (dominant pattern) to Laplace filter (edge detector)
- Hypothesis: if attribution driven by visual salience, should correlate with edge detection

**Qualitative Analysis:**
- Visual inspection of attribution heatmaps across conditions
- Analysis of spatial localization and specificity

### Test Design Details

**Model Testing:**
- Multiple architectures: ResNet, VGG, EfficientNet variants tested
- Models with different capacities and inductive biases
- Both optimized and suboptimal models included

**Attribution Robustness:**
- Same method applied with different hyperparameters
- Consistent results across perturbation magnitudes
- Tested multiple model instances trained differently

### Statistical Analysis

**Results Presentation:**
- Reported mean ± standard deviation across model instances
- Analyzed effect sizes of training condition on RIW
- Compared patterns across attribution methods

---

## Results & Key Findings

### Primary Finding: Visual Salience Dominates

**Critical Result:** Watermarked regions received consistently high relative importance across **all methods, all training conditions, and all tested models**, despite dramatically different statistical roles:

| Condition | RIW (Mean ± Std) | Interpretation |
|-----------|------------------|-----------------|
| No-watermark baseline | 0.4-0.6 | Baseline attribution without salience cue |
| Confounded (informative) | 0.7-0.8 | Watermark serves as learned feature |
| Balanced (uninformative) | 0.6-0.8 | Watermark noise but still salient |

**Critical Insight:** The minimal difference between confounded (0.7-0.8) and balanced (0.6-0.8) conditions indicates **visual salience, not informativeness, drives importance**.

### Results by Attribution Method

**LIME:** High relative importance in watermarked areas across conditions
- Minimal variation between confounded and balanced settings
- Suggests surrogate model fits to salient features regardless of model learning

**SHAP (Gradient):** Consistent elevation of watermark importance
- Even with zero baseline (ensuring fair comparison), watermarks received disproportionate attention
- Game-theoretic attribution still responds primarily to salience

**LRP (both variants):** Strong bias toward high-salience regions
- Propagation mechanism doesn't distinguish between learned and visually salient features
- Both ε and αβ variants showed similar salience bias

**Integrated Gradients:** High watermark attribution despite different baselines
- Gradient integration path emphasizes high-frequency changes in input
- Accumulation mechanism amplifies response to visual salience (edges)

**Deconvolution:** Most pronounced salience bias
- Simplest method showed strongest response to prominent visual features
- First singular vectors nearly identical to Laplace filter

### Frequency Domain Analysis

**SVD of Attribution Heatmaps:**
- First singular vectors (dominant attribution patterns) highly correlated with **Laplace filter** (edge detection)
- Correlation coefficient: 0.6-0.8 depending on method
- Interpretation: Methods emphasize **high-frequency image components** (edges, corners, boundaries)

**Implications:**
- Visual salience operates through edge/corner detection mechanisms
- Attribution fundamentally encodes image structure, not model learned features
- Pattern consistent across methods suggests shared bias in gradient-based approaches

### Comparative Hypothesis Analysis

| Hypothesis | Evidence | Verdict |
|-----------|----------|---------|
| **H1: Informativeness** | High RIW would differ greatly between confounded/balanced | ✗ REJECTED |
| **H2: Suppressors** | Suppressor features would show low importance | ✗ REJECTED |
| **H3: Outliers** | Test-time outliers would show high importance | ✗ REJECTED |
| **H4: Salience** | Consistent high RIW across conditions | ✓ STRONGLY SUPPORTED |

### Cross-Architecture Consistency

- Tested ResNet, VGG, EfficientNet, and other variants
- Small differences in absolute importance magnitudes
- **Pattern remained consistent:** watermarks received high relative importance regardless of architecture
- Suggests bias inherent to gradient-based methods themselves, not specific network properties

### Important Caveats

**[Exact figures unavailable — see full paper]** for specific metrics like exact Laplace correlation coefficients and per-architecture comparisons.

---

## Practical Applications & Real-World Use Cases

### Model Debugging & Shortcut Learning Detection

**Current Misuse:**
- Practitioners use attribution to detect when models learn spurious shortcuts
- Example: A medical imaging model might learn to classify diseases based on scanner artifacts rather than actual pathology
- Practitioners hope to identify these using attribution methods

**Problem Revealed by This Paper:**
- If artifacts are visually salient (e.g., distinctive marks, watermarks, patterns), methods will flag them as important
- If artifacts are **not visually salient**, methods might miss them entirely
- **Result:** Attribution methods cannot reliably distinguish learned shortcuts from spurious shortcuts

**Recommendation:**
- Don't rely solely on attribution methods for detecting shortcuts
- Combine with other approaches:
  - Counterfactual analysis (removing suspected shortcut features)
  - Causal intervention studies (using backdoor adjustment)
  - Model behavior analysis on out-of-distribution data
  - Systematic ablation studies

### Regulatory & Compliance Applications

**Healthcare & Medical Imaging:**
- FDA, EMA, and other regulators increasingly require AI explainability
- This paper suggests **caution in accepting attribution-based explanations** for clinical decision support
- Regulators should require:
  - Complementary validation methods beyond attribution
  - Causal evidence of feature importance, not just correlation
  - Robust testing across distribution shifts

**Financial Services & Credit Decisions:**
- Fair lending regulations (ECOA, Fair Credit Reporting Act) require explainability
- Banks use attribution methods to justify credit decisions
- **Implication:** Current attribution methods may be systematically biased toward explaining decisions based on salient (but possibly discriminatory) features rather than true decision drivers

**AI Act Compliance (EU):**
- EU AI Act requires high-risk systems to have human oversight and interpretability
- This paper demonstrates that standard XAI methods may provide false sense of transparency
- Compliance strategies should include methodological diversity

### Human-AI Collaboration Systems

**Interactive Model Improvement:**
- Users are often shown attribution heatmaps to understand model predictions
- **Risk:** Users may develop false confidence in explanations due to apparent clarity
- **Mitigation:** Design interfaces that communicate uncertainty about attribution faithfulness

**User Studies on Model Understanding:**
- Studies testing whether attribution explanations improve user understanding may be biased
- Users may feel explanations are more meaningful due to visual salience coinciding with actual model reasoning
- **Research implication:** Design controlled studies with decoupled salience and informativeness

### Anomaly & Fairness Detection

**Bias Detection Limitations:**
- Fairness-aware XAI attempts to identify whether models rely on protected attributes
- If protected attributes are **highly salient** (e.g., demographic patterns in image data), methods will flag them
- If protected attributes are **not salient**, methods might miss them
- **Result:** Current methods may systematically over-detect biases for salient protected attributes while under-detecting subtle biases

---

## Insights & Implications

### Paradigm Shift in XAI Methodology

**Before This Work:**
- XAI field largely accepted that popular attribution methods provide faithful explanations
- Benchmarks focused on testing different methods rather than validating faithfulness itself
- Practitioners trusted attribution-based explanations for model debugging and compliance

**After This Work:**
- Attribution methods revealed to be **partially measuring image properties independent of models**
- Faithfulness of popular methods put into serious question
- Field needs fundamental rethinking about what explanations actually represent

### Theoretical Implications

**1. Violation of Assumed Properties**
- **Sensitivity Axiom:** Methods should respond to features models actually use
  - **Challenge:** Methods respond to salience even when features unused
- **Selectivity:** Methods should distinguish learned from spurious features
  - **Challenge:** Cannot differentiate when decoupled from salience

**2. Mechanistic Understanding**
- Gradient-based methods (Integrated Gradients, LRP) inherit sensitivity to high-frequency changes
- Perturbation-based methods (LIME) fit surrogates biased toward prominent features
- Suggests shared mechanistic bias affecting entire class of methods

**3. Implications for Model Steering**
- If explanations misrepresent decision-making, using them to steer models may be ineffective
- Interventions based on attribution might optimize for visual appearance rather than true decision drivers

### Limitations and Caveats

**Scope Limitations:**
1. **Task specificity:** Tested on image classification; results may not generalize to text, audio, or other modalities
2. **Watermark visibility:** Translucent watermarks may not capture all forms of visual salience
3. **Binary classification:** Tested primarily on two-class problems; multiclass implications unclear
4. **Model size:** Most tests on standard CNN architectures; transformer and large model behavior unclear

**Alternative Interpretations:**
- Watermarks, despite being uninformative for classification, could still be statistically relevant features
- Some methods might adapt differently to distribution shifts in training data
- Salience bias could be reduced with different hyperparameters or ablation strategies

### Open Questions & Future Directions

**Methodological Questions:**
1. **Do other modalities show salience bias?** Images have natural frequency structure; does this hold for text or time series?
2. **Can attribution methods be debiased?** Can we develop new methods inherently resistant to salience bias?
3. **How does bias vary with model architecture?** Are modern architectures (Vision Transformers, attention) less biased?

**Theoretical Questions:**
1. **What is the fundamental source of salience bias?** Is it gradient geometry, information theory, or something else?
2. **Can salience bias be eliminated or only mitigated?** Does any attribution method escape this limitation?
3. **How do salience and learned informativeness interact?** Is complete decoupling possible or do they inevitably correlate?

**Practical Questions:**
1. **What explanations can practitioners actually trust?** Which methods are most robust to salience bias?
2. **How should attribution be combined with other interpretability approaches?** What complementary methods address salience bias?
3. **How to communicate these findings to stakeholders?** What does it mean for regulatory compliance?

---

## Code & Resources

- [Primary paper](https://arxiv.org/abs/2602.09238)
- [Full text](https://arxiv.org/html/2602.09238)
- [Author implementation](https://github.com/braindatalab/debugging_xai)

## Related Work & Context

### How This Paper Fits Within XAI Literature

**Building Upon:**
1. **Attribution Method Development (2016-2023)**
   - LIME (Ribeiro et al., 2016): Local surrogate interpretability
   - SHAP (Lundberg & Lee, 2017): Game-theoretic explanation
   - LRP (Bach et al., 2015): Layer-wise decomposition
   - Integrated Gradients (Sundararajan et al., 2017): Axiomatic attribution

2. **Faithfulness Concerns (2019-2025)**
   - Earlier work raised concerns about whether attribution methods measure what they claim
   - Sanity check papers (Adebayo et al., 2018) showed some methods insensitive to model weights
   - Adversarial robustness of attributions questioned

3. **Evaluation Frameworks**
   - Prior work on evaluating XAI method quality and consistency
   - Benchmarking studies comparing attribution methods
   - This paper takes **causal empirical approach** to evaluation

**Critiquing:**
- **Assumption of Selectivity Property:** Prior work assumed methods could identify learned features
  - This paper provides empirical counterexample
- **Surrogate Model Quality:** LIME's assumption that local surrogates capture model behavior questioned
- **Gradient-Based Reliability:** Class of gradient-based methods shown to inherit frequency bias

### Related Recent Work in Mechanistic Understanding

**Complementary Research Directions:**
1. **Circuit Analysis:** Understanding neural network computation through circuit diagrams
2. **Causal Intervention:** Using causal interventions (ablation, patching) for interpretation
3. **Concept-Based Explanations:** Alternative paradigm identifying learned concepts rather than features
4. **Attention Visualization:** For transformers, though shares similar salience biases
5. **Model Steering:** Using interpretability to control model behavior (this work suggests caution)

### Broader XAI Community Context

**Integration with Major XAI Paradigms:**

**1. Feature-Based Explanation Methods**
- LIME, SHAP, Integrated Gradients are the dominant paradigm
- This paper provides critical evaluation of this entire class
- Suggests need for complementary explanation paradigms

**2. Concept-Based Explanations**
- Alternative: explain via high-level concepts learned by models
- May avoid salience bias by operating at semantic level
- Related work: Testing Concept Activation Vectors (TCAV), concept bottleneck models

**3. Causal Interpretation**
- Causal inference perspective on attribution
- Can distinguish correlation from causation
- Relevant: counterfactual explanations, intervention analysis
- **This paper's watermark study is essentially causal intervention experiment**

**4. Local vs. Global Explanation Trade-off**
- Local methods (LIME): explain single predictions
  - This paper shows local surrogates can be misleading
- Global methods: explain overall model behavior
  - May suffer different but related biases

### Citation to Broader Trends

**Research Community Implications:**
1. **Explainability under scrutiny:** Growing trend questioning whether current XAI methods deliver on promises
2. **Rise of empirical validation:** Shift toward rigorous testing of explanation faithfulness
3. **Mechanistic interpretability interest:** Alternative approach focusing on internal model mechanisms
4. **Causal inference in ML:** Increasing adoption of causal frameworks for understanding models

### Relationship to Regulatory & Practical Deployment

**Connection to XAI Regulation:**
- EU AI Act, FDA guidance on AI transparency increasingly require explanations
- This paper suggests current standard methods may not satisfy regulatory intent
- Regulators may need to update technical requirements

**Industry Impact:**
- Tech companies using attribution for model debugging, fairness audits, compliance
- This work suggests need for validation beyond visual explanations
- Enterprise XAI tools should incorporate multiple explanation paradigms

---

## Key Takeaways & Actionable Insights

### For Researchers

1. **Attribution Method Development Must Address Salience Bias**
   - Current methods inherently biased toward low-level visual properties
   - New methods needed that can distinguish learned from salient features
   - Evaluation must use controlled experiments like watermark paradigm

2. **Benchmarking Needs Revision**
   - Current benchmarks may not capture faithfulness
   - Need datasets where salience decoupled from informativeness
   - Evaluation should test mechanism, not just consistency

3. **Mechanistic Understanding Gap**
   - Why do gradient-based methods emphasize high frequencies?
   - Can we develop fundamentally different attribution mechanisms?
   - Is salience bias fixable or inherent to gradient-based approaches?

### For Practitioners

1. **Use Attribution Cautiously**
   - Don't rely on single attribution method for critical decisions
   - Combine with other validation approaches (ablation, counterfactuals, causal analysis)
   - Be skeptical of visually pleasing explanations

2. **Validation Strategy**
   - Test on distribution shifts or out-of-distribution data
   - Verify that "important" features actually drive predictions
   - Use counterfactual analysis: actually remove important features, does prediction change?

3. **Communication**
   - Don't present attribution heatmaps as definitive proof of model reasoning
   - Acknowledge uncertainty and known biases
   - Communicate that explanations are approximate, not exact

### For Stakeholders & Regulators

1. **Explainability ≠ Trustworthiness**
   - A model with explanation is not inherently more trustworthy
   - Current XAI methods can create false confidence
   - Require multiple complementary validation approaches

2. **Audit & Oversight**
   - Can't assume attribution-based audits are sufficient
   - Need rigorous testing of actual decision drivers
   - Consider independent verification of explanations

3. **Standards Development**
   - Current standards for AI transparency may need technical updates
   - Should specify multiple explanation methods, not just one
   - Include validation requirements beyond visual explanations

---

## Conclusion

This paper delivers a crucial wake-up call to the XAI community: **popular attribution methods may not faithfully reveal model decision-making**. Through elegant experimental design using watermarked images, the authors provide compelling evidence that visual salience—not task-learned informativeness—primarily drives feature importance attribution in methods across LIME, SHAP, LRP, Integrated Gradients, and Deconvolution.

The implications are profound:
- Practitioners cannot reliably use attribution for model debugging
- Explanations based on current methods may create false confidence
- Regulators cannot assume attribution-based interpretability satisfies transparency requirements
- The field needs fundamentally rethinking about what "explanation" means

Rather than diminishing XAI's importance, this work points toward more rigorous, careful science. Future progress requires:
- New attribution methods designed to overcome salience bias
- Controlled evaluation frameworks measuring faithfulness directly
- Integration of causal inference with interpretability
- Humble communication about current limitations

This paradigm-challenging paper will likely become a foundation for a more rigorous second generation of Explainable AI research.

---

## References & Further Reading

**Primary Source:**
- Clark, B., Oliveira, M., Wilming, R., & Haufe, S. (2026). Feature salience – not task-informativeness – drives machine learning model explanations. arXiv preprint arXiv:2602.09238.

**Related Attribution Methods (Foundational):**
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?": Explaining the Predictions of Any Classifier. arXiv:1602.04938.
- Sundararajan, M., Taly, A., & Yan, Q. (2017). Axiomatic Attribution for Deep Networks. In ICML.
- Lundberg, S. M., & Lee, S. I. (2017). A Unified Approach to Interpreting Model Predictions. In NeurIPS.
- Bach, S., Binder, A., Montavon, G., Klauschen, F., Müller, K. R., & Samek, W. (2015). On Pixel-Wise Explanations for Non-Linear Classification Decisions by Deconvolutional Networks. PLOS ONE, 10(7), e0130140.

**Related Faithfulness & Sanity Check Papers:**
- Adebayo, H., Gilmer, J., Muelly, M., Goodfellow, I., Hardt, M., & Kim, B. (2018). Sanity Checks for Saliency Maps. In NeurIPS.
- Simonyan, K., Vedaldi, A., & Zisserman, A. (2013). Deep Inside Convolutional Networks: Visualising Image Classification Models and Saliency Maps. In ICLR Workshops.
