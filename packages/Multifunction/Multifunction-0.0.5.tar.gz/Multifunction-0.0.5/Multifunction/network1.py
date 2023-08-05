import requests

class c():
    def __init__(self):
        pass
    def get_url(self,url):
        return requests.get(url=url)

    def file_downloads(self,url, path):
        r = requests.get(url, stream=True)
        f = open(path, 'wb')
        for a in r.iter_content(chunk_size=100):  # iterÊÇiter
            f.write(a)