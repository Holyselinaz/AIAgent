import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions
from prompts import system_prompt


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description="Gemini CLI chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    # Build messages list
    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    # Handle function calls vs normal text
    function_calls = response.function_calls

    if function_calls:
        for function_call in function_calls:
            print(
                f"Calling function: "
                f"{function_call.name}({function_call.args})"
            )
    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print("Response:")

        print(response.text)


if __name__ == "__main__":
    main()