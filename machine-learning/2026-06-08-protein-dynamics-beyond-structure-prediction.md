# Protein Dynamics Beyond Structure Prediction

**ArXiv ID:** 2606.08647  
**Submitted:** June 2026  
**Authors:** Juliette Griffié, Philipp Berens, Sander Dieleman, Demis Hassabis, and 39+ collaborators

## Executive Summary

This paper marks a paradigm shift in computational biology by establishing a research roadmap to move beyond static protein structure prediction toward understanding dynamic protein folding kinetics, conformational dynamics, and macromolecular self-assembly. While AlphaFold has revolutionized three-dimensional structure prediction from sequences, the quantitative understanding of how proteins explore their conformational space, transition between states, and assemble into functional complexes remains largely unexplored. The work bridges machine learning, molecular dynamics, and experimental biophysics to enable predictive science of protein dynamics.

## Problem Statement

### Prior Limitations

Traditional structure prediction models like AlphaFold and RoseTTAFold predict static three-dimensional conformations—a single "end state" structure. This approach has achieved landmark success but fundamentally misses critical biological phenomena:

- **Folding pathways:** How sequences fold in time, including intermediates and misfolding routes
- **Conformational ensembles:** The distribution of conformations proteins sample in living cells
- **Kinetic properties:** Timescales of folding, unfolding, and state transitions
- **Macromolecular assembly:** How multiple protein chains and RNA molecules coordinate to form functional complexes
- **Proteostasis dynamics:** Real-time responses to cellular stress and chaperone machinery

### Research Gap

Proteins exist as dynamic, stochastic systems shaped by:
- Amino acid sequence and physical forces
- Co-translational folding constraints
- Molecular chaperone assistance
- Cellular thermodynamic conditions
- Temporal integration during synthesis

Predicting static structures captures only a snapshot; understanding protein function requires mechanistic models of dynamic behavior.

## Core Concepts & Theory

### Protein Folding as a Dynamic Process

**Folding Funnel Hypothesis:** Proteins navigate a complex energy landscape (the "folding funnel") during folding. The energy landscape is characterized by:
- A global minimum (native state) at the bottom
- Multiple local minima (misfolded or intermediate states)
- Rugged topology with barriers to overcome
- Stochastic transitions between states

**Timescales of Interest:**
- Femtoseconds: Bond vibrations
- Picoseconds to nanoseconds: Local structural fluctuations
- Microseconds to milliseconds: Domain motions and secondary structure formation
- Seconds to minutes: Complete folding trajectories
- Hours to days: Proteostasis maintenance and degradation

### Key Experimental Techniques

**Single-Molecule Methods:**
- Optical tweezers and atomic force microscopy for tracking individual protein folding
- Single-molecule fluorescence for monitoring state transitions
- Time-resolved cryo-electron microscopy for capturing intermediates

**Bulk Biophysical Measurements:**
- Nuclear magnetic resonance (NMR) spectroscopy for conformational ensembles
- Hydrogen-deuterium exchange mass spectrometry (HDX-MS) for dynamics
- Surface plasmon resonance for kinetic rate constants

**Computational Approaches:**
- Molecular dynamics simulations for sampling conformational space
- Markov state models for kinetic predictions
- Graph neural networks for learning force fields

### Comparison with Structure-Only Prediction

| Aspect | Structure Prediction (AlphaFold) | Dynamics Prediction (This Work) |
|--------|----------------------------------|----------------------------------|
| Output | Single native structure | Conformational ensemble, kinetics |
| Input | Sequence only | Sequence + dynamics data |
| Complexity | Single forward pass | Multi-step trajectory |
| Biological relevance | Necessary but incomplete | Captures functional mechanism |
| Computational cost | ~Seconds per protein | Minutes to hours |

## Main Ideas & Contributions

### 1. Integrating Multiple Data Modalities

The paper advocates for unified frameworks combining:
- **Structural data:** PDB structures, cryo-EM ensembles
- **Kinetic data:** Folding rates, state transition times from single-molecule experiments
- **Ensemble data:** NMR chemical shifts, HDX protection patterns
- **Functional data:** Activity assays, conformational selection models

