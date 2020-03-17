# dsc180a_A3 ~ Replication 

## Introduction 

This quarter has focused on Quantifying Abstraction. We have been looking at the painter, Piet Mondrian's work, and have been analyzing his shift from "real" to more abstract images. We have been aiming to quantify his work, and replicate a similar project done by Jason Bailey. 

With quantifying abstract features, we can assign a complexity score to each painting. 
- color score
- variance 
- edge score

complexity score = (color_score + variance_score + edge_score) / 3

## Description of Contents 

PROJECT
├── .env
├── .gitignore
├── README.md
├── config
│   ├── data-params.json
│   └── test-params.json
├── data
│   ├── urls
├── notebooks
│   └── .gitkeep
├── references
│   └── .gitkeep
├── requirements.txt
├── run.py
└── src
    └── etl.py
