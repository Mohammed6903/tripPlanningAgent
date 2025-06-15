from google.adk.agents import Agent, LoopAgent, SequentialAgent
from dotenv import load_dotenv
from google.adk.tools.tool_context import ToolContext

from .tools.serper_search import serper_search
from .tools.news import get_news
from .tools.weather import get_weather
from .tools.time import get_current_time
from .tools.currency import get_currency_rate
from .tools.flight import get_flight_pricing

load_dotenv()

APP_NAME = "travel_planner_agent"
USER_ID = "user123"
SESSION_ID_BASE = "loop_exit_tool_session"
GEMINI_MODEL = "gemini-2.0-flash"
STATE_INITIAL_PROMPT = "initial_prompt"

STATE_CURRENT_DOC = "current_document"
STATE_CRITICISM = "criticism"
COMPLETION_PHRASE = "No major issues found."


def exit_loop(tool_context: ToolContext):
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True

    return {}


initial_planning_agent = Agent(
    name="travel_planner_agent",
    model="gemini-2.0-flash",
    description=(
        "Creates the initial draft of a comprehensive travel plan based on user input. "
        "Gathers information about destinations, weather, flights, and creates a structured itinerary."
    ),
    # include_contents="none",
    instruction="""You are a Budget Travel Planning Assistant that MUST use the available tools to create accurate, data-driven travel plans.

        **MANDATORY TOOL USAGE PROCESS:**
        1. **ALWAYS start by using get_current_time** to know today's date for planning future dates
        2. **ALWAYS use serper_search** to research the destination, attractions, and travel tips
        3. **ALWAYS use get_weather** to check climate conditions for the destination
        4. **ALWAYS use get_flight_pricing** to get real flight cost estimates
        5. **ALWAYS use get_currency_rate** if planning international travel
        6. **ALWAYS use get_news** to check for any travel advisories or current events

        **Required Plan Structure:**
        1. **Destination Analysis**: 
        - Use serper_search to research the destination
        - Use get_weather to determine best visiting seasons
        - Include current travel conditions and tips

        2. **Detailed Itinerary**: 
        - Create day-wise schedule with specific times
        - Base recommendations on serper_search results
        - Include must-visit places found through research

        3. **Accurate Budget Breakdown**:
        - Use get_flight_pricing for real flight costs
        - Use get_currency_rate for international destinations
        - Research accommodation costs via serper_search
        - Provide detailed cost table:
            * Flights (round-trip per person)
            * Accommodation (per night)
            * Local transportation
            * Food and dining
            * Attractions and activities
            * Miscellaneous expenses
            * Total cost (group and per person)

        **CRITICAL REQUIREMENTS:**
        - You MUST use the tools before providing recommendations
        - Use serper_search to gather any kind of data required
        - Use only future dates (get current date first)
        - Base all recommendations on tool-gathered data
        - Prioritize cost-efficiency, safety, and convenience
        - Make the plan actionable and research-backed

        **Output Format:** Structured travel plan with tool-verified information, no meta-commentary.
    """,
    tools=[
        get_news,
        get_weather,
        get_current_time,
        get_currency_rate,
        get_flight_pricing,
        serper_search,
    ],
    output_key=STATE_CURRENT_DOC,
)


critic_agent_in_loop = Agent(
    name="TravelPlanCriticAgent",
    model=GEMINI_MODEL,
    # include_contents="none",
    instruction=f"""You are a travel plan quality reviewer. Check if the plan shows evidence of proper tool usage and meets quality standards.

    **Travel Plan to Review:**
    ```
    {{current_document}}
    ```

    **Review Criteria:**
    - ✅ Shows evidence of tool usage (real data, current information, specific prices)
    - ✅ Uses valid future dates only (use get_current_time to verify)
    - ✅ Includes research-backed destination recommendations
    - ✅ Lists specific must-visit attractions with details
    - ✅ Provides detailed day-wise itinerary with times
    - ✅ Contains comprehensive budget breakdown with realistic prices
    - ✅ Includes weather/seasonal information
    - ✅ Is practical, safe, and cost-efficient
    - ✅ Contains real world research on best enjoyments of the destination within the specified budget

    **Your Task:**
    1. **First, use get_current_time to verify dates are valid**
    2. Check if the plan appears to use real, researched data vs generic information.
        - Verify all of the data like pricing, timing, and recommmendations by using the appropriate tools.
    3. If you find specific, actionable improvements:
    - Output ONLY those suggestions in a structured format
    - Make sure none of the data is generic, assumed, estimated or vague
    4. If the plan meets all criteria with clear evidence of tool usage:
    - Output EXACTLY: "{COMPLETION_PHRASE}"

    Provide only the critique or the completion phrase.""",
    tools=[
        get_news,
        get_weather,
        get_current_time,
        get_currency_rate,
        get_flight_pricing,
        serper_search,
    ],
    description="Reviews and critiques travel plans to ensure they meet quality standards and verify tool usage.",
    output_key=STATE_CRITICISM,
)


refiner_travel_agent_in_loop = Agent(
    name="RefinerTravelAgent",
    model=GEMINI_MODEL,
    # include_contents="none",
    instruction=f"""You are a travel plan improvement specialist. Use available tools to address feedback and improve the travel plan.

    **Current Travel Plan:**
    ```
    {{current_document}}
    ```

    **Feedback:**
    {{criticism}}

    **Instructions:**
    1. **If feedback is EXACTLY "{COMPLETION_PHRASE}":**
    - Call the 'exit_loop' tool immediately
    - Do not output any text

    2. **If feedback mentions missing tool usage or data:**
    - **MUST use the appropriate tools** to gather the missing information:
        * get_current_time for date validation
        * serper_search for destination research and current prices
        * get_weather for climate information
        * get_flight_pricing for accurate flight costs
        * get_currency_rate for international travel
        * get_news for travel advisories
    - Apply the gathered information to improve the plan
    - Address each criticism point with tool-verified data

    3. **For other feedback:**
    - Use tools as needed to gather supporting information
    - Apply feedback to improve the travel plan structure
    - Maintain format but enhance with real data

    **Critical:** You MUST use tools to address data-related feedback. Output only the improved travel plan or call exit_loop.""",
    description="Refines the travel plan based on critique feedback or calls exit_loop if the plan is complete.",
    tools=[
        exit_loop,
        get_news,
        get_weather,
        get_current_time,
        get_currency_rate,
        get_flight_pricing,
        serper_search,
    ],
    output_key=STATE_CURRENT_DOC,
)

refinement_loop = LoopAgent(
    name="TravelPlanRefinementLoop",
    sub_agents=[
        critic_agent_in_loop,
        refiner_travel_agent_in_loop,
    ],
    max_iterations=5,
    description="Iteratively refines the travel plan until it meets quality standards.",
)


root_agent = SequentialAgent(
    name="IterativeTravelPlanningPipeline",
    sub_agents=[initial_planning_agent, refinement_loop],
    description=(
        "A comprehensive travel planning system that creates detailed, budget-friendly travel plans. "
        "It researches destinations, creates structured itineraries, provides cost estimates, "
        "and iteratively refines plans until they meet high quality standards. "
        "The system ensures all recommendations are practical, cost-effective, and actionable."
    ),
)
