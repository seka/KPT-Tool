define ["jquery", "cssloader"], ($, cssLoader) ->
  localPath = "/static/stylesheets/top/main.css"
  pathFromApp = require.toUrl(localPath)
  cssLoader.link(pathFromApp)

