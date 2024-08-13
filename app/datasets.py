from torch.utils.data import Dataset
import torch

class TokenizedDataset(Dataset):
    '''used in the training pipeline'''
    def __init__(self, X_tokenized, y_labels):
        self.input_ids = [item['input_ids'].squeeze(0) for item in X_tokenized]
        self.token_type_ids = [item['token_type_ids'].squeeze(0) for item in X_tokenized]
        self.attention_mask = [item['attention_mask'].squeeze(0) for item in X_tokenized]
        self.labels = [torch.tensor(label) for label in y_labels]

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx],
            'token_type_ids': self.token_type_ids[idx],
            'attention_mask': self.attention_mask[idx],
            'labels': self.labels[idx]
        }
    
class InferenceDataset(Dataset):
    '''used in the inference pipeline'''
    def __init__(self, texts, tokenizer, max_len=64):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer(text.split(), is_split_into_words=True, 
                                  padding='max_length', truncation=True, 
                                  max_length=self.max_len, return_tensors="pt")
        
        # Squeeze to remove the batch dimension (which is 1)
        input_ids = encoding["input_ids"].squeeze()
        attention_mask = encoding["attention_mask"].squeeze()
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }