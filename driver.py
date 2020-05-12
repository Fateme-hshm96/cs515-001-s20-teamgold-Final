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

CommitAnalyzer.analyzeComplexity(bugCausing, bugFixing, notBugs)

# CommitAnalyzer.analyzeDayOfBug(bugCausing, bugFixing, notBugs)

# CommitAnalyzer.analyzeChangedMethods(bugCausing, bugFixing, notBugs)


def plot_dict(dict, y_label):
    plt.bar(range(len(dict)), list(dict.values()), align='center')
    plt.xticks(range(len(dict)), list(dict.keys()), rotation=-90)
    plt.xlabel('Project Name')
    plt.ylabel(y_label)
    plt.show()

avg_num_files = {}
avg_lines_added = {}
avg_lines_removed = {}
avg_num_methods_changed = {}
num_author = {}
for key, val in bugFixing.items():
    authors = set()
    times = []
    a = 0
    b = 0
    c = 0
    d = 0
    for commit in val:
        authors.add(commit['author'])
        a += commit['num_files']
        b += commit['lines_added']
        c += commit['lines_removed']
        d += commit['num_methods_changed']

    numCommits = len(val)
    if numCommits != 0:

        # print(str(timedelta(seconds=sum(map(lambda f: int(f[0]) * 3600 + int(f[1]) * 60 + int(f[2]),
        #                                    map(lambda f: f.split(':'), times))) / len(times))))
        avg_num_files[key] = a/numCommits
        avg_lines_added[key] = b/numCommits
        avg_lines_removed[key] = c/numCommits
        avg_num_methods_changed[key] = d/numCommits
        num_author[key] = len(authors)


plot_dict(avg_num_files, 'Average Number of Files Modified for Fix')
plot_dict(avg_lines_added, 'Average Number of Lines Added for Fix')
plot_dict(avg_lines_removed, 'Average Number of Lines Removed for Fix')
plot_dict(avg_num_methods_changed, 'Average Number of Methods Changed for Fix')
plot_dict(num_author, 'Average Number of Authors Involved in Fixing')