import db
import flask
app = flask.Flask(__name__)
app.debug = True

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
    return blog_list(1)

@route("/index.html")
def index():
    articles = db.Session().query(db.Article) \
        .filter(db.Article.type==db.ArticleType.by_key("blog_post")).all()
    return flask.render_template('index.html', articles=articles)

PAGES_LIMIT = 5

@route("/blog_list_<int:page>.html")
def blog_list(page):
    query = db.Session.query(db.Article).filter(db.Article.type==db.ArticleType.by_key("blog_post"))
    articles_count = query.count()
    articles = query.offset(page / PAGES_LIMIT).limit(PAGES_LIMIT).all()
    print "articles:", articles
    return flask.render_template('blog_list.html',
            articles_count=articles_count,
            articles = articles,
        )

