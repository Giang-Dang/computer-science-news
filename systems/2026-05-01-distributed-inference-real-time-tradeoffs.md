# Cloud Is Closer Than It Appears: Revisiting the Tradeoffs of Distributed Real-Time Inference

## Executive Summary

This paper challenges the conventional wisdom that cloud-based inference is unsuitable for latency-sensitive cyber-physical systems. Through formal analytical modeling and realistic simulations of autonomous driving, the authors demonstrate that properly provisioned cloud platforms can match or exceed on-device inference performance while offering significant advantages in computational flexibility and energy efficiency. The work provides a quantitative framework for evaluating distributed inference architectures and empirically shows that cloud is often the preferred option for real-time perception-driven control.

## Problem Statement

Current distributed cyber-physical systems (CPS) architectures typically prioritize on-device inference to avoid network latency and contention-induced delays from remote cloud platforms. This design choice, however, places substantial computational burden on edge devices, limiting their energy budget and thermal dissipation capabilities. Moreover, modern deep neural networks for perception impose extreme computational demands—video processing, LiDAR interpretation, multi-sensor fusion—making local-only inference infeasible for many real-time applications.

The research gap: there is no principled analytical framework for determining when cloud-based inference is appropriate for latency-sensitive tasks. Existing assumptions about cloud unsuitability rely on outdated network conditions and underestimate the benefits of amortizing computation across high-throughput cloud infrastructure. A formal model characterizing the tradeoffs between on-device and cloud inference under realistic safety constraints is needed.

## Core Concepts & Theory

### System Model Components

**Sensing and Control Loop:**
- Perception module: Processes sensor data (camera, LiDAR, radar)
- Inference: Neural network processing for decision-making
- Control: Real-time response to perception output
- Cycle constraint: Entire loop must complete within deadline D

**Latency Sources:**
1. **Sensing latency** (t_sense): Time for sensor to capture frame
2. **Inference latency** (t_infer): Neural network processing time
3. **Network latency** (t_net): Communication delay to/from cloud
4. **Queueing latency** (t_queue): Wait time for cloud compute resource
5. **Control latency** (t_control): Time to execute control command

**Key Variables:**
- Sensing frequency (f): How often new perception data arrives
- Platform throughput (λ): Cloud platform's inference capacity (inferences/sec)
- Network delay (τ_net): Round-trip communication time
- Safety constraint (D): Maximum total latency allowed

### Analytical Model

**On-Device Inference:**
- Latency: t_total = t_sense + t_infer_local + t_control
- Constraint: t_total ≤ D
- Energy: Sustained computation on edge device
- Scalability: Limited by device power budget

**Cloud Inference:**
- Latency: t_total = t_sense + t_net + t_queue + t_infer_cloud + t_net + t_control
- Key insight: High cloud throughput can reduce t_queue below network latency
- When λ >> f (throughput >> sensing frequency), queueing overhead becomes negligible
- Constraint: t_net + t_queue + t_infer_cloud ≤ D - t_sense - t_control

**Critical Amortization Condition:**
If cloud throughput λ >> sensing frequency f, then:
- t_queue ≈ 1/λ (average per-request wait time)
- Total cloud inference latency ≈ 2·t_net + 1/λ + t_infer_cloud
- For high-throughput platforms, 2·t_net becomes the dominant term
- Cloud becomes viable if 2·t_net + 1/λ < t_infer_local

### Theoretical Results

1. **Amortization Regime**: Cloud inference latency can be lower than on-device if platform throughput >> frequency of inference requests

2. **Network Bandwidth Tolerance**: For emergency braking (100ms deadline), round-trip latency <50ms still allows cloud inference with modern GPUs

3. **Provisioning Rules**: Cloud platform should be provisioned with capacity λ ≥ 10·f to ensure queueing contributes <10% of deadline budget

## Main Ideas & Key Contributions

1. **Formal Latency Model**: Derives closed-form expressions for distributed inference latency capturing all components (network, queueing, compute). This enables quantitative comparison between architectures

2. **Amortization Principle**: Demonstrates that high-throughput cloud platforms can amortize network round-trip cost across many requests, making cloud inference viable for real-time tasks

3. **Safety-Aware Analysis**: Integrates task-specific safety constraints (maximum allowable latency) into the architectural decision framework, moving beyond average-case analysis

4. **Empirical Validation**: Simulations with real autonomous driving scenarios (emergency braking) using actual vehicular dynamics show cloud-based inference can maintain safety margins

5. **Practical Provisioning Guidelines**: Provides actionable rules for cloud capacity planning to meet latency requirements, enabling data-center architects to serve real-time applications

