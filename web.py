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
    return blog_list(0)

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
    pages_count = max(articles_count / PAGES_LIMIT + (1 if articles_count % PAGES_LIMIT > 0 else 0), 1)
    offset = PAGES_LIMIT * page
    articles = query.offset(offset).limit(PAGES_LIMIT).all()
    return flask.render_template('blog_list.html',
            pages_count=pages_count,
            page=page,
            articles=articles,
        )

