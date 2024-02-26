react_prompt = """
Using the ReAct framework, please provide reasoning traces and task-specific actions when answering the following question. Your only action is 'SearchKB' (Search Knowledge Base) that allows you to find information in a database. Given this constraint, answer the question provided by the user in single backticks.
There can be Thought, Action, Observation or FinalAnswer available after the question. So please do not to repeat a same Thought or Observation. Do not repeat the same search text for the action. If the latest search didn't extract any answer, try to change the search text.
If you don't get any answer from any of the Action try to divide what you are searching. Sometimes information about what you are trying to search might not be available together. You might need to go more granular.
If you don't know how ReAct framework works, refer the following example.

Question: `What is the moto of the university where Barack Obama transferred in 1981?`
Action: SearchKB with search_text "Barack Obama university transfer"
Observation: In 1981, Obama transferred from Occidental to Columbia University in New York City.
Thought: I need to find the motto of Columbia University, where Barack Obama transferred in 1981.
Action: SearchKB with search_text "Columbia University moto"
Observation: Columbia University's motto is "In Thy light shall we see light".
Thought: The motto of Columbia University is "In Thy light shall we see light".
FinalAnswer: In Thy light shall we see light.

The provided example is generic but you have to follow the steps as followed in the example.
First think, have a thought based on what's the question and then go take an action. Don't directly take any action without a thought in the history. Use the respective functions for Thought, Action, Observation, and FinalAnswer to reply.
A Thought is followed by an Action and an Action is followed by either Observation or FinalAnswer. I the final answer is not reached start with a Thought and follow the same process.
You have access to the history so don't repeat (call) the same Thoughts or Observations which are already available in the history. Also do not search the same search_text again if its already available in the history.
If you don't get any answer from the Action change the search_text in the next iteration.
Once you observe the final answer, please use the FinalAnswer function to provide the final answer.
Please go step by step, don't directly try and reach the final answer. Don't assume things!
"""

react_prompt_answer = """You will be provided with a question inside single backticks and history of action and reasoning inside triple backticks. The history will contain a flow of Thought, Action, Answer (Search Result), and Observation in multiple numbers. Using the history you need to answer the provided question. You just need to use the history to answer, please don't use your knowledge to answer. Moreover, using the history provide an explanation for the answer you reached at."""
