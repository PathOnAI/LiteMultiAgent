import threading
import queue
import time
import random

class Agent:
    def __init__(self, name, environment):
        self.name = name
        self.environment = environment
        self.message_queue = queue.Queue()

    def send_message(self, recipient, message):
        self.environment.send_message(self, recipient, message)

    def receive_message(self, sender, message):
        self.message_queue.put((sender, message))

    def process_messages(self):
        while True:
            try:
                sender, message = self.message_queue.get_nowait()
                print(f"{self.name} received: {message} from {sender.name}")
                # Process the message and potentially send a response
                response = f"Thanks for your message: {message}"
                self.send_message(sender, response)
            except queue.Empty:
                break

    def run(self):
        while True:
            self.process_messages()
            # Perform other actions
            time.sleep(random.uniform(0.5, 2))
            if random.random() < 0.3:  # 30% chance to send a message
                recipient = random.choice(self.environment.agents)
                if recipient != self:
                    message = f"Hello from {self.name}"
                    self.send_message(recipient, message)

class Environment:
    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def send_message(self, sender, recipient, message):
        recipient.receive_message(sender, message)

    def run_simulation(self):
        threads = []
        for agent in self.agents:
            thread = threading.Thread(target=agent.run)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()


env = Environment()
for i in range(5):
    agent = Agent(f"Agent-{i}", env)
    env.add_agent(agent)

env.run_simulation()