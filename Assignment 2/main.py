from rankers import PivotedLengthNormalizatinRanker, BM25Ranker, CustomRanker
from pyserini.index import IndexReader, IndexTerm
from tqdm import tqdm, trange
import sys

def run_test(ranker):
    '''
    Prints the relevance scores of the top retrieved documents.
    '''
    scores = []
    print(query_id + ': ' + query)
    for i in range(ranker.documents):
        doc_id = (ranker.convert_map)[i]
        score = ranker.score(query, doc_id)
        scores.append((doc_id, score))

    scores.sort(reverse=True, key=lambda x: x[1])

    for i in range(5):
        output_file.write(query_id + ',' + scores[i][0] + '\n')


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("usage: python algorthm_test.py path/to/index_file path/to/query_file ranking_function")
        exit(1)

    # NOTE: You should already have used pyserini to generate the index files
    # before calling main
    index_fname = sys.argv[1]
    index_reader = IndexReader(index_fname)  # Reading the indexes

    # Choose which ranker class you want to use
    if sys.argv[3] == 'Pivoted':
        ranker = PivotedLengthNormalizatinRanker(index_reader)
    elif sys.argv[3] == 'BM25':
        ranker = BM25Ranker(index_reader)
    elif sys.argv[3] == 'Custom':
        ranker = CustomRanker(index_reader)
    else:
        print("ranking_function: one of the following {Pivoted, BM25, Custom}")
        exit(1)

    # Read the queries
    with open(sys.argv[2], 'r', newline='') as query_file, open('output.csv', 'w') as output_file:
        output_file.write('QueryId,DocumentId\n')
        while True:
            line = query_file.readline()
            if not line:
                break
            line = line.replace('\n', '')
            row = line.split('\t')
            query_id = row[0]
            query = row[1]
            run_test(ranker)
