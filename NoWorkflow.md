# NoWorkflow
## general agent
* if there is a workflow of a use-case specific AI agent
  * convert the workflow into prompts
  * put all tools to one single agent
  * give the single agent the prompt to have a plan and execute

## different settings
  * use case specific agent:
    * define workflow for specific scenario, different agents work for different part of the work
      * example: one research agent, one production agent
      * use case: very specific use case
  * general agent:
    * a general agent but really work hard on the prompting
      * so it can make plan really well
    * a general agent chooses workflow, in each workflow there are different agents working together
      * the general agent is essentially doing the planning
        * but instead of planning by itself, it chooses from existing workflows
          * in each flow, the tool interaction is perfectly defined already!
        * currently if you ask LLM to make a plan, it couldn't utilize existing tools efficently in the planning stage
          * so sometimes, it's plan is not that good, takes more time and money
        * if it's really common-sense, maybe LLM can already do that
      * memory and tool
        * for each task, the general agent
          * only takes the final output of each step
          * if there are multiple steps
            * no need to append each step to the message list of the general agent
          * if in each step, the agent is calling multiple tools
            * no need to use the toolcall and toolresponse message
    * a general agent, whose use a list of agents as tools
      * example: one research agent that research different sources
      * memory and tool