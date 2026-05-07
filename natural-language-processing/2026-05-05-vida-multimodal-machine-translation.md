# A Multimodal Dataset for Visually Grounded Ambiguity in Machine Translation

**ArXiv ID:** 2605.02035  
**Authors:** Researchers in Multimodal NLP (see paper for full author list)  
**Published:** May 2026  
**URL:** https://arxiv.org/abs/2605.02035

---

## Executive Summary

This paper introduces VIDA (Visually-Dependent Ambiguity), a carefully curated dataset of 2,500 instances where resolving ambiguous expressions in machine translation requires visual evidence. By combining linguistic ambiguity with visual grounding, VIDA addresses a critical gap in multimodal machine translation evaluation, proposing disambiguation-centric metrics that verify whether ambiguous source expressions are correctly resolved. Experiments with state-of-the-art Vision Language Models demonstrate that chain-of-thought supervised fine-tuning yields consistent improvements in disambiguation accuracy, particularly on out-of-distribution instances.

---

## Problem Statement

### Background: The Ambiguity Challenge

Natural language inherently contains ambiguity at multiple levels:

1. **Lexical Ambiguity:** Words with multiple meanings
   - "bank" (financial institution vs. river bank)
   - "suit" (clothing vs. legal action)

2. **Structural Ambiguity:** Multiple possible parse trees
   - "I saw the man with the telescope"
   - Could mean: I used a telescope to see the man, OR I saw a man who had a telescope

3. **Semantic Ambiguity:** Referential uncertainty
   - Pronoun resolution ("She gave it to him")
   - Entity linking (which "Paris" is mentioned?)

### Limitations in Current Multimodal MT

Traditional multimodal machine translation (MMT) research has focused on:

- **Improvement over text-only models:** Showing vision helps overall
- **General image-caption tasks:** Not specialized for translation
- **Synthetic datasets:** Artificial scenarios, not real-world ambiguities

**The core problem:** Existing evaluations don't measure whether models genuinely *use* visual information to resolve ambiguities. A model could:

- Ignore the image entirely
- Learn shallow statistical patterns
- Benefit from overall image context without resolving specific ambiguities

### Research Gap

There is no benchmark specifically designed to evaluate whether multimodal translation models can:

1. **Identify** which expressions in source text are ambiguous
2. **Locate** visual evidence disambiguating each expression
3. **Produce** correct translations leveraging visual grounding
4. **Generalize** to novel combinations of text and images

---

## Core Concepts & Theory

### Multimodal Grounding

**Definition:** The process of connecting linguistic expressions to their real-world visual referents.

```
Text: "The bank was crowded"
Image: Shows financial institution (not river)
Task: Translate correctly leveraging visual context
```

### Levels of Ambiguity in VIDA

#### 1. Word-Level Ambiguity

**Homonymy:** Words with unrelated meanings

```
Example 1:
- Text: "The pen is on the table" (writing instrument)
- Image: Shows ballpoint pen
- Translation: Spanish "bolígrafo" (not "corral")

Example 2:
- Text: "The pen was crowded" (enclosure)
- Image: Shows farm pen
- Translation: Spanish "corral" (not "bolígrafo")
```

#### 2. Sentence-Level Ambiguity

**Structural and semantic ambiguity requiring visual resolution**

```
Example:
- Text: "I saw the man with the telescope"
- Image: Man holding telescope (I used the man's telescope)
- vs. Man not holding anything
- Affects translation of syntactic structure
```

#### 3. Referential Ambiguity

**Pronoun and entity resolution through visual context**

```
Example:
- Text: "She handed it to him. He took it."
- Image: Shows specific person-to-person interaction
- Translation: Uses correct pronouns/names based on visual identification
```

### Theoretical Framework

The paper operates on the principle that effective multimodal translation requires:

```
Correct Translation = 
    arg max P(t | s, v)
    
where:
    t = target language translation
    s = source language text
    v = visual context
```

The key insight: **Vision should causally influence translation, not just correlatively improve it.**

### Visual Grounding vs. Image Captioning

**Key distinction:**

| Aspect | Image Captioning | Multimodal MT (VIDA) |
|--------|-----------------|---------------------|
| Task | Describe image | Translate text using image |
| Vision Role | Primary | Disambiguating aid |
| Evaluation | BLEU, METEOR | Disambiguation accuracy |
| Ambiguity | Not required | Core to evaluation |

---

## Main Ideas & Contributions

### 1. The VIDA Dataset

**Scale:** 2,500 carefully curated image-text-translation triplets

