import json
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = getenv("API_KEY")

model = ChatNVIDIA(
    model="deepseek-ai/deepseek-r1",
    api_key=API_KEY,
    temperature=0.6,
)

# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")


# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()},
)

chain = prompt | model | parser
response = chain.invoke({"query": joke_query})
print(json.dumps(response, indent=2))
