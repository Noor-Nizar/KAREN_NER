from transformers import Trainer, TrainingArguments
import torch

from sklearn.utils import shuffle

from app.data.lbox_handler import process_labelbox_data
from app.data.data_helpers import load_data, tokenize_and_align_labels, create_label_mappings, convert_labels_to_ids
from app.datasets import TokenizedDataset
from app.training.training_helpers import compute_metrics, compute_metrics_2


def prepare_data(tokenizer, re_process=False, train_size=128):
    if re_process:
        process_labelbox_data()

    X, y = load_data('data/processed.txt')
    X, y = shuffle(X, y, random_state=42)

    label_to_id, id_to_label = create_label_mappings(y)

    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    X_train_tokenized, y_train_tokenized = tokenize_and_align_labels(X_train, y_train, tokenizer)
    X_test_tokenized, y_test_tokenized = tokenize_and_align_labels(X_test, y_test, tokenizer)

    y_train_ids = convert_labels_to_ids(y_train_tokenized, label_to_id)
    y_test_ids = convert_labels_to_ids(y_test_tokenized, label_to_id)

    train_dataset = TokenizedDataset(X_train_tokenized, y_train_ids)
    test_dataset = TokenizedDataset(X_test_tokenized, y_test_ids)

    return train_dataset, test_dataset, label_to_id, id_to_label

def get_trainer(model, train_dataset, test_dataset, cuda=True, batch_size=16, compute_metrics=compute_metrics):
    if not cuda: ## incase of running on mac it defaults on mps which is problematic -> set to cpu
        model = model.to('cpu')

    training_args = TrainingArguments(
        output_dir='./results',
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=50,
        weight_decay=0.01,
        logging_steps=10,
        eval_steps=10,
        logging_dir='./logs',
        no_cuda=not cuda,
        load_best_model_at_end = True,
        metric_for_best_model = 'eval_f1',
        save_strategy = "epoch",
        save_total_limit=1,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )

    return trainer

def train_model(model, train_dataset, test_dataset):
    trainer = get_trainer(model, train_dataset, test_dataset)
    trainer.train()

    return trainer.model

def prepare_and_train_model(model, re_process=False, train_size=128):
    train_dataset, test_dataset, label_to_id, id_to_label = prepare_data(re_process, train_size)
    trained_model = train_model(model, train_dataset, test_dataset)

    return trained_model, label_to_id, id_to_label





