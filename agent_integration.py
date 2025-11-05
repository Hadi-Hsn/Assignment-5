"""
Agent Integration Module
Integrates all three map servers with OpenAI Agents SDK
"""

import json
from typing import Dict, Any, List, Callable
import os
from dotenv import load_dotenv

# Import our map servers
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from servers.timetravel_map_server import TimeTravelMapServer, create_timetravel_tools
from servers.emotional_geography_server import EmotionalGeographyServer, create_emotional_geography_tools
from servers.quantum_navigation_server import QuantumNavigationServer, create_quantum_navigation_tools


class MapServerAgent:
    """
    Unified agent that integrates all map servers.
    This demonstrates MCP concept: one agent, multiple tool servers.
    """
    
    def __init__(self, api_key: str = None):
        """Initialize agent with all map servers"""
        # Load environment variables
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # Initialize all servers
        self.timetravel_server, self.timetravel_tools = create_timetravel_tools()
        self.emotional_server, self.emotional_tools = create_emotional_geography_tools()
        self.quantum_server, self.quantum_tools = create_quantum_navigation_tools()
        
        # Create unified tool registry
        self.tool_registry = self._build_tool_registry()
        
        print("🗺️  Map Server Agent initialized with 3 servers:")
        print(f"   ⏰ TimeTravel Map Server - {len(self.timetravel_tools)} tools")
        print(f"   💭 Emotional Geography Server - {len(self.emotional_tools)} tools")
        print(f"   🔮 Quantum Navigation Server - {len(self.quantum_tools)} tools")
        print(f"   📊 Total tools available: {len(self.tool_registry)}\n")
    
    def _build_tool_registry(self) -> Dict[str, Callable]:
        """Build registry mapping tool names to their execution functions"""
        registry = {}
        
        # TimeTravel tools
        registry['geocode_historical'] = self.timetravel_server.geocode_historical
        registry['get_location_timeline'] = self.timetravel_server.get_location_timeline
        registry['compare_eras'] = self.timetravel_server.compare_eras
        
        # Emotional Geography tools
        registry['get_location_emotions'] = self.emotional_server.get_location_emotions
        registry['find_places_by_emotion'] = self.emotional_server.find_places_by_emotion
        registry['get_emotional_heatmap'] = self.emotional_server.get_emotional_heatmap
        
        # Quantum Navigation tools
        registry['calculate_quantum_routes'] = self.quantum_server.calculate_quantum_routes
        registry['evaluate_route_confidence'] = self.quantum_server.evaluate_route_confidence
        registry['adaptive_reroute'] = self.quantum_server.adaptive_reroute
        
        return registry
    
    def get_all_tools(self) -> List[Dict]:
        """Get all available tools in OpenAI function calling format"""
        return self.timetravel_tools + self.emotional_tools + self.quantum_tools
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name with given parameters.
        This simulates how an AI agent would call MCP tools.
        """
        if tool_name not in self.tool_registry:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(self.tool_registry.keys())
            }
        
        try:
            # Execute the tool
            tool_function = self.tool_registry[tool_name]
            result = tool_function(**kwargs)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}",
                "tool": tool_name
            }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about all connected servers"""
        return {
            "agent_name": "Map Server Agent",
            "mcp_version": "1.0.0",
            "servers": [
                self.timetravel_server.get_server_info(),
                self.emotional_server.get_server_info(),
                self.quantum_server.get_server_info()
            ],
            "total_tools": len(self.tool_registry),
            "capabilities": [
                "Historical geography exploration",
                "Emotional sentiment mapping",
                "Probabilistic route planning"
            ]
        }
    
    def demonstrate_capabilities(self):
        """Run a demonstration of all capabilities"""
        print("=" * 60)
        print("MAP SERVER AGENT - CAPABILITY DEMONSTRATION")
        print("=" * 60)
        
        # Demo 1: TimeTravel
        print("\n📜 DEMO 1: Time Travel - Constantinople through history")
        print("-" * 60)
        result = self.execute_tool('get_location_timeline', location_name='Constantinople')
        if result.get('success'):
            print(f"Location: {result['location']}")
            print(f"Timeline events: {result['total_events']}")
            for event in result['timeline']:
                print(f"  • {event['year']}: {event['name']} - {event['event']}")
        
        # Demo 2: Emotional Geography
        print("\n\n💭 DEMO 2: Emotional Geography - Find peaceful places")
        print("-" * 60)
        result = self.execute_tool('find_places_by_emotion', 
                                   emotion='peace', 
                                   min_intensity=85)
        if result.get('success'):
            print(f"Found {result['total_matches']} peaceful destinations:")
            for loc in result['locations']:
                print(f"  • {loc['location']}: {loc['emotion_score']}/100 peace score")
        
        # Demo 3: Quantum Navigation
        print("\n\n🔮 DEMO 3: Quantum Navigation - NYC to Boston routes")
        print("-" * 60)
        result = self.execute_tool('calculate_quantum_routes',
                                   origin='New York',
                                   destination='Boston',
                                   mode='efficient')
        if result.get('success'):
            print(f"Analyzed {result['total_routes_analyzed']} routes:")
            for route in result['routes'][:2]:  # Show top 2
                print(f"\n  Route: {route['route_name']}")
                print(f"    Distance: {route['distance_km']} km")
                print(f"    Time: {route['estimated_time_min']} min")
                print(f"    Confidence: {route['confidence_score']:.0%}")
                print(f"    Quantum State: {route['quantum_state']}")
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)


