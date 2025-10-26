import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.call_function import call_function
import json

def main():

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. 
    If you need information, call a tool. Do not produce a final answer until you have enough information and are done with tool calls.
    When finished, respond with a plain natural-language answer and no tool calls.
    You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key) # a new instance of a gemini client

    if len(sys.argv) < 2:
        print("Usage: uv run main.py <prompt>")
        exit(1);
    user_prompt = sys.argv[1]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
            ]
    )
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ] # a list which stores only the user's message for now

    config=types.GenerateContentConfig(
        tools = [available_functions], 
        system_instruction=system_prompt)
    
    for iteration in range(20):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, config=config
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

        has_text = bool(response.text)
        has_tool_calls = bool(getattr(response, "function_calls", []))

        if has_text and not has_tool_calls:
            print("Final response: ")
            print(response.text)
            break
        else:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part)
                # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                try:
                    function_call_response = function_call_result.parts[0].function_response.response
                    if sys.argv[-1] == '--verbose':
                        print(f"-> {function_call_response}")
                    
                    tool_result = function_call_response.get("result")
                    tool_result_str = tool_result if isinstance(tool_result, str) else json.dumps(tool_result)
                    messages.append(
                        types.Content(role="user", parts=[types.Part(text=tool_result_str)])
                    )
                except Exception as e:
                    raise e
            # print(response.text)

    if len(sys.argv) == 3 and sys.argv[-1] == '--verbose':
        print("User prompt: ", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
