from pydriller import RepositoryMining
from pydriller import GitRepository
import sys
import re
import time
import datetime
import UrlLoader
import LanguageDetector
import IOUtils


def extractBuggyCommits(input_filename,local_repos_directory,output_directory):

   urls = UrlLoader.getRepos(input_filename)

   for url in urls:

      bug_counter = 0
      bugFixes = []

      urlTokens = url.split('/')
      projectName = urlTokens[len(urlTokens)-1]

      print("Analyzing",projectName)

      # 1. iterate over each project
      # 2. find all commits that fixed bugs using syntactic analysis
      # 3. find the commit that caused the bug
      # 4. for the commit that caused the bug, extract how many files were in the change set, the number of lines changed (added or removed), the author, how many commits the file has had to it, the number of contributors that have contributed to the file, contributor experience which returns the percentage of
      #    lines authored by the highest contributor of a file, the hunks count

      # commits count, contributor count and contributor experience are in process metrics

      startTime = time.time()

      for commit in RepositoryMining(local_repos_directory + "/" +str(projectName), only_in_branch='master',only_no_merge=True, since=datetime.datetime(2019,6,1,0,0,0)).traverse_commits():
         commit_msg = commit.msg
         containsBug = 'bug' in commit_msg.casefold()
         containsPatch = 'patch' in commit_msg.casefold()
         containsFix = 'fix' in commit_msg.casefold()
         containsBugIdentifier = bool(re.search('#+\d', commit_msg))
         if (containsBug and (containsFix or containsPatch or containsBugIdentifier)) or (containsFix and containsBugIdentifier):
            
            bug_counter = bug_counter + 1

            # get the list of modified files in the fix
            listFixedFiles = commit.modifications

            numFilesModifiedForFix = 0

            numLinesAddedForFix = 0
            numLinesRemovedForFix = 0
            totalComplexityFixedFiles = 0

            fileComplexityCount = 0
            averageComplexityFixedFiles = -1

            totalLinesOfCodeAllFiles = 0

            changedMethods = 0

            numFilesMoved = 0

            for file in listFixedFiles:

               sourceCodeLanguage = LanguageDetector.detect(file.filename)

               if (sourceCodeLanguage == None or file.nloc == 0): continue

               if (file.nloc): totalLinesOfCodeAllFiles = totalLinesOfCodeAllFiles + file.nloc

               numFilesModifiedForFix = numFilesModifiedForFix + 1

               numLinesAddedForFix = numLinesAddedForFix + file.added
               numLinesRemovedForFix = numLinesRemovedForFix + file.removed
               if file.complexity:
                  fileComplexityCount = fileComplexityCount + 1
                  totalComplexityFixedFiles = totalComplexityFixedFiles + file.complexity

               changedMethods = changedMethods + len(file.changed_methods)

            if (numFilesModifiedForFix == 0): continue

            if (fileComplexityCount != 0): 
               averageComplexityFixedFiles = totalComplexityFixedFiles / fileComplexityCount

            bugFixInfo = {
               "commit_hash": commit.hash,
               "author": commit.author.name,
               "total_complexity": totalComplexityFixedFiles,
               "average_complexity": averageComplexityFixedFiles,
               "sum_nloc": totalLinesOfCodeAllFiles,
               "num_files": numFilesModifiedForFix,
               "lines_added": numLinesAddedForFix,
               "lines_removed": numLinesRemovedForFix,
               "commit_date": commit.author_date,
               "branches": commit.branches,
               "num_methods_changed": changedMethods
            }

            bugFixes.append(bugFixInfo)

         tempMap = {projectName: bugFixes}

         IOUtils.writeBugMap(tempMap,output_directory,"_bug_fixing_commits")

      endTime = time.time()

      print("time", endTime - startTime)



def findBugCausingCommits(projectMap,local_repos_directory,output_directory):

   bugInducingProjectMap = {}

   for project,commits in projectMap.items():

      print("finding bug causing commits for ",str(local_repos_directory) + "/" + project)

      repo_path = str(local_repos_directory) + "/" + project

      repo = GitRepository(repo_path)

      startTime = time.time()

      bugInducingCommits = []

      hashes = [x["commit_hash"] for x in commits]

      # analyze each bug fix for this project
      for bugFix in RepositoryMining(repo_path, only_commits=hashes).traverse_commits():

         # get the commits that last touched the modified lines of the files
         commitsLastTouchedFix = repo.get_commits_last_modified_lines(bugFix)

         bugCausingHashes = set([])

         for filename, fileCommit in commitsLastTouchedFix.items():

            for fileHash in fileCommit:
               bugCausingHashes.add(fileHash)

         hashList = [x for x in bugCausingHashes]

         # get average statistics about each of these commits
         # number of files modified for the commit
         # number of lines added for the commit
         # number of lines removed for the commit
         # number of methods changed for the commit
         # author of the commit
         # the elapsed time for the bug fix
         # branches
         for bugCausingCommit in RepositoryMining(repo_path, only_commits=hashList).traverse_commits():

            numModifiedFiles = len(bugCausingCommit.modifications)
            linesAdded = 0
            linesRemoved = 0
            numMethodsChanged = 0
            sum_nloc = 0
            numFilesWithComplexity = 0
            sumComplexity = 0

            if numModifiedFiles <= 0: continue

            for modification in bugCausingCommit.modifications:
               sourceCodeLanguage = LanguageDetector.detect(modification.filename)
               if (sourceCodeLanguage == None or modification.nloc == 0 or modification.nloc is None): continue
               sum_nloc = sum_nloc + modification.nloc
               linesAdded = linesAdded + modification.added
               linesRemoved = linesRemoved + modification.removed
               numMethodsChanged = numMethodsChanged + len(modification.changed_methods)
               if modification.complexity:
                  numFilesWithComplexity = numFilesWithComplexity + 1
                  sumComplexity = sumComplexity + modification.complexity

            if (numFilesWithComplexity != 0): 
               averageComplexityFixedFiles = sumComplexity / numFilesWithComplexity

            bugInducingInfo = {
                  "commit_hash": bugCausingCommit.hash,
                  "author": bugCausingCommit.author.name,
                  "total_complexity": sumComplexity,
                  "average_complexity": averageComplexityFixedFiles,
                  "sum_nloc": sum_nloc,
                  "num_files": numModifiedFiles,
                  "lines_added": linesAdded,
                  "lines_removed": linesRemoved,
                  "commit_date": bugCausingCommit.author_date,
                  "branches": bugCausingCommit.branches,
                  "num_methods_changed": numMethodsChanged,
                  "time_to_fix": bugFix.author_date - bugCausingCommit.author_date
               }
            
            # print(bugInducingInfo["commit_hash"])
            # print(bugInducingInfo["author"])
            # print(bugInducingInfo["total_complexity"])
            # print(bugInducingInfo["average_complexity"])
            # print(bugInducingInfo["sum_nloc"])
            # print(bugInducingInfo["num_files"])
            # print(bugInducingInfo["lines_added"])
            # print(bugInducingInfo["lines_removed"])
            # print(bugInducingInfo["commit_date"])
            # print(bugInducingInfo["branches"])
            # print(bugInducingInfo["num_methods_changed"])
            # print(bugInducingInfo["time_to_fix"])

            bugInducingCommits.append(bugInducingInfo)

      tempMap = {project: bugInducingCommits}

      IOUtils.writeBugMap(tempMap,output_directory,"_bug_causing_commits")

      endTime = time.time()

      print("time", endTime - startTime)