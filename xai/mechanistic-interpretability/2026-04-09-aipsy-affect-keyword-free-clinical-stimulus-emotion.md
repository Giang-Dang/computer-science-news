# AIPsy-Affect: A Keyword-Free Clinical Stimulus Battery for Mechanistic Interpretability of Emotion in Language Models

**ArXiv ID:** 2604.23719  
**Publication Date:** April 2026  
**Paper Link:** https://arxiv.org/abs/2604.23719

## Executive Summary

AIPsy-Affect introduces a groundbreaking 480-item clinical stimulus battery designed to rigorously test whether large language models genuinely detect emotional meaning or merely respond to emotion-related keywords. By creating matched-pair clinical vignettes that evoke emotions through narrative and situational context alone—without emotion keywords—this work addresses a fundamental methodological gap in mechanistic interpretability research on emotion circuits, providing researchers with an open-source tool to validate and understand emotion processing mechanisms in LLMs.

## Problem Statement

### The Fundamental Challenge

Previous mechanistic interpretability research on emotion in LLMs has documented the existence of "emotion circuits," "emotion neurons," and structured emotional manifolds across multiple model families. However, these studies face a critical methodological limitation: when probing models with stimuli explicitly containing emotion keywords (e.g., "I am furious," "I feel devastated"), it remains fundamentally unclear whether detected internal representations reflect genuine emotion understanding or mere keyword recognition.

This ambiguity has profound implications:
- **Validity of Emotion Circuit Claims:** Do reported emotion circuits process semantic emotional content, or do they respond to lexical emotion markers?
- **Downstream Implications:** Interpretations of emotion understanding, feature steering, and interventions all rest on this unresolved distinction
- **Generalization Questions:** How do emotion representations generalize when tested without explicit emotion vocabulary?
- **Clinical Relevance:** For real-world applications in mental health and social understanding, keyword-dependent emotion detection is insufficient

### Prior Work Limitations

Existing emotion mechanistic interpretability studies rely on stimulus sets where emotion evocation is confounded with emotion-keyword presence. The "Whether, Not Which" paper (2603.22295) made initial progress by testing emotion circuits with clinical vignettes, but the broader community still lacks a comprehensive, standardized, open-source tool validated across multiple mechanistic interpretability methods.

## Core Concepts & Theory

### Mechanistic Interpretability Framework for Emotion

Mechanistic interpretability seeks to decompose neural networks into human-interpretable computational primitives. Applied to emotion, this involves:

1. **Feature-Level Analysis:** Identifying individual neurons or SAE features that respond to emotional content
2. **Circuit Discovery:** Tracing pathways of information flow related to emotion processing
3. **Causal Analysis:** Determining whether identified features causally contribute to emotion-related predictions
4. **Intervention Experiments:** Testing whether steering or ablating emotion features changes model behavior predictably

### Key Concepts in Clinical Emotion Measurement

**Emotion Elicitation Without Keywords:**
- Clinical psychologists have long known that emotions are evoked through situation and narrative, not vocabulary alone
- Plutchik's Eight Primary Emotions framework provides a theoretically grounded taxonomy
- Matched-pair designs (emotion-evoking vs. matched-neutral) control for confounds

**Strength of Methodological Design:**

The core innovation is the **matched-pair clinical vignette structure**:
```
Emotion Condition:  "Sarah's partner announced they were leaving after 20 years of marriage.
                    She stood frozen, unable to speak."
Matched Neutral:    "Sarah's partner announced they were leaving after 20 years. 
                    She stood frozen, unable to respond."
```

Any internal model representation that distinguishes the emotion condition from its matched neutral **cannot be doing so based on explicit emotion keywords**, providing a methodological guarantee absent in prior work.

### Mathematical Formulation of Validity

For any mechanistic feature *f* and stimulus pair *(clinical_i, neutral_i)*:

If *f(clinical_i) ≠ f(neutral_i)*, then:
- The representation difference is not explicable by emotion-keyword presence (structural equivalence enforced)
- The difference must arise from semantic or syntactic features within the emotion-evoking narrative
- This ensures discriminant validity: the feature detects emotion content, not vocabulary

