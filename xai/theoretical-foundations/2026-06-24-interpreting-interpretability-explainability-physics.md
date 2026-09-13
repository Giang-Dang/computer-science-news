# Interpreting "Interpretability" and Explaining "Explainability" in Machine Learning in Physics

**Authors:** Rikab Gambhir (MIT), Luisa Lucie-Smith (University of Hamburg), Jesse Thaler (MIT)

**ArXiv ID:** 2606.26228

**Publication Date:** June 24, 2026

**Pages:** 31

**Part of:** VERaiPHY Initiative

---

## Executive Summary

This paper provides a comprehensive framework for understanding the distinct concepts of interpretability and explainability as applied to machine learning in physics. By carefully defining interpretability as structural transparency and explainability as scientific content mapping, the authors clarify the trade-offs and contexts where each is most appropriate. The work is essential for developing trustworthy ML systems in scientific domains where understanding model behavior and decisions directly impacts research validity and discovery.

## Problem Statement

Machine learning has become increasingly central to physics research, yet the interpretation and explanation of ML models in scientific contexts remains poorly defined and often conflated. The key challenges addressed:

1. **Conceptual Confusion**: "Interpretability" and "explainability" are often used interchangeably despite having fundamentally different meanings and implications
2. **Domain Mismatch**: General-purpose XAI methods developed for other domains may not be appropriate or sufficient for physics applications
3. **Scientific Validity**: Physics requires not just understanding *why* a model makes predictions, but understanding whether those predictions align with known physics and can lead to new scientific insights
4. **Trade-off Navigation**: Scientists must understand the tensions between interpretability and model expressivity, explainability and adaptability
5. **Lack of Frameworks**: Existing XAI literature provides limited guidance on when to prioritize which type of explanation in scientific contexts

The paper addresses the urgent need for a principled, domain-aware framework for thinking about model interpretation in physics machine learning.

## Core Concepts & Theory

### Interpretability vs. Explainability: A Critical Distinction

The paper establishes clear, differentiated definitions:

**Interpretability**: Concerns the **structural transparency** of a model—the ability to understand or approximate its inner workings. This is about how the model functions mechanistically.

- Focus: How the model works internally
- Questions answered: "What computations does the model perform?"
- Methods: Circuit analysis, attention visualization, feature importance, neural network dissection
- Trade-off: More interpretable models are often less expressive

**Explainability**: Concerns the **scientific content** of a model—the ability to map model behavior and decisions onto domain knowledge and scientific principles. This is about what the model learns about the physical world.

- Focus: How model predictions relate to physics
- Questions answered: "What does the model tell us about the physical system?"
- Methods: Counterfactuals, causal analysis, physics-informed explanations, ablation studies
- Trade-off: More explainable systems may be less adaptable to new domains or phenomena

### Key Trade-offs Framework

**1. Interpretability vs. Expressivity**
- Interpretable models (linear, tree-based, rule-based) sacrifice representational power
- Complex models (deep neural networks) gain expressivity but lose interpretability
- Physics applications must choose where to position on this spectrum based on discovery goals

**2. Explainability vs. Adaptability**
- Models that are highly explainable in terms of known physics may fail to discover novel phenomena
- Models designed to discover new patterns may produce explanations that contradict established physics
- Scientists must decide: confirm existing knowledge or explore beyond it?

**3. Intrinsic vs. Post-Hoc Tools**
- Intrinsic interpretability: Built into model design (e.g., interpretable-by-design architectures)
- Post-hoc explainability: Applied after model training (e.g., LIME, SHAP, attention analysis)
- Each has strengths and limitations; optimal strategy often combines both

### Core Framework: Deliberate Modeling Choices

Rather than treating interpretability and explainability as inherent properties to achieve, the paper argues they should be understood as:

1. **Deliberate design choices** made during model development
2. **Task-specific requirements** depending on the scientific question
3. **Intervention-focused outcomes** requiring explicit plans for how explanations will be used
4. **Domain-aligned evaluations** grounded in physics principles, not just ML metrics

## Main Ideas & Key Contributions

### 1. Conceptual Clarification

**Novel Contribution**: This is among the first papers to rigorously distinguish interpretability from explainability in the context of physics ML, moving beyond generic XAI definitions.

**Why It Matters**: Many papers conflate these concepts, leading to confusion about what capabilities are actually needed. By clarifying the distinction, researchers can better specify which capability their work addresses.

### 2. Context-Dependent Framework

