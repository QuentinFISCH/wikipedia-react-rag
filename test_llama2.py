import requests
import json
from react.prompt import react_prompt


user_input = """
Question: `What is the moto of the university where Barack Obama transferred in 1981?`
Action: SearchKB with search_text "Barack Obama university transfer"
Observation: In 1981, Obama transferred from Occidental to Columbia University in New York City.
Thought: I need to find the motto of Columbia University, where Barack Obama transferred in 1981.
Action: SearchKB with search_text "Columbia University moto"
Observation: Columbia University's motto is "In Thy light shall we see light".
"""

# Action: SearchKB with search_text "Columbia University moto"
# Observation: Columbia University's motto is "In Thy light shall we see light".
# Thought: The motto of Columbia University is "In Thy light shall we see light".
# FinalAnswer: In Thy light shall we see light.
full_response = []

prompt = """
[INST] <<SYS>>
{react_prompt}
<</SYS>> [/INST]
[INST]
The user input is: {user_input}
What is the next action?
[/INST]
"""
url = 'http://localhost:11434/api/generate'
data = {
    "model": "llama2",
    "prompt": prompt.format(react_prompt=react_prompt, user_input=user_input)
}
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers, stream=True)
try:
    for line in response.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = json.loads(line.decode('utf-8'))
            # print(decoded_line['response'])  # uncomment to results, token by token
            full_response.append(decoded_line['response'])
finally:
    response.close()
print(''.join(full_response))
