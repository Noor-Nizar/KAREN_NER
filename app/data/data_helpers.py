from app.logger import logger
from typing import List

def load_data(file_path):
    '''loades preprocessed data in format of word entity mapping'''
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read().split('\n\n')  # Split sentences
    sentences = []
    labels = []
    for item in data:
        words = []
        tags = []
        lines = item.splitlines()
        for line in lines:
            if line:
                word, tag = line.split()
                words.append(word)
                tags.append(tag)
        sentences.append(words)
        labels.append(tags)
    return sentences, labels

def tokenize_and_align_labels(sentences, labels, tokenizer, max_length:int=None):
    '''
    Because the tokenization may split the words into subwords we need to align the labels with the tokenized inputs.
    This function tokenizes the input sentences and aligns the labels with the tokenized inputs.
    Returned tokenized_inputs and tokenized_labels are lists of dictionaries with the keys 'input_ids', 'attention_mask'.
    Returned tokenized_labels IS A PADDED LIST OF STRINGS/ENTITIES
    '''

    if max_length is None:
        logger.warning('max_length is None, setting it to 64')
        max_length = 64
    
    tokenized_inputs = []
    tokenized_labels = []
    
    for sentence, label in zip(sentences, labels):
        # Tokenize the input sentence with word-level tokenization
        tokenized_input = tokenizer(sentence, 
                                    is_split_into_words=True,  ## Assuming the input is already split into words
                                    padding='max_length', 
                                    max_length=max_length,
                                    truncation=True,
                                    return_tensors='pt')

        word_ids = tokenized_input.word_ids()  # Map tokens back to their word index
        label_ids = []
        
        previous_word_idx = None

        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # Special tokens or padding tokens
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])  # Take the original label
            else:
                label_ids.append(label[word_idx].replace('B-', 'I-'))  # TODO : Currently align subwords with 'I-', Needs more research to check if this is the optimal way
            
            previous_word_idx = word_idx

        tokenized_inputs.append(tokenized_input)
        tokenized_labels.append(label_ids)

    return tokenized_inputs, tokenized_labels

def create_label_mappings(labels):
    '''
    creates label to id and id to label mappings
    '''
    unique_labels = list(set(label for sublist in labels for label in sublist))
    unique_labels = sorted(unique_labels)
    label_to_id = {label: i for i, label in enumerate(unique_labels)}
    id_to_label = {i: label for label, i in label_to_id.items()}
    return label_to_id, id_to_label

def convert_labels_to_ids(labels, label_to_id):
    return [[label_to_id.get(label, -100) for label in sublist] for sublist in labels]