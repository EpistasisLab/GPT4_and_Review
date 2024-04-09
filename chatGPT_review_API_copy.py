# %% [markdown]
# # Assistants API Overview (Python SDK)

# %% [markdown]
# The new [Assistants API](https://platform.openai.com/docs/assistants/overview) is a stateful evolution of our [Chat Completions API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api) meant to simplify the creation of assistant-like experiences, and enable developer access to powerful tools like Code Interpreter and Retrieval.

# %% [markdown]
# ![Assistants API Diagram](../images/assistants_overview_diagram.png)

# %% [markdown]
# ## Chat Completions API vs Assistants API
# 
# The primitives of the **Chat Completions API** are `Messages`, on which you perform a `Completion` with a `Model` (`gpt-3.5-turbo`, `gpt-4`, etc). It is lightweight and powerful, but inherently stateless, which means you have to manage conversation state, tool definitions, retrieval documents, and code execution manually.
# 
# The primitives of the **Assistants API** are
# 
# - `Assistants`, which encapsulate a base model, instructions, tools, and (context) documents,
# - `Threads`, which represent the state of a conversation, and
# - `Runs`, which power the execution of an `Assistant` on a `Thread`, including textual responses and multi-step tool use.
# 
# We'll take a look at how these can be used to create powerful, stateful experiences.
# 

# Make sure to install like below
# %%
# pip install --upgrade openai

# %% [markdown]
# And make sure it's up to date by running:
# 

# %%
# pip show openai | grep Version


# %% [markdown]
# The easiest way to get started with the Assistants API is through the [Assistants Playground](https://platform.openai.com/playground).
# 

# %% [markdown]
# ![Assistants Playground](../images/assistants_overview_assistants_playground.png)
# 

# %%
import os
import json
import time
from openai import OpenAI

import json

def show_json(obj):
    display(json.loads(obj.model_dump_json()))

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="api-key", # Enter your API key here
)

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
    model="gpt-4-1106-preview",
)
show_json(assistant)

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    return thread, run

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def show_json(obj):
    print(json.loads(obj.model_dump_json()))


MATH_ASSISTANT_ID = assistant.id  # or a hard-coded ID like "asst-..."
# MATH_ASSISTANT_ID = "asst-2X2xX3dPQ4w"
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key = "api-key", # Enter your API key here
)

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")
# Replace with the actual path to your folder containing PDF files
folder_path = "/Users/bhandaryp/Documents/DSN/systematic_review_chatgpt/table_creation/" # This is the folder which contains the PDFs that you want to provide to GPT-4
file_ID_list = []
# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    # Check if the file is a PDF
    if file_name.endswith(".pdf"):
        file_path = os.path.join(folder_path, file_name)
        # Upload the file
        uploaded_file = client.files.create(
            file=open(file_path, "rb"),
            purpose="assistants",
        )
        # Assuming uploaded_file has an 'id' attribute
        file_ID_list.append(uploaded_file.id)
        print(f"Uploaded {file_name} with ID {uploaded_file.id}")
# At this point, file_ID_list contains the IDs of all uploaded file

# %%
file_ID_list

# %% [markdown]
# We can see the `step_details` for two Steps:
# 
# 1. `tool_calls` (plural, since it could be more than one in a single Step)
# 2. `message_creation`
# 
# The first Step is a `tool_calls`, specifically using the `code_interpreter` which contains:
# 
# - `input`, which was the Python code generated before the tool was called, and
# - `output`, which was the result of running the Code Interpreter.
# 
# The second Step is a `message_creation`, which contains the `message` that was added to the Thread to communicate the results to the user.
# 

# %% [markdown]
# ### Retrieval
# 
# Another powerful tool in the Assistants API is [Retrieval](https://platform.openai.com/docs/assistants/tools/knowledge-retrieval): the ability to upload files that the Assistant will use as a knowledge base when answering questions. This can also be enabled from the Dashboard or the API, where we can upload files we want to be used.
# 

# %%
# Update Assistant
assistant = client.beta.assistants.update(
    MATH_ASSISTANT_ID,
    tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
    # file_ids=[file.id, file_2.id],
    file_ids=file_ID_list,
)
show_json(assistant)

# Below, in the quotes, add your prompt to GPT-4
# %%
thread, run = create_thread_and_run(
    "The seven key steps of the cancer-immunity cycle include: 1. Release of cancer antigens 2. Cancer antigen presentation 3. Priming and activation 4. Trafficking of T cells to tumors 5. Infiltration of T cells into tumors 6. Recognition of cancer cells by T cells 7. Killing of cancer cells. I have provided 11 PDF files. Please use only these files and exclude any external information. Using these files and no other external information, can you use these steps and give me a list of these steps and the corresponding considerations to bear for inhibitors and stimulators for each of these seven steps in the cancer immunity cycle"
)
run = wait_on_run(run, thread)
pretty_print(get_response(thread))



