from lolzapi import pylolzapi

client = pylolzapi.api("token")

print(client.get.last_post(2430762))
