# Workflow for the CI-CD model for github and Travis

- we no more commit in master
- clone master repo, this will have the cict 
- you commit in the cloned repo in github
- Travis will run the cict
- once successful, a pull request need to be send to master branch. (Need to figure the pull request part).
- master will run Travis when a new commit is pulled in.
