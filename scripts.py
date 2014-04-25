from git import *
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
		cppres = Popen(["cppcheck","-I "+owner+"/"+repo+"/include ",owner+"/"+repo+"/src"], stdout=PIPE).stdout.read()
		commitlog = "COMMIT %s - %s\r\n%s (%s <%s>)\r\n\r\n" % commit["id"], commit["timestamp"], commit["message"], commit["author"]["name"], commit["author"]["email"]
		# Write to file
		with open(owner+"."+repo+"."+branch+".log", "w") as logfile:
			logfile.write(commitlog+cppres)
		print "Logfile written!"
		return "All okay!"
	return process

bind["Hamcha/OlegDB"] = Oleg("Hamcha", "OlegDB")
bind["infoforcefeed/OlegDB"] = Oleg("infoforcefeed", "OlegDB")