from src.search import SearchEngine
from src.crawl import CommonCrawlClient

def main():
    print("=== Python Search Engine with Common Crawl Data ===\n")
    
    # Initialize Common Crawl client
    print("Initializing Common Crawl client...")
    crawl_client = CommonCrawlClient()
    
    # Fetch sample documents from Common Crawl
    print("Fetching documents from Common Crawl...")
    print("This may take a few minutes as we're downloading from the web...\n")
    
    try:
        # Get sample documents
        crawl_documents = crawl_client.get_sample_documents()
        
        if not crawl_documents:
            print("No documents retrieved from Common Crawl. Using fallback data.")
            crawl_documents = {
                0: {
                    'content': "Python is a high-level programming language known for its simplicity and readability",
                    'url': "example.com/python",
                    'domain': "example.com"
                },
                1: {
                    'content': "Machine learning algorithms help computers learn patterns from data without explicit programming",
                    'url': "example.com/ml", 
                    'domain': "example.com"
                }
            }
        
        print(f"Successfully retrieved {len(crawl_documents)} documents\n")
 
        engine = SearchEngine(use_stemming=True)
        
        print("Indexing documents...")
        engine.add_crawl_documents(crawl_documents)
        
        print("\\nIndexed Documents:")
        print("-" * 50)
        for doc_id, doc_data in crawl_documents.items():
            if isinstance(doc_data, dict):
                content_preview = doc_data['content'][:100] + "..." if len(doc_data['content']) > 100 else doc_data['content']
                print(f"Doc {doc_id}: {doc_data.get('url', 'Unknown URL')}")
                print(f"  Domain: {doc_data.get('domain', 'Unknown')}")
                print(f"  Preview: {content_preview}")
                print()
        
        # Test queries
        test_queries = [
            "python programming",
            "machine learning",
            "data science",
            "algorithm"
        ]
        
        print("\\n" + "="*60)
        print("SEARCH RESULTS")
        print("="*60)
        
        for query in test_queries:
            print(f"\\nQuery: '{query}'")
            print("-" * 40)
            
            results = engine.search(query, max_results=5)
            
            if results:
                for i, (score, doc_id, content, doc_data) in enumerate(results, 1):
                    print(f"{i}. Score: {score:.4f}")
                    if isinstance(doc_data, dict):
                        print(f"   URL: {doc_data.get('url', 'Unknown')}")
                        print(f"   Domain: {doc_data.get('domain', 'Unknown')}")
                    
                    # Show content preview
                    content_preview = content[:200] + "..." if len(content) > 200 else content
                    print(f"   Content: {content_preview}")
                    print()
            else:
                print("   No matches found.")
        
        print("\\n" + "="*60)
        print("Search completed successfully!")
        
    except Exception as e:
        print(f"Error during Common Crawl operation: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()