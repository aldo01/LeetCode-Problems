#!/usr/bin/env python3
"""
Weather MCP Server

A Model Context Protocol server that provides weather information using the Open-Meteo API.
This server exposes multiple tools for getting weather data, forecasts, and location information.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Weather")

# Constants
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1"
GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1"


class WeatherData(BaseModel):
    """Weather data model"""
    temperature: float
    humidity: Optional[int] = None
    wind_speed: float
    wind_direction: Optional[int] = None
    weather_code: int
    description: str


class Location(BaseModel):
    """Location model"""
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    admin1: Optional[str] = None


async def make_request(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Make an HTTP request with proper error handling and timeout.
    
    Args:
        url: The URL to request
        params: Optional query parameters
        
    Returns:
        JSON response data or None if request failed
    """
    headers = {
        "User-Agent": "weather-mcp-server/1.0",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, 
                params=params,
                headers=headers, 
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


def weather_code_to_description(code: int) -> str:
    """Convert weather code to human-readable description"""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, f"Unknown weather condition (code: {code})")


@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> str:
    """
    Get current weather conditions for a specific location.
    
    Args:
        latitude: Latitude of the location (-90 to 90)
        longitude: Longitude of the location (-180 to 180)
    
    Returns:
        Current weather information as a formatted string
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "timezone": "auto"
    }
    
    data = await make_request(f"{OPEN_METEO_BASE_URL}/forecast", params)
    
    if not data or "current_weather" not in data:
        return f"Unable to fetch current weather data for coordinates ({latitude}, {longitude})"
    
    current = data["current_weather"]
    weather_desc = weather_code_to_description(current.get("weathercode", 0))
    
    return f"""Current Weather:
