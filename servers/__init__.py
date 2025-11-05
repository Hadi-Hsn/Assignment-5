"""
MCP Map Servers Package
Innovative map servers demonstrating Model Context Protocol
"""

from .timetravel_map_server import TimeTravelMapServer, create_timetravel_tools
from .emotional_geography_server import EmotionalGeographyServer, create_emotional_geography_tools
from .quantum_navigation_server import QuantumNavigationServer, create_quantum_navigation_tools

__version__ = "1.0.0"
__all__ = [
    "TimeTravelMapServer",
    "create_timetravel_tools",
    "EmotionalGeographyServer", 
    "create_emotional_geography_tools",
    "QuantumNavigationServer",
    "create_quantum_navigation_tools"
]
