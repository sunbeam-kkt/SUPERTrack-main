# SUPERTrack-main

### This is the official code of the paper ***SUPER-Track: Semantic Unified Pseudo-segmentation and Enhanced Representation for Multi-UAV Perception***

*The rapid expansion of unmanned aerial vehicle (UAV) applications has heightened the demand for robust multi-UAV detection and tracking. Although significant progress has been made in object detection and trajectory prediction, existing methods remain challenged by appearance ambiguity in small targets, cluttered backgrounds, and frequent motion perturbations, often resulting in identity switches and fragmented trajectories. Furthermore, most trackers overlook high-level semantic cues, limiting long-term consistency under occlusion and noise. In this study, we propose a novel framework specifically designed for multi-UAV tracking. First, we introduce a multi-instance semantic pseudo-segmentation strategy that separates UAV foregrounds from visually similar backgrounds while suppressing distractors through hard negative mining. Second, we formulate a spatiotemporal consistency constraint to enhance target stability and mitigate information loss from occlusions or viewpoint changes. Third, we develop a semantic precision tracker that performs window-based video analysis, extracts instance-level semantics, and encodes them into high-level feature representations. Extensive experiments demonstrate that our approach achieves state-of-the-art performance in both small-object detection and multi-UAV tracking.*

The structure of the UAV detection part is shown as subfigure:

![IPS-SOD](https://github.com/sunbeam-kkt/SUPERTrack-main/blob/main/docs/SBD-based%20on%20YOLOv13.jpg)

Correspondingly, the structure of UAV target tracking is shown in the following figure:

![CSPTracker](https://github.com/sunbeam-kkt/SUPERTrack-main/blob/main/docs/CSPTracker.jpg)

We can easily start training the SUPERTrack model by:

```python
python train.py
```

Then run the following code to train the tracker:

```python
python csptracker.py
```

Calculate the MOTA value using the detection code officially released by CVPR. First, enter folder __MultiUAV_Baseline_code_and_submissi__, then run:

```python
python tool/2_compute_MOTA.py
```

And you also can test the trained model by run:

```python
python test.py
```

The visualization of SUPERTrack on AntiUAV410 datatset is shown in the following figure:

![visualization](https://github.com/sunbeam-kkt/SUPERTrack-main/blob/main/AntiUAV410.jpg)

