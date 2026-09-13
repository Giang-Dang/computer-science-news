# An Embedded RISC-V Evaluation of Kolmogorov–Arnold Networks in Hard-Constrained Recurrent Physics-Informed Models

**Authors:** Enzo Nicolas Spotorno, Josafat Leal Filho  
**arXiv ID:** 2608.00737  
**Submission Date:** August 2026  
**Conference:** SBESC 2026  
**Categories:** Machine Learning, Artificial Intelligence, Performance

## Executive Summary

This paper investigates the deployment of Kolmogorov-Arnold Networks (KANs) in resource-constrained embedded systems, specifically RISC-V architectures. The study bridges the gap between modern deep learning research and practical edge computing deployment by evaluating KAN performance in hard-constrained environments while handling physics-informed modeling tasks with recurrent architectures.

## Problem Statement

Modern neural networks, particularly vision and deep learning models, face significant challenges when deployed to embedded systems with strict computational and memory constraints. While foundation models excel in data-rich scenarios, their deployment on edge devices (RISC-V based processors, microcontrollers, etc.) remains underexplored. Physics-informed neural networks (PINNs) add additional complexity through hard constraints that must be satisfied during training and inference.

The research gap exists in understanding how emerging architectures like Kolmogorov-Arnold Networks perform under these extreme resource constraints, and whether they offer advantages over traditional MLPs in embedded contexts.

## Core Concepts & Theory

### Kolmogorov-Arnold Networks (KANs)

KANs represent a recent advancement in neural network design based on the Kolmogorov-Arnold representation theorem. Unlike traditional multi-layer perceptrons (MLPs) that apply learnable transformations to fixed activation functions, KANs place learnable univariate functions on edges rather than nodes.

**Key differences from MLPs:**
- KANs use learnable activation functions instead of fixed non-linearities (ReLU, sigmoid, etc.)
- The representation is more mathematically grounded in approximation theory
- Potentially more efficient parameter usage for certain function classes

### RISC-V Architecture

RISC-V (Reduced Instruction Set Computer - Version 5) is an open-source instruction set architecture designed for embedded and IoT applications with minimal computational overhead.

### Physics-Informed Neural Networks (PINNs)

PINNs incorporate physical laws as hard constraints into the training objective, ensuring predictions remain physically consistent. In recurrent settings, these constraints must be maintained across temporal sequences.

## Main Ideas & Contributions

1. **First embedded evaluation of KANs**: Comprehensive evaluation of KAN performance on RISC-V processors under hard memory and computational budgets
2. **Recurrent KAN implementation**: Extension of KAN architecture to handle temporal/sequential dependencies in physics-informed settings
3. **Hard-constrained optimization**: Methodology for maintaining physics constraints in embedded KAN training
4. **Performance characterization**: Benchmark results comparing KANs to MLPs on embedded systems

## Methodology & Implementation

### Experimental Setup

- **Target platform:** RISC-V based embedded processors
- **Network architecture:** Recurrent KAN variants with hard physical constraints
- **Baseline comparisons:** Traditional MLPs with physics constraints
- **Dataset:** Physics-informed modeling tasks (specific domains covered in full paper)

### Evaluation Metrics

[Exact figures unavailable — see full paper]

The paper likely measures:
- Inference latency and throughput
- Memory footprint (model size, peak memory usage)
- Energy consumption
- Prediction accuracy vs. constraint satisfaction trade-offs
- Comparison against MLP baselines on same hardware

### Key Results

[Exact figures unavailable — see full paper]

The research demonstrates KAN viability in embedded environments while maintaining hard physical constraints through careful implementation and optimization strategies.

## Practical Applications & Use Cases

1. **Edge AI for Scientific Computing:** Deploying physics-informed models to remote sensors and IoT devices for real-time environmental monitoring

2. **Robotics:** Robot control systems with embedded physics constraints running on RISC-V processors for real-time decision making

3. **Structural Health Monitoring:** Embedded systems that predict structural behavior while respecting engineering constraints

4. **Smart Sensors:** Agricultural, industrial, or environmental sensors with integrated physics-aware AI capabilities

5. **Autonomous Systems:** Edge deployment of neural models in vehicles and drones with real-time physics-informed constraints

## Insights & Implications

- **Efficiency gains:** KANs may offer parameter efficiency advantages in memory-constrained settings, potentially offsetting computational overhead
- **Constraint handling:** Demonstrates that hard physical constraints can be effectively integrated into modern architectures beyond traditional PINNs
- **RISC-V ecosystem:** Validates RISC-V viability for AI/ML workloads beyond traditional CPU tasks
- **Research implications:** Opens questions about which architectural choices matter most under extreme resource constraints

## Code & Resources

- **Submission venue:** SBESC 2026 (Brazilian Symposium on Embedded Systems)
- **Extension of:** ICLR Workshop Paper (indicates prior related work)
- **Implementation likely available:** Check authors' institutional repositories post-publication

## Related Work & Context

- **Prior KAN research:** KAN 2.0, KANICE, Kolmogorov-Arnold PointNet and other KAN variants
- **RISC-V ML:** Emerging work on deploying neural networks to open-source ISAs
- **Physics-informed ML:** DynoPT, NEURIPINN, and other PINN architectures
- **Embedded ML:** TinyML frameworks, quantization techniques, knowledge distillation

## Future Research Directions

- Extension to other emerging architectures on embedded systems
- Integration with neuromorphic hardware
- Online learning and adaptation on edge devices
- Energy-aware architecture design for embedded neural networks
