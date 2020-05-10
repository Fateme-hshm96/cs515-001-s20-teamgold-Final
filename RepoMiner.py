import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)
from pydriller import RepositoryMining
from pydriller import GitRepository
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.contributors_count import ContributorsCount
import sys
import re
import time
import UrlLoader
import LanguageDetector
import IOUtils


urls = UrlLoader.getRepos("repos_small_2.txt")

projectMap = {}

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

   for commit in RepositoryMining("./repos_to_analyze/"+str(projectName), only_in_branch='master',only_no_merge=True).traverse_commits():
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

      projectMap[projectName] = bugFixes


IOUtils.writeBugMap(projectMap,"./bug_fixing_commits")


endTime = time.time()

print("time", endTime - startTime)