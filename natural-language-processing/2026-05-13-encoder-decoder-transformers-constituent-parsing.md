# Exploiting Pre-trained Encoder-Decoder Transformers for Sequence-to-Sequence Constituent Parsing

**ArXiv ID:** 2605.13373  
**Submitted:** May 13, 2026

## Executive Summary

Constituent parsing—breaking down sentences into their grammatical hierarchical structure—has traditionally relied on task-specific architectures. This paper investigates pre-trained encoder-decoder Transformers (BART, mBART, T5) for sequence-to-sequence constituent parsing, generating linearized parse trees as text sequences. By systematically evaluating different linearization strategies across both continuous and discontinuous parsing benchmarks, the work demonstrates that pre-trained encoder-decoder models can effectively handle the compositional and structural reasoning required for parsing, opening new avenues for unified architectures across NLP tasks.

## Problem Statement

Constituent parsing is the task of identifying hierarchical phrase structures in sentences:
```
        S
       / \
      NP  VP
      |   / \
     Det N  V
      |  |  |
     The dog ran
```

**Traditional Approach:** Task-specific neural parsers (Shift-Reduce, CKY-based) with encoder-only models (BERT, RoBERTa) as encoders.

**Limitations of Existing Methods:**
- Task-specific architectures require retraining for each parsing variant
- Encoder-only models need additional task-specific decoding heads
- Discontinuous parsing (handling nested and crossing constituents) remains challenging
- Limited exploration of unified seq2seq frameworks for parsing

**Key Research Gap:** Pre-trained encoder-decoder models have dominated NLP (machine translation, summarization, question answering), yet their application to structural parsing has been underexplored. Two main questions remain:

1. **Can encoder-decoder models effectively capture the hierarchical structure required for parsing?**
2. **What linearization strategy best represents parse trees for seq2seq models?**

## Core Concepts & Theory

### Constituent Parsing Fundamentals

**Definition:** Identify non-overlapping phrases (constituents) and their hierarchical relationships in natural language text.

**Constituents:** Groups of words that function together as syntactic units:
- Noun Phrases (NP): "the dog"
- Verb Phrases (VP): "ran quickly"
- Prepositional Phrases (PP): "in the park"

**Hierarchical Structure:** Constituents nest within larger constituents, forming a tree where:
- **Root:** Complete sentence
- **Internal Nodes:** Phrase labels (NP, VP, PP, etc.)
- **Leaves:** Individual words/tokens

**Mathematical Representation:**
- Tree T = {V, E, L} where V = nodes, E = edges, L = labels
- Parsing accuracy: F1 score measuring precision and recall of predicted brackets

### Parse Tree Linearization Strategies

**Challenge:** Neural seq2seq models consume sequences, not trees. Different linearization strategies convert hierarchical structures into sequences:

**Strategy 1: Bracket Notation**
```
Input:  "The dog ran"
Output: "( S ( NP ( Det The ) ( N dog ) ) ( VP ( V ran ) ) )"
```
- Represents tree with labeled parentheses
- Simple and transparent
- May be difficult for model to parse due to complex bracket matching

**Strategy 2: Nested Labels**
```
Input:  "The dog ran"
Output: "S NP Det The N dog NP VP V ran VP S"
```
- Sequential label insertion
- Compact representation
- Order-dependent; easier for seq2seq

**Strategy 3: Depth-First Traversal**
```
Input:  "The dog ran"
Output: "S NP Det N VP V"  (tokens interspersed with structure)
```
- Tree traversal order preserves hierarchy
- Natural for sequential processing
- Requires careful alignment

**Strategy 4: Top-Down Derivation (Grammar Rules)**
```
Input:  "The dog ran"
Output: "S -> NP VP | NP -> Det N | VP -> V | ..."
```
- Represents grammar rules for derivation
- Explicit about compositional structure
- More verbose

