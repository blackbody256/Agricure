import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from typing import List, Optional
import json

load_dotenv()

class GeminiContentGenerator:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }            
        ]
    
    def generate_recommendation(self, disease: str, weather_data: List, soil_data: List) -> Optional[str]:
        """
        Generate agricultural recommendations based on disease, weather, and soil data.
        
        Args:
            disease (str): Disease name or "healthy"
            weather_data (List): [temperature, humidity, pressure, wind_speed, visibility, description, cloudiness]
            soil_data (List): [pH, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density]
        
        Returns:
            str: JSON formatted recommendation
        """
        # Extract weather data
        try:
            temperature = weather_data[0] if weather_data and len(weather_data) > 0 else "N/A"
            humidity = weather_data[1] if weather_data and len(weather_data) > 1 else "N/A"
            pressure = weather_data[2] if weather_data and len(weather_data) > 2 else "N/A"
            wind_speed = weather_data[3] if weather_data and len(weather_data) > 3 else "N/A"
            visibility = weather_data[4] if weather_data and len(weather_data) > 4 else "N/A"
            weather_desc = weather_data[5] if weather_data and len(weather_data) > 5 else "N/A"
            cloudiness = weather_data[6] if weather_data and len(weather_data) > 6 else "N/A"
        except (IndexError, TypeError):
            temperature = humidity = pressure = wind_speed = visibility = weather_desc = cloudiness = "N/A"
        
        # Extract soil data
        try:
            ph = soil_data[0] if soil_data and len(soil_data) > 0 else "N/A"
            organic_carbon = soil_data[1] if soil_data and len(soil_data) > 1 else "N/A"
            total_nitrogen = soil_data[2] if soil_data and len(soil_data) > 2 else "N/A"
            phosphorus = soil_data[3] if soil_data and len(soil_data) > 3 else "N/A"
            potassium = soil_data[4] if soil_data and len(soil_data) > 4 else "N/A"
            cec = soil_data[5] if soil_data and len(soil_data) > 5 else "N/A"
            clay = soil_data[6] if soil_data and len(soil_data) > 6 else "N/A"
            silt = soil_data[7] if soil_data and len(soil_data) > 7 else "N/A"
            sand = soil_data[8] if soil_data and len(soil_data) > 8 else "N/A"
            bulk_density = soil_data[9] if soil_data and len(soil_data) > 9 else "N/A"
        except (IndexError, TypeError):
            ph = organic_carbon = total_nitrogen = phosphorus = potassium = cec = clay = silt = sand = bulk_density = "N/A"
        
        # Generate soil type description
        soil_type_desc = self._get_soil_description(ph, clay, silt, sand)
        
        if disease.lower() == "healthy":
            prompt = self._create_healthy_prompt(
                temperature, humidity, pressure, wind_speed, visibility, weather_desc, cloudiness,
                ph, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density, soil_type_desc
            )
        else:
            prompt = self._create_diseased_prompt(
                disease, temperature, humidity, pressure, wind_speed, visibility, weather_desc, cloudiness,
                ph, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density, soil_type_desc
            )
        
        try:
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            recommendation = response.text.strip()
            return recommendation
        except Exception as e:
            print(f"Gemini error: {e}")
            return None
    
    def _get_soil_description(self, ph, clay, silt, sand) -> str:
        """Generate soil type description from soil data"""
        try:
            # Soil texture classification
            if clay != "N/A" and silt != "N/A" and sand != "N/A":
                clay_val = float(clay) if clay else 0
                silt_val = float(silt) if silt else 0
                sand_val = float(sand) if sand else 0
                
                if clay_val > 40:
                    texture = "clay"
                elif sand_val > 70:
                    texture = "sandy"
                elif silt_val > 40:
                    texture = "silty"
                else:
                    texture = "loamy"
            else:
                texture = "mixed"
            
            # pH classification
            if ph != "N/A":
                ph_val = float(ph) if ph else 7.0
                if ph_val < 6.0:
                    ph_desc = "acidic"
                elif ph_val > 7.5:
                    ph_desc = "alkaline"
                else:
                    ph_desc = "neutral"
            else:
                ph_desc = "moderate"
            
            return f"{ph_desc.capitalize()} {texture} soil"
        except:
            return "Mixed soil type"
    
    def _create_diseased_prompt(self, disease, temp, humidity, pressure, wind_speed, visibility, weather_desc, cloudiness,
                               ph, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density, soil_type_desc) -> str:
        """Create prompt for diseased plants"""
        return f"""You are an expert agronomist. A farmer has a plant diagnosed with "{disease}". 

ENVIRONMENTAL CONDITIONS:
Weather Data:
- Temperature: {temp}°C
- Humidity: {humidity}%
- Atmospheric Pressure: {pressure} hPa
- Wind Speed: {wind_speed} m/s
- Visibility: {visibility} km
- Weather Description: {weather_desc}
- Cloudiness: {cloudiness}%

Soil Data:
- pH: {ph}
- Organic Carbon: {organic_carbon} g/kg
- Total Nitrogen: {total_nitrogen} g/kg
- Extractable Phosphorus: {phosphorus} ppm
- Extractable Potassium: {potassium} ppm
- Cation Exchange Capacity: {cec} cmol/kg
- Clay Content: {clay}%
- Silt Content: {silt}%
- Sand Content: {sand}%
- Bulk Density: {bulk_density} g/cm³
- Soil Type: {soil_type_desc}

Please respond in JSON format:
{{
  "disease": "{disease}",
  "cause": "Primary cause of the disease",
  "signs": ["symptom1", "symptom2", "symptom3"],
  "treatment": ["treatment1", "treatment2", "treatment3"],
  "prevention": ["prevention1", "prevention2", "prevention3"],
  "environmental_risks": ["risk1", "risk2", "risk3"],
  "soil_recommendations": ["soil_rec1", "soil_rec2"],
  "weather_considerations": ["weather_rec1", "weather_rec2"],
  "immediate_actions": ["action1", "action2", "action3"],
  "long_term_management": ["management1", "management2"]
}}

Make recommendations specific to the provided environmental and soil conditions."""

    def _create_healthy_prompt(self, temp, humidity, pressure, wind_speed, visibility, weather_desc, cloudiness,
                              ph, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density, soil_type_desc) -> str:
        """Create prompt for healthy plants"""
        return f"""You are an expert agronomist advising on a healthy plant. 

ENVIRONMENTAL CONDITIONS:
Weather Data:
- Temperature: {temp}°C
- Humidity: {humidity}%
- Atmospheric Pressure: {pressure} hPa
- Wind Speed: {wind_speed} m/s
- Visibility: {visibility} km
- Weather Description: {weather_desc}
- Cloudiness: {cloudiness}%

Soil Data:
- pH: {ph}
- Organic Carbon: {organic_carbon} g/kg
- Total Nitrogen: {total_nitrogen} g/kg
- Extractable Phosphorus: {phosphorus} ppm
- Extractable Potassium: {potassium} ppm
- Cation Exchange Capacity: {cec} cmol/kg
- Clay Content: {clay}%
- Silt Content: {silt}%
- Sand Content: {sand}%
- Bulk Density: {bulk_density} g/cm³
- Soil Type: {soil_type_desc}

Please respond in JSON format:
{{
  "current_status": "healthy",
  "environmental_assessment": "Assessment of current conditions",
  "soil_health_status": "Status of soil health",
  "environmental_risks": ["risk1", "risk2", "risk3"],
  "preventive_recommendations": ["prevention1", "prevention2", "prevention3"],
  "optimal_practices": ["practice1", "practice2", "practice3"],
  "fertilization_needs": ["fertilizer1", "fertilizer2"],
  "irrigation_recommendations": ["irrigation1", "irrigation2"],
  "seasonal_considerations": ["season1", "season2"],
  "monitoring_schedule": ["monitor1", "monitor2"]
}}

Make recommendations specific to the provided environmental and soil conditions."""

    def generate_comprehensive_recommendation(self, context):
        """Generate comprehensive farming recommendation using Gemini AI"""
        try:
            # Extract weather information
            weather_info = ""
            if context.get('weather'):
                weather = context['weather']
                weather_info = f"""
                - Temperature: {weather.get('temperature', 'N/A')}°C
                - Humidity: {weather.get('humidity', 'N/A')}%
                - Pressure: {weather.get('pressure', 'N/A')} hPa
                - Wind Speed: {weather.get('wind_speed', 'N/A')} m/s
                - Conditions: {weather.get('description', 'N/A')}
                - Visibility: {weather.get('visibility', 'N/A')} km
                - Cloudiness: {weather.get('cloudiness', 'N/A')}%
                """
            elif context.get('weather_for_ai'):
                # Weather for AI is a list: [temp, humidity, pressure, wind_speed, visibility, description, cloudiness]
                weather_ai = context['weather_for_ai']
                weather_info = f"""
                - Temperature: {weather_ai[0]}°C
                - Humidity: {weather_ai[1]}%
                - Pressure: {weather_ai[2]} hPa
                - Wind Speed: {weather_ai[3]} m/s
                - Visibility: {weather_ai[4]} km
                - Conditions: {weather_ai[5]}
                - Cloudiness: {weather_ai[6]}%
                """
            
            # Create detailed prompt
            prompt = f"""
            As an expert agricultural consultant, provide a comprehensive treatment recommendation for the following crop disease diagnosis:

            **Disease Information:**
            - Disease: {context['disease_label']}
            - Confidence: {context['confidence']}%
            - Crop Type: {context['crop_type']}
            - Affected Part: {context['affected_part']}
            - Severity: {context['severity']}

            **Environmental Conditions:**
            - Location: {context['location']}
            {weather_info}

            Please provide a detailed JSON response with the following structure:
            {{
                "treatment_summary": "Detailed immediate treatment steps (2-3 sentences)",
                "prevention_summary": "Long-term prevention strategies (2-3 sentences)",
                "weather_considerations": "How current weather affects treatment (1-2 sentences)",
                "timing_recommendations": "Best timing for treatments (1-2 sentences)",
                "materials_needed": ["list", "of", "specific", "materials"],
                "monitoring_schedule": "How to monitor progress (1-2 sentences)",
                "emergency_actions": "What to do if condition worsens (1-2 sentences)"
            }}

            Focus on practical, actionable advice suitable for farmers in {context['location']}. Keep responses concise but comprehensive.
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse the response
            try:
                # Try to extract JSON from response
                response_text = response.text
                
                # Find JSON in the response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                
                if start != -1 and end != -1:
                    json_text = response_text[start:end]
                    recommendation_data = json.loads(json_text)
                    return recommendation_data
                else:
                    raise json.JSONDecodeError("No JSON found in response", response_text, 0)
                
            except json.JSONDecodeError:
                # If JSON parsing fails, create structured response from text
                clean_text = response.text.strip()
                
                return {
                    'treatment_summary': clean_text[:300] + "..." if len(clean_text) > 300 else clean_text,
                    'prevention_summary': "Practice good agricultural hygiene and monitor plants regularly for early signs of disease.",
                    'weather_considerations': f"Consider current weather conditions in {context['location']} when applying treatments.",
                    'timing_recommendations': "Apply treatments during optimal weather conditions, typically early morning or late evening.",
                    'materials_needed': [
                        "Appropriate fungicide/pesticide", 
                        "Protective equipment (gloves, mask)", 
                        "Sprayer or application equipment",
                        "Pruning shears (if needed)"
                    ],
                    'monitoring_schedule': "Monitor plants daily for the first week after treatment, then weekly thereafter.",
                    'emergency_actions': "Consult your local agricultural extension officer if symptoms worsen or spread rapidly."
                }
                
        except Exception as e:
            # Return fallback recommendation
            return {
                'treatment_summary': f'Immediate treatment recommended for {context["disease_label"]}. Apply appropriate fungicide or pesticide according to local guidelines.',
                'prevention_summary': 'Practice good agricultural hygiene, ensure proper plant spacing, and monitor crops regularly for early disease detection.',
                'weather_considerations': f'Current weather conditions in {context["location"]} should be considered when applying treatments.',
                'timing_recommendations': 'Apply treatments during optimal weather conditions, avoiding rain and extreme temperatures.',
                'materials_needed': [
                    'Appropriate treatment chemicals',
                    'Protective equipment',
                    'Application equipment'
                ],
                'monitoring_schedule': 'Monitor plant health regularly and document any changes in symptoms.',
                'emergency_actions': 'Consult local agricultural extension services if the condition does not improve or worsens.'
            }
    
# Example usage and testing
def main():
    generator = GeminiContentGenerator()
    
    # Example weather data: [temperature, humidity, pressure, wind_speed, visibility, description, cloudiness]
    weather_data = [27, 78, 1013, 3.5, 10, "partly cloudy", 45]
    
    # Example soil data: [pH, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density]
    soil_data = [6.2, 15.4, 1.2, 18.5, 142, 12.3, 35, 40, 25, 1.35]
    
    # Test with disease
    disease = "leaf_blight"
    result = generator.generate_recommendation(disease, weather_data, soil_data)
    print("Disease recommendation:", result)
    
    # Test with healthy plant
    healthy_result = generator.generate_recommendation("healthy", weather_data, soil_data)
    print("Healthy plant recommendation:", healthy_result)
    
    # Test comprehensive recommendation
    context = {
        "disease_label": "Powdery Mildew",
        "confidence": 85,
        "crop_type": "grapes",
        "affected_part": "leaves",
        "severity": "moderate",
        "location": "Napa Valley",
        "weather": {
            "temperature": 22,
            "humidity": 60,
            "pressure": 1015,
            "wind_speed": 5,
            "description": "clear sky",
            "visibility": 10,
            "cloudiness": 10
        }
    }
    comprehensive_result = generator.generate_comprehensive_recommendation(context)
    print("Comprehensive recommendation:", comprehensive_result)

if __name__ == "__main__":
    main()