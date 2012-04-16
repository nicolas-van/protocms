
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

});
})();

