
(function() {
admin = {};
admin.templateEngine = new TemplateEngine();
admin.loaded = admin.templateEngine.loadFile("templates.html").pipe(function() {

admin.Widget = nova.Widget.extend({
    template: function() {
        return "<div></div>";
    },
    renderElement: function() {
        var html = this.template({widget: this});
        var $elem = $(html);
        $elem.replaceAll(this.$element);
        this.$element = $elem;
    },
});

admin.jsonRpc = function(url, fct_name, params, settings) {
    var data = {
        jsonrpc: "2.0",
        method: fct_name,
        params: params,
        id: Math.floor(Math.random()* (1000*1000*1000)),
    };
    return $.ajax(url, _.extend({}, settings, {
        url: url,
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
    })).pipe(function(result) {
        if (result.error !== undefined) {
            return $.Deferred().reject("server", result.error);
        }
        else
            return result.result;
    }, function() {
        var def = $.Deferred();
        return def.reject.apply(def, ["communication"].concat(_.toArray(arguments)));
    });
};

admin.Session = nova.Class.extend({
    call: function(fct_name, args, kwargs) {
        return admin.jsonRpc("../adminapi", fct_name, {args: args || [], kwargs: kwargs || {}});
    },
});

admin.session = admin.Session();

admin.Admin = admin.Widget.extend({
    template: admin.templateEngine.admin,
    start: function() {
        this.menu = new admin.Menu(this);
        this.menu.$displayTo = $(".content", this.$element);
        this.menu.appendTo($(".navigation", this.$element));
    },
});

admin.menuElements = [];

admin.Menu = admin.Widget.extend({
    template: admin.templateEngine.menu,
    renderElement: function() {
        this.elements = _.sortBy(admin.menuElements, function(el) {
            return el.importance;
        });
        this._super();
    },
    start: function() {
        var self = this;
        $("a", this.$element).click(function(ev) {
            var index = Number($(ev.target).attr("data-index"));
            self.display(index);
        });
        this.display(0);
    },
    display: function(index) {
        var elem = this.elements[index].class_;
        if (this.current)
            this.current.destroy();
        this.current = new (elem)(this.getParent());
        this.current.appendTo(this.$displayTo);
    },
});

admin.Articles = admin.Widget.extend({
    template: admin.templateEngine.articles,
});
admin.menuElements.push({string: "Articles", importance: 1, class_: admin.Articles});


});
})();

