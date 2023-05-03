#!/bin/sh -e
set -x

ruff src --fix
black src
isort src