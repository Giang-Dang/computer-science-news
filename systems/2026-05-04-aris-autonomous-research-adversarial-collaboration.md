# ARIS: Autonomous Research via Adversarial Multi-Agent Collaboration

## Executive Summary

ARIS is an open-source research harness that enables autonomous machine learning research through cross-model adversarial collaboration, eliminating human bottlenecks in iterative research workflows. By orchestrating critique-to-action loops between different model families, ARIS achieves state-of-the-art research automation with built-in assurance mechanisms for verifying experimental claims, positioning it as a paradigm shift for scalable, reproducible ML research.

**ArXiv ID:** [2605.03042](https://arxiv.org/abs/2605.03042)  
**Submission Date:** May 4, 2026  
**Authors:** Wan Shui Yin, Alex Li, David Dao, and collaborators  

---

## Problem Statement

### Current Challenges
- **Research Bottleneck**: Traditional ML research relies on human researchers to iteratively refine code, manuscripts, and experimental designs through manual review cycles
- **Scalability Issues**: The human-in-the-loop approach does not scale to the volume and complexity of modern research tasks
- **Reproducibility Crisis**: Lack of standardized mechanisms for verifying that experimental claims are supported by evidence
- **Verification Gaps**: Existing systems fail to systematically check whether claims in manuscripts match experimental results

### Prior Limitations
- Previous automation attempts focused on single-model systems without adversarial feedback
- Lack of comprehensive assurance layers for research integrity
- Manual quality control remains the bottleneck in research workflows

### Research Gap
The field lacks an open-source, generalizable framework that combines autonomous agent orchestration with multi-stage verification mechanisms for end-to-end research automation.

---

## Core Concepts & Theory

### 1. Adversarial Multi-Agent Collaboration

The core innovation is a critique-to-action loop where:
- **Executor Agent**: Produces artifacts (code, manuscript sections, experiment designs) in response to prompts
- **Reviewer Agent**: From a different model family, assigns review scores under a predefined rubric and returns structured action items
- **Convergence Check**: Decides whether to run another round or accept the artifact as provisionally satisfactory

```
┌──────────────────────────────────────────────────────────────┐
│                  Critique-to-Action Loop                      │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Executor produces artifact (code/manuscript/design)       │
│         ↓                                                      │
│  2. Reviewer assigns score (1-10) and identifies issues       │
│         ↓                                                      │
│  3. Convergence check: score ≥ 6/10 & critical items done?   │
│         ↓                                                      │
│  4. If NO → Executor addresses items (go to step 1)           │
│     If YES → Accept artifact as provisionally satisfactory    │
│         ↓                                                      │
│  5. Move to next research task                                │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

### 2. Three-Stage Assurance Layer

**Stage 1: Integrity Verification**
- Checks that experimental code runs correctly and produces outputs
- Verifies that claims in text are well-formed and parseable
- Ensures logical consistency between related claims

**Stage 2: Result-to-Claim Mapping**
- Matches generated claims against raw experimental results
- Validates that statistics cited in text are computed from reported numbers
- Cross-checks any causal or comparative statements against evidence

**Stage 3: Claim Auditing**
- Systematically audits manuscript statements against the claim ledger
- Cross-references all claims against raw evidence and computed results
- Detects hallucinations or unsupported statements

### 3. Five-Pass Scientific Editing Pipeline
1. **Grammar and Clarity Pass**: Language quality and readability
2. **Technical Accuracy Pass**: Verification of mathematical notation and domain terminology
3. **Evidence Citation Pass**: Ensures all claims have supporting evidence
4. **Logical Consistency Pass**: Detects contradictions within the manuscript
5. **Formatting Pass**: Standardization and consistency checks

### 4. Mathematical Foundation

The default configuration uses a **threshold-based convergence criterion**:
- Termination when: `review_score ≥ 6/10 AND all_critical_items_resolved == True`
- Maximum rounds: 4 (default, configurable)
- Allows graceful degradation if convergence is unattainable

---

## Main Ideas & Contributions

### 1. Novel Critique-Based Orchestration
- **First-of-its-kind**: Cross-model adversarial collaboration as default configuration for research tasks
- **Dual-Model Strategy**: Executor and reviewer from different model families reduce systematic biases
- **Scalable Feedback Loop**: Enables rapid iteration without human intervention

### 2. Comprehensive Assurance Mechanisms
- **Three-Stage Verification**: Combines syntactic, semantic, and evidential checks
- **Claim Ledger System**: Maintains structured record of all research claims for post-hoc auditing
- **Mathematical Proof Checking**: Validates mathematical notation and logical structure
- **Visual Inspection**: Renders PDFs and checks for visual consistency

### 3. Practical Automation Architecture
- **End-to-End Workflow**: Handles code generation, manuscript writing, and experimental design simultaneously
- **Modular Design**: Each component (executor, reviewer, assurance) can be customized independently
- **Open-Source Implementation**: Lightweight markdown-based system without framework lock-in

### 4. Deployed Research Harness
- **Production Deployment**: Validated in real research workflows at multiple institutions
- **Artifact Quality**: Measurable improvements in manuscript quality and research integrity
- **Reproducibility**: All research artifacts (code, data, results) tracked and auditable

---

## Methodology & Implementation

### Datasets and Experimental Setup

**Research Tasks Evaluated:**
- Code generation for ML experiments (various architectures and datasets)
- Manuscript section writing (methodology, results, conclusions)
- Experimental design and hyperparameter optimization
- Literature review synthesis

**Experimental Infrastructure:**
- Multiple model families: Claude Opus, GPT-4, Llama variants
- Time complexity: measured iterations to convergence per task
- Quality metrics: human expert evaluation of artifacts
- Reproducibility verification: independent replication attempts

### Evaluation Metrics and Benchmarks

| Metric | Description | Target |
|--------|-------------|--------|
| **Convergence Rate** | % of tasks reaching acceptance threshold | >85% |
| **Iterations to Convergence** | Average review cycles needed | <3.5 |
| **Claim Verification Accuracy** | % of claims verified against evidence | >95% |
| **False Positive Rate** | Unwarranted rejection of correct claims | <5% |
| **Code Execution Success** | % of generated code running error-free | >90% |
| **Human Expert Agreement** | Expert rating correlation with system score | ρ > 0.78 |

### Key Results

**Quantitative Findings:**
- Achieved 87.3% convergence rate on diverse research tasks
- Reduced average iterations to convergence from ~5.2 (human) to ~2.8 (ARIS)
- Claim verification accuracy: 96.2% with <3% false positive rate
- Code generation success rate: 92% for standard ML tasks
- Manuscript quality improvement: 34% reduction in factual errors vs. baseline

**Qualitative Observations:**
- Reviewers from different model families identify complementary issues
- Assurance layer catches subtle claim-evidence mismatches (>80% accuracy)
- Artifact diversity increases with cross-model collaboration
- System gracefully handles incomplete or ambiguous specifications

### Statistical Analysis

**Significance Testing:**
- Paired t-tests comparing ARIS vs. single-model baselines: p < 0.001
- Effect sizes (Cohen's d): 1.2-1.8 across metrics
- Convergence rate difference: 15-20 percentage points vs. baselines

---

## Practical Applications & Use Cases

### 1. Research Institutions
- **Automated Paper Generation**: Speed up research publication pipelines
- **Literature Review Synthesis**: Automatically compile state-of-the-art summaries
- **Experimental Automation**: Design and execute ML experiments end-to-end
- **Reproducibility Verification**: Ensure experimental claims are supported by evidence

### 2. AI/ML Companies
- **Model Development**: Accelerate R&D cycles for new architectures
- **Benchmarking Pipelines**: Automated comparison of models across datasets
- **Documentation Generation**: Create comprehensive technical documentation
- **Quality Assurance**: Verify model behavior against design specifications

### 3. Educational Settings
- **Student Project Guidance**: Automated feedback on research methodology
- **Lab Report Generation**: Assist students in writing scientifically rigorous reports
- **Research Mentoring**: Provide consistent, scalable feedback on student research

### 4. Open Science Initiatives
- **Preprint Validation**: Screen ArXiv submissions for common issues
- **Peer Review Assistance**: Automate routine review checks
- **Data Analysis Pipelines**: Generate reproducible analysis workflows

### Implementation Challenges

**Technical Challenges:**
- Balancing reviewer strictness to avoid over-rejection
- Handling domain-specific research requiring specialized knowledge
- Managing context window limitations for large experiments
- Ensuring consistency across multiple review cycles

**Practical Challenges:**
- Integration with existing research workflows
- Building trust in automated systems for critical research
- Customizing for domain-specific research standards
- Training researchers to work effectively with automated feedback

---

## Insights & Implications

### Broader Field Impact

**Paradigm Shift in Research Automation:**
- Demonstrates that cross-model collaboration outperforms single-model approaches
- Validates that systematic verification can detect subtle research errors
- Shows that research can scale beyond human bottlenecks

### State-of-the-Art Advancement

- **First Fully-Automated Research Harness**: End-to-end automation from experiment design to manuscript publication
- **Distributed Review Model**: Multiple model families working in tandem improve quality
- **Assurance-First Design**: Puts verification mechanisms at the center of automation

### Limitations and Open Questions

**Known Limitations:**
- Requires clear task specifications; works best with well-defined research objectives
- Struggles with novel research directions requiring creative leaps
- Dependent on quality of review rubrics and evaluation criteria
- May miss domain-specific edge cases

**Open Research Questions:**
1. Can this approach scale to full research programs spanning multiple papers?
2. How do we balance automation with maintaining human oversight and judgment?
3. What safeguards are needed to prevent AI-generated research from introducing systematic biases?
4. How can we extend this to research requiring extensive human experimentation?
5. Can cross-model collaboration be made more efficient with fewer review cycles?

---

## Code & Resources

### Official Repository and Resources

- **GitHub Repository**: [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)
- **ArXiv Paper**: [https://arxiv.org/abs/2605.03042](https://arxiv.org/abs/2605.03042)
- **HTML Version**: [https://arxiv.org/html/2605.03042](https://arxiv.org/html/2605.03042)
- **Hugging Face Paper Page**: [2605.03042](https://huggingface.co/papers/2605.03042)

### Dependencies and Compute Requirements

**Software Dependencies:**
- Python 3.9+
- Multiple LLM APIs (Claude, GPT-4, or Llama)
- PDF rendering libraries (for visual inspection)
- Markdown parsing and manipulation libraries
- Standard ML libraries (NumPy, Pandas, scikit-learn)

**Computational Requirements:**
- **Model Access**: Requires API access to at least 2 different model families
- **Processing Time**: Average research task takes 5-30 minutes depending on complexity
- **Storage**: ~100MB per research project for artifacts and logs
- **Network**: Internet connection for API calls to language model services

### Quick-Start Guide

```bash
# 1. Clone the repository
git clone https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep.git
cd Auto-claude-code-research-in-sleep

# 2. Set up environment
pip install -r requirements.txt
export CLAUDE_API_KEY="your-api-key"
export OPENAI_API_KEY="your-openai-key"

# 3. Configure your research task in a specification file
cat > research_spec.md << 'EOF'
## Research Task: Analyze Performance of Transformer Variants
- Implement 3 transformer variants
- Run on standard benchmarks
- Generate manuscript comparing results
- Verify claims against experimental data
EOF

# 4. Run ARIS
python aris.py --spec research_spec.md --max-rounds 4 --threshold 6.0

# 5. Review generated artifacts
ls output/
cat output/manuscript.md
cat output/results_summary.json
```

---

## Related Work & Context

### Related Recent Papers

1. **Agent Collaboration Frameworks**
   - [MultiAgent Collaboration Attack](https://arxiv.org/html/2406.14711) - Investigating adversarial attacks in multi-agent collaborations
   - [Redefining AI Red Teaming in the Agentic Era](https://arxiv.org/html/2605.04019v1) - From weeks to hours

2. **Research Automation**
   - AutoML and AutoAI systems
   - Code generation for scientific computing
   - Automated machine learning workflows

3. **Verification and Assurance**
   - Program synthesis and verification
   - Claim verification in NLP
   - Scientific evidence assessment

### Prior Work Foundations

- **Code Generation**: Built on transformer-based code generation (Codex, GitHub Copilot)
- **Verification Methods**: Extends program synthesis verification techniques
- **Multi-Agent Systems**: Combines debate frameworks with structured critique
- **Scientific Writing**: Builds on NLP-based scientific text generation

### Possible Future Research Directions

1. **Enhanced Cross-Model Collaboration**: Mixing more than 2 model families; weighted ensemble approaches
2. **Domain-Specific Expertise**: Incorporating specialized domain validators
3. **Interactive Refinement**: Human-in-the-loop for creative research directions
4. **Longitudinal Studies**: Multi-paper research programs with knowledge retention
5. **Failure Analysis**: Understanding systematic gaps in automated research
6. **Ethical Frameworks**: Guidelines for responsible automated research
7. **Real-Time Collaboration**: Live integration with human researchers

---

## Conclusion

ARIS represents a significant step toward fully autonomous research workflows by combining sophisticated multi-agent orchestration with comprehensive verification mechanisms. The system's ability to autonomously generate, review, and verify research artifacts opens new possibilities for scaling ML research beyond human bottlenecks. As the field continues to advance, ARIS provides a foundation for exploring the promises and challenges of AI-driven research automation.

**Key Takeaway**: The future of research may not be "AI replacing researchers," but rather "AI augmenting researchers at scale" through systematic, verifiable automation.
