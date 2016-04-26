function getWikimediaImage(elem, name, src) {
  var size = 500;
  var url = "//en.wikipedia.org/w/api.php?action=query&titles=" + name + "&prop=pageimages&format=json&pithumbsize=" + size;
  $.ajax({
    url: url,
    dataType: 'jsonp'
  }).done(function(data) {
      var pages = data.query.pages;
      var page = pages[Object.keys(pages)[0]];
      if (src)
        elem.src = page.thumbnail.source;
      else
        $(elem).css("background-image", "url(" + page.thumbnail.source + ")");
    }).fail(function() {
      console.log('Error: could not connect to wikimedia api');
      return null;
    });
}

$('.img-headshot').each(function() {
  if (this.dataset.playerName)
    getWikimediaImage(this, this.dataset.playerName.replace(/\ /g, '_'));
});

$('.img-profile').each(function() {
  if (this.dataset.playerName) {
    getWikimediaImage(this, this.dataset.playerName.replace(/\ /g, '_'), true);
  }
});
