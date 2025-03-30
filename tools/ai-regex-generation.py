import os
import time
import random

import httpx
from llama_index.core import PromptTemplate

import asyncwhois
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    # todo: add support or substitute LLM providers
    # from llama_index.llms.ollama import Ollama
    from llama_index.llms.bedrock import Bedrock

    # todo: adjust LLM params like temperature, etc.
    bedrock_llm = Bedrock(model="anthropic.claude-v2", context_size=128000)
    return bedrock_llm


# todo: do prompt engineering! try few-shot examples?
PROMPT_TEMPLATE = """\
Below is the text output from a WHOIS Server.
---------------------
{context_str}
---------------------
Using the text above, generate regular expressions to parse the key value pairs.
Answer: \
"""


if __name__ == "__main__":

    # todo: pick a domain name
    domain_name = ""

    for fn in os.listdir("./data"):

        # todo: after the first run, you can just read in this file without having to re-query the server.
        with open(f"./data/{fn}", "r") as f:
            query_output = f.read()

        # get an LLM and give it the prompt
        llm = get_llm()
        prompt = PromptTemplate(PROMPT_TEMPLATE).format(context_str=query_output)
        response = llm.complete(prompt)

        out_fn = fn.lstrip("query_")
        # save results
        with open(f"regexes_{out_fn}", "w") as out:
            out.write(str(response))

        # todo: test the regexes! Feel free to manual/anecdotal or empirical methods.
        #  bonus: write a script/function that can take the AI-generated regexes and automatically try them on the text.
