(function(require) {
  require.config({
    baseUrl: "/static/coffeescripts/top",
    paths: {
      "jquery": "/static/bower_components/jquery/dist/jquery.min"
      , "underscore": "/static/bower_components/underscore-min"
    },
    shim: {
      "jquery": {
        exports: "$"
      }
      , "underscore": {
        exports: "_"
      }
    }
  });

  return require({
    paths: {
      cs: "/static/bower_components/require-cs/cs"
      , "coffee-script": "/static/bower_components/coffeescript/extras/coffee-script"
    }
  }, ["cs!main"]);
})(require);
