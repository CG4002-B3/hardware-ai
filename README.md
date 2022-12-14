# hardware-ai

Hardware AI component for LaserTag project. For more details, please refer to [Project demo](https://youtu.be/nKTPNiXV2OA) and [Hardware AI component explained](https://youtu.be/flD5HsB7LyY)

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
* Run C Synthesis. If nothing goes wrong, you should see a Synthesis Report with hardware resources usage, latency, ...
* Run C Siumulation. Check whether the result of the hardware implementation matches the target actions.
* Run C/RTL Cosimulation (can skip)
* Export RTL (you may need to change the date time of your computer to the year 2021). 

### 2.4 Generate Bitstream (Vivado)
* Open Vivado
* Follow [Vivado one-time-setup](#32-vivado-one-time-setup) to create a new project or open an old project with the correct config
* If you already have to correct block design, just refresh the generated IP, or follow the last few steps of [Vivado one-time-setup](#32-vivado-one-time-setup) to remove and add the repo with the new IP again
* Generate Bitstream

### 2.5 Transfer bitstream to Ultra96
* After bitstream is generated using Vivado, the bitstream file `.bit` can be found under `project_dir/runs/impl_1` and the hardware handoff file `.hwh` can be found under `project_dir/project_name.srcs/sources_1/bd/design_name/hw_handoff`
* Copy those 2 files to Ultra96 (make sure they have the same name)

# 3. Appendix

## 3.1 Vivado HLS one-time-setup
* Create a new project 
* Specify Project Name and Project Location (should not have space in the path). Click Next
* Specify the Top Function, should be `inference`. Click Next. Click Next
* For Solution Configuration, under Part Selection, search for `xczu3eg-sbva484-1-i`. Click OK. Click Finsh
* Add new files `core.cpp` and `core.h` under `Souce`, `test_core.cpp` under `Test Bench`. The project structure should be like below

```
project_name
+-- includes
+-- Source
|   +-- core.cpp
|   +-- core.h
+-- Test Bench
|   +-- test_core.cpp
+-- Solution1
```
* Copy respective files from `hls/`

## 3.2 Vivado one-time-setup
* Create a new project. Click Next
* Specify Project name and Project location (should not have space in the path). Click Next 4 times
* For Default Part, under Parts, search for `xczu3eg-sbva484-1-i`. Click Next. Click Finsh
* Under Project Manager, choose Settings > Project Settings > IP > IP Repository. Under IP Repositories, click `+` and search for the directory that contains the IP generated in [step 2.3](#23-extract-ip-core-vivado-hls), add that directory to the IP repositories.
* Under IP Generator, select Create Block Design, specify Design name, and click OK.
* On the Diagram pannel, click `+` and add the following blocks to the block design:
    * Zynq UltraScale+ MPSoC
    * AXI Direct Memory Access
    * AXI SmartConnect
    * AXI Interconnect
    * The IP generated in [step 2.3](#23-extract-ip-core-vivado-hls)
* Make connections as the attached diagram (pay attention to m_axis and s_axis ports), Run Connection Automation if it's prompted. A Processor System Reset block will be automatically added.

![block diagram](imgs/block_diagram.jpeg)

* Click on Zynq UltraScale+ MPSoC and AXI Direct Memory Access to customize the IP (disable Scatter Gather Engine, disable peripherals, match bit length and address length of axi stream). Save block design.
* Click Validate Design to make sure everything is connected correctly.
* Under Souces > Design Sources, right click on the design, choose Create HLD Wrapper, click OK.
* Generate Bitstream
