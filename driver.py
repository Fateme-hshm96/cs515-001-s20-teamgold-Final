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
IOUtils.readBugMap(bugFixing, bug_fixing_commits_dir)

# read in buggy commits
IOUtils.readBugMap(bugCausing, bug_causing_commits_dir)

# read in buggy commits
IOUtils.readBugMap(notBugs, not_bugs_dir)


def keywithmaxval(d):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def analyzeAuthors():
    bugFixAuthors = {}
    bugCausingAuthors = {}

    for project, commits in bugFixing.items():
        for commit in commits:
            if commit['author'] in bugFixAuthors:
                bugFixAuthors[commit['author']] = bugFixAuthors[commit['author']] + 1
            else:
                bugFixAuthors[commit['author']] = 1

    for project, commits in bugCausing.items():
        for commit in commits:
            if commit['author'] in bugCausingAuthors:
                bugCausingAuthors[commit['author']] = bugCausingAuthors[commit['author']] + 1
            else:
                bugCausingAuthors[commit['author']] = 1

    print(bugFixAuthors)
    print(bugCausingAuthors)

    print("\n")

    mostFixes = keywithmaxval(bugFixAuthors)
    mostBugs = keywithmaxval(bugCausingAuthors)

    print("most bugs", mostBugs, bugCausingAuthors[mostBugs])
    print("most fixes", mostFixes, bugFixAuthors[mostFixes])

    authors, numBugs = list(bugFixAuthors.keys()), list(bugFixAuthors.values())

    authors = [x for _, x in sorted(zip(numBugs, authors), reversed=True)]
    numBugs = sorted(numBugs)

    print(authors)
    print(numBugs)
    # for author,bugs in bugFixAuthors.items():
    plt.plot(authors, numBugs)
    plt.show

    input("press key to exit")


def plot_dict(dict, y_label):
    plt.bar(range(len(dict)), list(dict.values()), align='center')
    plt.xticks(range(len(dict)), list(dict.keys()), rotation=-90)
    plt.xlabel('Project Name')
    plt.ylabel(y_label)
    plt.show()


bugCausingList = []
bugFixingList = []

for project, commits in bugCausing.items():
    numMethodsModifiedBugCausing = []
    for commit in commits:
        numMethodsModifiedBugCausing.append(commit["num_methods_changed"])
    bugCausingList.append(sum(numMethodsModifiedBugCausing) / len(numMethodsModifiedBugCausing))

for project, commits in bugFixing.items():
    numMethodsModifiedBugFixing = []
    for commit in commits:
        numMethodsModifiedBugFixing.append(commit["num_methods_changed"])
    bugFixingList.append(sum(numMethodsModifiedBugFixing) / len(numMethodsModifiedBugFixing))

print(bugCausingList)
print(bugFixingList)

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



