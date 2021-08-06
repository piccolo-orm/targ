#!/bin/bash

SOURCES="targ tests"

isort $SOURCES
black $SOURCES
flake8 $SOURCES
mypy $SOURCES
