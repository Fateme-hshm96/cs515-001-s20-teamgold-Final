import git
import UrlLoader

urls = UrlLoader.getRepos('repos.txt')

for url in urls:
   print("cloning ",url)
   try:
      git.Git("./repos_to_analyze").clone(url)
   except:
      print("\trepo already exists... skipping.")