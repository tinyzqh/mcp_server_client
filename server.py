from fastmcp import FastMCP

# Create a FastMCP application instance; "demo" is the application name
app = FastMCP("demo")


# Register the weather query tool for retrieving weather info of a given city
@app.tool(name="weather", description="Query city weather")
def get_weather(city: str):
    # Preset weather data (can be replaced with actual API calls in real use)
    weather_data = {"北京": {"temp": 25, "condition": "Sunny"}, "上海": {"temp": 28, "condition": "Cloudy"}}
    # Return the weather data of the given city, or an error if not found
    return weather_data.get(city, {"error": "City not found"})


# Register the stock query tool for retrieving stock price by code
@app.tool(name="stock", description="Query stock price")
def get_stock(code: str):
    # Preset stock data (can be replaced with actual API calls in real use)
    stock_data = {"600519": {"name": "贵州茅台", "price": 1825.0}, "000858": {"name": "五粮液", "price": 158.3}}
    # Return the stock data for the given code, or an error if not found
    return stock_data.get(code, {"error": "Stock not found"})


if __name__ == "__main__":
    # Start the HTTP server with streamable response support
    app.run(
        transport="streamable-http",  # Use streamable HTTP transport
        host="127.0.0.1",  # Bind to local address
        port=4200,  # Port number
        path="/demo",  # URL path prefix
        log_level="debug",  # Debug log level
    )
