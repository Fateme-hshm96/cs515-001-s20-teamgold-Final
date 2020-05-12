import re

def getReposWebAddresses(filename):
   repos = []

   f = open(filename,"r")

   for line in f:
      if re.search('https:', line):
         repos.append(line.strip())

   return repos

def getReposPlainName(filename):
   repos = []

   f = open(filename,"r")

   for line in f:
      repos.append(line.strip())

   return repos