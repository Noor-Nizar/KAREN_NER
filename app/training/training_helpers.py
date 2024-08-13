from transformers import EvalPrediction
from sklearn.metrics import classification_report

from app.inference import get_labels_tuned

def compute_metrics(p: EvalPrediction):
    predictions, labels = p.predictions, p.label_ids
    predictions = predictions.argmax(axis=-1)
    
    # Flatten the sequences for classification_report
    true_labels = [label for doc in labels for label in doc if label != -100]
    pred_labels = [pred for doc, true_doc in zip(predictions, labels) for pred, true in zip(doc, true_doc) if true != -100]
    
    report = classification_report(true_labels, pred_labels, labels=list(get_labels_tuned().keys()), target_names=list(get_labels_tuned().values()), output_dict=True, zero_division=0)
    
    # Return the metrics of interest
    return {
        'precision': report['macro avg']['precision'],
        'recall': report['macro avg']['recall'],
        'f1': report['macro avg']['f1-score']
    }

def compute_metrics_2(p: EvalPrediction):
    predictions, labels = p.predictions, p.label_ids
    predictions = predictions.argmax(axis=-1)
    
    # Flatten the sequences for classification_report
    true_labels = [label for doc in labels for label in doc if label != -100]
    pred_labels = [pred for doc, true_doc in zip(predictions, labels) for pred, true in zip(doc, true_doc) if true != -100]

    report = classification_report(true_labels, pred_labels, labels=list(get_labels_tuned().keys()), target_names=list(get_labels_tuned().values()), output_dict=False, zero_division=0)
    
    print(report)
    # Return the metrics of interest
    return {"done": 1}