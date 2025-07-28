from src.search import SearchEngine

if __name__ == "__main__":
    print("=== Search Engine with Porter Stemming ===\n")
    
    # Create engines with and without stemming for comparison
    engine_with_stemming = SearchEngine(use_stemming=True)
    engine_without_stemming = SearchEngine(use_stemming=False)
    
    documents = {
        0: "Python is a great programming language for machine learning applications",
        1: "Machine learning algorithms require good data preprocessing techniques", 
        2: "Data science involves statistical analysis and programming skills",
        3: "Python libraries like numpy and pandas are essential for data analysis",
        4: "Programming requires logical thinking and problem solving abilities",
        5: "Learning new programming languages improves your coding skills"
    }
    
    # Add documents to both engines
    engine_with_stemming.add_documents(documents)
    engine_without_stemming.add_documents(documents)
    
    # Test queries that benefit from stemming
    test_queries = [
        "programming languages",
        "learning algorithms", 
        "data analysis"
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 40)
        
        print("With Porter Stemming:")
        results_stemmed = engine_with_stemming.search(query)
        for score, doc_id, content, _ in results_stemmed:
            print(f"  Score: {score:.4f} - Doc {doc_id}: {content}")
        
        print("\nWithout Stemming:")
        results_normal = engine_without_stemming.search(query)
        for score, doc_id, content, _ in results_normal:
            print(f"  Score: {score:.4f} - Doc {doc_id}: {content}")
        
        print(f"\nStemming found {len(results_stemmed)} results vs {len(results_normal)} without stemming")
        print("=" * 60 + "\n")