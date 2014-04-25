import web
import json

# Import all scripts
import scripts

urls = (
    '/richelieu/([^/]*)/([^/]*)', 'push'
)

app = web.application(urls, globals())

refstr = len("refs/heads/")

class push:
    def POST(self, owner, repo):
        push = json.loads(web.input()["payload"])
        branch = push["ref"][refstr:]
        print "[%s/%s] New commit on %s by %s <%s>" % (owner, repo, branch, push["pusher"]["name"], push["pusher"]["email"])
        # Do we have a script ready?
        if owner+"/"+repo in scripts.bind:
            scripts.bind[owner+"/"+repo](branch)

if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("0.0.0.0", 4567))