6. **Energy Efficiency Quantification**: Shows cloud-based inference can reduce edge device power consumption by 10-100x while meeting latency constraints

## Methodology & Implementation

### Simulation Framework

**Vehicle Dynamics:**
- Realistic emergency braking scenario using bicycle model
- Sensor: front-facing camera for obstacle detection
- Control task: compute deceleration needed to avoid collision
- Safety criterion: stopping distance < safe distance (function of velocity)

**Network Simulation:**
- Latency: Realistic RTT of 20-100ms (depending on geography)
- Throughput: Gigabit connections (1000 Mbps)
- Packet loss: Minimal (modern cloud infrastructure)
- Congestion: Modeled as queueing in M/M/c system

**Cloud Platform Simulation:**
- GPU throughput: Measured on actual hardware
  - Single A100: ~2000 inference/sec for ResNet-50 (batch=32)
  - Single H100: ~3000 inference/sec
- Batching: Requests accumulated and processed in batches
- Latency components: Batch assembly time, inference time, result transmission

**Neural Network Models:**
- Perception module: Object detection (YOLOv8), semantic segmentation
- Model size: 50M-200M parameters (practical for autonomous systems)
- Batch inference time: 10-50ms on modern GPUs

### Experimental Parameters

| Parameter | On-Device | Cloud |
|-----------|-----------|-------|
| Sensing frequency | 30 Hz | 30 Hz |
| Inference time | 40-100ms | 10-30ms (batch) |
| Network RTT | - | 20-100ms |
| Queueing overhead | - | ~1-5ms (at adequate provisioning) |
| Device power | 30-50W | Amortized across users |
| Total latency budget | 100-150ms | 100-150ms |

### Evaluation Metrics

**Primary Metrics:**
- End-to-end latency (p50, p95, p99 percentiles)
- Probability of deadline miss (safety metric)
- Energy consumption (joules per inference)

**Secondary Metrics:**
- Cost per inference
- Throughput utilization
- Scalability to multiple vehicles/sensors

### Datasets & Benchmarks

- **KITTI Dataset**: Real autonomous driving data from camera sensors
- **Cityscapes**: Urban scene understanding for semantic segmentation
- **NUSC (nuScenes)**: Multi-sensor autonomous driving dataset
- **Custom Simulation**: Generated emergency braking scenarios with varying vehicle speeds and obstacle positions

## Practical Applications & Real-World Use Cases

1. **Autonomous Vehicle Systems**: 
   - Safety-critical perception (object detection, pedestrian recognition)
   - Allows leveraging massive cloud compute while meeting <100ms deadline
   - Multiple vehicles share cloud infrastructure efficiently

2. **Connected Vehicle Services**:
   - Fleet management with shared cloud inference backbone
   - Enables features like coordinated path planning across vehicles
   - Energy savings on vehicle hardware

3. **Industrial Robotics**:
   - Manufacturing quality control using computer vision
   - Precision tasks with 50-200ms acceptable latencies
   - Shared inspection infrastructure across multiple production lines

4. **Smart City Infrastructure**:
   - Traffic monitoring and adaptive signal control
   - Crowd analytics for public safety
   - Shared perception cloud for distributed sensors

5. **Medical Robotics**:
   - Surgical assistance with 100-500ms latency budgets
   - Centralized computing for complex 3D reconstruction
   - Reduced heating/noise in operating rooms

6. **Aerospace Applications**:
   - Automated inspections of critical infrastructure
   - Satellite image analysis with <30 second decision windows
   - Reduces payload power requirements

## Insights & Implications

### Architectural Paradigm Shift

- **From Edge-Centric to Hybrid**: The traditional edge-first assumption is questioned. Hybrid architectures with selective cloud offloading are now preferred
- **Network as Enabler**: Good network connectivity (5G, fiber) becomes a key strategic asset for real-time systems
- **Compute Cost vs. Latency**: In cloud-abundant future, latency is more fungible than in device-limited edge scenarios

### Resource Allocation

- **Device Power Budget**: Edge devices can focus on control/actuation, offloading perception compute to cloud
- **Infrastructure Investment**: Data centers become critical infrastructure for time-sensitive systems, not just batch processing
- **Energy Efficiency**: Centralized GPU compute is more power-efficient per FLOP than distributed edge TPUs

### Safety and Reliability

- **Redundancy**: Cloud infrastructure enables multi-model ensembles for safety-critical perception
- **Monitoring**: Centralized vantage point for detecting anomalies and adversarial inputs
- **Graceful Degradation**: Well-connected system can switch between on-device and cloud inference dynamically

### Limitations & Open Questions

