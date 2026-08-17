"""
True AI Assist (Gemini Vision)
-------------------
This uses the Gemini 2.5 Flash model to act as a virtual civil engineer.
It analyzes the uploaded image to classify the road damage, determine its 
severity, and provide a reasoning.

Requires GEMINI_API_KEY environment variable.
"""
import os
import json
from google import genai
from google.genai import types

def suggest_from_image(image_path):
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("GEMINI_API_KEY not found, skipping AI analysis.")
            return None

        client = genai.Client(api_key=api_key)
        
        # Read image file
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        prompt = (
            "You are an expert civil engineer. Analyze the road damage in this image. "
            "Identify the damage type (choose from: pothole, crack, damaged_road, surface_damage). "
            "Determine the severity (choose from: low, medium, high, critical). "
            "Provide a confidence score between 0.0 and 1.0. "
            "Also provide a short 'ai_reasoning' string explaining your severity choice based on the image."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "damage_type": {"type": "STRING"},
                        "severity": {"type": "STRING"},
                        "confidence": {"type": "NUMBER"},
                        "ai_reasoning": {"type": "STRING"}
                    },
                    "required": ["damage_type", "severity", "confidence", "ai_reasoning"]
                }
            )
        )
        
        result = json.loads(response.text)
        
        # Ensure returned damage type and severity match our DB enums
        damage_mapping = {
            "pothole": "pothole",
            "crack": "crack",
            "damaged_road": "damaged_road",
            "surface_damage": "surface_damage"
        }
        
        sev_mapping = {
            "low": "low",
            "medium": "medium",
            "high": "high",
            "critical": "critical"
        }
        
        final_type = damage_mapping.get(result.get("damage_type", "").lower(), "pothole")
        final_sev = sev_mapping.get(result.get("severity", "").lower(), "medium")
        
        return {
            "damage_type": final_type,
            "severity": final_sev,
            "confidence": result.get("confidence", 0.8),
            "ai_reasoning": result.get("ai_reasoning", "Analyzed by Gemini AI.")
        }
    except Exception as e:
        print(f"AI Suggestion Error: {e}")
        return None
