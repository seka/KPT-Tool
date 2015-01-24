(function() {
  (function() {
    return define(function() {
      var link = function(url) {
        var el;
        el = document.createElement("link");
        el.type = "text/css";
        el.rel = "stylesheet";
        el.href = url;
        return document.getElementsByTagName("head")[0].appendChild(el);
      };
      return {
        link: link
      };
    });
  })();
}).call(this);
