# Informative Post-Hoc Explanations Only Exist for Simple Functions

**Authors:** Eric Günther, Balázs Szabados, Robi Bhattacharjee, Sebastian Bordt, Ulrike von Luxburg  
**Affiliation:** University of Tübingen, Tübingen AI Center  
**ArXiv ID:** 2508.11441  
**Submitted:** August 15, 2025  
**Link:** [arXiv:2508.11441](https://arxiv.org/abs/2508.11441)

## Executive Summary

This paper provides a rigorous learning-theory-based framework for evaluating when post-hoc explanation algorithms actually provide meaningful information about machine learning models. The authors demonstrate that under weak assumptions, popular explanation methods (SHAP, LIME, gradient-based methods, counterfactual explanations) are fundamentally non-informative for complex decision functions—a finding that challenges the practical utility of these widely-used techniques and establishes theoretical conditions under which explanations become informative.

## Problem Statement

Post-hoc explanation algorithms have become ubiquitous in machine learning, with practitioners relying on methods like SHAP, LIME, and gradient-based saliency maps to understand model decisions. However, a critical gap exists: while these methods are widely deployed, there is limited theoretical understanding of whether they actually provide meaningful information about complex models.

The core question this paper addresses is fundamental: **What does it mean for an explanation to be "informative" about a decision function?** Furthermore, **under what conditions can local post-hoc explanations reduce our uncertainty about model behavior for complex models?**

Previous work has focused on explaining specific model behaviors or designing new explanation methods, but lacks a unified theoretical framework for evaluating whether explanations are genuinely informative versus merely appearing to provide insights.

## Core Concepts & Theory

### Informativeness Framework

The paper introduces the concept of **informativeness** grounded in learning theory. An explanation is informative with respect to a space of decision functions $\mathcal{H}$ if it reduces the complexity of the space of plausible decision functions consistent with both the model's predictions and the explanation.

**Formal Definition:**
- An explanation is informative if it significantly reduces the Rademacher complexity or VC dimension of the hypothesis class of functions that are consistent with both the model's output and the provided explanation.
- Intuitively: the explanation narrows down which functions could plausibly be the true decision function.

### Key Learning-Theory Concepts

1. **Hypothesis Space Reduction:** Explanations constrain the set of plausible functions. The more constraints an explanation imposes, the more informative it is.

2. **Complexity Measures:** The paper uses standard learning theory complexity measures:
   - Rademacher complexity
   - VC dimension
   - These measure how rich a function class is—simpler classes have lower complexity

3. **Function Space Assumptions:** Different assumptions about the decision function class lead to different conclusions:
   - Differentiable functions: very rich class with high complexity
   - Lipschitz-continuous functions: adds smoothness constraint
   - Low-gradient functions: adds additional curvature constraints
   - Decision trees: discrete structures with different complexity properties

### Explanation Methods Analyzed

The framework is applied to four popular families of explanation methods:

1. **Gradient-Based Explanations:** Compute partial derivatives to identify influential features
2. **Counterfactual Explanations:** Find minimal feature changes that flip the model's prediction
3. **SHAP Explanations:** Game-theoretic attribution based on Shapley values
4. **Anchor Explanations:** Find sufficient feature sets that maintain predictions

## Main Ideas & Key Contributions

### Primary Theoretical Results

The paper's main contributions are negative results that challenge conventional wisdom:

1. **Gradient explanations are non-informative for differentiable functions:**
   - A gradient explanation does not significantly reduce the space of plausible differentiable functions
   - The reason: many different functions can produce the same gradient at a specific point
   - **Condition for informativeness:** Gradients become informative when restricted to low-gradient/low-curvature function spaces

2. **Counterfactual explanations are non-informative for general differentiable functions:**
   - Knowing that changing features X→X' flips a prediction does not eliminate most plausible differentiable functions
   - **Condition for informativeness:** Counterfactuals become informative under Lipschitz continuity constraints

3. **SHAP explanations are non-informative for decision trees:**
   - SHAP values do not meaningfully constrain which decision tree could be the true model
   - **Condition for informativeness:** SHAP becomes informative with stronger structural assumptions

4. **Anchor explanations suffer similar limitations:**
   - Anchors identify sufficient feature sets but do not strongly constrain broader function classes
   - Requires additional robustness or simplicity assumptions to be informative

### Why Are Popular Methods Non-Informative?

The fundamental issue is a **capacity mismatch:**
- Complex function classes (differentiable functions, trees) are extremely rich
- Individual local explanations constrain only small regions of this vast space
- A single local explanation cannot significantly reduce complexity for such expressive classes

**Example:** For the space of all differentiable functions, knowing that the gradient at point x is [0.5, -0.2, 0.1] still leaves an infinite number of functions consistent with this gradient. The gradient provides local information but doesn't constrain the global behavior of complex models.

### Conditions Under Which Explanations Become Informative

The paper provides positive results establishing when post-hoc explanations can be informative:

1. **Robustness-Based Informativeness:**
   - If the model is Lipschitz-continuous with bounded constant, counterfactual explanations become informative
   - Smoothness constraints narrow the function space significantly

2. **Curvature-Based Informativeness:**
   - Gradient explanations are informative on function classes with bounded gradients and Hessians
   - This models functions that change slowly and predictably

3. **Simplicity-Based Informativeness:**
   - Explanations are informative when combined with minimum description length (MDL) principles
   - Favoring simpler functions makes explanations more constraining

4. **Structural Assumptions:**
   - For tree-based models, additional structural constraints (e.g., limited depth) make SHAP informative
   - The key is making the model class sufficiently simple

## Methodology & Implementation

### Theoretical Framework

The paper employs standard learning theory machinery:

1. **Rademacher Complexity Analysis:**
   - For each explanation method, compute how much it reduces Rademacher complexity
   - Show that for unrestricted function classes, reduction is minimal
   - For restricted classes, quantify the reduction

2. **VC Dimension Calculations:**
   - Compute VC dimensions before and after applying explanation constraints
   - Show relative impact of explanation constraints

3. **Adversarial Analysis:**
   - For each explanation method, construct adversarial examples
   - Show functions consistent with explanation but behaving completely differently elsewhere
   - Demonstrates non-informativeness constructively

### Key Proofs and Results

**Theorem (Informal):** For the space of all differentiable functions $\mathcal{D}$:
- A gradient explanation at a single point does not significantly reduce the VC dimension or Rademacher complexity of $\mathcal{D}$

**Theorem (Informal):** For Lipschitz-continuous functions with constant $L$:
- A counterfactual explanation that identifies features X whose change from $x$ to $x'$ flips the prediction reduces the hypothesis space size by a factor that depends on $L$ and the magnitude of change
- Smaller Lipschitz constants → more informative explanations

### Empirical Validation

While primarily theoretical, the paper includes experiments demonstrating:

1. **Adversarial Examples Consistent with Explanations:**
   - Trained neural networks where SHAP/LIME explanations suggest one behavior but actual model behaves differently
   - Shows theoretical non-informativeness manifests in practice

2. **Comparison on Different Function Classes:**
   - Linear models: explanations are informative (small function class)
   - Tree models: SHAP becomes informative with structural constraints
   - Neural networks: explanations provide minimal information for unrestricted function classes

3. **Empirical Rademacher Complexity:**
   - Measures complexity of function classes with and without explanation constraints
   - Quantifies informativeness empirically

[Exact figures unavailable — see full paper for specific experimental results and metrics]

## Practical Applications & Real-World Use Cases

### Healthcare & Medical AI

The results have critical implications for regulated domains:
- **Current practice:** Clinicians rely on explanations from models for diagnostic support
- **Implication:** Without additional model constraints (e.g., Lipschitz bounds, limited depth), explanations may not meaningfully characterize model behavior
- **Recommendation:** Combine explanations with model simplicity constraints or certified robustness guarantees

### Finance & Credit Decisions

In loan approval systems:
- **Current practice:** SHAP explanations show which factors contribute to denial decisions
- **Implication:** For complex models, SHAP alone may not capture true decision logic
- **Recommendation:** Use inherently interpretable models or combine SHAP with robustness certification

### Legal & Regulatory Compliance

For AI used in high-stakes decisions:
- **GDPR & Right to Explanation:** Regulation requires explanations, but this paper shows many explanations may be non-informative
- **Implication:** Compliance requires not just explanation provision but verification that explanations meaningfully characterize decisions
- **Solution:** Implement model constraints that ensure explanations are theoretically informative

### Autonomous Systems

For self-driving cars or robotics:
- **Current practice:** Safety relies partly on understanding decision-making through explanations
- **Implication:** Unconstrained neural networks may have non-informative explanations despite appearing comprehensive
- **Recommendation:** Use structured model architectures with theoretical informativeness guarantees

## Insights & Implications

### Fundamental Insights

1. **Expressiveness vs. Interpretability Tradeoff:**
   - Complex, expressive models (deep neural networks) are inherently difficult to meaningfully explain
   - Post-hoc explanations can only truly inform about simple or constrained models
   - This suggests a fundamental tension: expressiveness and true interpretability may be incompatible

2. **Local vs. Global Understanding:**
   - Post-hoc explanations provide local information (at specific instances)
   - For complex models, local information cannot constrain global behavior
   - Understanding complex models may require global, not local, explanation approaches

3. **The Explanation-Simplicity Nexus:**
   - Meaningful explanations require assumptions about model simplicity
   - Without such assumptions, explanations become decorative rather than informative
   - The field should shift toward enforcing interpretable by design, not explaining after-the-fact

### Implications for XAI Research

1. **Beyond Popular Methods:**
   - The field's reliance on SHAP, LIME, and similar methods may be misplaced for complex models
   - Alternative approaches needed: mechanistic interpretability, concept-based methods, inherently interpretable models

2. **Theoretical Rigor:**
   - Future XAI work should include theoretical analysis of informativeness
   - Empirical plausibility ("explanations look reasonable") is insufficient
   - Formal guarantees about what explanations constrain are needed

3. **Model Design for Interpretability:**
   - Rather than explaining black boxes, design white boxes
   - Use models with structural constraints that ensure explanations are meaningful
   - Consider inherently interpretable architectures (decision trees, generalized additive models, sparse models)

4. **Certification and Verification:**
   - Combine explanations with formal verification methods
   - Prove that explanations constrain model behavior over continuous input regions
   - Use robustness certificates to enable informative explanations

### Limitations of the Approach

1. **Worst-Case Analysis:**
   - The framework considers unrestricted function classes
   - In practice, models may have implicit inductive biases that constrain them
   - Average-case or empirical analysis might yield different conclusions

2. **Function Class Selection:**
   - Informativeness depends heavily on the chosen function class
   - Different assumptions lead to different conclusions
   - No universal notion of informativeness across all contexts

3. **Practical vs. Theoretical:**
   - A theoretically non-informative explanation might still provide practical value
   - The framework measures information-theoretic reduction, not utility for human understanding
   - Domain-specific considerations may justify explanations despite theoretical limitations

## Code & Resources

### Paper Access
- **ArXiv PDF:** [https://arxiv.org/pdf/2508.11441](https://arxiv.org/pdf/2508.11441)
- **ArXiv Abstract:** [https://arxiv.org/abs/2508.11441](https://arxiv.org/abs/2508.11441)

### Implementation & Reproducibility

The paper is primarily theoretical with formal proofs. However, the empirical validation could be reproduced using:

**Required Libraries:**
- NumPy, SciPy (numerical computations)
- scikit-learn (model training, baseline models)
- SHAP (SHAP explanations)
- LIME (LIME explanations)
- PyTorch (for training neural networks)

**Computational Requirements:**
- Standard CPU workstation suitable for experiments
- No specialized GPU hardware required for main theoretical results

### Related Implementations

For practitioners interested in the implications:

1. **Inherently Interpretable Models:**
   - [InterpretML](https://github.com/interpretml/interpret) - Collection of interpretable models
   - [ExplainableAI.py](https://github.com/interpretml/interpret-community) - Microsoft's XAI framework

2. **Robustness Certification:**
   - [DeepG](https://github.com/locuslab/DeepG) - Neural network verification
   - [Marabou](https://github.com/NeuralNetworkVerification/Marabou) - Formal verification tool

3. **Alternative Explanation Methods:**
   - [Concept Bottleneck Models](https://github.com/karandesai-96/concept-bottleneck-models)
   - [Mechanistic Interpretability Toolkit](https://github.com/redwoodresearch/interp) - Redwood Research

## Related Work & Context

### Connection to Broader XAI Landscape

This paper significantly impacts several XAI communities:

**1. Post-Hoc Explanation Methods:**
- **SHAP & LIME Community:** The findings directly challenge the assumptions under which these methods are deployed
- The paper does not claim these methods are useless, but rather clarifies their theoretical limitations
- Motivates research into conditions where these methods are reliable

**2. Mechanistic Interpretability:**
- Supports the mechanistic interpretability community's focus on understanding internal model structure
- Suggests post-hoc explanations alone are insufficient for understanding complex models
- Complements work on circuit discovery, sparse autoencoders, and feature attribution within models

**3. Inherently Interpretable Models:**
- Reinforces arguments for inherently interpretable models (decision trees, GAMs, linear models)
- These models naturally satisfy the simplicity conditions under which explanations become informative

**4. Formal Methods & Verification:**
- Connects to formal verification literature that seeks provable guarantees about model behavior
- Suggests combining explanations with certification methods

**5. Fairness & Accountability:**
- Directly relevant to fairness literature: if explanations are non-informative, bias detection via explanations may be unreliable
- Motivates integrated approaches combining explainability and fairness certification

### Related Recent Work

**Theoretical Foundations:**
- "In Defence of Post-hoc Explainability" - Argues for contextualized post-hoc explanations
- "Post-Hoc Explanations Fail to Achieve their Purpose in Adversarial Contexts" - Shows limitations under adversarial conditions
- "Towards Unified Attribution: Analyzing Diverse Feature Attribution Approaches" - Categorizes attribution methods systematically

**Challenges to Explainability Claims:**
- "Explanation in artificial intelligence: Insights from the social sciences" - Critiques whether explanations address human needs
- "The (Un)reliability of Saliency Methods" - Questions reliability of saliency-based explanations
- "Beyond Technocratic XAI" - Examines who benefits from explanations and what constitutes meaningful explanation

**Alternatives to Post-Hoc Explanations:**
- "Mechanistic Interpretability for Neural Networks: Circuits, Sparse Features and Symbolic Reasoning" - Overview of mechanistic approaches
- "From Mechanistic to Compositional Interpretability" - Category-theoretic framework for composable interpretability
- "Concept Bottleneck Models" - Inherently interpretable architectures using human-defined concepts

### Future Research Directions

Building on this work, several research directions are suggested:

1. **Empirical Informativeness Studies:**
   - Measure whether explanations correlate with model behavior empirically
   - Determine if theoretical non-informativeness matches practical outcomes

2. **Conditional Informativeness:**
   - Develop methods to determine, given a specific model instance, whether explanations are informative
   - Create diagnostic tools for practitioners

3. **Hybrid Approaches:**
   - Combine post-hoc explanations with mechanistic understanding
   - Design models that are both expressive and constrained enough for informative explanations

4. **Explanation Design for Complex Models:**
   - Rather than explaining all models equally, design explanations tailored to model constraints
   - Custom explanation methods for specific model architectures

5. **User-Centered Evaluation:**
   - Study whether theoretically informative explanations help human decision-makers
   - Bridge gap between information-theoretic and cognitive definitions of informativeness

## Broader Impact & Significance

### Scientific Impact

This paper challenges a widespread assumption in the explainable AI community: that popular post-hoc explanation methods reliably convey information about model decisions. By providing rigorous theoretical analysis, it elevates the discourse from "explanations look plausible" to "do explanations actually inform?"

### Implications for AI Safety and Trust

The findings suggest that:
- **Transparency ≠ Interpretability:** A model with explanations is not necessarily interpretable
- **Regulation requires rigor:** Simply providing explanations (as many regulations require) may be insufficient without informativeness guarantees
- **Design matters:** Model architecture choices fundamentally affect the meaningfulness of explanations

### Recommendations for Practitioners

1. **Verify before relying:** If using explanations for high-stakes decisions, empirically verify that explanations correlate with model behavior
2. **Add constraints:** Combine black-box models with robustness guarantees to enable informative explanations
3. **Prefer white-box:** When possible, use inherently interpretable models rather than post-hoc explanations of complex models
4. **Use multiple methods:** Combine multiple explanation approaches; if they agree, more confidence; if they disagree, model may be fundamentally non-interpretable

## Discussion & Critical Perspective

While this paper makes valuable theoretical contributions, some limitations should be noted:

1. **Function Class Dependence:** Results hold for specific function space assumptions; different assumptions yield different conclusions

2. **Practical vs. Theoretical Informativeness:** Human understanding may not align perfectly with information-theoretic informativeness

3. **Null Result Interpretation:** The paper shows non-informativeness under weak assumptions; stronger assumptions recover informativeness, which some might interpret as "explanations work when the model is simple"

4. **Constructive Solutions:** The paper primarily identifies problems; it provides fewer constructive solutions for practitioners with complex models

Despite these nuances, the paper makes an important contribution by rigorously establishing theoretical limits of post-hoc explanation methods and providing clear conditions under which they become informative.
