"""
Unit tests for Emotional Geography Map Server
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.emotional_geography_server import EmotionalGeographyServer


class TestEmotionalGeographyServer:
    """Test suite for Emotional Geography Server"""
    
    @pytest.fixture
    def server(self):
        """Create server instance for testing"""
        return EmotionalGeographyServer()
    
    def test_server_initialization(self, server):
        """Test that server initializes correctly"""
        assert server.server_name == "Emotional Geography Map Server"
        assert server.version == "1.0.0"
        assert len(server.emotional_database) > 0
    
    def test_get_server_info(self, server):
        """Test server info returns correct structure"""
        info = server.get_server_info()
        assert "name" in info
        assert "tools" in info
        assert len(info["tools"]) == 3
    
    def test_get_location_emotions_success(self, server):
        """Test successful emotion retrieval"""
        result = server.get_location_emotions("Paris, France")
        
        assert result["success"] is True
        assert "location" in result
        assert "emotional_profile" in result
        
        profile = result["emotional_profile"]
        assert "dominant_emotion" in profile
        assert "all_emotions" in profile
        assert "overall_intensity" in profile
        
        # Check emotions are scored 0-100
        for emotion, score in profile["all_emotions"].items():
            assert 0 <= score <= 100
    
    def test_get_location_emotions_not_found(self, server):
        """Test emotion query for non-existent location"""
        result = server.get_location_emotions("Atlantis")
        
        assert result["success"] is False
        assert "error" in result
        assert "available_locations" in result
    
    def test_get_location_emotions_fuzzy_match(self, server):
        """Test fuzzy matching of location names"""
        result = server.get_location_emotions("Paris")  # Without ", France"
        
        # Should still find Paris, France through fuzzy matching
        assert result["success"] is True
        assert "Paris" in result["location"]["name"]
    
    def test_find_places_by_emotion_valid(self, server):
        """Test finding places by specific emotion"""
        result = server.find_places_by_emotion("peace", min_intensity=70)
        
        assert result["success"] is True
        assert result["emotion_query"] == "peace"
        assert "locations" in result
        assert "total_matches" in result
        
        # All returned locations should meet minimum intensity
        for loc in result["locations"]:
            assert loc["emotion_score"] >= 70
        
        # Results should be sorted by score (descending)
        scores = [loc["emotion_score"] for loc in result["locations"]]
        assert scores == sorted(scores, reverse=True)
    
    def test_find_places_by_emotion_invalid(self, server):
        """Test with invalid emotion"""
        result = server.find_places_by_emotion("happiness", min_intensity=70)
        
        assert result["success"] is False
        assert "valid_emotions" in result
    
    def test_find_places_by_emotion_high_threshold(self, server):
        """Test with very high intensity threshold"""
        result = server.find_places_by_emotion("peace", min_intensity=95)
        
        assert result["success"] is True
        # Should find at least Reykjavik
        assert result["total_matches"] >= 1
    
    def test_get_emotional_heatmap_multiple_locations(self, server):
        """Test heatmap generation with multiple locations"""
        locations = ["Paris, France", "Tokyo, Japan", "Reykjavik, Iceland"]
        result = server.get_emotional_heatmap(locations)
        
        assert result["success"] is True
        assert len(result["heatmap_points"]) == 3
        assert "statistics" in result
        
        stats = result["statistics"]
        assert "max" in stats
        assert "min" in stats
        assert "average" in stats
    
    def test_get_emotional_heatmap_with_filter(self, server):
        """Test heatmap with emotion filter"""
        locations = ["Paris, France", "Kyoto, Japan"]
        result = server.get_emotional_heatmap(locations, emotion_filter="peace")
        
        assert result["success"] is True
        assert result["emotion_filter"] == "peace"
        
        # Each point should only have the filtered emotion
        for point in result["heatmap_points"]:
            assert "peace" in point["emotions"]
    
    def test_get_emotional_heatmap_invalid_location(self, server):
        """Test heatmap with some invalid locations"""
        locations = ["Paris, France", "InvalidCity", "Tokyo, Japan"]
        result = server.get_emotional_heatmap(locations)
        
        assert result["success"] is True
        # Should only include valid locations
        assert len(result["heatmap_points"]) == 2
    
    def test_insights_generation(self, server):
        """Test that insights are generated"""
        result = server.get_location_emotions("Reykjavik, Iceland")
        
        assert result["success"] is True
        assert "insights" in result
        assert len(result["insights"]) > 0
        # Iceland should have peace-related insight
        insights_text = " ".join(result["insights"]).lower()
        assert "peace" in insights_text or "tranquil" in insights_text
    
    def test_sample_sentiments_present(self, server):
        """Test that sample sentiments are included"""
        result = server.get_location_emotions("Tokyo, Japan")
        
        assert result["success"] is True
        assert "sample_sentiments" in result
        assert len(result["sample_sentiments"]) > 0


class TestEmotionalGeographyEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def server(self):
        return EmotionalGeographyServer()
    
    def test_emotion_case_insensitive(self, server):
        """Test that emotion queries are case insensitive"""
        result1 = server.find_places_by_emotion("peace")
        result2 = server.find_places_by_emotion("PEACE")
        result3 = server.find_places_by_emotion("Peace")
        
        assert result1["success"] is True
        assert result2["success"] is True
        assert result3["success"] is True
        assert result1["total_matches"] == result2["total_matches"]
    
    def test_min_intensity_boundaries(self, server):
        """Test minimum intensity boundary values"""
        result_low = server.find_places_by_emotion("joy", min_intensity=0)
        result_high = server.find_places_by_emotion("joy", min_intensity=100)
        
        assert result_low["success"] is True
        assert result_high["success"] is True
        assert result_low["total_matches"] >= result_high["total_matches"]
    
    def test_empty_heatmap(self, server):
        """Test heatmap with empty location list"""
        result = server.get_emotional_heatmap([])
        
        assert result["success"] is True
        assert len(result["heatmap_points"]) == 0
    
    def test_recommendation_generation(self, server):
        """Test that recommendations are meaningful"""
        result = server.find_places_by_emotion("inspiration", min_intensity=80)
        
        assert result["success"] is True
        assert "recommendation" in result
        assert len(result["recommendation"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
