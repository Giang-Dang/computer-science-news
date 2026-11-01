# ConceptX: Concept-Level Explainability for Auditing & Steering LLM Responses

**ArXiv ID:** [2505.07610](https://arxiv.org/abs/2505.07610)

**Authors:** Kenza Amara, Rita Sevastjanova, Mennatallah El-Assady

**Submission Date:** May 12, 2025

**Venue:** NeurIPS 2025

---

## Executive Summary

ConceptX introduces a model-agnostic method for generating concept-level explanations of large language model (LLM) outputs through Shapley-based coalitional sampling over semantic concepts. Rather than explaining predictions at the token level, ConceptX operates at the concept level—measuring how changes in user-provided or automatically-detected concepts shift the semantic similarity of LLM responses. This approach enables both auditing of LLM behavior and steering of outputs toward desired properties (sentiment, harmlessness) without model retraining.

---

## Problem Statement

Existing explanation methods for LLMs predominantly operate at the token level, analyzing the contribution of individual tokens to model predictions. Token-level methods like TokenSHAP suffer from several critical limitations:

1. **Lack of semantic coherence:** Individual tokens do not correspond to interpretable units of meaning; users reason about concepts (topics, entities, properties) rather than individual tokens.

2. **Limited human alignment:** Token-level explanations often include function words (prepositions, articles, conjunctions) that contribute little semantic value and confuse human understanding.

3. **Insufficient granularity for intervention:** Token-level attribution does not directly support concept-level steering—practitioners cannot easily modify abstract ideas in a prompt and observe effects on output properties.

4. **Scalability challenges:** Existing attribution methods become computationally expensive when applied to long prompts and diverse output dimensions (sentiment, toxicity, fairness).

Prior work on concept-based explanations (e.g., TCAV, ACE) primarily targets vision models, and their extension to LLMs remains underdeveloped. Concept Bottleneck Models (CBMs) provide interpretability but require models to be explicitly trained with concept supervision—a constraint inapplicable to pre-trained LLMs.

ConceptX addresses this gap by providing a model-agnostic, post-hoc method for concept-level explanations that:
- Operates on semantic concepts rather than tokens
- Scales to practical LLM use cases
- Directly enables both diagnosis (understanding) and intervention (steering)

---

## Core Concepts & Theory

### Concept-Based Attribution via Shapley Values

ConceptX builds on the Shapley value framework—a cooperative game-theory approach for fairly distributing credit among contributors. Traditional Shapley attribution assigns importance to individual features; ConceptX extends this to concepts.

**Shapley Value Definition (Informal):**
For a feature or concept's contribution to a prediction, the Shapley value is the average marginal contribution of that feature when added to all possible subsets of other features:

```
φ(i) = (1/|S|!) Σ [v(S ∪ {i}) - v(S)]
```

where v(S) is the value (utility) of subset S, and the sum averages over all orderings.

**ConceptX's Approach:**
1. **Coalitional Sampling:** Rather than enumerate all 2^n subsets of concepts (intractable for large concept sets), ConceptX samples coalitions uniformly at random and approximates Shapley values via Monte Carlo.

2. **Concept Definition:** A concept is a set of semantically related words identified from the prompt. ConceptX uses ConceptNet to group words by semantic similarity and filters out function words.

3. **Utility Function:** The utility v(S) is the cosine similarity between:
   - The LLM response obtained when concepts in coalition S are present in the prompt
   - A target response or target property (e.g., "benign," "positive sentiment")

4. **Importance Score:** Each concept's importance is the difference in mean cosine similarity when the concept is included vs. excluded across sampled coalitions.

### Connection to Game Theory

The Shapley value is the unique solution that satisfies:
- **Symmetry:** Features with identical contributions receive equal importance
- **Efficiency:** Importance scores sum to the total value gained
- **Null Player:** Features that do not affect predictions receive zero importance
- **Additivity:** The method respects linear combinations of value functions

By grounding concept attribution in Shapley values, ConceptX inherits these axiomatic guarantees, providing a principled justification for why concept importances are fair and meaningful.

### Distinction from Token-Level Methods

| Aspect | Token-Level (e.g., TokenSHAP) | Concept-Level (ConceptX) |
|--------|-----|------|
| **Unit of Attribution** | Individual tokens | Semantic concepts (groups of words) |
| **Interpretability** | Relies on linguistic knowledge to aggregate tokens into concepts | Directly interpretable to domain experts and end users |
| **Function Word Handling** | Includes prepositions, articles, conjunctions; noise | Filters function words; focuses on content |
| **Intervention Support** | Difficult to modify individual tokens and observe effects | Direct concept-level steering: remove/reweight concepts |
| **Concept Dependency** | No explicit concept model | Uses ConceptNet or user-provided concept definitions |

---

## Main Ideas & Key Contributions

### 1. Model-Agnostic Concept Attribution

ConceptX operates post-hoc on any LLM without access to weights or gradients. The method only requires:
- The LLM's API or forward pass
- A set of concepts (automatically detected or user-provided)
- A target property or reference response

This universality enables explanation of proprietary and open-source LLMs alike, making it deployable in real-world settings where model internals are unavailable.

### 2. Concept-Level Steering

Beyond diagnosis, ConceptX enables intervention:
- **Prompt Editing:** Identify harmful or undesired concepts, remove them from prompts, and observe output changes.
- **Concept Weighting:** Upweight beneficial concepts or downweight harmful ones without prompt modification.
- **No Retraining:** All interventions operate at the input level; the LLM remains unchanged.

**Empirical Finding:** On Mistral-7B, removing the top harmful concept in adversarial prompts roughly halved the attack success rate, demonstrating the method's practical effectiveness.

### 3. Faithfulness and Human Alignment

ConceptX is evaluated against token-level baselines (TokenSHAP) on:
- **Faithfulness:** How well an explanation predicts the true model behavior when features are perturbed.
- **Human alignment:** Agreement with human judgments of importance for the same concepts.

**Key Result:** Across three LLMs (GPT-3.5, Mistral-7B, Llama-2), ConceptX consistently outperforms TokenSHAP on both metrics. Human raters prefer concept-level explanations over token-level attributions.

### 4. Concept Robustness

ConceptX's explanations remain stable under minor variations to the prompt (e.g., paraphrasing, synonym substitution). This robustness indicates that the method captures meaningful semantic relationships rather than superficial token statistics.

---

## Methodology & Implementation

### Concept Detection & Representation

**Automatic Concept Extraction:**
1. Tokenize the input prompt
2. Filter out function words (articles, prepositions, conjunctions, auxiliary verbs) using a predefined stop-word list
3. Group remaining tokens by semantic similarity using ConceptNet embeddings
4. Assign a label to each group (e.g., "positive sentiment," "entity type")

**User-Provided Concepts:**
Users can manually specify concepts of interest (e.g., for domain-specific auditing).

**Concept Vectors:**
Each concept is represented as an aggregation of its constituent word embeddings (e.g., mean pooling).

### Coalitional Sampling Procedure

```
Algorithm: ConceptX Explanation

Input:
  - Prompt p
  - LLM F
  - Target property or response t
  - Concepts C = {c1, c2, ..., cn}
  - Number of samples M
  
Output:
  - Importance scores φ(ci) for each concept ci

for m = 1 to M:
  S_m ← sample random subset of C uniformly
  response_S ← F(prompt with concepts S_m active)
  similarity_S ← cosine_similarity(response_S, target_t)
  
  for each concept c in C:
    if c in S_m:
      coalition_with := S_m
      coalition_without := S_m \ {c}
      value_with ← cosine_similarity(F(p | coalition_with), t)
      value_without ← cosine_similarity(F(p | coalition_without), t)
      φ(c) += (value_with - value_without) / M

Return φ
```

### Evaluation Metrics

**Faithfulness (Input Perturbation Fidelity):**
- Rank concepts by importance according to ConceptX
- Iteratively remove top concepts from the prompt
- Measure how rapidly the LLM's output diverges from the original
- If importance scores are faithful, important concepts' removal should cause larger output shifts

**Human Alignment:**
- Show human raters two LLM responses and a prompt
- Ask which concepts are most important for explaining the LLM's output
- Compare human judgments to ConceptX rankings

**Computational Efficiency:**
- Number of LLM forward passes required scales with M (number of Monte Carlo samples)
- Typical configurations: M ∈ {100, 500, 1000} depending on desired accuracy
- [Exact figures unavailable — see full paper] for detailed runtime comparisons

### Limitations

1. **Computational Cost:** Shapley value estimation via Monte Carlo remains expensive; M = 1000 samples may require thousands of forward passes, limiting real-time deployment.

2. **Concept Definition Dependency:** Explanation quality depends critically on concept definitions. Poor automatic concept detection (e.g., missing domain-specific terms) degrades explanation quality.

3. **Limited Scalability to Long Prompts:** For prompts with hundreds of distinct concepts, sampling becomes less effective. The method has not been demonstrated on very long documents (e.g., >10,000 tokens).

4. **Concept Granularity Trade-offs:** Coarse-grained concepts may obscure important details; fine-grained concepts increase computational cost and reduce interpretability.

5. **Target Property Specification:** The method requires explicit definition of the target property or reference response. Vague targets (e.g., "more informative") are difficult to operationalize.

---

## Practical Applications & Real-World Use Cases

### 1. Safety and Adversarial Robustness

**Use Case:** Defending LLMs against jailbreak attacks.

**Application:**
- Identify which concepts in adversarial prompts are responsible for harmful outputs
- Remove or downweight these concepts to mitigate attacks
- Monitor high-risk concepts in user-submitted content

**Real Impact:** Removing the top harmful concept in Mistral-7B adversarial prompts reduced attack success rate by ~50%, demonstrating practical defensive value.

### 2. Compliance and Auditing

**Use Case:** Meeting regulatory requirements (GDPR, AI Act, FDA guidance on AI) for explainability.

**Application:**
- Audit LLM outputs for bias, fairness violations, or unintended dependencies
- Identify which user-provided concepts drive biased predictions
- Generate explanations for high-stakes decisions (credit approval, medical recommendations)

**Regulatory Benefit:** Concept-level explanations align with human reasoning and support audit trails; they are more suitable for compliance documentation than token-level attributions.

### 3. Output Steering Without Retraining

**Use Case:** Customizing LLM behavior for specific organizations without fine-tuning.

**Application:**
- Detect concepts that trigger unwanted behaviors (e.g., promotional language, sensitive topics)
- Modify prompts in real-time to avoid these concepts
- Upweight desired concepts to encourage beneficial outputs (e.g., empathy, specificity)

**Operational Benefit:** Fast iteration and deployment; no need for model retraining or GPU resources.

### 4. Interactive Debugging and Improvement

**Use Case:** Data science teams improving prompt quality and LLM behavior.

**Application:**
- Iteratively inspect concept importances
- A/B test prompt variations by modifying important concepts
- Identify weak spots in LLM reasoning (e.g., concepts the model relies on but shouldn't)

**Example:** A chatbot development team detects that the LLM relies heavily on "financial advice" concepts in casual conversations, leading to inappropriate suggestions. They modify prompts to de-emphasize these concepts, improving conversation quality.

### 5. Transparency and Trust

**Use Case:** Building user trust in AI systems.

**Application:**
- Display concept-level explanations to end users (e.g., in customer support chatbots)
- Explain why an LLM provided a specific recommendation or answer
- Allow users to challenge explanations ("Why did you emphasize X concept?")

**User Benefit:** Improves perceived fairness and reduces "black box" concerns.

---

## Insights & Implications

### Advances in xAI Theory

1. **Bridging Concept and Token Explanations:** ConceptX demonstrates that Shapley-based attribution can be elevated from tokens to meaningful semantic units, potentially inspiring similar approaches in other domains (vision, speech).

2. **Axiomatic Foundation for Concept Attribution:** By grounding explanations in Shapley values, the work provides theoretical justification for fairness and uniqueness properties, distinguishing it from ad-hoc concept importance measures.

3. **Post-hoc Explainability Without Concept Supervision:** Unlike Concept Bottleneck Models, ConceptX does not require retraining with concept labels, making it immediately applicable to existing LLMs.

### Limitations and Open Questions

1. **Sampling Efficiency:** Current Monte Carlo sampling for Shapley values is computationally expensive. Future work might explore variance reduction techniques or approximation algorithms that are faster without sacrificing quality.

2. **Concept Granularity and Automation:** Automatic concept detection remains a bottleneck. How can we automatically discover task-relevant concept hierarchies? How do we avoid over-fragmentation (too many fine-grained concepts) or under-specification (too few coarse concepts)?

3. **Dynamic Concepts:** Do concept importances vary across output length, LLM temperature, or output style? How stable are explanations across different runs of the same LLM?

4. **Compositionality:** Can concepts be composed or negated in ways that explain complex LLM behavior? E.g., does "concept A AND NOT concept B" matter more than individual concepts?

5. **Generalization Across Models:** Do explanation rankings transfer across different LLMs, or are they model-specific? This matters for building reusable explanation benchmarks.

### Impact on Trustworthy AI

- **Explainability:** ConceptX advances explainability by operating at a semantic level humans naturally reason about, unlike token-level methods.
- **Auditability:** Concept-level explanations support systematic audits of LLM behavior, aiding compliance with emerging AI regulations.
- **Control:** The steering capabilities provide practitioners with actionable levers to improve LLM behavior, advancing the goal of controlled AI deployment.
- **Fairness:** By identifying concept-driven biases, organizations can detect and mitigate fairness issues before deployment.

### Future Research Directions

1. **Efficiency Improvements:** Develop faster Shapley approximations tailored to language models (e.g., by exploiting LLM structure or fine-tuning).

2. **Concept Learning:** Automatically discover optimal concept hierarchies from data, rather than relying on ConceptNet or manual specification.

3. **Causal Concept Analysis:** Combine ConceptX with causal inference to distinguish correlation (which concepts are important) from causation (which concepts actually cause outputs).

4. **Multi-output Explanations:** Extend the method to explain multiple output properties simultaneously (e.g., helpfulness + safety + fairness).

5. **Integration with Mechanistic Interpretability:** Combine concept-level explanations with mechanistic interpretability techniques (e.g., circuit analysis) to understand how internal LLM mechanisms implement concept-level reasoning.

---

## Code & Resources

**Official Implementation:**
- GitHub Repository: [github.com/k-amara/ConceptX](https://github.com/k-amara/ConceptX)
- License: [Check repository for license terms]

**Paper and Documentation:**
- ArXiv PDF: [arXiv:2505.07610](https://arxiv.org/abs/2505.07610)
- ArXiv HTML: [ar5iv.labs.arxiv.org/html/2505.07610](https://ar5iv.labs.arxiv.org/html/2505.07610)

**Dependencies:**
- Python 3.8+
- PyTorch
- Hugging Face Transformers (for LLM access)
- ConceptNet (for concept embeddings)
- NumPy, Pandas (for data processing)

**Computational Requirements:**
- GPU recommended for LLM inference (required for practical sampling with large M)
- Memory: ~8–16 GB for typical LLM models
- Runtime: [Exact figures unavailable — see full paper] — expect M × (LLM inference time) for explanation generation

**Quick Start:**
```python
from conceptx import ConceptX
import torch

# Initialize ConceptX
explainer = ConceptX(
    model_name="mistralai/Mistral-7B-Instruct-v0.1",
    concept_source="auto"  # or "user_provided"
)

# Generate explanation
prompt = "How should I invest my savings?"
target = "conservative financial advice"
importances = explainer.explain(
    prompt=prompt,
    target=target,
    num_samples=500
)

# Steer LLM output
modified_prompt = explainer.steer(
    prompt=prompt,
    top_harmful_concepts=3,
    action="remove"
)
```

**Interactive Visualizations (if provided):**
- [Check paper for interactive demo links] — some venues (e.g., NeurIPS workshops) include browser-based visualizations

---

## Related Work & Context

### Concept-Based Explanation Methods

**Prior Art:**
- **TCAV (Testing with Concept Activation Vectors)** (Kim et al., 2018): Pioneered concept-based explanations for vision models; requires user-defined concepts and model gradients.
- **ACE (Automated Concept-based Explanations)** (Ghorbani et al., 2019): Automatically discovers concept-like features in CNNs; extends TCAV but remains computationally expensive.
- **Concept Bottleneck Models (CBMs)** (Koh et al., 2020): Train models to explicitly predict concepts before predictions; provides interpretability but requires concept-labeled data.

**ConceptX's Innovation:** Post-hoc, model-agnostic, and directly applicable to pre-trained LLMs without retraining or concept supervision.

### Feature Attribution Methods

**Token-Level Baselines:**
- **LIME (Local Interpretable Model-agnostic Explanations)** (Ribeiro et al., 2016): Creates local linear approximations; influenced by SHAP but less principled.
- **SHAP (SHapley Additive exPlanations)** (Lundberg & Lee, 2017): Unifies multiple attribution methods under Shapley values; computational cost limits practical use for high-dimensional data.
- **TokenSHAP** (for LLMs): Applies SHAP at the token level; suffers from lack of semantic coherence.
- **Attention-based methods** (e.g., Attention Rollout): Use attention weights as proxies for importance; recent work (Jain & Wallace, 2019) questions their faithfulness.

**ConceptX as an Evolution:** Lifts token-level Shapley attribution to concepts, improving interpretability while retaining axiomatic guarantees.

### Concept-Based Learning and Steering

**Related Approaches:**
- **Prompt Engineering:** Ad-hoc methods for modifying prompts; lack principled importance guidance.
- **Instruction Fine-tuning:** Can modify LLM behavior but requires labeled data and computational resources.
- **In-context Learning:** Uses examples to steer outputs; complementary to ConceptX (can combine both).
- **Concept-based Prompt Templates:** Some practitioners manually identify important concepts; ConceptX automates this.

**Synergies:** ConceptX can inform prompt engineering by identifying which concepts matter most; the steering capability can be combined with in-context learning for further customization.

### Mechanistic Interpretability and LLM Internals

**Related Directions:**
- **Circuit Analysis** (Zoom et al., 2023; Wang et al., 2023): Identify interpretable subgraphs in neural networks.
- **Activation Patching / Causal Tracing** (Meng et al., 2023): Intervene on internal activations to understand model behavior.
- **SAEs (Sparse Autoencoders)** (Cunningham et al., 2023): Decompose hidden states into interpretable features.

**Complementarity:** ConceptX operates at the input/output level; mechanistic methods operate at the internal level. Combining both could yield richer understanding (e.g., which internal mechanisms implement concept-driven reasoning).

### Fairness and Trustworthy AI Standards

**Regulatory Context:**
- **GDPR Article 22:** Right to explanation for automated decision-making; ConceptX supports compliance through interpretable, human-aligned explanations.
- **EU AI Act:** Requires high-risk AI systems to be interpretable; concept-level explanations satisfy explainability mandates better than token-level methods.
- **FDA Guidance on AI/ML Software as a Medical Device:** Encourages human-interpretable explanations; ConceptX aligns with these recommendations.

**Practical Standards:**
- ConceptX's ability to generate human-aligned explanations and steer behavior directly addresses regulatory mandates for transparency and control.

### xAI Community Connections

**LIME/SHAP Ecosystem:**
- ConceptX extends the Shapley-based explanation paradigm to concepts, bringing Shapley's rigor to concept attribution.

**Concept Activation Vector Community:**
- ConceptX complements CAV-style approaches by providing a post-hoc, data-agnostic alternative to learning concept directions from data.

**Mechanistic Interpretability (MI) Movement:**
- While MI focuses on internal circuits, ConceptX's input-level analysis provides a complementary lens: what external (prompt-level) concepts matter most?

**Steering and Control:**
- Part of the broader movement toward controllable AI systems; aligns with work on constrained decoding, preference optimization, and alignment research.

---

## Summary Table

| Aspect | Details |
|--------|---------|
| **Paper Title** | ConceptX: Concept-Level Explainability for Auditing & Steering LLM Responses |
| **Authors** | Kenza Amara, Rita Sevastjanova, Mennatallah El-Assady |
| **ArXiv ID** | 2505.07610 |
| **Submission Date** | May 12, 2025 |
| **Venue** | NeurIPS 2025 |
| **Key Innovation** | Shapley-based concept-level attribution with steering capabilities |
| **xAI Subfield** | Concept-Based Explanations |
| **Main Contribution** | Post-hoc, model-agnostic concept attribution and LLM behavior steering without retraining |
| **Evaluation** | Faithfulness (input perturbation), human alignment studies across GPT-3.5, Mistral-7B, Llama-2 |
| **Primary Use Case** | Auditing and steering LLMs for safety, fairness, and compliance |
| **Code Availability** | [github.com/k-amara/ConceptX](https://github.com/k-amara/ConceptX) |

---

## References

1. **ConceptX Paper:** Amara, K., Sevastjanova, R., & El-Assady, M. (2025). ConceptX: Concept-Level Explainability for Auditing & Steering LLM Responses. In *Advances in Neural Information Processing Systems (NeurIPS 2025)*.

2. **Shapley Values:** Shapley, L. S. (1953). A value for n-person games. *Contributions to the Theory of Games*, 2(28), 307–317.

3. **SHAP:** Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems (NeurIPS)*, 30.

4. **TCAV:** Kim, B., Wattenberg, M., Gilmer, J., Cai, C., Wexler, J., Viegas, F., & Sayres, R. (2018). Interpretability beyond feature attribution: Quantitative testing with concept activation vectors. *Proceedings of the International Conference on Machine Learning (ICML)*.

5. **ConceptNet:** Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual graph of general knowledge. In *AAAI Conference on Artificial Intelligence*.

6. **Concept Bottleneck Models:** Koh, I., Sagawa, S., Marklund, H., Xie, S. M., Zhang, M., Balsubramanian, A., ... & Liang, P. (2020). Concept bottleneck models. *International Conference on Machine Learning (ICML)*.
