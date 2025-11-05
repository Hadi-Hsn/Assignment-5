"""
Quantum Navigation Map Server - A Creative MCP Server for Probabilistic Routing

This server provides probabilistic routing with multiple path alternatives,
confidence scores, and real-time adaptability. Think of it as "quantum" because
it considers multiple possible routes simultaneously and collapses to the best
option based on various factors.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import math
import random


class RouteMode(Enum):
    """Different routing optimization modes"""
    FASTEST = "fastest"
    SCENIC = "scenic"
    SAFEST = "safest"
    ADVENTUROUS = "adventurous"
    EFFICIENT = "efficient"


@dataclass
class PathSegment:
    """Represents a segment of a route"""
    from_point: str
    to_point: str
    distance_km: float
    estimated_time_min: int
    confidence: float  # 0-1
    conditions: List[str]


@dataclass
class QuantumRoute:
    """Represents a probabilistic route with uncertainty"""
    route_id: str
    segments: List[PathSegment]
    total_distance_km: float
    total_time_min: int
    overall_confidence: float
    risk_factors: List[str]
    advantages: List[str]


class QuantumNavigationServer:
    """
    MCP Server for probabilistic navigation and routing.
    
    Operations:
    1. calculate_quantum_routes: Calculate multiple probabilistic routes between locations
    2. evaluate_route_confidence: Analyze confidence and risk factors for a specific route
    3. adaptive_reroute: Suggest route adaptations based on real-time conditions
    """
    
    def __init__(self):
        self.server_name = "Quantum Navigation Map Server"
        self.version = "1.0.0"
        
        # Simulated road network with uncertainty factors
        self.route_network = {
            ("Beirut", "Byblos"): {
                "routes": [
                    {
                        "name": "Coastal Highway",
                        "distance": 37,
                        "base_time": 45,
                        "confidence": 0.75,
                        "factors": ["Beach traffic", "Power cuts possible", "Coastal congestion"],
                        "advantages": ["Scenic Mediterranean views", "Multiple stops available"]
                    },
                    {
                        "name": "Mountain Route",
                        "distance": 42,
                        "base_time": 55,
                        "confidence": 0.85,
                        "factors": ["Winding roads", "Weather dependent"],
                        "advantages": ["Avoids coastal traffic", "Beautiful mountain scenery"]
                    }
                ]
            },
            ("AUB Campus", "Downtown Beirut"): {
                "routes": [
                    {
                        "name": "Hamra-Bliss Route",
                        "distance": 3,
                        "base_time": 15,
                        "confidence": 0.60,
                        "factors": ["Heavy traffic", "Demonstrations possible", "Power cuts affect lights"],
                        "advantages": ["Most direct", "Many alternative paths"]
                    },
                    {
                        "name": "Corniche Route",
                        "distance": 4,
                        "base_time": 20,
                        "confidence": 0.80,
                        "factors": ["Pedestrian traffic", "Weather dependent"],
                        "advantages": ["Scenic sea views", "Walkable", "Less congested"]
                    }
                ]
            },
            ("AUB Main Gate", "Downtown Beirut"): {
                "routes": [
                    {
                        "name": "Hamra-Bliss Route",
                        "distance": 3,
                        "base_time": 15,
                        "confidence": 0.60,
                        "factors": ["Heavy traffic", "Demonstrations possible", "Power cuts affect lights"],
                        "advantages": ["Most direct", "Many alternative paths"]
                    },
                    {
                        "name": "Corniche Route",
                        "distance": 4,
                        "base_time": 20,
                        "confidence": 0.80,
                        "factors": ["Pedestrian traffic", "Weather dependent"],
                        "advantages": ["Scenic sea views", "Walkable", "Less congested"]
                    }
                ]
            },
            ("Hamra", "Downtown Beirut"): {
                "routes": [
                    {
                        "name": "Hamra Street Direct",
                        "distance": 2,
                        "base_time": 12,
                        "confidence": 0.65,
                        "factors": ["Heavy traffic", "Street vendors", "Power cuts"],
                        "advantages": ["Shortest route", "Many shops"]
                    },
                    {
                        "name": "Verdun Route",
                        "distance": 3,
                        "base_time": 18,
                        "confidence": 0.75,
                        "factors": ["Shopping traffic", "One-way streets"],
                        "advantages": ["Less congested", "Better road quality"]
                    }
                ]
            },
            ("Beirut", "Tripoli"): {
                "routes": [
                    {
                        "name": "Coastal Highway North",
                        "distance": 85,
                        "base_time": 90,
                        "confidence": 0.70,
                        "factors": ["Traffic checkpoints", "Road quality varies", "Power cuts"],
                        "advantages": ["Direct route", "Coastal scenery"]
                    },
                    {
                        "name": "Mountain Highway",
                        "distance": 95,
                        "base_time": 110,
                        "confidence": 0.75,
                        "factors": ["Mountain weather", "Winding roads"],
                        "advantages": ["Cooler in summer", "Less traffic"]
                    }
                ]
            },
            ("Beirut", "Zahle"): {
                "routes": [
                    {
                        "name": "Damascus Road",
                        "distance": 54,
                        "base_time": 65,
                        "confidence": 0.82,
                        "factors": ["Mountain pass", "Checkpoint delays"],
                        "advantages": ["Scenic Bekaa Valley", "Good road condition"]
                    }
                ]
            },
            ("New York", "Boston"): {
                "routes": [
                    {
                        "name": "I-95 Express",
                        "distance": 346,
                        "base_time": 240,
                        "confidence": 0.85,
                        "factors": ["Highway traffic", "Construction zones"],
                        "advantages": ["Fastest under normal conditions", "Multiple service areas"]
                    },
                    {
                        "name": "Coastal Route 1",
                        "distance": 412,
                        "base_time": 320,
                        "confidence": 0.92,
                        "factors": ["Weather dependent", "Seasonal traffic"],
                        "advantages": ["Scenic views", "Charming coastal towns"]
                    },
                    {
                        "name": "Inland Alternate",
                        "distance": 368,
                        "base_time": 280,
                        "confidence": 0.78,
                        "factors": ["Less direct", "Variable conditions"],
                        "advantages": ["Avoids major highways", "Lower traffic"]
                    }
                ]
            },
            ("San Francisco", "Los Angeles"): {
                "routes": [
                    {
                        "name": "I-5 Direct",
                        "distance": 615,
                        "base_time": 360,
                        "confidence": 0.90,
                        "factors": ["Monotonous", "High truck traffic"],
                        "advantages": ["Fastest route", "Straightforward navigation"]
                    },
                    {
                        "name": "Highway 1 Pacific Coast",
                        "distance": 750,
                        "base_time": 600,
                        "confidence": 0.75,
                        "factors": ["Weather closures", "Winding roads", "Fog risk"],
                        "advantages": ["Breathtaking scenery", "Tourist attractions", "Beach access"]
                    },
                    {
                        "name": "Highway 101 Moderate",
                        "distance": 680,
                        "base_time": 450,
                        "confidence": 0.88,
                        "factors": ["Small town traffic", "Variable speed limits"],
                        "advantages": ["Balanced route", "Wine country", "Good services"]
                    }
                ]
            },
            ("London", "Edinburgh"): {
                "routes": [
                    {
                        "name": "M1/A1(M) Motorway",
                        "distance": 665,
                        "base_time": 420,
                        "confidence": 0.82,
                        "factors": ["Roadworks common", "Weather in North"],
                        "advantages": ["Most direct", "Good infrastructure"]
                    },
                    {
                        "name": "A1 Scenic",
                        "distance": 685,
                        "base_time": 480,
                        "confidence": 0.88,
                        "factors": ["Smaller roads", "Village traffic"],
                        "advantages": ["Historic sites", "Traditional villages", "Varied scenery"]
                    }
                ]
            }
        }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Return MCP server information"""
        return {
            "name": self.server_name,
            "version": self.version,
            "description": "Navigate with uncertainty - explore multiple route possibilities with confidence scores and adaptive suggestions",
            "tools": [
                {
                    "name": "calculate_quantum_routes",
                    "description": "Calculate multiple probabilistic routes between two locations with confidence scores and trade-offs",
                    "parameters": {
                        "origin": "string - Starting location",
                        "destination": "string - Target destination",
                        "mode": "string - Routing preference (fastest, scenic, safest, adventurous, efficient)",
                        "risk_tolerance": "float - How much uncertainty to accept (0.0-1.0, default 0.5)"
                    }
                },
                {
                    "name": "evaluate_route_confidence",
                    "description": "Deep analysis of a route's confidence level, risk factors, and success probability",
                    "parameters": {
                        "origin": "string - Starting location",
                        "destination": "string - Target destination",
                        "route_name": "string - Specific route to evaluate"
                    }
                },
                {
                    "name": "adaptive_reroute",
                    "description": "Suggest route adaptations based on changing conditions and live factors",
                    "parameters": {
                        "current_location": "string - Current position",
                        "destination": "string - Target destination",
                        "conditions": "array - Current condition factors (traffic, weather, etc.)"
                    }
                }
            ]
        }
    
    def calculate_quantum_routes(self, origin: str, destination: str, 
                                 mode: str = "efficient",
                                 risk_tolerance: float = 0.5) -> Dict[str, Any]:
        """
        Calculate multiple probabilistic routes between locations.
        
        Args:
            origin: Starting location
            destination: Target destination
            mode: Routing preference
            risk_tolerance: Acceptable uncertainty level (0-1)
            
        Returns:
            Multiple route options with probabilities
        """
        # Find route pair
        route_key = self._find_route_key(origin, destination)
        
        if not route_key:
            return {
                "success": False,
                "error": f"No routes found between '{origin}' and '{destination}'",
                "available_routes": self._get_available_route_pairs()
            }
        
        route_data = self.route_network[route_key]
        routes = route_data["routes"]
        
        # Apply mode preferences and risk tolerance
        scored_routes = []
        for route in routes:
            score = self._calculate_route_score(route, mode, risk_tolerance)
            
            # Add uncertainty modeling
            time_variance = self._calculate_time_uncertainty(route)
            
            scored_routes.append({
                "route_name": route["name"],
                "distance_km": route["distance"],
                "estimated_time_min": route["base_time"],
                "time_range": {
                    "optimistic": route["base_time"] - time_variance,
                    "expected": route["base_time"],
                    "pessimistic": route["base_time"] + time_variance
                },
                "confidence_score": route["confidence"],
                "suitability_score": round(score, 2),
                "risk_factors": route["factors"],
                "advantages": route["advantages"],
                "quantum_state": self._generate_quantum_state(route["confidence"])
            })
        
        # Sort by suitability
        scored_routes.sort(key=lambda x: x["suitability_score"], reverse=True)
        
        result = {
            "success": True,
            "origin": origin,
            "destination": destination,
            "routing_mode": mode,
            "risk_tolerance": risk_tolerance,
            "total_routes_analyzed": len(scored_routes),
            "routes": scored_routes,
            "recommendation": self._generate_route_recommendation(scored_routes[0], mode),
            "quantum_analysis": {
                "explanation": "Multiple route 'states' exist simultaneously until you choose. Each has different probabilities of being optimal based on conditions.",
                "superposition_count": len(scored_routes)
            }
        }
        
        return result
    
    def evaluate_route_confidence(self, origin: str, destination: str, 
                                  route_name: str) -> Dict[str, Any]:
        """
        Perform deep analysis of a specific route's confidence.
        
        Args:
            origin: Starting location
            destination: Target destination
            route_name: Name of specific route to analyze
            
        Returns:
            Detailed confidence analysis
        """
        route_key = self._find_route_key(origin, destination)
        
        if not route_key:
            return {
                "success": False,
                "error": "Route not found"
            }
        
        # Find specific route
        routes = self.route_network[route_key]["routes"]
        target_route = None
        for route in routes:
            if route["name"].lower() == route_name.lower():
                target_route = route
                break
        
        if not target_route:
            return {
                "success": False,
                "error": f"Route '{route_name}' not found",
                "available_routes": [r["name"] for r in routes]
            }
        
        # Detailed confidence breakdown
        confidence_factors = self._analyze_confidence_factors(target_route)
        success_probability = self._calculate_success_probability(target_route)
        
        result = {
            "success": True,
            "route": {
                "name": target_route["name"],
                "origin": origin,
                "destination": destination
            },
            "overall_confidence": target_route["confidence"],
            "success_probability": round(success_probability, 3),
            "confidence_breakdown": confidence_factors,
            "risk_assessment": {
                "level": self._get_risk_level(target_route["confidence"]),
                "factors": target_route["factors"],
                "mitigation_strategies": self._suggest_mitigations(target_route["factors"])
            },
            "timing_reliability": {
                "on_time_probability": round(target_route["confidence"] * 0.9, 2),
                "delay_likelihood": round(1 - target_route["confidence"], 2),
                "expected_variance_min": self._calculate_time_uncertainty(target_route)
            }
        }
        
        return result
    
    def adaptive_reroute(self, current_location: str, destination: str,
                        conditions: List[str]) -> Dict[str, Any]:
        """
        Suggest route adaptations based on current conditions.
        
        Args:
            current_location: Current position
            destination: Target destination
            conditions: Current condition factors
            
        Returns:
            Adaptive routing suggestions
        """
        # Analyze conditions
        condition_severity = self._analyze_conditions(conditions)
        
        # Find applicable routes
        route_key = self._find_route_key(current_location, destination)
        
        if not route_key:
            return {
                "success": False,
                "error": "No routes available for rerouting"
            }
        
        routes = self.route_network[route_key]["routes"]
        
        # Re-score routes based on current conditions
        adapted_routes = []
        for route in routes:
            # Adjust confidence based on conditions
            adjusted_confidence = self._adjust_confidence_for_conditions(
                route, conditions
            )
            
            impact = self._calculate_condition_impact(route, conditions)
            
            adapted_routes.append({
                "route_name": route["name"],
                "original_confidence": route["confidence"],
                "adjusted_confidence": round(adjusted_confidence, 2),
                "confidence_change": round(adjusted_confidence - route["confidence"], 2),
                "estimated_time": route["base_time"] + impact["time_delta"],
                "condition_impact": impact,
                "recommendation": self._get_adaptation_recommendation(
                    route, adjusted_confidence, impact
                )
            })
        
        # Sort by adjusted confidence
        adapted_routes.sort(key=lambda x: x["adjusted_confidence"], reverse=True)
        
        result = {
            "success": True,
            "current_location": current_location,
            "destination": destination,
            "current_conditions": conditions,
            "condition_severity": condition_severity,
            "adapted_routes": adapted_routes,
            "best_option": adapted_routes[0],
            "quantum_collapse": {
                "explanation": "Based on current conditions, the quantum superposition of routes has collapsed to favor the most reliable option",
                "confidence_shift": f"Conditions shifted route preferences by up to {max(abs(r['confidence_change']) for r in adapted_routes):.0%}"
            }
        }
        
        return result
    
    def _find_route_key(self, origin: str, destination: str) -> Optional[Tuple[str, str]]:
        """Find route key in network (handles both directions)"""
        for key in self.route_network.keys():
            if (key[0].lower() in origin.lower() and key[1].lower() in destination.lower()) or \
               (key[1].lower() in origin.lower() and key[0].lower() in destination.lower()):
                return key
        return None
    
    def _get_available_route_pairs(self) -> List[str]:
        """Get list of available route pairs"""
        return [f"{origin} ↔ {dest}" for origin, dest in self.route_network.keys()]
    
    def _calculate_route_score(self, route: Dict, mode: str, risk_tolerance: float) -> float:
        """Calculate route suitability score based on mode and risk tolerance"""
        base_score = route["confidence"] * 100
        
        # Adjust based on mode
        if mode == "fastest":
            # Prefer shorter times
            time_score = 100 / (1 + route["base_time"] / 100)
            return base_score * 0.4 + time_score * 0.6
        elif mode == "scenic":
            # Check for scenic advantages
            scenic_bonus = 20 if any("scenic" in adv.lower() or "view" in adv.lower() 
                                    for adv in route["advantages"]) else 0
            return base_score * 0.5 + scenic_bonus + (route["distance"] / 10)
        elif mode == "safest":
            # Heavily weight confidence
            return route["confidence"] * 120
        elif mode == "adventurous":
            # Prefer lower confidence (more uncertainty = more adventure!)
            return (1 - route["confidence"]) * 80 + len(route["factors"]) * 10
        else:  # efficient
            # Balance all factors
            efficiency = (route["confidence"] * 50) + (100 / (1 + route["base_time"] / 200))
            return efficiency
    
    def _calculate_time_uncertainty(self, route: Dict) -> int:
        """Calculate time variance based on confidence"""
        base_variance = route["base_time"] * 0.15  # 15% base variance
        confidence_factor = (1 - route["confidence"])
        return int(base_variance * (1 + confidence_factor * 2))
    
    def _generate_quantum_state(self, confidence: float) -> str:
        """Generate quantum state description"""
        if confidence >= 0.9:
            return "|reliable⟩"
        elif confidence >= 0.8:
            return "0.8|reliable⟩ + 0.2|uncertain⟩"
        elif confidence >= 0.7:
            return "0.7|reliable⟩ + 0.3|uncertain⟩"
        else:
            return "0.6|reliable⟩ + 0.4|uncertain⟩"
    
    def _generate_route_recommendation(self, route: Dict, mode: str) -> str:
        """Generate human-readable recommendation"""
        return (f"Based on {mode} mode, '{route['route_name']}' is your best option "
               f"with {route['confidence_score']:.0f}% suitability and "
               f"{route['confidence_score']:.0%} confidence.")
    
    def _analyze_confidence_factors(self, route: Dict) -> Dict[str, float]:
        """Break down confidence into component factors"""
        return {
            "route_infrastructure": round(route["confidence"] + random.uniform(-0.05, 0.05), 2),
            "historical_reliability": round(route["confidence"] + random.uniform(-0.08, 0.02), 2),
            "weather_independence": round(route["confidence"] - len(route["factors"]) * 0.05, 2),
            "navigation_clarity": round(0.85 + random.uniform(-0.1, 0.1), 2)
        }
    
    def _calculate_success_probability(self, route: Dict) -> float:
        """Calculate probability of successful journey"""
        return route["confidence"] * (1 - len(route["factors"]) * 0.03)
    
    def _get_risk_level(self, confidence: float) -> str:
        """Categorize risk level"""
        if confidence >= 0.85:
            return "LOW"
        elif confidence >= 0.75:
            return "MODERATE"
        else:
            return "ELEVATED"
    
    def _suggest_mitigations(self, factors: List[str]) -> List[str]:
        """Suggest risk mitigation strategies"""
        mitigations = []
        for factor in factors:
            if "traffic" in factor.lower():
                mitigations.append("Check live traffic before departure and during journey")
            if "weather" in factor.lower():
                mitigations.append("Monitor weather forecasts and have backup timing")
            if "construction" in factor.lower():
                mitigations.append("Use real-time navigation apps for construction updates")
        return mitigations if mitigations else ["Monitor conditions regularly", "Allow extra time"]
    
    def _analyze_conditions(self, conditions: List[str]) -> str:
        """Analyze severity of current conditions"""
        if len(conditions) >= 3:
            return "HIGH"
        elif len(conditions) >= 2:
            return "MODERATE"
        else:
            return "LOW"
    
    def _adjust_confidence_for_conditions(self, route: Dict, conditions: List[str]) -> float:
        """Adjust route confidence based on current conditions"""
        adjusted = route["confidence"]
        
        for condition in conditions:
            # Check if condition affects this route
            for factor in route["factors"]:
                if any(word in factor.lower() for word in condition.lower().split()):
                    adjusted -= 0.1  # Reduce confidence
        
        return max(0.4, min(1.0, adjusted))  # Clamp between 0.4 and 1.0
    
    def _calculate_condition_impact(self, route: Dict, conditions: List[str]) -> Dict[str, Any]:
        """Calculate impact of conditions on route"""
        time_delta = 0
        severity = "minimal"
        
        matching_factors = sum(1 for cond in conditions 
                             if any(cond.lower() in factor.lower() 
                                   for factor in route["factors"]))
        
        if matching_factors >= 2:
            time_delta = int(route["base_time"] * 0.25)
            severity = "significant"
        elif matching_factors == 1:
            time_delta = int(route["base_time"] * 0.1)
            severity = "moderate"
        
        return {
            "time_delta": time_delta,
            "severity": severity,
            "affected_factors": matching_factors
        }
    
    def _get_adaptation_recommendation(self, route: Dict, adjusted_confidence: float,
                                      impact: Dict) -> str:
        """Generate adaptation recommendation"""
        if adjusted_confidence >= 0.8:
            return f"Continue with {route['name']} - still reliable despite conditions"
        elif adjusted_confidence >= 0.65:
            return f"{route['name']} usable but expect delays of ~{impact['time_delta']} minutes"
        else:
            return f"Consider alternative to {route['name']} due to current conditions"


