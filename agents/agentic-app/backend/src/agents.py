#!pip install -q langchain-openai termcolor langchain_community duckduckgo_search==7.1.0 wikipedia openapi-python-client==0.12.3 langgraph langchain_experimental

# Imports
import os
import json
import getpass

from langchain_openai import ChatOpenAI

from langchain_experimental.utilities import PythonREPL
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langgraph.prebuilt import create_react_agent
from IPython.display import Image, display
from langchain_core.tools import tool

from typing_extensions import TypedDict
from typing import Annotated



from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_core.messages import BaseMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import Tool

INFERENCE_SERVER_URL = os.getenv('API_URL_GRANITE')
MODEL_NAME = "granite-3-8b-instruct"
API_KEY= os.getenv('API_KEY_GRANITE')

llm = ChatOpenAI(
    openai_api_key=API_KEY,
    openai_api_base= f"{INFERENCE_SERVER_URL}/v1",
    model_name=MODEL_NAME,
    top_p=0.92,
    temperature=0.01,
    max_tokens=512,
    presence_penalty=1.03,
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

repl = PythonREPL()

@tool
def python_repl(
    code: Annotated[str, "The python code to execute to generate your calculations."],
):
    """Use this to execute python code. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""
    try:
        result = repl.run(code)
    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}"
    result_str = f"Successfully executed:\n\`\`\`python\n{code}\n\`\`\`\nStdout: {result}"
    return (
        result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."
    )
duckduckgo_search = DuckDuckGoSearchRun()

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [duckduckgo_search, python_repl, wikipedia]

graph = create_react_agent(llm, tools=tools, debug=False)
#display(Image(graph.get_graph().draw_mermaid_png())

user_query = "Calculate the distance between Madrid and Vegas in minutes and calculate how many seconds will spend flighing over"

inputs = {"messages": [("user", user_query)]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()