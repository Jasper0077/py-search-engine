import math
from ..algorithms.porter_stemming import PorterStemmer

class VectorSearch:
    def magnitude(self, concordance):
        total = 0
        for count in concordance.values():
            total += count ** 2
        return math.sqrt(total)
    
    def relation(self, concordance1, concordance2):
        relevance, topval = 0, 0
        for word, count in concordance1.items():
            if word in concordance2:
                topval += count * concordance2[word]
        
        magnitude_product = self.magnitude(concordance1) * self.magnitude(concordance2)
        if magnitude_product != 0:
            relevance = topval / magnitude_product
        return relevance
    
    def concordance(self, document, use_stemming=False, stemmer=None):
        if type(document) != str:
            raise ValueError('Supplied Argument should be of type string')
        con = {}
        for word in document.split(' '):
            if use_stemming and stemmer:
                word = stemmer.stem(word)
            if word in con:
                con[word] += 1
            else:
                con[word] = 1
        return con


class SearchEngine:
    def __init__(self, use_stemming=True):
        self.vector_search = VectorSearch()
        self.documents = {}
        self.index = {}
        self.use_stemming = use_stemming
        self.stemmer = PorterStemmer() if use_stemming else None
    
    def add_crawl_documents(self, crawl_documents):
        """Add documents from CommonCrawlClient format"""
        for doc_id, doc_data in crawl_documents.items():
            content = doc_data.get('content', '')
            if content:
                self.add_document(doc_id, content)
                # Store additional metadata
                self.documents[doc_id] = {
                    'content': content,
                    'url': doc_data.get('url', ''),
                    'domain': doc_data.get('domain', ''),
                    'timestamp': doc_data.get('timestamp', '')
                }
    
    def add_document(self, doc_id, content):
        if not isinstance(self.documents.get(doc_id), dict):
            self.documents[doc_id] = content
        self.index[doc_id] = self.vector_search.concordance(
            content.lower(), self.use_stemming, self.stemmer
        )
    
    def add_documents(self, documents_dict):
        for doc_id, content in documents_dict.items():
            self.add_document(doc_id, content)
    
    def search(self, query, max_results=None):
        query_concordance = self.vector_search.concordance(
            query.lower(), self.use_stemming, self.stemmer
        )
        matches = []
        
        for doc_id in self.index:
            relation = self.vector_search.relation(query_concordance, self.index[doc_id])
            if relation != 0:
                doc_data = self.documents[doc_id]
                if isinstance(doc_data, dict):
                    content = doc_data['content']
                else:
                    content = doc_data
                matches.append((relation, doc_id, content, doc_data))
        
        matches.sort(reverse=True)
        
        if max_results:
            matches = matches[:max_results]
        
        return matches