# MCP Tool definitions
def create_quantum_navigation_tools():
    """Create tool definitions for the Quantum Navigation Server"""
    server = QuantumNavigationServer()
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_quantum_routes",
                "description": "Calculate multiple probabilistic routes between locations with confidence scores, time ranges, and trade-off analysis. Perfect for understanding all your routing options.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Starting location (e.g., 'New York', 'San Francisco')"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Target destination"
                        },
                        "mode": {
                            "type": "string",
                            "description": "Routing preference",
                            "enum": ["fastest", "scenic", "safest", "adventurous", "efficient"],
                            "default": "efficient"
                        },
                        "risk_tolerance": {
                            "type": "number",
                            "description": "Acceptable uncertainty level (0.0-1.0, default 0.5)",
                            "default": 0.5
                        }
                    },
                    "required": ["origin", "destination"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "evaluate_route_confidence",
                "description": "Perform deep analysis of a specific route's reliability, including success probability, risk factors, and timing variance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Starting location"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Target destination"
                        },
                        "route_name": {
                            "type": "string",
                            "description": "Name of specific route to analyze"
                        }
                    },
                    "required": ["origin", "destination", "route_name"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "adaptive_reroute",
                "description": "Get dynamic route recommendations based on current conditions like traffic, weather, or road closures. Routes adapt to reality in real-time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "current_location": {
                            "type": "string",
                            "description": "Current position"
                        },
                        "destination": {
                            "type": "string",
                            "description": "Target destination"
                        },
                        "conditions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Current conditions (e.g., ['heavy traffic', 'rain', 'construction'])"
                        }
                    },
                    "required": ["current_location", "destination", "conditions"]
                }
            }
        }
    ]
    
    return server, tools


if __name__ == "__main__":
    # Demo the server
    server = QuantumNavigationServer()
    
    print("=== Quantum Navigation Map Server Demo ===\n")
    print(json.dumps(server.get_server_info(), indent=2))
    
    print("\n\n=== Example 1: Calculate routes NYC to Boston ===")
    result1 = server.calculate_quantum_routes("New York", "Boston", mode="efficient")
    print(json.dumps(result1, indent=2))
    
    print("\n\n=== Example 2: Evaluate route confidence ===")
    result2 = server.evaluate_route_confidence("New York", "Boston", "I-95 Express")
    print(json.dumps(result2, indent=2))
    
    print("\n\n=== Example 3: Adaptive rerouting ===")
    result3 = server.adaptive_reroute("New York", "Boston", ["heavy traffic", "construction"])
    print(json.dumps(result3, indent=2))
