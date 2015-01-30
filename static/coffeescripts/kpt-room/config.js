(function(require) {
  require.config({
    baseUrl: "/static/coffeescripts/kpt-room",
    paths: {
      "jquery": "/static/bower_components/jquery/dist/jquery.min"
      , "underscore": "/static/bower_components/underscore/underscore-min"
      , "masonry": "/static/bower_components/masonry/dist/masonry.pkgd.min"
    },
    shim: {
      "jquery": {
        exports: "$"
      }
      , "underscore": {
        exports: "_"
      }
      , "masonry": ["jquery"]
    }
  });

  return require({
    paths: {
      cs: "/static/bower_components/require-cs/cs"
      , "coffee-script": "/static/bower_components/coffeescript/extras/coffee-script"
    }
  }, ["cs!main"]);
})(require);
