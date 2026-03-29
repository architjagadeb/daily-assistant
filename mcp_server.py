from mcp.server.fastmcp import FastMCP
from finance_tracker import analyze_finance
from health_tracker import analyze_health
from news_handler import get_news_summary
from calendar_handler import get_calendar_summary

mcp = FastMCP("daily-assistant")

@mcp.tool()
def get_news():
    """Fetches and summarizes top news headlines"""
    return get_news_summary()

@mcp.tool()
def analyze_finance_data():
    """Analyzes finance data and provides insights"""
    return analyze_finance()

@mcp.tool()
def analyze_health_data():
    """Analyzes health data and provides insights"""
    return analyze_health()

@mcp.tool()
def get_calendar_events():
    """Fetches and summarizes calendar events"""
    return get_calendar_summary([])



if __name__ == "__main__":
    mcp.run()

