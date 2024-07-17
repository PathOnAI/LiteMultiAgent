# Code Generation, Execution and Debugging
from autogen import config_list_from_json
import autogen
from datetime import datetime
import argparse
import os

import sys

# sys.path.append("../")

from autogen_utils import Tee

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config = {"config_list": config_list, "seed": 42}


class GroupChat:
    def __init__(self):
        human_input_mode = "NEVER"
        formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_name = "group_chat_work_dir" + "_" + formatted_datetime
        # Create user proxy agent, coder, product manager
        # self.user_proxy = autogen.UserProxyAgent(
        #     name="user_proxy",
        #     system_message="A human admin who will give the idea and run the code provided by software_engineer.",
        #     code_execution_config={"last_n_messages": 2, "work_dir": dir_name, "use_docker": False},
        #     human_input_mode=human_input_mode,
        # )
        self.debugger = autogen.AssistantAgent(
            name="debugger",
            # system_message="A human admin who will give the idea and run the code provided by software_engineer.",
            code_execution_config={"last_n_messages": 2, "work_dir": dir_name, "use_docker": False},
            # human_input_mode=human_input_mode,
            llm_config=llm_config,
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
        self.groupchat = autogen.GroupChat(agents=[self.debugger, self.swe, self.pm], messages=[], max_round=10)
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=llm_config, is_termination_msg=lambda x: x.get("content", "").rstrip().find("TERMINATE") >= 0,)

    def start_chat(self, message):
        # Start the conversation
        self.pm.initiate_chat(self.manager, message=message)


def main():
    default_message = "Build a calculator that add numbers from 1 to 100 in python"
    parser = argparse.ArgumentParser(description="Chat initiation script")
    parser.add_argument("-f", "--filename", type=str,
                        help="filename that has the message to initiate the chat")
    args = parser.parse_args()
    filename = args.filename
    # if filename:
    #     try:
    #         with open(filename, 'r', encoding='utf-8') as file:
    #             message = file.read().strip()
    #             print(f"File content: {message}")
    #     except FileNotFoundError:
    #         print(f"The file {filename} does not exist.")
    # else:
    #     message = default_message
    #     # print(f"The chat message is {message}")
    message = default_message
    group_chat = GroupChat()
    print(f"Starting chat...")
    # Open a file to write output
    # with open('output.txt', 'w') as f:
    #     # Create a Tee object to write to both sys.stdout and the file
    #     tee = Tee(sys.stdout, f)
    #     # Redirect sys.stdout to the Tee object
    #     sys.stdout = tee
    group_chat.start_chat(message)


if __name__ == "__main__":
    main()