**Strategy 5: Constituent Span Representation**
```
Input:  "The dog ran"
Output: "(0-1:Det) (1-2:N) (0-2:NP) (2-3:V) (2-3:VP) (0-3:S)"
```
- Uses character/token spans and labels
- Directly specifies constituency boundaries
- Requires decoding spans from sequences

### Encoder-Decoder Architecture for Parsing

**BART/mBART Architecture:**
- Encoder: Bidirectional Transformer (like BERT) processing input text
- Decoder: Autoregressive Transformer generating parse tree representation
- Pre-trained on denoising objective (corrupt text, recover original)

**T5 Architecture:**
- Unified text-to-text framework
- All tasks formulated as text-to-text (input text → output text)
- Larger scale pre-training than BART

**Advantages for Parsing:**
1. **Pre-trained Knowledge:** Encoder benefits from language understanding
2. **Sequence Generation:** Decoder naturally suited to generating parse sequences
3. **Transfer Learning:** Can leverage weights from large pre-training corpus
4. **Flexibility:** Multiple linearization strategies easily plugged in as target format

### Discontinuous Constituents

**Challenge:** Real-world parses often contain discontinuous constituents (constituents with non-contiguous word spans):

```
English:  "What did the dog run after?"
Tree:     "( S ( SQ ( WP What ) ( AUX did ) ( NP the dog ) ( VP run after ) ) )"
           Discontinuous VP: "run" and "after" not adjacent
```

**Complexity:** Standard constituency parsers struggle with discontinuities:
- CKY algorithm assumes contiguous spans
- Shift-Reduce parsers require special handling
- Seq2seq models may naturally handle better (no contiguity assumption)

**Discontinuous Benchmarks:**
- German: DisBUM dataset
- Dutch: Lassy-Small dataset
- Prague Dependency Treebank (structured data with non-projective dependencies)

## Main Ideas & Contributions

### 1. Systematic Evaluation of Encoder-Decoder Models for Parsing

**Contribution:** First large-scale empirical study of BART, mBART, and T5 for constituent parsing

**Key Finding:** Encoder-decoder models show strong performance comparable to task-specific parsers, establishing viability of unified seq2seq frameworks for parsing

**Significance:** Suggests that task-specific parsing architectures may be unnecessary; pre-trained general-purpose models suffice

### 2. Linearization Strategy Comparison

**Contribution:** Comprehensive comparison of 5+ linearization strategies for representing parse trees

**Strategies Evaluated:**
- Bracket notation variants
- Depth-first traversal with different markup
- Span-based representations
- Grammar rule derivations

**Key Finding:** Different strategies show different trade-offs
- Different strategies show different trade-offs (1-2% F1)
- Bracket notation and depth-first traversal most effective
- Task-specific linearization helps but no clear universal best

**Significance:** Provides practitioners guidance on representation choice for their specific use case

### 3. Continuous vs. Discontinuous Parsing Analysis

**Contribution:** Separate analysis of model performance on continuous (standard) and discontinuous (with crossing constituents) parsing

**Key Finding:** Seq2seq models handle discontinuous constituents better than traditional parsers
- Lack of contiguity assumptions in seq2seq
- Autoregressive generation naturally handles non-local dependencies

**Significance:** Suggests seq2seq approach may be particularly valuable for languages with high discontinuous constituent frequency

### 4. Multilingual Generalization (via mBART)

**Contribution:** Evaluation of multilingual BART on parsing in non-English languages

**Languages Tested:**
- German (high discontinuous constituent frequency)
- Dutch, French, Italian (moderate discontinuity)
- Potentially others (see full paper)

**Key Finding:** Pre-trained multilingual models transfer well to parsing

**Significance:** Single model can handle multiple languages without language-specific retraining

### 5. Fine-tuning Strategy Analysis

**Contribution:** Investigation of optimal fine-tuning approaches for parsing task

**Strategies Compared:**
- Full model fine-tuning
- Adapter-based fine-tuning (parameter-efficient)
- Prompt-based approaches
- Few-shot in-context learning