The paper introduces a framework for determining when each type of explanation is most valuable:

| Context | Interpretability Priority | Explainability Priority | Reasoning |
|---------|--------------------------|----------------------|-----------|
| **Model Validation** | High | Medium | Need to verify model correctness internally |
| **Physics Discovery** | Medium | High | Need to map patterns to physical principles |
| **Real-Time Application** | High | Low | Need fast decisions with clear decision boundaries |
| **Regulatory Compliance** | Medium | High | Need to justify decisions to authorities |
| **Theory Development** | Low | High | Need to understand physical implications |

### 3. Task Specification and Intervention Plans

A key insight: Interpretability and explainability should only be evaluated in the context of how explanations will actually be used.

- **Task Specification**: Clear definition of the scientific question and success metrics
- **Intervention Plan**: How will the explanation lead to scientific progress or decision-making?
- **Success Metrics**: Whether the explanation actually enables the intended intervention

Example: An attention visualization (interpretable) might satisfy the "show me what the model looked at" requirement but fail to provide scientific insight (explainability) about why certain weather patterns lead to climate effects.

### 4. Application-Specific Considerations

The paper emphasizes that physics ML differs fundamentally from other domains:

1. **Ground Truth Comparisons**: Physics often has theoretical predictions to compare against
2. **Physical Constraints**: Models can be evaluated against known physical laws
3. **Reproducibility**: Scientific explanations must be reproducible across similar conditions
4. **Parsimony**: Physics values simplicity and elegance in explanations
5. **Predictive Power**: Explanations should improve future predictive capability

## Methodology & Implementation

### Paper Structure and Approach

The paper employs a **conceptual and comparative analysis** approach rather than proposing new algorithms:

1. **Literature Review**: Comprehensive survey of interpretability and explainability definitions across ML and physics
2. **Definitional Analysis**: Careful parsing of how these terms are used in different contexts
3. **Framework Development**: Construction of decision matrices for when to prioritize each
4. **Case Studies**: Examples from real physics applications showing the framework in practice

### Key Methodological Points

**1. Scope Analysis**
- Interpretability is inherently *local* (understanding specific model decisions)
- Explainability can be *local* or *global* (explaining individual predictions or general patterns)

**2. Tool Categorization**

**Intrinsic Interpretability Methods:**
- Linear models and interpretable-by-design architectures
- Sparse networks with pruning
- Tree-based models
- Rule-based systems

**Post-Hoc Interpretability Methods:**
- Attention visualization
- Saliency maps and gradient-based methods
- Feature importance scores (SHAP, LIME)
- Activation analysis and circuit discovery

**Post-Hoc Explainability Methods:**
- Counterfactual explanations
- Causal intervention analysis
- Physics-informed surrogate models
- Ablation studies grounded in domain knowledge

### Evaluation Metrics

[Exact figures unavailable — see full paper]

The paper discusses how interpretability and explainability should be evaluated:

**Interpretability Metrics:**
- Fidelity of model reconstructions
- Consistency of feature explanations
- Human-understandability scores

**Explainability Metrics:**
- Alignment with known physics
- Predictive value of scientific insights
- Reproducibility across similar systems
- Domain expert validation

## Practical Applications & Real-World Use Cases

### 1. Climate Science and Weather Prediction

**Challenge**: ML models for climate prediction are often "black boxes" making decisions crucial for policy recommendations.

**Application**:
- Interpretability: Understanding which atmospheric variables the model relies on (attention to pressure, temperature, humidity patterns)
- Explainability: Mapping model predictions to known climate physics (e.g., linking jet stream shifts to temperature anomalies)

**Impact**: Scientists can validate whether the model has learned physically plausible relationships, not just correlations in training data.

### 2. Astrophysics and Cosmology

**Challenge**: ML for galaxy classification, gravitational lensing analysis, or dark matter detection must balance discovery with physical rigor.

**Application**:
- Interpretability: Visualizing which morphological features activate model responses
- Explainability: Determining if learned features correspond to known astrophysical properties (luminosity, star formation rate, chemical composition)

**Regulatory Implication**: Publication in physics journals increasingly requires explanations of model decisions aligned with physics principles.

### 3. High Energy Physics

**Challenge**: ML is used in data analysis and event classification, where misclassification can mislead particle physics discoveries.

**Application**:
- Interpretability: Understanding decision boundaries in feature space
- Explainability: Confirming that model decisions align with known particle physics and detector physics

**Compliance Need**: Particle physics collaborations require documentation of model behavior and validation against physics simulations.

