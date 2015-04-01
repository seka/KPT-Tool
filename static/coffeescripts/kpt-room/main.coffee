define ["jquery", "underscore", "masonry", "modal"], ($, _, Masonry) ->
  template = _.template """
    <div class="items">
      <p><%- entry %></p>
      <ul>
        <li><a href="#" class="good-click-trigger">そう思う！</a></li>
        <li><a href="#">コメントする</a></li>
        <li><a href="#">コメントを見る</a></li>
      </ul>
      <div class="clear"></div>
    </div>
  """

  keepContainer = document.querySelector "#kpt-keep"
  keepMasonry = new Masonry keepContainer, {
        itemSelector: ".items"
      }

  problemContainer = document.querySelector "#kpt-problem"
  problemMasonry = new Masonry problemContainer, {
        itemSelector: ".items"
      }

  tryContainer = document.querySelector "#kpt-try"
  tryMasonry = new Masonry tryContainer, {
        itemSelector: ".items"
      }

  roomId = $("#room-id").val()
  sock = new WebSocket("ws://#{document.domain}:5000/websock/connect/room/#{roomId}")

  sock.onmessage = (e) ->
    data = JSON.parse e.data
    el = $ template
      entry: "#{data.entry}"

    # appendだと再配置がうまくいかない？
    switch data.type
      when "keep"
        $(keepContainer).prepend el
        keepMasonry.prepended el
      when "problem"
        $(problemContainer).prepend el
        problemMasonry.prepended el
      when "try"
        $(tryContainer).prepend el
        tryMasonry.prepended el
      when "remove"
        $("#kptid-#{data.kpt_id}").remove()
        keepMasonry.remove $ "#kptid-#{data.kpt_id}"
        problemMasonry.remove $ "#kptid-#{data.kpt_id}"

    keepMasonry.layout()
    problemMasonry.layout()
    tryMasonry.layout()

  sock.onopen = () ->
    $(".event-delete-kpt").click () ->
      kptId = $(@).attr "id"
      obj = JSON.stringify
        kpt_id: kptId
        type: "remove"
      sock.send obj

    $(".kpt-click-trigger").click (e) ->
      roomId = $("#room-id").val()
      msg = $("#kpt-message").val()
      type = $(@).val()

      return true if not msg

      obj = JSON.stringify
        room_id: roomId
        entry: msg
        type: type
      sock.send obj

    $(".kpt-click-trigger").click (e) ->
      roomId = $("#room-id").val()
      msg = $("#kpt-message").val()
      type = $(@).val()

      return true if not msg

      obj = JSON.stringify
        room_id: roomId
        entry: msg
        type: type
      sock.send obj

  goodSock = new WebSocket("ws://#{document.domain}:5000/websock/connect/good")
  goodSock.onopen = () ->
    $(".good-click-trigger").click (e) ->
      kptId = $(@).val()
      text = $(@).text()
      count = parseInt(text.match(/\d+/))
      obj = {}

      if text.match("そう思う！")
        obj = JSON.stringify
          kpt_id: kptId
          type: "add"
          count: count
        text = text.replace "そう思う！", "取り消す"
      else
        obj = JSON.stringify
          kpt_id: kptId
          type: "sub"
          count: count
        text = text.replace "取り消す", "そう思う！"

      $(@).text text
      goodSock.send obj

  goodSock.onmessage = (e) ->
    data = JSON.parse e.data
    kptId = data.kpt_id
    el = $("#kptid-#{kptId}").find(".good-click-trigger")
    text = el.text()

    if data.type is "sub"
      if data.user?
        text = text.replace "取り消す", "そう思う！"
      count = data.count - 1
    else
      if data.user?
        text = text.replace "そう思う！", "取り消す"
      count = data.count + 1

    el.text text.replace /\d+/, "#{count}"

  $(".event-delete-room").click () ->
    roomId = $(@).attr "id"
    $.get "/room/delete/#{roomId}", { room_id: roomId }, (data) ->
      window.location.href = "/" if data is "Success"