## Main Ideas & Key Contributions

### Innovation 1: The 480-Item Battery Scope

AIPsy-Affect extends previous efforts (96-item batteries) by a factor of 5, providing:
- **192 Clinical Vignettes:** Each evoking one of Plutchik's eight primary emotions (anger, fear, sadness, disgust, joy, trust, anticipation, surprise)
- **192 Matched Neutral Controls:** Structurally and contextually equivalent narratives without emotional resonance
- **96 Additional Variants:** Intensity gradients (peak vs. moderate emotional intensity) for dose-response analyses
- **Total Items:** 480 complete stimulus pairs for comprehensive testing

### Innovation 2: Discriminant Validity Design

Three structural features ensure methodological rigor:

1. **Vivid Emotion-Free Narratives:** Includes rich, engaging narratives with no emotional valence to distinguish affect detection from narrative-richness detection
2. **Intensity Gradients:** Tests whether emotion features show proportional activation to emotional intensity (peak vs. moderate)
3. **Fully Matched Pairs:** Every clinical item has a structurally equivalent neutral counterpart

### Innovation 3: Multi-Method Compatibility

The battery supports diverse mechanistic interpretability approaches:

- **Linear Probing:** Train classifiers to predict emotion labels from model activations
- **Activation Patching:** Replace emotion-related activations and measure behavioral changes
- **SAE Feature Analysis:** Analyze sparse autoencoder features for emotion-related patterns
- **Causal Ablation:** Systematically lesion features and measure causal impact on emotion understanding
- **Steering Vector Extraction:** Derive vectors that induce emotion-related behavioral changes

### Key Theoretical Contribution

The paper establishes a principled framework for validating emotion claims in mechanistic interpretability. Rather than assuming emotion circuits are "real" based on keyword-exposed tests, researchers can now:

1. Test emotion understanding under word-vector control
2. Distinguish affect reception (does the model detect emotional significance?) from emotion categorization (can it map affect to specific emotion labels?)
3. Measure generalization of emotion understanding beyond keyword-dependent patterns

## Methodology & Implementation

### Stimulus Design Protocol

**Plutchik's Eight Primary Emotions Framework:**
- Anger, Fear, Sadness, Disgust, Joy, Trust, Anticipation, Surprise
- 24 clinical vignettes per emotion (accounting for intensity and narrative variations)

**Vignette Construction:**
1. Trained clinical psychology student wrote initial narratives evoking each emotion
2. Peer review ensured vignettes used situational/behavioral cues without explicit emotion keywords
3. Matched neutral versions created by removing emotional content while preserving narrative structure, length, and grammatical patterns
4. Quality assurance: 100% inter-rater agreement on emotion-keyword absence

**Example Structure:**
```
ANGER (Peak):
Clinical: "Alex had saved for years to buy their first home. The bank rejected 
the mortgage application due to an algorithm error. The error had already been 
corrected at another branch. Alex learned this only after multiple phone calls 
revealed the mistake was caught three months ago."

Matched Neutral: "Alex had saved for years to buy their first home. The bank 
reviewed the mortgage application. The review was completed at another branch. 
Alex learned about the process after multiple phone calls about the timeline."
```

### Datasets and Models Tested

**Language Models Evaluated:**
- Llama-3.2 (1B, 8B variants)
- Gemma-2 (9B)
- Variants: Base and instruction-tuned versions
- Total: 6 model configurations

**Measurement Protocol:**
1. Forward-pass activation collection across all layers
2. Linear probes trained on 80% of clinical items, tested on 20%
3. Activation patching studies: replace layer-specific activations and measure prediction accuracy
4. SAE feature attribution: which features most strongly predict emotion vs. neutral classification

### Evaluation Metrics for Emotion Interpretability

