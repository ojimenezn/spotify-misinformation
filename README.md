# Misinformation within Spotify Podcasts

## Abstract

We propose a Natural Language Processing (NLP)-based approach to identify potentially misinformative claims in podcast transcripts. 
The proposed system uses a sentence-level analysis of podcast transcripts and claims from a fact-checked database by encoding these into a latent space, which is then explored to search for pairs with high semantic similarity. 
This approach resulted in SpotiFact, a dataset of more than 27 million similar pairs from the Spotify Podcast Dataset compiled to link stance (whether in agreement or not), out of which we manually label a subset of 1,200 claims from the top 3000 claims with highest similarity scores. 
We find that although most matched pairs are unlikely to be directly related, results suggest facts and misinformation spread at roughly the same rate within Spotify podcasts. 
In addition, we build a set of machine learning models that are able to automatically detect misinformation in podcast transcripts, out of which a SentenceBERT + Linear Classifier performs best with an AUC score of 0.67. 

## Overview

This repo contains code written to explore misinformation within Spotify Podcasts. The contributers are Jonathan Leo, Omar Jiménez, and Abhijeet Tomar. This started off as a class project within the Georgia Tech class CS 8803, Data Science for Social Networks, taught by Dr. Srijan Kumar.

The preprocessing step can be performed locally on your machine, but the rest of the steps require Google Colab and Google Drive. We used these tools due to limited computational and storage resources. For this project we upgraded to Google Colab Pro ($9.99 per month), which allows for more GPU resources and more instance runtime, and Google One Basic ($1.99 per month), which upgrades Google Drive storage to 100 GB (compared to 15 GB). 

Steps to properly setup the folder structure within Google Drive is detailed below.

### Spotify Podcast Data

The spotify podcast dataset must be requested and used for non-commercial purposes per their license. Info about requesting and use can be found here: https://podcastsdataset.byspotify.com

Once acquired, copy the ```podcasts-no-audio-13GB``` folder into the top directory of this repo.

## How to Run

### 1. Local Conda Environment

We used conda or miniconda as a package manager for the locally run scripts. Create a conda environment and install the required packages located in requirements.txt by running 

```conda create --name <env> --file requirements.txt```

### 2. Preprocessing

To run the preprocessing steps on the Spotify podcast dataset and scrape the politifact dataset, run the following commands in the terminal:

```
cd preprocessing
python read_podcasts.py
python politifact_scraping.py
```

These scripts will produce two files within the ```preprocessing/outputs``` directory.

* ```podcast_claims_context_2.tsv``` contains the podcast claims with 2 sentences on each side as surrounding context. 

* ```politifact_filtered.csv``` contains the fact checked politifact claims.

### 3. Google Drive and Google Colab setup

For the rest of the steps, Google Drive and Google Colab are used due to limited computational resources. To setup these files, upload the ```colab_setup.ipynb``` notebook (located in top directory) to Google Colab and run all the cells. This will setup the file structure within your Google Drive needed to run the rest of this project. 

After running, navigate to the ```'/drive/MyDrive/spotify-misinformation/preprocessing-outputs``` folder newly created within your Google Drive. Upload the preprocessed dataset files (```podcast_claims_context_2.tsv``` and ```politifact_filtered.csv```) within ```preprocessing/outputs``` to this folder. You should be all set to run the additional Colab notebooks after this step.

### 4. Claim Matching

The claim matching code is located within the ipython notebook ```colab-notebooks/matching-claims.ipynb```. Upload this notebook to your Google Colab and run all cells.

This notebook will embed both podcast claims and fact checked claims using SentenceBert, compute the cosine similarity between them, and store paired podcast and fact checked claims indices that have cosine similarity higher than 0.4.

The output of this notebook is stored within ```/drive/MyDrive/spotify-misinformation/matched-claims-output/matched_claims_context_2.txt```. The columns are the fact checked claim index, podcast claim index, and cosine similarity score. 

### 5. Manual Labeling

This step is optional since we provide our manually curated dataset already, which is located at ```manually-labeled-matched-pairs.csv```. To skip recreating this dataset, upload this file into the ```/drive/MyDrive/spotify-misinformation/labeling-output``` folder. Otherwise it can be recreated by following the steps below.

For the manual labeling process, the top 3000 paired claims ranked by cosine similarity were taken and randomly split them into datasets for the authors to label. The code to form these files and calculate interrater agreement once they're labeled is found at ```colab-notebooks/labeling.ipynb```. Upload this notebook to colab and run all cells to get these datasets and calculate interrater agreement. 

We used the following label schema:

| Stance Agreement     | Label |
| -----------------    |:-----:|
| Not yet labeled      | -1    |
| Agreement            | 1     |
| Partial Agreement    | 2     |
| Disagreement         | 3     |
| Partial Disagreement | 4     |
| Unrelated            | 5     |
| Inconclusive         | 6     |

The individual datasets manually labeled by the authors are provided in the directory ```authors-labeling-datasets```. These were combined into ```manually-labeled-matched-pairs.csv``` using the process described within the paper. 

### 6. Model Benchmarking and Prediction 

Once the manually labeled dataset is copied over or recreated, various models can be trained. We train 3 models which are described in the paper. Each is a different type of embedding trained with a linear classifier on top. The embeddings models are a frozen SentenceBert model, a frozen BERT-Large model, and a finetuned BERT-Large model. 

To train these models, upload the ```colab-notebooks/model-training.ipynb``` notebook to colab and run all cells. This will train the three models mentioned above using the hyperparameters and splits of the models we report in the paper. The performance is printed as output to the training cells and the weights of the best models are saved in the ```/drive/MyDrive/spotify-misinformation/modeling-output/trained-models``` folder on Google drive. 

From our results, the best performing model was SentenceBERT + Linear Classifier. To run this classifier on the matched_claims data that wasn't labeled, upload the ```colab-notebooks/sbert-model-prediction.ipynb``` notebook and run all cells. This will predict the stance of each matched pair then save this information along with the ground truth politifact label and the misinformation label via our misinformation mapping schema defined in the paper. This output is located in ```/drive/MyDrive/spotify-misinformation/modeling-output/```. Specifically ```/drive/MyDrive/spotify-misinformation/modeling-output/predicted_mc_context_2.txt``` contains the matched claim indices, cosine similarity score, SentenceBERT prediction, fact checked claim label, and corresponding misinformation claim.

### 7. Data Analysis

We provide some preliminary data analysis of the matched claims, manually labeled claims, and predicted matched claims within the ```colab-notebooks/data-analysis.ipynb``` notebook. Run all cells to see various visualizations we used within our paper and final presentation. These figures are saved to the ```/drive/MyDrive/spotify-misinformation/data-analysis-output``` folder.
