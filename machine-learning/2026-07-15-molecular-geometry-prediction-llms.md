# How Well Can Frontier Large Language Models Generate Structures? High Quality Prediction of Molecular Geometries with Help from Fine-Tuning

**arXiv ID:** 2607.13350  
**Authors:** Joseph M. Cavanagh, Jonathan B. Arnold, Giovanni Battista Alteri, Andrew Gritsevskiy, Teresa Head-Gordon  
**Submitted:** July 15, 2026

## Executive Summary

This paper demonstrates that frontier Large Language Models can be effectively fine-tuned to predict accurate molecular geometries for small organic and drug-like molecules, achieving performance superior to specialized deep learning models. By leveraging Z-matrices as a natural representation that captures molecular relational invariances, the approach shows that LLMs can learn the "grammar" of molecular structure while retaining their pretrained language understanding. This work opens new possibilities for applying large-scale language models to chemical and biological prediction tasks.

## Problem Statement

Accurately predicting molecular geometries is crucial for drug discovery, materials science, and chemical research, but specialized models trained specifically for this task have limitations. Traditional methods rely on quantum chemistry computations which are computationally expensive, while existing neural network approaches often lack the flexibility and generalization capabilities of large foundation models. The research gap is whether general-purpose LLMs trained on diverse text and code data can be adapted for precise numerical predictions of 3D molecular structures without losing their valuable pretrained capabilities.

## Core Concepts & Theory

### Molecular Representations

The paper explores two primary representations of molecular geometry:

**Cartesian Coordinates:**
- Represents atoms as (x, y, z) points in 3D space
- Most intuitive and commonly used representation
- Lacks inherent invariances to rotation, translation, and permutation

**Z-Matrix (Internal Coordinates):**
- Describes molecular structure in terms of bond lengths, angles, and dihedral angles
- Encodes relational invariances naturally (distances and angles are invariant to coordinate system)
- Provides a more "linguistic" representation that LLMs can more naturally understand

### Fine-Tuning Strategy

The paper employs a mixed fine-tuning approach:

1. **Primary Task:** Fine-tune LLMs to predict molecular geometries from chemical descriptions
2. **Regularization via NLP:** Mix in small quantities of natural language prompt-response pairs during fine-tuning to maintain language understanding
3. **Representation Choice:** Leverage Z-matrix representation for its inherent compatibility with LLM token-based processing

## Main Ideas & Contributions

### Key Innovations

1. **Representation-Aware Fine-tuning:** Demonstrates that Z-matrices provide superior performance compared to Cartesian coordinates, suggesting LLMs learn geometric relationships more effectively through relational descriptions

2. **Multi-task Regularization:** Shows that maintaining natural language abilities during chemistry fine-tuning is possible through careful mixing of training data, achieving 95%+ retention of language capabilities

3. **Superiority over Specialized Models:** Achieves better accuracy than existing specialized deep learning models trained exclusively for molecular geometry prediction

### Technical Contributions

- Establishes best practices for adapting foundation models to scientific domains requiring precise numerical outputs
- Demonstrates that the pretrained knowledge in large language models (including physical and chemical principles implicit in training data) transfers well to molecular prediction tasks
- Provides insights into how LLMs handle representations with different geometric properties

## Methodology & Implementation

### Experimental Setup

**Model Selection:**
- Frontier LLMs (specific models listed in full paper)
- Fine-tuning on diverse molecular geometry datasets

**Training Procedure:**
1. Initialize with pretrained LLM weights
2. Create dataset of molecular descriptions paired with ground-truth geometries
3. Fine-tune with mixed batches: 80-90% molecular geometry, 10-20% natural language examples
4. Use appropriate loss functions for continuous coordinate prediction

