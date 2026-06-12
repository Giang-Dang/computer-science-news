# Watch, Remember, Reason: Human-View Video Understanding with MLLMs

**Authors:** Jiahao Meng, Yue Tan, Qi Xu, Kuan Gao, Weisong Liu, Yanwei Li, Jason Li, Lingdong Kong, Haochen Wang, Qianyu Zhou, Jiangning Zhang, Guangliang Cheng, Yunhai Tong, Lu Qi, Minghsuan Yang  
**Affiliations:** Peking University, Wuhan University, Shanghai Jiao Tong University, and others  
**ArXiv ID:** 2606.07433  
**Submitted:** June 5, 2026  
**Category:** Computer Vision / Multimodal Learning  

## Executive Summary

This comprehensive survey examines how multimodal large language models (MLLMs) are transforming video understanding, moving from short clips to long, complex, knowledge-intensive sequences. The work organizes the landscape around three functional capabilities—watching, remembering, and reasoning—and identifies critical challenges in spatio-temporal perception, efficient long-video processing, memory modeling, and faithful reasoning. By examining diverse application domains (egocentric, sports, instructional, medical, narrative videos) and evaluation benchmarks, the paper provides a structured roadmap for advancing video understanding at the intersection of vision and language.

## Problem Statement

### Evolution of Video Understanding

Video understanding has undergone a paradigm shift:

**Phase 1: Short-Clip Classification (2010s)**
- Static action recognition: classify 3-5 second clips
- Methods: 3D CNNs, optical flow, appearance-based models
- Limitation: Ignores temporal context and semantic reasoning

**Phase 2: Long-Video Comprehension (Early 2020s)**
- Dense video captioning, temporal grounding: understand clips within longer videos
- Methods: Transformer-based encoders, temporal attention
- Limitation: Still primarily appearance-based; limited language grounding

**Phase 3: Multimodal Reasoning (2025-2026)**
- Complex reasoning combining vision, audio, text, and knowledge
- Methods: Multimodal LLMs as foundation
- Challenges: Efficiency, memory, faithful reasoning

### Current Challenges with MLLMs for Video

MLLMs show promise but face several bottlenecks:

1. **Perceptual Challenges**
   - Fine-grained visual details often lost in compression to feed LLMs
   - Audio-visual alignment and synchronization
   - Efficient perception under computational constraints

2. **Memory and Context**
   - Long videos exceed typical LLM context windows
   - Selective memory: which frames/events are critical?
   - Streaming scenarios where memory must be continuously updated

3. **Reasoning Gap**
   - LLMs excel at language reasoning but struggle with spatial-temporal reasoning
   - Hallucinations in video descriptions
   - Lack of grounding for factual claims

4. **Computational Efficiency**
   - Processing full-resolution videos is expensive
   - Token budgets limit how much information can be passed to the LLM
   - Real-time applications (autonomous driving, surveillance) require speed

### Research Gap

While short video understanding with MLLMs is well-studied, comprehensive frameworks addressing all three capabilities (watching → remembering → reasoning) across diverse video types remain limited. The field lacks a unified taxonomy and systematic evaluation methodology.

## Core Concepts & Theory

### Three-Capability Framework

The survey organizes video understanding around three interconnected capabilities:

#### 1. Watching (Perception)

**Definition**: Extracting meaningful visual and audio information from video streams.

**Challenges Addressed**:

- **Fine-grained Perception**: Capturing details beyond what standard video encoders preserve
  - Solution approaches: High-resolution region focus, salient frame selection, specialized detectors for details
  
- **Comprehensive Perception**: Holistic scene understanding
  - Includes object detection, scene understanding, activity recognition
  - Requires balance between detail and efficiency
  
- **Audio-Visual Alignment**: Synchronizing and integrating audio and visual modalities
  - Many video events are best understood multi-modally (speech + visual context)
  - Challenges: Temporal misalignment, background noise
  
