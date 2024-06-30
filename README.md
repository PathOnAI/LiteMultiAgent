# MultiAgent


## 06/29, Saturday
* one agent
  * understand langchain agent design
  * change tavily_search to return the complete result for the first page
* multi agents
  * evaluation metrics: effectiveness, efficiency
    * for example, if we pass more tools to one agent, that agents could finish a lot of tasks, but it is very costly since there are too many prompt tokens
  * one super agent
    * delegation
      * https://github.com/OpenDevin/OpenDevin/blob/874b4c90753f5297512c7cf28b82da7b7aa14edd/agenthub/delegator_agent/agent.py#L14
      * study
      * coder
      * verifier