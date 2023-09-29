import requests
import json
from decouple import config
from requests.auth import HTTPBasicAuth


def news_post(wpBaseUrl, title, content, url, postStatus="publish"):
    """
    Create a new WordPress post using the WordPress REST API.

    Args:
        wp_base_url (str): The base URL of your WordPress site.
        title (str): The title of the post.
        content (str): The content of the post.
        url (str): The URL associated with the post.
        post_status (str, optional): The status of the post (default is "publish").

    Returns:
        None

    Prints:
        "Post created successfully" on success.
        "Failed to create post: <error_message>" on failure.
    """
    # The URL for the API endpoint
    wp_url = f"{wpBaseUrl}/wp-json/wp/v2/posts"

    username = config("WP_USERNAME")
    password = config("WP_PASSWORD")

    auth = HTTPBasicAuth(username, password)

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    data = {
        "status": postStatus,
        "title": title,
        "content": content,
        "url": url,
    }
    response = requests.post(wp_url, json=data, auth=auth, headers=headers)
    # Check the response
    if response.status_code == 201:
        print("Post created successfully")
    else:
        print(f"Failed to create post: {response.text}")