📍 Location: {latitude:.2f}°, {longitude:.2f}°
🌡️ Temperature: {current.get('temperature', 'N/A')}°C
💨 Wind: {current.get('windspeed', 'N/A')} km/h at {current.get('winddirection', 'N/A')}°
🌤️ Conditions: {weather_desc}
🕐 Time: {current.get('time', 'N/A')}"""


@mcp.tool()
async def get_weather_forecast(latitude: float, longitude: float, days: int = 3) -> str:
    """
    Get weather forecast for a specific location.
    
    Args:
        latitude: Latitude of the location (-90 to 90)
        longitude: Longitude of the location (-180 to 180)
        days: Number of forecast days (1-7, default: 3)
    
    Returns:
        Weather forecast information as a formatted string
    """
    # Limit days to reasonable range
    days = max(1, min(days, 7))
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max",
        "forecast_days": days,
        "timezone": "auto"
    }
    
    data = await make_request(f"{OPEN_METEO_BASE_URL}/forecast", params)
    
    if not data or "daily" not in data:
        return f"Unable to fetch forecast data for coordinates ({latitude}, {longitude})"
    
    daily = data["daily"]
    forecast_lines = [f"📅 {days}-Day Weather Forecast for {latitude:.2f}°, {longitude:.2f}°:\n"]
    
    for i in range(len(daily["time"])):
        date = daily["time"][i]
        temp_max = daily["temperature_2m_max"][i]
        temp_min = daily["temperature_2m_min"][i]
        weather_code = daily["weathercode"][i]
        precipitation = daily["precipitation_sum"][i]
        wind_speed = daily["windspeed_10m_max"][i]
        
        weather_desc = weather_code_to_description(weather_code)
        
        forecast_lines.append(f"""📆 {date}:
  🌡️ {temp_min}°C - {temp_max}°C
  🌤️ {weather_desc}
  🌧️ Precipitation: {precipitation}mm
  💨 Max wind: {wind_speed} km/h""")
    
    return "\n\n".join(forecast_lines)


@mcp.tool()
async def search_location(query: str, limit: int = 5) -> str:
    """
    Search for locations by name to get coordinates.
    
    Args:
        query: Location name to search for (city, address, etc.)
        limit: Maximum number of results to return (1-10, default: 5)
    
    Returns:
        List of matching locations with coordinates
    """
    limit = max(1, min(limit, 10))
    
    params = {
        "name": query,
        "count": limit,
        "language": "en",
        "format": "json"
    }
    
    data = await make_request(f"{GEOCODING_BASE_URL}/search", params)
    
    if not data or "results" not in data or not data["results"]:
        return f"No locations found for query: '{query}'"
    
    locations = []
    for result in data["results"]:
        location_info = f"""📍 {result.get('name', 'Unknown')}"""
        if result.get('admin1'):
            location_info += f", {result['admin1']}"
        if result.get('country'):
            location_info += f", {result['country']}"
        location_info += f"\n   📍 Coordinates: {result.get('latitude', 'N/A'):.4f}°, {result.get('longitude', 'N/A'):.4f}°"
        if result.get('population'):
            location_info += f"\n   👥 Population: {result['population']:,}"
        locations.append(location_info)
    
    return f"🔍 Search results for '{query}':\n\n" + "\n\n".join(locations)


@mcp.tool()
async def get_weather_by_city(city_name: str) -> str:
    """
    Get current weather for a city by name.
    
    Args:
        city_name: Name of the city
    
    Returns:
        Current weather information for the city
    """
    # First, search for the city to get coordinates
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    location_data = await make_request(f"{GEOCODING_BASE_URL}/search", params)
    
    if not location_data or "results" not in location_data or not location_data["results"]:
        return f"City '{city_name}' not found. Please check the spelling or try a different name."
    
    location = location_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    
    # Get weather for the coordinates
    weather_info = await get_current_weather(latitude, longitude)
    
    # Replace coordinate info with city info
    city_display = location.get('name', city_name)
    if location.get('admin1'):
        city_display += f", {location['admin1']}"
    if location.get('country'):
        city_display += f", {location['country']}"
    
    weather_info = weather_info.replace(
        f"📍 Location: {latitude:.2f}°, {longitude:.2f}°",
        f"📍 Location: {city_display}"
    )
    
    return weather_info


@mcp.tool()
async def get_weather_alerts(latitude: float, longitude: float) -> str:
    """
    Get weather alerts and warnings for a specific location.
    Note: This is a placeholder implementation as Open-Meteo doesn't provide alerts in the free tier.
    
    Args:
        latitude: Latitude of the location (-90 to 90)
        longitude: Longitude of the location (-180 to 180)
    
    Returns:
        Weather alerts information
    """
    # Get current weather to check for severe conditions
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "forecast_hours": 24
    }
    
    data = await make_request(f"{OPEN_METEO_BASE_URL}/forecast", params)
    
    if not data:
        return f"Unable to fetch weather data for coordinates ({latitude}, {longitude})"
    
    alerts = []
    
    # Check current conditions
    if "current_weather" in data:
        current = data["current_weather"]
        wind_speed = current.get("windspeed", 0)
        
        if wind_speed > 50:
            alerts.append("⚠️ HIGH WIND WARNING: Wind speeds above 50 km/h detected")
        elif wind_speed > 30:
            alerts.append("🌪️ WIND ADVISORY: Elevated wind speeds detected")
    
    # Check hourly forecast for extreme conditions
    if "hourly" in data:
        hourly = data["hourly"]
        max_wind = max(hourly.get("windspeed_10m", [0]))
        total_precipitation = sum(hourly.get("precipitation", [0]))
        
        if max_wind > 70:
            alerts.append("🚨 SEVERE WIND WARNING: Expected wind gusts over 70 km/h")
        
        if total_precipitation > 25:
            alerts.append("🌧️ HEAVY RAIN WARNING: Significant precipitation expected (>25mm)")
    
    if not alerts:
        alerts.append("✅ No weather alerts currently active for this location")
    
    return f"🚨 Weather Alerts for {latitude:.2f}°, {longitude:.2f}°:\n\n" + "\n".join(alerts)


if __name__ == "__main__":
    # Run the MCP server
    logger.info("Starting Weather MCP Server...")
    mcp.run(transport='stdio')