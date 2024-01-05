import sys
import os
from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI
from util.utils import get_arguments, read_content


##
# Main function to take input HTTP archive (HAR) data recorded by a browser and use an LLM to
# describe the Gherkin features and scenarios that the log data implies for an application.
##
def main():
    try:
        args = get_arguments("Use an LLM to introspect a HTTP Archive (HAR) file to describe the "
                             "Gherkin features/scenarious it implies.")
        config = load_api_config()
        log_data = read_content(args.input)
        prompt = build_templated_prompt(log_data)
        response_text = prompt_llm_get_response(config, prompt)
        print(response_text)

    except Exception as e:
        print(f"An error occurred: {e}")
        print(sys.exc_info()[2])
        exit(1)


##
# Loads API configuration from a .env file.
##
def load_api_config():
    load_dotenv()
    config = {
        "api_key": os.getenv("API_KEY", "").strip(),
        "api_model": os.getenv("API_MODEL", "").strip(),
        "api_base": os.getenv("API_BASE", "").strip(),
        "api_type": os.getenv("API_TYPE", "").strip(),
        "api_version": os.getenv("API_VERSION", "").strip()
    }

    if not config.get("api_key"):
        raise ValueError("No 'api_key' value defined in '.env' file or env var")

    if not config.get("api_model"):
        raise ValueError("No 'api_model' value defined in '.env' file or env var")

    return config


##
# Build a new prompt filling in the gaps in a parameterized prompt text template..
##
def build_templated_prompt(logdata):
    template = """
The log data below came from an HTTP Archive (HAR) file produced by the Chrome browser, having
tracked a user in a browser who was interacting with a web application. Using this logged data,
describe the business purpose of the application and what the user was trying to achieve using
the Gherkin business language to describe the web application's behavior. The Gherkin responses
part of your response must be output inside a markdown code block.

```{logdata}```
"""

    prompt = template.format(logdata=logdata)
    return prompt


##
# Send the new expanded prompt to the GPT API and return its response.
# Sets some extra parameters for using the GPT4 API if hitting an Azure hosted version of the API.
##
def prompt_llm_get_response(config, prompt):
    if config.get("api_type").lower() == AZURE_TYPE:
        client = AzureOpenAI(
            api_key=config.get("api_key"),
            api_version=config.get("api_version"),
            azure_endpoint=config.get("api_base"),
        )
    else:
        client = OpenAI(
            api_key=config.get("api_key"),
        )

    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(
        model=config.get("api_model"),
        messages=messages,
        temperature=TEMP,
    )

    return completion.choices[0].message.content


# Constants
TEMP = 0.7
AZURE_TYPE = "azure"


##
# Main
##
if __name__ == "__main__":
    main()
