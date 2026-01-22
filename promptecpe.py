import ast

def safe_parse_response(response):
    try:
        response = response.strip()
        parsed_list = ast.literal_eval(response)
        if not isinstance(parsed_list, list):
            raise ValueError(f"Parsed result is not a list: {parsed_list}")
        return parsed_list
    except Exception as e:
        print(f"Error when EE: {e}")
        return None

def ask_model_until_success(agent, prompt, llm):
    while True:
        response = llm.chat(agent, prompt)
        parsed_list = safe_parse_response(response)
        if parsed_list is not None:
            return parsed_list
def ecp_prompt(turn_idx, speaker_now,speaker_other, utterance, history, personality_now,personality_other,abstract,llm):
  system_prompts = f"""You are the speaker {speaker_now} in this conversation. Your personality is described by the Big Five traits (0-7 Scale) as follows: {personality_now}. You should analyze your own internal emotional causes based on the conversation context."""
  user_prompts = f"""You are Speaker {speaker_now} in the following conversation with Speaker {speaker_other}.
You are an emotional reasoning agent. Your task is to **analyze only the latest utterance** and extract emotion-cause pairs.

Core subject discussed in the conversation:
{abstract}  

Conversation history:
{history} 

Latest utterance (the sole focus of your analysis):
Turn {turn_idx} {speaker_now}: {utterance}

Follow these steps:

**STEP 1: Emotion Detection**
Use **Appraisal Theory** to assess if the latest utterance expresses emotion.
- Consider the following factors:
  - Goal Congruence: Did the speaker's expectation match reality?
  - Agency: Who or what triggered the emotion (self, other, or external)?
  - Norm Violation: Was there a social or moral breach?
  - Controllability: Could the speaker control the event or situation?
If emotion is **detected**, proceed to **STEP 2**. If no emotion is detected, output:
{{
  "emotion_potential": false,
  "emotion_cause_pairs": []
}}
and stop.
**STEP 2: Reasoning & Emotion-Cause Pair Extraction**
For the latest turn {turn_idx} utterance, you MUST evaluate all five reasoning paths:
  - **Current Self Cause**: Identify if the latest turn {turn_idx} utterance is the cause of Speaker {speaker_now}'s emotion.
  - **Previous Self Cause**: Identify which prior utterance by Speaker {speaker_now} triggered the emotion in the latest turn {turn_idx} utterance.
  - **Empathy Cause**: Identify which prior turn by Speaker {speaker_other} showed empathy towards Speaker {speaker_now}, triggering the emotion in the latest turn {turn_idx} utterance.
  - **Sarcasm Cause**: Identify which prior turn by Speaker {speaker_other} involved sarcasm or mockery, triggering the emotion in the latest turn {turn_idx} utterance.
  - **External Cause**: Identify any external events (other than Speaker {speaker_now} and Speaker {speaker_other}) mentioned in prior turns that triggered the emotion in the latest turn {turn_idx} utterance.

**STEP 3: Output (Strict Format)**
Output a single JSON object in the following format, and nothing else:
{{
  "emotion_potential": "true_or_false",
  "appraisal": {{
    "goal_congruence": "true_or_false",
    "agency": "self/other/external",
    "norm_violation": "true_or_false",
    "controllability": "true_or_false"
  }},
  "Current_Self_Cause": {{
      "confidence": "float_from_0_to_1",
      "emotion_cause_pairs":  [{turn_idx}, cause_turn_number] 
    ,...}}, 
  "Previous_Self_Cause": {{
      "confidence": "float_from_0_to_1",
      "emotion_cause_pairs":  [{turn_idx}, cause_turn_number] 
    ,...}}, 
  "Empathy_Cause": {{ 
      "confidence": "float_from_0_to_1",
      "emotion_cause_pairs":  [{turn_idx}, cause_turn_number] 
    ,...}},   
  "Sarcasm_Cause": {{
      "confidence": "float_from_0_to_1",
      "emotion_cause_pairs":  [{turn_idx}, cause_turn_number] 
    ,...}},    
  "External_Cause": {{
      "confidence": "float_from_0_to_1",
      "emotion_cause_pairs":  [{turn_idx}, cause_turn_number] 
    ,...}}, 
  "emotion_cause_pairs": [
    [{turn_idx}, cause_turn_number_1],
    [{turn_idx}, cause_turn_number_2],
    ...]
}}

**STEP 4: Reflection**  
Before outputting the JSON, reflect silently:

- Did you check all reasoning paths separately?  
- Did you miss a weaker but valid cause from another path?  
- If only one cause was chosen, was that due to model bias or true exclusivity?

Revise if needed. Output only the final JSON.

- Do NOT output any explanation, reasoning process, or any text outside the JSON object.
- If no emotion is detected, set "emotion_potential": false and "emotion_cause_pairs": [].
"""
  response = ask_model_until_success(system_prompts,user_prompts,llm)

  return response