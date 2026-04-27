# LASA: Language-Agnostic Semantic Alignment at the Semantic Bottleneck for LLM Safety

**ArXiv ID:** [2604.12710](https://arxiv.org/abs/2604.12710)  
**Published:** April 14, 2026  
**Authors:** Junxiao Yang, Haoran Liu, Jinzhe Tu, Jiale Cheng, Zhexin Zhang, Shiyao Cui, Jiaqi Weng, Jialing Tao, Hui Xue, Hongning Wang, Han Qiu, Minlie Huang  
**Field:** AI Safety / Natural Language Processing  

---

## Executive Summary

LASA addresses a critical but underappreciated safety vulnerability in large language models: **multilingual safety alignment failures**. Models aligned to refuse harmful requests in English often comply with identical requests posed in low-resource languages (Swahili, Bengali, Yoruba, etc.), with attack success rates as high as 24.7%. LASA identifies the root cause—alignment training is biased toward high-resource language representations—and proposes anchoring safety alignment at the *semantic bottleneck*: an intermediate layer where cross-lingual representations converge. The result is a dramatic reduction in multilingual attack success rate from 24.7% to **2.8%** on LLaMA-3.1-8B-Instruct.

---

## Problem Statement

Modern LLM safety alignment (RLHF, DPO, Constitutional AI) is predominantly trained on English data. While models often generalize basic instruction-following to other languages, **safety refusals do not generalize comparably**. This creates an attack surface:

- A request like "How do I synthesize methamphetamine?" is refused in English
- The same request in Yoruba, Swahili, or even Russian may be answered

This is not a hypothetical threat. Studies have shown that safety-aligned models can be "jailbroken" simply by asking in low-resource languages, without any adversarial prompting tricks.

### Why Does This Happen?

The conventional explanation is "insufficient multilingual training data for safety." LASA provides a more precise structural explanation:

1. LLMs develop **language-agnostic semantic representations** in intermediate layers — the model's internal understanding of meaning transcends language
2. Safety alignment, however, is applied at the **language-dominant layers** (closer to the output) where English-specific surface patterns dominate
3. The result: semantic understanding is language-agnostic, but safety refusal mechanisms are language-specific

This is the fundamental mismatch LASA identifies and resolves.

---

## Core Concepts & Theory

### The Semantic Bottleneck

Through probing experiments on the internal representations of LLMs, the authors identify a specific layer range — the **semantic bottleneck** — where:

1. Representations from different languages (for the same semantic content) are geometrically *closest* to each other (low cross-lingual distance)
2. Representations for different semantic content are geometrically *most separated* (high inter-class distance)

Formally, the semantic bottleneck layer `l*` satisfies:

```
l* = argmin_l d_lang(h_l(x_en), h_l(x_fr))  
              while maximizing d_sem(h_l(x_safe), h_l(x_harmful))
```

Where:
- `h_l(x)` = hidden representation of text `x` at layer `l`
- `d_lang` = distance between same-meaning texts in different languages
- `d_sem` = distance between safe and harmful content

This is analogous to how vision transformers develop object-centric representations in intermediate layers while early and late layers are more feature/class-specific.

### Why Align at the Semantic Bottleneck?

Safety alignment applied at the semantic bottleneck operates on **language-independent semantic content**, meaning:
- A refusal trained for English harmful content generalizes to the same harmful content in all languages
- The model learns "this semantic concept is harmful" rather than "this English phrase is harmful"

### LASA: The Alignment Method

LASA injects safety alignment directly at the semantic bottleneck layer via:

1. **Bottleneck identification**: Automated layer selection using cross-lingual representation similarity metrics
2. **Semantic-level contrastive training**: Training a safety classifier/refusal mechanism that operates on semantic bottleneck representations
3. **Gradient-based anchoring**: Regularizing the model's fine-tuning to maintain semantic bottleneck representations while learning safety refusals

The training objective:

```
L_LASA = L_safety + λ · L_semantic_consistency
```

Where:
- `L_safety` = standard safety alignment loss (refusal reward, harmfulness penalty)
- `L_semantic_consistency` = KL divergence between bottleneck representations before and after fine-tuning (prevents catastrophic forgetting of language-agnostic features)

---

## Main Ideas & Key Contributions

### 1. Empirical Identification of the Semantic Bottleneck

The paper provides the first systematic empirical characterization of the semantic bottleneck in LLMs and demonstrates that it exists consistently across model families (LLaMA, Qwen) and sizes (7B-32B).

### 2. Structural Diagnosis of Multilingual Safety Failures

LASA provides a mechanistic explanation for why current safety alignment fails multilingually: the mismatch between where semantic understanding occurs (semantic bottleneck) and where safety is enforced (output layers with English bias).

### 3. LASA Alignment Procedure

A practical method to anchor safety alignment at the semantic bottleneck, eliminating the language-specific bias. The procedure is efficient and can be applied as a post-processing step on top of existing safety-aligned models.

### 4. Comprehensive Cross-Lingual Safety Evaluation

The paper evaluates safety across 20+ languages spanning multiple scripts and resource levels, providing a rigorous benchmark for multilingual safety.

---

## Methodology & Implementation

### Bottleneck Identification Protocol

1. Sample 1000 sentence pairs: (same meaning, different languages)
2. Compute pairwise representation distances at each layer
3. Identify the layer with minimum cross-lingual distance (semantic bottleneck)

This protocol is model-agnostic and takes ~1 GPU-hour.

### Safety Alignment at the Bottleneck

LASA uses a lightweight intervention: a **safety projection layer** inserted at the semantic bottleneck that maps harmful semantic representations to a "safe" subspace, while leaving benign representations unchanged:

```
h_l*_safe = P_safe · h_l* + (I - P_safe) · h_l*  
           = h_l*  for benign content
           = refusal_direction  for harmful content
```

Where `P_safe` is learned via contrastive training on (harmful, benign) pairs.

### Training Data

- **Harmful content**: Standard safety datasets (AdvBench, HarmBench, WildGuard) translated to 20+ languages using high-quality MT
- **Benign content**: Instruction-following data in 20+ languages

### Evaluation

| Model | Language | Baseline ASR | LASA ASR |
|-------|----------|-------------|---------|
| LLaMA-3.1-8B-Instruct | Average (20 langs) | 24.7% | **2.8%** |
| Qwen2.5-7B-Instruct | Average (20 langs) | 18.3% | **3.1%** |
| Qwen2.5-32B-Instruct | Average (20 langs) | 15.6% | **3.8%** |
| Qwen3-7B-Instruct | Average (20 langs) | 21.2% | **3.4%** |

ASR = Attack Success Rate (lower is better). Results show consistent improvement across model families and sizes.

---

## Practical Applications & Real-World Use Cases

### 1. Global Deployment of Safety-Critical LLMs

Any LLM deployed globally — in customer service, healthcare, legal information, education — is exposed to multilingual queries. LASA makes global deployment safer by ensuring safety guarantees are not language-dependent.

### 2. Low-Resource Language Communities

Multilingual safety failures disproportionately harm communities that speak low-resource languages, as they receive less safety protection. LASA directly addresses this equity concern.

### 3. LLM Red-Teaming and Auditing

LASA's framework for measuring multilingual attack success rates provides a standardized audit protocol for LLM safety teams to assess and address multilingual safety gaps.

### 4. Regulatory Compliance

Emerging AI safety regulations (EU AI Act, etc.) are increasingly requiring that safety measures be effective across languages. LASA provides a technical path to meeting these requirements.

---

## Insights & Implications

### Safety Alignment Must Be Language-Agnostic

LASA's most important implication is that **safety alignment should be designed to be language-agnostic from the start**, rather than relying on language-by-language coverage. The semantic bottleneck provides the technical mechanism to achieve this.

### The Bottleneck as a General Alignment Target

The semantic bottleneck may be valuable beyond safety—for other forms of alignment (factuality, harmlessness, helpfulness) where we want model behavior to be consistent across surface forms of the same underlying request.

### Cross-Lingual Transfer of Values

LASA's success suggests that "values" (what is harmful, what is appropriate) can be encoded in language-agnostic representations and transferred effectively across languages through the bottleneck. This has broader implications for value alignment research.

### Limitations

- **Script-based attacks**: Adversarial inputs using unusual Unicode characters or obfuscated scripts may not be caught by semantic bottleneck alignment
- **Low-resource language quality**: MT-translated training data may not perfectly capture idiomatic harmful requests in low-resource languages
- **Dynamic harmful content**: New types of harmful content that emerge after training may not be covered

---

## Code & Resources

- **Paper (arXiv)**: [https://arxiv.org/abs/2604.12710](https://arxiv.org/abs/2604.12710)
- **OpenReview**: [https://openreview.net/pdf/65d345e79628aee6fa1493834deab1c586168fdc.pdf](https://openreview.net/pdf/65d345e79628aee6fa1493834deab1c586168fdc.pdf)
- **HuggingFace**: [https://huggingface.co/papers/2604.12710](https://huggingface.co/papers/2604.12710)

**Dependencies**:
- PyTorch, HuggingFace Transformers
- Multilingual MT system (for data translation)
- Probing toolkit for layer analysis

---

## Related Work & Context

### Prior Multilingual Safety Work
- **SORRY-Bench**: Benchmarks for safety across languages
- **Lingua-SafetyBench** (2601.22737): Multilingual safety evaluation for VLMs
- **Safety Layers in LLMs** (2408.17003): Related work on identifying safety-related layers

### Related Alignment Methods
- **DPO (Direct Preference Optimization)**: Standard alignment method, typically English-focused
- **Constitutional AI**: Rules-based alignment, mostly English
- **Lazy Safety Alignment** (2405.18641): Minimizing impact of safety alignment on general capabilities

### Future Directions
- Extension to multimodal safety (vision-language models with multilingual inputs)
- Dynamic semantic bottleneck identification as models are fine-tuned
- Combining LASA with adversarial training against cross-lingual attacks