- **Network Stability**: Analysis assumes relatively consistent RTT; highly variable networks could violate assumptions
- **Adversarial Resilience**: Cloud connectivity creates new attack vectors (inference adversarial examples transmitted over network)
- **Regulatory**: Safety standards may not yet account for cloud-based inference in critical systems
- **Latency Extremes**: P99 latencies still relevant for safety; mean analysis insufficient
- **Wireless Variability**: 5G/cellular RTT much more variable than fiber; needs more thorough analysis
- **Failure Modes**: Network partition between vehicle and cloud; fallback strategy needed

### Future Directions

- Extend to multi-task inference (simultaneous perception tasks with shared computation)
- Integrate federated learning for on-device model improvement without full cloud dependency
- Study edge-cloud splits (some processing on device, some on cloud) optimized for specific latency budgets
- Investigate collaborative inference across multiple vehicles (joint perception with shared cloud compute)
- Formal verification of deadline guarantees under network variability

## Code & Resources

**Paper:**
- ArXiv: [https://arxiv.org/abs/2605.00005](https://arxiv.org/abs/2605.00005)
- ArXiv HTML: [https://arxiv.org/html/2605.00005](https://arxiv.org/html/2605.00005)
- IEEE Xplore: [https://ieeexplore.ieee.org/document/11133852/](https://ieeexplore.ieee.org/document/11133852/)
- NSF Public Access: [https://par.nsf.gov/biblio/10627004](https://par.nsf.gov/biblio/10627004)

**Authors:**
- Pragya Sharma
- Hang Qiu
- Mani Srivastava

**Dependencies:**
- Simulation: CARLA Simulator (open-source autonomous driving simulator) or custom vehicle dynamics
- Machine learning: PyTorch/TensorFlow for neural network execution
- Networking: ns-3 for network simulation (optional, for detailed network modeling)
- Optimization: Standard convex optimization tools

**Computational Requirements:**
- Simulation: CPU-based (moderate performance acceptable for emulation)
- Cloud platform simulation: GPU recommended for realistic throughput numbers
- Full-system simulation: 1-10 hours on standard workstations

**Reproducibility:**
- KITTI and nuScenes datasets publicly available
- Simulation code organization: core physics → network layer → inference layer
- Parameterizable: easy to adjust network latency, platform throughput, safety constraints

## Related Work & Context

### Real-Time Systems Theory

- **Control Systems**: Classic deadline-driven scheduling and real-time control theory
- **Cyber-Physical Systems**: Safety constraints in networked control systems
- **Embedded Systems**: Edge computing paradigms and resource constraints

### Distributed Inference

- **Model Partitioning**: Splitting neural networks between devices (ANSOR, Nimble)
- **Edge Computing**: Offloading computation to nearby servers
- **Federated Learning**: Distributed training while preserving privacy

### Autonomous Systems

- **Sensor Fusion**: Integrating multiple sensor modalities with latency constraints
- **Safety Verification**: Formal methods for autonomous system reliability
- **Real-time Perception**: Structured approaches to time-bounded inference

### Related Recent Papers

- **TimelyNet** (2026): Adaptive neural architecture for autonomous driving with dynamic deadlines
- **Impact Analysis of Inference Time Attack** (2505.03850): Security perspective on inference latency in perception
- **Model-Distributed Inference for LLMs** (2505.18164): Edge inference techniques for large models
- **Distributed Learning Systems Survey** (2501.05323): Broader perspective on distributed AI systems

### Network and Infrastructure

- **5G and Cellular Networks**: Improved but variable latency for mobile systems
- **Network Slicing**: Guaranteed bandwidth and latency for critical services
- **Edge Data Centers**: Distributed cloud infrastructure closer to users

## Conclusions

This paper makes an important correction to conventional wisdom in systems design. By developing a formal model and validating it empirically, the authors show that cloud-based inference is not inherently incompatible with real-time perception-driven control tasks. The key is proper provisioning of cloud infrastructure relative to sensing frequency. The work enables architects to make data-driven decisions about on-device vs. cloud inference based on quantitative latency-energy-cost tradeoffs, opening new possibilities for scalable autonomous systems.

## References

- Sharma, P., Qiu, H., & Srivastava, M. (2026). Cloud is closer than it appears: Revisiting the tradeoffs of distributed real-time inference. *arXiv preprint arXiv:2605.00005*.
- Misra, S., & Goswami, S. (2007). Network coding for IoT/M2M data collection: Improving transport layer efficiency. *IEEE Internet of Things Journal*.
- Geyer, R., Klein, G., & Noe, F. (2017). State of the art and challenges ahead for the cluster computing frameworks: A systematic review and future perspective. *ACM Computing Surveys*, 51(6), 1-38.
