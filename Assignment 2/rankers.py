from pyserini.index import IndexReader, IndexTerm
from tqdm import tqdm, trange
import sys
import numpy as np

class Ranker(object):
    '''
    The base class for ranking functions. Specific ranking functions should
    extend the score() function, which returns the relevance of a particular 
    document for a given query.
    '''
    
    
    def __init__(self, index_reader):
        self.index_reader = index_reader
        self.documents = index_reader.stats()['documents']
        self.non_empty_documents = index_reader.stats()['non_empty_documents']
        self.convert_map = {}
        self.document_vector = {}
        self.term_positions = {}
        self.term_counts = {}
        self.total_length = 0

        for i in range(self.documents):
            doc_id = index_reader.convert_internal_docid_to_collection_docid(i)
            self.convert_map[i] = doc_id
            try:
                document_vector = index_reader.get_document_vector(doc_id)
                self.document_vector[doc_id] = document_vector
                self.term_positions[doc_id] = index_reader.get_term_positions(doc_id)
            except:
                pass

        for term in index_reader.terms():
            self.term_counts[term.term] = term.df
            self.total_length += len(term.term) * term.cf
        
    def score(query, doc):        
        '''
        Returns the score for how relevant this document is to the provided query.
        Query is a tokenized list of query terms and doc_id is the identifier
        of the document in the index should be scored for this query.
        '''
        
        rank_score = 0
        return rank_score


class PivotedLengthNormalizatinRanker(Ranker):
    
    def __init__(self, index_reader):
        super(PivotedLengthNormalizatinRanker, self).__init__(index_reader)

        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)


    def score(self, query, doc_id, b=0.3):
        '''
        Scores the relevance of the document for the provided query using the
        Pivoted Length Normalization ranking method. Query is a tokenized list
        of query terms and doc_id is a numeric identifier of which document in the
        index should be scored for this query.

        '''

        rank_score = 0
        
        ###########################YOUR CODE GOES HERE######################
        #
        # TODO: Implement Pivoted Length Normalization here. You'll want to use
        # the information in the self.index_reader. This object will let you
        # convert the the query and document into vector space representations,
        # as well as count how many times the term appears across all documents.
        #
        # IMPORTANT NOTE: We want to see the actual equation implemented
        # below. You cannot use any of Pyserini's built-in BM25-related code for
        # your solution. If in doubt, check with us.
        #        
        # For some hints, see the IndexReader documentation:
        # https://github.com/castorini/pyserini/blob/master/docs/usage-indexreader.md
        #
        ###########################END OF CODE#############################
        if not doc_id in self.document_vector:
            return 0

        avg_len = self.total_length / self.non_empty_documents
        tf = self.document_vector[doc_id]
        d_len = sum([tf[term] * len(term) for term in tf.keys()])
        analyzed = self.index_reader.analyze(query)
        unique = set(analyzed)
        for token in unique:
            qtf = analyzed.count(token)
            if token in tf:
                count = tf[token]
                df = self.term_counts[token]
                rank_score += qtf * (1 + np.log(1 + np.log(count))) / (1 - b + b * d_len / avg_len) * np.log((self.non_empty_documents + 1) / df)
        
        return rank_score

    

