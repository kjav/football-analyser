function getWikimediaImage(elem, name) {
  var size = 500;
  var url = "//en.wikipedia.org/w/api.php?action=query&titles=" + name + "&prop=pageimages&format=json&pithumbsize=" + size;
  $.ajax({
    url: url,
    dataType: 'jsonp'
  }).done(function(data) {
      var pages = data.query.pages;
      var page = pages[Object.keys(pages)[0]];
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
