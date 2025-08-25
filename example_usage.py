#!/usr/bin/env python3
"""
Example usage of the Weather MCP Server tools.

This file demonstrates how to use each tool provided by the weather MCP server.
Note: This is for demonstration purposes. In practice, these tools would be
called by an AI model through the MCP protocol.
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import our server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the weather server functions (this would normally be done by MCP)
try:
    from weather_mcp_server import (
        get_current_weather,
        get_weather_forecast,
        search_location,
        get_weather_by_city,
        get_weather_alerts
    )
except ImportError as e:
    print(f"❌ Error importing weather server: {e}")
    print("💡 Make sure to install dependencies first:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


async def demo_current_weather():
    """Demo getting current weather by coordinates."""
    print("🌤️ Demo: Current Weather by Coordinates")
    print("=" * 50)
    
    # New York City coordinates
    result = await get_current_weather(40.7128, -74.0060)
    print(result)
    print()


async def demo_weather_forecast():
    """Demo getting weather forecast."""
    print("📅 Demo: Weather Forecast")
    print("=" * 50)
    
    # London coordinates, 5-day forecast
    result = await get_weather_forecast(51.5074, -0.1278, days=5)
    print(result)
    print()


async def demo_location_search():
    """Demo searching for locations."""
    print("🔍 Demo: Location Search")
    print("=" * 50)
    
    # Search for Paris
    result = await search_location("Paris", limit=3)
    print(result)
    print()


async def demo_weather_by_city():
    """Demo getting weather by city name."""
    print("🏙️ Demo: Weather by City Name")
    print("=" * 50)
    
    # Get weather for Tokyo
    result = await get_weather_by_city("Tokyo")
    print(result)
    print()


async def demo_weather_alerts():
    """Demo getting weather alerts."""
    print("🚨 Demo: Weather Alerts")
    print("=" * 50)
    
    # Check alerts for Miami (hurricane-prone area)
    result = await get_weather_alerts(25.7617, -80.1918)
    print(result)
    print()


async def interactive_demo():
    """Interactive demo allowing user input."""
    print("🎮 Interactive Weather Demo")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Get weather for a city")
        print("2. Search for locations")
        print("3. Get weather by coordinates")
        print("4. Get weather forecast")
        print("5. Check weather alerts")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ").strip()
        
        try:
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                city = input("Enter city name: ").strip()
                if city:
                    result = await get_weather_by_city(city)
                    print(f"\n{result}")
            elif choice == "2":
                query = input("Enter location to search: ").strip()
                if query:
                    result = await search_location(query, limit=5)
                    print(f"\n{result}")
            elif choice == "3":
                try:
                    lat = float(input("Enter latitude (-90 to 90): ").strip())
                    lon = float(input("Enter longitude (-180 to 180): ").strip())
                    result = await get_current_weather(lat, lon)
                    print(f"\n{result}")
                except ValueError:
                    print("❌ Invalid coordinates. Please enter numbers.")
            elif choice == "4":
                try:
                    lat = float(input("Enter latitude (-90 to 90): ").strip())
                    lon = float(input("Enter longitude (-180 to 180): ").strip())
                    days = int(input("Enter forecast days (1-7): ").strip() or "3")
                    result = await get_weather_forecast(lat, lon, days)
                    print(f"\n{result}")
                except ValueError:
                    print("❌ Invalid input. Please enter numbers.")
            elif choice == "5":
                try:
                    lat = float(input("Enter latitude (-90 to 90): ").strip())
                    lon = float(input("Enter longitude (-180 to 180): ").strip())
                    result = await get_weather_alerts(lat, lon)
                    print(f"\n{result}")
                except ValueError:
                    print("❌ Invalid coordinates. Please enter numbers.")
            else:
                print("❌ Invalid choice. Please enter 0-5.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


async def run_all_demos():
    """Run all demo functions."""
    print("🌤️ Weather MCP Server Demo")
    print("=" * 60)
    print()
    
    demos = [
        demo_current_weather,
        demo_weather_forecast,
        demo_location_search,
        demo_weather_by_city,
        demo_weather_alerts
    ]
    
    for demo in demos:
        try:
            await demo()
        except Exception as e:
            print(f"❌ Error in {demo.__name__}: {e}")
            print()
    
    print("✅ All demos completed!")
    print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Weather MCP Server Demo")
    parser.add_argument(
        "--interactive", 
        action="store_true", 
        help="Run interactive demo"
    )
    args = parser.parse_args()
    
    try:
        if args.interactive:
            asyncio.run(interactive_demo())
        else:
            asyncio.run(run_all_demos())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)