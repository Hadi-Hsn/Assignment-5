"""
Flask Web Application for MCP Map Servers Demo
Provides an interactive web interface to demonstrate all three map servers
"""

from flask import Flask, render_template, request, jsonify
import sys
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add servers directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'servers'))

from timetravel_map_server import TimeTravelMapServer
from emotional_geography_server import EmotionalGeographyServer
from quantum_navigation_server import QuantumNavigationServer
from weather_server import WeatherServer
from fetch_server import FetchServer

app = Flask(__name__)

# Initialize all servers
timetravel_server = TimeTravelMapServer()
emotional_server = EmotionalGeographyServer()
quantum_server = QuantumNavigationServer()
weather_server = WeatherServer()
fetch_server = FetchServer()  # Official MCP Fetch Server

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def index():
    """Render the main demo page"""
    return render_template('index.html')

@app.route('/api/servers')
def get_servers():
    """Get information about all available servers"""
    return jsonify({
        'servers': [
            timetravel_server.get_server_info(),
            emotional_server.get_server_info(),
            quantum_server.get_server_info(),
            {
                'name': 'Lebanese Weather Server',
                'version': weather_server.version,
                'description': 'Provides weather information for Lebanese cities and mountain resorts',
                'operations': 4
            },
            {
                'name': 'MCP Fetch Server (Official)',
                'version': fetch_server.version,
                'description': 'Official MCP server for fetching web content',
                'operations': 2,
                'source': 'github.com/modelcontextprotocol/servers'
            }
        ]
    })

# TimeTravel Map Server Endpoints
@app.route('/api/timetravel/geocode', methods=['POST'])
def timetravel_geocode():
    """Geocode a location at a specific historical time"""
    data = request.json
    location = data.get('location', '')
    year = data.get('year', 2024)
    
    result = timetravel_server.geocode_historical(location, year)
    return jsonify(result)

@app.route('/api/timetravel/timeline', methods=['POST'])
def timetravel_timeline():
    """Get historical timeline for a location"""
    data = request.json
    location = data.get('location', '')
    start_year = data.get('start_year')
    end_year = data.get('end_year')
    
    result = timetravel_server.get_location_timeline(location, start_year, end_year)
    return jsonify(result)

@app.route('/api/timetravel/compare', methods=['POST'])
def timetravel_compare():
    """Compare a location across different eras"""
    data = request.json
    location = data.get('location', '')
    year1 = data.get('year1', 1900)
    year2 = data.get('year2', 2000)
    
    result = timetravel_server.compare_eras(location, year1, year2)
    return jsonify(result)

# Emotional Geography Server Endpoints
@app.route('/api/emotional/location', methods=['POST'])
def emotional_location():
    """Get emotional profile for a location"""
    data = request.json
    location = data.get('location', '')
    
    result = emotional_server.get_location_emotions(location)
    return jsonify(result)

@app.route('/api/emotional/find', methods=['POST'])
def emotional_find():
    """Find places by emotion type"""
    data = request.json
    emotion = data.get('emotion', 'peace')
    min_intensity = data.get('min_intensity', 70)
    
    result = emotional_server.find_places_by_emotion(emotion, min_intensity)
    return jsonify(result)

# Quantum Navigation Server Endpoints
@app.route('/api/quantum/routes', methods=['POST'])
def quantum_routes():
    """Calculate quantum routes between locations"""
    data = request.json
    origin = data.get('origin', '')
    destination = data.get('destination', '')
    mode = data.get('mode', 'driving')
    risk_tolerance = data.get('risk_tolerance', 0.5)
    
    result = quantum_server.calculate_quantum_routes(origin, destination, mode, risk_tolerance)
    return jsonify(result)

@app.route('/api/quantum/confidence', methods=['POST'])
def quantum_confidence():
    """Evaluate confidence for a specific route"""
    data = request.json
    origin = data.get('origin', '')
    destination = data.get('destination', '')
    route_id = data.get('route_id', '')
    
    result = quantum_server.evaluate_route_confidence(origin, destination, route_id)
    return jsonify(result)

