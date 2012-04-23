
(function() {
admin = {};
admin.templateEngine = new TemplateEngine();
admin.loaded = admin.templateEngine.loadFile("templates.html").pipe(function() {

admin.Widget = nova.Widget.extend({
    template: function() {
        return "<div></div>";
    },
    renderElement: function() {
        var html = this.template();
        var $elem = $(html);
        $elem.replaceAll(this.$element);
        this.$element = $elem;
    },
});

admin.Admin = admin.Widget.extend({
    template: admin.templateEngine.admin,
});

var json_rpc = function(url, fct_name, params, settings) {
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
        return json_rpc("../adminapi", fct_name, {args: args || [], kwargs: kwargs || {}});
    },
});

var ses = new admin.Session();
ses.call("hello").then(function() {
    console.log("everything is fine", _.toArray(arguments));
}, function() {
    console.log("everything goes bad", _.toArray(arguments));
});

});
})();

