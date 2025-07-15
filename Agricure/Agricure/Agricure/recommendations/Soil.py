import time
import requests
from typing import Dict, List, Optional

class ISDAsoilClient:
    BASE_URL = "https://api.isda-africa.com"
    LOGIN_ENDPOINT = "/login"
    SOILPROP_ENDPOINT = "/isdasoil/v2/soilproperty"
    TOKEN_LIFETIME = 3600  # seconds

    def __init__(self):
        self.username = "sseluyindaeva@gmail.com"
        self.password = "Password,jr10"
        self.token = None
        self.token_issued = 0

    def _login(self):
        resp = requests.post(
            f"{self.BASE_URL}{self.LOGIN_ENDPOINT}",
            data={"username": self.username, "password": self.password}
        )
        resp.raise_for_status()
        self.token = resp.json().get("access_token")
        self.token_issued = time.time()
        if not self.token:
            raise ValueError("Login failed: no token received")

    def _ensure_token(self):
        if (not self.token) or (time.time() - self.token_issued > self.TOKEN_LIFETIME - 60):
            self._login()

    def get_soil_properties(self, lat: float, lon: float, properties: list = None, depth: str = None) -> Optional[Dict]:
        """
        Fetch soil data at lat/lon.
        - properties: list e.g. ["ph", "carbon_organic"]
        - depth: "0-20" or "20-50"
        """
        self._ensure_token()
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"lat": lat, "lon": lon}
        if properties:
            params["property"] = ",".join(properties)
        if depth:
            params["depth"] = depth

        try:
            resp = requests.get(
                f"{self.BASE_URL}{self.SOILPROP_ENDPOINT}",
                headers=headers,
                params=params
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error getting soil data: {e}")
            return None

    def get_soil_for_gemini(self, lat: float, lon: float) -> List:
        """Get soil data formatted for Gemini AI input"""
        try:
            # Get comprehensive soil data
            raw_data = self.get_soil_properties(lat, lon)
            if not raw_data:
                return [None, None, None, None, None, None, None, None, None, None]
            
            # Extract and format soil properties
            filtered_data = filter_agronomy_soil(raw_data)
            
            # Return as list for Gemini
            return [
                filtered_data.get('pH', {}).get('value'),
                filtered_data.get('organic_carbon_gkg', {}).get('value'),
                filtered_data.get('total_nitrogen_gkg', {}).get('value'),
                filtered_data.get('extractable_phosphorus_ppm', {}).get('value'),
                filtered_data.get('extractable_potassium_ppm', {}).get('value'),
                filtered_data.get('cec_cmolkg', {}).get('value'),
                filtered_data.get('clay_percent', {}).get('value'),
                filtered_data.get('silt_percent', {}).get('value'),
                filtered_data.get('sand_percent', {}).get('value'),
                filtered_data.get('bulk_density_gcm3', {}).get('value')
            ]
        except Exception as e:
            print(f"Error formatting soil data for Gemini: {e}")
            return [None, None, None, None, None, None, None, None, None, None]

def filter_agronomy_soil(raw_data: Dict) -> Dict:
    """
    Extracts key soil properties for agronomic analysis.
    Returns a dictionary with up to 10 fields:
    - pH, organic carbon, total nitrogen, extractable phosphorus, potassium,
      cation exchange capacity (CEC), clay %, silt %, sand %, bulk density.
    """
    if not raw_data:
        return {}
    
    props = raw_data.get('property', {})
    depths = ['0-20', '20-50']

    def get_value(prop_name):
        arr = props.get(prop_name, [])
        # prefer 0–20 cm depth
        for item in arr:
            if item.get('depth', {}).get('value') == depths[0]:
                return item.get('value', {}).get('value'), item.get('value', {}).get('unit')
        # else pick first available
        if arr:
            return arr[0].get('value', {}).get('value'), arr[0].get('value', {}).get('unit')
        return None, None

    data = {}
    mapping = {
        'ph': 'pH',
        'carbon_organic': 'organic_carbon_gkg',
        'nitrogen_total': 'total_nitrogen_gkg',
        'phosphorous_extractable': 'extractable_phosphorus_ppm',
        'potassium_extractable': 'extractable_potassium_ppm',
        'cation_exchange_capacity': 'cec_cmolkg',
        'clay_content': 'clay_percent',
        'silt_content': 'silt_percent',
        'sand_content': 'sand_percent',
        'bulk_density': 'bulk_density_gcm3'
    }

    for key, out_key in mapping.items():
        val, unit = get_value(key)
        if val is not None:
            data[out_key] = {'value': val, 'unit': unit}

    return data

def get_soil_type_description(soil_data: List) -> str:
    """Convert soil composition to descriptive soil type"""
    if not soil_data or len(soil_data) < 10:
        return "Unknown soil type"
    
    ph, organic_carbon, total_nitrogen, phosphorus, potassium, cec, clay, silt, sand, bulk_density = soil_data
    
    # Basic soil texture classification
    if clay is not None and silt is not None and sand is not None:
        if clay > 40:
            texture = "clay"
        elif sand > 70:
            texture = "sandy"
        elif silt > 40:
            texture = "silty"
        else:
            texture = "loamy"
    else:
        texture = "mixed"
    
    # pH classification
    if ph is not None:
        if ph < 6.0:
            ph_desc = "acidic"
        elif ph > 7.5:
            ph_desc = "alkaline"
        else:
            ph_desc = "neutral"
    else:
        ph_desc = "moderate"
    
    return f"{ph_desc.capitalize()} {texture} soil"

# Example usage
if __name__ == "__main__":
    client = ISDAsoilClient()
    
    # Test coordinates (example location)
    lat, lon = -0.72, 35.24
    
    # Get soil data for Gemini
    soil_data = client.get_soil_for_gemini(lat, lon)
    print("Soil data for Gemini:", soil_data)
    
    # Get soil type description
    soil_type = get_soil_type_description(soil_data)
    print("Soil type:", soil_type)