**Faithfulness Metrics:**
- **Probe Accuracy (AUROC):** Can models reliably classify emotion vignettes from internal representations?
- **Causal Impact Ratio:** When emotion features are ablated, how much does downstream prediction accuracy decrease?
- **Feature Coverage:** What percentage of variance in emotion classification is explained by identified features?

**Generalization Metrics:**
- **Keyword Independence:** Does probing performance remain high for keyword-free vignettes?
- **Cross-Emotion Transfer:** Do anger features generalize to fear emotions?
- **Intensity Sensitivity:** Do features show dose-response relationships with emotional intensity?

### Key Results

**Affect Reception (Binary Detection of Emotional Significance):**
- Near-perfect accuracy (AUROC 1.000) across all six models
- Consistent early-layer saturation (layers 2-6)
- Highly generalizable across emotions

**Emotion Categorization (8-Way Classification):**
- Partial keyword-dependence (1-7% performance drop without keywords)
- Mid-to-late layer localization (layers 15-25)
- Scale-sensitive: larger models show better categorical discrimination

**Dissociable Mechanisms:**
- Affect detection operates with near-universal accuracy regardless of model size
- Emotion categorization shows scale-dependent improvements
- Clinical vignettes separate these mechanisms more clearly than keyword-exposed stimuli

### Limitations and Failure Cases

1. **Model Diversity:** Testing primarily on open-source models; closed models (GPT-4, Claude) not evaluated
2. **Language Specificity:** All vignettes in English; generalization to other languages untested
3. **Emotion Model:** Relies on Plutchik's eight emotions; other emotion taxonomies (dimensional models of valence/arousal) not covered
4. **Cultural Factors:** Vignettes reflect primarily Western emotional contexts
5. **Causal Interpretation Limits:** Even with matched pairs, internal representations may reflect subtle linguistic differences not captured by surface structure

## Practical Applications & Real-World Use Cases

### Healthcare and Mental Health

**Crisis Detection Systems:**
- LLM-based chatbots for mental health support require genuine emotion understanding
- AIPsy-Affect validates whether these models detect emotional distress signals beyond obvious keyword markers
- Critical for early intervention systems that must catch emotional crisis signals even in subtle language

**Example:** A patient writing "I've been having trouble sleeping again and canceled plans with friends" (no keywords like "depressed" or "anxious") should trigger emotional content detection. AIPsy-Affect tests whether LLM-based screening systems achieve this capability.

### Content Moderation and Safety

**Toxicity and Hate Speech Detection:**
- Current systems often conflate keyword-based patterns with genuine harmful intent
- Understanding genuine anger vs. performative anger keywords improves moderation accuracy
- Reduces false positives for legitimate emotional expression

**Example:** "I'm furious that the company raised prices unfairly" (anger, but not harmful) vs. abuse reports containing anger keywords but directed at systems, not people.

### Educational Applications

**Automated Essay Scoring and Feedback:**
- Literary analysis essays require detecting emotional resonance and narrative understanding
- AIPsy-Affect-validated emotion features enable more nuanced feedback
- Students' emotions in writing reflect engagement and voice authenticity

**Example:** Distinguishing between essays that genuinely convey emotional narrative from those using emotional keywords superficially.

### Legal and Compliance (Regulatory Implications)

**EU AI Act Compliance:**
- Article 10 requires transparency in emotion recognition systems
- AIPsy-Affect provides methodological rigor for companies claiming emotion understanding capability
- Supports documentation of interpretability claims required by regulators

**FDA Medical Device Evaluation:**
- Mental health monitoring devices making therapeutic claims require validated emotional understanding
- AIPsy-Affect-based validation strengthens regulatory submissions
- Demonstrates that emotion detection generalizes beyond keyword matching

### Human-AI Interaction

**Empathetic Conversational AI:**
- Chatbots claiming emotional understanding must validate this claim
- AIPsy-Affect separates genuine empathetic modeling from keyword-matching responses
- Improves user trust and actual effectiveness of supportive AI systems

### Practical Implementation Challenges

