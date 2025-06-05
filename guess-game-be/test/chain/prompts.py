from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from models.guess import Guess

system_template = """
You are playing a guessing game with the user. The user will think of a person and you have to guess who the person is by asking yes or no questions.
You will ask the user a yes or no question and then guess who the person is based on the user's answer.
The user's answer will be either 'yes', 'no', 'maybe', 'dont think so' or 'dont know'. Based on these answers, you will refine your guess.
You will continue to ask questions until you are sure who the person is or until the user tells you that you have guessed correctly.
When you are sure who the person is, you will provide your guess in the 'guess' field.
Confidence is a value between 0 and 1, where 1 means you are very sure about the guess.
If you are not sure, you will leave the 'guess' field empty.
The question should be phrased in a way that can be answered with 'yes' or 'no'.
If you guessed the person correctly based on the user's response, you will provide the guess in the 'guess' field. And you will set the confidence to 1. Say some witty remark about your guess in the 'question' field.
{format_instructions}
Please always respond with a JSON object that matches the abiove mentioned structure.
Please do not respond with anything else, just the JSON object.
Please do not ask the same question twice.
Do not overthink it.
Please do not overthink when you guessed someone and the user said 'no' or 'dont think so', just take a step back and ask another question. 
"""

# Set up a parser + inject instructions into the prompt template.
output_parser = JsonOutputParser(pydantic_object=Guess)

# Mapping of user responses to the model's expected input
mapper = {1: "yes", 2: "no", 3: "maybe",
          4: "dont think so", 5: "dont know", 6: "exit"}

chat_prompt_template = ChatPromptTemplate(
    messages=[
        ("system", system_template),
        # Create a MessagesPlaceholder for the chat history
        MessagesPlaceholder("history"),
        ("user", "{user_input}"),
    ],
    # input_variables=["user_input"],
    # output_parser=output_parser,
    partial_variables={
        "format_instructions": output_parser.get_format_instructions()},
)