### 4. Autonomous Scientific Instruments

**Challenge**: ML systems controlling scientific instruments (telescopes, spectrometers, detectors) must make reliable decisions in real-time.

**Application**:
- Interpretability: Fast, clear decision boundaries for instrument control
- Explainability: Ensuring decisions respect physical constraints and known instrumental properties

**Practical Feasibility**: Both interpretable architectures and post-hoc analysis are typically necessary to ensure reliable autonomous operation.

### 5. Scientific Discovery via ML

**Challenge**: When ML is expected to discover new physics or phenomena, understanding model insights is paramount.

**Application**:
- Priority shifts: Explainability becomes more critical than interpretability
- Focus: Identifying which learned patterns correspond to novel physics vs. artifacts
- Method: Combine model analysis with simulation validation

**Discovery Risk**: Without proper explanation, models might identify artifacts or biases rather than genuine physical phenomena.

## Insights & Implications

### Broader Implications for Trustworthy AI

1. **Interpretability ≠ Trust**: A highly interpretable model that learns incorrect physics is less trustworthy than an explainable complex model that discovers correct physics

2. **Domain Matters**: Generic XAI approaches may be insufficient for physics; domain-specific validation and explanation strategies are necessary

3. **Scientific Rigor**: Physics applies standards of rigor (reproducibility, theoretical grounding, predictive power) that should inform XAI evaluation

4. **Deliberate Design**: Interpretability and explainability must be specified as requirements *before* model development, not retrofitted afterwards

### Limitations and Failure Cases

**Interpretability Limitations:**
- Attention patterns may not truly reflect which information the model uses (attention is not explanation)
- Interpretable approximations of complex models may be unfaithful
- Visual interpretability methods can be misleading in high-dimensional spaces

**Explainability Limitations:**
- Models may learn physically correct patterns that are still scientifically uninteresting
- Explanations in terms of known physics may miss novel phenomena
- Domain experts may disagree on what constitutes a "good" explanation

**Framework Limitations:**
- Trade-offs between interpretability and expressivity are not always sharp; some models achieve both
- Task specification is difficult in exploratory research where questions are not pre-specified
- Intervention plans may be uncertain in fundamental research contexts

### Open Questions and Future Directions

1. **Unified Evaluation**: How can we develop metrics that simultaneously evaluate interpretability, explainability, and scientific validity?

2. **Hybrid Approaches**: Can we better combine intrinsic interpretability with post-hoc explanation to get benefits of both?

3. **Physics-Specific Methods**: What new explanation methods could be developed specifically for physics applications?

4. **Automated Validation**: Can we automate validation of model explanations against physics simulations and known laws?

5. **Sociological Factors**: How do social factors (career incentives, publication norms) influence which explanations scientists find convincing?

## Code & Resources

**Paper Access:**
- Full PDF: https://arxiv.org/pdf/2606.26228
- Abstract/HTML: https://arxiv.org/abs/2606.26228

**Related Initiatives:**
- VERaiPHY Initiative: Verified Artificial Intelligence for Physics (collaborative effort across multiple institutions)

**Related Codebases & Tools:**

While the paper itself is primarily conceptual, the following tools implement the interpretation and explanation methods discussed:

