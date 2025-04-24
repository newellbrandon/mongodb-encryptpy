git config --global init.defaultBranch main
git init
git add -A
git branch -M main
git remote add origin git@github.com:newellbrandon/mongodb-encryptpy.git
git pull origin main
git add -A
git commit -am "initial commit"
git push --set-upstream origin main
