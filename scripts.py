from git import *
from subprocess import Popen, PIPE

bind = {}

def Oleg(owner, repo):
	def process(branch):
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
		print cppres

	return process

bind["Hamcha/OlegDB"] = Oleg("Hamcha", "OlegDB")
bind["infoforcefeed/OlegDB"] = Oleg("infoforcefeed", "OlegDB")