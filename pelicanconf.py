AUTHOR = 'Abulele'
SITENAME = 'Abulele'
SITEDESCRIPTION = ('Sport science student and self-taught Python developer, '
                   'building practical tools and learning in public from Cape Town.')
SITEURL = 'https://abulele-portfolio.onrender.com'
TIMEZONE = 'Africa/Johannesburg'
DEFAULT_LANG = 'en'
THEME = 'theme/abulele'
ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']
DEFAULT_PAGINATION = 5
DIRECT_TEMPLATES = ['index', 'blog', 'projects', 'archives', 'categories', 'tags', 'authors']

# Live GitHub wiring (plugins/github_projects.py)
PLUGIN_PATHS = ['plugins']
PLUGINS = ['github_projects']
GITHUB_USERNAME = 'abulele0929'

# Journal feed
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = None
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_RSS = None
PATH = 'content'
STATIC_PATHS = ['images']