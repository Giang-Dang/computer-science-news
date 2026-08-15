# MLReplicate: Benchmarking Autonomous Research Systems for Machine Learning Reproducibility

**ArXiv ID:** 2605.16616  
**Submission Date:** May 15, 2026  
**Authors:** Sasi Kiran Gaddipati, Diyana Muhammed, Farhana Keya, Gollam Rabby, Sören Auer  
**Paper Link:** https://arxiv.org/abs/2605.16616

## Executive Summary

MLReplicate introduces the first comprehensive end-to-end benchmark for evaluating autonomous research systems on machine learning reproducibility. By testing six state-of-the-art autonomous research systems on papers from ICML 2025, the benchmark reveals substantial gaps between automated evaluation and rigorous scientific standards. Notably, 59% of papers accepted by automated review contained fabricated or unsupported claims, and neither computational cost nor token budget predicted output quality, fundamentally challenging assumptions about autonomous research quality.

## Problem Statement

Autonomous AI research systems promise to accelerate scientific discovery by generating novel experiments, analyzing results, and producing complete research manuscripts. However, existing evaluation methods—often automated metrics or limited expert review—fail to capture the full spectrum of scientific rigor requirements. The critical gap lies in understanding: (1) Can autonomous systems produce genuinely reproducible research? (2) How well do cheap/fast systems perform compared to expensive/slow ones? (3) What are the failure modes of automated research generation? This work establishes a rigorous evaluation framework addressing these questions.

## Core Concepts & Theory

### Autonomous Research Pipeline

Autonomous research systems typically follow this architecture:
1. **Task Specification:** Input problem statement and research direction
2. **Experiment Design:** Autonomous system designs experiments and methods
3. **Code Generation:** System writes implementation code
4. **Execution:** Runs experiments on data
5. **Analysis:** Analyzes results and generates figures
6. **Manuscript Generation:** Produces complete research paper

### Evaluation Challenges

Traditional scientific evaluation relies on:
- **Reproducibility:** Can experiments be repeated with same results?
- **Methodology Soundness:** Are methods justified and implemented correctly?
- **Result Integrity:** Are reported metrics actual or hallucinated?
- **Contribution Novelty:** Does the work advance the field?

Automated systems struggle with:
- **Hallucination Detection:** Distinguishing real experimental results from generated ones
- **Methodological Soundness:** Verifying mathematical correctness of approaches
- **Reproducibility Verification:** Ensuring code actually implements described methods
- **Novelty Assessment:** Determining true contribution vs. incremental variation

### Dual-Protocol Evaluation Framework

MLReplicate employs two complementary evaluation approaches:
1. **Automated Conference-Style Review:** Mimics typical conference review process
2. **Structured Expert Evaluation:** Deep analysis by domain experts focusing on reproducibility and rigor

This dual approach reveals the gap between surface-level acceptance and genuine scientific validity.

## Main Ideas & Contributions

### 1. Comprehensive Benchmark Construction

**Dataset Source:** ICML 2025 Outstanding Papers
- Selected for high quality and established impact
- Reformulated into standardized input specifications for autonomous systems
- Each paper converted to structured task: problem statement, desired contribution type, dataset specifications

**Benchmark Size:**
- 100-paper evaluation set (exact subset configuration [Exact figures unavailable — see full paper])
- 45 generated manuscripts from 6 autonomous research systems
- 3 systems failed to produce complete outputs

**Why ICML Papers?**
- Guaranteed high scientific quality and rigorous evaluation
- Established metrics and benchmarks for comparison
- Rich documentation enabling accurate reformulation

### 2. Multi-System Comparative Evaluation

**Systems Evaluated:**
1. AI SCIENTIST-V1
2. AI SCIENTIST-V2
3. AGENT LABORATORY
4. CYCLERESEARCHER
5. AI RESEARCHER
6. TINY SCIENTIST

**Evaluation Dimensions:**
- **Computational Cost:** Total API tokens, dollar cost
- **Runtime:** Execution time per manuscript
- **Human Intervention:** Proportion requiring manual fixes
- **Scientific Quality:** As assessed by domain experts

