#!/bin/bash
cd "$(dirname "$0")"
python -u run_it_all.py --username Thrall > log/thrall.log 2>&1 &
python -u run_it_all.py --username Uther > log/uther.log 2>&1 &
python -u run_it_all.py --username Anduin > log/anduin.log 2>&1 &
python -u run_it_all.py --username Valeera > log/valeera.log 2>&1 &
python run_it_all.py --username Jaina --creator