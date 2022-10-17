# hardware-ai

1. [Set up](#1-set-up)
2. [Pipeline](#2-pipeline)\
    2.1 [Convert raw data](#21-convert-raw-data)\
    2.2 [Train model](#22-train-model)\
    2.3 [Extract IP Core (Vivado HLS)](#23-extract-ip-core-vivado-hls)\
    2.4 [Generate Bitstream (Vivado)](#24-generate-bitstream-vivado)\
    2.5 [Transfer bitstream to Ultra96](#25-transfer-bitstream-to-ultra96)
3. [Appendix](#3-appendix)\
    3.1 [Vivado HLS one-time-setup](#31-vivado-hls-one-time-setup)\
    3.2 [Vivado one-time-setup](#32-vivado-one-time-setup)


## 1. Set up

* Fork https://github.com/CG4002-B3/hardware-ai
* Clone https://github.com/your-username/hardware-ai.git
* `cd hardware-ai`
* Create virtual environment

```
python -m venv venv
conda deactivate # if you are using conda
source venv/bin/activate
```

* Install dependencies: `pip install -r requirements`


## 2. Pipeline

### 2.1 Convert raw data
* Create 2 empty folder `json` and `csv` inside `convert` if they are not there
* Put all raw data (json format txt) files to `convert/json`
* Run `python convert.py` 
    * Note: if it throws an error, there must be something wrong with the raw data file in `convert/json`
* Converted files can be found in `convert/csv`

### 2.2 Train model
* Copy all files from `convert/csv` to `integration/data/raw`
* Open jupyter notebook
* Restart & run all `integration/full_classificaiton.ipynb` to train the model
* Restart & run all `integration/prepare_hls.ipynb` to get the weights for HLS

### 2.3 Extract IP Core (Vivado HLS)
* Open Vivado HLS
* Follow [Vivado HLS one-time-setup](#31-vivado-hls-one-time-setup) to create a new project or open an old project with the correct config
* Update `core.h` file with the parameters from `integration/prepare_hls.ipynb`:
    * Number of input features `INPUT_SIZE`
    * Number of hidden neurons `HIDDEN_SIZE`
    *  Weights for 2 layers: `l1_weights`, `l2_weights`, `l1_bias`, and `l2_bias`
* Update `test_core.cpp` with the test benchmark from `integration/prepare_hls.ipynb`:
    * Number of testing samples to compare `NUM_SAMPLES`
    * Put the samples into `input` 2d-array
    * Put the corresponding inference result into `action`

### 2.4 Generate Bitstream (Vivado)
* Open Vivado
* Follow [Vivado one-time-setup](#32-vivado-one-time-setup) to create a new project or open an old project with the correct config


### 2.5 Transfer bitstream to Ultra96

# 3. Appendix

## 3.1 Vivado HLS one-time-setup
* Create a new project 
* Part number: xczu3eg-sbva484-1-i

## 3.2 Vivado one-time-setup



