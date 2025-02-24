import googlemaps

class GoogleMap:

    _instance = None

    def __new__(cls, api_key=""):
        
        if cls._instance is None:
            cls._instance = super(GoogleMap, cls).__new__(cls)
            cls._instance.client = googlemaps.Client(key=api_key)  # ✅ Google Maps API 객체 생성
        return cls._instance  

