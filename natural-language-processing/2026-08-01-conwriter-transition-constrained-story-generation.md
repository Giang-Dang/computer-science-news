# ConWriter: Transition-Constrained Stateful Long-Form Story Generation with Lightweight Neuro-Symbolic Consistency Control

**ArXiv ID:** 2608.05169  
**Authors:** Jindong Li, et al.  
**Submitted:** August 2026  
**Field:** Natural Language Processing, Generative Models

## Executive Summary

ConWriter introduces a training-free framework for generating coherent long-form stories that maintain narrative consistency across extended contexts. By combining neural language generation with lightweight symbolic reasoning about story state transitions, ConWriter addresses a fundamental challenge in AI-generated narrative: the accumulation of temporal, factual, character, and stylistic inconsistencies as stories grow. This work is significant for content creation, interactive fiction, and any application requiring coherent long-horizon text generation.

## Problem Statement

Contemporary language models struggle with long-form story generation due to several compounding challenges:

**Core Issues:**
- **Context window limitations:** Relevant past information gets pushed out of context as stories grow
- **Consistency drift:** Subtle inconsistencies accumulate (character names change, timeline contradictions, plot holes)
- **Error propagation:** Early mistakes in story state become harder to fix as dependent content is generated
- **Constraint satisfaction:** Maintaining logical narrative structure and satisfying story requirements

**Consistency Errors Include:**
1. Temporal inconsistencies (timeline contradictions, impossible sequences)
2. Factual errors (contradictory character facts, setting details)
3. Character inconsistencies (personality shifts, relationship changes)
4. Commonsense violations (physics, social norms)
5. Stylistic drift (tone, narrative perspective changes)

**Why Existing Approaches Fall Short:**
- Pure prompting-based methods have no mechanism to track or validate narrative state
- Full neuro-symbolic approaches require expensive training
- Hard constraint methods are brittle and reduce generation quality
- Centralized tracking is computationally expensive for long contexts

## Core Concepts & Theory

### Scene-Level Generation Architecture

ConWriter decomposes long-form story generation into manageable scenes:

**Key Insight:** Rather than generating paragraph-by-paragraph, structure story generation at semantic scene boundaries where narrative state is well-defined and checkable.

### Lightweight Neuro-Symbolic System

**Three Core Components:**

1. **Static Story Requirements**
   - Plot points that must occur
   - Character constraints (who exists, key relationships)
   - Setting specifications
   - Encoded as simple structured data (no training needed)

2. **Dynamic Narrative Memory**
   - Maintains evolving story state across scenes
   - Tracks: character relationships, factual details, plot advancement, timeline
   - Updated after each scene generation
   - Lightweight symbolic representation (not full semantic parse)

3. **Uncertainty-Aware Risk Signals**
   - Models uncertainty in generated content
   - Identifies which narrative elements might be inconsistent
   - Prioritizes validation for high-risk elements
   - Guides targeted repair before errors propagate

### Consistency Validation Mechanism

**Transition Checking:**
- Verifies that new scenes satisfy required narrative transitions
- Checks temporal ordering is consistent
- Validates character state changes are logically justified
- Confirms plot progression toward goals

**Localized Repair:**
- When inconsistencies detected, re-generate only affected passage
- Uses updated narrative context for repair
- Prevents costly full-story regeneration
- Maintains story coherence with minimal computational overhead

## Main Ideas & Contributions

1. **Scene-Level Decomposition:** Novel approach to managing context by decomposing generation into narrative units with clear state boundaries

2. **Lightweight Symbolic Reasoning:** Minimal-training symbolic component that catches errors early without expensive full neuro-symbolic inference

3. **Uncertainty-Guided Validation:** Probabilistic approach to consistency checking that focuses validation efforts where needed most

4. **Training-Free Framework:** Works with existing language models without fine-tuning, enabling rapid deployment

5. **Systematic Consistency Taxonomy:** Comprehensive framework for understanding and addressing narrative consistency problems

## Methodology & Implementation

### Story Generation Pipeline

**Phase 1: Story Planning**
- Parse story requirements (plot points, characters, constraints)
- Initialize narrative memory with character/setting information
- Create scene outline

