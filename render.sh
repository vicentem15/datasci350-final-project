#!/bin/bash
# Render script - activates venv and renders the report

source venv/bin/activate
quarto render report.qmd
