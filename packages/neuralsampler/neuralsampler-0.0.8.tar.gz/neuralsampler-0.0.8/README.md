[![PyPI version](https://badge.fury.io/py/neuralsampler.svg)](https://badge.fury.io/py/neuralsampler)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1gEUjfsmoinemOb3P6p0UCI3zfYx-T8uI?usp=sharing)

## NeuralSampler - Pytorch

Implementation of Neural Sampler. 

## Install

``` bash
$ pip install neuralsampler
```

or install the latest version by 
``` bash 
pip install -U git+https://JiahaoYao:{password}@github.com/JiahaoYao/neuralsampler.git@main
```

Install the jax (follow the official instruction [here](https://github.com/google/jax#installation))
```bash 
pip install jax jaxlib==0.1.64+[YOUR_CUDA_VERSION] -f https://storage.googleapis.com/jax-releases/jax_releases.html
```
e.g. 
```bash
pip install --upgrade jax jaxlib==0.1.64+cuda101 -f https://storage.googleapis.com/jax-releases/jax_releases.html
```


## Usage

```python
import torch
from neuralsampler import neuralsampler
```

## Run the code 

```bash 
python main.py 
```

## Run the scripts 

```bash 
python scripts/test_job.py 
```

## Ignore me (random things)
```
this repo is to collect all the random results and reproduce the experiments here 

and then jax 

i will use jax and flax, like shown here: https://github.com/yang-song/score_sde

there are the templates of building the jax neural networks (quite interesting to try this functional programming )
```


## Todo list 
- [x] this library is on the pytorch
- [x] i am also going to prepare the colab notebook 
- [x] the dataset is through the gdown: you can download the dataset from the google drive  
