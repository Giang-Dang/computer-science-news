# AutoDesign: Meta-Harness Optimization for Long-Horizon Agentic Design

**ArXiv ID:** 2608.13560  
**Submission Date:** August 13, 2026  
**Authors:** Multiple institutions including Meituan, MBZUAI, Huazhong University of Science and Technology, Peking University, Tsinghua University  
**Paper Link:** https://arxiv.org/abs/2608.13560

## Executive Summary

AutoDesign introduces a novel framework for long-horizon agentic design tasks where transforming multimodal sources (research papers, data, specifications) into structured media outputs is conceptualized as an iterative process guided by a meta-harness optimizer. The framework enables autonomous code agents to recursively improve design harnesses based on rollout feedback. On paper-to-poster generation, AutoDesign achieves a 78.32 score, outperforming commercial systems and demonstrating the viability of automated long-horizon design automation.

## Problem Statement

Long-horizon multimodal design tasks—such as converting academic papers into presentation posters—require complex reasoning, content synthesis, and iterative refinement. Traditional approaches either rely on manual human effort or isolated tool chains that lack coherent optimization. The research gap addresses the need for end-to-end autonomous systems that can reason over multimodal inputs, maintain design consistency, and iteratively improve outputs through feedback-guided optimization.

## Core Concepts & Theory

### Model-Harness Architecture

The core insight of AutoDesign is separating the design problem into:
- **Model Component:** The language model performing generative tasks
- **Harness Component:** The execution framework orchestrating tool calls, reasoning, and state management

This separation enables optimization at the harness level without modifying the underlying model, creating a flexible, interpretable design system.

### Meta-Harness Optimizer

The meta-harness optimizer functions as a high-level controller that:
1. Observes rollout trajectories from code agents executing harnesses
2. Extracts failure patterns and performance bottlenecks
3. Proposes iterative harness improvements (editing prompts, refining tool specifications, adjusting reasoning flows)
4. Validates improvements on validation sets before deployment

### Long-Horizon Reasoning Strategy

The framework employs a recursive refinement loop:
- **Initial Harness Design:** Based on task specification and design principles
- **Agent Execution:** Code agent executes the harness with tool access (layout generators, content extractors, etc.)
- **Feedback Collection:** Outputs evaluated against design quality metrics
- **Harness Optimization:** Meta-harness proposes targeted improvements
- **Iteration:** Process repeats until convergence or resource limits

## Main Ideas & Contributions

### 1. Agentic Design Conceptualization

**Innovation:** Framing complex design tasks as agentic optimization problems where both the agent and its harness co-evolve based on performance feedback.

**Significance:** Enables systematic automation of tasks previously requiring human designers, while maintaining explainability through explicit harness editing.

### 2. PosterBench Evaluation Framework

**Contribution:** A comprehensive benchmark comprising:
- **Main Track:** 100 academic papers spanning five disciplines (ML, CV, NLP, Systems, AI)
- **Mini Track:** 10 papers for controlled evaluation and reproducibility
- **Evaluation Metrics:** Automated checks plus human evaluation of design quality, accuracy, and visual coherence

**Impact:** Provides standardized evaluation for long-horizon agentic design systems beyond paper-to-poster generation.

### 3. Cost-Effective Long-Horizon Automation

**Key Result:** AutoDesign executes 253 tool calls and 11 editing turns within 40 minutes for under $3 using accessible models, demonstrating practical scalability.

**Technical Achievement:** Demonstrates that careful harness design enables efficient long-horizon reasoning without requiring state-of-the-art frontier models.

## Methodology & Implementation

### Experimental Setup

**Task Definition:** Convert academic research papers into conference-quality posters, requiring:
- Title and abstract extraction
- Key contribution visualization
- Result summarization
- Visual layout optimization

**Baseline Comparison:**
- Closed-source commercial system (Claude Design): 70.87 score
- Human designer reference: 82.15 score (upper bound)
- AutoDesign: 78.32 score

### Evaluation Protocol

**Automated Evaluation:**
- Design structure validation (required sections present)
- Typography correctness (font sizes, spacing)
- Content accuracy (information from source paper faithfully represented)

