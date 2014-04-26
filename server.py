import web
import json
import os, os.path

# Import all scripts
import scripts

urls = (
    '/richelieu/([^/]*)/([^/]*)/?', 'push',
    '/richelieu/([^/]*)/([^/]*)/(.*)', 'get'
)

app = web.application(urls, globals())

refstr = len("refs/heads/")
render = web.template.render("templates")

class push:
    def GET(self, owner, repo):
        branches = [ f[len(owner+"."+repo+"."):len(f)-5].replace(".","/") for f in os.listdir(owner) if os.path.isfile(owner+"/"+f) and f.startswith(owner+"."+repo) and f.endswith("json") ]
        return render.branchlist(data={"branches":branches,"owner":owner,"repo":repo})
    def POST(self, owner, repo):
        push = json.loads(web.input()["payload"])
        branch = push["ref"][refstr:]
        print "[%s/%s] New commit on %s by %s <%s>" % (owner, repo, branch, push["pusher"]["name"], push["pusher"]["email"])
        # Do we have a script ready?
        if owner+"/"+repo in scripts.bind:
            scripts.bind[owner+"/"+repo](branch, push["head_commit"])

class get:
    def GET(self, owner, repo, branch):
        fname = owner+"."+repo+"."+branch.replace("/",".")
        # Check if logfile exists
        if os.path.isfile(owner+"/"+fname+".json"):
            web.header('Content-Type', 'text/html')
            with open(owner+"/"+fname+".json", "r") as logfile:
                logdata = json.loads(logfile.read())
            with open(owner+"/"+fname+".cppcheck.log","r") as cppcheck:
                cppdata = cppcheck.read()
                logdata["cpp"] = cppdata
            return render.log(data=logdata)
        else:
            return web.notfound()

if __name__ == "__main__":
    web.httpserver.runsimple(app.wsgifunc(), ("127.0.0.1", 4567))
