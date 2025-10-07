# SUPERTrack-main

### This is the official code of the paper ***SUPER-Track: Semantic Unified Pseudo-segmentation and Enhanced Representation for Multi-UAV Perception***

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

