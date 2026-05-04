# How Language Models Process Out-of-Distribution Inputs: A Two-Pathway Framework

## Executive Summary

This paper reveals that existing out-of-distribution (OOD) detection methods for large language models are fundamentally confounded by sequence length, a factor that cannot be ignored through simple filtering. The authors propose a two-pathway framework that separates OOD detection into two complementary mechanisms: embedding-based methods that detect topic shifts, and processing-trajectory methods that identify adversarial or covert-intent inputs. This framework explains why different OOD detection methods excel on different types of distribution shifts and provides a principled approach to robust OOD detection.

## Problem Statement

Recent white-box OOD detection methods for LLMs—including CED, RAUQ, and WildGuard confidence scores—appear effective in initial evaluations but contain a critical structural flaw: they are confounded by sequence length. When evaluation protocols control for length, these methods collapse to near-random performance. This reveals a fundamental issue: existing approaches cannot distinguish genuine OOD signals from artifacts introduced by varying input lengths.

The core challenge is understanding how LLMs actually process out-of-distribution inputs. Current methods lack a principled framework for decomposing the different types of OOD detection problems (topic shifts vs. adversarial inputs) and fail to identify which model components genuinely signal OOD behavior.

## Core Concepts & Theory

### The Confounding Problem

**Sequence Length Artifact:**
- Attention mechanisms have logarithmic dependence on input sequence length
- Longer sequences produce systematically different attention patterns
- OOD detection methods unknowingly exploit these length-dependent patterns
- Length-matched evaluation reveals that most methods perform near chance

### Two-Pathway Framework

The paper identifies two distinct detection pathways:

**1. Embedding Pathway (What the text is about):**
- Operating at the token embedding layer
- Captures semantic content and topical information
- Effective for detecting vocabulary-distinctive OOD inputs
- Uses k-NN methods on embedding space
- Excels when OOD inputs use distinct vocabulary

**2. Processing Trajectory Pathway (How the model processes input):**
- Operates across hidden state evolution through transformer layers
- Captures layer-by-layer transformation of representations
- Detects covert-intent and adversarial inputs
- Particularly effective for OOD that shares vocabulary with in-distribution
- Reveals how attention circuits engage differently for adversarial content

### Vocabulary-Transparency Spectrum

OOD examples fall along a spectrum:
- **Vocabulary-Distinctive OOD**: Uses novel words/phrases not in training distribution (easy for embedding methods)
- **Vocabulary-Transparent OOD**: Uses in-distribution vocabulary but with adversarial intent (requires trajectory analysis)
- **Covert-Intent OOD**: Semantically innocuous text designed to cause harmful model behavior

## Main Ideas & Key Contributions

1. **Length Confounding Diagnosis**: Identifies and demonstrates that sequence length is a critical confounding factor in existing OOD detection methods through rigorous length-matched evaluation protocols

2. **Processing Trajectory Discovery**: Shows that hidden-state evolution across layers contains genuine OOD signals independent of length artifacts. Layer-0 k-NN signals are almost entirely length-based artifacts, while later layers develop genuine OOD detection capability

3. **Crossover Phenomenon**: Demonstrates empirical crossover between k-NN (embedding) and trajectory-based methods across 6 different OOD detection tasks. Each pathway wins on different OOD types, providing evidence for complementarity

4. **Circuit Attribution Analysis**: Using mechanistic interpretability techniques, identifies that adversarial OOD detection specifically engages attention circuits, while semantic tasks broadly distribute across circuits

5. **Practical Detection Framework**: Provides practitioners with clear guidance on when to use each detection pathway and how to combine them for robust OOD detection

## Methodology & Implementation

### Experimental Design

**OOD Detection Tasks:**
1. Topic shift detection (FOIL-MT, FOIL-SO)
2. Semantic adversarial examples
3. Jailbreak prompt detection
4. Out-of-context examples
5. Covert adversarial intent
6. Distribution shift benchmarks

**Length-Matched Evaluation:**
- Original evaluation: uncontrolled sequence lengths (confounded)
- Length-matched evaluation: control for length distribution
- This reveals true OOD signal vs. length artifacts

**Models Tested:**
- Modern LLMs (Llama, GPT-series)
- Various model sizes to test scalability
- Both base and instruction-tuned variants

### Key Measurements

**Detection Metrics:**
- AUROC (Area Under Receiver Operating Characteristic)
- AUPR (Area Under Precision-Recall curve)
- Threshold-dependent metrics for practical deployment

**Statistical Analysis:**
- Per-layer analysis (showing layer-0 collapse to chance)
- Per-token analysis (identifying which parts of inputs trigger OOD signals)
- Circuit attribution (mechanistic interpretability)

### Datasets

- **FOIL-MT/FOIL-SO**: Topic shift benchmarks
- **SQuAD Adversarial**: Adversarial examples on reading comprehension
- **JailBreak Datasets**: Prompts designed to elicit harmful outputs
- **Standard Distribution Shift**: Established OOD benchmarks

## Practical Applications & Real-World Use Cases

1. **Safety-Critical LLM Deployment**: Identifying adversarial and jailbreak attempts in production systems. The trajectory pathway is particularly valuable for detecting covert-intent inputs that use normal vocabulary