### 2. Machine Learning for Dynamics Prediction

Novel architectures needed:
- **Trajectory models:** RNNs/Transformers trained on molecular dynamics simulations to predict next-frame positions
- **Energy functions:** Learning differentiable potential energy surfaces from experimental data
- **Kinetic models:** Graph neural networks predicting transition rates between conformational states

### 3. Co-Translation and Synthesis Constraints

Proteins fold *during* translation, not after. This introduces:
- Temporal ordering (N-terminus emerges first)
- Ribosome-mediated kinetic trapping
- Chaperone co-translation assistance
- Reduced conformational space compared to post-translational folding

### 4. Macromolecular Assembly Mechanisms

Beyond single proteins, understanding:
- Protein-protein interaction specificity and kinetics
- RNA-protein complex formation
- Multi-subunit complex assembly order
- Phase separation and biomolecular condensate formation

## Methodology & Implementation

### Data Integration Pipeline

```
Experimental Measurements
├── Structures (PDB, AlphaFold predictions)
├── Single-molecule trajectories
├── NMR chemical shifts & relaxation rates
├── Cryo-EM ensemble data
└── Kinetic constants (kfold, kunfold)
         ↓
    Feature Engineering
├── Sequence representations (ESM embeddings)
├── Graph neural network encoding
├── Temporal windowing for trajectories
└── Conformational descriptors
         ↓
    ML Model Training
├── Trajectory prediction (diffusion models)
├── Energy landscape learning
├── Kinetic rate prediction
└── Ensemble characterization
         ↓
    Validation
├── Prediction accuracy on held-out proteins
├── Comparison with new experiments
└── Biological interpretation
```

### Key Datasets

- **PDB Database:** ~150,000 protein structures with resolution heterogeneity
- **Simulation Databases:** OpenMM, GROMACS trajectories for learning force fields
- **Single-Molecule Studies:** Curated datasets from AFM, optical tweezers experiments (~500+ proteins)
- **NMR Databases:** BMRB with chemical shift and relaxation data (~11,000 assignments)

### Evaluation Metrics

[Exact figures unavailable — see full paper]

Expected metrics include:
- **Kinetic prediction:** RMSE on predicted folding rates vs. experimental values
- **Ensemble quality:** KL-divergence between predicted and NMR-derived chemical shift distributions
- **Trajectory sampling:** Comparison of predicted contact maps vs. single-molecule force-extension curves
- **Functional prediction:** Correlation between predicted conformational flexibility and experimental activity data

## Practical Applications & Use Cases

### 1. Protein Engineering

**Rational Design of Faster Folding:**
- Identify and eliminate kinetic traps through dynamics prediction
- Design mutations that stabilize functional intermediates
- Accelerate therapeutic protein production (antibodies, enzymes)

**Example:** Engineering antibodies with improved stability without sacrificing binding affinity by optimizing conformational kinetics.

### 2. Misfolding Disease Understanding

**Neurodegenerative Diseases:**
- Predict why Alzheimer's (Aβ, tau) and Parkinson's (α-synuclein) proteins misfold
- Design small molecules to stabilize native conformations
- Understand amyloid nucleation kinetics

**Example:** Rationally design compounds to slow α-synuclein aggregation in Parkinson's disease.

### 3. Therapeutic Intervention

**Proteostasis Engineering:**
- Predict which proteins accumulate under cellular stress
- Design interventions through chaperones or degradation pathways
- Personalized medicine based on individual protein variant dynamics

**Example:** Cancer cells often upregulate heat-shock proteins; predicting their dynamics enables targeted inhibition.

### 4. Synthetic Biology

**De Novo Protein Design:**
- Design proteins with specified dynamical properties (flexible linkers, rigid cores)
- Predict allosteric mechanisms before synthesis
- Optimize enzyme catalytic efficiency through conformational selection

### 5. RNA-Protein Complex Dynamics

