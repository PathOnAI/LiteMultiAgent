from autogen import config_list_from_json
import autogen
from datetime import datetime
import argparse
import os

import sys
from contextlib import redirect_stdout
from contextlib import contextmanager

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list, "seed": 42}

class GroupChat:
    def __init__(self):
        human_input_mode="ALWAYS"
        formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = "group_chat_work_dir"+"_"+formatted_datetime
        # Create user proxy agent, coder, product manager
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            system_message="A human admin who will give the idea and run the code provided by software_engineer.",
            code_execution_config={"last_n_messages": 2, "work_dir": dir_name, "use_docker":False},
            human_input_mode=human_input_mode,
        )
        self.swe = autogen.AssistantAgent(
            name="software_engineer",
            llm_config=llm_config,
        )
        self.pm = autogen.AssistantAgent(
            name="product_manager",
            system_message="You will help break down the initial idea into a well scoped requirement for the software_engineer; Do not involve in future conversations or error fixing",
            llm_config=llm_config,
        )

        # Create groupchat
        self.groupchat = autogen.GroupChat(agents=[self.user_proxy, self.swe, self.pm], messages=[])
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=llm_config)

    def start_chat(self,message):
        # Start the conversation
        self.user_proxy.initiate_chat(self.manager, message=message)

class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # Ensure real-time writing

    def flush(self):
        for f in self.files:
            f.flush()

@contextmanager
def redirect_stdout_to_file_and_terminal(file):
    original_stdout = sys.stdout
    sys.stdout = file
    try:
        yield
    finally:
        sys.stdout = original_stdout

def main():
    default_message = "Build a classic & basic Blackjack game with one standard 52-card decks and 2 players in python"
    parser = argparse.ArgumentParser(description="Chat initiation script")
    parser.add_argument("-f", "--filename", type=str,
                    help="filename that has the message to initiate the chat")
    args = parser.parse_args()
    filename = args.filename
    if filename:
        try:
            with open(filename, 'r',encoding='utf-8') as file:
                message = file.read().strip()
                print(f"File content: {message}")
        except FileNotFoundError:
            print(f"The file {filename} does not exist.")
    else:
        message = default_message 
    # print(f"The chat message is {message}")    
    group_chat = GroupChat()
    print(f"Starting chat...") 
    # Open a file to write output
    with open('output.txt', 'w') as f:
        # Create a Tee object to write to both sys.stdout and the file
        tee = Tee(sys.stdout, f)
        # Redirect sys.stdout to the Tee object
        sys.stdout = tee
        group_chat.start_chat(message)
    
    


if __name__ == "__main__":
    main()
    