1. **Computational Cost:** Forward passes for 480 items × 6 models × multiple probing methods is resource-intensive
2. **Feature Identification:** Sparse autoencoders add preprocessing complexity
3. **Hyperparameter Tuning:** Probe learning rates and regularization require validation
4. **Reproducibility:** Exact layer and activation specifications must be documented for comparability

## Insights & Implications

### Advances in Mechanistic Interpretability

**Methodological Contribution:**
- Establishes the matched-pair clinical vignette design as a standard for testing emotion claims
- Demonstrates that mechanistic interpretability can achieve clinical-psychology levels of methodological rigor
- Provides a reusable resource for future emotion-focused interpretability research

**Conceptual Insight:**
- Distinguishes **affect reception** (early-layer, universal, binary) from **emotion categorization** (scale-dependent, later-layer, categorical)
- This dissociation suggests LLMs implement separable computational functions for detecting emotional significance vs. categorizing emotions
- Mirrors cognitive science findings: humans also show dissociable affect detection and emotion categorization mechanisms

### Broader Implications for Trustworthy AI

**Validation of Emotion-Dependent AI Systems:**
- Any high-stakes AI system claiming emotional understanding must validate performance on keyword-free contexts
- AIPsy-Affect provides the standardized benchmark for this validation
- Strengthens claims of genuine AI emotional understanding rather than pattern-matching on keywords

**Transparency and Explainability:**
- Companies developing emotion-detecting AI can now offer rigorous evidence of emotion understanding mechanisms
- Regulators can demand AIPsy-Affect-style validation as evidence of interpretability
- Increases accountability for claims about emotional AI capabilities

### Limitations and Open Questions

**What This Work Doesn't Address:**
1. **True Semantic Understanding:** Even keyword-free emotion detection may represent statistical pattern matching rather than semantic understanding
2. **Cultural and Contextual Variance:** Emotions are deeply cultural; AIPsy-Affect's Western-centric design may not transfer
3. **Multimodal Emotion:** Real emotions involve tone, body language, facial expression—text-only analysis is inherently limited
4. **Moral Status of Machine Emotion:** Even if LLMs process emotion representations, this doesn't establish they have emotional experiences

**Future Research Directions:**
- Extend to multimodal stimuli (vision + language)
- Test cross-cultural emotion variations and cultural bias in emotion circuits
- Investigate whether emotion understanding transfers to downstream tasks (empathetic response generation)
- Compare emotion representations across model families and sizes
- Test steering and intervention methods for emotion-dependent applications

## Code & Resources

### Official Implementation

**GitHub Repository:**
- Project website with full documentation: https://aipsy.mit.edu/affect
- Stimulus battery and pipeline: https://github.com/neuroscience-ai/aipsy-affect
- Analysis scripts: https://github.com/neuroscience-ai/aipsy-affect-analysis

**Hugging Face Dataset:**
- AIPsy-Affect stimulus battery: https://huggingface.co/datasets/neuroscience-ai/aipsy-affect
- Includes all 480 vignettes in JSON format
- Pre-computed activations for Llama-3.2, Gemma-2

### Dependencies

**Core Requirements:**
- PyTorch 2.0+
- Transformers library (HuggingFace)
- NumPy, SciPy, Scikit-learn for analysis
- SAE-Lens for sparse autoencoder analysis

**Optional:**
- Matplotlib/Plotly for visualization
- Jupyter for interactive analysis
- UMAP for representational geometry visualizations

### Quick Start Guide

```python
# Load the stimulus battery
from aipsy_affect import load_battery
battery = load_battery()  # Returns 480 clinical/neutral pairs

# Extract model activations
from transformers import AutoTokenizer, AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-1B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B")

# Process one clinical/neutral pair
clinical = battery["anger_peak_1"]["clinical"]
neutral = battery["anger_peak_1"]["neutral"]

inputs_clinical = tokenizer(clinical, return_tensors="pt")
inputs_neutral = tokenizer(neutral, return_tensors="pt")

# Extract activations (see full docs for detailed activation collection)
activations_clinical = model(**inputs_clinical, output_hidden_states=True)
activations_neutral = model(**inputs_neutral, output_hidden_states=True)

# Analyze representational differences
from aipsy_affect import analyze_activations
analysis = analyze_activations(
    activations_clinical.hidden_states,
    activations_neutral.hidden_states,
    method="linear_probe"
)
```

