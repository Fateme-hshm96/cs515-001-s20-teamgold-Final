# import IOUtils
# import RepoMiner
# import os

# projectMap = {}

# repository_list = "./repos_with_fixes_extracted"
# bug_fixing_commits_dir = "./commits_not_bugs"
# path_to_local_repos = "./repos_to_analyze"

# # Delete output folder to re-run buggy commit extraction
# # if not os.path.exists(bug_fixing_commits_dir):
# RepoMiner.extractBuggyCommits(repository_list,path_to_local_repos,bug_fixing_commits_dir)

# # # read in buggy commits
# # IOUtils.readBugMap(projectMap,bug_fixing_commits_dir)

# # # use SZZ algorithm to find the big causing commits
# # if not os.path.exists(bug_causing_commits_dir):
# #    RepoMiner.findBugCausingCommits(projectMap,path_to_local_repos,bug_causing_commits_dir)




# # bug causing commit extraction code
# ####################################################

# import IOUtils
# import RepoMiner
# import os

# projectMap = {}

# repository_list = "./repos_with_fixes_extracted"
# bug_fixing_commits_dir = "./bug_fixing_commits_all"
# bug_causing_commits_dir = "./bug_causing_commits_all"
# path_to_local_repos = "./repos_to_analyze"

# # Delete output folder to re-run buggy commit extraction
# if not os.path.exists(bug_fixing_commits_dir):
#    RepoMiner.extractBuggyCommits(repository_list,path_to_local_repos,bug_fixing_commits_dir)

# # read in buggy commits
# IOUtils.readBugMap(projectMap,bug_fixing_commits_dir)

# # use SZZ algorithm to find the big causing commits
# # if not os.path.exists(bug_causing_commits_dir):
# RepoMiner.findBugCausingCommits(projectMap,path_to_local_repos,bug_causing_commits_dir)




import IOUtils
import RepoMiner
import os
import matplotlib.pyplot as plt

bugFixing = {}
bugCausing = {}
notBugs = {}

repository_list = "./repos_with_fixes_extracted"
bug_fixing_commits_dir = "./bug_fixing_commits_all"
bug_causing_commits_dir = "./bug_causing_commits_all"
not_bugs_dir = "./commits_not_bugs"
path_to_local_repos = "./repos_to_analyze"

# read in buggy commits
IOUtils.readBugMap(bugFixing,bug_fixing_commits_dir)

# read in buggy commits
IOUtils.readBugMap(bugCausing,bug_causing_commits_dir)

# read in buggy commits
IOUtils.readBugMap(notBugs,not_bugs_dir)

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

def analyzeAuthors():
   bugFixAuthors = {}
   bugCausingAuthors = {}

   for project,commits in bugFixing.items():
      for commit in commits:
         if commit['author'] in bugFixAuthors:
            bugFixAuthors[commit['author']] = bugFixAuthors[commit['author']] + 1  
         else: bugFixAuthors[commit['author']] = 1


   for project,commits in bugCausing.items():
      for commit in commits:
         if commit['author'] in bugCausingAuthors:
            bugCausingAuthors[commit['author']] = bugCausingAuthors[commit['author']] + 1  
         else: bugCausingAuthors[commit['author']] = 1

   print(bugFixAuthors)
   print(bugCausingAuthors)

   print("\n")

   mostFixes = keywithmaxval(bugFixAuthors)
   mostBugs = keywithmaxval(bugCausingAuthors)

   print("most bugs",mostBugs,bugCausingAuthors[mostBugs])
   print("most fixes",mostFixes,bugFixAuthors[mostFixes])


   authors,numBugs = list(bugFixAuthors.keys()), list(bugFixAuthors.values())

   authors = [x for _,x in sorted(zip(numBugs,authors),reversed=True)]
   numBugs = sorted(numBugs)


   print(authors)
   print(numBugs)
   # for author,bugs in bugFixAuthors.items():
   plt.plot(authors,numBugs)
   plt.show

   input("press key to exit")


bugCausingList = []
bugFixingList = []

for project,commits in bugCausing.items():
   numMethodsModifiedBugCausing = []
   for commit in commits:
      numMethodsModifiedBugCausing.append(commit["num_methods_changed"])
   bugCausingList.append(sum(numMethodsModifiedBugCausing)/len(numMethodsModifiedBugCausing))
   


for project,commits in bugFixing.items():
   numMethodsModifiedBugFixing = []
   for commit in commits:
      numMethodsModifiedBugFixing.append(commit["num_methods_changed"])
   bugFixingList.append(sum(numMethodsModifiedBugFixing)/len(numMethodsModifiedBugFixing))


print(bugCausingList)
print(bugFixingList)
