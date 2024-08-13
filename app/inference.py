import torch
from torch.utils.data import DataLoader

from app.datasets import InferenceDataset
from app.data.data_helpers import decode_and_align_labels, decode_and_align_labels_main
from app.regex_finders import regex_ner

def get_labels_tuned():
    # FIXME : update this automatically
    return {0: 'B-Age', 1: 'B-Colors', 2: 'B-Currency', 3: 'B-Dates', 4: 'B-Prices', 5: 'B-Quantity', 6: 'B-Times', 7: 'B-Units', 8: 'I-Age', 9: 'I-Currency', 10: 'I-Dates', 11: 'I-Prices', 12: 'I-Quantity', 13: 'I-Times', 14: 'I-Units', 15: 'O'}
def get_labels_main():
    ''' Returns the labels for inference '''
    custom_labels = ["O", "B-job", "I-job", "B-nationality", "B-person", "I-person", "B-location","B-time", "I-time", "B-event", "I-event", "B-organization", "I-organization", "I-location", "I-nationality", "B-product", "I-product", "B-artwork", "I-artwork"]
    return custom_labels

def predict(texts, model, tokenizer, batch_size=8, max_len=64):
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

def get_word2entity(ent_dec, text):
    '''entity decoded, text'''
    temp_dict = {}
    for i, entity in enumerate(ent_dec):
        if entity == "O":
            continue
        temp_dict.update({text[i]: {"index": i, "entity":entity}})
    return temp_dict

def merge_(w2e: dict) -> dict:
    '''
    sample input : {'5': {'index': 5, 'entity': 'B-time'}, 'AM': {'index': 6, 'entity': 'I-time'}}
    sample output : {'5 AM': {'index': [5, 6], 'entity': 'time'}}
    '''
    merged_dict = {}
    temp_word = None
    temp_indices = []
    temp_entity = None

    # Sort to ensure correct order
    sorted_items = sorted(w2e.items(), key=lambda x: x[1]['index'])

    for word, info in sorted_items:
        entity_type = info['entity'].split('-')[1]

        if temp_word is None:
            # first word or no ongoing merge
            temp_word = word
            temp_indices = [info['index']]
            temp_entity = entity_type
        elif temp_entity == entity_type and info['entity'].startswith('I-'):
            # Continuation of the same entity
            temp_word += f" {word}"
            temp_indices.append(info['index'])
        else:
            # different entity or a new 'B-' tag, save the previous merge
            merged_dict[temp_word] = {"index": temp_indices, "entity": temp_entity}
            temp_word = word
            temp_indices = [info['index']]
            temp_entity = entity_type

    # add the last merged entity
    if temp_word:
        merged_dict[temp_word] = {"index": temp_indices, "entity": temp_entity}

    return merged_dict


def infer_main(texts, model, tokenizer, max_length=64):
    ''' Returns the entities for the given texts '''
    custom_labels = get_labels_main()
    predictions, probs = predict(texts, model, tokenizer) # TODO: Handle probs
    tokenized_input = [tokenizer(text, 
                                    is_split_into_words=False, 
                                    padding='max_length', 
                                    max_length=max_length, 
                                    truncation=True,
                                    return_tensors='pt') for text in texts]
    
    texts_aln, predictions_aln = decode_and_align_labels_main(tokenized_input, predictions, tokenizer)
    output = []
    for i, prediction in enumerate(predictions_aln):
        ent_dec = [custom_labels[pred] for pred in prediction]
        w2e = get_word2entity(ent_dec, texts_aln[i])
        merged = merge_(w2e)
        output.append(merged)

    return output

def infer_tuned(texts, model, tokenizer, max_length=64):
    ''' Returns the entities for the given texts '''
    custom_labels = get_labels_tuned()
    predictions, probs = predict(texts, model, tokenizer) # TODO: Handle probs
    tokenized_input = [tokenizer(text, 
                                    is_split_into_words=False, 
                                    padding='max_length', 
                                    max_length=max_length, 
                                    truncation=True,
                                    return_tensors='pt') for text in texts]
    
    texts_aln, predictions_aln = decode_and_align_labels(tokenized_input, predictions, tokenizer)
    output = []
    for i, prediction in enumerate(predictions_aln):
        ent_dec = [custom_labels[pred] for pred in prediction]
        w2e = get_word2entity(ent_dec, texts_aln[i])
        merged = merge_(w2e)
        output.append(merged)

    return output


def infer(texts, model_main, tokenizer_main, model_tuned, tokenizer_tuned, max_length=64):
    ''' Returns the entities for the given texts '''
    output_main = infer_main(texts, model_main, tokenizer_main, max_length)
    output_tuned = infer_tuned(texts, model_tuned, tokenizer_tuned, max_length)
    output_regex = [regex_ner(text) for text in texts]
    return {"main": output_main, "tuned": output_tuned, "regex": output_regex}