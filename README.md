# Bolotin Viewer

Bolotin Viewer is a Flask based application that assists with those with vision impairments.


## Installation


```bash
git clone https://github.com/mavsharklife/bolotin-viewer.git
cd bolotin-viewer
pip install -r requirements.txt
```

### Dependencies

| Package | Version |
|---|---|
| Flask | 3.1.3 |
| numpy | 2.4.2 |
| opencv-contrib-python | 4.11.0.86 |
| opencv-python | 4.13.0.92 |
| opencv-python-headless | 4.10.0.84 |
| torch (CUDA 12.8) | 2.10.0 |
| ultralytics | 8.4.14 |

>  Note: The `torch` version listed is built for CUDA 12.8. If you don't have the correct GPU, install the CPU version instead:
> ```bash
> pip install torch --index-url https://download.pytorch.org/whl/cpu
> ```
    


# Acknowledgements

This project uses Ultralytics YOLO26 (Version 26.0.0).
Jocher, G., & Qiu, J. (2026). Ultralytics YOLO26 (Version 26.0.0).
Retrieved from https://github.com/ultralytics/ultralytics
Licensed under AGPL-3.0.
