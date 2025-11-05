#!/usr/bin/env python3
"""
Lebanese Weather MCP Server

Provides weather information for Lebanese cities and regions.
Includes current conditions, forecasts, and climate data specific to Lebanon.

Author: MCP Integration
Date: 2024
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import random

# Sample weather data for Lebanese locations
LEBANON_WEATHER_DATA = {
    "beirut": {
        "name": "Beirut",
        "coordinates": {"lat": 33.8886, "lon": 35.4955},
        "elevation": 34,
        "climate": "Mediterranean",
        "typical_temp_range": {"winter": "10-18°C", "summer": "24-32°C"}
    },
    "faraya": {
        "name": "Faraya (Ski Resort)",
        "coordinates": {"lat": 33.9833, "lon": 35.8167},
        "elevation": 1850,
        "climate": "Mountain Mediterranean",
        "typical_temp_range": {"winter": "-5-5°C", "summer": "15-25°C"}
    },
    "tripoli": {
        "name": "Tripoli",
        "coordinates": {"lat": 34.4367, "lon": 35.8497},
        "elevation": 0,
        "climate": "Mediterranean",
        "typical_temp_range": {"winter": "8-16°C", "summer": "22-30°C"}
    },
    "zahle": {
        "name": "Zahle (Bekaa Valley)",
        "coordinates": {"lat": 33.8469, "lon": 35.9019},
        "elevation": 945,
        "climate": "Continental Mediterranean",
        "typical_temp_range": {"winter": "2-12°C", "summer": "18-32°C"}
    },
    "byblos": {
        "name": "Byblos (Jbeil)",
        "coordinates": {"lat": 34.1208, "lon": 35.6481},
        "elevation": 20,
        "climate": "Mediterranean",
        "typical_temp_range": {"winter": "9-17°C", "summer": "23-30°C"}
    },
    "sidon": {
        "name": "Sidon (Saida)",
        "coordinates": {"lat": 33.5633, "lon": 35.3714},
        "elevation": 25,
        "climate": "Mediterranean",
        "typical_temp_range": {"winter": "10-18°C", "summer": "24-31°C"}
    },
    "tyre": {
        "name": "Tyre (Sour)",
        "coordinates": {"lat": 33.2733, "lon": 35.2039},
        "elevation": 15,
        "climate": "Mediterranean",
        "typical_temp_range": {"winter": "11-18°C", "summer": "24-30°C"}
    },
    "baalbek": {
        "name": "Baalbek",
        "coordinates": {"lat": 34.0067, "lon": 36.2183},
        "elevation": 1150,
        "climate": "Continental",
        "typical_temp_range": {"winter": "0-10°C", "summer": "20-35°C"}
    },
    "cedars": {
        "name": "The Cedars (Bcharre)",
        "coordinates": {"lat": 34.2833, "lon": 36.0167},
        "elevation": 2000,
        "climate": "Alpine Mediterranean",
        "typical_temp_range": {"winter": "-8-2°C", "summer": "12-22°C"}
    },
    "aub": {
        "name": "AUB Campus (Hamra)",
        "coordinates": {"lat": 33.8972, "lon": 35.4795},
        "elevation": 50,
        "climate": "Mediterranean",
        "typical_temp_range": {"winter": "10-18°C", "summer": "24-32°C"}
    }
}

# Weather conditions pool
WEATHER_CONDITIONS = [
    "clear", "partly_cloudy", "cloudy", "light_rain", "rain", 
    "thunderstorm", "fog", "windy", "humid", "dry"
]

LEBANON_WEATHER_PATTERNS = {
    "coastal": ["clear", "partly_cloudy", "humid", "windy"],
    "mountain": ["clear", "cloudy", "light_rain", "fog"],
    "valley": ["clear", "dry", "hot", "cloudy"]
}


class WeatherServer:
    """Lebanese Weather MCP Server implementation"""
    
    def __init__(self):
        self.name = "lebanese-weather"
        self.version = "1.0.0"
        self.capabilities = {
            "tools": [
                {
                    "name": "get_current_weather",
                    "description": "Get current weather conditions for a Lebanese city or region",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name (e.g., beirut, faraya, zahle, aub)"
                            }
                        },
                        "required": ["location"]
                    }
                },
                {
                    "name": "get_weather_forecast",
                    "description": "Get 5-day weather forecast for a Lebanese location",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City name (e.g., beirut, tripoli, byblos)"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days (1-5)",
                                "default": 5
                            }
                        },
                        "required": ["location"]
                    }
                },
                {
                    "name": "get_ski_conditions",
                    "description": "Get skiing conditions for Lebanese mountain resorts (Faraya, Cedars, etc.)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "resort": {
                                "type": "string",
                                "description": "Ski resort name (faraya, cedars)"
                            }
                        },
                        "required": ["resort"]
                    }
                },
                {
                    "name": "compare_locations",
                    "description": "Compare weather between two Lebanese locations",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "location1": {
                                "type": "string",
                                "description": "First location"
                            },
                            "location2": {
                                "type": "string",
                                "description": "Second location"
                            }
                        },
                        "required": ["location1", "location2"]
                    }
                }
            ]
        }
    
    def _generate_current_weather(self, location_key: str) -> Dict[str, Any]:
        """Generate realistic current weather for a location"""
        location = LEBANON_WEATHER_DATA[location_key]
        
        # Determine season
        month = datetime.now().month
        is_winter = month in [12, 1, 2, 3]
        is_summer = month in [6, 7, 8, 9]
        
        # Base temperature on season and elevation
        if is_winter:
            base_temp = 12 - (location["elevation"] / 100)
        elif is_summer:
            base_temp = 28 - (location["elevation"] / 150)
        else:
            base_temp = 20 - (location["elevation"] / 120)
        
        temp = round(base_temp + random.uniform(-3, 3), 1)
        
        # Determine conditions based on location type
        if location["elevation"] > 1000:
            condition = random.choice(LEBANON_WEATHER_PATTERNS["mountain"])
        elif location["elevation"] < 100:
            condition = random.choice(LEBANON_WEATHER_PATTERNS["coastal"])
        else:
            condition = random.choice(WEATHER_CONDITIONS)
        
        return {
            "location": location["name"],
            "coordinates": location["coordinates"],
            "temperature": temp,
            "condition": condition,
            "humidity": random.randint(40, 85),
            "wind_speed": random.randint(5, 25),
            "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
            "pressure": random.randint(1005, 1025),
            "visibility": random.randint(5, 20),
            "uv_index": random.randint(1, 10) if not is_winter else random.randint(1, 5),
            "timestamp": datetime.now().isoformat(),
            "elevation": location["elevation"],
            "climate_zone": location["climate"]
        }
    
    def _generate_forecast(self, location_key: str, days: int) -> List[Dict[str, Any]]:
        """Generate weather forecast for multiple days"""
        location = LEBANON_WEATHER_DATA[location_key]
        forecast = []
        
        for day in range(days):
            date = datetime.now() + timedelta(days=day)
            month = date.month
            is_winter = month in [12, 1, 2, 3]
            is_summer = month in [6, 7, 8, 9]
            
            if is_winter:
                temp_high = round(15 - (location["elevation"] / 100) + random.uniform(-2, 2), 1)
                temp_low = round(8 - (location["elevation"] / 100) + random.uniform(-2, 2), 1)
            elif is_summer:
                temp_high = round(32 - (location["elevation"] / 150) + random.uniform(-2, 2), 1)
                temp_low = round(22 - (location["elevation"] / 150) + random.uniform(-2, 2), 1)
            else:
                temp_high = round(22 - (location["elevation"] / 120) + random.uniform(-2, 2), 1)
                temp_low = round(14 - (location["elevation"] / 120) + random.uniform(-2, 2), 1)
            
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "day_name": date.strftime("%A"),
                "temp_high": temp_high,
                "temp_low": temp_low,
                "condition": random.choice(WEATHER_CONDITIONS),
                "precipitation_chance": random.randint(0, 80),
                "wind_speed": random.randint(5, 30)
            })
        
        return forecast
    
    def _generate_ski_conditions(self, resort_key: str) -> Dict[str, Any]:
        """Generate ski conditions for mountain resorts"""
        location = LEBANON_WEATHER_DATA[resort_key]
        month = datetime.now().month
        is_ski_season = month in [12, 1, 2, 3]
        
        if is_ski_season:
            snow_depth = random.randint(50, 200)
            conditions_rating = random.choice(["Excellent", "Good", "Fair"])
            lifts_open = random.randint(4, 8)
            new_snow_24h = random.randint(0, 30)
        else:
            snow_depth = 0
            conditions_rating = "Closed - Off Season"
            lifts_open = 0
            new_snow_24h = 0
        
        return {
            "resort": location["name"],
            "elevation": location["elevation"],
            "coordinates": location["coordinates"],
            "snow_depth_cm": snow_depth,
            "new_snow_24h_cm": new_snow_24h,
            "conditions_rating": conditions_rating,
            "temperature": round(-2 + random.uniform(-5, 8), 1) if is_ski_season else round(15 + random.uniform(-5, 10), 1),
            "lifts_open": lifts_open,
            "total_lifts": 8,
            "runs_open": f"{random.randint(10, 25)}/25" if is_ski_season else "0/25",
            "season_status": "Open" if is_ski_season else "Closed",
            "visibility": random.choice(["Excellent", "Good", "Moderate", "Poor"]) if is_ski_season else "N/A",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather for a location"""
        location_key = location.lower().strip()
        
        if location_key not in LEBANON_WEATHER_DATA:
            return {
                "error": f"Location '{location}' not found",
                "available_locations": list(LEBANON_WEATHER_DATA.keys()),
                "suggestion": "Try: beirut, faraya, tripoli, zahle, aub, cedars, baalbek, byblos, sidon, or tyre"
            }
        
        return {
            "success": True,
            "current_weather": self._generate_current_weather(location_key)
        }
    
    def get_weather_forecast(self, location: str, days: int = 5) -> Dict[str, Any]:
        """Get weather forecast for a location"""
        location_key = location.lower().strip()
        days = max(1, min(days, 5))  # Limit to 1-5 days
        
        if location_key not in LEBANON_WEATHER_DATA:
            return {
                "error": f"Location '{location}' not found",
                "available_locations": list(LEBANON_WEATHER_DATA.keys())
            }
        
        location_data = LEBANON_WEATHER_DATA[location_key]
        forecast = self._generate_forecast(location_key, days)
        
        return {
            "success": True,
            "location": location_data["name"],
            "coordinates": location_data["coordinates"],
            "forecast_days": days,
            "forecast": forecast
        }
    
    def get_ski_conditions(self, resort: str) -> Dict[str, Any]:
        """Get ski conditions for a resort"""
        resort_key = resort.lower().strip()
        
        valid_resorts = ["faraya", "cedars"]
        if resort_key not in valid_resorts:
            return {
                "error": f"Ski resort '{resort}' not found",
                "available_resorts": valid_resorts,
                "suggestion": "Try: faraya or cedars"
            }
        
        return {
            "success": True,
            "ski_conditions": self._generate_ski_conditions(resort_key)
        }
    
    def compare_locations(self, location1: str, location2: str) -> Dict[str, Any]:
        """Compare weather between two locations"""
        loc1_key = location1.lower().strip()
        loc2_key = location2.lower().strip()
        
        if loc1_key not in LEBANON_WEATHER_DATA:
            return {"error": f"Location '{location1}' not found"}
        if loc2_key not in LEBANON_WEATHER_DATA:
            return {"error": f"Location '{location2}' not found"}
        
        weather1 = self._generate_current_weather(loc1_key)
        weather2 = self._generate_current_weather(loc2_key)
        
        temp_diff = abs(weather1["temperature"] - weather2["temperature"])
        elevation_diff = abs(weather1["elevation"] - weather2["elevation"])
        
        return {
            "success": True,
            "comparison": {
                "location1": weather1,
                "location2": weather2,
                "differences": {
                    "temperature_diff": round(temp_diff, 1),
                    "elevation_diff": elevation_diff,
                    "humidity_diff": abs(weather1["humidity"] - weather2["humidity"]),
                    "wind_speed_diff": abs(weather1["wind_speed"] - weather2["wind_speed"])
                },
                "recommendation": self._get_comparison_recommendation(weather1, weather2)
            }
        }
    
    def _get_comparison_recommendation(self, weather1: Dict, weather2: Dict) -> str:
        """Generate recommendation based on weather comparison"""
        if weather1["temperature"] > weather2["temperature"] + 5:
            return f"{weather1['location']} is significantly warmer"
        elif weather2["temperature"] > weather1["temperature"] + 5:
            return f"{weather2['location']} is significantly warmer"
        elif weather1["elevation"] > 1000 and weather2["elevation"] < 500:
            return f"{weather1['location']} offers cooler mountain climate, {weather2['location']} has coastal conditions"
        else:
            return "Both locations have similar weather conditions"
    
    def handle_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        try:
            if method == "get_current_weather":
                return self.get_current_weather(**params)
            elif method == "get_weather_forecast":
                return self.get_weather_forecast(**params)
            elif method == "get_ski_conditions":
                return self.get_ski_conditions(**params)
            elif method == "compare_locations":
                return self.compare_locations(**params)
            else:
                return {"error": f"Unknown method: {method}"}
        except Exception as e:
            return {"error": str(e)}


def main():
    """Main entry point for MCP server"""
    server = WeatherServer()
    
    print("🌤️  Lebanese Weather MCP Server", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("Status: Running", file=sys.stderr)
    print(f"Version: {server.version}", file=sys.stderr)
    print(f"Available locations: {len(LEBANON_WEATHER_DATA)}", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    # Keep server running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped", file=sys.stderr)


if __name__ == "__main__":
    main()
