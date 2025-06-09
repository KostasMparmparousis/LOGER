## Setup Environment
1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if not already installed.
2. Create and activate the environment:
   ```bash
   conda env create -f environment.yml
   conda activate loger
   ```

## Training Guide

1. Configure the model checkpoint path in `train.py` (line 313):
   ```python
   model_dir = "/your/path/here"  # Update this path to save your checkpoint
   ```

2. Run the training script:
   ```bash
   python3 train.py
   ```

## Testing guide

1. Configure the model checkpoint path in `test_loaded_checkpoint.py` (line 20):
   ```python
   MODEL_DIR = "/your/path/here"  # Update this path to load your checkpoint
   ```

2. Run the testing script:
   ```bash
   python3 test_loaded_checkpoint.py \
       /path/to/workload/experiment1/job/run1/ \
   ```

---

# LOGER: A Learned Optimizer towards Generating Efficient and Robust Query Execution Plans

## Requirements

Before running LOGER, please install [PyTorch](https://pytorch.org/get-started/locally/) and [Deep Graph Library (DGL)](https://www.dgl.ai/pages/start.html) following the instructions on the pages, and run the command `pip install -r requirements.txt` to install psycopg2 and cx-Oracle. In addition, we use [psqlparse](https://github.com/alculquicondor/psqlparse) to parse queries. Since we found that installing psqlparse with `pip` may result in errors, we recommend building it directly with setup.py. We provide a compiled version in our repository.

## Running

To train LOGER with default settings, please use the following command.

```shell
python train.py
```

We provide a list of available arguments to change settings.

- `-D DATABASE`: To specify the PostgreSQL database name. By default, we set the name to `imdb`.
- `-U USER`: To specify the PostgreSQL user name. The default value is `postgres`.
- `-P PASSWORD`: To specify the password of the PostgreSQL user. By default, the password is not used.
- `--port PORT`: To specify the port of PostgreSQL.
- `-d TRAIN TEST`: To train with the specified training and testing workloads. TRAIN is the folder of training workload, and TEST is for testing workload.
- `-e EPOCHS`: To train with the specified number of epochs. The default value is `200`.
- `-F FILE_ID`: To change the output file ID of experiment results and checkpoints. The default value is `1`.
- `-b BEAM_SIZE`: To change the beam size of $\epsilon$-beam search. The default value is `4`. To use $\epsilon$-greedy, please use a value less than 0.
- `-l NUM_LAYERS`: To specify the number of Graph Transformer layers used in the query representation module. The default value is `1`.
- `-w WEIGHT`: To specify the weight factor of reward weighting. The default value is `0.1`.
- `-N`: To directly choose physical operators instead of using restricted operator.
- `--bushy`: To allow bushy plan generation.
- `--no-exploration`: To use the original beam search instead of $\epsilon$-beam search.
- `--no-expert-initialization`: To forbid initializing the experience dataset with expert knowledge.
- `--seed VALUE`: To set the random seed of training.
