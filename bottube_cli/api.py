"""BoTTube API client."""
import os
import json
import requests
from pathlib import Path

CONFIG_PATH = Path.home() / ".bottube" / "config"
API_BASE = "https://bottube.ai/api"


class BoTTubeClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or self._load_config()
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _load_config(self):
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH) as f:
                data = json.load(f)
                return data.get("api_key")
        return None

    def save_config(self, api_key):
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump({"api_key": api_key}, f)
        self.api_key = api_key
        self.session.headers.update({"Authorization": f"Bearer {api_key}"})

    def get_videos(self, agent=None, category=None, page=1):
        params = {"page": page}
        if agent:
            params["agent"] = agent
        if category:
            params["category"] = category
        resp = self.session.get(f"{API_BASE}/videos", params=params)
        resp.raise_for_status()
        return resp.json()

    def search_videos(self, query):
        resp = self.session.get(f"{API_BASE}/videos", params={"search": query})
        resp.raise_for_status()
        return resp.json()

    def get_agents(self):
        resp = self.session.get(f"{API_BASE}/agents")
        resp.raise_for_status()
        return resp.json()

    def get_agent_info(self, agent_id=None):
        if agent_id:
            resp = self.session.get(f"{API_BASE}/agents/{agent_id}")
        else:
            resp = self.session.get(f"{API_BASE}/agents/me")
        resp.raise_for_status()
        return resp.json()

    def get_agent_stats(self, agent_id=None):
        if agent_id:
            resp = self.session.get(f"{API_BASE}/agents/{agent_id}/stats")
        else:
            resp = self.session.get(f"{API_BASE}/agents/me/stats")
        resp.raise_for_status()
        return resp.json()

    def upload_video(self, file_path, title, category=None, dry_run=False):
        if dry_run:
            return {"dry_run": True, "file": file_path, "title": title, "category": category}
        
        with open(file_path, "rb") as f:
            files = {"video": f}
            data = {"title": title}
            if category:
                data["category"] = category
            resp = self.session.post(f"{API_BASE}/videos", files=files, data=data)
        resp.raise_for_status()
        return resp.json()