@app.route('/api/quantum/reroute', methods=['POST'])
def quantum_reroute():
    """Get adaptive rerouting based on conditions"""
    data = request.json
    origin = data.get('origin', '')
    destination = data.get('destination', '')
    conditions = data.get('conditions', [])
    
    result = quantum_server.adaptive_reroute(origin, destination, conditions)
    return jsonify(result)

# Weather Server Endpoints
@app.route('/api/weather/current', methods=['POST'])
def weather_current():
    """Get current weather for a Lebanese location"""
    data = request.json
    location = data.get('location', '')
    
    result = weather_server.get_current_weather(location)
    return jsonify(result)

@app.route('/api/weather/forecast', methods=['POST'])
def weather_forecast():
    """Get weather forecast for a Lebanese location"""
    data = request.json
    location = data.get('location', '')
    days = data.get('days', 5)
    
    result = weather_server.get_weather_forecast(location, days)
    return jsonify(result)

@app.route('/api/weather/ski', methods=['POST'])
def weather_ski():
    """Get ski conditions for Lebanese mountain resorts"""
    data = request.json
    resort = data.get('resort', '')
    
    result = weather_server.get_ski_conditions(resort)
    return jsonify(result)

@app.route('/api/weather/compare', methods=['POST'])
def weather_compare():
    """Compare weather between two Lebanese locations"""
    data = request.json
    location1 = data.get('location1', '')
    location2 = data.get('location2', '')
    
    result = weather_server.compare_locations(location1, location2)
    return jsonify(result)

# Fetch Server Endpoints (Official MCP Server)
@app.route('/api/fetch', methods=['POST'])
def fetch_url():
    """Fetch content from a URL"""
    data = request.json
    url = data.get('url', '')
    max_length = data.get('max_length', 5000)
    start_index = data.get('start_index', 0)
    raw = data.get('raw', False)
    
    result = fetch_server.fetch(url, max_length, start_index, raw)
    return jsonify(result)

@app.route('/api/fetch/multiple', methods=['POST'])
def fetch_multiple():
    """Fetch multiple URLs"""
    data = request.json
    urls = data.get('urls', [])
    max_length = data.get('max_length', 5000)
    
    result = fetch_server.fetch_multiple(urls, max_length)
    return jsonify(result)

