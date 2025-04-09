from consts import SECTIONS_TO_EXTRACT, DELETE_SECTIONS
import re

def midpoint(lat1, lon1, lat2, lon2):
    return {"latitude": (lat1 + lat2)/2, "longitude": (lon1 + lon2)/2}

def format_coordinates(coords: list) -> dict:
    return midpoint(coords[0][0], coords[0][1], coords[1][0], coords[1][1])

def handle_info_section(obj: dict):
    data = obj.pop("sectionConfiguration")["root"]["sections"]
    obj["overview"] = data
    return obj

def process_json(obj, section_name):
    if section_name == "lnglat":
        coordinates = find_coordinates(obj)
        if coordinates:
            return format_coordinates(coordinates)
        return {}
    
    extracted_data = {}
    found_sections = set()
    
    def traverse(data, path=""):
        if data is None:
            return None
            
        if isinstance(data, dict):
            result = {}
            for section in SECTIONS_TO_EXTRACT:
                if section in data and section not in found_sections:
                    found_sections.add(section)
                    extracted_data[section] = traverse(data[section])
            
            for key, value in data.items():
                if key in DELETE_SECTIONS or key == "showMoreButton" or key == "__typename":
                    continue
                processed_value = traverse(value, f"{path}.{key}" if path else key)
                if processed_value is not None:
                    result[key] = processed_value
                    
            return result if result else None
            
        elif isinstance(data, list):
            result = []
            for item in data:
                processed_item = traverse(item, path)
                if processed_item is not None:
                    result.append(processed_item)
            return result if result else None
            
        else:
            return data
    
    traverse(obj)
    if section_name == "reviews":
        extracted_data = find_first_array(obj)
    return extracted_data

def find_coordinates(obj):
    if isinstance(obj, list) and len(obj) > 1 and isinstance(obj[1], list):
        try:
            return obj[1][0][1]
        except (IndexError, TypeError):
            pass
    
    if isinstance(obj, dict):
        for value in obj.values():
            result = find_coordinates(value)
            if result:
                return result
    
    if isinstance(obj, list):
        for item in obj:
            result = find_coordinates(item)
            if result:
                return result
    
    return None

def search_key(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        
        for k, v in data.items():
            found = search_key(v, key)
            if found is not None:
                return found
    
    elif isinstance(data, list):
        for item in data:
            found = search_key(item, key)
            if found is not None:
                return found
    
    return None

def find_first_array(obj):
    if isinstance(obj, list):
        return obj
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            result = find_first_array(value)
            if result:
                return result

    return []