define ["jquery", "underscore", "masonry"], ($, _, Masonry) ->
  template = _.template """
    <div class="items">
      <p><%- message %></p>
      <ul>
        <li><a href="#">そう思う！</a></li>
        <li><a href="#">コメントする</a></li>
        <li><a href="#">コメントを見る</a></li>
      </ul>
      <div class="clear"></div>
    </div>
  """

  keepContainer = document.querySelector "#kpt-keep"
  masonry = new Masonry keepContainer, {
        itemSelector: ".items"
      }

  problemContainer = document.querySelector "#kpt-problem"
  masonry = new Masonry problemContainer, {
        itemSelector: ".items"
      }

  tryContainer = document.querySelector "#kpt-try"
  console.log tryContainer
  masonry = new Masonry tryContainer, {
        itemSelector: ".items"
      }

  sock = new WebSocket("ws://#{document.domain}:5000/websock/connect")

  sock.onopen = () ->
    sock.send("test data -------")

  sock.onmessage = (e) ->
    $("#kpt-keep").append template {
      message: "#{e.data}"
    }