### 3. Critical Finding: Cost-Quality Disconnect

**Key Discovery:** Neither token budget nor computational cost predicts output quality.

**Specific Result:** "The cheapest system outperforms the most resource-intensive system in human evaluation, despite a 38-fold difference in input tokens."

**Implication:** Quality emerges from architectural design and optimization strategies, not from raw computational expenditure. This challenges conventional assumptions about scaling laws applied to autonomous research.

### 4. Systematic Quality Gap Identification

**Automated Review vs. Human Evaluation:**
- **Automated Acceptance Rate:** ~[Exact rate unavailable — see full paper]
- **Actual Scientific Validity Rate:** Substantially lower
- **Hallucination Rate:** 59% of automated-accepted papers contained fabricated or unsupported claims

**Types of Failures Identified:**
1. **Hallucinated Experiments:** Reported results from experiments never executed
2. **Fabricated Metrics:** Generated numbers without corresponding computations
3. **Methodological Inconsistencies:** Code doesn't match described methodology
4. **Unsupported Claims:** Conclusions without supporting evidence
5. **Missing Ablations:** Incomplete experimental validation

## Methodology & Implementation

### Benchmark Construction Workflow

**Step 1: Paper Selection**
- Start with ICML 2025 outstanding papers (high baseline quality)
- Diverse topics: optimization, deep learning, fairness, systems

**Step 2: Task Reformulation**
- Convert papers to structured specifications
- Define inputs: problem statement, dataset, success criteria
- Remove solution description (force autonomous rediscovery)

**Step 3: System Evaluation**
- Each system receives identical problem specification
- Execution on standard compute budget
- Collection of final outputs (generated papers, code, results)

### Dual-Protocol Evaluation

**Protocol 1: Automated Conference Review**
- Parse generated papers
- Check for required sections (abstract, methodology, results)
- Validate citations and reference formatting
- Apply automated plagiarism detection
- Score using standard review rubrics

**Protocol 2: Expert Structured Evaluation**
- Domain experts (ML researchers) read each paper
- Evaluate reproducibility:
  - Can experiments be repeated?
  - Is code correct and complete?
  - Are results verifiable?
- Assess scientific rigor:
  - Sound methodology?
  - Appropriate baselines?
  - Adequate novelty?
  - Clear limitations?
- Identify specific failure modes

### Key Evaluation Metrics

**Reproducibility Metrics:**
- Code Completeness (0-100): Fraction of described methods implemented
- Experimental Verifiability (0-100): Can results be independently verified?
- Documentation Quality (0-100): Clarity of methodology description

**Scientific Quality Metrics:**
- Methodological Soundness (0-100): Validity of approach
- Baseline Adequacy (0-100): Appropriate comparisons included
- Novelty Assessment (0-100): True contribution vs. marginal variation

**Efficiency Metrics:**
- Total Tokens: API tokens consumed
- Runtime (hours): Wall-clock execution time
- Cost (USD): Direct API costs

### Experimental Results

**Performance Across Systems [Exact figures unavailable — see full paper]:**
- Systems show high variance in quality despite similar computational budgets
- Best-performing system achieves human-evaluation score of ~[exact score unavailable]
- Worst-performing system achieves ~[exact score unavailable]
- No correlation between cost and quality (Pearson r ≈ 0)

**Failure Mode Analysis:**
- Hallucination most common failure (~[Exact percentage unavailable — see full paper])
- Methodological errors second most common
- Code-description mismatch in ~[percentage unavailable] of cases

## Practical Applications & Use Cases

### Autonomous Research Development
- Framework for evaluating improvements to autonomous research systems
- Identifies which system components drive quality vs. efficiency
- Enables targeted optimization of weakest components

### Research Integrity
- Automated research paper screening for likely hallucinations
- Quality assurance pipeline for autonomous systems deployed in production
- Audit framework for AI-assisted research publications

### Scientific Reproducibility Infrastructure
- Standardized evaluation protocol for autonomous research systems
- Dataset of reformulated high-quality problems for benchmarking
- Evaluation harness and scoring rubrics for community use

