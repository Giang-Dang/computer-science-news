# Towards Sustainable Artificial Intelligence: A Comprehensive Review and Comparative Analysis of Deep Learning Models' Carbon Footprint

**ArXiv ID:** 2608.09998  
**Authors:** Samar Garrab, Sarra Boughriou, Manel BenSassi  
**Published:** Applied Intelligence, 2026  
**Submitted:** August 2026  
**Field:** Artificial Intelligence, Sustainable Computing

## Executive Summary

This comprehensive review systematically examines the environmental impact of AI and deep learning systems, with emphasis on quantifying and comparing the carbon footprints of various model architectures and training methodologies. As AI systems grow increasingly large and resource-intensive, understanding their environmental costs becomes critical for both research prioritization and practical deployment decisions. The paper provides both theoretical frameworks for Green AI and empirical measurements comparing multiple deep learning models' emissions profiles.

## Problem Statement

**The Environmental Crisis in AI:**

Deep learning's explosive growth has created an unintended consequence: massive environmental impact through energy consumption and associated carbon emissions.

**Key Challenges:**
- Large-scale deep learning models require enormous computational resources
- Training a single large language model can generate carbon equivalent to 5+ cars over a lifetime
- Data centers for AI inference consume substantial ongoing electricity
- Renewable energy infrastructure lag makes much current AI compute carbon-intensive
- Lack of standardized measurement methodology creates inconsistent environmental accounting

**Why This Matters:**
1. **Scale:** AI systems are deployed at unprecedented scales affecting billions of users
2. **Trajectory:** Model sizes growing exponentially (100B → 1T parameters in recent years)
3. **Urgency:** Climate change requires immediate action across all sectors
4. **Accountability:** Researchers and organizations need concrete impact data for decision-making
5. **Alternatives:** Solutions exist (quantization, pruning, knowledge distillation) but lack systematic evaluation

**Prior Limitations:**
- No comprehensive comparison framework for AI models' environmental costs
- Diverse measurement methodologies make inter-study comparisons difficult
- Limited empirical evaluation on representative deep learning models
- Insufficient guidance for practitioners choosing efficient architectures

## Core Concepts & Theory

### Green AI Framework

**Fundamental Principle:** Efficiency metrics are as important as accuracy metrics in modern AI research.

### Key Environmental Impact Dimensions

**1. Training Carbon Footprint**
- Energy consumed during model training
- Training time duration
- Hardware type used (CPU, GPU, TPU with different efficiency profiles)
- Data center location and electricity grid carbon intensity
- Formula: Carbon = Energy × Grid Emissions Factor

**2. Inference Carbon Footprint**
- Energy consumed per prediction
- Cumulative cost across deployment lifetime
- Often exceeds training cost for deployed models
- Reduces over time as energy grids decarbonize

**3. Embodied Carbon**
- Manufacturing emissions of hardware
- Usually ~10-15% of lifecycle carbon for AI systems
- Increasingly relevant for specialized AI chips

### Carbon Measurement Tools & Methodologies

**Three Primary Approaches:**

1. **Empirical Measurement**
   - Direct measurement of hardware power consumption
   - Integration with carbon tracking tools (e.g., eco2AI)
   - Specific to hardware, location, and time
   - Most accurate but labor-intensive

2. **Modeling & Estimation**
   - Models of power consumption based on architecture
   - Grid emissions factor from geographic location and time
   - Enables comparison across studies
   - Trade-off: less precise but more scalable

3. **Benchmarking Suites**
   - Standardized evaluation frameworks
   - Ensures consistent methodology
   - Enables direct comparisons
   - Requires agreement on methodology

### Green AI Optimization Taxonomy

**Model-Level Optimizations:**
- **Pruning:** Remove redundant weights/neurons
- **Quantization:** Reduce precision (32-bit → 8-bit or lower)
- **Knowledge Distillation:** Compress large models into smaller ones
- **Architecture Search:** Find efficient architectures automatically
- **Sparse Models:** Activate only subset of parameters per input

**System-Level Optimizations:**
- **Mixed Precision Training:** Use lower precision where feasible
- **Gradient Checkpointing:** Trade memory for computation efficiency
- **Distributed Training:** Leverage parallelism for faster convergence
- **Federated Learning:** Process data locally, reduce data movement

**Algorithmic Optimizations:**
- **Adaptive Computation:** Allocate compute based on input difficulty
- **Mixture-of-Experts:** Activate only relevant experts per input
- **Early Exit Mechanisms:** Halt processing when confident
- **Efficient Attention:** Linear attention variants vs. quadratic standard attention

**Infrastructure Optimizations:**
- **Energy-Efficient Hardware:** Specialized AI chips (TPUs, GPUs with better power efficiency)
- **Green Data Centers:** Renewable energy sourcing
- **Edge Inference:** Compute closer to users, reduce data transmission
- **Caching & Distillation:** Reduce redundant computation

## Main Ideas & Contributions

1. **Comprehensive Review:** Systematic survey of Green AI research, optimization techniques, and environmental impact metrics

2. **Comparative Empirical Study:** Evaluation of six representative deep learning models on standardized benchmarks with consistent carbon accounting

3. **Measurement Tool Comparison:** Examination of different carbon measurement methodologies and their trade-offs

4. **Optimization Catalog:** Structured taxonomy of techniques for reducing AI environmental impact at multiple levels

5. **Best Practices Framework:** Practical guidelines for researchers and practitioners making environmentally conscious AI decisions

