# AR/EN NER Challenge

This challenge was part of my internship at KeemetAI. The project description can be found in the PDF file located in the root directory.

## Challenge Overview

The goal is to capture the following entities in both Arabic and English languages:
- Dates
- Times
- Measurement Units
- Quantity
- Colors
- Currency
- Age
- Prices

Existing NER models, such as [marefa-nlp/marefa-ner](https://huggingface.co/marefa-nlp/marefa-ner) (1) and [hatmimoha/arabic-ner](https://huggingface.co/hatmimoha/arabic-ner) (2), do not capture all the required entities. Additionally, the data they were trained on is unavailable, making fine-tuning challenging.

## Approach

### Day 1

- Searched for AR + EN NER models on Hugging Face but couldn't find suitable ones.
- Attempted to find datasets containing the required entities but was unsuccessful.
- Implemented a pipeline for:
  - **Synthetic Data Generation** using GPT
  - **Annotation** using LabelBox
  - **Fine-tuning** a smaller NER model variant
  - **Concatenating** the output of the fine-tuned model with a larger model (1).

### Day 2

- Continued Implementation of the pipeline.
- Added Regex Parsers for easily parsable entities like Colors.
- Created the API and Dockerfile.

## Limitations & Future Work

1. **Collected Data**: The dataset is small (~190 samples) and lacks diversity. About 60% of the data was annotated automatically using GPT-4. For production use, more time should be invested in data collection and annotation.

2. **Regex Parsers**: Regex parsers are effective for Colors and Units but may not be ideal for Dates, Times, Prices, Currency, Age, and Quantity.

3. **Entity Detection Selection**: The API currently provides three separate outputs from different approaches. There is no logic to merge these outputs into a final result. This requires a testing dataset to determine the best merging strategy.

## Installation and Usage

### Inference

1. Build the Dockerfile.
2. Run the container.
3. Check `examples.ipynb` for examples on how to use the API.

**Expected Input Shape**: 
```json
{"texts": ["string1", "string2"]}
```
Returns: Dictionary with outputs from each approach.

### Training

- use the training Utils provided, such as the LabelBox parser and data handlers formatters in `app/`