from geopy.distance import geodesic

def calcular_distancia(lon1, lat1, lon2, lat2):
    punto1 = (lat1, lon1)
    punto2 = (lat2, lon2)
    distancia = geodesic(punto1, punto2).kilometers
    return distancia
