from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools.Tools import Tools
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

def plan_trip():

    tools = Tools()

    tools_for_agent = [
        Tool(
            name="get_weather_data",
            func=tools.get_weather_data,
            description=Tools.get_weather_data.__doc__,
        ),
        Tool(
            name="get_trending_attractions",
            func=tools.get_trending_attractions,
            description=Tools.get_trending_attractions.__doc__,
        ),
    ]
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful travel assistant.
                You should explicitly consider the weather and trending attractions in your answer.
                You should also provide the user with clothing recommendations based on the weather.
                Make sure to use the tools for getting information before giving the final answer.""",
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"), # This is where the agent can store data for later use (e.g. tool outputs)
        ]
    )

    # Create an LLM instance
    llm = AzureChatOpenAI(azure_deployment="gpt-4", openai_api_version="2024-02-01")

    # Build the tool calling agent
    agent = create_tool_calling_agent(llm=llm, tools=tools_for_agent, prompt=prompt)

    # Execute the agent
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    return agent_executor

if __name__ == "__main__":
    
    # This is a simple test to run the agent once    
    
    # Get the user input
    usr_input = input("How may I help you?\n")

    # Create the agent executor
    agent_executor = plan_trip()
    
    # Invoke the agent
    result = agent_executor.invoke({"input": usr_input})

    # Print the agent output
    pprint(result)
    