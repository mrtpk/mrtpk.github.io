# mrtpk.github.io
This site is build using Jekyll minima. The theme was modified to suit my needs.

More details on minima theme is at it's [repo](https://github.com/jekyll/minima).

## Environment Setup:

#### We need Ruby development kit and Jekyll for building this site:
+ Install `ruby+dev-kit` from [ruby installer page](https://rubyinstaller.org/downloads/). I installed all the packages.
+ Install the jekyll and bundler gems - `gem install jekyll bundler`

#### If you want to edit this repo:
+ Clone this repo - `git clone https://github.com/mrtpk/mrtpk.github.io.git`
+ cd to `mrtpk.github.io` folder
+ Checkout `builder` branch - `git checkout builder`
+ Update bundle - `bundle update`
+ Install bundle - `bundle install`

#### If you want to create a new website:
+ Create new Jekyll project `jekyll new project_name`
+ cd to `project_name` folder
+ Update bundle - `bundle update`
+ Install bundle - `bundle install`

#### Build website and host it on your local machine:
+ To build the site to `_site` folder - `bundle exec jekyll build`
+ Run website locally at `http://127.0.0.1:4000/` - `bundle exec jekyll serve` 

## Some tips:
+ The `minima` theme will be installed locally on your system at `bundle show minima`. We can copy layouts and include files and edit them to suit our needs.
+ To add `favicon` to jenkyll minima - Add `<link rel="shortcut icon" type="image/png" href="{{ 'path to the favicon' }}">` to `<head>` tag.
+ Since the GitHub Pages [doesn't support](https://pages.github.com/versions/) the Jekyll plugin [`jekyll-paginate-v2`](https://github.com/sverrirs/jekyll-paginate-v2) I'm using, I'm uploading static pages to the `master` branch and then deploying the site.

If you have any feedback or questions, feel free to raise an issue.
