"""
API Manager - Centralized management of external API integrations
"""
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime, timedelta
import httpx
from config import settings
from utils.logger import logger


class APIManager:
    """
    Manages external API integrations with rate limiting and caching
    """
    
    def __init__(self):
        """Initialize API manager"""
        self.client = httpx.AsyncClient(timeout=30.0)
        self.cache = {}
        self.cache_ttl = {}
        logger.info("API Manager initialized")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached response if still valid"""
        if key in self.cache:
            if datetime.now() < self.cache_ttl.get(key, datetime.now()):
                logger.debug(f"Cache hit for {key}")
                return self.cache[key]
            else:
                # Cache expired
                del self.cache[key]
                del self.cache_ttl[key]
        return None
    
    def _set_cache(self, key: str, value: Any, ttl_minutes: int = 10):
        """Cache response"""
        self.cache[key] = value
        self.cache_ttl[key] = datetime.now() + timedelta(minutes=ttl_minutes)
        logger.debug(f"Cached {key} for {ttl_minutes} minutes")
    
    async def search_web(self, query: str, engine: str = "google") -> Dict[str, Any]:
        """
        Search the web using specified search engine
        
        Args:
            query: Search query
            engine: Search engine to use (google, bing)
            
        Returns:
            Search results
        """
        cache_key = f"search:{engine}:{query}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            if engine == "google" and settings.google_search_api_key:
                results = await self._google_search(query)
            elif engine == "bing" and settings.bing_search_api_key:
                results = await self._bing_search(query)
            else:
                results = {"error": "Search engine not configured"}
            
            self._set_cache(cache_key, results, ttl_minutes=60)
            return results
            
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return {"error": str(e)}
    
    async def _google_search(self, query: str) -> Dict[str, Any]:
        """Search using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": settings.google_search_api_key,
            "cx": settings.google_search_engine_id,
            "q": query
        }
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant information
        results = []
        for item in data.get("items", [])[:5]:
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })
        
        return {"results": results, "query": query}
    
    async def _bing_search(self, query: str) -> Dict[str, Any]:
        """Search using Bing Search API"""
        url = "https://api.bing.microsoft.com/v7.0/search"
        headers = {"Ocp-Apim-Subscription-Key": settings.bing_search_api_key}
        params = {"q": query, "count": 5}
        
        response = await self.client.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("webPages", {}).get("value", []):
            results.append({
                "title": item.get("name"),
                "link": item.get("url"),
                "snippet": item.get("snippet")
            })
        
        return {"results": results, "query": query}
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """
        Get weather information for a location
        
        Args:
            location: City name or coordinates
            
        Returns:
            Weather data
        """
        if not settings.openweather_api_key:
            return {"error": "Weather API not configured"}
        
        cache_key = f"weather:{location}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": location,
                "appid": settings.openweather_api_key,
                "units": "metric"
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            weather = {
                "location": data.get("name"),
                "temperature": data.get("main", {}).get("temp"),
                "description": data.get("weather", [{}])[0].get("description"),
                "humidity": data.get("main", {}).get("humidity"),
                "wind_speed": data.get("wind", {}).get("speed")
            }
            
            self._set_cache(cache_key, weather, ttl_minutes=30)
            return weather
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return {"error": str(e)}
    
    async def get_news(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Get latest news
        
        Args:
            topic: News topic or None for general news
            
        Returns:
            News articles
        """
        if not settings.news_api_key:
            return {"error": "News API not configured"}
        
        cache_key = f"news:{topic or 'general'}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": settings.news_api_key,
                "pageSize": 5
            }
            
            if topic:
                params["q"] = topic
            else:
                params["country"] = "us"
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name"),
                    "published_at": article.get("publishedAt")
                })
            
            result = {"articles": articles, "topic": topic}
            self._set_cache(cache_key, result, ttl_minutes=15)
            return result
            
        except Exception as e:
            logger.error(f"News API error: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global API manager instance
api_manager = APIManager()
