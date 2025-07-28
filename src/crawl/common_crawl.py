import requests
import json
import gzip
import re
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.in_script = False
        self.in_style = False
    
    def handle_starttag(self, tag, attrs):
        if tag.lower() in ['script', 'style']:
            if tag.lower() == 'script':
                self.in_script = True
            elif tag.lower() == 'style':
                self.in_style = True
    
    def handle_endtag(self, tag):
        if tag.lower() == 'script':
            self.in_script = False
        elif tag.lower() == 'style':
            self.in_style = False
    
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            text = data.strip()
            if text:
                self.text_content.append(text)
    
    def get_text(self):
        return ' '.join(self.text_content)


class CommonCrawlClient:
    def __init__(self):
        self.base_url = "https://index.commoncrawl.org"
        self.cdx_api_url = f"{self.base_url}/CC-MAIN-2025-30-index"
        
    def search_urls(self, domain, limit=10):
        """Search for URLs from a specific domain in Common Crawl"""
        params = {
            'url': f"{domain}/*",
            'output': 'json',
            'limit': limit
        }
        
        try:
            response = requests.get(self.cdx_api_url, params=params, timeout=10)
            response.raise_for_status()
            
            results = []
            for line in response.text.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        results.append({
                            'url': data.get('url', ''),
                            'timestamp': data.get('timestamp', ''),
                            'filename': data.get('filename', ''),
                            'offset': data.get('offset', ''),
                            'length': data.get('length', '')
                        })
                    except json.JSONDecodeError:
                        continue
            
            return results
        except requests.RequestException as e:
            print(f"Error searching Common Crawl: {e}")
            return []
    
    def fetch_document(self, filename, offset, length):
        """Fetch a specific document from Common Crawl"""
        if not all([filename, offset, length]):
            return None
            
        archive_url = f"https://data.commoncrawl.org/{filename}"
        headers = {
            'Range': f'bytes={offset}-{int(offset) + int(length) - 1}'
        }
        
        try:
            response = requests.get(archive_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Decompress gzip content
            content = gzip.decompress(response.content).decode('utf-8', errors='ignore')
            
            # Extract HTML content from WARC record
            html_content = self._extract_html_from_warc(content)
            return html_content
            
        except (requests.RequestException, gzip.BadGzipFile, UnicodeDecodeError) as e:
            print(f"Error fetching document: {e}")
            return None
    
    def _extract_html_from_warc(self, warc_content):
        """Extract HTML content from WARC record"""
        # Find the HTML content after HTTP headers
        html_start = warc_content.find('\r\n\r\n')
        if html_start == -1:
            html_start = warc_content.find('\n\n')
        
        if html_start != -1:
            # Skip the HTTP headers
            html_content = warc_content[html_start + 4:]
            # Remove any remaining HTTP headers that might be present
            html_start = html_content.find('<')
            if html_start != -1:
                return html_content[html_start:]
        
        return warc_content
    
    def extract_text_from_html(self, html_content):
        """Extract clean text from HTML content"""
        if not html_content:
            return ""
        
        # Create parser instance
        parser = HTMLTextExtractor()
        
        try:
            parser.feed(html_content)
            text = parser.get_text()
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
            text = text.strip()
            
            return text
        except Exception as e:
            print(f"Error extracting text from HTML: {e}")
            return ""
    
    def get_documents(self, domains, max_docs_per_domain=5):
        """Fetch and process documents from multiple domains"""
        documents = {}
        doc_id = 0
        
        for domain in domains:
            print(f"Searching {domain}...")
            search_results = self.search_urls(domain, limit=max_docs_per_domain * 2)
            processed = 0
            for result in search_results:
                if processed >= max_docs_per_domain:
                    break
                print(f"Fetching {result['url']}...")
                html_content = self.fetch_document(
                    result['filename'], 
                    result['offset'], 
                    result['length']
                )
                
                if html_content:
                    text_content = self.extract_text_from_html(html_content)
                    
                    if text_content and len(text_content) > 100:  # Only keep substantial content
                        documents[doc_id] = {
                            'url': result['url'],
                            'content': text_content,
                            'domain': domain,
                            'timestamp': result['timestamp']
                        }
                        doc_id += 1
                        processed += 1
                        print(f"✓ Processed document {doc_id-1}: {len(text_content)} characters")
                    else:
                        print("✗ Document too short or empty")
                else:
                    print("✗ Failed to fetch document")
        
        return documents
    
    def get_sample_documents(self):
        """Get sample documents from popular domains for testing"""
        sample_domains = [
            "en.wikipedia.org",
            "stackoverflow.com", 
            "github.com"
        ]
        
        return self.get_documents(sample_domains, max_docs_per_domain=2)