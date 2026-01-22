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
    """
    循环请求模型，直到获得符合格式的解析结果
    """
    while True:
        response = llm.chat(agent, prompt)
        parsed_data = safe_parse_personality_response(response)
        if parsed_data is not None:
            return parsed_data

def personality_recognition_task(id, entry, llm):

    agent = f"""You are a professional personality assessment expert. Based on the following dialogue between Speaker A and Speaker B, assess their Big Five personality traits, which include:"""


    prompt = f"""
        You are a personality analysis expert. Your task is to infer the Big Five personality trait scores of the following two people (speaker A and speaker B) from multiple rounds of conversation. These traits include:

        - O: Openness to Experience
        - C: Conscientiousness
        - E: Extraversion
        - A: Agreeableness
        - N: Neuroticism

        Each trait should be scored on a scale from 0 to 1 (with one decimal point of precision), where 0 means very low and 1 means very high.

        Base your assessment solely on the content of the conversation, including each speaker's language use, tone, emotional expressions, attitude, and interpersonal behavior.

        **Conversation**:
        {entry}

        **Output** Never include explanations. Only return valid JSON objects in the specified format.
        Only output the following formats:
        "A": {{"Openness": float, "Conscientiousness": float, "Extraversion": float, "Agreeableness": float, "Neuroticism": float}}
        "B": {{"Openness": float, "Conscientiousness": float, "Extraversion": float, "Agreeableness": float, "Neuroticism": float}}
        """


    result = ask_personality_until_success(agent, prompt, llm)
    return result