**Human Evaluation:**
- Expert review on visual design quality
- Judged correctness and completeness of content
- Assessed overall conference-poster suitability

### Results

AutoDesign achieves 78.32/100 on PosterBench Main Track, surpassing Claude Design by 7.45 points. Detailed breakdown [Exact figures unavailable — see full paper].

**Performance Characteristics:**
- Execution time: 40 minutes per paper
- Cost per paper: <$3 USD
- Tool calls per iteration: ~253 over full pipeline
- Harness edits: ~11 refinement rounds

### Comparison with Existing Approaches

| Approach | Automation Level | Design Quality | Cost | Scalability |
|----------|-----------------|-----------------|------|------------|
| Manual Design | Low | High | High | Low |
| Template-Based | High | Low | Low | High |
| AutoDesign | High | 78.3/100 | <$3 | High |
| Claude Design | High | 70.9/100 | [Not disclosed] | High |

## Practical Applications & Use Cases

### Academic Publishing
- Automated poster generation for conference submissions
- Slide deck creation from research papers
- Visual abstract generation for journals

### Content Generation
- Systematic conversion of white papers to marketing collateral
- Technical documentation to presentation materials
- Research reports to executive summaries

### Design Automation
- Templated design systems that maintain brand consistency while adapting content
- Batch processing of multimodal content into standardized outputs
- Quality-controlled design pipelines for enterprise content management

### Educational Applications
- Automated generation of teaching materials from research papers
- Creation of visual study aids for complex technical concepts
- Standardized presentation of research across departments

## Insights & Implications

### Broader Field Impact

AutoDesign demonstrates that long-horizon creative tasks can be systematically automated through careful separation of concerns (model vs. harness) and iterative optimization. This challenges the assumption that design requires human judgment and opens new directions for agentic automation.

### State-of-the-Art Advancement

The framework achieves results within 4% of human designers while operating at 1/27th the cost (human-hours basis), suggesting that agentic design systems can meaningfully complement human designers in production workflows.

### Key Limitations and Open Questions

1. **Generalization:** How well does the learned harness transfer to novel paper domains or design formats?
2. **Explainability:** While harness editing provides some transparency, the evolution of harness quality metrics remains somewhat opaque
3. **Feedback Loop Stability:** Long refinement loops risk converging to local optima in harness design space
4. **User Customization:** Current approach assumes fixed design objectives; adaptability to user preferences needs exploration

### Future Research Directions

- **Multi-Agent Collaboration:** Exploring systems where multiple specialized agents co-design harnesses
- **Cross-Domain Transfer:** Applying meta-harness optimization to other long-horizon tasks (video editing, software development)
- **Interactive Refinement:** Incorporating human-in-the-loop feedback for faster harness convergence
- **Theoretical Analysis:** Formal analysis of harness optimization dynamics and convergence properties

## Code & Resources

**Official Resources:**
- Project Website: https://autodesign.designanything.ai
- Code Repository: [Available on GitHub as per paper]
- Benchmark Data: PosterBench (100 papers + mini track)

**Dependencies & Requirements:**
- Language models (tested with multiple frontier models)
- Tool APIs for design elements (layout, typography, image processing)
- Evaluation infrastructure (automated metrics + human evaluation protocols)

**Compute Requirements:**
- ~40 minutes per task on standard cloud infrastructure
- <$3 per task in API costs
- No specialized hardware required

## Related Work & Context

### Prior Work Foundations
- **Agentic AI Systems:** Builds on research in language model agents and tool use
- **Iterative Optimization:** Related to reinforcement learning from human feedback (RLHF) and evolutionary algorithms
- **Design Automation:** Connects with graphical design synthesis and automatic UI generation literature

### Complementary Research
- **Meta-Learning:** Harness optimization relates to learning-to-learn and hyperparameter optimization
- **Prompt Optimization:** Similar principles to recent work on automatic prompt engineering
- **Long-Horizon Reasoning:** Relates to planning and hierarchical reinforcement learning

### Future Research Connections
- Integration with multimodal foundation models for improved creative reasoning
- Application to software engineering tasks (code generation with iterative refinement)
- Expansion to interactive design scenarios with real-time user feedback