**Phase 2: Scene Generation**
- Generate scene content using LLM guided by:
  - Current narrative memory state
  - Scene objectives
  - Character constraints
  - Temporal ordering requirements

**Phase 3: Consistency Validation**
- Check narrative transitions
- Validate temporal consistency
- Assess character consistency
- Identify uncertainty-flagged content for review

**Phase 4: Targeted Repair**
- For detected inconsistencies: re-generate problematic passage
- For high-uncertainty content: request confirmation or regenerate
- Update narrative memory based on validated content

### Experimental Setup

**Benchmark:** ConStory-Bench with four tasks:
- **Continuation:** Extend existing story while maintaining consistency
- **Generation:** Create complete story from requirements
- **Expansion:** Add details to story outline
- **Completion:** Finish partial story coherently

**Baselines:**
- Direct LLM generation without consistency checks
- Naive prompting approaches
- Full neuro-symbolic methods (for comparison)

### Evaluation Metrics

[Exact figures unavailable — see full paper]

Key metrics likely include:
- **Consistency score:** Fraction of consistency checks passed
- **Human evaluation:** Coherence, narrativity, engagement ratings
- **Error types:** Breakdown of temporal vs. factual vs. character errors
- **Efficiency:** Computation cost vs. naive regeneration
- **Story quality:** Length, complexity, plot sophistication

### Results

ConWriter demonstrates:
- Significant reduction in consistency errors compared to baseline language model generation
- Minimal computational overhead vs. naive consistency checking approaches
- Effective maintenance of narrative coherence across extended stories
- Preservation of story quality and engagement despite consistency constraints
- Successful handling of complex narrative structures with multiple characters and timelines

## Practical Applications & Use Cases

### Interactive Fiction & Gaming
- Dynamic narrative generation for interactive fiction systems
- Dialogue-driven story generation with character consistency
- Procedural content generation for game narratives

### Content Creation Platforms
- Assisted novel writing with automated consistency checking
- Screenplay generation maintaining plot coherence
- Blog/article series generation with consistent voice

### Educational Applications
- Personalized educational stories that maintain learning narrative
- Interactive textbooks with branching narratives
- Case study generation for training scenarios

### Chatbot & Conversational AI
- Story-telling chatbots that maintain consistent personas
- Long-horizon conversation systems
- Interactive narrative experiences

### Entertainment & Publishing
- Automated story generation for entertainment platforms
- Writing assistant tools for human authors
- Localization and adaptation while preserving narrative structure

## Insights & Implications

1. **Scene-Level Abstraction:** Narrative consistency is tractable when operating at appropriate level of abstraction (scenes vs. tokens/paragraphs)

2. **Hybrid Approaches Effective:** Lightweight symbolic reasoning provides significant consistency benefits without expensive learning

3. **Uncertainty Matters:** Explicit uncertainty modeling enables efficient resource allocation for consistency verification

4. **Practical Scalability:** Framework scales to multi-page stories while remaining computationally practical

5. **Training-Free Deployment:** Enables immediate use with existing models without infrastructure investment

## Limitations & Open Questions

1. Requires clear narrative structure (less suitable for experimental/avant-garde narratives)
2. Performance on very long contexts (100+ pages) not extensively explored
3. Handling of surprise plot elements that violate established patterns
4. Quality of symbolic memory representation on complex narratives
5. Cross-lingual narrative consistency maintenance

## Code & Resources

**Official Repository:** [To be confirmed in paper]
**Key Dependencies:**
- Language model API (OpenAI API, HuggingFace, or local models)
- Symbolic reasoning framework (likely lightweight rule engine)
- Story representation library

**Benchmark Data:** ConStory-Bench available for evaluation

## Related Work & Context

### Foundation Areas
- Long-form text generation with language models
- Narrative understanding and story comprehension
- Symbolic reasoning systems for NLP
- Consistency and coherence in generated text

### Related Recent Work
- StoryWriter: Multi-agent framework for long story generation
- Long-context modeling approaches
- Neuro-symbolic NLP systems
- Consistency checking in machine translation

### Future Research Directions
- Scaling to very long stories (novelength)
- Multi-author collaborative story generation
- Cross-media narrative (text + image + video consistency)
- User interactive feedback integration
- Generation of surprising yet consistent plot twists
- Cross-cultural and cross-lingual narrative consistency
