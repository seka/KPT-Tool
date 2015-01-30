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

