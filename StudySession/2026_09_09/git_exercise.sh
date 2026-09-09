# what is git branch
git branch # branch you're on have *
# Ex. git branch studysession
# creating branch
# create a branch called feature/search
git switch -c feature/search # create a branch and switch to the branch
git branch feature/search # create a branch

# merging branch
git merge feature/study_session # merge changes on feature/study_session to feature/search
# merge conflicts and resolve conflicts
# Open the file with conflicts - inspect lines between >>>>> ,===== and <<<<< 
# Decide what to keep/how to keep

# pull request (PR)
