# Random Face

A simple python library for fast image generation of people who do not exist.

<p align="center">
  <img src="res/faces.jpeg"/>
</p>

## Requirements

* Linux, Windows, MacOS
* Python 3.8+
* CPU compatible with OpenVINO.

## Install package

```bash
pip install random_face
```

## Install the latest version

```bash
git clone https://github.com/bes-dev/random_face.git
cd random_face
pip install -r requirements.txt
python download_model.py
pip install .
```

## Demo

```bash
python -m random_face.demo
```

## Example

```python
import cv2
import random_face

engine = random_face.get_engine()
face = engine.get_random_face()
cv2.imshow("face", face)
cv2.waitKey()
```
