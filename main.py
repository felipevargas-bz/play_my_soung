from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
origins = [
    "*"  # Si usas otro puerto o frontend diferente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # O usa ["*"] para todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube API key.
API_KEY = "AIzaSyD0AVt10WBiVp3sqbukm5t4Ew76-uYZ2Cs"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def send_response_to_chatwoot(message: str):
    import requests

    account_id = "95848"
    api_token = "tywKFxfaWW93HUVDWGcc6uxf"
    conversation_id = "6"
    base_url = 'https://app.chatwoot.com/api/v1'
    end_point = f"/accounts/{account_id}/conversations/{conversation_id}/messages"
    url = f'{base_url}{end_point}'
    headers = {
        "Content-Type": "application/json",
        "api_access_token": api_token
    }
    data = {
        "content": str(message),
        "message_type": "outgoing",
        "private": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        try:
            response_json = response.json()
            print(f"Response JSON: {response_json}")
        except ValueError:
            print("No se pudo decodificar la respuesta como JSON.")
    else:
        print("Error en la solicitud: ", response.status_code)


@app.post("/schedule")
def schedule_message(body: dict):
    """
    Endpoint to schedule a message to be sent to Chatwoot.
    """
    message = f"""
    {body['name']}
    
    {body["link"]}
    """
    send_response_to_chatwoot(message)
    return {"message": "Message scheduled successfully!"}


@app.get("/search", response_model=List[dict])
def search_videos(query: str):
    """
    Endpoint to search for music videos on YouTube based on the provided query.
    Uses the videoCategoryId=10 parameter to filter results for music.
    """
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",  # Music category
        "maxResults": 5,
        "key": API_KEY
    }
    
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error calling YouTube API")
    
    data = response.json()
    results = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        video_title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        results.append({"title": video_title, "url": video_url})
    
    return results

if __name__ == "__main__":
    send_response_to_chatwoot("Hello there!")