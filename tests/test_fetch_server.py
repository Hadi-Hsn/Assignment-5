"""
Unit tests for Fetch Server (MCP Official)
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.fetch_server import FetchServer


class TestFetchServer:
    """Test suite for Fetch Server"""
    
    @pytest.fixture
    def server(self):
        """Create server instance for testing"""
        return FetchServer()
    
    def test_server_initialization(self, server):
        """Test that server initializes correctly"""
        assert server.name == "fetch"
        assert server.version == "0.1.0"
        assert server.user_agent == "ModelContextProtocol/1.0 (Fetch Server)"
        assert server.client is not None
    
    def test_get_server_info(self, server):
        """Test server info returns correct structure"""
        info = server.get_server_info()
        assert "name" in info
        assert "version" in info
        assert "description" in info
        assert "operations" in info
        assert info["operations"] == 2  # fetch and fetch_multiple
    
    def test_capabilities_structure(self, server):
        """Test capabilities are properly structured"""
        caps = server.capabilities
        assert "tools" in caps
        assert len(caps["tools"]) == 2
        
        # Check tool names
        tool_names = [tool["name"] for tool in caps["tools"]]
        assert "fetch" in tool_names
        assert "fetch_multiple" in tool_names
        
        # Check each tool has required fields
        for tool in caps["tools"]:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
            assert "properties" in tool["inputSchema"]
    
    def test_fetch_valid_url(self, server):
        """Test fetching a valid URL"""
        # Using a reliable public URL
        result = server.fetch("https://example.com")
        
        assert "content" in result
        # May succeed or have network error - both are valid responses
        if result.get("success"):
            assert "url" in result
            assert result["url"] == "https://example.com"
            assert "content_type" in result
            assert "status_code" in result
            assert result["status_code"] == 200
            assert "length" in result
            assert "total_length" in result
    
    def test_fetch_invalid_url(self, server):
        """Test fetching with invalid URL format"""
        result = server.fetch("not-a-valid-url")
        
        assert "error" in result
        assert "Invalid URL" in result["error"]
    
    def test_fetch_with_max_length(self, server):
        """Test fetching with max_length parameter"""
        result = server.fetch("https://example.com", max_length=100)
        
        if result.get("success"):
            assert len(result["content"]) <= 100
            if result["total_length"] > 100:
                assert result["truncated"] is True
    
    def test_fetch_with_start_index(self, server):
        """Test fetching with start_index parameter"""
        result = server.fetch("https://example.com", start_index=50, max_length=100)
        
        if result.get("success"):
            assert len(result["content"]) <= 100
    
    def test_fetch_raw_mode(self, server):
        """Test fetching in raw mode (no markdown conversion)"""
        result = server.fetch("https://example.com", raw=True)
        
        if result.get("success"):
            assert "content" in result
            # Raw mode should return plain text
            assert isinstance(result["content"], str)
    
    def test_fetch_markdown_mode(self, server):
        """Test fetching with markdown conversion (default)"""
        result = server.fetch("https://example.com", raw=False)
        
        if result.get("success"):
            assert "content" in result
            # Should contain markdown formatting or source URL
            content = result["content"]
            assert isinstance(content, str)
    
    def test_fetch_multiple_urls(self, server):
        """Test fetching multiple URLs"""
        urls = ["https://example.com", "https://example.org"]
        result = server.fetch_multiple(urls)
        
        assert result["success"] is True
        assert "results" in result
        assert "total_urls" in result
        assert result["total_urls"] == 2
        assert "successful" in result
        assert "failed" in result
        assert len(result["results"]) == 2
        
        # Check each result has proper structure
        for res in result["results"]:
            assert "url" in res
    
    def test_fetch_multiple_empty_list(self, server):
        """Test fetching with empty URL list"""
        result = server.fetch_multiple([])
        
        assert result["success"] is True
        assert result["total_urls"] == 0
        assert len(result["results"]) == 0
    
    def test_fetch_multiple_with_max_length(self, server):
        """Test fetching multiple URLs with max_length"""
        urls = ["https://example.com"]
        result = server.fetch_multiple(urls, max_length=100)
        
        assert result["success"] is True
        if result["successful"] > 0:
            # Check that max_length was applied
            for res in result["results"]:
                if res.get("success"):
                    assert res["length"] <= 100
    
    def test_handle_request_fetch(self, server):
        """Test handle_request with fetch method"""
        params = {"url": "https://example.com", "max_length": 1000}
        result = server.handle_request("fetch", params)
        
        assert "url" in result or "error" in result
    
    def test_handle_request_fetch_multiple(self, server):
        """Test handle_request with fetch_multiple method"""
        params = {"urls": ["https://example.com"], "max_length": 1000}
        result = server.handle_request("fetch_multiple", params)
        
        assert "results" in result or "error" in result
    
    def test_handle_request_unknown_method(self, server):
        """Test handle_request with unknown method"""
        result = server.handle_request("unknown_method", {})
        
        assert "error" in result
        assert "Unknown method" in result["error"]
    
    def test_extract_text_from_html(self, server):
        """Test HTML text extraction"""
        html = """
        <html>
            <head><title>Test</title></head>
            <body>
                <script>alert('test');</script>
                <p>Hello World</p>
                <style>.test { color: red; }</style>
                <div>Content</div>
            </body>
        </html>
        """
        
        text = server._extract_text_from_html(html)
        
        assert "Hello World" in text
        assert "Content" in text
        assert "alert" not in text  # Script should be removed
        assert "color: red" not in text  # Style should be removed
    
    def test_convert_to_markdown(self, server):
        """Test HTML to markdown conversion"""
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Main Title</h1>
                <h2>Subtitle</h2>
                <p>This is a paragraph.</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </body>
        </html>
        """
        
        markdown = server._convert_to_markdown(html, "https://example.com")
        
        assert "# Test Page" in markdown or "Test Page" in markdown
        assert "Main Title" in markdown
        assert "Subtitle" in markdown
        assert "paragraph" in markdown
        assert "Source: https://example.com" in markdown


class TestFetchServerEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def server(self):
        return FetchServer()
    
    def test_fetch_with_protocol_missing(self, server):
        """Test URL without protocol"""
        result = server.fetch("example.com")
        
        # Should fail with invalid URL error
        assert "error" in result
    
    def test_fetch_with_special_characters(self, server):
        """Test URL with special characters"""
        result = server.fetch("https://example.com/path?query=test&param=value")
        
        # Should handle URL encoding properly
        assert "url" in result or "error" in result
    
    def test_fetch_nonexistent_domain(self, server):
        """Test fetching non-existent domain"""
        result = server.fetch("https://this-domain-definitely-does-not-exist-12345.com")
        
        assert "error" in result
    
    def test_fetch_multiple_mixed_validity(self, server):
        """Test fetching mix of valid and invalid URLs"""
        urls = [
            "https://example.com",
            "invalid-url",
            "https://example.org"
        ]
        result = server.fetch_multiple(urls)
        
        assert result["success"] is True
        assert result["failed"] >= 1  # At least the invalid URL should fail
    
    def test_max_length_zero(self, server):
        """Test with max_length of 0"""
        result = server.fetch("https://example.com", max_length=0)
        
        if result.get("success"):
            assert result["length"] == 0
            assert result["content"] == ""
    
    def test_start_index_beyond_content(self, server):
        """Test start_index beyond content length"""
        result = server.fetch("https://example.com", start_index=999999)
        
        if result.get("success"):
            # Should return empty or handle gracefully
            assert "content" in result
    
    def test_negative_parameters(self, server):
        """Test with negative parameters"""
        # Should handle negative values gracefully
        result = server.fetch("https://example.com", max_length=-100, start_index=-50)
        
        # Should either work or return error
        assert "content" in result or "error" in result


class TestFetchServerHTTPHandling:
    """Test HTTP-specific scenarios"""
    
    @pytest.fixture
    def server(self):
        return FetchServer()
    
    def test_user_agent_set(self, server):
        """Test that user agent is properly set"""
        assert "User-Agent" in server.client.headers
        assert server.client.headers["User-Agent"] == server.user_agent
    
    def test_timeout_configuration(self, server):
        """Test that timeout is configured"""
        assert server.client.timeout is not None
    
    def test_redirect_following(self, server):
        """Test that redirects are followed"""
        # The client should be configured to follow redirects
        assert server.client.follow_redirects is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
