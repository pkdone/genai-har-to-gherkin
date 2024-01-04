# HTTP Archive To Gherkin Scenarios Demo Using GenAI

A demo project that provides a very basic example of taking the input HTTP archive ([HAR](https://en.wikipedia.org/wiki/HAR_(file_format))) data recorded by a browser for a user interfacing with a web application and using an LLM to describe the Gherkin features and scenarios of the application that the log data implies.


## Prerequisites Before Running For A First Time

1. Ensure you have an account registered for [OpenAI's API Platform](https://platform.openai.com/) with an [API key](https://platform.openai.com/account/api-keys) you have created, or if using an Azure sandboxed version of an OpenAI GPT model, you have the endpoint, provisioned model and keys for that model.

1. Ensure you have installed Python 3 and [PIP](https://pip.pypa.io/en/stable/installation/) on your workstation.

1. In a terminal on your workstation, from the root folder of this project, run the following command to copy an example environment configuration file to a new file into the same root folder called **`.env`**, and then edit the values for the properties shown in this new **`.env`** file to reflect your specific environment settings:

    ```console
    cp 'EXAMPLE.env' '.env'
    ```

1. In the terminal, initialise the required Python environment for you to be able to execute the application correctly.

    ```console
    python3 -m pip install --user virtualenv
    python3 -m venv my-test-env
    source my-test-env/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    ```

1. Ensure you have a web application accessible from a browser on your workstation. If you don't have one accessible, as long as you have a recent version of Docker installed, you can clone, configure and run the following demo web application from GitHub: [icehrm HR management system](https://github.com/gamonoid/icehrm).


## Steps To Run

1. From a browser, record a user's session using a web application to perform various common tasks provided by that application and save the file to a local folder (the rest of the instructions will assume you have saved this to `~/localhost.har` so you will need to change any subsequent references to this file path, show in the rest of this README, accordingly). An example of how to do this in a Google Chrome browser is [documented here](https://support.zendesk.com/hc/en-us/articles/4408828867098-Generating-a-HAR-file-for-troubleshooting-).

1. From the terminal, execute the first script to reduce the size of the HAR file to just the relevant request/response entries to enable to have a far greater chance of being small enough to subsequently use as-is in a single prompt sent to a regular LLM.

    ```console
    python src/extract-har-entities.py -i ~/localhost.har > ~/reduced-localhost.har
    ```

1. From the terminal, execute the second to build a prompt asking an LLM to generate Gherkin features/scenarios for the given reduced-size HTTP Archive logged data.

    ```console
    python src/prompt-llm-har-to-gherkin.py -i ~/reduced-localhost.har
    ```
