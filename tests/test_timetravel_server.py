"""
Unit tests for TimeTravel Map Server
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.timetravel_map_server import TimeTravelMapServer


class TestTimeTravelMapServer:
    """Test suite for TimeTravel Map Server"""
    
    @pytest.fixture
    def server(self):
        """Create server instance for testing"""
        return TimeTravelMapServer()
    
    def test_server_initialization(self, server):
        """Test that server initializes correctly"""
        assert server.server_name == "TimeTravel Map Server"
        assert server.version == "1.0.0"
        assert len(server.historical_database) > 0
    
    def test_get_server_info(self, server):
        """Test server info returns correct structure"""
        info = server.get_server_info()
        assert "name" in info
        assert "version" in info
        assert "tools" in info
        assert len(info["tools"]) == 3
    
    def test_geocode_historical_success(self, server):
        """Test successful historical geocoding"""
        result = server.geocode_historical("Constantinople", 1453)
        
        assert result["success"] is True
        assert "location" in result
        assert result["location"]["query_year"] == 1453
        assert result["location"]["name"] == "Constantinople"
        assert "latitude" in result["location"]
        assert "longitude" in result["location"]
    
    def test_geocode_historical_not_found(self, server):
        """Test geocoding with non-existent location"""
        result = server.geocode_historical("Atlantis", 1000)
        
        assert result["success"] is False
        assert "error" in result
        assert "suggestion" in result
    
    def test_geocode_historical_interpolation(self, server):
        """Test that server interpolates between documented years"""
        result = server.geocode_historical("Berlin", 1970)
        
        assert result["success"] is True
        # Should find closest documented year (1961 or 1989)
        assert result["temporal_accuracy"] == "interpolated"
        assert result["year_difference"] > 0
    
    def test_get_location_timeline_full(self, server):
        """Test getting complete timeline"""
        result = server.get_location_timeline("Constantinople")
        
        assert result["success"] is True
        assert result["location"] == "Constantinople"
        assert len(result["timeline"]) > 0
        assert "total_events" in result
        assert "time_span" in result
        
        # Check timeline is sorted
        years = [event["year"] for event in result["timeline"]]
        assert years == sorted(years)
    
    def test_get_location_timeline_filtered(self, server):
        """Test timeline with year filters"""
        result = server.get_location_timeline("Berlin", start_year=1900, end_year=2000)
        
        assert result["success"] is True
        # All events should be within range
        for event in result["timeline"]:
            assert 1900 <= event["year"] <= 2000
    
    def test_compare_eras_success(self, server):
        """Test comparing two time periods"""
        result = server.compare_eras("New York", 1624, 1898)
        
        assert result["success"] is True
        assert "era1" in result
        assert "era2" in result
        assert "changes" in result
        
        # Check that it detected name change
        assert result["era1"]["name"] == "New Amsterdam"
        assert result["era2"]["name"] == "New York City"
        assert result["changes"]["name_changed"] is True
    
    def test_compare_eras_same_period(self, server):
        """Test comparing same time period"""
        result = server.compare_eras("Berlin", 1961, 1961)
        
        assert result["success"] is True
        assert result["changes"]["years_between"] == 0
    
    def test_case_insensitive_location_search(self, server):
        """Test that location search is case insensitive"""
        result1 = server.geocode_historical("constantinople", 1453)
        result2 = server.geocode_historical("CONSTANTINOPLE", 1453)
        result3 = server.geocode_historical("Constantinople", 1453)
        
        assert result1["success"] is True
        assert result2["success"] is True
        assert result3["success"] is True
    
    def test_historical_context_present(self, server):
        """Test that results include historical context"""
        result = server.geocode_historical("Berlin", 1961)
        
        assert result["success"] is True
        assert "historical_context" in result["location"]
        assert len(result["location"]["historical_context"]) > 0
        # Should mention Berlin Wall
        assert "Wall" in result["location"]["historical_context"]


class TestTimeTravelEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def server(self):
        return TimeTravelMapServer()
    
    def test_very_old_year(self, server):
        """Test with very ancient year"""
        result = server.geocode_historical("Constantinople", 100)
        assert result["success"] is True
        # Should return data even for year before city founding
    
    def test_future_year(self, server):
        """Test with future year"""
        result = server.geocode_historical("Istanbul", 2100)
        assert result["success"] is True
        # Should use most recent data
    
    def test_empty_location_name(self, server):
        """Test with empty location name"""
        result = server.geocode_historical("", 1453)
        assert result["success"] is False
    
    def test_timeline_reverse_years(self, server):
        """Test timeline with reversed year range"""
        result = server.get_location_timeline("Berlin", start_year=2000, end_year=1900)
        assert result["success"] is True
        # Should return empty or handle gracefully
        assert result["total_events"] == 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
