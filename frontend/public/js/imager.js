function getWikimediaImage(elem, name, src, team) {
  if (team) {
    $.getJSON("http://en.wikipedia.org/w/api.php?action=mobileview&format=json&page=" + name + "&redirect=yes&sections=0&prop=text&sectionprop=toclevel%7Clevel%7Cline%7Cnumber%7Cindex%7Cfromtitle%7Canchor&callback=?", function(json) { 
      var wikitext = json.mobileview.sections[0].text;
      var full = 'http:' + wikitext.split('<img alt=')[1].split('src="')[1].split('" ')[0];
      if (src) elem.src = full;
      else $(elem).css('background-image', 'url(' + full + ')');
    });    
  } else {
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
}

$('.img-headshot').each(function() {
  if (this.dataset.playerName)
    getWikimediaImage(this, this.dataset.playerName.replace(/\ /g, '_'), false, false);
  if (this.dataset.teamName) {
    var name = this.dataset.teamName;
    if (name.startsWith('AFC'))
      getWikimediaImage(this, name.replace(/\ /g, '_'), false, true);
    else
      getWikimediaImage(this, name.replace(/\ /g, '_') + '_F.C.', false, true);
  }
});

$('.img-profile').each(function() {
  if (this.dataset.playerName)
    getWikimediaImage(this, this.dataset.playerName.replace(/\ /g, '_'), true, false);
  if (this.dataset.teamName) {
    var name = this.dataset.teamName;
    if (name.startsWith('AFC'))
      getWikimediaImage(this, name.replace(/\ /g, '_'), true, true);
    else
      getWikimediaImage(this, name.replace(/\ /g, '_') + '_F.C.', true, true);
  }
});
