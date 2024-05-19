from pprint import pprint
import os
from dotenv import load_dotenv
from textwrap import dedent
from openai import OpenAI

from phi.assistant import Assistant
from phi.knowledge.base import AssistantKnowledge
from phi.llm.openai.chat import OpenAIChat
from phi.tools import youtube_tools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.shell import ShellTools
from phi.tools.calculator import Calculator
from phi.tools.youtube_tools import YouTubeTools
from phi.tools.file import FileTools
from phi.tools.tavily import TavilyTools
from phi.tools.yfinance import YFinanceTools
from phi.tools.python import PythonTools
from phi.tools.wikipedia import WikipediaTools
from phi.tools.website import WebsiteTools

from tavily import TavilyClient

from tools.crypto import CoinTracker
from tools.core import MarvinCore
from tools.calendar import MarvinCalender

from phi.knowledge.text import TextKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.embedder.openai import OpenAIEmbedder

from utils import list_all_available_openai_models, sanitize_collection_name

load_dotenv()


# Add generic function as tool

# Useful tools
# DuckDuckGo
# ShellTools
# Calculator
# YouTubeTools
# FileTools
# Tavily (Think about searching for current date events)
# YFinanceTools (You need to mention to use this tool since it might want to try answering itself or use web search (e.g. tavily)
# PythonTools

# Useful Assistants
# PythonAssistant

# Utilities
# PgVector, Ollama

# Useful Constructs
# Assistant, Tool, LLM, Task


# TODO: How to add logging (e.g. for tools to see their original response)

# open_ai_client = OpenAi

calculator_tool = Calculator()

python_tool = PythonTools(run_code=True)

shell_tool = ShellTools()
file_tool = FileTools()

web_tool = TavilyTools(
    os.getenv('TAVILY_API_KEY'),
    use_search_context=True
)

youtube_tool = YouTubeTools()

finance_tool = YFinanceTools(
    company_info=True,
    company_news=True,
    stock_fundamentals=True,
    income_statements=True,
    key_financial_ratios=True,
    analyst_recommendations=True,
    technical_indicators=True,
    historical_prices=True,
)


# crypto_tool = CoinTracker(api_key=None, api_secret=None)
# print(crypto_tool.get_coin_price('Bitcoin'))
# exit()

# assistant = Assistant(
#     tools=[
#         calculator_tool,
#         python_tool,
#         shell_tool,
#         file_tool,
#         web_tool,
#         youtube_tool, 
#         finance_tool,
#         # crypto_tool,
#         ],
#     show_tool_calls=True
# )
#
# while True:
#     prompt = input("You: ")
#     if prompt == "exit":
#         break
#     # response = tavily.get_search_context(query=prompt.strip(), search_depth="advanced")
#     # pprint(response)
#     assistant.print_response(prompt.strip())


database_host = os.getenv('POSTGRES_HOST')
database_user = os.getenv('POSTGRES_USER')
database_password = os.getenv('POSTGRES_PASSWORD')
database_name = os.getenv('POSTGRES_DB_NAME')

database_url = f"postgresql+psycopg://{database_user}:{database_password}@{database_host}/{database_name}"

print(database_url)


if __name__ == "__main__":
    openai_client = OpenAI()
    user_name = input("What is your name ?")
    santized_username = sanitize_collection_name(user_name)
    # print(santized_username.strip())
    # exit()

    knowledge_base = AssistantKnowledge(
        vector_db=PgVector2(
            schema=database_name,
            collection=f"text_documents",
            db_url= database_url,
            # embedder=OllamaEmbedder(model="llama3")
            embedder=OpenAIEmbedder(openai_client=openai_client)
        ),
        num_documents=10,
    )
    # knowledge_base.clear()
    assistant = Assistant(
        # llm=Ollama(model="llama3"),
        llm=OpenAIChat(
            openai_client=openai_client,
            model="gpt-4o",
        ),
        description="""
                You can chain the tools to get the best result.
                try to be creative with responses and be proactive, suggest user things that are relevent to context and tools you have.
        """,
        debug_mode=True,
        show_tool_calls=True,
        knowledge_base=knowledge_base,
        tools=[MarvinCore(knowledge_base),MarvinCalender(), DuckDuckGo()],
        add_references_to_prompt=True,
    )
    # exit()

    while True :
        x = input("How can I help you ?")
        assistant.print_response(x, markdown=True)
        print("\n-*- Metrics:")
        pprint(assistant.llm.metrics)