def create_sample_queries() -> List[Dict[str, Any]]:
    """Create sample queries that demonstrate agent usage"""
    return [
        {
            "user_query": "What was Constantinople called in 1930?",
            "tool_call": {
                "name": "geocode_historical",
                "parameters": {"location_name": "Constantinople", "year": 1930}
            },
            "explanation": "Using TimeTravel server to explore historical name changes"
        },
        {
            "user_query": "I want to visit somewhere inspiring for my creative retreat",
            "tool_call": {
                "name": "find_places_by_emotion",
                "parameters": {"emotion": "inspiration", "min_intensity": 80}
            },
            "explanation": "Using Emotional Geography to find inspiring destinations"
        },
        {
            "user_query": "What's the fastest route from San Francisco to Los Angeles?",
            "tool_call": {
                "name": "calculate_quantum_routes",
                "parameters": {"origin": "San Francisco", "destination": "Los Angeles", "mode": "fastest"}
            },
            "explanation": "Using Quantum Navigation to find optimal route"
        },
        {
            "user_query": "Compare how Paris makes people feel vs Tokyo",
            "tool_call": {
                "name": "get_emotional_heatmap",
                "parameters": {"locations": ["Paris, France", "Tokyo, Japan"]}
            },
            "explanation": "Using Emotional Geography for comparative analysis"
        },
        {
            "user_query": "How has Berlin changed from 1961 to 1989?",
            "tool_call": {
                "name": "compare_eras",
                "parameters": {"location_name": "Berlin", "year1": 1961, "year2": 1989}
            },
            "explanation": "Using TimeTravel server to analyze historical changes"
        }
    ]


if __name__ == "__main__":
    # Initialize agent
    agent = MapServerAgent()
    
    # Show server information
    print("\n" + "=" * 60)
    print("AGENT INFORMATION")
    print("=" * 60)
    info = agent.get_server_info()
    print(json.dumps(info, indent=2))
    
    # Run demonstrations
    print("\n")
    agent.demonstrate_capabilities()
    
    # Show sample queries
    print("\n\n" + "=" * 60)
    print("SAMPLE QUERY PATTERNS")
    print("=" * 60)
    samples = create_sample_queries()
    for i, sample in enumerate(samples, 1):
        print(f"\n{i}. User Query: \"{sample['user_query']}\"")
        print(f"   Tool: {sample['tool_call']['name']}")
        print(f"   Explanation: {sample['explanation']}")
