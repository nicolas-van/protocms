import web
import flask
import db

@web.route("/")
def root():
    return flask.redirect(flask.url_for("index"))

@web.route("/index.html")
def index():
    return blog_list(0)

web.static_pages_fcts.append(lambda: ["/index.html"])

PAGES_LIMIT = 5

@web.route("/blog_list_<int:page>.html")
def blog_list(page):
    query = db.session.query(db.Article).filter(db.Article.type==db.ArticleType.by_key("blog_post"))
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
    articles_count = db.session.query(db.Article).filter(db.Article.type==db.ArticleType.by_key("blog_post")).count()
    pages_count = max(articles_count / PAGES_LIMIT + (1 if articles_count % PAGES_LIMIT > 0 else 0), 1)
    return ["/blog_list_%i.html" % i for i in range(pages_count)] 
web.static_pages_fcts.append(gen_blog_list_urls)