2. **Content Moderation**: Distinguishing between topic shifts (often benign) and potentially harmful adversarial inputs. Different pathways can be weighted based on moderation policies

3. **Adaptive Uncertainty Quantification**: Using two-pathway predictions to provide confidence estimates that account for different types of distribution shifts, enabling systems to defer to humans appropriately

4. **Fine-tuning Safety**: Understanding which types of OOD the model struggles with helps prioritize additional training or alignment efforts

5. **Robustness Evaluation**: Companies benchmarking LLMs can use this framework to comprehensively evaluate OOD robustness across multiple dimensions

6. **Efficient Filtering**: Trajectory-based methods can be applied selectively to suspicious inputs after embedding-based filtering, creating a tiered detection system

## Insights & Implications

### Broader Field Impact

- **Methodological Rigor**: Demonstrates the critical importance of proper baselines and control conditions in ML safety research. Length-matched evaluation should be standard practice
- **Mechanistic Understanding**: Shows that interpretability tools (circuit analysis) can validate and explain OOD detection mechanisms
- **Framework Transferability**: The two-pathway decomposition likely applies beyond LLMs to other neural architectures and modalities

### Understanding Model Robustness

- **Multiple Vulnerability Types**: Models can be vulnerable to different types of distribution shifts in different ways
- **Layer-Specific Behavior**: OOD signal emergence across layers reveals different processing stages with distinct capabilities
- **Attention Role**: Attention circuits are particularly important for detecting adversarial/covert-intent OOD, suggesting they are key to robustness

### Limitations & Open Questions

- **Generalization**: Does the two-pathway framework hold across very different architectures (SSMs, hybrids)?
- **Scalability**: How does the phenomenon scale to much larger models where layer dynamics differ?
- **Real-world Performance**: Evaluation on synthetic OOD; how well does this transfer to naturally occurring distribution shifts?
- **Deployment Tradeoffs**: Trajectory-based detection is more expensive computationally; what are practical deployment tradeoffs?

### Future Directions

- Integrate two-pathway framework into defenses (adversarial training, prompt engineering)
- Investigate why trajectory methods are particularly effective for attention-based adversarial detection
- Extend framework to other modalities (vision, multimodal)
- Study how pathway effectiveness evolves during model training and fine-tuning
- Develop more efficient trajectory analysis methods for production systems

## Code & Resources

**Paper:**
- ArXiv: [https://arxiv.org/abs/2605.00269](https://arxiv.org/abs/2605.00269)
- Published: April 30, 2026

**Author:**
- Hamidreza Saghir

**Dependencies:**
- PyTorch or JAX
- HuggingFace Transformers library
- Standard NLP evaluation tools
- Mechanistic interpretability libraries (for circuit analysis)

**Computational Requirements:**
- GPU inference: A100/H100 for rapid evaluation
- Storage: Models range from 7B to 70B parameters
- Analysis: Per-layer attention computation significant but manageable

**Implementation Considerations:**
- k-NN methods require efficient nearest-neighbor search (FAISS, etc.)
- Trajectory analysis benefits from GPU-accelerated batch processing
- Length-matched evaluation requires careful data preprocessing

## Related Work & Context

### OOD Detection in Machine Learning

- **Baseline OOD Methods**: Maximum softmax probability, ODIN, Mahalanobis distance
- **LLM-Specific OOD**: Recent work on LLM OOD detection (RAUQ, WildGuard, CED)
- **Adversarial Robustness**: Foundational work on adversarial examples and model robustness

### Mechanistic Interpretability

- **Sparse Autoencoders**: Understanding learned features in LLMs
- **Circuit Analysis**: Isolating specific learned behaviors to attention heads and MLP layers
- **Activation Analysis**: Understanding how information transforms across layers

### Safety and Alignment

- **Jailbreak Detection**: Methods for identifying adversarial prompts
- **Content Moderation**: Systems for identifying harmful outputs
- **Alignment Research**: Understanding model behavior on out-of-training-distribution tasks

### Related Recent Papers

- **LLMs for OOD Detection Survey** (2409.01980): Comprehensive overview of OOD methods for LLMs
- **Embedding Trajectory for Mathematical Reasoning** (2405.14039): Similar trajectory-based analysis in different domain
- **Procedural Execution in LLMs** (2605.00817): Related analysis of how LLMs process structured inputs

## Conclusions

This paper makes a critical methodological contribution to LLM safety research by identifying a widespread confound (sequence length) and proposing a principled framework for decomposing OOD detection. The two-pathway framework—separating embedding-based and trajectory-based detection—explains empirical phenomena and provides actionable guidance for practitioners building safer LLM systems. The work exemplifies how careful experimental design and mechanistic analysis can reveal fundamental truths about model behavior.

## References

- Saghir, H. (2026). How language models process out-of-distribution inputs: A two-pathway framework. *arXiv preprint arXiv:2605.00269*.
- Hendrycks, D., & Gimpel, K. (2016). A baseline for detecting misclassified and out-of-distribution examples in neural networks. *ICLR*.
- Wang, X., Wang, B., Huang, Z., & Su, Y. (2024). Do llms build spatial world models? Evidence from grid-based reference games. *arXiv preprint arXiv:2604.10690*.