- **Efficient Perception**: Reducing computational cost while maintaining information richness
  - Techniques: Frame subsampling, dynamic frame selection, adaptive compression

**Subcategories**:
- Fine-grained, comprehensive, audio-visual, efficient

#### 2. Remembering (Memory)

**Definition**: Maintaining and retrieving relevant information across long video sequences.

**Memory Paradigms**:

- **Offline Memory**: Processing entire video before reasoning begins
  - Approach: Aggregate features, compress key frames, summarize segments
  - Advantage: Global context, thorough processing
  - Disadvantage: High latency, large memory footprint
  
- **Streaming Memory**: Incrementally processing video and maintaining running memory
  - Approach: Sliding windows, hierarchical summaries, selective retention
  - Advantage: Low latency, online applicability
  - Disadvantage: Risk of losing distant but important information

**Key Challenges**:
- **Memory Compression**: Fitting long videos into limited token budgets
- **Importance Weighting**: Deciding what to remember vs. forget
- **Temporal Dynamics**: Tracking changes and causality over time

#### 3. Reasoning (Inference)

**Definition**: Using memorized information to answer questions, make predictions, or generate descriptions.

**Reasoning Modalities**:

- **Text-Only Reasoning**: Generate descriptions or answers based on visual memory
  - Challenges: Ensuring generated text is grounded in video, avoiding hallucinations
  
- **Thinking with Videos**: Intermediate reasoning steps that explicitly ground reasoning in visual evidence
  - Approach: Chain-of-thought, grounding in specific frames/regions
  - Benefit: More transparent and verifiable reasoning

**Challenges**:
- **Faithfulness**: Ensuring reasoning respects visual evidence
- **Completeness**: Covering all relevant aspects
- **Efficiency**: Scaling reasoning to complex videos

### Spatio-Temporal Concepts

#### Spatio-Temporal Perception

Understanding objects, actions, and events distributed across space and time:

- **Objects**: Tracking identity and position over time
- **Actions**: Understanding how objects interact and change
- **Events**: Aggregating actions into meaningful occurrences
- **Scenes**: Understanding the overall spatial-temporal context

#### Long-Range Dependencies

Video understanding requires reasoning about causality and correlation across distant frames:

- **Causal**: Event A causes event B (e.g., person picks up cup → person drinks)
- **Narrative**: Events form a coherent story arc
- **Functional**: Objects have roles that persist (protagonist, antagonist)

## Main Ideas & Contributions

### 1. Comprehensive Taxonomy

**Contribution**: First systematic organization of video understanding with MLLMs around functional capabilities (watching → remembering → reasoning).

**Impact**: Provides a clear conceptual framework for researchers to locate their work and identify gaps.

### 2. Multi-Domain Analysis

**Contribution**: Examines how capabilities differ across application domains:
- **Egocentric** (first-person): Spatial understanding, hand-object interaction
- **Sports**: Action recognition, tactical understanding, player tracking
- **Instructional** (how-to): Temporal step sequences, object manipulation
- **Medical**: Clinical reasoning, anatomical understanding, diagnostic reasoning
- **Narrative**: Story understanding, character development, plot progression

**Value**: Reveals domain-specific challenges and solution approaches.

### 3. Challenge Identification

**Key Challenges Mapped**:

| Challenge | Watching | Remembering | Reasoning |
|-----------|----------|-------------|-----------|
| **Spatio-temporal** | Tracking, scene understanding | Maintaining object identity | Causality reasoning |
| **Long-video** | Efficiency at scale | Compression, forgetting | Context limitation |
| **Memory** | Extraction | Consolidation | Retrieval |
| **Streaming** | Real-time processing | Online updates | Interactive reasoning |
| **Faithfulness** | Accuracy of perception | Fidelity of memory | Grounding verification |

### 4. Benchmark and Evaluation Framework

