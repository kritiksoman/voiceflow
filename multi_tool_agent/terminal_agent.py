from google import genai
from google.genai import types
import os
from multi_tool_agent.index_db import window_tool
from multi_tool_agent.os_tools import set_current_window, close_given_window


instruction = "open finder."

def terminal_agent(instruction):
    # Define the function declaration for the model
    window_tool_function = {
        "name": "window_tool",
        "description": "Identify the program on which the user wants to perform an action.",
        "parameters": {
            "type": "object",
            "properties": {
                "window_name": {
                    "type": "string",
                    "description": "Name of the window to open or close. The name should be a valid application name on macOS.",
                }
            },
            "required": ["window_name"],
        },
    }

    open_window_function = {
        "name": "set_current_window",
        "description": "Open the given program.",
        "parameters": {
            "type": "object",
            "properties": {
                "window_name": {
                    "type": "string",
                    "description": "Name of the window to open. The name should be a valid application name on macOS.",
                }
            },
            "required": ["window_name"],
        },
    }

    close_window_function = {
        "name": "close_given_window",
        "description": "Close the given program.",
        "parameters": {
            "type": "object",
            "properties": {
                "window_name": {
                    "type": "string",
                    "description": "Name of the window to close. The name should be a valid application name on macOS.",
                }
            },
            "required": ["window_name"],
        },
    }

    # Configure the client and tools
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    state_tools = types.Tool(function_declarations=[window_tool_function])
    state_config = types.GenerateContentConfig(tools=[state_tools])

    action_tools = types.Tool(function_declarations=[open_window_function, close_window_function])
    action_config = types.GenerateContentConfig(tools=[action_tools])


    # Send request with function declarations
    state_response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Parse the user input to identify the window for the window_tool_function. \nUser input: {instruction}\n",
        config=state_config,
    )

    # Check for a function call
    if state_response.candidates[0].content.parts[0].function_call:
        function_call = state_response.candidates[0].content.parts[0].function_call
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        #  In a real app, you would call your function here:
        # result = function_call.name(**function_call.args)
        result = eval(function_call.name+"(**"+str(function_call.args)+")")
        state = result['metadatas'][0][0]['window_name']    # action = 

    else:
        print("Couldn't process state : ", state_response.text)


    action_response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"Parse the user input to identify the tool which should be called to perform the user's command. \nUser input: {instruction}\n",
    config=action_config,
    )

    # Check for a function call
    if action_response.candidates[0].content.parts[0].function_call:
        function_call = action_response.candidates[0].content.parts[0].function_call
        print(f"Function to call: {function_call.name}")
        print(f"Arguments: {function_call.args}")
        #  In a real app, you would call your function here:
        # result = function_call.name(**function_call.args)
        result = eval(function_call.name+"('"+state+"')")
        # state = result['metadatas'][0][0]['window_name']    # action = 
        print( )

    else:
        print("Couldn't process state : ", action_response.text)
    # print(result)
    print()