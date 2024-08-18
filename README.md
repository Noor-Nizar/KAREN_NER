# KAREN NER - Keemet AI AR/EN NER Challenge

This challenge was part of my internship at KeemetAI. The project description can be found in the PDF file located in the root directory.

## Challenge Overview

The goal is to capture the following entities in both Arabic and English languages:
- Dates - Times - Measurement Units - Quantity - Colors - Currency - Age - Prices

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

### Day 3

- Annotated the automatically annotated examples mentioend above, revised the manual annotations. Resulting in an F-Score increase of ~0.15
- Used manually annotated data.txt file as an example for Gemini 1.5 Pro to generate sythetic annotated data (~ extra samples 300)
- Trained on the synthetic data, and evaluated on the manual data, result was 0.8 Weighted F1-Score. This confirmed that the synthetic data was useful.
- Combined the manually annotated data with the synthetic data, and trained on the combined data. The result was 0.95 Weighted F1-Score on the eval split of the combined data.
- Despite high weighted F1-Score model had perormaed poorly on specific entities which were not well present in the data, such as Age, and Currency. Attempted to generate more synthetic data for these entities, Macro F1-Score increased from 0.74 to 0.8
- Bug Fixes, Response Schema Unification.

## Limitations & Future Work

1. **Collected Data**: Testing needs to be done to ensure that the synthetic data is sufficient and will generalize to real-world data.

2. **Regex Parsers**: Regex parsers are effective for Colors and Units but may not be ideal for Dates, Times, Prices, Currency, Age, and Quantity.

3. **Entity Detection Selection**: The API currently provides three separate outputs from different approaches. There is no logic to merge these outputs into a final result. This requires a testing dataset to determine the best merging strategy.

## Usage

### Inference

1. Download Model state from https://drive.google.com/drive/u/0/folders/1erHkR3eRgE5KxvmeiygdJZP0Sv48-6AG and extract it in the models/ directory.
2. Build the Dockerfile.
3. Run the container.
4. Check `examples.ipynb` for examples on how to use the API.


### Training

- use the training Utils provided, such as the LabelBox parser and data handlers formatters in `app/`
