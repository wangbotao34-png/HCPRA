import ast
import json

def safe_parse_personality_response(response):

    try:

        clean_response = response.strip()

        parsed_data = ast.literal_eval(clean_response)
        

        if isinstance(parsed_data, dict) and "A" in parsed_data and "B" in parsed_data:
            return parsed_data
        else:
            raise ValueError(f"Format mismatch: {parsed_data}")
    except Exception as e:
        print(f"Error when parsing personality: {e}")
        return None

def ask_personality_until_success(agent, prompt, llm):
    while True:
        response = llm.chat(agent, prompt)
        parsed_data = safe_parse_personality_response(response)
        if parsed_data is not None:
            return parsed_data

def personality_recognition_task(id, entry, llm):

    agent = """You are a conversation summarization expert. Your task is to summarize the main topic of a conversation in one concise sentence. Focus on the core subject and key points."""

    prompt = f"""Create a one-sentence summary of this conversation as a static memory record. The summary should:
        1. Identify the conversation setting/scene
        2. State the main topic of discussion
        3. Describe the key content exchanged
        4. Keep the summary factual and objective
        5. Avoid emotional interpretations

        **Conversation:**
        {entry}

        Format: "In a [setting/scene], a conversation about [topic] where [Speaker A] [content] and [Speaker B] [content]" """

    result = ask_personality_until_success(agent, prompt, llm)
    return result