**Contribution**: Surveys existing benchmarks and proposes evaluation dimensions:
- **Task Types**: VQA, captioning, grounding, retrieval, prediction
- **Supervision**: Annotations (frames, regions, captions, scripts)
- **Modalities**: Video, audio, text, multimodal
- **Capability Dimensions**: Perception fidelity, memory efficiency, reasoning correctness

**Impact**: Enables systematic comparison across methods and motivates new benchmarks.

## Methodology & Implementation

### Survey Methodology

The paper conducts a comprehensive literature review organized by:

1. **Capability-first organization**: What approaches address watching, remembering, and reasoning?
2. **Domain analysis**: How do solutions differ across video types?
3. **Benchmark evaluation**: What metrics and datasets are used?
4. **Trend analysis**: What directions is the field moving?

### Benchmark Coverage

#### Task-Specific Benchmarks

**Video Question Answering (VQA)**
- Examples: MSRVTT-QA, ActivityNet-QA, EgoSchema
- Evaluation: Accuracy of answers requiring different reasoning types
- Reasoning Type: Temporal order, counting, causality, comparison

**Dense Video Captioning**
- Examples: YouCook2, CrossTask, VATEX
- Evaluation: BLEU, METEOR, CIDEr scores measuring caption quality
- Coverage: Short descriptions vs. detailed narration

**Temporal Action Localization**
- Examples: Charades-STA, ActivityNet
- Evaluation: Intersection-over-Union (IoU) at different thresholds
- Requirement: Grounding language to specific temporal regions

**Video Grounding**
- Examples: ViTT, Didemo, ANET-SV
- Evaluation: Localization accuracy (frame-level IoU)
- Challenge: Fine-grained temporal alignment

### Evaluation Metrics

#### Vision-Language Metrics

- **BLEU, METEOR, CIDEr**: Standard NLP metrics applied to video captioning
- **SPICE**: Semantic similarity of captions
- **VQA Accuracy**: Exact match or fuzzy match for VQA tasks

#### Spatio-Temporal Metrics

- **Temporal IoU**: Overlap between predicted and ground-truth temporal regions
- **Spatial IoU**: Overlap for bounding boxes or regions
- **Spatio-Temporal IoU**: Combined metric for localization tasks

#### Reasoning Metrics

- **Faithfulness**: Does generated text align with video content? [Exact figures unavailable — see full paper]
- **Completeness**: How much of relevant information is captured?
- **Efficiency**: Tokens used vs. quality achieved

## Practical Applications & Use Cases

### 1. Autonomous Driving

**Application**: Understanding road scenes from vehicle cameras

**Challenges Specific to Domain**:
- Real-time constraints (streaming perception)
- Safety-critical reasoning (prediction of accidents)
- Multi-modal signals (video + sensor data)

**Implementation Complexity**: High

**Feasibility**: Moderate—safety-critical applications require verified systems

**Current Status**: Active research area; no production systems widely deployed yet

### 2. Robotic Manipulation and Navigation

**Application**: Robots understanding task instructions from videos or generating navigation plans from visual observations

