import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini API client
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

def get_game_recommendations(prompt, count=4):
    """
    Generate video game recommendations based on a user prompt using Google's Gemini API.
    Only returns game names, without any additional information.
    
    Args:
        prompt (str): User's description of what kind of game they're looking for
        count (int): Number of game recommendations to generate. 1 main game + 3 similar games.
        
    Returns:
        list: List of strings containing recommended game names
    """
    system_instruction = f"""
    You are a video game recommendation expert. When given a description or request,
    recommend exactly {count} video games that match the criteria.
    
    The FIRST game should be the BEST match for the user's request.
    The remaining {count-1} games should be SIMILAR to the first game but with interesting variations.
    
    ONLY return the exact titles of the games. DO NOT include any other information.
    Your response should be ONLY a valid JSON array of strings with JUST the game names.
    
    Example response format:
    ["Game Title 1", "Game Title 2", "Game Title 3", "Game Title 4"]
    
    DO NOT include any explanation, description, or additional text in your response.
    IMPORTANT: Make sure to return ONLY valid complete JSON array of strings.
    """
    
    try:
        # Configure Google Search as a tool for grounding
        google_search_tool = Tool(
            google_search = GoogleSearch()
        )
        
        # Make the request with Google Search grounding enabled
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=2048,
                tools=[google_search_tool],  # Enable Google Search grounding
            )
        )
        
        # Extract the text response
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            # Get the text from the first part of the first candidate's content
            response_text = response.candidates[0].content.parts[0].text
            
            # Parse the text as JSON - the system instruction tells the model to format as JSON
            try:
                # Find JSON array in the text (in case model includes explanatory text)
                json_match = re.search(r'(\[[\s\S]*\])', response_text)
                if json_match:
                    json_text = json_match.group(1)
                else:
                    json_text = response_text
                
                # Parse the JSON array of game names
                game_names = json.loads(json_text)
                
                # Ensure we have exactly 'count' games (or fewer if that's all we got)
                if len(game_names) > count:
                    game_names = game_names[:count]
                    
                return game_names
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON from Gemini response: {e}")
                print(f"Raw response: {response_text}")
                return []
        else:
            print("No valid candidates found in the response")
            return []
    except Exception as e:
        # Log the error and return an empty list
        print(f"Error getting recommendations from Gemini: {e}")
        return []