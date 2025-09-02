import math
from typing import List
from .entities import Location, Driver


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def find_drivers_within_radius(drivers: List[Driver], location: Location, radius_km: float) -> List[Driver]:
    """Find drivers within specified radius of a location"""
    nearby_drivers = []
    for driver in drivers:
        if driver.current_location:
            distance = calculate_distance(
                location.latitude, location.longitude,
                driver.current_location.latitude, driver.current_location.longitude
            )
            if distance <= radius_km:
                nearby_drivers.append(driver)
    return nearby_drivers


def find_closest_drivers(drivers: List[Driver], location: Location, limit: int) -> List[Driver]:
    """Find the closest drivers to a location, limited by count"""
    drivers_with_distance = []
    for driver in drivers:
        if driver.current_location:
            distance = calculate_distance(
                location.latitude, location.longitude,
                driver.current_location.latitude, driver.current_location.longitude
            )
            drivers_with_distance.append((driver, distance))
    
    drivers_with_distance.sort(key=lambda x: x[1])
    return [driver for driver, _ in drivers_with_distance[:limit]]