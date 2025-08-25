# Weather MCP Server

A comprehensive Model Context Protocol (MCP) server that provides weather information and forecasting capabilities using the Open-Meteo API.

## Features

This MCP server provides the following tools:

- **🌤️ Current Weather**: Get real-time weather conditions for any location
- **📅 Weather Forecast**: Get multi-day weather forecasts (up to 7 days)
- **🔍 Location Search**: Search for cities and locations to get coordinates
- **🏙️ Weather by City**: Get weather directly by city name
- **🚨 Weather Alerts**: Check for weather warnings and severe conditions

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Make the server executable** (optional):
   ```bash
   chmod +x weather_mcp_server.py
   ```

## Usage

### Running the Server

The MCP server can be run in several ways:

#### 1. Direct Python Execution
```bash
python weather_mcp_server.py
```

#### 2. Using MCP CLI (Development Mode)
```bash
mcp dev weather_mcp_server.py
```

#### 3. As an Executable
```bash
./weather_mcp_server.py
```

### Available Tools

#### `get_current_weather(latitude, longitude)`
Get current weather conditions for specific coordinates.

**Parameters:**
- `latitude` (float): Latitude coordinate (-90 to 90)
- `longitude` (float): Longitude coordinate (-180 to 180)

**Example:**
```python
# Get current weather for New York City
get_current_weather(40.7128, -74.0060)
```

#### `get_weather_forecast(latitude, longitude, days=3)`
Get weather forecast for a location.

**Parameters:**
- `latitude` (float): Latitude coordinate (-90 to 90)
- `longitude` (float): Longitude coordinate (-180 to 180)
- `days` (int): Number of forecast days (1-7, default: 3)

**Example:**
```python
# Get 5-day forecast for London
get_weather_forecast(51.5074, -0.1278, days=5)
```

#### `search_location(query, limit=5)`
Search for locations by name to get coordinates.

**Parameters:**
- `query` (str): Location name to search for
- `limit` (int): Maximum results to return (1-10, default: 5)

**Example:**
```python
# Search for Paris
search_location("Paris", limit=3)
```

#### `get_weather_by_city(city_name)`
Get current weather for a city by name (combines location search + weather).

**Parameters:**
- `city_name` (str): Name of the city

**Example:**
```python
# Get weather for Tokyo
get_weather_by_city("Tokyo")
```

#### `get_weather_alerts(latitude, longitude)`
Get weather alerts and warnings for a location.

**Parameters:**
- `latitude` (float): Latitude coordinate (-90 to 90)
- `longitude` (float): Longitude coordinate (-180 to 180)

**Example:**
```python
# Check alerts for Miami
get_weather_alerts(25.7617, -80.1918)
```

## Configuration

### Environment Variables

The server uses the following optional environment variables:

- `LOG_LEVEL`: Set logging level (default: INFO)
- `REQUEST_TIMEOUT`: HTTP request timeout in seconds (default: 30)

### API Information

This server uses the **Open-Meteo API**, which:
- ✅ Requires no API key
- ✅ Is free to use
- ✅ Provides accurate weather data
- ✅ Has good global coverage
- ⚠️ Has rate limits for high usage

## Integration with AI Models

This MCP server is designed to work with AI models that support the Model Context Protocol. When integrated:

1. **Claude/GPT Integration**: The AI can call weather tools naturally in conversation
2. **Automatic Location Resolution**: Users can ask "What's the weather in Paris?" and the server handles location lookup
3. **Rich Formatting**: Weather data is returned in human-readable format with emojis
4. **Error Handling**: Graceful handling of network issues and invalid coordinates

### Example AI Interactions

```
User: "What's the weather like in Tokyo right now?"
AI: [Calls get_weather_by_city("Tokyo")]

User: "Give me a 5-day forecast for coordinates 40.7128, -74.0060"
AI: [Calls get_weather_forecast(40.7128, -74.0060, days=5)]

User: "Are there any weather alerts for Miami?"
AI: [Calls get_weather_alerts(25.7617, -80.1918)]
```

## Development

### Project Structure
```
weather-mcp-server/
├── weather_mcp_server.py    # Main server implementation
├── requirements.txt         # Python dependencies
└── README.md               # This documentation
```

### Adding New Features

To extend the server with additional weather tools:

1. **Add new tool function** with `@mcp.tool()` decorator
2. **Include proper type hints** and docstrings
3. **Handle errors gracefully** using the `make_request()` helper
4. **Format output consistently** with emojis and clear structure

### Testing

Test the server locally:

```bash
# Start in development mode
mcp dev weather_mcp_server.py

# Test individual tools
python -c "
import asyncio
from weather_mcp_server import get_current_weather
print(asyncio.run(get_current_weather(40.7128, -74.0060)))
"
```

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Network timeouts**: Check internet connection and firewall settings

3. **Invalid coordinates**: Ensure latitude is between -90 and 90, longitude between -180 and 180

4. **No location found**: Try different search terms or check spelling

### Logging

Enable debug logging for troubleshooting:

```bash
LOG_LEVEL=DEBUG python weather_mcp_server.py
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

🌤️ **Happy weather forecasting!** 🌤️