- **Mechanistic Interpretability**: https://github.com/redwoodresearch/interp (circuit discovery tools)
- **Feature Importance**: https://github.com/slundberg/shap (SHAP implementations)
- **Physics-ML Libraries**: JAX (https://github.com/google/jax) for building interpretable physics models
- **Attention Visualization**: https://github.com/huggingface/transformers (attention analysis tools)

**Installation & Dependencies:**

As a conceptual paper, there are no computational requirements for reading. However, implementing the framework requires:
- Familiarity with PyTorch or TensorFlow for model building
- Understanding of physics domain (varies by application)
- XAI libraries (SHAP, LIME, Captum) for post-hoc explanation

**Quick Start Guide:**

To apply this framework to your physics ML project:

1. **Specify your task**: What is the scientific question and how will ML help answer it?
2. **Identify explanations needed**: Does your project require interpretability, explainability, or both?
3. **List your constraints**: What are your computational budget, model expressivity needs, and domain constraints?
4. **Design your model**: Choose architecture/methods aligned with your explanation needs
5. **Plan interventions**: How will explanations actually influence scientific decisions or actions?
6. **Validate against physics**: Test whether explanations align with known physics and discover expected patterns

## Related Work & Context

### Connection to Other xAI Subfields

**1. Feature Attribution and Interpretability**
- Related papers: SHAP (Lundberg & Lee, 2017), LIME (Ribeiro et al., 2016)
- Distinction: Those papers focus on general post-hoc methods; this paper contextualizes their use in physics
- Advancement: Emphasizes limitations of generic attribution methods for scientific domains

**2. Mechanistic Interpretability**
- Related papers: Circuits work (Olah et al., Circuits group at Anthropic)
- Distinction: Mechanistic interpretability focuses on understanding model internals; this paper emphasizes science alignment
- Advancement: Adds layer of physics validation to mechanistic analysis

**3. Causal Inference and Explanation**
- Related papers: Causal models (Pearl, 2000), causal explanations in ML (Goyal et al.)
- Connection: Explainability in physics often requires causal reasoning
- Advancement: Framework for deciding when causal explanations are needed vs. alternatives

**4. Concept-Based Explanations**
- Related papers: TCAV (Kim et al., 2018), concept bottleneck models
- Distinction: Those papers develop methods for concept extraction; this discusses when concepts matter for physics
- Advancement: Emphasizes alignment with domain concepts vs. learned concepts

**5. Human-Centered XAI**
- Related papers: Work on user studies, cognitive science of explanation
- Connection: Framework depends on understanding how scientists use explanations
- Advancement: Adds domain-specific considerations for physics

**6. Theoretical Foundations**
- Related papers: "Interpretability Needs a New Paradigm" (Lipton, 2018)
- Connection: Shares critique of loose terminology in XAI
- Advancement: Proposes structured framework for physics applications specifically

### Prior Work This Paper Builds Upon

1. **XAI Survey Papers**: Synthesizes definitions from multiple survey papers on explainability
2. **Physics ML Literature**: Reviews existing applications of ML in physics domains
3. **Scientific Method Philosophy**: Grounds framework in scientific reasoning and epistemology
4. **ML Systems Literature**: Incorporates insights from responsible AI and ML governance

### Future Research Directions

**Short-term (1-2 years):**
1. Develop physics-specific evaluation benchmarks for interpretability and explainability
2. Create standardized case studies across physics domains
3. Build tools automating validation against physics laws

**Medium-term (2-5 years):**
1. Integrate uncertainty quantification with explanation
2. Develop hybrid interpretable/explainable model architectures
3. Create standards for physics ML publication requirements

**Long-term (5+ years):**
1. Physics-specific XAI as a recognized subfield with its own conferences/venues
2. Automated scientific hypothesis generation from model explanations
3. Integration with formal verification for physics constraints

### Connection to Broader xAI Communities

This work bridges multiple communities:

- **XAI Community**: Proposes domain-specific refinement of interpretability/explainability concepts
- **Physics Community**: Advocates for rigorous explanation practices in ML-assisted science
- **Scientific ML Community**: Emphasizes importance of interpretable scientific discovery
- **ML Governance Community**: Demonstrates how domain context affects explanation needs
- **Mechanistic Interpretability Community**: Complements technical work with scientific validation layer

## Author Affiliations and Research Groups

**Rikab Gambhir** - MIT
- Research focus: ML for high energy physics
- Previous work: Physics simulations, neural networks for particle detection

**Luisa Lucie-Smith** - University of Hamburg  
- Research focus: Cosmology and astrophysics simulations
- Previous work: ML applications to galaxy surveys and structure formation

**Jesse Thaler** - MIT (LHC Theory Group)
- Research focus: Theoretical high energy physics and ML
- Previous work: Machine learning for particle physics, jet substructure analysis

---

## Summary

This paper makes a fundamental contribution to xAI by rigorously distinguishing interpretability (structural transparency) from explainability (scientific content) in the context of physics machine learning. Rather than proposing new algorithms, it establishes a conceptual framework for understanding when each type of explanation is needed, the trade-offs involved, and how to design ML systems with explanation as a first-class requirement.

The work is particularly valuable for the growing community of researchers applying deep learning to physics, where the stakes are high (decisions impact scientific validity) and the domain has its own standards for rigor. By grounding the framework in scientific epistemology and physics applications, the authors demonstrate that generic XAI approaches are insufficient and that domain-specific thinking is essential.

For physics practitioners, this paper provides actionable guidance on specifying explanation requirements early in model development and validating explanations against domain knowledge. For the broader XAI community, it shows how conceptual clarity and domain specificity can advance the field beyond one-size-fits-all approaches.
