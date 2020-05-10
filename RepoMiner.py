from pydriller import RepositoryMining
from pydriller import GitRepository
from pydriller.metrics.process.contributors_experience import ContributorsExperience
from pydriller.metrics.process.contributors_count import ContributorsCount
import re
import time
import UrlLoader

urls = UrlLoader.getRepos("repos_small_2.txt")

projectMap = {}

for url in urls:

   bug_counter = 0
   bugs = []

   urlTokens = url.split('/')
   print(url)
   projectName = urlTokens[len(urlTokens)-1]
   # print(urlTokens[len(urlTokens)-1])

   # 1. iterate over each project
   # 2. find all commits that fixed bugs using syntactic analysis
   # 3. find the commit that caused the bug
   # 4. for the commit that caused the bug, extract how many files were in the change set, the number of lines changed (added or removed), the author, how many commits the file has had to it, the number of contributors that have contributed to the file, contributor experience which returns the percentage of
   #    lines authored by the highest contributor of a file, the hunks count

   startTime = time.time()

   gr = GitRepository(url)

   gr.repo

   for commit in RepositoryMining(url, only_in_branch='master',only_no_merge=True,clone_repo_to='./').traverse_commits():
      commit_msg = commit.msg
      if ('bug' in commit_msg.casefold() and ('fix' in commit_msg.casefold() or 'patch' in commit_msg.casefold() or bool(re.search('#+\d', commit_msg)))) or ('fix' in commit_msg.casefold() and bool(re.search('#+\d', commit_msg))):
         
         # print(commit_msg)
         # bug_counter = bug_counter + 1
         bugFixer = commit.author.name
         
         # get the list of modified files in the fix
         listFixedFiles = commit.modifications

         numFilesModifiedForFix = len(listFixedFiles)

         numLinesAddedForFix = 0
         numLinesRemovedForFix = 0

         for file in listFixedFiles:

            numLinesAddedForFix = numLinesAddedForFix + file.added
            numLinesRemovedForFix = numLinesRemovedForFix + file.removed




   print("number of bugs is " + str(bug_counter))


endTime = time.time()

print(endTime - startTime)