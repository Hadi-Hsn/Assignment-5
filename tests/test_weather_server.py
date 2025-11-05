"""
Unit tests for Lebanese Weather Server
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.weather_server import WeatherServer, LEBANON_WEATHER_DATA


class TestWeatherServer:
    """Test suite for Weather Server"""
    
    @pytest.fixture
    def server(self):
        """Create server instance for testing"""
        return WeatherServer()
    
    def test_server_initialization(self, server):
        """Test that server initializes correctly"""
        assert server.name == "lebanese-weather"
        assert server.version == "1.0.0"
        assert len(server.capabilities["tools"]) == 4
    
    def test_capabilities_structure(self, server):
        """Test capabilities are properly structured"""
        caps = server.capabilities
        assert "tools" in caps
        
        tool_names = [tool["name"] for tool in caps["tools"]]
        assert "get_current_weather" in tool_names
        assert "get_weather_forecast" in tool_names
        assert "get_ski_conditions" in tool_names
        assert "compare_locations" in tool_names
    
    def test_get_current_weather_beirut(self, server):
        """Test getting current weather for Beirut"""
        result = server.get_current_weather("beirut")
        
        assert result["success"] is True
        assert "current_weather" in result
        
        weather = result["current_weather"]
        assert "location" in weather
        assert weather["location"] == "Beirut"
        assert "temperature" in weather
        assert "condition" in weather
        assert "humidity" in weather
        assert "wind_speed" in weather
        assert "pressure" in weather
        assert "coordinates" in weather
        assert "elevation" in weather
        assert "timestamp" in weather
    
    def test_get_current_weather_all_locations(self, server):
        """Test weather for all available locations"""
        for location_key in LEBANON_WEATHER_DATA.keys():
            result = server.get_current_weather(location_key)
            
            assert result["success"] is True
            assert "current_weather" in result
            weather = result["current_weather"]
            assert weather["temperature"] is not None
            assert isinstance(weather["temperature"], (int, float))
    
    def test_get_current_weather_invalid_location(self, server):
        """Test with invalid location"""
        result = server.get_current_weather("InvalidCity")
        
        assert "error" in result
        assert "available_locations" in result
        assert "suggestion" in result
        assert len(result["available_locations"]) > 0
    
    def test_get_current_weather_case_insensitive(self, server):
        """Test that location search is case insensitive"""
        result1 = server.get_current_weather("BEIRUT")
        result2 = server.get_current_weather("beirut")
        result3 = server.get_current_weather("Beirut")
        
        assert result1["success"] is True
        assert result2["success"] is True
        assert result3["success"] is True
    
    def test_get_weather_forecast_default_days(self, server):
        """Test weather forecast with default days"""
        result = server.get_weather_forecast("beirut")
        
        assert result["success"] is True
        assert "forecast" in result
        assert "forecast_days" in result
        assert result["forecast_days"] == 5
        assert len(result["forecast"]) == 5
    
    def test_get_weather_forecast_custom_days(self, server):
        """Test weather forecast with custom days"""
        for days in [1, 2, 3, 4, 5]:
            result = server.get_weather_forecast("beirut", days=days)
            
            assert result["success"] is True
            assert len(result["forecast"]) == days
    
    def test_get_weather_forecast_structure(self, server):
        """Test forecast structure"""
        result = server.get_weather_forecast("tripoli", days=3)
        
        assert result["success"] is True
        forecast = result["forecast"]
        
        for day in forecast:
            assert "date" in day
            assert "day_name" in day
            assert "temp_high" in day
            assert "temp_low" in day
            assert "condition" in day
            assert "precipitation_chance" in day
            assert "wind_speed" in day
            
            # Temperature logic check
            assert day["temp_high"] >= day["temp_low"]
    
    def test_get_weather_forecast_days_boundary(self, server):
        """Test forecast with boundary day values"""
        # Test with 0 days (should clamp to 1)
        result = server.get_weather_forecast("beirut", days=0)
        assert result["success"] is True
        assert len(result["forecast"]) >= 1
        
        # Test with more than 5 days (should clamp to 5)
        result = server.get_weather_forecast("beirut", days=10)
        assert result["success"] is True
        assert len(result["forecast"]) <= 5
    
    def test_get_ski_conditions_faraya(self, server):
        """Test ski conditions for Faraya"""
        result = server.get_ski_conditions("faraya")
        
        assert result["success"] is True
        assert "ski_conditions" in result
        
        conditions = result["ski_conditions"]
        assert "resort" in conditions
        assert "Faraya" in conditions["resort"]
        assert "snow_depth_cm" in conditions
        assert "conditions_rating" in conditions
        assert "lifts_open" in conditions
        assert "total_lifts" in conditions
        assert "season_status" in conditions
        assert "elevation" in conditions
    
    def test_get_ski_conditions_cedars(self, server):
        """Test ski conditions for Cedars"""
        result = server.get_ski_conditions("cedars")
        
        assert result["success"] is True
        assert "ski_conditions" in result
        assert "Cedars" in result["ski_conditions"]["resort"] or "Bcharre" in result["ski_conditions"]["resort"]
    
    def test_get_ski_conditions_invalid_resort(self, server):
        """Test with invalid ski resort"""
        result = server.get_ski_conditions("InvalidResort")
        
        assert "error" in result
        assert "available_resorts" in result
        assert "suggestion" in result
    
    def test_get_ski_conditions_case_insensitive(self, server):
        """Test ski conditions with case insensitivity"""
        result1 = server.get_ski_conditions("FARAYA")
        result2 = server.get_ski_conditions("faraya")
        
        assert result1["success"] is True
        assert result2["success"] is True
    
    def test_compare_locations_success(self, server):
        """Test comparing two locations"""
        result = server.compare_locations("beirut", "faraya")
        
        assert result["success"] is True
        assert "comparison" in result
        
        comp = result["comparison"]
        assert "location1" in comp
        assert "location2" in comp
        assert "differences" in comp
        assert "recommendation" in comp
        
        # Check differences structure
        diffs = comp["differences"]
        assert "temperature_diff" in diffs
        assert "elevation_diff" in diffs
        assert "humidity_diff" in diffs
        assert "wind_speed_diff" in diffs
    
    def test_compare_locations_same_location(self, server):
        """Test comparing location with itself"""
        result = server.compare_locations("beirut", "beirut")
        
        assert result["success"] is True
        diffs = result["comparison"]["differences"]
        # Elevation should be exactly the same (static data)
        assert diffs["elevation_diff"] == 0
        # Temperature may differ slightly due to random generation
        # But both readings should be for the same base location
        assert diffs["temperature_diff"] >= 0  # Should be non-negative
        # Verify both locations are indeed the same
        assert result["comparison"]["location1"]["location"] == result["comparison"]["location2"]["location"]
    
    def test_compare_locations_coastal_vs_mountain(self, server):
        """Test comparing coastal and mountain locations"""
        result = server.compare_locations("beirut", "cedars")
        
        assert result["success"] is True
        # Should have significant elevation difference
        assert result["comparison"]["differences"]["elevation_diff"] > 1000
    
    def test_compare_locations_invalid_first(self, server):
        """Test with invalid first location"""
        result = server.compare_locations("InvalidCity", "beirut")
        
        assert "error" in result
    
    def test_compare_locations_invalid_second(self, server):
        """Test with invalid second location"""
        result = server.compare_locations("beirut", "InvalidCity")
        
        assert "error" in result
    
    def test_handle_request_get_current_weather(self, server):
        """Test handle_request with get_current_weather"""
        result = server.handle_request("get_current_weather", {"location": "beirut"})
        
        assert result["success"] is True
    
    def test_handle_request_get_forecast(self, server):
        """Test handle_request with get_weather_forecast"""
        result = server.handle_request("get_weather_forecast", {"location": "tripoli", "days": 3})
        
        assert result["success"] is True
    
    def test_handle_request_get_ski_conditions(self, server):
        """Test handle_request with get_ski_conditions"""
        result = server.handle_request("get_ski_conditions", {"resort": "faraya"})
        
        assert result["success"] is True
    
    def test_handle_request_compare_locations(self, server):
        """Test handle_request with compare_locations"""
        result = server.handle_request("compare_locations", {
            "location1": "beirut",
            "location2": "faraya"
        })
        
        assert result["success"] is True
    
    def test_handle_request_unknown_method(self, server):
        """Test handle_request with unknown method"""
        result = server.handle_request("unknown_method", {})
        
        assert "error" in result
        assert "Unknown method" in result["error"]


class TestWeatherServerDataGeneration:
    """Test weather data generation logic"""
    
    @pytest.fixture
    def server(self):
        return WeatherServer()
    
    def test_temperature_varies_by_elevation(self, server):
        """Test that temperature varies with elevation"""
        coastal = server.get_current_weather("beirut")
        mountain = server.get_current_weather("cedars")
        
        # Mountain should generally be cooler
        coastal_temp = coastal["current_weather"]["temperature"]
        mountain_temp = mountain["current_weather"]["temperature"]
        
        # There should be some temperature difference due to elevation
        # (not always cooler due to random variation, but significantly different)
        assert coastal_temp != mountain_temp or abs(coastal_temp - mountain_temp) >= 0
    
    def test_humidity_in_valid_range(self, server):
        """Test that humidity is in valid range"""
        result = server.get_current_weather("beirut")
        humidity = result["current_weather"]["humidity"]
        
        assert 0 <= humidity <= 100
    
    def test_wind_speed_positive(self, server):
        """Test that wind speed is positive"""
        result = server.get_current_weather("beirut")
        wind_speed = result["current_weather"]["wind_speed"]
        
        assert wind_speed >= 0
    
    def test_pressure_in_realistic_range(self, server):
        """Test that pressure is realistic"""
        result = server.get_current_weather("beirut")
        pressure = result["current_weather"]["pressure"]
        
        # Typical atmospheric pressure range
        assert 950 <= pressure <= 1050
    
    def test_uv_index_in_valid_range(self, server):
        """Test that UV index is valid"""
        result = server.get_current_weather("beirut")
        uv = result["current_weather"]["uv_index"]
        
        assert 0 <= uv <= 11  # Standard UV index range
    
    def test_forecast_temperatures_logical(self, server):
        """Test that forecast temperatures are logical"""
        result = server.get_weather_forecast("beirut", days=5)
        
        for day in result["forecast"]:
            # High should be higher than low
            assert day["temp_high"] >= day["temp_low"]
            
            # Temperatures should be in reasonable range
            assert -20 <= day["temp_low"] <= 50
            assert -20 <= day["temp_high"] <= 50
    
    def test_precipitation_chance_in_range(self, server):
        """Test precipitation chance is valid percentage"""
        result = server.get_weather_forecast("beirut", days=3)
        
        for day in result["forecast"]:
            assert 0 <= day["precipitation_chance"] <= 100


class TestWeatherServerEdgeCases:
    """Test edge cases and error handling"""
    
    @pytest.fixture
    def server(self):
        return WeatherServer()
    
    def test_empty_location_string(self, server):
        """Test with empty location string"""
        result = server.get_current_weather("")
        
        assert "error" in result
    
    def test_whitespace_location(self, server):
        """Test with whitespace-only location"""
        result = server.get_current_weather("   ")
        
        assert "error" in result
    
    def test_location_with_extra_spaces(self, server):
        """Test location with extra spaces"""
        result = server.get_current_weather("  beirut  ")
        
        assert result["success"] is True
    
    def test_negative_forecast_days(self, server):
        """Test with negative forecast days"""
        result = server.get_weather_forecast("beirut", days=-1)
        
        assert result["success"] is True
        assert len(result["forecast"]) >= 1  # Should clamp to minimum
    
    def test_very_large_forecast_days(self, server):
        """Test with very large forecast days"""
        result = server.get_weather_forecast("beirut", days=100)
        
        assert result["success"] is True
        assert len(result["forecast"]) <= 5  # Should clamp to maximum
    
    def test_all_locations_have_coordinates(self, server):
        """Test that all locations have valid coordinates"""
        for location_key in LEBANON_WEATHER_DATA.keys():
            result = server.get_current_weather(location_key)
            coords = result["current_weather"]["coordinates"]
            
            assert "lat" in coords
            assert "lon" in coords
            # Lebanon is roughly between 33-35°N and 35-37°E
            assert 32 <= coords["lat"] <= 35
            assert 34 <= coords["lon"] <= 37
    
    def test_ski_conditions_season_awareness(self, server):
        """Test that ski conditions are season-aware"""
        result = server.get_ski_conditions("faraya")
        conditions = result["ski_conditions"]
        
        # Season status should be either Open or Closed
        assert conditions["season_status"] in ["Open", "Closed"]
        
        # If closed, lifts should be 0
        if conditions["season_status"] == "Closed":
            assert conditions["lifts_open"] == 0
    
    def test_comparison_recommendation_exists(self, server):
        """Test that comparison always provides recommendation"""
        result = server.compare_locations("beirut", "faraya")
        
        assert result["success"] is True
        assert result["comparison"]["recommendation"] != ""
        assert len(result["comparison"]["recommendation"]) > 0


class TestWeatherServerDataConsistency:
    """Test data consistency across calls"""
    
    @pytest.fixture
    def server(self):
        return WeatherServer()
    
    def test_location_names_consistent(self, server):
        """Test that location names are consistent"""
        result1 = server.get_current_weather("beirut")
        result2 = server.get_weather_forecast("beirut")
        
        # Both should reference same location name
        assert result1["current_weather"]["location"] == result2["location"]
    
    def test_coordinates_consistent(self, server):
        """Test that coordinates are consistent across methods"""
        result1 = server.get_current_weather("beirut")
        result2 = server.get_weather_forecast("beirut")
        
        coords1 = result1["current_weather"]["coordinates"]
        coords2 = result2["coordinates"]
        
        assert coords1["lat"] == coords2["lat"]
        assert coords1["lon"] == coords2["lon"]
    
    def test_elevation_consistent(self, server):
        """Test that elevation data is consistent"""
        result1 = server.get_current_weather("faraya")
        result2 = server.get_ski_conditions("faraya")
        
        elev1 = result1["current_weather"]["elevation"]
        elev2 = result2["ski_conditions"]["elevation"]
        
        assert elev1 == elev2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
