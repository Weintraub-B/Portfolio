import json
from pathlib import Path

def test_url_list_loadable():
    url_path = Path("url_list.json")
    assert url_path.exists(), "url_list.json does not exist"
    with url_path.open("r") as f:
        data = json.load(f)
    assert isinstance(data, list), "url_list.json must contain a list"
    assert all("url" in item for item in data), "Each item should have a 'url' key"