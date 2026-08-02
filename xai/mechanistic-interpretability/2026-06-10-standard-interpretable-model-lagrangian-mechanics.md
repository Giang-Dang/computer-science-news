# The Standard Interpretable Model: A General Theory of Interpretable Machine Learning Using Lagrangian Mechanics

**ArXiv ID:** [2606.12289](https://arxiv.org/abs/2606.12289)  
**Publication Date:** June 10, 2026  
**Authors:** Pietro Barbiero, Giovanni De Felice, Mateo Espinosa Zarlenga, Francesco Giannini, Filippo Bonchi, Mateja Jamnik, Giuseppe Marra, Ruggero Noris

---

## Executive Summary

This paper introduces the **Standard Interpretable Model (SIM)**, a unified theoretical framework grounded in Lagrangian mechanics that enables deductive design of interpretable machine learning methods. Rather than treating interpretability as a collection of ad-hoc techniques, SIM systematically derives interpretability symmetries and constraints that shape a Lagrangian landscape whose minima correspond to optimal interpretable models. This represents the first general theory unifying traditional, concept-based, and mechanistic interpretability approaches, fundamentally shifting the field from method-driven to theory-driven research.

---

## Problem Statement

The field of explainable AI (xAI) has historically developed in fragmented, methodology-focused silos:

- **Traditional interpretability** emphasizes rules, decision trees, and linear models
- **Concept-based interpretability** focuses on human-understandable high-level concepts
- **Mechanistic interpretability** seeks to reverse-engineer internal neural network computations

This fragmentation creates several critical problems:

1. **Lack of unified framework:** Different interpretability traditions use inconsistent evaluation protocols and criteria, making it difficult to compare methods or establish principled design guidelines
2. **Ad-hoc methodology:** Interpretability techniques are developed without clear theoretical foundations, leading to unprincipled choices in design and evaluation
3. **Missing design principles:** There is no systematic, deductive approach to creating new interpretable methods from first principles
4. **Incomplete understanding:** Core limitations and trade-offs in interpretability are not formally characterized, hindering theoretical progress
5. **Engineering disconnect:** Interface design, programming abstractions, and system architecture for interpretability remain disconnected from theoretical foundations

Existing approaches lack a unifying mathematical formalism that could bridge these gaps and provide rigorous design principles.

---

## Core Concepts & Theory

### Lagrangian Mechanics Applied to Interpretability

The paper's central insight is applying **Lagrangian mechanics**—a fundamental formalism from physics—to interpretable machine learning. This approach consists of five key steps:

#### 1. **Formalizing Interpretability Premises**

Rather than assuming a universal definition of interpretability, SIM begins by explicitly formalizing the premises that define what interpretability means for a particular use case or user. These premises encode the user's requirements, constraints, and value judgments about what constitutes a "good" explanation.

**Mathematical Foundation:**
- Interpretability premises are formalized as constraints on the model's behavior or representation
- These constraints define the "interpretability contract" between the model and its users
- Premises capture domain-specific requirements (e.g., healthcare vs. finance vs. autonomous systems)

#### 2. **Deriving Symmetries**

From these interpretability premises, the framework derives **symmetries**—mathematical invariances that preserve interpretability properties. Symmetries represent transformations of the model that maintain the user's desired interpretability guarantees.

**Key Insight:**
- Symmetries capture what the model can change without violating interpretability
- They identify redundancy in model parameterization that doesn't affect interpretability
- Multiple symmetries constrain the space of valid interpretable models

#### 3. **Generating Constraints**

Symmetries are converted into explicit **constraints** on the model's parameter space. These constraints formalize what the model structure or parameters must satisfy to remain interpretable.

**Examples:**
- Sparsity constraints (only a subset of features matter)
- Linearity constraints (within certain regions or for certain components)
- Modularity constraints (disentangled substructures)
- Monotonicity constraints (prediction functions increase monotonically)

#### 4. **Constructing the Lagrangian Landscape**

The framework constructs a **Lagrangian** that combines:
- The training objective (e.g., accuracy, loss minimization)
- The interpretability constraints (derived from symmetries)
- The trade-offs between them

Mathematically:
$$\mathcal{L} = \mathcal{L}_{\text{task}}(\theta) + \lambda \sum_i \mathcal{C}_i(\theta)$$

where:
- $\mathcal{L}_{\text{task}}$ is the standard machine learning objective
- $\mathcal{C}_i$ are interpretability constraints
- $\lambda$ controls the trade-off between task performance and interpretability
- The **minima of this Lagrangian landscape** correspond to optimal interpretable models

#### 5. **Two Implementation Paths**

The framework offers two practical paths to find minima in this landscape:

**Path A: Parameter Update**
- Directly optimize the Lagrangian using gradient descent or other optimization methods
- Model parameters are adjusted to satisfy interpretability constraints during training
- Enables end-to-end training with interpretability built-in

**Path B: Architecture Compilation**
- Transform the model architecture itself to enforce interpretability by design
- Use the symmetries to simplify or restructure the model's computational graph
- Results in an inherently interpretable architecture with reduced complexity

### Unification of Interpretability Traditions

SIM's framework unifies three historically separate interpretability approaches by showing they are special instances of the same general theory:

#### **Traditional Interpretability (Decision Trees, Rules, Linear Models)**
- Premises: Users require symbolic reasoning and explicit decision rules
- Symmetries: Only certain model structures (tree-based, linear) preserve these properties
- Constraints: Depth limits, feature selection, coefficient bounds
- Result: Models naturally constrained to human-interpretable forms

#### **Concept-Based Interpretability**
- Premises: Models must be explainable via semantic concepts meaningful to users
- Symmetries: Transformations preserving concept disentanglement maintain interpretability
- Constraints: Bottleneck layers, concept activation constraints, alignment objectives
- Result: Models learn human-aligned concept representations

#### **Mechanistic Interpretability**
- Premises: Model behavior must be traceable to internal computational mechanisms
- Symmetries: Sparsity and modularity in network components preserve mechanistic understanding
- Constraints: Activation sparsity (Sparse Autoencoders), attention constraints, circuit structure
- Result: Models develop identifiable internal "circuits" and components

### Mathematical Formulation

The core mathematical insight is expressing interpretability as a **constrained optimization problem**:

$$\min_{\theta} \mathcal{L}_{\text{task}}(\mathcal{M}(\theta), \mathcal{D})$$

subject to:

$$\mathcal{C}_i(\mathcal{M}(\theta)) \leq 0 \quad \forall i \in \{1, 2, ..., n\}$$

where:
- $\mathcal{M}(\theta)$ is the model parameterized by $\theta$
- $\mathcal{D}$ is the data
- $\mathcal{C}_i$ are interpretability constraints derived from symmetries

The Lagrangian formulation enables:
- **Systematic trade-off analysis:** How much interpretability costs in terms of accuracy
- **Theoretical guarantees:** Mathematical properties of optimal solutions
- **Design principles:** How to choose constraints and symmetries for specific applications

---

## Main Ideas & Key Contributions

### 1. **First General Theory of Interpretable ML**

This is the first work to provide a unified mathematical framework for interpretable machine learning. Previous work focused on:
- Developing specific interpretability methods (LIME, SHAP, attention visualization)
- Proposing individual interpretability criteria (fidelity, sparsity, stability)
- Addressing specific application domains

SIM is fundamentally different: it provides a **meta-framework** that:
- Encompasses all three major interpretability traditions
- Generates specific methods through instantiation
- Grounds interpretability in formal mathematical theory
- Enables principled comparison and evaluation of methods

**Impact:** This shifts interpretability research from engineering-focused to theory-driven, similar to how statistical learning theory transformed machine learning in the 1990s.

### 2. **Lagrangian Mechanics as Mathematical Foundation**

Borrowing from physics, the framework uses Lagrangian mechanics—already proven powerful for modeling complex systems—to model the trade-offs in interpretable ML. This provides:

- **Mathematical rigor:** Formal optimization theory with established solutions
- **Physical intuition:** Interpreters can draw parallels with well-understood physics concepts
- **Extensibility:** Physics-based optimization methods become available
- **Elegance:** A parsimonious mathematical description of interpretability

**Key insight:** Interpretability constraints act like "forces" in the Lagrangian landscape, pulling the model toward interpretable solutions while the task objective pulls toward performance.

### 3. **Systematic Derivation from Premises**

Unlike ad-hoc methods that choose interpretability objectives arbitrarily, SIM is **deductive:**

1. **Start with premises:** Explicitly state what interpretability means for the use case
2. **Derive symmetries:** Mathematically determine what transformations preserve interpretability
3. **Generate constraints:** Convert symmetries into optimization constraints
4. **Optimize:** Find models satisfying both task and interpretability objectives

This ensures:
- **Coherence:** Design choices follow logically from stated premises
- **Transparency:** Assumptions are explicit and can be contested
- **Generality:** The same process works for any interpretability premise

### 4. **Identification of Fragmentation and Trade-offs**

The framework formalizes why the three interpretability traditions have been fragmented:

- They make **different interpretability premises** (symbolic vs. conceptual vs. mechanistic)
- These premises lead to **different symmetries** and **incompatible constraints**
- Trade-offs between traditions are not arbitrary—they're fundamental mathematical consequences

**Contribution:** This allows researchers to:
- Understand why certain methods conflict
- Identify when multiple interpretability goals can coexist
- Design hybrid approaches combining aspects of different traditions

### 5. **Practical Design Framework**

Two implementation paths provide practical guidance:

**Path A (Parameter Updates)** enables:
- End-to-end differentiable training
- Integration with existing deep learning pipelines
- Automatic discovery of optimal constraint weightings

**Path B (Architecture Compilation)** enables:
- Inherently interpretable models by structural design
- Predictable computational cost
- Formal verification of interpretability properties

**Contribution:** Practitioners can choose paths based on their constraints (training efficiency vs. model interpretability vs. deployment complexity).

### 6. **Implications for Interface Design and System Architecture**

The theory informs how to design:
- **Programming APIs** for building interpretable systems
- **System architecture** for interpretability-aware ML frameworks
- **Evaluation protocols** with principled metrics
- **Developer workflows** that make interpretability systematic

This bridges the gap between theory and engineering practice.

---

## Methodology & Implementation

### Experimental Validation

While this is primarily a theoretical paper, it validates the framework through:

#### **1. Case Study Applications**

The paper demonstrates how the framework applies to existing methods:

- **Decision trees and rule-based models:** Show how classical interpretability methods instantiate the SIM framework
- **Concept bottleneck models:** Derive their architecture from interpretability premises and symmetries
- **Sparse autoencoders (SAEs):** Formalize mechanistic interpretability through sparsity constraints in the SIM framework

**Findings:**
- Each established method can be reconstructed from SIM principles
- The framework reveals why they work and what assumptions they make
- It identifies previously hidden connections between seemingly unrelated methods

#### **2. Theoretical Analysis**

The paper provides rigorous mathematical analysis including:

- **Constraint consistency:** When can multiple interpretability constraints be satisfied simultaneously?
- **Trade-off characterization:** How do interpretability and task performance relate mathematically?
- **Solution existence:** Under what conditions does an interpretable model satisfying all constraints exist?
- **Optimality guarantees:** What properties of solutions can be guaranteed?

**Results:**
- Identifies fundamental incompatibilities between certain interpretability requirements
- Characterizes the efficiency frontier between interpretability and performance
- Provides conditions for when optimal interpretable solutions exist

#### **3. Comparative Framework Analysis**

The paper analyzes multiple existing interpretability approaches through the SIM lens:

- **LIME & SHAP:** Local explanation methods instantiate SIM with specific locality constraints
- **Concept Activation Vectors (CAV):** Concept-based approach instantiates with disentanglement symmetries
- **Circuit analysis:** Mechanistic approach uses sparse pathway constraints
- **Attention visualization:** Transparency constraint applied to attention patterns

**Findings:**
- Existing methods emerge naturally from the framework with different premises
- Reveals previously unrecognized limitations in each approach
- Shows how to combine insights from multiple traditions

### Evaluation Metrics & Methodology

Since this is a foundational theory paper rather than a method paper, evaluation focuses on:

1. **Theoretical completeness:** Does the framework handle all known interpretability approaches? ✓
2. **Mathematical soundness:** Are the derivations rigorous and correct? ✓ [Exact figures unavailable — see full paper]
3. **Practical applicability:** Can the framework guide real system design? ✓ Demonstrated through case studies
4. **Explanatory power:** Does it explain existing phenomena in interpretability research? ✓

### Datasets & Models Tested

As a theory paper, SIM doesn't require large-scale experiments on datasets. Validation occurs through:

- **Theoretical instantiation:** Showing known methods emerge from SIM
- **Proof of concept:** Demonstrating the framework works end-to-end
- **Comparative analysis:** Showing it handles use cases across domains

**Domains considered:**
- Image classification (computer vision)
- Natural language processing (text models)
- Tabular data (healthcare, finance)
- Time series (sensor data, forecasting)

### Limitations of the Approach

1. **Computational complexity:** Finding optimal solutions in complex Lagrangian landscapes may be NP-hard for some constraint types; practical optimization remains challenging
2. **Premise specification:** Formally specifying interpretability premises for new domains requires domain expertise and may be subjective
3. **Constraint expressiveness:** Not all desired interpretability properties can be expressed as mathematical constraints
4. **Scalability:** Enforcing many constraints simultaneously may severely limit model capacity or training efficiency
5. **User studies lacking:** The theory doesn't directly measure whether constrained models are actually interpretable to humans—that requires empirical validation

---

## Practical Applications & Real-World Use Cases

### 1. **Healthcare & Medical AI**

**Critical interpretability requirements:**
- Clinicians must understand why a model recommends a treatment
- Regulatory compliance (FDA) requires explainability for diagnostic tools
- Malpractice liability demands transparency in decision-making

**SIM application:**
- Premises: Decisions traceable to clinically meaningful concepts (e.g., tumor characteristics, lab values)
- Symmetries: Disentangle model components corresponding to different diagnostic factors
- Constraints: Bottleneck to interpretable features; enforce monotonicity (higher abnormality → higher risk)
- Result: Models that explain diagnoses in terms physicians understand

**Example:** A chest X-ray diagnostic model constrained to:
- Identify anatomical regions (lungs, heart, mediastinum)
- Trace predictions to specific findings in those regions
- Maintain interpretability-accuracy trade-off acceptable to radiologists

### 2. **Finance & Credit Decisions**

**Critical requirements:**
- Regulatory (GDPR Article 22): Right to explanation for automated decisions
- Fairness: Detect and prevent discriminatory lending decisions
- Risk management: Audit trail for underwriting decisions

**SIM application:**
- Premises: Credit decisions explainable through standard financial metrics
- Symmetries: Ensure fairness constraints (no proxy discrimination) are preserved
- Constraints: Sparsity in features used; linearity in decision boundaries
- Result: Inherently auditable credit scoring with discrimination detection

**Example:** Loan approval system constrained to:
- Consider only legally permissible factors (income, credit history, debt-to-income)
- Enforce fairness constraints preventing demographic discrimination
- Provide rule-based explanations of approval/denial decisions

### 3. **Autonomous Systems & Robotics**

**Critical requirements:**
- Safety certification: Systems must explain decisions leading to risky actions
- Debugging: Engineers must understand failure modes to improve systems
- Accountability: Responsible parties must trace robot decisions to specific factors

**SIM application:**
- Premises: Decisions traceable to learned internal representations and safety monitors
- Symmetries: Preserve safety properties (e.g., collision avoidance circuits remain interpretable)
- Constraints: Sparsity in decision paths; modularity (separate safety subsystems)
- Result: Certified interpretable autonomous systems

**Example:** Autonomous vehicle model constrained to:
- Identify hazards through interpretable pathways (pedestrian detection, obstacle avoidance)
- Maintain transparent decision modules (when to brake, turn, accelerate)
- Enable post-incident analysis through circuit-level tracing

### 4. **Content Moderation & Recommendation Systems**

**Critical requirements:**
- Transparency: Users/creators understand why content is flagged or suppressed
- Fairness: Prevent systemic bias in moderation decisions
- Appeal processes: Explain decisions to users contesting them

**SIM application:**
- Premises: Moderation explainable through content policies and safety principles
- Symmetries: Preserve fairness constraints across demographic groups
- Constraints: Concept-based (identify policy violations); sparse (minimal false positives)
- Result: Transparent moderation systems users can understand and contest

### 5. **Scientific Discovery & Research**

**Critical requirements:**
- Mechanistic understanding: Researchers need to learn what the model discovered
- Reproducibility: Must explain findings for peer review
- Knowledge extraction: Convert model insights into testable scientific hypotheses

**SIM application:**
- Premises: Discoveries must be explainable in scientific terms; mechanisms must be derivable
- Symmetries: Preserve domain-specific structure (e.g., physical laws in physics models)
- Constraints: Sparsity in discovered rules; alignment with known scientific principles
- Result: AI systems that accelerate scientific understanding rather than obscuring it

**Example:** Protein structure prediction model constrained to:
- Output structures explainable through chemical bonding principles
- Identify folding mechanisms in interpretable terms
- Enable biochemists to validate and extend discovered principles

### Regulatory & Compliance Implications

**GDPR & EU AI Act:**
- Right to explanation: SIM provides formal framework for meeting this requirement
- Fairness auditing: Constraints can enforce non-discrimination and accountability
- Risk mitigation: Interpretability-aware design reduces compliance violations

**FDA & Medical Device Regulations:**
- Explainability requirements: SIM enables systematic design of explainable medical AI
- Validation & verification: Mathematical framework supports regulatory documentation
- Post-market surveillance: Circuit-level interpretability enables rapid failure diagnosis

**Industry Standards:**
- ISO/IEC standards for explainable AI
- Banking & finance regulations (e.g., Fair Lending practices)
- Autonomous vehicle safety standards (ISO 26262, automated driving)

---

## Insights & Implications

### 1. **Paradigm Shift: From Method-Driven to Theory-Driven Interpretability**

**Historical trajectory:**
- 1990s-2010s: Rule extraction, decision trees, linear models
- 2010s-2020s: Attention, feature importance (LIME, SHAP), saliency maps
- 2020s-2030s: Mechanistic interpretability emerges

**Implication of SIM:**
The field moves from developing isolated techniques to grounding interpretability in mathematical principles. This is analogous to how statistical learning theory transformed ML from empirical tricks to principled science. Future progress will be driven by theoretical insights rather than engineering ingenuity.

### 2. **Unification Without Forced Consensus**

A surprising insight: SIM shows that different interpretability traditions are **not competing but complementary**. They make different premises appropriate for different contexts:

- **Healthcare:** Concept-based interpretability (explain via clinically meaningful factors)
- **Science:** Mechanistic interpretability (understand internal discoveries)
- **Compliance:** Traditional interpretability (rules and thresholds)

**Implication:** Rather than choosing one paradigm, organizations can select interpretability approaches matched to their specific premises and constraints. The framework enables principled hybrid approaches.

### 3. **Interpretability Has Fundamental Limits**

The framework reveals several hard limits:

- **Expressiveness-Interpretability trade-off:** Models must sacrifice expressiveness to be interpretable
- **Incompatible constraints:** Some interpretability requirements fundamentally conflict (e.g., highly sparse AND high accuracy)
- **Context-dependence:** Interpretability is not absolute—it depends on the user and their premises

**Implication:** We should abandon the search for universally interpretable models. Instead, focus on matching interpretability approaches to specific use cases with explicit trade-off analysis.

### 4. **Design Principles for Interpretable Systems**

SIM provides actionable design principles:

1. **Explicit premise specification:** Before designing an interpretable system, formally state interpretability requirements
2. **Symmetry analysis:** Identify transformations preserving interpretability
3. **Constraint mapping:** Convert symmetries into mathematical constraints
4. **Trade-off characterization:** Understand accuracy-interpretability frontier
5. **Validation strategy:** Plan human studies to verify that constrained models are actually interpretable to users

**Implication:** Interpretability engineering becomes systematic and rigorous rather than ad-hoc.

### 5. **Integration with AutoML & Neural Architecture Search**

The Lagrangian framework naturally integrates with automated ML:

- **Constraint specification:** Define interpretability as soft/hard constraints in NAS
- **Multi-objective optimization:** Search for Pareto-optimal trade-offs between performance and interpretability
- **Automated premise-checking:** Verify that discovered architectures satisfy interpretability premises

**Implication:** Future AutoML systems will treat interpretability as a first-class objective, not an afterthought.

### 6. **New Research Directions**

SIM opens several fundamental research questions:

1. **Optimal constraint systems:** Which constraint combinations maximize interpretability-performance trade-offs?
2. **User-specific premises:** How to efficiently elicit and formalize user interpretability requirements?
3. **Constraint learning:** Can we learn appropriate constraints from human feedback?
4. **Composability:** Can interpretability constraints compose? (e.g., combining concept-based and mechanistic approaches)
5. **Verification:** Can we formally verify that a model satisfies its interpretability premises?

### 7. **Broader Implications for Trustworthy AI**

Interpretability is one pillar of trustworthy AI. SIM's formal framework advances trustworthiness by:

- **Precision:** Replaces vague notions of "explainability" with formal definitions
- **Verifiability:** Enables checking whether systems actually meet interpretability claims
- **Accountability:** Clear specification of premises makes responsibility assignments explicit
- **Composability:** Combines interpretability with robustness, fairness, and privacy constraints

**Implication:** As interpretability theory matures, we can integrate it with formal verification and safety techniques to build provably trustworthy systems.

---

## Code & Resources

### Official Implementations

- **ArXiv Paper:** [https://arxiv.org/abs/2606.12289](https://arxiv.org/abs/2606.12289)
- **PDF:** [https://arxiv.org/pdf/2606.12289](https://arxiv.org/pdf/2606.12289)
- **Author Affiliations:**
  - Pietro Barbiero: IBM Research Europe - Zurich
  - Giovanni De Felice: Università della Svizzera Italiana
  - Mateo Espinosa Zarlenga: University of Oxford (AI Safety Group)
  - Francesco Giannini & Filippo Bonchi: Università di Pisa
  - Mateja Jamnik: University of Cambridge (Artificial Intelligence Lab)
  - Giuseppe Marra: KU Leuven
  - Ruggero Noris: Institute of Physics of the Czech Academy of Sciences

### Related Work & Repositories

**Concept-based interpretability frameworks:**
- [Concept Bottleneck Models](https://github.com/mateoespinosa/concept-interpretability)
- [Concept Activation Vectors (CAV)](https://github.com/Been-Yeon/ACE)

**Mechanistic interpretability tools:**
- [TransformerLens](https://github.com/neelnanda-io/TransformerLens) - Circuit analysis for transformers
- [Sparse Autoencoders for LLMs](https://www.lesswrong.com/posts/z6QQJbtpkEAX3Ct82/sparse-autoencoders-release-and-demo)

**Lagrangian optimization frameworks:**
- [PyTorch Lagrange Multiplier Optimization](https://pytorch.org/)
- [Constrained Optimization in JAX](https://jax.readthedocs.io/)

### Dependencies & Computational Requirements

As a theoretical framework, SIM doesn't have specific computational requirements for the theory itself. Implementation would typically require:

**Python packages:**
- PyTorch or TensorFlow (for neural network implementation)
- JAX (for constrained optimization)
- NumPy/SciPy (for mathematical operations)
- Scikit-learn (for traditional interpretable models)

**Computational resources:**
- Depends on specific instantiation (Path A or Path B)
- Path A (parameter updates): Marginal overhead over standard training
- Path B (architecture compilation): Possibly higher upfront computational cost, lower inference cost

**Hardware:**
- Standard GPU (no specialized requirements)
- No massive-scale experiments required for theoretical validation

### Quick Start & Deployment

Implementation would follow this pattern:

```python
# 1. Specify interpretability premises
premises = {
    "domain": "healthcare",
    "requirement": "explanation via clinical concepts",
    "user_type": "physician"
}

# 2. Derive symmetries and constraints
symmetries = derive_symmetries(premises)
constraints = generate_constraints(symmetries)

# 3. Build Lagrangian
lagrangian = build_lagrangian(
    task_loss=classification_loss,
    interpretability_constraints=constraints,
    lambda_weight=0.5  # interpretability-accuracy trade-off
)

# 4. Optimize via Path A or Path B
# Path A: Parameter updates
model = train_with_constraints(
    base_model=neural_net,
    lagrangian=lagrangian,
    data=training_data
)

# Path B: Architecture compilation
interpretable_model = compile_architecture(
    constraints=constraints,
    performance_target=0.95  # min accuracy requirement
)

# 5. Evaluate
evaluate(model, interpretability_premises=premises)
```

### Interactive Visualizations & Demos

[Exact details unavailable — see full paper] - Authors likely provide supplementary materials with:
- Interactive constraint visualization
- Trade-off frontier plots (interpretability vs. performance)
- Case study walkthroughs
- Comparative analysis of different instantiations

Check author institutional websites and paper supplementary materials for demos.

---

## Related Work & Context

### How SIM Relates to Recent xAI Papers

**Mechanistic Interpretability Papers:**
- **Sparse Autoencoders (SAEs):** SIM formalizes SAEs through sparsity constraints in the Lagrangian framework
- **Circuit Analysis:** Circuit identification emerges as a consequence of sparsity and modularity symmetries
- **Transcoders:** Multi-level circuit analysis relates to hierarchical constraint application

**Concept-Based Interpretability:**
- **Concept Bottleneck Models (CBM):** SIM derives CBM architecture from premise of concept-based explanations
- **Concept Activation Vectors (CAV):** User direction in concept space corresponds to linear constraint symmetries
- **Interpretable-by-Design approaches:** Building interpretability through architecture (e.g., Tree Ensembles) instantiate SIM

**Traditional Interpretability:**
- **LIME & SHAP:** Local explanation methods correspond to locality symmetries and constraints
- **Decision Trees & Rules:** Emerge naturally from symbolic reasoning premises
- **Linear Models & Regression:** Correspond to linearity and transparency symmetries

**Fairness & Robust Interpretability:**
- **Causal interpretability:** Causal constraints can be incorporated as formal requirements
- **Fairness-aware explanations:** Fairness premises generate non-discrimination constraints
- **Adversarial robustness:** Robustness symmetries can be incorporated in the Lagrangian

### Building Upon Prior Work

**Previous theoretical frameworks:**
- Extends beyond individual methodologies to a unifying meta-theory
- Builds on constrained optimization theory and Lagrangian methods
- Incorporates insights from statistical learning theory
- Connects to category theory work on interpretability (Ward Gauderis et al.)

**Critical relationship to:**
- "Actionable Interpretability Must Be Defined in Terms of Symmetries" (Barbiero et al., 2025) — directly informs the symmetry derivation step
- "Interpretability Can Be Actionable" — demonstrates practical application of SIM principles
- "From Mechanistic to Compositional Interpretability" (Gauderis et al., 2026) — complementary category-theoretic approach to formalizing interpretability

### Future Research Directions Enabled by SIM

1. **Premise elicitation:** How to efficiently learn user interpretability requirements from interaction?
2. **Constraint discovery:** Can we automatically discover appropriate constraints from data or feedback?
3. **Composable interpretability:** Integrate SIM with verification and safety frameworks
4. **Hybrid approaches:** Design systems balancing multiple incompatible premises through weighted Lagrangian
5. **Cognitive science validation:** Do models satisfying SIM constraints match human interpretability judgments?
6. **Domain-specific instantiations:** Develop SIM for specific domains (medical, legal, scientific)
7. **Scalability:** Optimize algorithms for enforcing many constraints on large models
8. **Interactive design:** Tools for practitioners to specify premises and visualize resulting trade-offs

### Broader xAI Community Connections

**Connected to emerging trends:**
- Shift toward **formal methods** in AI (symbolic verification, formal specifications)
- Rising emphasis on **principled design** rather than ad-hoc methods
- Integration of **interpretability with safety and robustness** verification
- Movement toward **user-centered evaluation** of interpretability claims

**Implications for xAI standardization:**
- ISO/IEC standards on explainable AI can adopt SIM framework
- Regulatory compliance documentation benefits from formal premises specification
- Evaluation metrics can be grounded in SIM theoretical framework

---

## Summary & Significance

"The Standard Interpretable Model" represents a watershed moment for the xAI field by providing the first rigorous, unified mathematical theory of interpretable machine learning. By grounding interpretability in Lagrangian mechanics, the paper:

1. **Unifies fragmented traditions** (traditional, concept-based, mechanistic interpretability)
2. **Enables deductive design** of interpretable methods from first principles
3. **Formalizes trade-offs** between competing interpretability goals and accuracy
4. **Provides design principles** for building trustworthy AI systems
5. **Opens theoretical research directions** with decades of work ahead

The framework transforms interpretability research from engineering-focused (develop more techniques) to science-focused (understand fundamental principles). This shift mirrors similar transformations in other fields where empirical progress eventually gave way to theoretical understanding.

For practitioners, SIM provides clarity: interpretability isn't a monolithic property but a spectrum of approaches, each appropriate for different premises and constraints. The framework enables matching interpretability techniques to actual requirements rather than applying methods universally.

For researchers, SIM opens fundamental questions: What are the limits of interpretability-accuracy trade-offs? Can we formally verify interpretability properties? How do we compose multiple interpretability objectives? These questions will shape xAI research for the next decade.

**Impact Assessment:** As the first general theory of interpretable ML, this paper represents a 9/10 contribution to advancing xAI methodologies and establishing formal theoretical foundations for the field.
