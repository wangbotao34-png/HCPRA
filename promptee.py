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
def emotion_prompt(turn_idx, speaker_now, speaker_other, utterance, history, global_history, personality_now, personality_other,abstract, llm):
  agent = f"""You are Speaker {speaker_now} in this conversation. Your personality traits are described by the Big Five (0-7 Scale) as: {personality_now}. Focus on recognizing your emotional state during the dialogue."""
  prompt = f"""You are Speaker {speaker_now} in a conversation with Speaker {speaker_other}.  
Based on the dialogue context, predict the emotion of the latest utterance.

Key Principles:
1. Default to Neutral:
   - When in doubt, prefer neutral emotion
   - Only assign emotions when there are clear emotional indicators
   - Consider neutral as the baseline emotional state

2. Emotion Detection Thresholds:
   - Require strong evidence for non-neutral emotions
   - Look for explicit emotional words or clear emotional context
   - Consider both verbal and contextual emotional cues

3. Personality Influence:
   - Use personality traits to validate emotional expressions
   - Consider personality as a filter rather than an amplifier
   - Be conservative in attributing emotions based on personality

Emotion Categories and Detection Criteria:
- angry (0.0-1.0): 
  * Requires explicit anger indicators (e.g., "damn", "hell", "annoying")
  * Or clear hostile/confrontational context
  * Default to 0.0 unless clear evidence exists
- disgust (0.0-1.0):
  * Requires explicit disgust indicators (e.g., "hate", "violent", "disgusting")
  * Or clear repulsion/aversion context
  * Default to 0.0 unless clear evidence exists
- fear (0.0-1.0):
  * Requires explicit fear indicators (e.g., "death", "bear", "nightmare")
  * Or clear threat/anxiety context
  * Default to 0.0 unless clear evidence exists
- happy (0.0-1.0):
  * Requires explicit happiness indicators (e.g., "good", "glad", "lcve")
  * Or clear positive/joyful context
  * Default to 0.0 unless clear evidence exists
- sad (0.0-1.0):
  * Requires explicit sadness indicators (e.g., "terrible", "bad", "apologize")
  * Or clear negative/sorrowful context
  * Default to 0.0 unless clear evidence exists
- surprise (0.0-1.0):
  * Requires explicit surprise indicators (e.g., "lucky", "chance", "guess")
  * Or clear unexpected/astonishing context
  * Default to 0.0 unless clear evidence exists
- neutral (0.0-1.0):
  * Default state when no clear emotions are present
  * Includes mild or ambiguous emotional expressions
  * Should be high (0.7-1.0) when no strong emotions are detected

Core subject discussed in the conversation:
{abstract}  

Conversation history:
{global_history}

Latest utterance:
Turn {turn_idx} {speaker_now}: {utterance}

Output your answer in the following format (Intensity values from 0.0 to 1.0):
[angry, disgust, fear, happy, sad, surprise, neutral]

Validation Rules:
1. Neutral Preference:
   - When no clear emotion is detected, set neutral to 0.8-1.0
   - Other emotions should be 0.0 in this case
   - Require strong evidence to override neutral state

2. Emotion Assignment:
   - Maximum of 1 emotion can have intensity > 0.5
   - Other emotions should be < 0.3
   - Sum of all intensities should be between 0.8 and 1.2

3. Evidence Requirements:
   - Require explicit emotional words or clear context
   - Be conservative in emotion attribution
   - Consider neutral as the default state

Do not explain or analyze. Respond only with the numerical array."""
    
  response = ask_model_until_success(agent, prompt, llm)
  return response