# LLM Chat Interface
@app.route('/api/chat', methods=['POST'])
def chat():
    """Process natural language queries using OpenAI"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Define available tools for function calling
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "geocode_historical",
                    "description": "Get geographic information about a location at a specific point in history",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The location name"},
                            "year": {"type": "integer", "description": "The year in history"}
                        },
                        "required": ["location", "year"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_location_timeline",
                    "description": "Get the historical timeline of events for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The location name"}
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_location_emotions",
                    "description": "Get the emotional profile and sentiment data for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The location name"}
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "find_places_by_emotion",
                    "description": "Find places that match a specific emotion or feeling",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "emotion": {"type": "string", "description": "The emotion to search for (peace, joy, inspiration, etc.)"},
                            "min_intensity": {"type": "integer", "description": "Minimum intensity score (0-100)", "default": 70}
                        },
                        "required": ["emotion"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_quantum_routes",
                    "description": "Calculate multiple route options with probability scores between two locations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {"type": "string", "description": "Starting location"},
                            "destination": {"type": "string", "description": "Destination location"},
                            "mode": {"type": "string", "enum": ["driving", "walking", "transit"], "default": "driving"}
                        },
                        "required": ["origin", "destination"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get current weather conditions for a Lebanese city or region (Beirut, Faraya, AUB, Tripoli, Zahle, Byblos, Cedars, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "City name (e.g., beirut, faraya, zahle, aub)"}
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather_forecast",
                    "description": "Get 5-day weather forecast for a Lebanese location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "City name (e.g., beirut, tripoli, byblos)"},
                            "days": {"type": "integer", "description": "Number of days (1-5)", "default": 5}
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_ski_conditions",
                    "description": "Get skiing conditions for Lebanese mountain resorts (Faraya, Cedars)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "resort": {"type": "string", "description": "Ski resort name (faraya, cedars)"}
                        },
                        "required": ["resort"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_web_content",
                    "description": "Fetch and extract content from any website URL (news, articles, information about Lebanon, AUB, etc.)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "description": "The URL to fetch"},
                            "max_length": {"type": "integer", "description": "Maximum characters to return (default: 5000)", "default": 5000}
                        },
                        "required": ["url"]
                    }
                }
            }
        ]
        
        # Call OpenAI with function calling
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are an AI assistant helping users explore Lebanon and the American University of Beirut (AUB) through five specialized servers:
                1. Lebanon Historical Geography - Explore Lebanese heritage from Phoenician times through Ottoman era, French Mandate, to modern Lebanon. Includes AUB campus evolution since 1866.
                2. Beirut Emotional Geography - Discover the emotional character of Lebanese neighborhoods, AUB campus locations, and cultural sites.
                3. Lebanon Smart Navigation - Get reliable routes in Lebanon accounting for power cuts, traffic, infrastructure challenges.
                4. Lebanese Weather Service - Real-time weather for Lebanese cities and ski resorts (Beirut, Faraya, Cedars, AUB, Tripoli, Byblos, Zahle, etc.).
                5. MCP Fetch Server (OFFICIAL) - Fetch real web content about Lebanon, AUB, news, articles from any URL.
                                4. Lebanese Weather Service - Real-time weather for Lebanese cities and ski resorts (Beirut, Faraya, Cedars, AUB, Tripoli, Byblos, Zahle, etc.).
                
                Help users by calling the appropriate functions. Be conversational and provide cultural context about Lebanese locations."""},
                {"role": "user", "content": user_message}
            ],
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        # Check if function calls were made
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            # Execute the appropriate function
            function_result = None
            if function_name == "geocode_historical":
                function_result = timetravel_server.geocode_historical(
                    arguments['location'], 
                    arguments.get('year', 2024)
                )
            elif function_name == "get_location_timeline":
                function_result = timetravel_server.get_location_timeline(
                    arguments['location']
                )
            elif function_name == "get_location_emotions":
                function_result = emotional_server.get_location_emotions(
                    arguments['location']
                )
            elif function_name == "find_places_by_emotion":
                function_result = emotional_server.find_places_by_emotion(
                    arguments['emotion'],
                    arguments.get('min_intensity', 70)
                )
            elif function_name == "calculate_quantum_routes":
                function_result = quantum_server.calculate_quantum_routes(
                    arguments['origin'],
                    arguments['destination'],
                    arguments.get('mode', 'driving')
                )
            elif function_name == "get_current_weather":
                function_result = weather_server.get_current_weather(
                    arguments['location']
                )
            elif function_name == "get_weather_forecast":
                function_result = weather_server.get_weather_forecast(
                    arguments['location'],
                    arguments.get('days', 5)
                )
            elif function_name == "get_ski_conditions":
                function_result = weather_server.get_ski_conditions(
                    arguments['resort']
                )
            elif function_name == "fetch_web_content":
                function_result = fetch_server.fetch(
                    arguments['url'],
                    arguments.get('max_length', 5000)
                )
            
            # Get final response with function result
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """You are an AI assistant helping users interact with three creative map servers.
                    Present the function results in a clear, friendly way. Highlight interesting insights."""},
                    {"role": "user", "content": user_message},
                    message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(function_result)
                    }
                ]
            )
            
            return jsonify({
                'response': second_response.choices[0].message.content,
                'function_called': function_name,
                'function_result': function_result
            })
        else:
            # No function call, just return the message
            return jsonify({
                'response': message.content,
                'function_called': None
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("Lebanon & AUB Map Servers Demo")
    print("="*70)
    print("\n🚀 Starting Flask server...")
    print("📍 Open your browser to: http://localhost:5000")
    print("\n💡 Available Servers:")
    print("   1. Lebanon Historical Geography - From Phoenicia to modern AUB")
    print("   2. Beirut Emotional Geography - Discover Lebanese places by feeling")
    print("   3. Lebanon Smart Navigation - Navigate with local awareness")
    print("   4. Lebanese Weather Service - Climate data for cities & ski resorts")
    print("   5. MCP Fetch Server ⭐ OFFICIAL - Fetch real web content")
    print("\n🎓 American University of Beirut | EECE 798S - Agentic Systems")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5000, use_reloader=False)
