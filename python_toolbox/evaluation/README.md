# Python Toolbox for Evaluation

This Python script evaluates **training** dataset of TanksAndTemples benchmark.
The script requires ``Open3D`` and a few Python packages such as ``matplotlib``, ``json``, ``numpy``.

## How to use:
**Step 0**. Reconstruct 3D model and recover camera poses from the training dataset.
The raw videos of the training dataset can be found from:
https://tanksandtemples.org/download/

**Step 1**. Download evaluation data (ground truth geometry + reference reconstruction) using
[this link](https://drive.google.com/open?id=1VDHEqGAuLyGa7Bv3lGOr1KX2RhPbHLxw). For this example, we regard ``TanksAndTemples/evaluation/data/`` as a dataset folder.

**Step 2**. Install Open3D. Follow instructions from http://open3d.org/docs/getting_started.html

**Step 3**. Clone this repository and follow instructions in ``setup.py``.

**Step 4**. Run the evaluation script and grab some coffee.
```
python run.py
```
This will show like below:
```
===========================
Evaluating Ignatius
===========================
C:/git/TanksAndTemples/evaluation/data/Ignatius/Ignatius_COLMAP.ply
Reading PLY: [========================================] 100%
Read PointCloud: 6929586 vertices.
C:/git/TanksAndTemples/evaluation/data/Ignatius/Ignatius.ply
Reading PLY: [========================================] 100%
:
ICP Iteration #0: Fitness 0.9980, RMSE 0.0044
ICP Iteration #1: Fitness 0.9980, RMSE 0.0043
ICP Iteration #2: Fitness 0.9980, RMSE 0.0043
ICP Iteration #3: Fitness 0.9980, RMSE 0.0043
ICP Iteration #4: Fitness 0.9980, RMSE 0.0042
ICP Iteration #5: Fitness 0.9980, RMSE 0.0042
ICP Iteration #6: Fitness 0.9979, RMSE 0.0042
ICP Iteration #7: Fitness 0.9979, RMSE 0.0042
ICP Iteration #8: Fitness 0.9979, RMSE 0.0042
ICP Iteration #9: Fitness 0.9979, RMSE 0.0042
ICP Iteration #10: Fitness 0.9979, RMSE 0.0042
[EvaluateHisto]
Cropping geometry: [========================================] 100%
Pointcloud down sampled from 6929586 points to 1449840 points.
Pointcloud down sampled from 1449840 points to 1365628 points.
C:/git/TanksAndTemples/evaluation/data/Ignatius/evaluation//Ignatius.precision.ply
Cropping geometry: [========================================] 100%
Pointcloud down sampled from 5016769 points to 4957123 points.
Pointcloud down sampled from 4957123 points to 4181506 points.
[compute_point_cloud_to_point_cloud_distance]
[compute_point_cloud_to_point_cloud_distance]
:
[ViewDistances] Add color coding to visualize error
[ViewDistances] Add color coding to visualize error
:
[get_f1_score_histo2]
==============================
evaluation result : Ignatius
==============================
distance tau : 0.003
precision : 0.7679
recall : 0.7937
f-score : 0.7806
==============================
```
and so on for other datasets.

**Step 5**. Check the evaluation folders. For example, ``TanksAndTemples/evaluation/data/Ignatius/evaluation/`` will have following outputs.

<img src="images/f-score.jpg" width="400">

``PR_Ignatius_@d_th_0_0030.pdf`` (Precision and recall curve with F-score)

| <img src="images/precision.jpg" width="200"> | <img src="images/recall.jpg" width="200"> |
|--|--|
| ``Ignatius.precision.ply``  | ``Ignatius.recall.ply`` |

(Color coded by jet colormap)
