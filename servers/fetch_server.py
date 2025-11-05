#!/usr/bin/env python3
"""
MCP Fetch Server - Official MCP Server Integration

Based on the official MCP Fetch server from:
https://github.com/modelcontextprotocol/servers/tree/main/src/fetch

This server provides web content fetching capabilities following the
Model Context Protocol specification.

Author: Official MCP Implementation (adapted)
Date: 2024
"""

import sys
import httpx
from typing import Optional, Dict, Any, List
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json


class FetchServer:
    """
    Official MCP Fetch Server Implementation
    
    Provides tools for fetching and processing web content.
    Based on the official Model Context Protocol fetch server.
    """
    
    def __init__(self):
        self.name = "fetch"
        self.version = "0.1.0"
        self.description = "Official MCP server for fetching web content"
        
        # User agent for requests
        self.user_agent = "ModelContextProtocol/1.0 (Fetch Server)"
        
        # HTTP client with reasonable timeouts
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={"User-Agent": self.user_agent}
        )
        
        self.capabilities = {
            "tools": [
                {
                    "name": "fetch",
                    "description": "Fetches a URL from the internet and extracts its contents as markdown",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL to fetch"
                            },
                            "max_length": {
                                "type": "integer",
                                "description": "Maximum number of characters to return (default: 5000)",
                                "default": 5000
                            },
                            "start_index": {
                                "type": "integer", 
                                "description": "Start reading from this character index (default: 0)",
                                "default": 0
                            },
                            "raw": {
                                "type": "boolean",
                                "description": "Get raw content without markdown conversion",
                                "default": False
                            }
                        },
                        "required": ["url"]
                    }
                },
                {
                    "name": "fetch_multiple",
                    "description": "Fetches multiple URLs in parallel and returns their contents",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "urls": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of URLs to fetch"
                            },
                            "max_length": {
                                "type": "integer",
                                "description": "Maximum characters per URL",
                                "default": 5000
                            }
                        },
                        "required": ["urls"]
                    }
                }
            ]
        }
    
    def _extract_text_from_html(self, html: str) -> str:
        """
        Extract readable text from HTML content.
        Removes scripts, styles, and converts to clean text.
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "meta", "link"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading/trailing space
            lines = (line.strip() for line in text.splitlines())
            
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            return f"Error parsing HTML: {str(e)}"
    
    def _convert_to_markdown(self, html: str, url: str) -> str:
        """
        Convert HTML to markdown-like format.
        Extracts main content and structures it.
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "meta", "link"]):
                element.decompose()
            
            markdown = []
            
            # Try to get title
            title = soup.find('title')
            if title:
                markdown.append(f"# {title.get_text().strip()}\n")
            
            # Get main content
            main = soup.find('main') or soup.find('article') or soup.find('body') or soup
            
            # Process elements
            for element in main.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote']):
                text = element.get_text().strip()
                if not text:
                    continue
                
                if element.name == 'h1':
                    markdown.append(f"\n# {text}\n")
                elif element.name == 'h2':
                    markdown.append(f"\n## {text}\n")
                elif element.name == 'h3':
                    markdown.append(f"\n### {text}\n")
                elif element.name == 'h4':
                    markdown.append(f"\n#### {text}\n")
                elif element.name == 'h5':
                    markdown.append(f"\n##### {text}\n")
                elif element.name == 'h6':
                    markdown.append(f"\n###### {text}\n")
                elif element.name == 'p':
                    markdown.append(f"{text}\n")
                elif element.name == 'li':
                    markdown.append(f"- {text}")
                elif element.name == 'blockquote':
                    markdown.append(f"> {text}\n")
            
            result = '\n'.join(markdown)
            
            # Add source URL
            result += f"\n\n---\nSource: {url}\n"
            
            return result
            
        except Exception as e:
            return f"Error converting to markdown: {str(e)}\n\nRaw text:\n{self._extract_text_from_html(html)}"
    
    def fetch(
        self,
        url: str,
        max_length: int = 5000,
        start_index: int = 0,
        raw: bool = False
    ) -> Dict[str, Any]:
        """
        Fetch a URL and return its content.
        
        Args:
            url: The URL to fetch
            max_length: Maximum characters to return
            start_index: Starting character index
            raw: Return raw text instead of markdown
            
        Returns:
            Dictionary with success status and content
        """
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return {
                    "error": "Invalid URL format",
                    "url": url
                }
            
            # Fetch content
            response = self.client.get(url)
            response.raise_for_status()
            
            # Get content type
            content_type = response.headers.get('content-type', '').lower()
            
            # Process based on content type
            if 'text/html' in content_type:
                if raw:
                    content = self._extract_text_from_html(response.text)
                else:
                    content = self._convert_to_markdown(response.text, url)
            else:
                # For non-HTML content, return as-is
                content = response.text
            
            # Apply slicing
            if start_index > 0 or max_length < len(content):
                end_index = min(start_index + max_length, len(content))
                content = content[start_index:end_index]
                
                truncated = end_index < len(response.text)
            else:
                truncated = False
            
            return {
                "success": True,
                "url": url,
                "content": content,
                "content_type": content_type,
                "status_code": response.status_code,
                "length": len(content),
                "truncated": truncated,
                "total_length": len(response.text)
            }
            
        except httpx.TimeoutException:
            return {
                "error": "Request timed out",
                "url": url
            }
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP error: {e.response.status_code}",
                "url": url,
                "status_code": e.response.status_code
            }
        except Exception as e:
            return {
                "error": str(e),
                "url": url
            }
    
    def fetch_multiple(
        self,
        urls: List[str],
        max_length: int = 5000
    ) -> Dict[str, Any]:
        """
        Fetch multiple URLs and return their contents.
        
        Args:
            urls: List of URLs to fetch
            max_length: Maximum characters per URL
            
        Returns:
            Dictionary with results for each URL
        """
        results = []
        
        for url in urls:
            result = self.fetch(url, max_length=max_length)
            results.append(result)
        
        # Count successes and failures
        successes = sum(1 for r in results if r.get('success'))
        failures = len(results) - successes
        
        return {
            "success": True,
            "total_urls": len(urls),
            "successful": successes,
            "failed": failures,
            "results": results
        }
    
    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            if method == "fetch":
                return self.fetch(**params)
            elif method == "fetch_multiple":
                return self.fetch_multiple(**params)
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            return {"error": str(e)}
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "operations": len(self.capabilities["tools"])
        }


def main():
    """Main entry point for MCP server"""
    server = FetchServer()
    
    print("🌐 MCP Fetch Server (Official)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("Status: Running", file=sys.stderr)
    print(f"Version: {server.version}", file=sys.stderr)
    print("Source: Official MCP Servers Repository", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # Keep server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped", file=sys.stderr)


if __name__ == "__main__":
    main()
