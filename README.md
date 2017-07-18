# Tanks and Temples - Python script
This repository provides two python scripts:
- upload-t2-result.py : for submitting result for evaluation.
- download_t2_dataset.py : for downloading dataset from website.

Please cite following paper if you are using this software.

```
@article{Knapitsch2017,
    author    = {Arno Knapitsch and Jaesik Park and Qian-Yi Zhou and Vladlen Koltun},
    title     = {Tanks and Temples: Benchmarking Large-Scale Scene Reconstruction},
    journal   = {ACM Transactions on Graphics},
    volume    = {36},
    number    = {4},
    year      = {2017},
}
```

For more details, please visit [tanksandtemples.org](http:\\tanksandtemples.org)

## Requirements
These scripts are tested on Python 2.7 and Python 3.x.

Python 2.7 users need to install `requests` package using following command
```
sudo pip install requests
```

## Usage
Downloader
```
> python download_t2_dataset.py [-h] [-s] [--modality MODALITY] [--group GROUP] [--unpack_off] [--calc_md5_off]

Example 1: download all videos for intermediate and advanced scenes
> python download_t2_dataset.py --modality video --group both

Example 2: download image sets for intermediate scenes (quick start setting)
> python download_t2_dataset.py --modality image --group intermediate

Example 3: show the status of downloaded data
> python download_t2_dataset.py -s
```

Uploader
```
> python upload-t2-results.py [-h] [--group GROUP]

Example 1: upload intermediate and advanced reconstruction results
> python upload-t2-results.py --group both

Example 2: upload only intermediate results
> python upload-t2-results.py --group intermediate
```