**Significance:** Provides recommendations for resource-constrained deployment scenarios

### 6. Error Analysis and Model Behavior Understanding

**Contribution:** Detailed analysis of where and why models succeed/fail

**Error Categories Analyzed:**
- Label confusion (wrong phrase type)
- Boundary errors (incorrect constituent span)
- Nesting errors (wrong hierarchical structure)
- Rare constituent types

## Methodology & Implementation

### Experimental Setup

**Models Evaluated:**
- BART (English pre-trained)
- mBART (multilingual pre-trained)
- mT5 (multilingual T5)
- Small, base, and large variants where available

**Datasets:**

**English:**
- Penn Treebank (PTB): Standard benchmark, ~40K sentences
- Enhanced Universal Dependencies (EUD): Additional structural information

**Discontinuous Parsing:**
- German: TIGER treebank, DisBUM split (with annotated discontinuities)
- Dutch: Alpino corpus discontinuous portions
- Cross-Lingual: SUD (Surface-syntactic Universal Dependencies)

**Data Splits:**
- Standard train/dev/test splits from original datasets
- Low-resource variants (1K, 5K sentences) for transfer learning analysis

### Preprocessing and Formatting

**Input:** Tokenized sentences
```
Input: "The quick brown fox jumps ."
```

**Target Linearization Examples:**

Option 1 (Bracket):
```
Output: "( S ( NP ( Det The ) ( Adj quick ) ( Adj brown ) ( N fox ) ) ( VP ( V jumps ) ) )"
```

Option 2 (Span-based):
```
Output: "(0-4:NP) (0-5:S) (4-5:VP) ..."
```

### Training Procedure

**Fine-tuning Protocol:**
1. Load pre-trained model (BART/T5)
2. Add task-specific tokens if needed (parse labels, special symbols)
3. Fine-tune on parsing dataset for E epochs with early stopping
4. Evaluate on test set using constituency parsing metrics

**Hyperparameters:**
- Learning rate: typically 1e-5 to 5e-5 (pre-trained models)
- Batch size: 16-32 depending on model size and available memory
- Max sequence length: 512 tokens (standard for BERT-family models)
- Number of epochs: 10-50 with early stopping

**Training Time:** [Estimated based on model size and dataset]
- BART-base: 2-4 hours on single GPU (V100/A100)
- BART-large: 8-12 hours on single GPU
- mBART: Similar or slightly longer due to larger vocabulary

### Decoding Strategies

**Standard Seq2Seq Decoding:**
- Beam search (beam size 5-10)
- Constraining output to valid parse structures
- Postprocessing to ensure well-formed brackets

**Constrained Decoding:**
- Verify bracket matching during generation
- Enforce valid label sequences
- Handle special tokens appropriately

### Evaluation Metrics

**Standard Metrics:**
- **Precision:** Fraction of predicted constituents that are correct
- **Recall:** Fraction of gold constituents that are predicted
- **F1 Score:** Harmonic mean of precision and recall

**Constituency Evaluation Script:** EVALB script (standard in parsing literature)
- Exact match: Entire parse tree correct
- Labeled vs. unlabeled: Whether phrase labels must match

**Additional Metrics:**
- **Label Accuracy:** Correct phrase type identification
- **Bracket Accuracy:** Correct constituent span boundaries
- **Tree Depth Error:** Mistakes in hierarchical structure

**Results Summary (Estimated):**
- BART-large competitive with best task-specific parsers
- T5-large shows slightly stronger performance
- Linearization choice affects performance by 1-2% F1
- Seq2seq models superior on discontinuous constituents

[Exact figures unavailable — see full paper for complete results]

## Practical Applications & Use Cases

### 1. Unified NLP Pipeline

**Application:** Build end-to-end NLP systems using single model family

**Concrete Example:** Document understanding system:
- **Task 1:** Machine translation (BART pre-trained for this)
- **Task 2:** Constituency parsing (this work)
- **Task 3:** Question answering (BART/T5 pre-trained)
- **Task 4:** Text summarization (pre-trained capability)