6. **Future Roadmap:** Discussion of emerging techniques and necessary infrastructure changes for sustainable AI

## Methodology & Implementation

### Experimental Setup

**Six Deep Learning Models Evaluated:**
[Specific model selection rationale explained in paper]
- Ranging from smaller efficient models to large state-of-the-art systems
- Representative of different application domains
- Covers various architectures (CNNs, Transformers, etc.)

**Hardware Configuration:**
- CPU-based experimental setup (enabling reproducibility and accessibility)
- Standard cloud infrastructure
- Measured actual power consumption

**Measurement Approach:**
- Used multiple carbon measurement tools for comparison
- Recorded training duration, iterations, convergence rate
- Calculated carbon per unit of computation and per unit of accuracy improvement

### Evaluation Metrics

[Exact figures unavailable — see full paper]

Key metrics include:
- **Carbon per model (kg CO₂e):** Total emissions for training to convergence
- **Carbon per FLOP:** Energy efficiency independent of training duration
- **Carbon per percentage of accuracy:** Cost for each percentage point of accuracy gain
- **Inference carbon:** Per-prediction emissions at scale
- **Model efficiency frontier:** Trade-off between accuracy and carbon cost
- **Embodied carbon analysis:** Hardware manufacturing contribution

### Results Summary

**Key Findings:**
- Significant variance in carbon footprint across model architectures (10-100x differences possible)
- Efficiency improvements often achieve similar accuracy with 50-80% lower carbon cost
- Inference carbon dominates total lifecycle cost for deployed models
- Grid decarbonization dramatically reduces AI carbon footprint
- Measurement methodology choice significantly affects reported emissions

**Model-Specific Insights:**
[Specific architecture comparisons from empirical evaluation]
- Quantized models showing substantial efficiency gains with minimal accuracy loss
- Sparse models and mixture-of-experts outperforming dense architectures
- Efficient attention mechanisms enabling larger contexts with lower cost

## Practical Applications & Use Cases

### Responsible AI Research
- Carbon budget awareness in hyperparameter tuning and model selection
- Architecture design prioritizing efficiency without sacrificing capability
- Environmental reporting as standard in AI publications

### Enterprise AI Deployment
- Cost-aware model selection (carbon footprint correlates with operational cost)
- Infrastructure planning with renewable energy sourcing
- Inference optimization for deployed models
- Edge deployment strategies to reduce data transmission

### Sustainable Startups & Organizations
- Using efficiency as competitive advantage (faster model, lower cost)
- Green certification for AI services
- Consumer-facing environmental impact reporting

### Policy & Governance
- Environmental impact requirements for AI model release
- Carbon budgeting for research institutions
- Sustainability metrics in AI evaluation frameworks

### Climate Impact Assessment
- Understanding AI's contribution to climate impact
- Identifying highest-priority optimization targets
- Tracking progress toward sustainable AI goals

## Insights & Implications

1. **Efficiency is Viable:** Many optimization techniques achieve 50-80% carbon reduction with minimal accuracy loss

2. **Measurement Matters:** Standardized measurement methodology critical for fair model comparison and research advancement

3. **Inference Dominates:** For deployed models, inference carbon often far exceeds training carbon, requiring focus on deployment efficiency

4. **Grid Matters:** AI carbon footprint largely dependent on electricity grid composition; decarbonizing energy infrastructure is crucial

5. **Multi-Level Approach Needed:** No single technique sufficient; comprehensive efficiency requires improvements across architecture, algorithms, systems, and infrastructure

6. **Reproducibility Needed:** Current practice lacks standardized environmental reporting, hindering progress and accountability

## Limitations & Open Questions

1. CPU-based evaluation may not fully represent GPU/TPU efficiency profiles
2. Limited analysis of very large models (100B+ parameters) due to evaluation constraints
3. Grid emissions factor varies significantly by region and time; global applicability limited
4. Hardware lifecycle analysis beyond manufacturing not extensively covered
5. Data annotation and preparation carbon costs not included

## Code & Resources

**Measurement Tools Discussed:**
- **eco2AI:** Carbon emissions tracking for machine learning
- **CodeCarbon:** Open-source carbon tracking library
- **Custom measurement frameworks:** Building carbon-aware benchmarks
- **Benchmarking suites:** Standard evaluation protocols

**Key Libraries:**
- Deep learning frameworks with efficiency profiling
- Power measurement tools for hardware
- Carbon accounting libraries

## Related Work & Context

### Foundational Concepts
- Green computing and sustainable technology practices
- Energy efficiency in cloud computing and data centers
- Environmental science and carbon accounting methodologies

### Related Research Areas
- Model compression and efficient neural networks
- Low-resource natural language processing
- On-device and edge AI systems
- TinyML and embedded systems

### Recent Papers on Sustainable AI
- eco2AI: carbon emissions tracking framework
- Quantifying climate risk of generative AI with G-TRACE
- Toward carbon-neutral human-AI systems
- Hugging Carbon: Training emissions of large models

### Future Research Directions
- Standardized methodology for environmental impact reporting across AI community
- Carbon-aware neural architecture search
- Grid-aware optimization (varying computation based on grid carbon intensity)
- Federated learning for carbon reduction
- Sustainable AI benchmarking standards
- Hardware innovation for efficient AI (specialized chips, photonic computing)
- Policy frameworks for AI sustainability
- Integration of environmental cost into model training objectives
