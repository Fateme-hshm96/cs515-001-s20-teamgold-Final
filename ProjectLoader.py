import re

def getRepos(filename):
   repos = []

   f = open(filename,"r")

   for line in f:
      if re.search('https:', line):
         repos.append(line.strip())

   return repos