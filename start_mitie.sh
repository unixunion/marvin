#!/usr/bin/env bash
rm -rf projects/default
python -m rasa_nlu.train -c  configs/config_mitie.json --fixed_model_name=fallback
python -m rasa_nlu.server -c configs/config_mitie.json