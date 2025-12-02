"""
Utility modules for Daegu Public Data Visualization v1.1.1.

Modules:
- loader: CSV data loading with encoding fallback and caching
- geo: Geospatial utilities for coordinate detection and distance calculations
- visualizer: Plotly charts and Folium maps generation
- chatbot: Anthropic Claude chatbot for data Q&A with Tool Calling
- tools: 15 data analysis tools for Tool Calling
"""
from utils.loader import (
    read_csv_safe,
    read_uploaded_csv,
    load_dataset,
    load_dataset_from_session,
    get_dataset_info
)
from utils.geo import (
    detect_lat_lng_columns,
    haversine_distance,
    validate_coordinates,
    compute_proximity_stats
)
from utils.visualizer import (
    plot_numeric_distribution,
    plot_categorical_distribution,
    plot_boxplot,
    plot_kde,
    plot_scatter,
    plot_with_options,
    check_missing_ratio,
    create_folium_map,
    create_overlay_map
)
from utils.chatbot import (
    SYSTEM_PROMPT,
    create_data_context,
    create_chat_response,
    create_chat_response_with_tools,
    stream_chat_response_with_tools,
    handle_chat_error,
    validate_api_key
)
from utils.tools import (
    TOOLS,
    execute_tool,
    TOOL_HANDLERS
)

__all__ = [
    # loader
    'read_csv_safe',
    'read_uploaded_csv',
    'load_dataset',
    'load_dataset_from_session',
    'get_dataset_info',
    # geo
    'detect_lat_lng_columns',
    'haversine_distance',
    'validate_coordinates',
    'compute_proximity_stats',
    # visualizer
    'plot_numeric_distribution',
    'plot_categorical_distribution',
    'plot_boxplot',
    'plot_kde',
    'plot_scatter',
    'plot_with_options',
    'check_missing_ratio',
    'create_folium_map',
    'create_overlay_map',
    # chatbot
    'SYSTEM_PROMPT',
    'create_data_context',
    'create_chat_response',
    'create_chat_response_with_tools',
    'stream_chat_response_with_tools',
    'handle_chat_error',
    'validate_api_key',
    # tools
    'TOOLS',
    'execute_tool',
    'TOOL_HANDLERS'
]