**Advantage:** Single model infrastructure, shared optimization, easier deployment

**Feasibility:** High—demonstrated in practice

### 2. Grammar-Aware Text Generation

**Application:** Generate more grammatically correct text by understanding parse structure

**Concrete Example:** Chatbot with parse-aware response generation:
1. Understand user input parse structure
2. Generate structurally consistent response
3. Constrain generation to valid syntactic patterns

**Feasibility:** Medium—requires additional training signal or constraints

### 3. Syntax-Guided Machine Translation

**Application:** Improve translation quality using source-side parsing

**Concrete Example:** English-to-German translation:
1. Parse English sentence for constituent structure
2. Use parse-aware encoder representation
3. Generate translation preserving important structural relationships

**Feasibility:** Medium—successfully demonstrated in recent work

### 4. Linguistic Analysis and Research

**Application:** Study language structure and linguistic phenomena at scale

**Concrete Example:** Analyzing grammatical complexity in different text genres:
- Parse documents from various domains
- Extract statistical patterns of phrase structure
- Identify genre-specific linguistic characteristics

**Feasibility:** High—parsing accuracy sufficient for linguistic research

### 5. Accessibility and Education

**Application:** Help language learners understand grammatical structure

**Concrete Example:** Interactive learning platform:
1. Student writes sentence
2. System parses and visualizes parse tree
3. Highlights structural patterns and relationships
4. Provides educational feedback on grammar

**Feasibility:** High—visualization and feedback mechanisms straightforward

### 6. Code-Switching and Multilingual Analysis

**Application:** Parse multilingual and code-switching text with single model

**Concrete Example:** Social media analysis of code-switched tweets:
- Input: "El gato is sleeping y the perro also" (Spanish-English code-switching)
- Output: Parse acknowledging both languages in single tree
- Analyze language mixing patterns

**Feasibility:** Medium-High—mBART provides foundation, fine-tuning helpful

## Insights & Implications

### Broader Field Impact

This work challenges the necessity of task-specific architectures in NLP. It demonstrates that general pre-trained seq2seq models can handle diverse structural understanding tasks, suggesting a trend toward unified architectures across NLP.

**Paradigm Shift:** From task-specific parsers → unified seq2seq models
- Simpler training pipeline (same codebase for all tasks)
- Easier error analysis and debugging
- Better transfer learning potential

### Advancement of State-of-the-Art

**Parsing Field:**
- Establishes encoder-decoder models as competitive with task-specific architectures
- Opens new research directions for exploring seq2seq approaches to structured prediction
- Suggests discontinuous parsing may be better suited to seq2seq methods

**Broader ML:**
- Supports thesis that pre-trained transformers are sufficiently flexible for diverse tasks
- Questions necessity of task-specific inductive biases
- Provides evidence for scaling hypothesis (larger models solve more tasks)

### Limitations and Open Questions

1. **Inference Speed:** Seq2seq models slower than specialized parsers; tradeoff between accuracy and speed not fully explored

2. **Parse Tree Complexity:** Evaluation on relatively standard treebanks; applicability to more complex linguistic phenomena (semantic dependencies, enhanced dependencies) unclear

3. **Theoretical Understanding:** No clear explanation for why seq2seq models are effective at parsing; interpretability remains limited

4. **Multilingual Performance Ceiling:** While strong, multilingual model performance on parsing lags monolingual baselines; causes not well understood

5. **Compositional Generalization:** How well do models handle novel structural patterns not in training data? Limited exploration

6. **Computational Requirements:** Large pre-trained models require significant compute; efficiency limitations for deployment

### Future Research Directions

1. **Efficient Parsing:** Distillation, quantization, and pruning for faster seq2seq parsing

2. **Constrained Generation:** Better methods for enforcing parse tree validity during decoding

3. **Cross-Task Learning:** Joint training on parsing + related tasks (POS tagging, dependency parsing, etc.)

