# nnterp: A Standardized Interface for Mechanistic Interpretability of Transformers

**Authors:** Clément Dumas  
**ArXiv ID:** [2511.14465](https://arxiv.org/abs/2511.14465)  
**Submitted:** November 18, 2025 (Revised: December 14, 2025)  
**Field:** Mechanistic Interpretability, Transformer Analysis, Standardized Interfaces

## Executive Summary

This paper introduces **nnterp**, a lightweight, unified library that solves a critical infrastructure problem in mechanistic interpretability research: the lack of standardization across transformer architectures. By providing a consistent API that works identically across 50+ model variants from 16 different architecture families while preserving exact HuggingFace behavior, nnterp enables researchers to write interpretability code once and deploy it across diverse models. This addresses the fundamental tradeoff between custom implementations (which provide consistent interfaces but introduce numerical mismatches) and direct HuggingFace access (which preserves behavior but lacks standardization).

## Problem Statement

### The Standardization Crisis in Mechanistic Interpretability

Mechanistic interpretability research faces a significant infrastructure bottleneck:

**Problem 1: The Interface-Accuracy Tradeoff**
- **Custom implementations** (e.g., TransformerLens): Provide clean, consistent APIs across models but require manual implementation for each architecture, introducing numerical mismatches with original models and limiting reproducibility
- **Direct HuggingFace access** (via NNsight): Preserves exact model behavior but lacks standardization—each architecture requires different access patterns (e.g., `model.gpt2.transformer.h[i].attn.out_proj` vs `model.llama.model.layers[i].self_attn`)

**Problem 2: Code Reusability Across Architectures**
- Researchers cannot easily share intervention code that works across models
- Circuit discovery, attention analysis, and activation steering techniques must be re-implemented for each new architecture
- This creates friction in cumulative mechanistic interpretability research

**Problem 3: Reproducibility and Verification**
- Numerical mismatches between custom implementations and original models make it difficult to validate interpretability findings
- Cross-architecture studies require either accepting implementation differences or conducting entirely separate analyses

## Core Concepts & Theory

### Mechanistic Interpretability Foundations

Mechanistic interpretability seeks to understand neural networks through causal analysis of their internal computations, treating them as computational graphs where:
- **Components** (attention heads, MLPs, neurons) perform localized functions
- **Pathways** are causal routes through which information flows
- **Circuits** are minimal subgraphs sufficient to implement specific model behaviors

### Key Analysis Techniques

**Logit Lens**
- Projects hidden states at each layer through the language modeling head's unembedding
- Reveals how the model's prediction evolves across layers
- Enables identification of which layers contribute most to final predictions
- Implementation: `logits = model.unembed(hidden_state)`

**Patchscope**
- Replaces activations from one input context with activations from another
- Enables causal intervention: does changing this activation change the output?
- Distinguishes between passive storage and active computation of information
- Implementation: Copy activation from `source_context[layer]` to `target_context[layer]`

**Activation Steering**
- Adds learned or discovered steering vectors to activations at specified layers
- Enables direct control of model behavior
- Tests whether a discovered feature actually causally impacts outputs
- Implementation: `activation += steering_vector * scale_factor`

### The Standardization Challenge

Transformer architectures differ in:
- **Module naming conventions**: `gpt2.transformer.h[i]` vs `llama.model.layers[i]`
- **Attention access patterns**: Hidden states may be fused (GPT-2) or separate (LLaMA)
- **MLP structure**: Dense → activation → dense vs variations in intermediate dimensions
- **Special modules**: Some models have RMSNorm, others have LayerNorm; some use rotary positional embeddings

Implementing a single analysis method across just 10 models requires 10 separate implementations, each with potential for bugs and mismatches.

## Main Ideas & Key Contributions

### 1. Unified API Through Module Renaming

nnterp provides a **consistent hierarchical access pattern**:

```python
model.layers[layer_idx].attn  # Attention module
model.layers[layer_idx].mlp   # MLP module
model.layers[layer_idx].attn.out_proj  # Attention output projection
model.layers[layer_idx].embedding  # Token/positional embeddings (where supported)
```

This works identically across GPT-2, LLaMA, Gemma, Mistral, Qwen, and other architectures.

**Implementation approach:**
- Maps HuggingFace module names to standardized names through automatic renaming
- Uses `nn.ModuleDict` to organize modules hierarchically
- Preserves exact numerical behavior—no reimplementation of layers

### 2. Comprehensive Architecture Support

nnterp spans **16 architecture families** with **50+ model variants**:
- **Decoder-only LLMs**: GPT-2, GPT-3, GPT-3.5, GPT-4, LLaMA, Gemma, Mistral, Qwen, Phi, Falcon, InternLM, others
- **Vision**: CLIP text encoders
- **Specialized**: Code models, multilingual models, instruction-tuned variants

Each variant is automatically detected and mapped to its appropriate architecture family.

### 3. Built-in Mechanistic Interpretability Methods

nnterp includes ready-to-use implementations:

**Standard Analyses**
- **Logit Lens**: View intermediate predictions at each layer
- **Patchscope**: Run activation interventions with clean API
- **Activation Steering**: Apply steering vectors at specified layers
- **Attention Access**: Direct access to attention probabilities (where models expose them)

**Integration with NNsight**
- nnterp wraps NNsight's powerful intervention capabilities
- Enables complex multi-step interventions: hooks, patches, steering, and monitoring
- Maintains NNsight's ability to backprop through interventions

### 4. Validation and Testing Infrastructure

The library includes comprehensive validation:
- **Consistency tests**: Verify that renamed modules behave identically to originals
- **Numerical matching**: Ensure outputs match HuggingFace implementations exactly
- **Architecture detection**: Automatic validation that correct mapping is used
- **Documentation**: API documentation with examples for each architecture

## Methodology & Implementation

### Architecture-Agnostic Module Mapping

**Core algorithm:**
1. Inspect HuggingFace model architecture at runtime
2. Identify architecture type (GPT-2, LLaMA, Gemma, etc.) through module structure inspection
3. Map architecture-specific names to standardized hierarchy
4. Create `nn.ModuleDict` with standardized names pointing to original modules
5. Validate numerical equivalence: run input through both original and renamed paths

**Example mapping for LLaMA:**
```
Original: model.model.layers[5].self_attn.q_proj
Standard: model.layers[5].attn.q_proj

Original: model.model.layers[5].mlp.gate_proj
Standard: model.layers[5].mlp.gate_proj
```

### Handling Architecture Variations

**Embedding access:** Some models fuse embeddings, others separate them
- Solution: Detect fusion at runtime and provide unified `embedding` interface
- Return token embeddings + positional embeddings as needed

**Attention head computation:** Some separate Q/K/V, others fuse into single projection
- Solution: Detect pattern and provide consistent `get_attention_patterns()` method
- Return attention as (batch, heads, seq_len, seq_len) uniformly

**Intermediate layer sizes:** MLPs vary in hidden dimension
- Solution: Provide automatic detection and document in API
- Access via `model.layers[i].mlp.hidden_dim` for architecture-aware code

### Evaluation Methodology

**Validation tests for each architecture:**
1. **Numerical equivalence**: Run same input through original and renamed modules, verify outputs match to floating-point precision
2. **Intervention correctness**: Apply known interventions (e.g., zero out attention heads) and verify expected behavior changes
3. **Cross-layer consistency**: Verify that layer indices and naming are consistent throughout model depth

**Supported model types tested:**
- Full-size models: LLaMA-7B, GPT-2-XL, Mistral-7B
- Instruction-tuned variants: Llama-2-Chat, Mistral-Instruct
- Specialized variants: Code models, multilingual models
- Smaller models for CI/CD: GPT-2-Small, Gemma-2B

### Integration with Common Interpretability Libraries

nnterp's standardized interface enables seamless integration with:
- **NNsight**: For advanced intervention APIs
- **TransformerLens**: For comparison and migration
- **Nanograd**: For training minimal circuits
- **Steering vectors research**: For activation steering experiments

## Practical Applications & Real-World Use Cases

### 1. Mechanistic Circuit Discovery

**Before nnterp:**
- Researchers independently implement circuit discovery algorithms for each architecture
- Results difficult to compare across models or replicate

**With nnterp:**
- Single implementation of circuit discovery algorithm works across all architectures
- Enables large-scale studies comparing circuits across model families
- Example: Discover "greater-than" circuit in both LLaMA and Mistral with identical code

**Research applications:**
- Identify consistent circuits across model scales and architectures
- Test if certain interpretable features are fundamental to language modeling

### 2. Cross-Architecture Model Analysis

**Comparative studies:**
- Do different architectures implement the same algorithms (circuits)?
- How do attention patterns differ between GPT and LLaMA for the same task?
- Are interpretable features reusable across architectures?

**Practical example:** Steering vectors discovered in GPT-2 might transfer to other decoder-only models with nnterp's standardization.

### 3. Mechanistic Validation of Safety Properties

**Safety research:**
- Understand how models implement behaviors related to fairness, truthfulness, and refusal
- Test whether safety mechanisms (from RLHF) are localized to specific circuits
- Verify that safety mechanisms are robust across architectures

**Example workflow:**
```python
# Single code works across models
for model_name in ['gpt2-large', 'llama-7b', 'mistral-7b']:
    model = load_model(model_name)
    model = nnterp.make_interpretable(model)
    
    # Patch out attention heads identified as harmful
    patched_logits = patch_intervention(
        model, 
        patch_locations=harmful_heads,
        inputs=test_prompts
    )
```

### 4. Reproducibility in Mechanistic Research

**Reproducibility crisis in interpretability:**
- Custom implementations create numerical mismatches
- Results difficult to replicate
- New architectures require re-implementation

**nnterp's solution:**
- Share code, not implementations
- Other researchers run exact same code on their models
- Guaranteed numerical equivalence to HuggingFace implementations
- Easier publication of findings with reproducible code

### 5. Educational and Pedagogical Use

**Teaching mechanistic interpretability:**
- Students can implement analysis techniques once and apply to all models
- Removes infrastructure complexity from learning curve
- Enables focus on conceptual understanding

**Workshop and tutorial materials:**
- Mechanistic interpretability workshops can teach techniques using nnterp
- Code examples work for all attendees' preferred models
- Removes architecture-specific debugging from exercises

## Insights & Implications

### Advancing Mechanistic Interpretability Research

**Impact 1: Democratizing Circuit Discovery**
- Circuit discovery techniques were limited to a few architectures (primarily GPT-2, small LLaMA)
- nnterp enables researchers to discover circuits across diverse model families
- Reveals whether discovered circuits are architecture-specific or universal

**Impact 2: Enabling Comparative Studies**
- Can now systematically compare how different architectures solve the same tasks
- Tests fundamental hypotheses: Is mechanistic interpretability architecture-invariant?
- Enables large-scale cross-architecture interpretability studies

**Impact 3: Community Infrastructure**
- Reduces friction in mechanistic interpretability research
- Researchers can focus on novel interpretability techniques rather than infrastructure
- Facilitates cumulative research: others can build on findings with same code

### Limitations and Open Questions

**Architectural Limitations:**
- Encoder-only models and encoder-decoder architectures may require extensions
- Vision transformers supported partially (CLIP); other vision models need testing
- Multimodal models (e.g., LLaVA) have components that fall outside scope

**Methodological Limitations:**
- Standardization only covers activation-space analysis; doesn't cover gradient-based methods directly
- Parameter access standardization (weights/biases) not addressed
- Doesn't solve the problem of different architectures implementing computations differently at a higher level

**Practical Limitations:**
- Large models require GPU memory for intervention experiments
- Some models have architectural quirks (sparse attention, custom kernels) that require special handling
- Batching behavior may differ subtly across architectures

### Future Research Directions

1. **Expanding architecture support:** Encoder-decoder models, vision-language models, multimodal architectures
2. **Standardizing weight access:** Unified interface for accessing and analyzing model parameters
3. **Gradient-based analysis interface:** Standardized APIs for gradient-based interpretability techniques
4. **Performance profiling:** Benchmarking intervention overhead across architectures
5. **Automatic circuit discovery:** Leverage standardization to enable fully automated circuit discovery pipelines

## Code & Resources

### Official Repository
- **GitHub:** [https://github.com/Butanium/nnterp](https://github.com/Butanium/nnterp)
- **License:** MIT (permissive for research and commercial use)
- **Documentation:** [https://butanium.github.io/nnterp/](https://butanium.github.io/nnterp/)

### Installation

```bash
# Via pip (recommended)
pip install nnterp

# From source
git clone https://github.com/Butanium/nnterp.git
cd nnterp
pip install -e .
```

### Dependencies

- **Core**: PyTorch, HuggingFace `transformers`
- **Enhanced analysis**: NNsight (for advanced interventions)
- **Optional**: CUDA for GPU acceleration

### Quick Start Guide

**Basic usage:**
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import nnterp

# Load model
model_name = "meta-llama/Llama-2-7b-hf"  # or gpt2, mistral, etc.
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Make interpretable
interpretable_model = nnterp.make_interpretable(model)

# Access standardized modules (same across all architectures)
attention_module = interpretable_model.model.layers[5].attn
mlp_module = interpretable_model.model.layers[5].mlp

# Run logit lens analysis
logits_by_layer = nnterp.logit_lens(
    model=interpretable_model,
    prompt="The capital of France is",
    tokenizer=tokenizer
)

# Apply activation steering
steering_vector = torch.randn(model.config.hidden_size)
steered_output = nnterp.apply_steering(
    model=interpretable_model,
    prompt="The capital of France is",
    tokenizer=tokenizer,
    steering_vector=steering_vector,
    layers=[10, 11, 12]
)
```

**Advanced usage with NNsight:**
```python
# Use NNsight for complex interventions
from nnsight import nnBench

with nnterp.NNsightSession(interpretable_model) as session:
    with model.forward() as runner:
        # Run patchscope intervention
        value_from_source = runner.model.layers[5].attn.v_proj.output
        
    # Modify activations
    value_from_source[...] = torch.zeros_like(value_from_source)
    
    # Get output with patched values
    final_output = runner.output
```

### Interactive Resources

- **Colab notebook**: Example mechanistic interpretability experiments with nnterp
- **Benchmarking tool**: Measure overhead of different intervention types across architectures
- **Model compatibility checker**: Verify nnterp support for specific models

## Related Work & Context

### Relationship to Existing Mechanistic Interpretability Tools

**TransformerLens (Nostalgebraist et al.)**
- Custom reimplementation of transformer architectures
- Provides excellent clean interface but requires implementation per architecture
- nnterp complements by working with original HuggingFace implementations
- Can migrate TransformerLens code to nnterp for broader architecture support

**NNsight (Chen et al.)**
- Lower-level library for transformer interventions with HuggingFace
- Lacks standardized interface across architectures
- nnterp sits on top, adding standardization layer
- Users can drop down to NNsight for advanced use cases

**Nanograd / Minimal Circuits**
- Minimizes circuits by retraining and identifying essential components
- nnterp enables identifying candidate circuits; nanograd verifies their minimality
- Complementary approaches for complete circuit discovery

### Broader Context in Mechanistic Interpretability

**The mechanistic interpretability research landscape:**
1. **Circuit discovery**: Identify minimal subgraphs implementing specific behaviors (ACDC, Subnetwork Probing, EAP)
2. **Feature analysis**: Understand what neurons/attention heads represent
3. **Causal interventions**: Patch, ablate, steer to verify causal roles
4. **Structural analysis**: Map computation graphs and understand algorithmic procedures
5. **Application to safety**: Use mechanistic understanding to improve safety properties

nnterp enables scaling circuit discovery and causal analysis across all architectures, accelerating progress in all downstream applications.

### Related Evaluation Benchmarks

- **InterpBench**: Benchmark with semi-synthetic models where circuits are known—useful for validating nnterp-based circuit discovery methods
- **MIB (Mechanistic Interpretability Benchmark)**: Real models and tasks—tests whether nnterp enables reliable mechanistic analysis across diverse scenarios

### Convergence with Broader AI Interpretability

**Trend 1: From Architecture-Specific to Universal Methods**
- Early work (circuits, attention analysis) focused on GPT-2
- Scaling to LLaMA, CLIP, other architectures revealed challenges
- nnterp enables universal mechanistic interpretability infrastructure

**Trend 2: From Post-hoc to Mechanistic Explanation**
- Broader field moving from feature attribution (SHAP, LIME) to mechanistic understanding
- nnterp accelerates this transition by making mechanistic analysis accessible

**Trend 3: Safety-Critical Application of Interpretability**
- Understanding model internals increasingly important for AI safety
- nnterp supports safety research by enabling reproducible mechanistic analysis of safety properties

## Conclusion

nnterp solves a critical infrastructure problem in mechanistic interpretability: the lack of standardization across transformer architectures. By enabling researchers to write analysis code once and deploy across 50+ model variants, nnterp accelerates the pace of mechanistic interpretability research, improves reproducibility, and facilitates comparative studies across architectures. The library's foundation—preserving exact HuggingFace behavior while providing standardized access patterns—ensures that findings remain numerically valid and directly applicable to real deployed models.

The work exemplifies how proper infrastructure can unlock research progress. Rather than proposing novel interpretability techniques, nnterp removes friction from existing techniques, enabling the community to focus on deeper scientific questions about how neural networks compute.
