#modules
import requests

class get:
    def __init__(self,api):
        self.api = api
    #List of posts in a thread
    def posts(self, thread_id, page_of_post_id="", post_ids="", page="", limit="", order=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?posts/&thread_id={thread_id}&page_of_post_id={page_of_post_id}&post_ids={post_ids}&page={page}&limit={limit}&order={order}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Return last post
    def last_post(self, thread_id):
        result = self.posts(thread_id)['thread']['links']['last_post']
        response = requests.get(result).json()
        return response
    #Get section threads
    def threads(self, forum_id="", thread_ids="", creator_user_id="", sticky="", thread_prefix_id="", thread_tag_id="", page="", limit="", order="", thread_create_date="", thread_update_date=""):
        response = requests.get(url=f"https://lolz.guru/api/index.php?threads/&forum_id={forum_id}&thread_ids={thread_ids}&creator_user_id={creator_user_id}&sticky={sticky}&thread_prefix_id={thread_prefix_id}&thread_tag_id={thread_tag_id}&page={page}&limit={limit}&order={order}&thread_create_date={thread_create_date}&thread_update_date={thread_update_date}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
class post:
    def __init__(self,api):
        self.api = api
    #Create a new post
    def post(self, thread_id, post_body, quote_post_id=""):
        response = requests.post(url=f"https://lolz.guru/api/index.php?posts/&thread_id={thread_id}&post_body={post_body}&quote_post_id={quote_post_id}",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
    #Like post
    def like(self, post_id):
        response = requests.post(url=f"https://lolz.guru/api/index.php?posts/{post_id}/likes",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
class delete:
    def __init__(self,api):
        self.api = api
    #Unlike post
    def like(self, post_id):
        response = requests.delete(url=f"https://lolz.guru/api/index.php?posts/{post_id}/likes",headers={'Authorization': f'Bearer {self.api}','Cookie': 'xf_logged_in=1'}).json()
        return response
#classes
class api:
    def __init__(self, api):
        self.api = api #set api
        self.get = get(self.api)
        self.post = post(self.api)
        self.delete = delete(self.api)

