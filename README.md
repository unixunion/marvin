# requirements

    conda create -n py36-marvin python=3.6
    conda activate py36-marvin
    conda install scikit-learn
    pip install -U sklearn-crfsuite
    pip install pyyaml requests
    pip install rasa_nlu scipy

# preparing spacy

    python -m spacy download en

# Runing the training data editor

    rasa-nlu-trainer -s database.json

# Running rasa

## Training

    rm -rf projects/default

### Train the AI:

    python -m rasa_nlu.train -c  configs/config_spacy.json

## Running

    python -m rasa_nlu.server -c configs/config_spacy.json

## testing

    curl -X POST localhost:5000/parse -d '{"q":"hello"}' | python -m json.tool


## reference

https://github.com/ugik/notebooks/blob/master/Tensorflow%20chat-bot%20response.ipynb
https://chatbotsmagazine.com/contextual-chat-bots-with-tensorflow-4391749d0077
https://github.com/tensorflow/models/tree/master/tutorials/embedding

http://www.nltk.org/book/ch00.html

https://github.com/Rapptz/discord.py

http://rasa-nlu.readthedocs.io/en/latest/tutorial.html#preparing-the-training-data

## README

https://rasa-nlu.readthedocs.io/en/latest/pipeline.html#ner-spacy
http://rasa-nlu.readthedocs.io/en/latest/installation.html#section-backends