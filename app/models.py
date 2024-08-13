from transformers import AutoTokenizer, AutoModelForTokenClassification

def get_tuning_model(freeze_layers: int = 6, path: str = None):
    '''
    Returns the model for fine-tuning
    '''
    model_name = "hatmimoha/arabic-ner"

    if path:
        model_name = path
    
    # Load the model and tokenizer
    model = AutoModelForTokenClassification.from_pretrained(model_name)

    # Freeze the first 6 layers
    for param in model.bert.encoder.layer[:freeze_layers].parameters():
        param.requires_grad = False
    
    return model

def get_tuning_tokenizer():
    '''
    Returns the tokenizer for fine-tuning
    '''
    model_name = "hatmimoha/arabic-ner"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer

def get_model():
    ''' Returns the model for inference '''
    custom_labels = ["O", "B-job", "I-job", "B-nationality", "B-person", "I-person", "B-location","B-time", "I-time", "B-event", "I-event", "B-organization", "I-organization", "I-location", "I-nationality", "B-product", "I-product", "B-artwork", "I-artwork"]

    model_cp = "marefa-nlp/marefa-ner"
    model_main = AutoModelForTokenClassification.from_pretrained(model_cp, num_labels=len(custom_labels))
    return model_main

def get_tokenizer():
    ''' Returns the tokenizer for inference '''
    model_cp = "marefa-nlp/marefa-ner"
    tokenizer_main = AutoTokenizer.from_pretrained(model_cp)
    return tokenizer_main
