define ["jquery", "masonry"], ($, Masonry) ->
  keepContainer = document.querySelector "#kpt-keep"
  masonry = new Masonry keepContainer, {
        itemSelector: ".item"
        columnWidth: 200
      }

  problemContainer = document.querySelector "#kpt-problem"
  masonry = new Masonry problemContainer, {
        itemSelector: ".item"
        columnWidth: 200
      }

  tryContainer = document.querySelector "#kpt-try"
  masonry = new Masonry tryContainer, {
        itemSelector: ".item"
        columnWidth: 200
      }

