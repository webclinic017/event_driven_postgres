#!/bin/bash

python prep_db.py

python -m flask run --host=0.0.0.0
