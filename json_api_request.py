import requests
import json
import argparse

def fetch_posts(limit):
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()[:limit]

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and save JSON posts from public API.")
    parser.add_argument("--limit", type=int, default=5, help="Number of posts to fetch")
    parser.add_argument("--output", default="posts.json", help="Output JSON filename")

    args = parser.parse_args()

    try:
        posts = fetch_posts(args.limit)
        save_to_json(posts, args.output)
        print(f"Saved {len(posts)} post(s) to {args.output}")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
