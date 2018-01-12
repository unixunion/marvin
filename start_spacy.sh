#!/usr/bin/env bash
rm -rf projects/default
python -m rasa_nlu.train -c  configs/config_spacy.json
python -m rasa_nlu.server -c configs/config_spacy.json