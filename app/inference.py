import torch
from typing import List

from torch.utils.data import DataLoader

from app.datasets import InferenceDataset
from app.regex_finders import regex_ner

def get_labels_tuned() -> dict:
    # FIXME : update this automatically
    return {0: 'B-Age', 1: 'B-Colors', 2: 'B-Currency', 3: 'B-Dates', 4: 'B-Prices', 5: 'B-Quantity', 6: 'B-Times', 7: 'B-Units', 8: 'I-Age', 9: 'I-Colors', 10: 'I-Currency', 11: 'I-Dates', 12: 'I-Prices', 13: 'I-Quantity', 14: 'I-Times', 15: 'I-Units', 16: 'O'}

def get_labels_main() -> dict:
    ''' Returns the labels for inference '''
    custom_labels = {0: 'O', 1: 'B-job', 2: 'I-job', 3: 'B-nationality', 4: 'B-person', 5: 'I-person', 6: 'B-location', 7: 'B-time', 8: 'I-time', 9: 'B-event', 10: 'I-event', 11: 'B-organization', 12: 'I-organization', 13: 'I-location', 14: 'I-nationality', 15: 'B-product', 16: 'I-product', 17: 'B-artwork', 18: 'I-artwork'}
    return custom_labels

def predict(texts : List, model, tokenizer, batch_size=8, max_len=64) -> tuple:
    # Prepare the dataset and dataloader
    dataset = InferenceDataset(texts, tokenizer, max_len)
    dataloader = DataLoader(dataset, batch_size=batch_size)

    model.eval()
    predictions = []
    probs = []

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"]
            attention_mask = batch["attention_mask"]

            # Move tensors to the same device as the model
            input_ids = input_ids.to(model.device)
            attention_mask = attention_mask.to(model.device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits

            # Get the argmax of logits along the last dimension
            batch_probs = torch.max(logits, dim=-1).values
            batch_predictions = torch.argmax(logits, dim=-1)
            predictions.extend(batch_predictions.cpu().numpy())
            probs.extend(batch_probs.cpu().numpy())

    return predictions, probs

def extract_entities_from_texts(texts : List, tokenized_inputs : dict, predictions_decoded : List) -> List:
    ''' maps the prediction from token level to character level, groups the same entities and returns the expected dictionary'''
    entity_list = []

    for text, tokenized_input, predictions in zip(texts, tokenized_inputs, predictions_decoded):
        entities = []
        offset_mapping = tokenized_input['offset_mapping'][0].tolist()

        current_entity = None
        current_start = None

        for idx, (prediction, offsets) in enumerate(zip(predictions, offset_mapping)):
            if offsets[0] == 0 and offsets[1] == 0:
                # Skip special tokens and padding
                continue
            
            entity_label = prediction[2:] if prediction.startswith(("B-", "I-")) else None
            start, end = offsets
            
            if entity_label:
                if current_entity is None:
                    # Start a new entity
                    current_entity = entity_label
                    current_start = start
                elif entity_label != current_entity:
                    # Store the previous entity
                    entities.append({
                        "entity": text[current_start:start],
                        "start_idx": current_start,
                        "end_idx": start,
                        "label": current_entity
                    })
                    # Start a new entity
                    current_entity = entity_label
                    current_start = start
            elif current_entity is not None:
                # store previous entity if current is "O"
                entities.append({
                    "entity": text[current_start:start],
                    "start_idx": current_start,
                    "end_idx": start,
                    "label": current_entity
                })
                current_entity = None

        # Handle remaining entity
        if current_entity is not None:
            entities.append({
                "entity": text[current_start:end],
                "start_idx": current_start,
                "end_idx": end,
                "label": current_entity
            })
        
        entity_list.append(entities)

    return entity_list

def infer_model(texts: List, model, tokenizer, custom_labels : dict, max_length=64):
    ''' Returns the entities for the given texts '''
    predictions, probs = predict(texts, model, tokenizer) # TODO: Handle probs
    tokenized_input = tokenizer(texts, 
                            is_split_into_words=False, 
                            padding='max_length', 
                            max_length=64, 
                            truncation=True,
                            return_tensors='pt',
                            return_offsets_mapping=True)
    
    predictions_decoded = [[custom_labels.get(pred, "O") for pred in prediction] for prediction in predictions]

    entities = extract_entities_from_texts(texts, [tokenized_input], predictions_decoded)
    return entities

def infer(texts, model_main, tokenizer_main, model_tuned, tokenizer_tuned, max_length=64):
    ''' Returns the entities for the given texts '''
    labels_main = get_labels_main()
    labels_tuned = get_labels_tuned()

    output_main = infer_model(texts, model_main, tokenizer_main, labels_main, max_length)
    output_tuned = infer_model(texts, model_tuned, tokenizer_tuned, labels_tuned, max_length)
    output_regex = [regex_ner(text) for text in texts]
    return {"main": output_main, "tuned": output_tuned, "regex": output_regex}