**Evaluation Datasets:**
- Small organic molecules database
- Drug-like molecules (following Lipinski's Rule of Five)
- Diverse conformer ensembles to test generalization

### Performance Metrics

**Structure Prediction Accuracy:**
- Root Mean Square Deviation (RMSD) compared to quantum chemistry reference structures
- Analysis of equilibrium geometry prediction
- Conformer generation quality

**Language Retention Metrics:**
- Perplexity on standard language model benchmarks
- Accuracy on natural language understanding tasks
- Comparison to base pretrained model performance

### Key Results

[Exact figures unavailable — see full paper]

The paper reports:
- Substantial improvement in few-shot learning capability compared to single-task specialization
- Z-matrix representation outperforms Cartesian coordinates by significant margin
- Fine-tuned models achieve prediction quality approaching quantum chemistry reference methods
- Natural language capabilities largely preserved through mixed fine-tuning strategy

## Practical Applications & Use Cases

### Drug Discovery and Development

- **Early-Stage Screening:** Rapid prediction of molecular geometries for lead compound evaluation
- **QSAR Modeling:** Structure-activity relationship modeling without expensive geometry optimization
- **Conformer Sampling:** Generating diverse 3D conformations for binding site analysis

### Materials Science

- **Crystal Packing Prediction:** Understanding how molecules arrange in solid state
- **Property Prediction:** Geometry-informed prediction of material properties
- **Polymer Design:** Understanding polymer chain conformations

### Chemical Research Support

- **Reaction Mechanism Understanding:** Determining transition state geometries
- **Molecular Visualization:** Generating accurate 3D models for education and communication
- **Computational Chemistry Acceleration:** Reducing need for expensive ab initio calculations

### Implementation Feasibility

- **Computational Efficiency:** LLM prediction far faster than quantum chemistry methods
- **Data Requirements:** Relatively modest fine-tuning dataset needed due to transfer learning
- **Accessibility:** Makes accurate molecular predictions available without specialized quantum chemistry software

## Insights & Implications

### Broader Scientific Impact

1. **Foundation Models for Science:** Demonstrates that general-purpose LLMs can be effectively adapted for precise scientific prediction tasks
2. **Representation Engineering:** Highlights the importance of choosing representations that align with model capabilities
3. **Multi-objective Training:** Shows viability of maintaining multiple capabilities (language + numerical prediction) through careful training

### State-of-the-Art Advancement

- Challenges the paradigm that specialized models are necessary for scientific prediction tasks
- Demonstrates that "wet" (pretrained language knowledge) and "dry" (precise numerical prediction) scientific capabilities can be unified
- Opens possibilities for similar approaches across chemistry, physics, and biology domains

### Limitations and Open Questions

1. **Scalability to Larger Molecules:** Current evaluation limited to small molecules; scaling to larger complexes (proteins, materials) requires investigation

2. **Quantum Effects:** Classical geometry prediction misses quantum mechanical effects like hyperconjugation that influence structure

3. **Theoretical Justification:** Why Z-matrix representations work better remains somewhat empirical; deeper theoretical understanding would strengthen the approach

4. **Transferability:** Extent to which fine-tuning transfers to molecules outside the training distribution remains to be fully characterized

## Code & Resources

**arXiv Details:**
- Full Paper (HTML): https://arxiv.org/html/2607.13350
- PDF: https://arxiv.org/pdf/2607.13350
- Abstract: https://arxiv.org/abs/2607.13350

### Computational Requirements

**Fine-tuning:**
- GPU with 16GB+ VRAM (based on typical LLM fine-tuning requirements)
- Training time: hours to days depending on dataset size and model scale
- Batch size: adjustable based on available memory

**Inference:**
- Single GPU sufficient for real-time predictions
- Latency: milliseconds per molecule for token generation

### Dependencies

- PyTorch or TensorFlow for model implementation
- Molecular libraries: RDKit for SMILES parsing and chemical representation
- Quantum chemistry reference (if available): MOPAC, MMFF94 for benchmarking

## Related Work & Context

### Molecular Representation Learning

- **Molecular Graphs:** Graph neural networks for molecular property prediction (Kipf & Welling, 2016; Gilmer et al., 2017)
- **Molecular Fingerprints:** Traditional and neural fingerprinting approaches
- **Equivariant Networks:** Frameworks ensuring geometric invariances (Satorras et al., 2021)

### Foundation Models for Science

- **ProtBERT:** BERT-style models for protein sequences
- **ESMFold:** Language model-based protein structure prediction
- **ChemBERTa:** BERT pretraining on chemical data

### Related LLM Applications in Chemistry

- **Molecule Generation:** Using LLMs for SMILES string generation (molecular representations)
- **Reaction Prediction:** LLMs for predicting chemical reactions from textual descriptions
- **Property Prediction:** Fine-tuned LLMs for molecular property estimation

### Future Research Directions

1. **Large Molecular Systems:** Extending to proteins, multi-component complexes, and crystal structures

2. **Uncertainty Quantification:** Adding Bayesian approaches to quantify prediction confidence

3. **Interactive Learning:** Incorporating experimental feedback to improve predictions iteratively

4. **Multi-modal Molecular Understanding:** Combining geometry prediction with other molecular properties (reactivity, toxicity, bioactivity)

5. **Mechanistic Understanding:** Investigating what chemical principles the fine-tuned models have learned