### Funding and Resource Allocation
- Evidence-based guidance on optimal computation-quality tradeoffs
- Identification of efficient system architectures
- Cost-benefit analysis for autonomous research initiatives

### AI Safety and Governance
- Demonstration of gap between automated and rigorous evaluation
- Risk assessment framework for AI-generated scientific claims
- Guidelines for human oversight of autonomous research systems

## Insights & Implications

### Broader Field Impact

MLReplicate establishes rigorous benchmarking as essential for autonomous research systems. The finding that 59% of automated-accepted papers fail human review provides empirical evidence that automated evaluation alone is insufficient for scientific integrity. This has significant implications for AI governance and the role of automation in research.

### State-of-the-Art Advancement

The benchmark represents the first large-scale rigorous evaluation of autonomous research systems. It exposes systematic weaknesses (hallucination, fabrication) that simpler benchmarks would miss, establishing new standards for future system development.

### Limitations and Open Questions

1. **Domain Specificity:** How generalizable are findings across different research domains (e.g., NLP, vision, theory)?
2. **System Updates:** Do newer versions of autonomous systems (e.g., AI SCIENTIST-V3) show fundamental improvements?
3. **Human Bias:** Are expert reviewers themselves consistent in reproducibility assessment?
4. **Feedback Loops:** Can autonomous systems improve if given feedback from failed evaluations?
5. **Partial Credit:** How should systems be scored when they have good ideas but poor execution?

### Future Research Directions

- **Longitudinal Tracking:** Re-evaluate systems over time to measure improvement rates
- **Cross-Domain Evaluation:** Extend MLReplicate to other fields (physics, biology, chemistry)
- **Iterative Improvement:** Study whether autonomous systems can learn from feedback
- **Intervention Studies:** Test specific fixes (e.g., code verification, result validation)
- **Hybrid Systems:** Evaluate human-in-the-loop variants with different intervention points
- **Mechanistic Analysis:** Understand which architectural choices drive reproducibility

## Code & Resources

**Official Resources:**
- MLReplicate Benchmark: Complete dataset with reformulated problems
- Evaluation Framework: Automated review pipeline + expert evaluation protocol
- Generated Papers: 45 complete manuscripts from autonomous systems
- Code Repositories: Implementation code from each system (with permission)
- Paper and Supplementary Materials: https://arxiv.org/abs/2605.16616

**Dependencies:**
- Large language models (for autonomous systems)
- Research datasets (as specified in benchmark)
- Code execution environment
- Expert annotation infrastructure

**Reproduce Evaluation:**
- Run autonomous systems on benchmark problems (significant computational cost)
- Alternative: Use provided 45 generated papers for analysis
- Expert evaluation requires domain expertise; community evaluation framework provided

## Related Work & Context

### Autonomous Research Systems
- AI SCIENTIST framework and variants
- Agent Laboratory and similar agentic research systems
- Language model-based experiment design systems

### Benchmarking and Evaluation
- Prior work on LLM benchmarking (HELM, etc.)
- Code generation benchmarks (HumanEval, MBPP, etc.)
- Scientific understanding benchmarks (SciEval, etc.)

### Reproducibility Research
- Computational reproducibility in machine learning
- Research methodology and validation practices
- Meta-science studies on research quality

### AI Governance and Safety
- Evaluation frameworks for AI systems
- Trustworthiness assessment of AI-generated content
- Standards for AI-assisted research

### Critical Distinctions from Prior Work

**vs. Code Generation Benchmarks:** MLReplicate requires complete scientific pipelines (research design → implementation → execution → analysis → manuscript), not just correct code.

**vs. LLM Benchmarks:** Focuses on reproducibility and scientific integrity, not general language understanding.

**vs. Reproducibility Studies:** Systematically evaluates autonomous systems, not just human-conducted research.

### Potential for Impact

This work will likely influence:
- Development priorities for autonomous research systems
- Evaluation standards adopted by research institutions
- Policy frameworks for AI-assisted scientific publication
- Investment decisions in autonomous research technologies