**Key Requirements**:
- Egocentric understanding (robot's perspective)
- Spatial reasoning (object layouts, reachability)
- Action understanding (step-by-step task decomposition)

**Feasibility**: Moderate to High—depends on environment structure

### 3. Healthcare and Medical Video Analysis

**Application**: Surgical video understanding, patient monitoring, clinical reasoning

**Domain-Specific Challenges**:
- Limited training data (privacy-restricted, domain-specific)
- High stakes for errors (patient safety)
- Specialized vocabulary and domain knowledge

**Opportunities**:
- Efficient memory for long surgeries (hours of video)
- Reasoning combining visual and textual knowledge

### 4. Sports Analysis and Commentary

**Application**: Generating real-time commentary, tactical analysis, highlight generation

**Advantages**:
- Abundant training data and benchmarks
- Clear event definitions and ground truth
- Commercial applications (broadcasting, coaching)

**Implementation Status**: Active commercial deployment; MLLMs could improve richness of analysis

### 5. Social Media and Content Understanding

**Application**: Video recommendation, content moderation, hashtag generation, summary generation

**Challenges**:
- Diversity of content (short clips to long-form videos)
- Detecting context-dependent sensitive content
- Summarization under time constraints

**Scale**: Billions of videos daily; efficiency critical

### 6. Educational Video Analysis

**Application**: Understanding instructional videos for knowledge extraction, quiz generation, personalized learning

**Opportunities**:
- Structured task knowledge (step sequences, prerequisites)
- Reasoning about domain concepts
- Multi-language support

## Insights & Implications

### Paradigm Shifts in Video Understanding

**From Static Features to Dynamic Reasoning**
- Before: Features extracted from frames, processed independently
- After: Language models reason about spatio-temporal dynamics
- Implication: Causality and abstraction become tractable

**From Supervised Learning to Foundation Models**
- Before: Task-specific models trained on annotated data
- After: General-purpose MLLMs fine-tuned with minimal data
- Implication: Broader generalization but reduced control over behavior

**From Single-Modality to Multi-Modality**
- Before: Primarily visual + minimal audio
- After: Integrated visual, audio, and knowledge reasoning
- Implication: Richer understanding but higher computational cost

### State-of-the-Art Advancements

The paper identifies several emerging advances:

1. **Memory-Efficient Long-Video Processing**
   - Hierarchical memory structures
   - Learnable importance weighting
   - Streaming inference protocols

2. **Fine-grained Perception Methods**
   - Region-based processing for details
   - Salient frame selection
   - Specialized modules for scene understanding

3. **Reasoning with Grounding**
   - Explicit grounding in frames/regions
   - Chain-of-thought reasoning for videos
   - Verifiable reasoning traces

### Limitations and Open Questions

1. **Hallucination Problem**
   - Challenge: MLLMs generate plausible-sounding but false statements about videos
   - Status: Partially understood, solutions emerging
   - Open: How to guarantee factual accuracy?

2. **Temporal Reasoning**
   - Challenge: Understanding causal and narrative sequences
   - Status: Better than appearance-only models, still limited
   - Open: How to build compositional temporal understanding?

3. **Real-time Processing**
   - Challenge: Current systems optimized for offline analysis
   - Status: Streaming models emerging, latency still high
   - Open: Sub-100ms streaming inference for safety-critical applications?

4. **Domain Generalization**
   - Challenge: Models trained on one video type struggle on another
   - Status: Limited evidence of transfer
   - Open: What properties enable cross-domain transfer?

5. **Computational Efficiency**
   - Challenge: Processing high-resolution videos is expensive
   - Status: Multiple compression approaches proposed
   - Open: Fundamental limits on efficiency-quality tradeoffs?

## Code & Resources

### Benchmark Datasets

**Major Video Understanding Benchmarks**:

1. **MSRVTT** (Million Video Text)
   - 10K videos, 200K captions
   - Tasks: VQA, retrieval, captioning
   - Language: English

2. **ActivityNet** (Extended)
   - 15K long videos with dense annotations
   - Tasks: Action localization, captioning
   - Language: English

3. **YouCook2**
   - 2K instructional videos
   - Dense captions for steps
   - Domain: Cooking videos

4. **EgoSchema** (Egocentric)
   - Long-form egocentric videos
   - Multiple-choice QA
   - Domain: Diverse first-person activities

5. **CrossTask**
   - Instructional videos with step annotations
   - Cross-domain alignment
   - Domain: How-to videos

### Implementation Stack for Practitioners

**Recommended Architecture**:

1. **Video Encoder**
   - Options: ViT-L (vision transformer), R3D (3D CNN), CLIP-based (multimodal pre-training)
   - Choice impacts: Perception quality, computation cost

2. **Memory Module**
   - Options: Sliding window attention, hierarchical summarization, learned compression
   - Design: Balance between completeness and efficiency

3. **Language Model**
   - Options: LLaMA, Mistral, GPT-based foundations
   - Fine-tuning: LoRA, prefix-tuning for efficiency

4. **Reasoning Framework**
   - Options: Chain-of-thought prompting, in-context examples, retrieval-augmented
   - Grounding: Explicit frame/region references

### Quick-Start Pipeline

To implement an MLLM for video understanding:

1. **Select encoder**: Trade-off resolution vs. latency
2. **Design memory**: Choose offline or streaming; decide compression ratio
3. **Choose LLM**: Balance capability (larger = more capable) vs. latency
4. **Implement reasoning**: Chain-of-thought, grounding mechanisms
5. **Evaluate**: Use established benchmarks; measure latency + quality
6. **Optimize**: Profile bottlenecks; apply domain-specific techniques
7. **Validate**: Test on application-specific scenarios before deployment

## Related Work & Context

### Foundation Work: Vision and Language

- **Vision Transformers (ViT)**: Enabled efficient visual encoding of images
- **Large Language Models**: Enabled reasoning and generation at scale
- **Multimodal Pre-training**: CLIP, ALIGN, others grounded vision in language
- **Video Transformers**: TimeSformer, ViViT extended vision models to video

### Recent Advances in MLLMs

- **CLIP-based models**: Efficient visual-language alignment
- **Diffusion models**: High-quality image/video generation
- **Large-scale pre-training**: Foundation models for video understanding
- **Efficient inference**: LoRA, quantization, flash attention for speed

### Related Recent Papers

- Video question answering systems
- Temporal action localization benchmarks
- Egocentric video understanding
- Long-form video understanding systems
- Instructional video analysis

## Future Research Directions

### Short-term (1-2 years)

1. **Better Efficiency**
   - More efficient memory structures for long videos
   - Lighter perception encoders without quality loss
   - Streaming inference protocols

2. **Reasoning Grounding**
   - Explicit grounding in frame/region references
   - Reducing hallucinations through fact-checking
   - Verifiable reasoning traces

3. **Domain-Specific Fine-tuning**
   - Benchmarks and models for specialized domains (medical, sports, instructional)
   - Transfer learning approaches

### Medium-term (2-4 years)

1. **Real-time Systems**
   - Sub-100ms inference for autonomous systems
   - Streaming perception-memory-reasoning pipelines
   - Hardware-aware optimization

2. **Multimodal Reasoning**
   - Integration of additional modalities (3D, sensor data, knowledge bases)
   - Cross-modal reasoning mechanisms
   - Unsupervised or self-supervised learning approaches

3. **Compositional Understanding**
   - Understanding complex narratives and causality
   - Temporal reasoning with formal semantics
   - Knowledge-grounded reasoning

### Long-term (4+ years)

1. **Human-Level Video Understanding**
   - Matching human performance on reasoning tasks
   - Natural language understanding of videos
   - Open-ended exploration and discovery from video

2. **Personalization**
   - Adapting to individual preferences and knowledge
   - Few-shot learning from user examples
   - Interactive learning and correction

3. **Trustworthiness**
   - Certified reasoning with formal guarantees
   - Interpretability of decisions
   - Fairness and bias mitigation

## Significance and Impact

This comprehensive survey arrives at a critical juncture in video understanding research. As multimodal models become more capable, the field is transitioning from perception-focused tasks (what's in the video?) to reasoning-focused tasks (why did that happen?). The three-capability framework (watching-remembering-reasoning) provides conceptual clarity to this transition and maps out the technical landscape clearly.

The paper's examination of domain-specific challenges reveals that video understanding is not one problem but a family of related problems. Medical videos present different challenges than sports videos; egocentric understanding differs fundamentally from third-person. This diversity means that a one-size-fits-all approach will fail—future systems must be adaptive and composable.

Finally, the detailed identification of open challenges should motivate targeted research efforts. Hallucination, efficiency, real-time processing, and temporal reasoning are not minor limitations; they are fundamental barriers to deploying video understanding systems in safety-critical applications. Addressing these will require not just better engineering but potentially new algorithmic and architectural innovations.
