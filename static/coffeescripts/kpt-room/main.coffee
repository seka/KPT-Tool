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

  sock = new WebSocket("ws://#{document.domain}:5000/websock/connect")

  sock.onopen = () ->
    sock.send("test data -------")

  sock.onmessage = (e) ->
    el = $ template {
      message: "#{e.data}"
    }
    # appendだと再配置がうまくいかない？
    $(keepContainer).prepend el
    keepMasonry.prepended( el )

