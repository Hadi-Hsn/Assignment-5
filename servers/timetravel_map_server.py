"""
TimeTravel Map Server - A Creative MCP Server for Historical Geography

This server allows AI agents to explore how locations have changed over time,
providing historical context, urban development patterns, and temporal geocoding.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import json
import random


@dataclass
class HistoricalLocation:
    """Represents a location at a specific point in time"""
    name: str
    latitude: float
    longitude: float
    year: int
    description: str
    existed: bool
    historical_context: str


class TimeTravelMapServer:
    """
    MCP Server for historical geographic exploration.
    
    Operations:
    1. geocode_historical: Find coordinates of a place as it existed in a specific year
    2. get_location_timeline: Get the history of how a location changed over time
    3. compare_eras: Compare a location between two different time periods
    """
    
    def __init__(self):
        self.server_name = "TimeTravel Map Server"
        self.version = "1.0.0"
        
        # Simulated historical database (in a real implementation, this would query historical APIs)
        self.historical_database = {
            "Beirut": [
                {"year": -3000, "name": "Berytus (Phoenician)", "lat": 33.8886, "lon": 35.4955,
                 "context": "Ancient Phoenician port city, center of maritime trade"},
                {"year": 64, "name": "Berytus (Roman)", "lat": 33.8886, "lon": 35.4955,
                 "context": "Roman colony, famous law school established"},
                {"year": 1866, "name": "Beirut", "lat": 33.8886, "lon": 35.4955,
                 "context": "American University of Beirut founded"},
                {"year": 1920, "name": "Beirut (French Mandate)", "lat": 33.8886, "lon": 35.4955,
                 "context": "Under French Mandate after WWI"},
                {"year": 1943, "name": "Beirut", "lat": 33.8886, "lon": 35.4955,
                 "context": "Lebanon gains independence, Beirut becomes capital"},
                {"year": 2024, "name": "Beirut", "lat": 33.8886, "lon": 35.4955,
                 "context": "Modern capital, resilient cultural hub of Lebanon"}
            ],
            "Gemmayzeh": [
                {"year": 1880, "name": "Gemmayzeh Quarter", "lat": 33.8947, "lon": 35.5189,
                 "context": "Historic Armenian and Greek Orthodox district established"},
                {"year": 1975, "name": "Gemmayzeh (Green Line)", "lat": 33.8947, "lon": 35.5189,
                 "context": "Near the Green Line during Lebanese civil war"},
                {"year": 2000, "name": "Gemmayzeh Arts District", "lat": 33.8947, "lon": 35.5189,
                 "context": "Post-war cultural renaissance, galleries and cafes flourish"},
                {"year": 2020, "name": "Gemmayzeh", "lat": 33.8947, "lon": 35.5189,
                 "context": "Devastating port blast damage, ongoing community rebuilding"}
            ],
            "AUB Campus": [
                {"year": 1866, "name": "Syrian Protestant College", "lat": 33.8972, "lon": 35.4795,
                 "context": "Founded by American missionaries, 16 students"},
                {"year": 1920, "name": "American University of Beirut", "lat": 33.8972, "lon": 35.4795,
                 "context": "Renamed AUB, expanded programs and campus"},
                {"year": 1975, "name": "AUB Campus (War Era)", "lat": 33.8972, "lon": 35.4795,
                 "context": "Continued operation during civil war, sanctuary for students"},
                {"year": 2024, "name": "AUB Campus", "lat": 33.8972, "lon": 35.4795,
                 "context": "Leading regional university, 158 years of excellence"}
            ],
            "AUB Main Gate": [
                {"year": 1866, "name": "College Entrance", "lat": 33.8975, "lon": 35.4790,
                 "context": "Original entrance to Syrian Protestant College"},
                {"year": 1920, "name": "AUB Main Gate", "lat": 33.8975, "lon": 35.4790,
                 "context": "Iconic campus entrance on Bliss Street"},
                {"year": 2024, "name": "AUB Main Gate", "lat": 33.8975, "lon": 35.4790,
                 "context": "Historic gateway welcoming generations of students"}
            ],
            "Byblos": [
                {"year": -5000, "name": "Gebal (Phoenician)", "lat": 34.1208, "lon": 35.6481,
                 "context": "Ancient Phoenician city, one of oldest continuously inhabited"},
                {"year": 64, "name": "Byblos (Roman)", "lat": 34.1208, "lon": 35.6481,
                 "context": "Roman colony, thriving port city"},
                {"year": 1104, "name": "Gibelet (Crusader)", "lat": 34.1208, "lon": 35.6481,
                 "context": "Crusader castle built overlooking the port"},
                {"year": 1920, "name": "Jbeil", "lat": 34.1208, "lon": 35.6481,
                 "context": "Lebanese town under French Mandate"},
                {"year": 2024, "name": "Byblos (Jbeil)", "lat": 34.1208, "lon": 35.6481,
                 "context": "UNESCO World Heritage Site, tourist destination"}
            ],
            "Constantinople": [
                {"year": 330, "name": "Constantinople", "lat": 41.0082, "lon": 28.9784, 
                 "context": "Founded by Constantine as the new capital of Roman Empire"},
                {"year": 1453, "name": "Constantinople", "lat": 41.0082, "lon": 28.9784,
                 "context": "Fell to Ottoman Empire, marking end of Byzantine Empire"},
                {"year": 1930, "name": "Istanbul", "lat": 41.0082, "lon": 28.9784,
                 "context": "Officially renamed to Istanbul by Turkish Republic"}
            ],
            "Berlin": [
                {"year": 1237, "name": "Berlin", "lat": 52.5200, "lon": 13.4050,
                 "context": "First documented mention of Berlin"},
                {"year": 1961, "name": "Berlin (Divided)", "lat": 52.5200, "lon": 13.4050,
                 "context": "Berlin Wall constructed, dividing East and West"},
                {"year": 1989, "name": "Berlin", "lat": 52.5200, "lon": 13.4050,
                 "context": "Berlin Wall fell, reunification began"}
            ],
            "New York": [
                {"year": 1624, "name": "New Amsterdam", "lat": 40.7128, "lon": -74.0060,
                 "context": "Dutch settlement established on Manhattan"},
                {"year": 1664, "name": "New York", "lat": 40.7128, "lon": -74.0060,
                 "context": "English captured and renamed the city"},
                {"year": 1898, "name": "New York City", "lat": 40.7128, "lon": -74.0060,
                 "context": "Five boroughs consolidated into modern NYC"}
            ]
        }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Return MCP server information"""
        return {
            "name": self.server_name,
            "version": self.version,
            "description": "Explore how locations have changed throughout history",
            "tools": [
                {
                    "name": "geocode_historical",
                    "description": "Find the coordinates and information about a location as it existed in a specific historical year",
                    "parameters": {
                        "location_name": "string - Name of the location",
                        "year": "integer - Historical year (e.g., 1453, 1776, 1945)"
                    }
                },
                {
                    "name": "get_location_timeline",
                    "description": "Retrieve a timeline showing how a location evolved through different historical periods",
                    "parameters": {
                        "location_name": "string - Name of the location",
                        "start_year": "integer - Starting year (optional)",
                        "end_year": "integer - Ending year (optional)"
                    }
                },
                {
                    "name": "compare_eras",
                    "description": "Compare a location between two different time periods to understand changes",
                    "parameters": {
                        "location_name": "string - Name of the location",
                        "year1": "integer - First year for comparison",
                        "year2": "integer - Second year for comparison"
                    }
                }
            ]
        }
    
    def geocode_historical(self, location_name: str, year: int) -> Dict[str, Any]:
        """
        Find coordinates of a place as it existed in a specific year.
        
        Args:
            location_name: Name of the location to search
            year: Historical year
            
        Returns:
            Dictionary with historical location data
        """
        # Search through historical database
        location_key = self._find_location_key(location_name)
        
        if not location_key:
            return {
                "success": False,
                "error": f"Location '{location_name}' not found in historical database",
                "suggestion": "Try 'Constantinople', 'Berlin', or 'New York'"
            }
        
        history = self.historical_database[location_key]
        
        # Find the most relevant historical entry for the given year
        closest_entry = min(history, key=lambda x: abs(x["year"] - year))
        
        # Check if location existed in that year
        existed = any(entry["year"] <= year for entry in history)
        
        result = {
            "success": True,
            "location": {
                "name": closest_entry["name"],
                "latitude": closest_entry["lat"],
                "longitude": closest_entry["lon"],
                "query_year": year,
                "closest_documented_year": closest_entry["year"],
                "existed": existed,
                "historical_context": closest_entry["context"]
            },
            "temporal_accuracy": "exact" if closest_entry["year"] == year else "interpolated",
            "year_difference": abs(year - closest_entry["year"])
        }
        
        return result
    
    def get_location_timeline(self, location_name: str, 
                             start_year: Optional[int] = None,
                             end_year: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a timeline of how a location changed over time.
        
        Args:
            location_name: Name of the location
            start_year: Starting year (optional)
            end_year: Ending year (optional)
            
        Returns:
            Timeline data structure
        """
        location_key = self._find_location_key(location_name)
        
        if not location_key:
            return {
                "success": False,
                "error": f"Location '{location_name}' not found in historical database"
            }
        
        history = self.historical_database[location_key]
        
        # Filter by year range if provided
        if start_year or end_year:
            filtered_history = [
                entry for entry in history
                if (not start_year or entry["year"] >= start_year) and
                   (not end_year or entry["year"] <= end_year)
            ]
        else:
            filtered_history = history
        
        timeline = {
            "success": True,
            "location": location_key,
            "timeline": [
                {
                    "year": entry["year"],
                    "name": entry["name"],
                    "coordinates": {"lat": entry["lat"], "lon": entry["lon"]},
                    "event": entry["context"]
                }
                for entry in sorted(filtered_history, key=lambda x: x["year"])
            ],
            "total_events": len(filtered_history),
            "time_span": {
                "earliest": min(entry["year"] for entry in filtered_history) if filtered_history else None,
                "latest": max(entry["year"] for entry in filtered_history) if filtered_history else None
            }
        }
        
        return timeline
    
    def compare_eras(self, location_name: str, year1: int, year2: int) -> Dict[str, Any]:
        """
        Compare a location between two time periods.
        
        Args:
            location_name: Name of the location
            year1: First year for comparison
            year2: Second year for comparison
            
        Returns:
            Comparison data
        """
        # Get data for both years
        era1 = self.geocode_historical(location_name, year1)
        era2 = self.geocode_historical(location_name, year2)
        
        if not era1.get("success") or not era2.get("success"):
            return {
                "success": False,
                "error": "Could not retrieve data for one or both time periods"
            }
        
        loc1 = era1["location"]
        loc2 = era2["location"]
        
        # Calculate differences
        name_changed = loc1["name"] != loc2["name"]
        coordinates_changed = (loc1["latitude"] != loc2["latitude"] or 
                              loc1["longitude"] != loc2["longitude"])
        
        comparison = {
            "success": True,
            "location": location_name,
            "era1": {
                "year": year1,
                "name": loc1["name"],
                "coordinates": {"lat": loc1["latitude"], "lon": loc1["longitude"]},
                "context": loc1["historical_context"]
            },
            "era2": {
                "year": year2,
                "name": loc2["name"],
                "coordinates": {"lat": loc2["latitude"], "lon": loc2["longitude"]},
                "context": loc2["historical_context"]
            },
            "changes": {
                "name_changed": name_changed,
                "coordinates_changed": coordinates_changed,
                "years_between": abs(year2 - year1)
            },
            "summary": self._generate_comparison_summary(loc1, loc2, year1, year2)
        }
        
        return comparison
    
    def _find_location_key(self, location_name: str) -> Optional[str]:
        """Find location key in database (case-insensitive)"""
        location_lower = location_name.lower()
        for key in self.historical_database.keys():
            if key.lower() == location_lower or any(
                entry["name"].lower() == location_lower 
                for entry in self.historical_database[key]
            ):
                return key
        return None
    
    def _generate_comparison_summary(self, loc1: Dict, loc2: Dict, 
                                    year1: int, year2: int) -> str:
        """Generate a human-readable summary of changes"""
        if loc1["name"] != loc2["name"]:
            return (f"Between {year1} and {year2}, '{loc1['name']}' was renamed to "
                   f"'{loc2['name']}'. This reflects significant political or cultural changes.")
        else:
            return (f"Between {year1} and {year2}, '{loc1['name']}' maintained its name "
                   f"but underwent historical developments.")


# MCP Tool definitions for integration with OpenAI Agents SDK
def create_timetravel_tools():
    """Create tool definitions for the TimeTravel Map Server"""
    server = TimeTravelMapServer()
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "geocode_historical",
                "description": "Find the coordinates and information about a location as it existed in a specific historical year. Useful for historical research, understanding how places changed over time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location_name": {
                            "type": "string",
                            "description": "Name of the historical location (e.g., 'Constantinople', 'New Amsterdam', 'Berlin')"
                        },
                        "year": {
                            "type": "integer",
                            "description": "Historical year to query (e.g., 1453, 1776, 1945)"
                        }
                    },
                    "required": ["location_name", "year"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_location_timeline",
                "description": "Retrieve a comprehensive timeline showing how a location evolved through different historical periods, including name changes, political transitions, and major events.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location_name": {
                            "type": "string",
                            "description": "Name of the location to get timeline for"
                        },
                        "start_year": {
                            "type": "integer",
                            "description": "Starting year for timeline (optional)"
                        },
                        "end_year": {
                            "type": "integer",
                            "description": "Ending year for timeline (optional)"
                        }
                    },
                    "required": ["location_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "compare_eras",
                "description": "Compare a location between two different time periods to understand what changed - names, borders, political control, or cultural significance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location_name": {
                            "type": "string",
                            "description": "Name of the location to compare"
                        },
                        "year1": {
                            "type": "integer",
                            "description": "First year for comparison"
                        },
                        "year2": {
                            "type": "integer",
                            "description": "Second year for comparison"
                        }
                    },
                    "required": ["location_name", "year1", "year2"]
                }
            }
        }
    ]
    
    return server, tools


if __name__ == "__main__":
    # Demo the server
    server = TimeTravelMapServer()
    
    print("=== TimeTravel Map Server Demo ===\n")
    print(json.dumps(server.get_server_info(), indent=2))
    
    print("\n\n=== Example 1: Geocode Constantinople in 1453 ===")
    result1 = server.geocode_historical("Constantinople", 1453)
    print(json.dumps(result1, indent=2))
    
    print("\n\n=== Example 2: Get Berlin Timeline ===")
    result2 = server.get_location_timeline("Berlin")
    print(json.dumps(result2, indent=2))
    
    print("\n\n=== Example 3: Compare New York between 1624 and 1898 ===")
    result3 = server.compare_eras("New York", 1624, 1898)
    print(json.dumps(result3, indent=2))
