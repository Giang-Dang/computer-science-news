# CircuitSteer: Geometrically Aligned Multi-Layer Steering via Sparse Autoencoder Circuits

**ArXiv ID:** [2608.05732](https://arxiv.org/abs/2608.05732)

**Authors:** Mehrshad Saadatinia, Ardalan Aryashad, Reza Razmara, Ali Abbasi, Seyedarmin Azizi

**Submission Date:** August 6, 2026

**Paper Type:** Novel Method / Empirical Study

---

## Executive Summary

CircuitSteer proposes a training-free method for steering large language models through semantic features identified and coordinated across multiple transformer layers via sparse autoencoders (SAEs). Rather than applying steering interventions at a single layer (as in prior work), CircuitSteer constructs coherent cross-layer feature circuits using geometric alignment principles and applies steering vectors at every layer of the circuit. The method demonstrates superior fluency preservation and effectiveness on challenging behaviors (sycophancy, refusal) where single-layer steering methods fail. This work bridges mechanistic interpretability (identifying internal circuits via SAEs) and controllability (steering model behavior), advancing both fields.

---

## Problem Statement

Current steering methods for large language models face critical limitations:

1. **Single-Layer Bottleneck:** Existing steering approaches (e.g., Contrastive Activation Addition) apply interventions at only one layer, limiting the breadth of influence and often causing unintended side effects.

2. **Fluency Degradation:** Many steering methods reduce generation quality (measured by increased perplexity) as they reduce target behaviors—a poor trade-off in practical applications.

3. **Limited Effectiveness on Complex Behaviors:** Single-layer steering struggles with complex, distributed behaviors like sycophancy (agreement-seeking) and refusal behaviors that likely involve computations across multiple layers.

4. **Lack of Interpretability in Steering:** Previous steering work operates on low-level activation vectors without identifying what semantic features are being manipulated. This makes it difficult to understand what the model is being "steered" to do.

5. **No Principled Multi-Layer Approach:** While multi-layer steering has been attempted, prior work lacks a principled way to coordinate interventions across layers—how to select which layers to intervene on, and how to align steering directions across layers?

6. **Destructive Interference:** Adding steering vectors at multiple layers naively can cause interference effects, where interventions at one layer cancel out or conflict with interventions at another layer.

CircuitSteer addresses these challenges by identifying semantic circuits through SAEs, using geometric alignment to coordinate multi-layer interventions, and demonstrating that this approach preserves fluency better than alternatives.

---

## Core Concepts & Theory

### 1. Sparse Autoencoders and Feature Circuits

**Sparse Autoencoders (SAEs) as Circuit Identifiers:**

A sparse autoencoder decomposes a model's activation vectors into sparse, interpretable features:

$$\text{SAE}(\mathbf{a}) = \mathbf{d}(\text{ReLU}(\mathbf{W}_{enc} \mathbf{a} + \mathbf{b}_{enc}))$$

Where:
- $\mathbf{a}$ is an activation vector from a transformer layer
- $\mathbf{W}_{enc}$ and $\mathbf{b}_{enc}$ are encoder parameters
- The ReLU encourages sparsity (most latent dimensions are zero)
- $\mathbf{d}$ is a dictionary of learned decoder directions (basis vectors)
- Each decoder direction represents a semantic feature

**Features as Circuits:**

A semantic feature (decoder direction) that activates across multiple layers forms a **circuit**. For example, a feature encoding "politeness" might activate in layer 5, layer 10, layer 15, etc. The circuit is the set of (layer, feature) pairs where this semantic feature is represented.

**Co-Activation:**

To identify which features across layers form meaningful circuits, CircuitSteer uses co-activation: features that activate together on similar inputs are more likely to be part of the same semantic circuit. This is measured as:

$$\text{co-activation}(f_i^l, f_j^{l'}) = \frac{\mathbb{E}[a_i^l \cdot a_j^{l'}]}{\sigma_i^l \sigma_j^{l'}}$$

Where $a_i^l$ is the activation of feature $i$ in layer $l$, and $\sigma$ denotes standard deviation.

### 2. Geometric Alignment Principle

**The Core Insight:**

While co-activation identifies which features belong together, it doesn't guarantee that steering interventions at different layers will work coherently. Two decoder directions $\mathbf{d}_i^l$ and $\mathbf{d}_j^{l'}$ may represent the same semantic concept but point in different geometric directions in their respective activation spaces.

**Geometric Alignment Criterion:**

CircuitSteer aligns steering directions using decoder direction similarity:

$$\text{alignment}(f_i^l, f_j^{l'}) = \frac{\mathbf{d}_i^l \cdot \mathbf{d}_j^{l'}}{|\mathbf{d}_i^l| |\mathbf{d}_j^{l'}|}$$

This is the cosine similarity between decoder directions. High alignment ($\cos \theta \approx 1$) means the directions point in similar directions—adding a vector in one direction should have coherent effects at both layers.

**Why Alignment Matters:**

Without alignment, steering could cause destructive interference:
- If decoder directions $\mathbf{d}_i^l$ and $\mathbf{d}_j^{l'}$ point in opposite directions ($\cos \theta \approx -1$), adding a steering vector $\alpha \mathbf{d}_i^l$ would activate the feature in layer $l$ but deactivate it in layer $l'$
- With alignment, steering is constructive: interventions reinforce the same semantic direction across layers

### 3. Multi-Layer Steering Vector Construction

**Algorithm:**

For a behavior to steer (e.g., reduce sycophancy):

1. **Identify target features:** Find features that activate more on high-sycophancy vs. low-sycophancy examples. These are features whose removal would reduce sycophancy.

2. **Build cross-layer circuit:** Starting with a target feature, find co-activated, geometrically aligned features in other layers.

3. **Construct steering vector:** For each layer in the circuit, average the decoder directions of circuit features:
   $$\mathbf{v}_{steer}^l = \text{mean}(\{\mathbf{d}_i^l : f_i \text{ in circuit}\})$$

4. **Apply at all circuit layers:** Modify activations at each layer:
   $$\mathbf{a}_{steer}^l = \mathbf{a}^l - \alpha \mathbf{v}_{steer}^l$$

Where $\alpha$ is a scaling factor controlling steering strength.

**Key Property - Training-Free:**

This entire process requires no training. It uses already-trained SAE dictionaries and geometric properties of the activation space. This makes it applicable to any model with SAEs available.

### 4. Comparison to Prior Steering Approaches

**Contrastive Activation Addition (CAA) and Single-Layer Steering:**

CAA identifies a direction in a single layer's activation space that distinguishes positive vs. negative examples:
$$\mathbf{v}_{CAA} = \text{mean}(\mathbf{a}^{+}) - \text{mean}(\mathbf{a}^{-})$$

Applied at one layer, then scaled and added to reduce unwanted behavior.

**Advantages of CircuitSteer over CAA:**
- Works at multiple layers simultaneously, covering more of the computation
- Geometric alignment ensures coherent interventions
- Preserves fluency better (lower perplexity increase)
- Succeeds on behaviors where CAA fails (sycophancy, refusal)

**Limitations CircuitSteer Addresses:**
- CAA at multiple layers causes fluency collapse (unintended side effects)
- Matched-layer CAA (applying same CAA vector at multiple layers) shows perplexity collapse, confirming naive multi-layer steering doesn't work
- CircuitSteer's geometric alignment is necessary and sufficient for coherent multi-layer steering

---

## Main Ideas & Key Contributions

### 1. Principled Multi-Layer Steering Framework

CircuitSteer establishes that multi-layer steering can be effective if grounded in:
- **Semantic coherence:** Features must represent the same concept (co-activation)
- **Geometric alignment:** Intervention directions must point the same way (alignment of decoder directions)
- **Distributed application:** Intervene at every circuit layer, not just one

This is the first work to propose geometric alignment as a principle for multi-layer steering, moving beyond ad-hoc approaches.

### 2. Integration of Mechanistic Interpretability with Steering

The method unifies two previously separate research threads:
- **Mechanistic interpretability:** Identifying what semantic features drive model behavior
- **Model steering/control:** Changing model behavior via activation interventions

By using SAE-identified features and their geometric properties, CircuitSteer shows how to translate mechanistic understanding into effective control.

### 3. Superior Fluency Preservation

A critical practical contribution: CircuitSteer is the only method tested that consistently preserves generation quality (perplexity < 1.0 normalized) while reducing target behaviors. This is essential for deployment—steering that degrades model quality is useless in practice.

**Empirical Results:**
- **Fluency:** Lowest normalized perplexity across all settings
- **Behavioral reduction:** Measurable reduction on 7 of 8 test configurations
- **Sycophancy on Gemma:** Only method with non-zero effect (others fail completely)

### 4. Training-Free, Model-Agnostic Approach

Unlike methods requiring:
- Fine-tuning or continued training
- Custom loss functions
- New model checkpoints

CircuitSteer only needs:
- Pre-trained SAE dictionaries for target model
- Simple matrix operations (no backprop)
- Applies immediately without modification to base model

This makes it broadly applicable and easy to deploy.

### 5. Geometric Analysis of Steering Efficacy

The paper provides a new lens for understanding steering:
- Geometric alignment (cosine similarity of decoder directions) predicts steering effectiveness
- Lack of alignment predicts failure
- This geometric criterion guides which layers and features to steer

This opens new research directions: what geometric properties predict other forms of model control?

---

## Methodology & Implementation

### Experimental Setup

**Models Tested:**
- **Gemma-2-2B:** A smaller, more interpretable model (allows full ablations)
- **Llama-3.1-8B-Instruct:** A practical, instruction-tuned model

**SAE Source:**
- Pre-trained dictionary scaling (DS) SAEs from Anthropic's SAE lens library
- Dictionary size: 4× model dimension (typical for LLM SAEs)

**Sparse Autoencoder Details:**
- Top-k activation with k=64 (at most 64 features active per token)
- Trained on model's residual stream activations
- Decoder directions normalized to unit vectors

### Behavioral Datasets

The paper evaluates steering on four behavior categories:

1. **Toxicity Reduction** (Reframing Task)
   - Dataset: REFRAME dataset
   - Goal: Reduce toxic language while preserving meaning
   - Metric: Human evaluation + automated toxicity classifiers

2. **Emotion Intensity** (HHEM Dataset)
   - Goal: Modulate emotional intensity in generations
   - Two directions: Increase vs. decrease intensity
   - Metric: Supervised emotion intensity classifier

3. **Sycophancy Reduction** (ElicitSycophancy Dataset)
   - Goal: Reduce agreement with incorrect human opinions
   - Dataset: Questions where model should correct humans
   - Metric: Logical consistency + human evaluation

4. **Refusal Behavior** (JailBreak Dataset)
   - Goal: Control refusal on adversarially generated prompts
   - Dataset: Jailbreaking attempts and benign requests
   - Metric: Manual annotation + behavior consistency

### Evaluation Metrics

**Behavioral Reduction:**
- Dataset-specific classifiers measuring target behavior
- Statistical significance tests (reported as significant at 95% confidence on 7/8 configs)

**Fluency/Quality:**
- **Perplexity:** Normalized perplexity on target model's generation
- **Benchmark:** Perplexity = 1.0 is neutral (no cost from steering)
- **Goal:** Minimize perplexity while maximizing behavioral reduction

**Trade-off Analysis:**
- Plots of behavioral reduction vs. normalized perplexity
- Identifies Pareto frontier: methods that maximize behavioral benefit with minimal fluency cost

### Ablation Studies

**Key Ablations:**

1. **Matched-Layer CAA:** Apply CAA-derived direction at all circuit layers
   - **Result:** Perplexity collapse (uncontrolled side effects)
   - **Interpretation:** Naive multi-layer doesn't work without alignment

2. **Co-activation Only:** Use only co-activation, skip geometric alignment
   - **Result:** Higher perplexity, reduced effectiveness
   - **Interpretation:** Alignment is necessary for coherent steering

3. **Single vs. Multi-Layer:** Compare single-layer vs. all-circuit-layer steering
   - **Result:** Multi-layer significantly more effective
   - **Interpretation:** Distributed computation requires distributed intervention

4. **Ablating Circuit Layers:** Remove individual layers from steering circuit
   - **Result:** Varied impact depending on layer's importance
   - **Interpretation:** Validates that identified circuits are causal

### Reproducibility

- **Code Available:** GitHub repository at github.com/mehrshad-sdtn/CircuitSteer
- **Data:** Uses publicly available datasets (REFRAME, ElicitSycophancy, etc.)
- **Dependencies:** Standard PyTorch + SAE lens library
- **Checkpoints:** Works with public model checkpoints (Gemma-2, Llama-3.1)

### Limitations of Approach

1. **SAE Availability:** Requires pre-trained SAEs for target model
   - SAEs not available for all models
   - SAE training quality affects steering quality

2. **Feature Interpretation:** Geometric alignment doesn't guarantee semantic meaning
   - A decoder direction pointing in the same direction as another might encode different concepts
   - Manual inspection needed for some circuits

3. **Scalability:** Computing co-activation and alignment across all features is computationally intensive
   - Feasible for 2-8B models, unclear for 70B+

4. **Behavior Specificity:** Circuits are behavior-specific
   - Different circuits needed for different behaviors
   - No single universal steering vector

5. **Causality Claims:** Alignment is correlational, not proven causal
   - While ablations support causality, full causal chains remain unclear

---

## Practical Applications & Real-World Use Cases

### 1. Reducing Harmful Model Behaviors in Production

**Scenario: Customer Support Chatbot**
- Problem: Model exhibits sycophancy, agreeing with incorrect user claims to seem helpful
- Solution: Use CircuitSteer to identify and dampen agreement-seeking circuits
- Benefit: Honest, helpful responses without fine-tuning or model replacement
- Real-world impact: Deploy safer models without expensive retraining

**Scenario: Content Moderation System**
- Problem: Model sometimes generates toxic content despite attempts to filter
- Solution: Identify toxicity-related features via SAE, steer to reduce
- Benefit: Layer-wise steering covers more of the toxic-generation pipeline
- Real-world impact: Practical fluency preservation allows deployment

### 2. Customizable Model Behavior without Fine-Tuning

**Use Case: Multi-Tenant API Service**
- Different customers want different model behaviors
- CircuitSteer allows per-customer steering vectors (training-free)
- Customers can request: "reduce formality," "be more concise," "avoid technical jargon"
- Implementation: Apply corresponding steering circuit + strength at inference time

**Use Case: Adaptive Behavior**
- Context-dependent steering (adjust to user preference in conversation)
- No redeployment needed—just change steering strength or target behavior
- Enables personalization without per-user fine-tuning cost

### 3. Model Alignment and Safety Verification

**Safety Auditing:**
- Use CircuitSteer to probe how easily models can be steered toward harmful behaviors
- If sycophancy circuit can be strengthened with same geometric alignment, model is vulnerable
- Use mechanistic understanding to design better alignment procedures

**Alignment Verification:**
- Deploy model with specific steering disabled (e.g., disable refusal circuit dampening)
- This creates honeypots: if model generates refusals when circuit is "off," something is wrong
- Mechanistic verification stronger than behavioral testing alone

### 4. Interpretability-Driven Debugging

**Debugging Model Failures:**
- Example: Model unexpectedly becomes toxic in certain contexts
- Use CircuitSteer framework to identify toxicity circuits
- Ablate them to verify causality
- If ablation fixes behavior, circuit identification is validated
- If not, search for other circuits—mechanistic approach guides debugging

**Understanding Emergent Behaviors:**
- When models exhibit unexpected behaviors, apply CircuitSteer to understand what circuits drive them
- Stronger interpretability → faster root cause analysis

### 5. Research on Model Internals

**Mechanistic Understanding:**
- Use steering results to infer what computations happen in intermediate layers
- Geometric alignment tells us what features participate in behavior
- Build maps of how semantics change across layers

**Cross-Model Analysis:**
- Compare circuits across different model architectures/sizes
- Are sycophancy circuits similar in Llama and Gemma?
- Build understanding of universal model principles

### 6. Compliance and Regulatory Requirements

**EU AI Act / GDPR:**
- Mechanistic explanations satisfy "explainability" requirements better than black-box methods
- CircuitSteer identifies interpretable features driving behavior
- Documentation: "model's sycophancy is reduced via SAE features X,Y,Z at layers L1,L2,L3"

**Finance and Healthcare:**
- Regulators demand interpretability in high-stakes domains
- CircuitSteer provides mechanistic evidence: which model components drive decisions?
- More credible than attention visualization or gradient attribution

---

## Insights & Implications

### 1. Geometric Principles Govern Model Control

A key finding: coherent model control requires geometric alignment of intervention directions. This principle likely extends beyond steering:
- What other forms of model control depend on geometric properties?
- Can we use geometry to predict controllability?
- Does this inform how to design better steering mechanisms?

### 2. Multi-Layer Semantics Matter

Behaviors are not localized to single layers. The fact that CircuitSteer's multi-layer approach is necessary (single-layer methods fail on sycophancy) suggests:
- Complex behaviors emerge from distributed, multi-layer computation
- Mechanistic interpretability must operate at multiple layers
- Single-layer explanations are incomplete

### 3. Fluency-Behavior Trade-off is Solvable

Prior steering work suffered from fluency degradation. CircuitSteer shows that with better circuit identification and geometric alignment, this trade-off can be largely eliminated. This opens practical deployment pathways.

### 4. SAEs Enable New Forms of Control

SAEs identify semantic features, enabling richer control than raw activation vectors:
- Can steer specific semantic concepts, not just low-level patterns
- Interpretability and controllability are linked
- Better mechanistic understanding → better control

### 5. Limitations and Remaining Questions

The paper also reveals important limitations:

**Theoretical Gaps:**
- Geometric alignment is correlational; causality not fully established
- Why does geometric alignment predict steering effectiveness? What's the mechanism?
- Does geometric alignment generalize to other behaviors/models?

**Practical Challenges:**
- Requires SAEs for every target model (computational cost)
- Scalability to larger models unclear
- Manual circuit inspection still needed in some cases

**Generalization:**
- Do identified circuits transfer across models?
- Does geometry-based prediction work for non-semantic behaviors?
- Can single geometric principle explain all steering phenomena?

### 6. Connection to Broader xAI and Safety Research

**For Explainability:**
- Mechanistic circuits provide more faithful explanations than post-hoc methods
- Geometric properties are interpretable and understandable

**For Safety and Alignment:**
- Demonstrates that we can understand and control model behavior through circuits
- Suggests alignment might be achievable through mechanistic means
- Raises questions about deceptive alignment: could a model hide an unaligned circuit?

**For Neuroscience:**
- Geometric principles in artificial neural networks might illuminate biological brains
- Multi-layer coding and alignment may be universal principles in intelligent systems

---

## Code & Resources

### Official Implementations

**GitHub Repository:**
- [CircuitSteer: github.com/mehrshad-sdtn/CircuitSteer](https://github.com/mehrshad-sdtn/CircuitSteer)
- Contains full implementation and experimental scripts
- Includes pretrained SAE dictionaries for tested models

### Dependencies and Requirements

**Core Dependencies:**
```
torch >= 2.0
transformers >= 4.35
numpy >= 1.24
scipy >= 1.10
```

**SAE and Interpretability Tools:**
```
sae-lens  # For loading and working with sparse autoencoders
anthropic-sae-release  # Dictionary files
plotly >= 5.0  # For evaluation visualizations
```

**Computational Requirements:**
- **Minimal (single-layer steering):** 1× GPU with 12GB VRAM
- **Standard (multi-layer + ablations):** 1× GPU with 24GB VRAM (A100 or RTX 4090)
- **Full experimental pipeline:** 2× GPUs recommended
- **Storage:** ~5GB for model weights + SAE dictionaries per model

### Quick Start Guide

**1. Setup Environment:**
```bash
git clone https://github.com/mehrshad-sdtn/CircuitSteer
cd CircuitSteer
pip install -r requirements.txt
```

**2. Load Model and SAE Dictionary:**
```python
from transformer_lens import HookedTransformer
from sae_lens import SAE

# Load model
model = HookedTransformer.from_pretrained("gemma-2-2b")

# Load pre-trained SAE
sae, cfg, sparsity_data = SAE.from_pretrained(
    release="gemma-2-2b-tuned",
    sae_id="blocks.6.hook_resid_post"
)
```

**3. Identify Co-Activated Features:**
```python
# Extract activations on behavioral dataset
activations = extract_activations(
    model, 
    positive_examples,  # high sycophancy
    negative_examples   # low sycophancy
)

# Compute co-activation matrix
co_act_matrix = compute_coactivation(
    model, activations, sae
)

# Find co-activated features
circuit = find_circuit(
    feature_id=target_feature,
    layers=[5, 10, 15],
    cothreshold=0.7,
    align_threshold=0.5
)
```

**4. Apply Steering:**
```python
# Build steering vector from circuit
steering_vectors = build_steering_vectors(
    circuit, sae
)

# Apply during generation
output = model.generate(
    prompt,
    interventions=steering_vectors,
    strength=1.0
)
```

### Interactive Tools

**SAE Feature Explorer:**
- Visualize learned features and their semantics
- Inspect co-activation patterns across layers
- Analyze geometric alignment

**Steering Sandbox:**
- Test steering strength and observe fluency vs. behavioral reduction trade-off
- Ablate individual circuit layers interactively
- Compare different behaviors' circuits

---

## Related Work & Context

### How CircuitSteer Relates to Other xAI Approaches

**Compared to Concept-Based Explanations (TCAV, ACE):**
- **Concept-based:** Define human concepts a priori, then find them in model
- **CircuitSteer:** Discover task-driven features via SAE, use them for steering
- **Complementary:** Could combine human concepts with CircuitSteer for richer control

**Compared to Feature Attribution (LIME, SHAP, Integrated Gradients):**
- **Attribution methods:** Explain single predictions post-hoc
- **CircuitSteer:** Identify circuits that drive whole behavior classes, enable control
- **Key difference:** CircuitSteer extracts causal circuits, not just correlational importance

**Compared to Other Steering Methods:**
- **CAA (Contrastive Activation Addition):** Single-layer, fluency costs
- **Prompt engineering:** Brittle, requires manual crafting
- **Fine-tuning:** Expensive, creates new model checkpoint
- **CircuitSteer:** Multi-layer, fluency-preserving, training-free

### Prior Work CircuitSteer Builds On

**Foundational Papers:**

1. **Sparse Autoencoders for Interpretability (Bau et al., Elhage et al., Anthropic work 2023-2024):**
   - Established SAEs as tools for finding interpretable features in transformers
   - CircuitSteer applies SAEs to the new domain of steering

2. **Steering / Activation Intervention (Li et al., Zou et al., 2023-2024):**
   - Showed that linear interventions in activation space can control model behavior
   - CircuitSteer extends to multi-layer, geometrically-aligned version

3. **Circuit Analysis (Anthropic, OpenAI Circuits Research, 2021-2023):**
   - Identified specific circuits (induction heads, copy mechanisms) in transformers
   - CircuitSteer operationalizes circuit understanding for control

4. **Model Steering for Safety (various 2024-2025 papers):**
   - Applied steering for value alignment, safety, behavioral control
   - CircuitSteer provides mechanistic understanding of why steering works

### Where This Research is Leading

**Near-term (2026-2027):**

- **Scaling:** Apply CircuitSteer to larger models (13B-70B+)
- **Multi-behavior steering:** Coordinate steering for multiple behaviors simultaneously
- **Circuit transfer:** Do identified circuits transfer across models of similar architecture?

**Medium-term (2027-2030):**

- **Causal validation:** Prove circuit causality through more rigorous intervention paradigms
- **Automated circuit discovery:** Machine learning to automatically identify circuits without manual inspection
- **Real-time steering:** Enable fast, online circuit extraction during inference

**Long-term Vision:**

- **Transparent model design:** Build models where circuits are interpretable by construction
- **Mechanistic alignment:** Verify model alignment through circuit inspection, not just behavioral testing
- **Human-machine collaboration:** Let humans inspect circuits and provide feedback, enabling tight control over AI behavior

### Connection to Broader xAI and AI Safety Communities

**In Explainability Research:**
- Shows that mechanistic circuits enable richer explanations than black-box attribution
- Bridges interpretability (understanding what model does) and controllability (making it do what we want)

**In AI Safety/Alignment:**
- Critical for alignment verification: can we ensure unaligned circuits don't exist?
- Suggests mechanistic approaches to safety may be more reliable than behavioral testing
- Raises questions about deceptive alignment: could models hide circuits?

**In Mechanistic Interpretability:**
- Demonstrates practical utility of mechanistic understanding
- Moves field from pure interpretation toward actionable control
- Geometric principles may be universal in neural systems

---

## References and Further Reading

**Directly Referenced / Related Papers:**

1. Bau et al. (2019). "Network Dissection" - Early feature visualization work
2. Elhage et al. (2021-2024). "Anthropic Interpretability Papers" - Circuits and SAE foundations
3. Contrastive Activation Addition (Zou et al., Li et al., 2024)
4. SAE Scaling work (Anthropic 2024-2025)

**Implementation Resources:**

- TransformerLens: https://github.com/neelneelneelneel/TransformerLens
- SAE Lens: https://github.com/jbloomAus/SAELens
- Anthropic SAE Release: Pre-trained dictionaries for major models

**Related Surveys:**

- "Mechanistic Interpretability for Neural Networks: Circuits, Sparse Features and Symbolic Reasoning" (arXiv 2607.07316)
- "Mechanistic Interpretability for AI Safety" (review, 2024)

**Adjacent Research Areas:**

- Activation engineering and intervention studies
- Model steering for safety alignment
- Geometric analysis of neural representations
- Sparse representation learning

---

## Conclusion

CircuitSteer demonstrates that effective, practical model steering is possible through mechanistic understanding. By identifying semantic circuits via sparse autoencoders and coordinating multi-layer interventions using geometric alignment, the method achieves:

- **Superior fluency preservation** (lowest perplexity increase across all settings)
- **Broader effectiveness** (works on complex behaviors where single-layer methods fail)
- **Training-free deployment** (no model retraining required)
- **Interpretable control** (we understand what circuits we're manipulating)

For xAI researchers, CircuitSteer demonstrates the power of mechanistic interpretability as a foundation for model understanding and control. For practitioners deploying large language models, it offers practical tools for behavior customization without expensive fine-tuning.

The work reveals fundamental principles about multi-layer neural computation—that geometric alignment of representations across layers is key to coherent information flow and controllability. These principles likely extend far beyond steering, with implications for understanding, designing, and controlling neural systems.

---

## Document Metadata

- **Created:** October 18, 2026
- **Paper Version:** arXiv v1 (submitted August 6, 2026)
- **Document Status:** Comprehensive technical documentation
- **xAI Subfield:** Mechanistic Interpretability (Steering & Control)
- **Related Subfields:** Model Control, Activation Intervention, Sparse Autoencoders
