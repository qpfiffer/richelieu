from git import *
import json, os, difflib
from subprocess import Popen, PIPE

bind = {}

def Oleg(owner, repo):
    def process(branch, commit):
        # Select git dir
        git = Repo(owner+"/"+repo).git
        # Switch to branch
        print "Switching to branch "+branch
        git.checkout(branch)
        # Pull latest edits
        print "Pulling edits.."
        git.pull()
        # Run ccpcheck
        print "Running ccpcheck.."
        cppres = Popen(["cppcheck","-I",owner+"/"+repo+"/include",owner+"/"+repo+"/src"], stdout=PIPE, stderr=PIPE).stderr.readlines()
        cdata = {"id":commit["id"], "timestamp":commit["timestamp"], "owner":owner, "repo":repo, "branch": branch, "message":commit["message"], "author":commit["author"]}
        filepath = owner+"."+repo+"."+branch.replace("/",".")
        # Load old file (if it exists)
        if os.path.isfile(filepath+".cppcheck.log"):
            with open(owner+"/"+filepath+".cppcheck.diff","r") as difffile:
                oldcpp = difffile.readlines()
                cppdiff = difflib.unified_diff(oldcpp, cppres)
                outcpp = ''.join(cppdiff)
        else:
            outcpp = ''.join(cppres)
        # Run clang static analyzer (scan-build)
        print "Running clang static analyzer.."
        clangres = Popen(["scan-build","--use-analyzer","/usr/bin/clang","-o","/var/www/scans/"+owner+"/"+repo,"gmake","clean","liboleg","oleg_test"], cwd=owner+"/"+repo, stdout=PIPE, stderr=PIPE).stdout.readlines()
        last = clangres[len(clangres)-1]
        if last.find("No bugs") < 0:
            cdata["dir"] = last[last.find("20"):last.find("examine")-5]
        # Write to files
        with open(owner+"/"+filepath+".cppcheck.diff","w") as difffile:
            difffile.write(''.join(cppres))
        with open(owner+"/"+filepath+".cppcheck.log","w") as cppfile:
            cppfile.write(outcpp)
        with open(owner+"/"+filepath+".json", "w") as logfile:
            logfile.write(json.dumps(cdata))
        print "Logfile written!"
        return "All okay!"
    return process

bind["Hamcha/OlegDB"] = Oleg("Hamcha", "OlegDB")
bind["infoforcefeed/OlegDB"] = Oleg("infoforcefeed", "OlegDB")