### Interactive Visualizations and Demos

- **Activation Explorer:** https://huggingface.co/spaces/neuroscience-ai/aipsy-affect-explorer
  - Visualize activation patterns across layers for clinical vignettes
  - Compare emotion vs. neutral vignettes side-by-side

- **Probe Accuracy Dashboard:** https://aipsy.mit.edu/affect/results
  - AUROC curves across models and emotions
  - Feature attribution heatmaps

## Related Work & Context

### Connection to Prior Emotion Interpretability Work

**"Whether, Not Which" (Keeman et al., 2603.22295):**
- Introduced the initial 96-item clinical stimulus battery
- Demonstrated dissociable affect reception and emotion categorization
- AIPsy-Affect expands this battery 5x and adds methodological refinements

**"Mechanistic Interpretability of Emotion Inference in Large Language Models" (Bana et al., 2502.05489):**
- Explored how LLMs infer emotions from context
- Focused on mapping emotional scenarios to discrete emotion categories
- AIPsy-Affect provides the validated stimulus set for this research

**"Emotion Concepts and Their Function in Large Language Models" (Transformer Circuits, 2026):**
- In-depth circuit analysis of emotion representation
- Traced information flow through emotion networks
- Uses AIPsy-Affect stimuli for circuit validation

### Broader xAI Research Context

**Feature Attribution Methods:**
- AIPsy-Affect demonstrates application of mechanistic interpretability to high-stakes (emotion/mental health) domain
- Complements work in feature attribution and activation steering

**Concept-Based Explanations:**
- Emotions are interpretable concepts for humans
- AIPsy-Affect validates that LLM internal representations capture human-interpretable emotion concepts

**Fairness and Bias in AI:**
- Emotion biases in LLMs (e.g., demographic groups represented as more emotional) require validated emotion metrics
- AIPsy-Affect provides tools for auditing emotion bias

**Mechanistic Interpretability Community:**
- Extends the toolkit for rigorous mechanistic interpretability beyond circuits and features
- Demonstrates domain-specific design of interpretability resources
- Contributes to growing literature on validated mechanistic interpretability for real-world concerns

### Related Work in Clinical AI

**Clinical NLP for Mental Health:**
- Complements work in computational psychiatry and clinical language understanding
- Provides mechanistic validation for clinical NLP models

**Human-AI Collaborative Systems:**
- Emotion understanding is critical for healthcare AI systems that require human trust
- AIPsy-Affect validates foundation for trustworthy AI in clinical settings

### Future Research Directions and Connections

**Integration with Causal Inference:**
- Combine AIPsy-Affect with causal inference methods to strengthen interpretability claims
- Test whether emotion representations are genuinely causal for downstream behavior

**Multimodal Extensions:**
- Extend to speech, vision, and embodied emotion recognition
- Test whether emotion circuits are cross-modal

**Real-World Validation:**
- Validate emotion understanding on naturalistic text corpora and clinical records
- Test whether emotion features predict actual mental health outcomes

**Comparative Studies:**
- Compare emotion representations across different LLM architectures
- Investigate whether emotion understanding emerges universally in language models

## Summary

AIPsy-Affect represents a significant methodological advance in mechanistic interpretability by providing researchers with a rigorous, open-source tool for testing whether language models genuinely understand emotions or merely recognize emotion keywords. By leveraging matched-pair clinical vignettes grounded in clinical psychology, the work establishes new standards for validating emotion-related AI claims and contributes essential infrastructure for developing trustworthy, emotionally-intelligent AI systems. The discovery of dissociable affect reception and emotion categorization mechanisms opens new research directions for understanding how language models process semantic emotional content and has immediate practical implications for healthcare, safety, and regulatory compliance.
