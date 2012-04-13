
var TemplateEngine = function() {
    this.init();
}

_.extend(TemplateEngine.prototype, {
    _template_setting: {
        interpolate : /\{\{\-(.+?)\}\}/g,
        escape: /\{\{(.+?)\}\}/g,
        evaluate: /\{\%(.+?)\%\}/g,
    },
    init: function() {
        this.set_environment({});
    },
    load_file: function(filename) {
        var self = this;
        return $.get(filename).pipe(function(content) {
            return self._parse_file(content);
        });
    },
    _parse_file: function(file_content) {
        var reg = /\{\#\s*template\s+(\w+)\s*\#\}((?:.*\n)*?)\{\#\s*endtemplate\s*\#\}/g;
        var to_add = {};
        var search;
        while (search = reg.exec(file_content)) {
            if (this[search[1]])
                throw new Error(search[1] + " is an already defined template");
            this[search[1]] = this._build_template(search[2]);
        }
    },
    _build_template: function(template) {
        var self = this;
        var result = _.template(template, undefined, this._template_setting);
        return function(data) {
            return result(_.extend({engine: self}, self._env, data));
        };
    },
    set_environment: function(env) {
        this._env = env;
    },
});

