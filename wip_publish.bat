@REM # Updates the repo with static web pages created from builder
rm -rf build
git clone https://github.com/mrtpk/mrtpk.github.io.git build
bundle exec jekyll build
cd build
rm -rf *
cp -r ../_site/* ./
git add -A
git commit -m "Site updated"
git push origin master