Trip Planning Agent Documentation
![image](https://github.com/user-attachments/assets/efeff132-288c-48ec-b8cb-66e793d45551)
*Fig.1: Events tracing for a sample prompt*
![image](https://github.com/user-attachments/assets/3d8ff68c-c1ca-4021-91d4-490c2c040579)
*Fig.2: Events tracing for another prompt*
![image](https://github.com/user-attachments/assets/8197bf9a-19e9-4a47-b3d9-0cfa378a03f2)
![image](https://github.com/user-attachments/assets/d6118e83-4342-4355-a0a2-65a5bdc5c9c5)
*Fig.3: Final planning response after refinement*

Overview
This project implements a multi-agent AI system using Google ADK to create comprehensive, budget-friendly travel plans. The system takes a user goal (e.g., "Plan a trip to Paris for 4 people in July 2025") and generates a detailed itinerary by routing data between agents, each enriching the output of the previous one, until the goal is achieved. The agents iteratively refine the plan to ensure it meets quality standards.
System Flow
The system operates as a pipeline with the following components:

Initial Planning Agent: Creates a draft travel plan using multiple APIs to gather data on destinations, weather, flights, currency rates, and news.
Refinement Loop:
Critic Agent: Reviews the plan for tool usage, data accuracy, and quality standards, providing specific improvement suggestions.
Refiner Agent: Addresses the critic’s feedback by fetching additional data via tools and improving the plan. If no issues are found, it exits the loop.


Output: A structured travel plan with a destination analysis, detailed itinerary, and budget breakdown.

Agent Interaction

The Initial Planning Agent starts by using tools to gather data and create a draft plan.
The Critic Agent checks the plan against quality criteria, ensuring tool usage and realistic data.
The Refiner Agent incorporates feedback, re-running tools if needed, until the plan is approved or the maximum iterations (5) are reached.
Agents pass data via shared state keys (current_document for the plan, criticism for feedback).

Agent Logic
Initial Planning Agent

Role: Creates the initial travel plan.
Tools Used:
get_current_time: Ensures future dates are used.
serper_search: Researches destinations, attractions, and costs.
get_weather: Checks climate conditions.
get_flight_pricing: Fetches flight costs via Amadeus API.
get_currency_rate: Gets exchange rates for international travel.
get_news: Checks for travel advisories.


Output: A structured plan with destination analysis, itinerary, and budget breakdown.
Logic: Follows a mandatory tool usage process to ensure data-driven recommendations, prioritizing cost-efficiency and safety.

Critic Agent

Role: Reviews the plan for quality and tool usage.
Tools Used: Same as Initial Planning Agent to verify data.
Logic:
Checks for evidence of tool usage (e.g., specific prices, dates).
Validates future dates using get_current_time.
Ensures the plan includes research-backed recommendations, a detailed itinerary, and a realistic budget.
Outputs specific improvement suggestions or the completion phrase ("No major issues found.").



Refiner Agent

Role: Improves the plan based on critic feedback.
Tools Used: Same as above, plus exit_loop to terminate the loop when complete.
Logic:
If feedback is the completion phrase, calls exit_loop.
Otherwise, uses tools to address missing or inaccurate data.
Outputs an updated plan, maintaining the required structure.



APIs Used
The system integrates the following public APIs:

OpenWeatherMap API (weather.py):
Purpose: Fetches current weather and climate data for destinations.
Endpoint: https://api.openweathermap.org/data/2.5/weather
Authentication: API key stored in .env as OPENWEATHER_API_KEY.


Amadeus API (flight.py):
Purpose: Retrieves flight pricing for budget estimation.
Endpoint: https://test.api.amadeus.com/v2/shopping/flight-offers
Authentication: Bearer token using AMADEUS_API_KEY and AMADEUS_API_SECRET in .env.


Frankfurter API (currency.py):
Purpose: Provides currency exchange rates for international travel.
Endpoint: https://api.frankfurter.app/latest
Authentication: None (public API).


EventRegistry API (news.py):
Purpose: Fetches news articles for travel advisories.
Endpoint: Uses EventRegistry’s Python SDK.
Authentication: API key stored in .env as NEWS_API_KEY.


Serper API (serper_search.py):
Purpose: Performs Google search for destination research and cost estimates.
Endpoint: https://google.serper.dev/search
Authentication: API key stored in .env as SERPER_API_KEY.



Setup Instructions
Prerequisites

Python 3.10+
Google ADK installed
API keys for:
OpenWeatherMap (OPENWEATHER_API_KEY)
Amadeus (AMADEUS_API_KEY, AMADEUS_API_SECRET)
EventRegistry (NEWS_API_KEY)
Serper (SERPER_API_KEY)
Google Gemini (GOOGLE_API_KEY)



Installation

Clone the repository:git clone <repository-url>
cd trip_planning_agent


Create a virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Create a .env file in the project root:touch .env

Add the following:
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=<your-google-studio-api-key>
OPENWEATHER_API_KEY=<your-openweathermap-key>
AMADEUS_API_KEY=<your-amadeus-api-key>
AMADEUS_API_SECRET=<your-amadeus-secret>
NEWS_API_KEY=<your-eventregistry-key>
SERPER_API_KEY=<your-serper-key>


Run the system:
Ensure Google ADK is configured.
Run `adk web` command to run web interface.
Run `adk run trip_planning_agent` command to run on terminal
Run `adk api_server` to create a local FastAPI server.





Project Structure
trip_planning_agent
├── __init__.py               # Package initialization
├── agent.py                 # Defines agents and pipeline
├── requirements.txt         # Python dependencies
└── tools
    ├── __init__.py          # Tools package initialization
    ├── currency.py          # Currency exchange rate tool
    ├── flight.py            # Flight pricing tool
    ├── news.py              # News and travel advisories tool
    ├── serper_search.py     # Web search tool
    ├── time.py              # Current time tool
    ├── weather.py           # Weather data tool

Evaluations
[To be provided later]
