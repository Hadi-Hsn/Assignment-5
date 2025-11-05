"""
Emotional Geography Map Server - A Creative MCP Server for Sentiment Mapping

This server maps emotions and sentiments to geographic locations, providing
insights into how people feel about different places based on aggregated data,
reviews, and social sentiment analysis.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import random
import math


class EmotionType(Enum):
    """Primary emotion categories"""
    JOY = "joy"
    SADNESS = "sadness"
    EXCITEMENT = "excitement"
    FEAR = "fear"
    PEACE = "peace"
    NOSTALGIA = "nostalgia"
    INSPIRATION = "inspiration"
    STRESS = "stress"


@dataclass
class EmotionalData:
    """Represents emotional sentiment data for a location"""
    location: str
    latitude: float
    longitude: float
    dominant_emotion: str
    emotion_scores: Dict[str, float]  # Emotion type -> score (0-100)
    sentiment_intensity: float
    sample_descriptions: List[str]


class EmotionalGeographyServer:
    """
    MCP Server for mapping emotions to geographic locations.
    
    Operations:
    1. get_location_emotions: Get the emotional profile of a specific location
    2. find_places_by_emotion: Find locations that evoke a specific emotion
    3. get_emotional_heatmap: Generate emotional intensity data for a region
    """
    
    def __init__(self):
        self.server_name = "Emotional Geography Map Server"
        self.version = "1.0.0"
        
        # Simulated emotional database (in real implementation, would analyze reviews, social media)
        self.emotional_database = {
            "Beirut": {
                "lat": 33.8886,
                "lon": 35.4955,
                "emotions": {
                    "nostalgia": 85,
                    "resilience": 90,
                    "joy": 70,
                    "hope": 75,
                    "melancholy": 60,
                    "inspiration": 80
                },
                "descriptions": [
                    "The city that rises from the ashes with unbreakable spirit",
                    "Corniche sunsets bring bittersweet memories",
                    "Every street corner tells a story of survival and beauty"
                ]
            },
            "Gemmayzeh": {
                "lat": 33.8947,
                "lon": 35.5189,
                "emotions": {
                    "nostalgia": 90,
                    "joy": 75,
                    "creativity": 85,
                    "sadness": 65,
                    "hope": 70,
                    "community": 80
                },
                "descriptions": [
                    "Historic streets filled with art and resilience",
                    "The heartbeat of Beirut's creative renaissance",
                    "Where tradition meets contemporary Lebanese culture",
                    "Rebuilding with beauty and determination"
                ]
            },
            "AUB Campus": {
                "lat": 33.8972,
                "lon": 35.4795,
                "emotions": {
                    "inspiration": 90,
                    "peace": 85,
                    "ambition": 80,
                    "joy": 75,
                    "nostalgia": 70,
                    "stress": 40
                },
                "descriptions": [
                    "Green sanctuary in the heart of Beirut",
                    "Where generations of leaders found their calling",
                    "The ancient trees whisper wisdom to students",
                    "A bubble of academic excellence and natural beauty"
                ]
            },
            "Hamra": {
                "lat": 33.8978,
                "lon": 35.4828,
                "emotions": {
                    "excitement": 85,
                    "nostalgia": 75,
                    "energy": 90,
                    "joy": 80,
                    "chaos": 70,
                    "inspiration": 65
                },
                "descriptions": [
                    "The intellectual and cultural heart of Beirut",
                    "Bustling street life from dawn to midnight",
                    "Where students, artists, and thinkers converge"
                ]
            },
            "AUB Main Gate": {
                "lat": 33.8975,
                "lon": 35.4790,
                "emotions": {
                    "anticipation": 85,
                    "pride": 90,
                    "nostalgia": 80,
                    "inspiration": 75,
                    "belonging": 88,
                    "excitement": 70
                },
                "descriptions": [
                    "The threshold where journeys begin",
                    "Generations have passed through these gates to knowledge",
                    "Every return brings waves of memories",
                    "The iconic gateway to academic excellence"
                ]
            },
            "Byblos": {
                "lat": 34.1208,
                "lon": 35.6481,
                "emotions": {
                    "wonder": 90,
                    "peace": 85,
                    "nostalgia": 95,
                    "inspiration": 88,
                    "joy": 75,
                    "awe": 92
                },
                "descriptions": [
                    "Walking through 7,000 years of history",
                    "Ancient harbor where civilizations were born",
                    "The old souk whispers tales of Phoenician traders",
                    "UNESCO heritage site with timeless Mediterranean charm"
                ]
            },
            "Paris, France": {
                "lat": 48.8566,
                "lon": 2.3522,
                "emotions": {
                    "joy": 75,
                    "inspiration": 85,
                    "nostalgia": 60,
                    "excitement": 70,
                    "peace": 45,
                    "stress": 40
                },
                "descriptions": [
                    "The city lights filled me with wonder",
                    "Walking along the Seine brought such peace",
                    "The art scene is incredibly inspiring"
                ]
            },
            "Tokyo, Japan": {
                "lat": 35.6762,
                "lon": 139.6503,
                "emotions": {
                    "excitement": 90,
                    "inspiration": 80,
                    "stress": 55,
                    "joy": 70,
                    "peace": 50,
                    "nostalgia": 45
                },
                "descriptions": [
                    "The energy of Shibuya is electrifying",
                    "Found unexpected tranquility in traditional gardens",
                    "Technology and tradition create constant amazement"
                ]
            },
            "Reykjavik, Iceland": {
                "lat": 64.1466,
                "lon": -21.9426,
                "emotions": {
                    "peace": 95,
                    "inspiration": 85,
                    "joy": 65,
                    "excitement": 60,
                    "nostalgia": 40,
                    "stress": 15
                },
                "descriptions": [
                    "The vast landscapes bring incredible calm",
                    "Northern lights stirred something deep within",
                    "Nature's raw beauty is overwhelming"
                ]
            },
            "New York City, USA": {
                "lat": 40.7128,
                "lon": -74.0060,
                "emotions": {
                    "excitement": 95,
                    "stress": 75,
                    "inspiration": 80,
                    "joy": 70,
                    "peace": 25,
                    "nostalgia": 50
                },
                "descriptions": [
                    "The city that never sleeps keeps you energized",
                    "Constant stimulus can be overwhelming",
                    "Every corner holds creative possibility"
                ]
            },
            "Kyoto, Japan": {
                "lat": 35.0116,
                "lon": 135.7681,
                "emotions": {
                    "peace": 90,
                    "nostalgia": 85,
                    "inspiration": 75,
                    "joy": 70,
                    "excitement": 45,
                    "stress": 20
                },
                "descriptions": [
                    "Ancient temples radiate serenity",
                    "Feels like stepping back in time",
                    "Traditional gardens promote deep reflection"
                ]
            }
        }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Return MCP server information"""
        return {
            "name": self.server_name,
            "version": self.version,
            "description": "Discover the emotional landscape of locations worldwide through aggregated sentiment analysis",
            "tools": [
                {
                    "name": "get_location_emotions",
                    "description": "Retrieve the emotional profile and sentiment data for a specific location",
                    "parameters": {
                        "location_name": "string - Name of the location (e.g., 'Paris, France')"
                    }
                },
                {
                    "name": "find_places_by_emotion",
                    "description": "Find locations that strongly evoke a specific emotion (joy, peace, excitement, etc.)",
                    "parameters": {
                        "emotion": "string - Target emotion (joy, peace, excitement, inspiration, nostalgia, stress)",
                        "min_intensity": "integer - Minimum emotion score (0-100, default 70)"
                    }
                },
                {
                    "name": "get_emotional_heatmap",
                    "description": "Generate emotional intensity data for multiple locations in a region for comparison",
                    "parameters": {
                        "locations": "array - List of location names to analyze",
                        "emotion_filter": "string - Optional: filter by specific emotion"
                    }
                }
            ]
        }
    
    def get_location_emotions(self, location_name: str) -> Dict[str, Any]:
        """
        Get the emotional profile of a specific location.
        
        Args:
            location_name: Name of the location
            
        Returns:
            Emotional data and analysis
        """
        # Find location in database
        location_data = self.emotional_database.get(location_name)
        
        if not location_data:
            # Try fuzzy matching
            location_key = self._find_similar_location(location_name)
            if location_key:
                location_data = self.emotional_database[location_key]
                location_name = location_key
            else:
                return {
                    "success": False,
                    "error": f"Location '{location_name}' not found in emotional database",
                    "available_locations": list(self.emotional_database.keys())
                }
        
        # Determine dominant emotion
        emotions = location_data["emotions"]
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])
        
        # Calculate overall sentiment intensity
        sentiment_intensity = sum(emotions.values()) / len(emotions)
        
        # Generate emotional insights
        insights = self._generate_emotional_insights(emotions)
        
        result = {
            "success": True,
            "location": {
                "name": location_name,
                "coordinates": {
                    "latitude": location_data["lat"],
                    "longitude": location_data["lon"]
                }
            },
            "emotional_profile": {
                "dominant_emotion": dominant_emotion[0],
                "dominant_score": dominant_emotion[1],
                "all_emotions": emotions,
                "overall_intensity": round(sentiment_intensity, 2)
            },
            "insights": insights,
            "sample_sentiments": location_data["descriptions"],
            "emotion_categories": {
                "positive": ["joy", "excitement", "inspiration", "peace"],
                "challenging": ["stress", "fear", "sadness"],
                "reflective": ["nostalgia", "peace"]
            }
        }
        
        return result
    
    def find_places_by_emotion(self, emotion: str, min_intensity: int = 70) -> Dict[str, Any]:
        """
        Find locations that evoke a specific emotion.
        
        Args:
            emotion: Target emotion to search for
            min_intensity: Minimum emotion score (0-100)
            
        Returns:
            List of matching locations
        """
        emotion = emotion.lower()
        
        # Validate emotion
        valid_emotions = ["joy", "sadness", "excitement", "fear", "peace", 
                         "nostalgia", "inspiration", "stress"]
        if emotion not in valid_emotions:
            return {
                "success": False,
                "error": f"Unknown emotion '{emotion}'",
                "valid_emotions": valid_emotions
            }
        
        # Search through database
        matching_locations = []
        
        for location_name, data in self.emotional_database.items():
            emotion_score = data["emotions"].get(emotion, 0)
            if emotion_score >= min_intensity:
                matching_locations.append({
                    "location": location_name,
                    "coordinates": {
                        "latitude": data["lat"],
                        "longitude": data["lon"]
                    },
                    "emotion_score": emotion_score,
                    "sample_description": data["descriptions"][0] if data["descriptions"] else ""
                })
        
        # Sort by emotion score
        matching_locations.sort(key=lambda x: x["emotion_score"], reverse=True)
        
        result = {
            "success": True,
            "emotion_query": emotion,
            "min_intensity": min_intensity,
            "total_matches": len(matching_locations),
            "locations": matching_locations,
            "recommendation": self._generate_emotion_recommendation(emotion, matching_locations)
        }
        
        return result
    
    def get_emotional_heatmap(self, locations: List[str], 
                             emotion_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate emotional intensity data for multiple locations.
        
        Args:
            locations: List of location names
            emotion_filter: Optional specific emotion to focus on
            
        Returns:
            Comparative emotional data
        """
        heatmap_data = []
        
        for location_name in locations:
            location_data = self.emotional_database.get(location_name)
            
            if location_data:
                if emotion_filter:
                    intensity = location_data["emotions"].get(emotion_filter.lower(), 0)
                else:
                    # Use average of all emotions
                    intensity = sum(location_data["emotions"].values()) / len(location_data["emotions"])
                
                heatmap_data.append({
                    "location": location_name,
                    "latitude": location_data["lat"],
                    "longitude": location_data["lon"],
                    "intensity": round(intensity, 2),
                    "emotions": location_data["emotions"] if not emotion_filter else {emotion_filter: intensity}
                })
        
        # Calculate statistics
        if heatmap_data:
            intensities = [point["intensity"] for point in heatmap_data]
            stats = {
                "max": max(intensities),
                "min": min(intensities),
                "average": round(sum(intensities) / len(intensities), 2),
                "range": max(intensities) - min(intensities)
            }
        else:
            stats = None
        
        result = {
            "success": True,
            "emotion_filter": emotion_filter or "overall",
            "heatmap_points": heatmap_data,
            "statistics": stats,
            "visualization_ready": True
        }
        
        return result
    
    def _find_similar_location(self, query: str) -> Optional[str]:
        """Find similar location names (simple string matching)"""
        query_lower = query.lower()
        for location in self.emotional_database.keys():
            if query_lower in location.lower() or location.lower() in query_lower:
                return location
        return None
    
    def _generate_emotional_insights(self, emotions: Dict[str, float]) -> List[str]:
        """Generate human-readable insights from emotion scores"""
        insights = []
        
        # Check for high positive emotions
        positive_emotions = {k: v for k, v in emotions.items() 
                           if k in ["joy", "excitement", "inspiration", "peace"] and v >= 70}
        if positive_emotions:
            top_positive = max(positive_emotions.items(), key=lambda x: x[1])
            insights.append(f"This location is particularly known for evoking {top_positive[0]} (score: {top_positive[1]})")
        
        # Check for high stress
        if emotions.get("stress", 0) >= 60:
            insights.append("This is a high-energy location that can be stimulating but sometimes overwhelming")
        
        # Check for balance
        emotion_range = max(emotions.values()) - min(emotions.values())
        if emotion_range < 30:
            insights.append("Visitors report a balanced emotional experience across different dimensions")
        
        # Check for peace
        if emotions.get("peace", 0) >= 80:
            insights.append("Ideal destination for those seeking tranquility and relaxation")
        
        return insights
    
    def _generate_emotion_recommendation(self, emotion: str, locations: List[Dict]) -> str:
        """Generate a recommendation based on emotion search"""
        if not locations:
            return f"No locations found with strong {emotion} ratings. Try lowering the minimum intensity."
        
        top_location = locations[0]
        return (f"For the strongest {emotion} experience, consider visiting {top_location['location']} "
               f"(emotion score: {top_location['emotion_score']})")


# MCP Tool definitions
def create_emotional_geography_tools():
    """Create tool definitions for the Emotional Geography Server"""
    server = EmotionalGeographyServer()
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_location_emotions",
                "description": "Retrieve the emotional profile and sentiment analysis for a specific location. Understand how people feel about a place based on aggregated data from reviews and social sentiment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location_name": {
                            "type": "string",
                            "description": "Name of the location to analyze (e.g., 'Paris, France', 'Tokyo, Japan')"
                        }
                    },
                    "required": ["location_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_places_by_emotion",
                "description": "Find travel destinations that evoke a specific emotion. Perfect for planning trips based on desired emotional experiences - seeking peace, excitement, inspiration, etc.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "emotion": {
                            "type": "string",
                            "description": "Target emotion: joy, peace, excitement, inspiration, nostalgia, or stress",
                            "enum": ["joy", "peace", "excitement", "inspiration", "nostalgia", "stress"]
                        },
                        "min_intensity": {
                            "type": "integer",
                            "description": "Minimum emotion score (0-100, default 70)",
                            "default": 70
                        }
                    },
                    "required": ["emotion"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_emotional_heatmap",
                "description": "Generate comparative emotional data for multiple locations. Useful for comparing emotional experiences across different cities or planning routes based on desired emotional journey.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "locations": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of location names to compare"
                        },
                        "emotion_filter": {
                            "type": "string",
                            "description": "Optional: focus on specific emotion for comparison"
                        }
                    },
                    "required": ["locations"]
                }
            }
        }
    ]
    
    return server, tools


if __name__ == "__main__":
    # Demo the server
    server = EmotionalGeographyServer()
    
    print("=== Emotional Geography Map Server Demo ===\n")
    print(json.dumps(server.get_server_info(), indent=2))
    
    print("\n\n=== Example 1: Get emotions for Paris ===")
    result1 = server.get_location_emotions("Paris, France")
    print(json.dumps(result1, indent=2))
    
    print("\n\n=== Example 2: Find peaceful places ===")
    result2 = server.find_places_by_emotion("peace", min_intensity=80)
    print(json.dumps(result2, indent=2))
    
    print("\n\n=== Example 3: Compare emotional heatmap ===")
    result3 = server.get_emotional_heatmap(
        ["Paris, France", "Tokyo, Japan", "Reykjavik, Iceland"],
        emotion_filter="peace"
    )
    print(json.dumps(result3, indent=2))
