import json
import openai

from core.schema import Experience


def init_openai(api_key):
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", )
    print(completion.choices[0].message.content)


def extract_skills_from_experience(experience: Experience, api_key):
    openai.api_key = api_key

    # flatten the list of highlights and remove duplicates
    highlights = list(set([item for sublist in experience.highlights for item in sublist]))

    # convert highlights into prompt that will identify any job skills in the highlights
    prompt = (f"Following is a list of highlights from my resume. "
              f"Each highlight is a task I've worked on. "
              f"Each highlight is separated with || "
              f"Identify any job skills from the highlights on this list. "
              f"Your response should be a list of skills separated by ||, "
              f"Do not include any other text in your response. The list of highlights is: ")

    for highlight in highlights:
        prompt += f"{highlight}||"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # extract the skills from the chatcompletion
    content = completion['choices'][0]['message']['content']

    # remove any duplicates and empty strings
    skills = list(set([skill.strip() for skill in content.split('||') if skill]))

    return skills









def format_skills(resume):
    skills = resume['skills']
    skills_list = []

    for skill in skills:
        skills_list.append(skill)

    return skills_list


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )

    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response

print(run_conversation())