**CRISPR Systems:**
- Predict Cas9 conformational changes during RNA targeting
- Optimize guide RNA binding kinetics
- Design improved CRISPR variants

## Insights & Implications

### Broader Field Impact

1. **Convergence of Disciplines:** Merges machine learning, structural biology, biophysics, and molecular dynamics into unified framework

2. **Accessibility of Dynamics:** Makes protein dynamics as accessible and routine as structure prediction, democratizing this knowledge

3. **Mechanistic Understanding:** Moves from "what do proteins look like?" to "why do proteins work this way?"—deeper biological insight

4. **Predictive Biology:** Enables rational interventions in proteostasis-related disorders affecting billions globally

### Fundamental Advances

- **Physics-Informed ML:** Encoding biophysical constraints (energy conservation, dynamics laws) into neural networks
- **Uncertainty Quantification:** Understanding which dynamics are predictable vs. stochastic
- **Temporal Extrapolation:** Predicting long-timescale phenomena from shorter simulations

### Limitations & Open Questions

1. **Computational Complexity:** Simulating protein dynamics at atomic resolution remains expensive; current models must make approximations

2. **Sparse Experimental Data:** Kinetic data is less abundant than structures; transfer learning across protein families needed

3. **Cellular Context:** Laboratory conditions differ from living cells; in-cell dynamics may show unexpected behavior

4. **Chaperone Interactions:** How to incorporate assistance from ~80 distinct human chaperone proteins remains unsolved

5. **Evolutionary Constraints:** Balancing optimization for function, kinetics, and evolutionary compatibility

## Code & Resources

### Official Repositories & Tools

- **AlphaFold:** https://github.com/deepmind/alphafold
- **OmegaFold:** Open-source variant for protein structure prediction
- **OpenMM:** GPU-accelerated molecular dynamics: https://openmm.org/
- **ESMFold:** Structure prediction from language model embeddings: https://github.com/facebookresearch/esmfold

### Computational Requirements

**Typical Setup:**
- GPU: NVIDIA A100 (40GB) or V100 (32GB) for MD simulations
- Storage: ~500 GB for curated training datasets
- Time: Days to weeks for training dynamics models on complete protein families

### Quick-Start Integration

Practitioners can use:
1. Pre-trained ESM-2 protein language models for sequence encoding
2. Existing MD force fields (AMBER, CHARMM) for trajectory generation
3. Graph neural networks (PyTorch Geometric) for kinetic prediction

## Related Work & Context

### Prior Foundational Work

**Structure Prediction:**
- AlphaFold2 (2020): Revolutionized protein structure prediction using attention mechanisms
- RoseTTAFold (2021): Integrating 1D, 2D, and 3D representations
- OmegaFold (2023): Open-source improvements and faster inference

**Dynamics Characterization:**
- Molecular dynamics simulations: Long-established but computationally expensive
- Single-molecule biophysics: Direct observation but low throughput
- Ensemble refinement: Combining structures with experimental constraints

### Emerging Complementary Approaches

- **Diffusion Models for Protein Generation:** Learning to generate valid protein sequences/structures
- **Reinforcement Learning for Design:** Optimizing proteins for multiple objectives simultaneously
- **Multi-Fidelity Learning:** Combining expensive atomistic and cheaper coarse-grained simulations

### Future Research Directions

1. **Real-Time Prediction:** Predict protein behavior during synthesis on the ribosome
2. **Cellular Simulation:** Integrate protein dynamics with cellular transport and compartmentalization
3. **Evolution Dynamics:** Understand how mutations alter folding pathways and disease susceptibility
4. **Multi-Scale Modeling:** Connect atomic-level protein dynamics to cellular phenotypes

## Conclusion

This paper outlines an ambitious but achievable vision: transforming protein dynamics from a specialized experimental domain into a predictable, engineering-accessible frontier. By leveraging machine learning, experimental advances, and computational power, the field can move beyond asking "what do proteins look like?" to answering "how do proteins fold, function, and evolve dynamically?"—unlocking unprecedented capacity to engineer biological systems and intervene in proteostasis diseases.
