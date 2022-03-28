import json
import csv
from pyserini.search import SimpleSearcher
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("usage: python generator.py path/to/raw_dataset path/to/queries (optional)path/to/sample")
        exit(1)
    
    document_path = sys.argv[1]
    filename = 'integrations/Android/collection/document.jsonl'
    with open(document_path, 'r', newline='') as file, open(filename, 'w') as json_file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            docid = row['DocumentId']
            title = row['Document Title']
            description = row['Document Description']
            if title == 'Unknown':
                title = ''
            if description == 'Unknown':
                description = ''
            doc_json = {"id": docid, "contents": title + ". " + title + ". " + description}
            json_str = json.dumps(doc_json)
            json_file.write(json_str + '\n')

    sample_query_id = []
    if len(sys.argv) == 4:
        sample_path = sys.argv[3]
        with open(sample_path, 'r', newline='') as file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                if not row['QueryId'] in sample_query_id:
                    sample_query_id.append(row['QueryId'])

    if len(sys.argv) == 3:
        query_path = sys.argv[2]
        filename = 'integrations/Android/query.tsv'
        with open(query_path, 'r', newline='') as file, open(filename, 'w') as tsv_file:
            csvreader = csv.DictReader(file)
            for row in csvreader:
                queryid = row['QueryId']
                description = row['Query Description']
                tsv_str = queryid + '\t' + description
                tsv_file.write(tsv_str + '\n')

    if len(sys.argv) == 4:
        query_path = sys.argv[2]
        filename = 'integrations/Android/query.tsv'
        with open(filename, 'w') as tsv_file:
            for target_id in sample_query_id:
                with open(query_path, 'r', newline='') as file:
                    csvreader = csv.DictReader(file)
                    for row in csvreader:
                        if row['QueryId'] == target_id:
                            description = row['Query Description']
                            tsv_str = target_id + '\t' + description
                            tsv_file.write(tsv_str + '\n')