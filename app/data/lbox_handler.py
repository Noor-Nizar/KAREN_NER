import json
import os

from app.logger import logger


def process_labelbox_data(project_id: str = '1'):
    '''
    Looks for exported annotations at data/FineTune.ndjson
    and the original samples in the format of .txt file / row  at data/sentences/ 
    and writes the processed data to data/processed_data.txt which is a word entity mapping txt file
    '''

    # File paths
    labelbox_file = 'data/box_annots.ndjson'
    sentences_dir = 'data/sentences/'
    output_file = 'data/processed.txt'

    output_lines = []

    with open(labelbox_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            
            external_id = data['data_row']['external_id']
            sentence_file_path = os.path.join(sentences_dir, external_id)
            
            with open(sentence_file_path, 'r') as f_sentence:
                sentence = f_sentence.read().strip()
            
            annotations = data['projects'][project_id]['labels'][0]['annotations']['objects']

            words = sentence.split()
            
            word_annotations = ['O'] * len(words)  # Default label is 'O' (Outside)
            
            # Map character-level annotations to word-level annotations
            current_char_idx = 0
            for i, word in enumerate(words):
                word_start_idx = current_char_idx
                word_end_idx = current_char_idx + len(word) - 1
                
                # Check if the word is part of an annotation
                for annotation in annotations:
                    start_idx = annotation['location']['start']
                    end_idx = annotation['location']['end']
                    entity = annotation['name']
                    
                    if word_end_idx >= start_idx and word_start_idx <= end_idx:
                        if word_start_idx == start_idx:
                            word_annotations[i] = f'B-{entity}'
                        else:
                            word_annotations[i] = f'I-{entity}'
                
                # Move to the next word
                current_char_idx += len(word) + 1  # +1 for the space
            
            # Create the final output for this sentence
            for word, annotation in zip(words, word_annotations):
                output_lines.append(f"{word}\t{annotation}")
            
            # Add a blank line to separate examples in the output file
            output_lines.append("")
    
    # Write all processed data to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))

    print(f"Processed data saved to {output_file}")