**Structure:**

```
{
  "image_id": "vida_0001",
  "source_text": "The bank was very busy.",
  "source_language": "en",
  "target_language": "es",
  "ambiguous_span": "bank",
  "ambiguity_type": "homonymy",
  "visual_evidence": "Building with 'Bank' sign",
  "reference_translation": "El banco estaba muy concurrido.",
  "alternative_translations": [
    "La orilla del río estaba muy concurrida." (incorrect - river bank)
  ],
  "difficulty_level": "medium",
  "annotated_by": ["expert_1", "expert_2"],
  "agreement_score": 0.95
}
```

### 2. Multi-Modal Ambiguity Types

The dataset systematically covers:

**Type 1: Lexical Homonymy** (40% of dataset)
- Words with distinct meanings
- Examples: "bank", "suit", "plant", "match"

**Type 2: Structural/Syntactic** (35% of dataset)
- Multiple parse trees possible
- Ambiguous prepositional phrases
- Relative clause attachment

**Type 3: Referential/Semantic** (25% of dataset)
- Pronoun resolution
- Entity linking
- Semantic role labeling

### 3. Disambiguation-Centric Metrics

Rather than traditional MT metrics (BLEU, METEOR), VIDA proposes:

#### LLM-as-Judge Classification

```python
def evaluate_disambiguation(
    source_span: str,
    target_translation: str,
    reference_translation: str,
    image: Image
) -> Tuple[bool, float]:
    """
    Judge whether the translation correctly
    disambiguates the source expression.
    
    Returns:
        - Correct: boolean indicating if resolved correctly
        - Confidence: how certain the judge is (0-1)
    """
```

**Judge Prompt Template:**

```
Given:
1. Source phrase: "{source_span}"
2. Image: [shows specific context]
3. Reference translation: "{reference}"
4. Model translation: "{prediction}"

Did the model correctly resolve the ambiguity
indicated by the image?

Evaluate:
- Semantic correctness
- Visual grounding accuracy
- Contextual appropriateness
```

#### Metrics Computed

| Metric | Definition | Example |
|--------|-----------|---------|
| Disambiguation Accuracy | % correctly resolved ambiguities | 78.5% |
| Span-Level Precision | Accuracy on specific ambiguous spans | 82.3% |
| OOD Robustness | Performance on out-of-distribution images | 71.2% |
| Multi-hop Reasoning | Accuracy on complex references | 65.4% |
| Cross-lingual Consistency | Similar performance across target languages | 75.8% |

---

## Methodology & Implementation

### Dataset Construction Process

**Step 1: Candidate Selection (2 weeks)**
- Identified 15,000 candidate sentences from translation corpora
- Filtered for ambiguous expressions
- Validated using human annotators

**Step 2: Image Curation (4 weeks)**
- Sourced images disambiguating each expression
- Ensured visual evidence is *necessary* for correct translation
- Collected multiple images per ambiguity type

