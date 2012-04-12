import db
import flask
import os
import os.path
app = flask.Flask(__name__)
app.debug = True

GEN_FOLDER = "dist"

static_pages_fcts = []

def route(*args, **kwargs):
    def wrapper(fct):
        tmp = dict(kwargs)
        tmp.setdefault("endpoint", fct.__name__)
        tmp["view_func"] = db.transactionnal(fct)
        app.add_url_rule(*args, **tmp)
        return tmp["view_func"]
    return wrapper

@route("/")
def root():
    return blog_list(0)

@route("/index.html")
def index():
    articles = db.Session().query(db.Article) \
        .filter(db.Article.type==db.ArticleType.by_key("blog_post")).all()
    return flask.render_template('index.html', articles=articles)

static_pages_fcts.append(lambda: "/index.html")

PAGES_LIMIT = 5

@route("/blog_list_<int:page>.html")
def blog_list(page):
    query = db.Session.query(db.Article).filter(db.Article.type==db.ArticleType.by_key("blog_post"))
    articles_count = query.count()
    pages_count = max(articles_count / PAGES_LIMIT + (1 if articles_count % PAGES_LIMIT > 0 else 0), 1)
    offset = PAGES_LIMIT * page
    articles = query.offset(offset).limit(PAGES_LIMIT).all()
    return flask.render_template('blog_list.html',
            pages_count=pages_count,
            page=page,
            articles=articles,
        )

def gen_blog_list_urls():
    count = db.Session.query(db.Article).filter(db.Article.type==db.ArticleType.by_key("blog_post")).count()
    pages_count = max(articles_count / PAGES_LIMIT + (1 if articles_count % PAGES_LIMIT > 0 else 0), 1)
    return ["/blog_list_%i.html" % i for i in range(pages_count)] 
static_pages_fcts.append(gen_blog_list_urls)

def gen_static_files_urls():
    files = []
    def find_files(folder, url):
        for f in os.listdir(folder):
            if os.path.isdir(os.path.join(folder, f)):
                find_files(os.path.join(folder, f), os.path.join(url, f))
            else:
                files.append(os.path.join(url, f))
    find_files(app.static_folder, "/static")
    return files

print gen_static_files_urls()

