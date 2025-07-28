# Python Search Engine

A lightweight, POC, vector-based search engine implementation with Porter stemming algorithm for improved text preprocessing and search accuracy. This simple project implements the idea from [https://ondoc.logand.com/d/2697/pdf](Basic Vector Space Search Engine Theory).

## Features

- **Vector Search**: Implements cosine similarity-based document ranking
- **Porter Stemming**: Reduces words to their root forms to improve matching (e.g., "running" → "run")
- **Common Crawl Integration**: Fetches real web documents from Common Crawl archive
- **HTML Text Extraction**: Strips HTML tags and extracts clean text content
- **Modular Design**: Separate classes for different functionalities
- **Flexible API**: Can be used with or without stemming

## Project Structure

```
py-search-engine/
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   └── porter_stemming.py    # Porter stemming algorithm
│   ├── crawl/
│   │   ├── __init__.py
│   │   └── common_crawl.py       # Common Crawl client and HTML processing
│   └── search/
│       ├── __init__.py
│       └── vector_search.py      # Vector search and search engine
├── example.py                    # Basic usage examples
├── example_crawl.py              # Common Crawl integration example
├── hello.py                      # Simple hello world
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd py-search-engine
```

2. Ensure Python 3.x is installed:

```bash
python --version
```

3. Install required dependencies:

```bash
pip install requests
```

## Usage

### Basic Usage

```python
from src.search import SearchEngine

# Create a search engine with stemming (default)
engine = SearchEngine(use_stemming=True)

# Add documents
documents = {
    0: "Python is a great programming language",
    1: "Machine learning algorithms require good data",
    2: "Data science involves programming skills"
}
engine.add_documents(documents)

# Search
results = engine.search("programming")
for score, doc_id, content in results:
    print(f"Score: {score:.4f} - {content}")
```

### Without Stemming

```python
# Create engine without stemming
engine = SearchEngine(use_stemming=False)
```

### Run the Examples

**Basic example with static data:**

```bash
python example.py
```

**Common Crawl example with real web documents:**

```bash
python example_crawl.py
```

The basic example demonstrates the difference between search results with and without Porter stemming. The Common Crawl example fetches real web documents and shows how to search through them.

## How It Works

### Vector Search Algorithm

1. **Document Processing**: Each document is converted to a concordance (word frequency map)
2. **Vector Representation**: Documents and queries are represented as vectors in word space
3. **Similarity Calculation**: Uses cosine similarity to rank document relevance
4. **Ranking**: Results are sorted by relevance score (higher = more relevant)

### Porter Stemming Algorithm

The Porter stemming algorithm reduces inflected words to their root form through a series of rule-based transformations:

- **Step 1**: Handle plurals and past participles (e.g., "cats" → "cat", "running" → "run")
- **Step 2**: Handle double consonants and ly-endings
- **Step 3**: Handle various suffixes
- **Step 4**: Remove suffixes in longer words
- **Step 5**: Clean up remaining suffixes

### Benefits of Stemming

- **Improved Recall**: Matches variations of words (e.g., "run", "running", "runs")
- **Reduced Index Size**: Fewer unique terms in the index
- **Better Semantic Matching**: Focuses on word roots rather than exact forms

## Classes

### `VectorSearch`

Core vector operations for document similarity.

**Methods:**

- `magnitude(concordance)`: Calculate vector magnitude
- `relation(concordance1, concordance2)`: Calculate cosine similarity
- `concordance(document, use_stemming, stemmer)`: Create word frequency map

### `SearchEngine`

High-level interface for document management and search.

**Methods:**

- `add_document(doc_id, content)`: Add single document
- `add_documents(documents_dict)`: Add multiple documents
- `add_crawl_documents(crawl_documents)`: Add documents from CommonCrawlClient
- `search(query, max_results)`: Search and return ranked results

### `PorterStemmer`

Implementation of the Porter stemming algorithm.

**Methods:**

- `stem(word)`: Reduce word to its root form

### `CommonCrawlClient`

Fetches and processes web documents from Common Crawl archive.

**Methods:**

- `search_urls(domain, limit)`: Search for URLs from a specific domain
- `fetch_document(filename, offset, length)`: Fetch a specific document
- `extract_text_from_html(html_content)`: Extract clean text from HTML
- `get_documents(domains, max_docs_per_domain)`: Fetch documents from multiple domains
- `get_sample_documents()`: Get sample documents for testing

## Performance Benefits

Using Porter stemming provides several computational advantages:

1. **Reduced Vocabulary**: Fewer unique terms to process
2. **Better Matching**: Related word forms are treated as equivalent
3. **Smaller Index**: Less memory usage for large document collections
4. **Improved Precision**: More focused search results

## Example Output

```
Query: 'programming languages'
----------------------------------------
With Porter Stemming:
  Score: 0.2357 - Doc 0: Python is a great programming language for machine learning applications
  Score: 0.1543 - Doc 5: Learning new programming languages improves your coding skills

Without Stemming:
  Score: 0.0000 - (no matches found)

Stemming found 2 results vs 0 without stemming
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Feel free to use and modify as needed.
