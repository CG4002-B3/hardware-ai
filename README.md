# hardware-ai

## Set up

- Fork https://github.com/CG4002-B3/hardware-ai
- Clone https://github.com/<username>/hardware-ai.git
- `cd hardware-ai`
- Create virtual environment

```
python -m venv venv
conda deactivate # if you are using conda
source venv/bin/activate
```

- Install dependencies: `pip install -r requirements`


## Pipeline

Convert raw data: 
- Put json files to `convert/json`
- Run `python convert.py`
- Converted files can be found in `convert/csv`

Train model:
- Copy all files from `convert/csv` to `integration/data/raw`
- Open jupyter notebook
- Restart & run all `integration/full_classificaiton.ipynb` to train the model
- Restart & run all `integration/prepare_hls.ipynb` to get the weights for HLS

Generate bitstream