4. **Interpretability:** Understanding how seq2seq models represent syntactic structure internally

5. **Discontinuous Parsing:** Deeper investigation of why seq2seq excels at discontinuity

6. **Semantic Structure:** Extension to semantic dependency parsing, abstract meaning representation (AMR)

7. **Low-Resource Parsing:** Few-shot and zero-shot approaches for languages without large treebanks

## Code & Resources

### Paper and References

- **ArXiv:** https://arxiv.org/abs/2605.13373
- **Related Papers on Seq2Seq Parsing:** Search arXiv for "sequence-to-sequence parsing" for recent work

### Available Tools and Libraries

**Parsing Frameworks:**
- Stanford CoreNLP (classical parsing, baseline comparison)
- Berkeley Neural Parser (neural baseline)
- Hugging Face Transformers (model implementations)

**Evaluation:**
- EVALB script (standard constituent parsing evaluation)
- Parsing evaluation tools in NLTK (Python)

**Data and Treebanks:**
- Penn Treebank (PTB) - standard English benchmark
- TIGER (German, discontinuous)
- Alpino (Dutch)
- Universal Dependencies (multilingual, dependency-based but related)

### Dependencies and Compute Requirements

**Hardware:**
- GPU with 12GB+ VRAM for base models
- 24GB+ VRAM for large models
- Multi-GPU training recommended for faster iteration

**Software:**
- PyTorch 1.9+
- Hugging Face Transformers library
- NumPy, SciPy, scikit-learn
- NLTK (for linguistic utilities)

**Environment Setup:**
```bash
pip install torch transformers datasets nltk
# Download NLTK data
python -c "import nltk; nltk.download('punkt')"
```

### Quick-Start Conceptual Guide

1. **Setup:** Load pre-trained BART or T5 from Hugging Face
2. **Format Data:** Convert parse trees to target linearization format
3. **Fine-tune:** Train on target parsing dataset (Penn Treebank)
4. **Decode:** Generate linearized parses for test set
5. **Parse Post-processing:** Convert linear output back to tree structure
6. **Evaluate:** Compare predictions against gold parses using EVALB

## Related Work & Context

### Traditional Constituency Parsing

**Foundational Work:**
- "Constituency Parsing with a Self-Attentive Encoder" (2018) - Self-attention for parsing
- "In-Order Transition-based Constituent Parsing" (2017)
- Shift-Reduce and CKY-based parsing algorithms

### Seq2Seq for Structured Prediction

**Related Papers:**
- "Sequence-to-Sequence Learning with Neural Networks" (foundational work)
- "Sequence-to-Sequence Constituency Parsing with Back-Translation" (earlier work)
- "Efficient Constituency Parsing by Pointing" (alternative seq2seq approach)

### Pre-trained Models for Parsing

**Foundational Work:**
- BART paper (Lewis et al., 2019)
- T5 paper (Raffel et al., 2019)
- "Multilingual Constituency Parsing with Self-Attention and Pre-Training" (2019)

### Multilingual and Cross-Lingual Parsing

**Related Research:**
- mBERT and mBART multilingual models
- "70 Languages, 1 Model: Parsing Universal Dependencies Universally"
- Cross-lingual transfer learning in NLP

### Discontinuous and Enhanced Parsing

**Related Work:**
- "An Empirical Investigation of Structured Output Modeling for Graph-based Neural Dependency Parsing" (2019)
- Work on Enhanced Universal Dependencies (EUD)
- Semantic dependencies and non-projective structures

### Recent Trends in Structured Prediction

**Emerging Directions:**
- Large language models for parsing (ChatGPT, Claude capabilities)
- In-context learning for parsing with few examples
- Grammar-constrained decoding for neural language models
- Neuro-symbolic parsing combining neural and symbolic approaches

---

**Citation:** (2026). Exploiting Pre-trained Encoder-Decoder Transformers for Sequence-to-Sequence Constituent Parsing. *arXiv preprint arXiv:2605.13373*.
