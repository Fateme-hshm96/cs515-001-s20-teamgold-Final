import IOUtils
import RepoMiner
import CommitAnalyzer
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

CommitAnalyzer.analyzeLinesAdded(bugCausing, bugFixing, notBugs)

CommitAnalyzer.analyzeLinesRemoved(bugCausing, bugFixing, notBugs)

CommitAnalyzer.analyzeNumFiles(bugCausing, bugFixing, notBugs)

CommitAnalyzer.analyzeComplexity(bugCausing, bugFixing, notBugs)

CommitAnalyzer.analyzeDayOfBug(bugCausing, bugFixing, notBugs)

CommitAnalyzer.analyzeChangedMethods(bugCausing, bugFixing, notBugs)