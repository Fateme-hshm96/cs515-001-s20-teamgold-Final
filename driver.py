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
allMaps = [bugFixing,bugCausing,notBugs]

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



# commit 9b94fb3965c6869b0ac47420958a4bbae0b2d54c in guava 22771 modified methods