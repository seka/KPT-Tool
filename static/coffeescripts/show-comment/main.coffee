define ["jquery", "underscore", "masonry", "modal"], ($, _, Masonry) ->
  template = _.template """
    <div id="<%- id %>" class="items">
      <p><%- comment %></p>
      <div class="clear"></div>
    </div>
  """

  container = document.querySelector "#kpt-comments"
  masonry = new Masonry container, {
        itemSelector: ".items"
      }

  kptId = $("#kpt-id").val()
  sock = new WebSocket("ws://#{document.domain}:5000/websock/connect/comment/#{kptId}")

  sock.onmessage = (e) ->
    data = JSON.parse e.data
    switch data.type
      when "append"
        el = $ template
          id: "#{data.kpt_id}"
          comment: "#{data.text}"

        # appendだと再配置がうまくいかない？
        $(container).prepend el
        masonry.prepended el

      when "remove"
        $("#commentid-#{data.commentId}").remove()
        masonry.remove $ "#commentid-#{data.commentId}"
    masonry.layout()

  $(".event-delete").click () ->
    commentId = $(@).attr "id"
    obj = JSON.stringify
      commentId: commentId
      type: "remove"
    sock.send obj
