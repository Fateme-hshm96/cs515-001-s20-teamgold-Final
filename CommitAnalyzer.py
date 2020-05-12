import matplotlib.pyplot as plt
import statistics
import datetime

def plot(title, xLabel, yLabel, xVals, yVals, filename):
   plt.xticks(rotation=90)
   plt.title(title)
   plt.ylabel(yLabel)
   plt.xlabel(xLabel)
   fig = plt.gcf()
   fig.set_size_inches(18.5, 11.5)
   font = { 'weight': 'normal',
         'size'   : 20}
   plt.rc('font', **font)
   plt.plot(xVals,yVals)
   plt.savefig(filename, bbox_inches='tight')
   
   plt.clf()

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


def analyzeLinesRemoved(bugCausing, bugFixing, notBugs):

   bugCausingList = []
   bugCausingProjects = []
   bugFixingList = []
   bugFixingProjects = []
   notBugsList = []
   notBugsProjects = []

   # remove duplicated commits
   for project,commits in bugCausing.items():
      uniqueCommits = []
      for commit in commits:
         tempHash = commit['commit_hash']
         if (tempHash in [x['commit_hash'] for x in uniqueCommits]): continue
         else: uniqueCommits.append(commit)
      bugCausing[project] = uniqueCommits


   for project,commits in bugCausing.items():
      numLinesRemovedBugCausing = []
      for commit in commits:
         numLinesRemovedBugCausing.append(commit["lines_removed"])
      if len(numLinesRemovedBugCausing) != 0: 
         bugCausingList.append(sum(numLinesRemovedBugCausing)/len(numLinesRemovedBugCausing))
         bugCausingProjects.append(project)


   for project,commits in bugFixing.items():
      numLinesRemovedBugFixing = []
      for commit in commits:
         numLinesRemovedBugFixing.append(commit["lines_removed"])
      if len(numLinesRemovedBugFixing) != 0: 
         bugFixingProjects.append(project)
         bugFixingList.append(sum(numLinesRemovedBugFixing)/len(numLinesRemovedBugFixing))

   for project,commits in notBugs.items():
      numLinesRemovedNotBugs = []
      for commit in commits:
         numLinesRemovedNotBugs.append(commit["lines_removed"])
      if len(numLinesRemovedNotBugs) != 0: 
         notBugsProjects.append(project)
         notBugsList.append(sum(numLinesRemovedNotBugs)/len(numLinesRemovedNotBugs))


   bugCausingProjectsSorted = [x for _,x in sorted(zip(bugCausingList,bugCausingProjects),reverse=True)]
   bugCausingSorted = sorted(bugCausingList,reverse=True)

   bugFixingProjectsSorted = [x for _,x in sorted(zip(bugFixingList,bugFixingProjects),reverse=True)]
   bugFixingSorted = sorted(bugFixingList,reverse=True)

   notBugsProjectsSorted = [x for _,x in sorted(zip(notBugsList,notBugsProjects),reverse=True)]
   notBugsSorted = sorted(notBugsList,reverse=True)

   bugFixingListSorted = sorted(bugFixingList,reverse=True)
   bugCausingListSorted = sorted(bugCausingList,reverse=True)
   notBugsListSorted = sorted(notBugsList,reverse=True)

   bugFixAverage = sum(bugFixingList)/len(bugFixingList)
   bugCausingAverage = sum(bugCausingList)/len(bugCausingList)
   notBugsAverage = sum(notBugsList)/len(notBugsList)

   print("bug fix average number of lines removed",bugFixAverage)
   print("bug causing average number of lines removed",bugCausingAverage)
   print("not bugs average number of lines removed",notBugsAverage)

   plt.hlines(bugFixAverage, 0, len(bugFixingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugFixAverage+1,'average = ' + str(bugFixAverage))
   plot("Average number of lines removed per project - bug fixes","github project", "Average number of lines removed per commit",bugFixingProjectsSorted,bugFixingListSorted,"lines-removed-bug-fixing.png")

   plt.hlines(bugCausingAverage, 0, len(bugCausingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugCausingAverage+1,'average = ' + str(bugCausingAverage))
   plot("Average number of lines removed per project - bug causers","github project", "Average number of lines removed per commit",bugCausingProjectsSorted,bugCausingListSorted,"lines-removed-bug-causing.png")

   plt.hlines(notBugsAverage, 0, len(notBugsListSorted), colors='k', linestyles='solid')
   plt.text(1,notBugsAverage+4,'average = ' + str(notBugsAverage))
   plot("Average number of lines removed per project - not bugs","github project", "Average number of lines removed per commit",notBugsProjectsSorted,notBugsListSorted,"lines-removed-not-bugs.png")


def analyzeLinesAdded(bugCausing, bugFixing, notBugs):

   bugCausingList = []
   bugCausingProjects = []
   bugFixingList = []
   bugFixingProjects = []
   notBugsList = []
   notBugsProjects = []

   # remove duplicated commits
   for project,commits in bugCausing.items():
      uniqueCommits = []
      for commit in commits:
         tempHash = commit['commit_hash']
         if (tempHash in [x['commit_hash'] for x in uniqueCommits]): continue
         else: uniqueCommits.append(commit)
      bugCausing[project] = uniqueCommits


   for project,commits in bugCausing.items():
      numLinesAddedBugCausing = []
      for commit in commits:
         numLinesAddedBugCausing.append(commit["lines_added"])
      if len(numLinesAddedBugCausing) != 0: 
         bugCausingList.append(sum(numLinesAddedBugCausing)/len(numLinesAddedBugCausing))
         bugCausingProjects.append(project)


   for project,commits in bugFixing.items():
      numLinesAddedBugFixing = []
      for commit in commits:
         numLinesAddedBugFixing.append(commit["lines_added"])
      if len(numLinesAddedBugFixing) != 0: 
         bugFixingProjects.append(project)
         bugFixingList.append(sum(numLinesAddedBugFixing)/len(numLinesAddedBugFixing))

   for project,commits in notBugs.items():
      numLinesAddedNotBugs = []
      for commit in commits:
         numLinesAddedNotBugs.append(commit["lines_added"])
      if len(numLinesAddedNotBugs) != 0: 
         notBugsProjects.append(project)
         notBugsList.append(sum(numLinesAddedNotBugs)/len(numLinesAddedNotBugs))


   bugCausingProjectsSorted = [x for _,x in sorted(zip(bugCausingList,bugCausingProjects),reverse=True)]
   bugCausingSorted = sorted(bugCausingList,reverse=True)

   bugFixingProjectsSorted = [x for _,x in sorted(zip(bugFixingList,bugFixingProjects),reverse=True)]
   bugFixingSorted = sorted(bugFixingList,reverse=True)

   notBugsProjectsSorted = [x for _,x in sorted(zip(notBugsList,notBugsProjects),reverse=True)]
   notBugsSorted = sorted(notBugsList,reverse=True)

   bugFixingListSorted = sorted(bugFixingList,reverse=True)
   bugCausingListSorted = sorted(bugCausingList,reverse=True)
   notBugsListSorted = sorted(notBugsList,reverse=True)

   bugFixAverage = sum(bugFixingList)/len(bugFixingList)
   bugCausingAverage = sum(bugCausingList)/len(bugCausingList)
   notBugsAverage = sum(notBugsList)/len(notBugsList)

   print("bug fix average number of lines added",bugFixAverage)
   print("bug causing average number of lines added",bugCausingAverage)
   print("not bugs average number of lines added",notBugsAverage)

   plt.hlines(bugFixAverage, 0, len(bugFixingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugFixAverage+1,'average = ' + str(bugFixAverage))
   plot("Average number of lines added per project - bug fixes","github project", "Average number of lines added per commit",bugFixingProjectsSorted,bugFixingListSorted,"lines-added-bug-fixing.png")

   plt.hlines(bugCausingAverage, 0, len(bugCausingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugCausingAverage+1,'average = ' + str(bugCausingAverage))
   plot("Average number of lines added per project - bug causers","github project", "Average number of lines added per commit",bugCausingProjectsSorted,bugCausingListSorted,"lines-added-bug-causing.png")

   plt.hlines(notBugsAverage, 0, len(notBugsListSorted), colors='k', linestyles='solid')
   plt.text(1,notBugsAverage+4,'average = ' + str(notBugsAverage))
   plot("Average number of lines added per project - not bugs","github project", "Average number of lines added per commit",notBugsProjectsSorted,notBugsListSorted,"lines-added-not-bugs.png")


def analyzeNumFiles(bugCausing, bugFixing, notBugs):

   bugCausingList = []
   bugCausingProjects = []
   bugFixingList = []
   bugFixingProjects = []
   notBugsList = []
   notBugsProjects = []

   # remove duplicated commits
   for project,commits in bugCausing.items():
      uniqueCommits = []
      for commit in commits:
         tempHash = commit['commit_hash']
         if (tempHash in [x['commit_hash'] for x in uniqueCommits]): continue
         else: uniqueCommits.append(commit)
      bugCausing[project] = uniqueCommits


   for project,commits in bugCausing.items():
      numFilesModifiedBugCausing = []
      for commit in commits:
         numFilesModifiedBugCausing.append(commit["num_files"])
      if len(numFilesModifiedBugCausing) != 0: 
         bugCausingList.append(sum(numFilesModifiedBugCausing)/len(numFilesModifiedBugCausing))
         bugCausingProjects.append(project)


   for project,commits in bugFixing.items():
      numFilesModifiedBugFixing = []
      for commit in commits:
         numFilesModifiedBugFixing.append(commit["num_files"])
      if len(numFilesModifiedBugFixing) != 0: 
         bugFixingProjects.append(project)
         bugFixingList.append(sum(numFilesModifiedBugFixing)/len(numFilesModifiedBugFixing))

   for project,commits in notBugs.items():
      numFilesModifiedNotBugs = []
      for commit in commits:
         numFilesModifiedNotBugs.append(commit["num_files"])
      if len(numFilesModifiedNotBugs) != 0: 
         notBugsProjects.append(project)
         notBugsList.append(sum(numFilesModifiedNotBugs)/len(numFilesModifiedNotBugs))


   bugCausingProjectsSorted = [x for _,x in sorted(zip(bugCausingList,bugCausingProjects),reverse=True)]
   bugCausingSorted = sorted(bugCausingList,reverse=True)

   bugFixingProjectsSorted = [x for _,x in sorted(zip(bugFixingList,bugFixingProjects),reverse=True)]
   bugFixingSorted = sorted(bugFixingList,reverse=True)

   notBugsProjectsSorted = [x for _,x in sorted(zip(notBugsList,notBugsProjects),reverse=True)]
   notBugsSorted = sorted(notBugsList,reverse=True)

   bugFixingListSorted = sorted(bugFixingList,reverse=True)
   bugCausingListSorted = sorted(bugCausingList,reverse=True)
   notBugsListSorted = sorted(notBugsList,reverse=True)

   bugFixAverage = sum(bugFixingList)/len(bugFixingList)
   bugCausingAverage = sum(bugCausingList)/len(bugCausingList)
   notBugsAverage = sum(notBugsList)/len(notBugsList)

   print("bug fix average number of files modified",bugFixAverage)
   print("bug causing average number of files modified",bugCausingAverage)
   print("not bugs average number of files modified",notBugsAverage)

   plt.hlines(bugFixAverage, 0, len(bugFixingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugFixAverage+1,'average = ' + str(bugFixAverage))
   plot("Average number of files changed per project - bug fixes","github project", "Average number of files changed per commit",bugFixingProjectsSorted,bugFixingListSorted,"files-changed-bug-fixing.png")

   plt.hlines(bugCausingAverage, 0, len(bugCausingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugCausingAverage+1,'average = ' + str(bugCausingAverage))
   plot("Average number of files changed per project - bug causers","github project", "Average number of files changed per commit",bugCausingProjectsSorted,bugCausingListSorted,"files-changed-bug-causing.png")

   plt.hlines(notBugsAverage, 0, len(notBugsListSorted), colors='k', linestyles='solid')
   plt.text(1,notBugsAverage+4,'average = ' + str(notBugsAverage))
   plot("Average number of files changed per project - not bugs","github project", "Average number of files changed per commit",notBugsProjectsSorted,notBugsListSorted,"files-changed-not-bugs.png")


def analyzeComplexity(bugCausing, bugFixing, notBugs):

   bugCausingList = []
   bugCausingProjects = []
   bugFixingList = []
   bugFixingProjects = []
   notBugsList = []
   notBugsProjects = []

   bugCausingCommitHashes = []

   # remove duplicated commits
   for project,commits in bugCausing.items():
      uniqueCommits = []
      for commit in commits:
         bugCausingCommitHashes.append(commit['commit_hash'])
         tempHash = commit['commit_hash']
         if (tempHash in [x['commit_hash'] for x in uniqueCommits]): continue
         else: uniqueCommits.append(commit)
      bugCausing[project] = uniqueCommits

   for project,commits in bugCausing.items():
      complexityBugCausing = []
      for commit in commits:
         complexityBugCausing.append(commit["average_complexity"])
      if len(complexityBugCausing) != 0: 
         bugCausingList.append(sum(complexityBugCausing)/len(complexityBugCausing))
         bugCausingProjects.append(project)

   for project,commits in bugFixing.items():
      complexityBugFixing = []
      for commit in commits:
         complexityBugFixing.append(commit["average_complexity"])
      if len(complexityBugFixing) != 0: 
         bugFixingList.append(sum(complexityBugFixing)/len(complexityBugFixing))
         bugFixingProjects.append(project)

   for project,commits in notBugs.items():
      numMethodsModifiedNotBugs = []
      for commit in commits:
         if (commit["commit_hash"] in bugCausingCommitHashes): continue
         numMethodsModifiedNotBugs.append(commit["num_methods_changed"])
      if len(numMethodsModifiedNotBugs) != 0: 
         notBugsProjects.append(project)
         notBugsList.append(sum(numMethodsModifiedNotBugs)/len(numMethodsModifiedNotBugs))


   bugCausingProjectsSorted = [x for _,x in sorted(zip(bugCausingList,bugCausingProjects),reverse=True)]
   bugCausingSorted = sorted(bugCausingList,reverse=True)

   bugFixingProjectsSorted = [x for _,x in sorted(zip(bugFixingList,bugFixingProjects),reverse=True)]
   bugFixingSorted = sorted(bugFixingList,reverse=True)

   notBugsProjectsSorted = [x for _,x in sorted(zip(notBugsList,notBugsProjects),reverse=True)]
   notBugsSorted = sorted(notBugsList,reverse=True)

   bugFixingListSorted = sorted(bugFixingList,reverse=True)
   bugCausingListSorted = sorted(bugCausingList,reverse=True)
   notBugsListSorted = sorted(notBugsList,reverse=True)

   bugFixAverage = sum(bugFixingList)/len(bugFixingList)
   bugCausingAverage = sum(bugCausingList)/len(bugCausingList)
   notBugsAverage = sum(notBugsList)/len(notBugsList)

   print("bug fix average complexity",bugFixAverage)
   print("bug causing average complexity",bugCausingAverage)
   print("not bugs average complexity",notBugsAverage)

   plt.hlines(bugFixAverage, 0, len(bugFixingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugFixAverage+1,'average = ' + str(bugFixAverage))
   plot("Average cyclomatic complexity of files in the commit - bug fixes","github project", "Average cyclomatic complexity of files",bugFixingProjectsSorted,bugFixingListSorted,"complexity-bug-fixing.png")

   plt.hlines(bugCausingAverage, 0, len(bugCausingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugCausingAverage+1,'average = ' + str(bugCausingAverage))
   plot("Average cyclomatic complexity of files in the commit - bug causers","github project", "Average cyclomatic complexity of files",bugCausingProjectsSorted,bugCausingListSorted,"complexity-bug-causing.png")

   plt.hlines(notBugsAverage, 0, len(notBugsListSorted), colors='k', linestyles='solid')
   plt.text(1,notBugsAverage+4,'average = ' + str(notBugsAverage))
   plot("Average cyclomatic complexity of files in the commit - not bugs","github project", "Average cyclomatic complexity of files",notBugsProjectsSorted,notBugsListSorted,"complexity-not-bugs.png")
         


def analyzeDayOfBug(bugCausing, bugFixing, notBugs):

   bugCausingList = []
   bugCausingProjects = []
   bugFixingList = []
   bugFixingProjects = []
   notBugsList = []
   notBugsProjects = []

   bugCausingCommitHashes = []

   # remove duplicated commits
   for project,commits in bugCausing.items():
      uniqueCommits = []
      for commit in commits:
         bugCausingCommitHashes.append(commit['commit_hash'])
         tempHash = commit['commit_hash']
         if (tempHash in [x['commit_hash'] for x in uniqueCommits]): continue
         else: uniqueCommits.append(commit)
      bugCausing[project] = uniqueCommits


   for project,commits in bugCausing.items():
      for commit in commits:
         bugCausingList.append(commit["commit_date"].weekday())
         bugCausingProjects.append(project)

   for project,commits in bugFixing.items():
      for commit in commits:
         bugFixingList.append(commit["commit_date"].weekday())
         bugFixingProjects.append(project)

   for project,commits in notBugs.items():
      for commit in commits:
         if (commit["commit_hash"] in bugCausingCommitHashes): continue
         notBugsList.append(commit["commit_date"].weekday())
         notBugsProjects.append(project)

   daysLists = [bugFixingList, bugCausingList, notBugsList]
   filenames = ["bug-fixing-days.png","bug-causing-days.png","not-bugs-days.png"]
   titles = ["Bug fixes per day","Bug causes per day","Regular commits per day"]
   labels = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

   for idx,daysList in enumerate(daysLists):

      monday = [x for x in daysList if x == 0]
      tuesday = [x for x in daysList if x == 1]
      wednesday = [x for x in daysList if x == 2]
      thursday = [x for x in daysList if x == 3]
      friday = [x for x in daysList if x == 4]
      saturday = [x for x in daysList if x == 5]
      sunday = [x for x in daysList if x == 6]

      bugCausingDaysFrequency = [len(monday),len(tuesday),len(wednesday),len(thursday),len(friday),len(saturday),len(sunday)]

      plot(titles[idx],"days","frequency",labels,bugCausingDaysFrequency,filenames[idx])

   monday = bugFixingList.count(0)/bugCausingList.count(0)
   tuesday = bugFixingList.count(1)/bugCausingList.count(1)
   wednesday = bugFixingList.count(2)/bugCausingList.count(2)
   thursday = bugFixingList.count(3)/bugCausingList.count(3)
   friday = bugFixingList.count(4)/bugCausingList.count(4)
   saturday = bugFixingList.count(5)/bugCausingList.count(5)
   sunday = bugFixingList.count(6)/bugCausingList.count(6)

   bugCausingDaysRatio = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]

   plot("Ratio bug fixes : bug causers per day","days","ratio",labels,bugCausingDaysRatio,"bug-days-ratio.png")

   monday = bugCausingList.count(0)/bugFixingList.count(0)
   tuesday = bugCausingList.count(1)/bugFixingList.count(1)
   wednesday = bugCausingList.count(2)/bugFixingList.count(2)
   thursday = bugCausingList.count(3)/bugFixingList.count(3)
   friday = bugCausingList.count(4)/bugFixingList.count(4)
   saturday = bugCausingList.count(5)/bugFixingList.count(5)
   sunday = bugCausingList.count(6)/bugFixingList.count(6)

   bugCausingDaysRatio = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]

   plot("Ratio bug causers : bug fixes per day","days","ratio",labels,bugCausingDaysRatio,"bug-days-ratio-2.png")

     

def analyzeChangedMethods(bugCausing, bugFixing, notBugs):

   bugCausingList = []
   bugCausingProjects = []
   bugFixingList = []
   bugFixingProjects = []
   notBugsList = []
   notBugsProjects = []

   # remove duplicated commits
   for project,commits in bugCausing.items():
      uniqueCommits = []
      for commit in commits:
         tempHash = commit['commit_hash']
         if (tempHash in [x['commit_hash'] for x in uniqueCommits]): continue
         else: uniqueCommits.append(commit)
      bugCausing[project] = uniqueCommits


   for project,commits in bugCausing.items():
      numMethodsModifiedBugCausing = []
      for commit in commits:
         numMethodsModifiedBugCausing.append(commit["num_methods_changed"])
      if len(numMethodsModifiedBugCausing) != 0: 
         bugCausingList.append(sum(numMethodsModifiedBugCausing)/len(numMethodsModifiedBugCausing))
         bugCausingProjects.append(project)


   for project,commits in bugFixing.items():
      numMethodsModifiedBugFixing = []
      for commit in commits:
         numMethodsModifiedBugFixing.append(commit["num_methods_changed"])
      if len(numMethodsModifiedBugFixing) != 0: 
         bugFixingProjects.append(project)
         bugFixingList.append(sum(numMethodsModifiedBugFixing)/len(numMethodsModifiedBugFixing))

   for project,commits in notBugs.items():
      numMethodsModifiedNotBugs = []
      for commit in commits:
         numMethodsModifiedNotBugs.append(commit["num_methods_changed"])
      if len(numMethodsModifiedNotBugs) != 0: 
         notBugsProjects.append(project)
         notBugsList.append(sum(numMethodsModifiedNotBugs)/len(numMethodsModifiedNotBugs))


   bugCausingProjectsSorted = [x for _,x in sorted(zip(bugCausingList,bugCausingProjects),reverse=True)]
   bugCausingSorted = sorted(bugCausingList,reverse=True)

   bugFixingProjectsSorted = [x for _,x in sorted(zip(bugFixingList,bugFixingProjects),reverse=True)]
   bugFixingSorted = sorted(bugFixingList,reverse=True)

   notBugsProjectsSorted = [x for _,x in sorted(zip(notBugsList,notBugsProjects),reverse=True)]
   notBugsSorted = sorted(notBugsList,reverse=True)

   bugFixingListSorted = sorted(bugFixingList,reverse=True)
   bugCausingListSorted = sorted(bugCausingList,reverse=True)
   notBugsListSorted = sorted(notBugsList,reverse=True)

   bugFixAverage = sum(bugFixingList)/len(bugFixingList)
   bugCausingAverage = sum(bugCausingList)/len(bugCausingList)
   notBugsAverage = sum(notBugsList)/len(notBugsList)

   print("bug fix average number of methods modified",bugFixAverage)
   print("bug causing average number of methods modified",bugCausingAverage)
   print("not bugs average number of methods modified",notBugsAverage)

   plt.hlines(bugFixAverage, 0, len(bugFixingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugFixAverage+1,'average = ' + str(bugFixAverage))
   plot("Average number of methods changed per project - bug fixes","github project", "Average number of methods changed per commit",bugFixingProjectsSorted,bugFixingListSorted,"methods-changed-bug-fixing.png")

   plt.hlines(bugCausingAverage, 0, len(bugCausingListSorted), colors='k', linestyles='solid')
   plt.text(1,bugCausingAverage+1,'average = ' + str(bugCausingAverage))
   plot("Average number of methods changed per project - bug causers","github project", "Average number of methods changed per commit",bugCausingProjectsSorted,bugCausingListSorted,"methods-changed-bug-causing.png")

   plt.hlines(notBugsAverage, 0, len(notBugsListSorted), colors='k', linestyles='solid')
   plt.text(1,notBugsAverage+4,'average = ' + str(notBugsAverage))
   plot("Average number of methods changed per project - not bugs","github project", "Average number of methods changed per commit",notBugsProjectsSorted,notBugsListSorted,"methods-changed-not-bugs.png")