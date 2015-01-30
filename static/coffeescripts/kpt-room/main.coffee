define ["jquery", "masonry"], ($, Masonry) ->
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
    console.log sock
    sock.send("test data -------")

  sock.onmessage = (e) ->
    console.log "#{e.data}"

