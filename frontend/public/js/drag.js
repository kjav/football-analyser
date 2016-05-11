$('#team1').on('drop dragdrop',function(){
    event.preventDefault();
    event.stopPropagation();
    $(this).css('background','');
});
$('#team1').on('dragenter',function(event){
    event.preventDefault();
    event.stopPropagation();
    $(this).css('background','#aaa');
});
$('#team1').on('dragleave',function(){
    event.preventDefault();
    event.stopPropagation();
    $(this).css('background','');
});
$('#team1').on('dragover',function(event){
    event.preventDefault();
    event.stopPropagation();
});
$('#team2').on('drop dragdrop',function(){
    event.preventDefault();
    event.stopPropagation();
    $(this).css('background','');
});
$('#team2').on('dragenter',function(event){
    event.preventDefault();
    event.stopPropagation();
    $(this).css('background','#aaa');
});
$('#team2').on('dragleave',function(){
    event.preventDefault();
    event.stopPropagation();
    $(this).css('background','');
});
$('#team2').on('dragover',function(event){
    event.preventDefault();
    event.stopPropagation();
});

function footballize(s) {
  s = s.replace(/\ /g, '_');
  return s.startsWith('AFC') ? s : s + '_F.C.';
}

select1.onchange = function() {
  getWikimediaImage(select1, footballize(select1.options[select1.value-1].innerHTML), true, true);
};
select2.onchange = function() {
  getWikimediaImage(select2, footballize(select2.options[select2.value-1].innerHTML), true, true);
};
getWikimediaImage(select1, footballize(select1.options[select1.value-1].innerHTML), true, true);
getWikimediaImage(select2, footballize(select2.options[select2.value-1].innerHTML), true, true);

function dragstart_handler(event) {
  var elem;
  if (event.target.tagName === 'A')
    elem = event.target.parentNode.parentNode;
  else
    elem = event.target;
  event.dataTransfer.setData("text/plain", elem.id + ',' + elem.children[0].firstChild.innerHTML);
  event.dataTransfer.dropEffect = 'move';
}

function drop_handler(event) {
  console.log(event.dataTransfer.getData('text'));
  var p = document.createElement('p');
  p.style.clear = 'both';
  p.innerHTML = event.dataTransfer.getData('text').split(',')[1] + ' ';
  p.id = event.dataTransfer.getData('text').split(',')[0];
  var cross = document.createElement('span');
  cross.classList.add('glyphicon');
  cross.classList.add('glyphicon-remove');
  cross.onclick = function(e) {
    var player = e.target.parentNode;
    var team = e.target.parentNode.parentNode;
    team.removeChild(player);
    updateTeamCounts();
  };
  cross.style.color = '#a94442';
  p.appendChild(cross);
  if (team1.contains(event.target) || team1 === event.target)
    team1.appendChild(p);
  if (team2.contains(event.target) || team2 === event.target)
    team2.appendChild(p);
  updateTeamCounts();
}

function analyze(e) {
  leftteamimage.src = select1.src;
  rightteamimage.src = select2.src;
  team1result.innerHTML = "<img src='loading.gif' style='height: 30px' />";
  team2result.innerHTML = "<img src='loading.gif' style='height: 30px' />";
  if (team1.children.length != 14) { alert('11 players needed in team 1'); e.preventDefault(); return false; }
  if (team2.children.length != 14) { alert('11 players needed in team 2'); e.preventDefault(); return false; }
  var _team1 = '' + select1.value;
  var _team2 = '' + select2.value;
  var _lineup1 = '';
  for (var i=3;i<team1.children.length;i++) {
    if (i != 3) _lineup1 = _lineup1 + ' ';
    _lineup1 = _lineup1 + team1.children[i].id.split('player')[1];
  }
  var _lineup2 = '';
  for (var i=3;i<team2.children.length;i++) {
    if (i != 3) _lineup2 = _lineup2 + ' ';
    _lineup2 = _lineup2 + team2.children[i].id.split('player')[1];
  }
  var score = $.ajax('/analyze?team1=' + _team1 + '&team2=' + _team2 + '&lineup1=' + _lineup1 + '&lineup2=' + _lineup2).done(function(data) {
    data = [data.split(',')[0].split('(')[1], data.split(', ')[1].split(')')[0]];
    var probs = getProb(+data[0], +data[1]);
    probs = probs.map(function(x) { return Math.round(x*1000)/10 });
    team1result.innerHTML = data[0] + '<br />(' + probs[0].toString() + '% odds)';
    team2result.innerHTML = data[1] + '<br />(' + probs[1].toString() + '% odds)';
  });
}

function getProbableLineup(team) {
  var parent = team === 1 ? team1 : team2;
  var currentLineup = parent.getElementsByTagName('p');
  while (currentLineup.length) currentLineup[0].parentNode.removeChild(currentLineup[0]);
  if (team === 1) team = select1.value;
  else team = select2.value;
  console.log(parent.children);
  $.ajax('/probablelineup?teamid=' + team).done(function(data) {
    var lineup = JSON.parse(data)[0];
    for (var i=1;i<12;i++) {
      var p = document.createElement('p');
      p.style.clear = 'both';
      p.id = 'player' + lineup['player' + i + 'id'];
      if (document.getElementById(p.id).tagName !== 'TR') p.innerHTML = document.getElementById(p.id).innerHTML.split('<')[0] + ' ';
      else p.innerHTML = document.getElementById(p.id).children[0].firstChild.innerHTML + ' ';
      var cross = document.createElement('span');
      cross.classList.add('glyphicon');
      cross.classList.add('glyphicon-remove');
      cross.onclick = function(e) {
        var player = e.target.parentNode;
        var t = e.target.parentNode.parentNode;
        t.removeChild(player);
        updateTeamCounts();
      };
      cross.style.color = '#a94442';
      p.appendChild(cross);
      parent.appendChild(p);
    }
    updateTeamCounts();
  });
}

function updateTeamCounts() {
  var n1 = team1.children.length - 3;
  if (n1 < 11) team1count.style.color = '#8a6d3b';
  else if (n1 > 11) team1count.style.color = '#a94442';
  else team1count.style.color = '#3c763d';
  team1count.innerHTML = '(' + (team1.children.length - 3).toString() + ')';
  var n2 = team2.children.length - 3;
  if (n2 < 11) team2count.style.color = '#8a6d3b';
  else if (n2 > 11) team2count.style.color = '#a94442';
  else team2count.style.color = '#3c763d';
  team2count.innerHTML = '(' + (team2.children.length - 3).toString() + ')';
}

updateTeamCounts();
