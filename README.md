# marvin

Marvin is a plugable chatops bot, which uses natural langing processing
to determine intents.

# status

*NOT READY*, NLP development underway, nothing else is done.

# requirements

    conda create -n py36-marvin python=3.6
    conda activate py36-marvin
    pip install pyyaml requests
    pip install rasa_nlu scipy

# configuring backends

config/*.json contain pure spacy and mitie+spacy pipelines.

Choose one or both of:

## mitie

    pip install git+https://github.com/mit-nlp/MITIE.git

Then download https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2
and put `total_word_feature_extractor.dat` into data/

## spacy

    pip install -U spacy
    python -m spacy download en
    # conda: conda install scikit-learn
    # pip: pip install -U scikit-learn scipy sklearn-crfsuite
    pip install -U sklearn-crfsuite

## mitie + spacy

Do both above!

# Running the training data editor

    rasa-nlu-trainer -s database.json

edit training sets

# Configuring

see config/

# Training

Edit data/database.md

# Running rasa server

## Training and Running

see start_mitie.sh and start_spacey.sh

## testing

### shell

    python shell.py

### curl

    curl -X POST localhost:5000/parse -d '{"q":"hello"}' | python -m json.tool

### discord

    DISCORD_KEY='foo' python discord_bot.py


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