class BM25Ranker(Ranker):

    def __init__(self, index_reader):
        super(BM25Ranker, self).__init__(index_reader)

        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)

    def score(self, query, doc_id, k1=1.0, b=0.75, k3=20):
        '''
        Scores the relevance of the document for the provided query using the
        BM25 ranking method. Query is a tokenized list of query terms and doc_id
        is a numeric identifier of which document in the index should be scored
        for this query.
        '''

        rank_score = 0
        
        ###########################YOUR CODE GOES HERE######################
        #
        # TODO: Implement BM25 here (using the equation from the slides). You'll
        # want to use the information in the self.index_reader. This object will
        # let you convert the the query and document into vector space
        # representations, as well as count how many times the term appears
        # across all documents.
        #
        # IMPORTANT NOTE: We want to see the actual equation implemented
        # below. You cannot use any of Pyserini's built-in BM25-related code for
        # your solution. If in doubt, check with us.
        #
        # For some hints, see the IndexReader documentation:
        # https://github.com/castorini/pyserini/blob/master/docs/usage-indexreader.md
        #
        ###########################END OF CODE#############################
        if not doc_id in self.document_vector:
            return 0

        avg_len = self.total_length / self.non_empty_documents
        tf = self.document_vector[doc_id]
        d_len = sum([tf[term] * len(term) for term in tf.keys()])

        analyzed = self.index_reader.analyze(query)
        unique = set(analyzed)
        for token in unique:
            qtf = analyzed.count(token)
            if token in tf:
                count = tf[token]
                df = self.term_counts[token]
                rank_score += np.log((self.non_empty_documents - df + 0.5) / (df + 0.5)) * (((k1 + 1) * count) / (k1 * (1 - b + b * d_len / avg_len) + count)) * (((k3 + 1) * qtf) / (k3 + qtf))

        return rank_score


    
class CustomRanker(Ranker):
    
    def __init__(self, index_reader):
        super(CustomRanker, self).__init__(index_reader)

        # NOTE: the reader is stored as a field of the subclass and you can
        # compute and cache any intermediate data in the constructor to save for
        # later (HINT: Which values in the ranking are constant across queries
        # and documents?)


    def score(self, query, doc_id, k1=1.2, b=0.75, k3=7):
        '''
        Scores the relevance of the document for the provided query using a
        custom ranking method. Query is a tokenized list of query terms and doc_id
        is a numeric identifier of which document in the index should be scored
        for this query.
        '''

        rank_score = 0
        
        ###########################YOUR CODE GOES HERE######################
        #
        # TODO: Implement your custome ranking function here. You'll want to use
        # the information in the self.index_reader. This object will let you
        # convert the the query and document into vector space representations,
        # as well as count how many times the term appears across all documents.
        #
        # IMPORTANT NOTE: We want to see the actual equation implemented
        # below. You cannot use any of Pyserini's built-in BM25-related code for
        # your solution. If in doubt, check with us.
        #
        # For some hints, see the IndexReader documentation:
        # https://github.com/castorini/pyserini/blob/master/docs/usage-indexreader.md
        #
        ###########################END OF CODE#############################
        if not doc_id in self.document_vector:
            return 0

        avg_len = self.total_length / self.non_empty_documents
        tf = self.document_vector[doc_id]
        d_len = sum([tf[term] * len(term) for term in tf.keys()])

        analyzed = self.index_reader.analyze(query)
        unique = set(analyzed)
        for token in unique:
            qtf = analyzed.count(token)
            if token in tf:
                count = tf[token]
                df = self.term_counts[token]

                left_dist = np.inf
                right_dist = np.inf
                pos = self.term_positions[doc_id][token]
                index = analyzed.index(token) - 1
                while index >= 0:
                    if analyzed[index] != token and analyzed[index] in tf:
                        left_token = analyzed[index]
                        left_pos = self.term_positions[doc_id][left_token]
                        left_dist = np.mean([np.mean([np.abs(x - y) for y in left_pos]) for x in pos])
                        break
                    index -= 1
                index = analyzed.index(token) + 1
                while index < len(analyzed):
                    if analyzed[index] != token and analyzed[index] in tf:
                        right_token = analyzed[index]
                        right_pos = self.term_positions[doc_id][right_token]
                        right_dist = np.mean([np.mean([np.abs(x - y) for y in right_pos]) for x in pos])
                        break
                    index += 1
                dist = min(left_dist, right_dist)

                rank_score += (1 / (dist + 1) + 1) * np.log((self.non_empty_documents + 1) / df) * (((k1 + 1) * count) / (k1 * (1 - b + b * d_len / avg_len) + count)) * np.log(((k3 + 1) * qtf) / (k3 + qtf) + 1)
        
        return rank_score