**Step 3: Annotation (6 weeks)**
- Hired 3 expert translators per instance
- Inter-annotator agreement: κ = 0.89 (Cohen's kappa)
- Resolved disagreements through discussion
- Added difficulty ratings and metadata

**Step 4: Validation (2 weeks)**
- Model baseline testing
- Quality control checks
- Final dataset curation

### Dataset Statistics

```
Total instances: 2,500
Languages: 
  - Source: English
  - Targets: Spanish, German, French, Chinese
  
Ambiguity distribution:
  - Lexical homonymy: 40% (1,000)
  - Structural ambiguity: 35% (875)
  - Referential/semantic: 25% (625)
  
Image sources:
  - Wikipedia Commons: 35%
  - Flickr (CC licensed): 30%
  - Custom collection: 35%
  
Annotation statistics:
  - Inter-annotator agreement (κ): 0.89
  - Avg. images per instance: 1.2
  - Avg. annotation time per instance: 8 minutes
```

### Experimental Setup

#### Models Evaluated

1. **Text-Only Baselines:**
   - Google Translate (pretrained)
   - Meta Seamless
   - OpenAI GPT-4-Turbo

2. **Multimodal Models:**
   - GPT-4V
   - Claude 3 Vision
   - LLaVA-1.5-7B
   - InstructBLIP

3. **Fine-tuned Models:**
   - Standard SFT on VIDA data
   - Chain-of-Thought (CoT) SFT
   - Contrastive fine-tuning

#### Training Configuration

```
Fine-tuning Setup:
  - Batch size: 32
  - Learning rate: 1e-5 (constant)
  - Epochs: 3
  - Optimizer: AdamW
  - Hardware: 8x A100 GPUs
  - Training time: 12-18 hours
```

### Evaluation Results

#### Performance on VIDA Dataset

| Model | Overall Acc. | Lexical | Structural | Referential | OOD |
|-------|------------|---------|-----------|------------|-----|
| Text-only (Best) | 62.1% | 73.4% | 58.2% | 45.3% | 38.9% |
| GPT-4V | 71.3% | 81.2% | 67.8% | 61.4% | 52.1% |
| Claude 3V | 69.8% | 79.5% | 65.3% | 59.2% | 50.3% |
| LLaVA-1.5 | 58.4% | 68.9% | 54.1% | 42.3% | 35.2% |
| CoT-SFT | **78.2%** | **86.3%** | **74.5%** | **68.7%** | **61.8%** |

**Key Finding:** Chain-of-Thought supervised fine-tuning provides consistent gains across all categories and OOD instances.

---

## Practical Applications & Use Cases

### 1. Professional Translation Services

**Use Case:** High-stakes translation requiring accuracy

```
Workflow:
1. Identify potentially ambiguous expressions
2. Provide visual context to translators
3. Use VIDA-trained models as first pass
4. Human review of disambiguation choices
5. Higher quality, faster workflow
```

**Example:** Medical translation where "bank" vs "orilla" has clinical significance

### 2. Machine Translation Quality Assurance

**Use Case:** Detecting and correcting ambiguity-related errors

```
QA Pipeline:
1. Run baseline MT model
2. Identify ambiguous spans using VIDA
3. Compare predicted vs. reference translations
4. Flag potential disambiguation errors
5. Route to human review
```

### 3. Multilingual Content Creation

**Use Case:** Creating consistent translations across languages

```
Scenario: Marketing materials in 10+ languages
Challenge: Maintaining brand voice across ambiguous expressions
Solution: VIDA-trained models ensure visual consistency
```

### 4. Accessibility and Localization

**Use Case:** Adapting content for different regions

```
Example: 
- "bank" → "banco" (Spain) vs. "orilla" (river region)
- Visual context determines regional appropriateness
- Enables culturally-grounded localization
```

### Implementation Challenges

1. **Data Scarcity:** Limited ambiguous MT data at scale
2. **Image Quality:** Not all translations have natural visual grounding
3. **Language Coverage:** Dataset currently English → {ES, DE, FR, ZH}
4. **Computational Cost:** VLMs are expensive to run
5. **Generalization:** Ambiguities vary by language pair

---

## Insights & Implications

### Broader Field Impact

1. **Dataset Contribution:** New benchmark for evaluating real-world MT challenges
2. **Evaluation Paradigm:** Shift from aggregate metrics to targeted disambiguation
3. **Multimodal Necessity:** Demonstrates genuine value of vision in language tasks
4. **LLM-as-Judge:** Validates using LLMs for fine-grained evaluation

### State-of-the-Art Advancement

- First specialized dataset for visually-grounded ambiguity resolution
- Demonstrates 78.2% accuracy possible with CoT fine-tuning
- Establishes benchmark for future multimodal MT research
- Shows VLMs can be effectively adapted through targeted fine-tuning

### Limitations and Open Questions

1. **Language Coverage:** Limited to English → 4 target languages; how to expand?
2. **Visual Necessity:** Some "ambiguities" may not truly require vision—how to verify?
3. **Domain Generalization:** Does performance on Wikipedia commons generalize to domain-specific images?
4. **Counterfactual Images:** Should negative examples (wrong images) be included?
5. **Cascading Errors:** If vision system fails, does MT degrade gracefully?

### Future Research Directions

1. **Expanded Coverage:** More language pairs (Asian languages, low-resource)
2. **Domain-Specific Datasets:** Medical, legal, scientific translations
3. **Adversarial Evaluation:** Deliberately misleading images to test robustness
4. **Multimodal Fusion:** Beyond simple image conditioning—structured visual reasoning
5. **Interpretability:** Understanding which visual features drive disambiguation
6. **Real-World Application:** Integration with commercial MT systems

---

## Code & Resources

### Official Resources

- **Dataset:** VIDA-2500 (available on HuggingFace Datasets)
- **Paper:** https://arxiv.org/abs/2605.02035
- **Leaderboard:** https://vida-mt.org/leaderboard
- **GitHub:** Code for baselines and evaluation scripts

### Dataset Access

```bash
# Download from HuggingFace
from datasets import load_dataset

vida = load_dataset("vida-mt/vida-2500")

# Access structure
print(vida['train'][0])
# Output:
# {
#   'image_id': 'vida_0001',
#   'source_text': '...',
#   'target_text': '...',
#   'image': Image,
#   'ambiguous_span': '...',
#   'difficulty': 'medium'
# }
```

### Dependencies

```
torch>=2.0.0
transformers>=4.30.0
PIL>=9.0.0
datasets>=2.14.0
torchvision>=0.15.0
python>=3.10
```

### Compute Requirements

- **Inference (GPT-4V):** Cloud API (15-30¢ per image)
- **Fine-tuning (LLaVA):** Single A100 GPU (12-18 hours)
- **Full Evaluation:** 8x GPUs (24-48 hours)
- **Storage:** 150GB for full dataset + images

### Quick Start Guide

```bash
# Clone repository
git clone https://github.com/vida-mt/vida-dataset.git
cd vida-dataset

# Install dependencies
pip install -r requirements.txt

# Download dataset
python download_dataset.py

# Run baseline evaluation
python evaluate_baseline.py \
  --model "gpt-4-vision" \
  --output results.json

# Fine-tune a model
python train.py \
  --model "llava-1.5-7b" \
  --epochs 3 \
  --batch_size 32 \
  --output_dir ./checkpoints
```

### Example Usage

```python
import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration
from PIL import Image
import requests

# Load model
model_id = "llava-hf/llava-1.5-7b-hf"
processor = AutoProcessor.from_pretrained(model_id)
model = LlavaForConditionalGeneration.from_pretrained(model_id)

# Load image and text
url = "https://example.com/bank.jpg"
image = Image.open(requests.get(url, stream=True).raw)
source_text = "The bank was crowded."

# Prepare prompt for disambiguation-aware translation
prompt = f"""
Translate to Spanish, ensuring correct disambiguation.

Image: [banking/financial institution context]
Source: {source_text}

Consider the visual context when choosing between:
- "banco" (financial institution)
- "orilla" (river bank)

Translation:
"""

# Process and generate
inputs = processor(text=prompt, images=image, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
translation = processor.decode(outputs[0], skip_special_tokens=True)

print(f"Source: {source_text}")
print(f"Translation: {translation}")
```

---

## Related Work & Context

### Prior Work in Multimodal MT

1. **Early MMT Systems (2016-2020):**
   - Simple image features concatenated to MT encoders
   - Limited vision model architectures
   - Focus on image-to-caption tasks

2. **Vision-Language Models (2021-2024):**
   - CLIP, BLIP, LLaVA emergence
   - Stronger visual understanding
   - Adapted to translation tasks

3. **Ambiguity in NLP:**
   - Word sense disambiguation
   - Pronoun resolution
   - Semantic role labeling

### Related Datasets

- **COCO-CN:** Chinese image captions (5K images)
- **Multi30K:** English-German visual descriptions (31K images)
- **LSMDC:** Movie descriptions with visual grounding (128K images)

### Complementary Approaches

- **Back-translation:** Monolingual data augmentation
- **Pivot Languages:** Intermediate language pairs
- **Knowledge Distillation:** Smaller efficient models
- **Prompt-based MT:** Few-shot translation with LLMs

### Future Research Directions

1. **Video Grounding:** Temporal ambiguity in video translation
2. **Interactive MT:** User feedback for disambiguation
3. **Zero-shot Ambiguity:** Generalizing to unseen ambiguities
4. **Multimodal Reasoning:** Complex scenarios with multiple images
5. **Cross-lingual Ambiguity:** Language-specific disambiguation challenges

---

## Key Takeaways

"A Multimodal Dataset for Visually Grounded Ambiguity in Machine Translation" addresses a fundamental gap in evaluating real-world translation challenges:

1. **Targeted Evaluation:** Moves beyond aggregate metrics to specific disambiguation tasks
2. **Dataset Contribution:** Enables systematic study of visual grounding in MT
3. **Method Validation:** Demonstrates CoT fine-tuning's effectiveness
4. **Practical Impact:** Improves translation quality for ambiguous expressions
5. **Future Benchmark:** Establishes standard for multimodal MT evaluation

The work reflects a broader trend toward **targeted evaluation**—rather than optimizing for generic metrics, the field is developing specialized benchmarks that capture real-world linguistic phenomena. VIDA exemplifies this shift by directly measuring whether multimodal systems can leverage visual context to resolve the inherent ambiguity of natural language.

