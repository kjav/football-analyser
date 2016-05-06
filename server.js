var express = require("express");
var app = express();
var swig = require("swig");
var router = express.Router();
var path = __dirname + '/frontend/views/';
var pg = require('pg');
var qs = require('querystring');
var url = require('url');
var spawn = require('child_process').spawn;

var swig = new swig.Swig();
app.engine('html', swig.renderFile);
app.set('view engine', 'html');

var simulator = spawn('python', ['analysis/simulation.py']);
var received = '';
var simulator_loaded = false;
var awaiting_results = null;
var stdout_buff = simulator.stdout.on('data', function(data) {
  if (!simulator_loaded) {
    received = received + data;
    if (~received.indexOf('ready for input\n')) {
      console.log('Simulator loaded!');
      simulator_loaded = true;
    }
  } else {
    var result = '' + data;
    if (awaiting_results) {
      awaiting_results(result);
    }
  }
});
var stderr_buff = simulator.stderr.on('data', function(data) {
  console.log('Simulation error: ' + data);
});

function simulate(team1, team2, lineup1, lineup2, callback) {
  awaiting_results = function(data) {
    callback(data);
    awaiting_results = null;
  };
  simulator.stdin.write(team1 + '\n');
  simulator.stdin.write(team2 + '\n');
  simulator.stdin.write(lineup1 + '\n');
  simulator.stdin.write(lineup2 + '\n');
}

var conString = "postgres://coxswain:Torpids2016@football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com/postgres";
//this initializes a connection pool
//it will keep idle connections open for a (configurable) 30 seconds
//and set a limit of 10 (also configurable)

router.use(function (req,res,next) {
  console.log("/" + req.method);
  next();
});

router.get("/editorial", function(req, res) {
  res.render(path + "editorial.html");
});

router.get("/",function(req,res){
  pg.connect(conString, function(err, client, done) {
    client.query('SELECT name, id FROM player', [], function(err, result) {
      res.render(path + "dashboard.html", { players: result.rows });
    });
  });
});

router.get('/lineup', function(req, res) {
  pg.connect(conString, function(err, client, done) {
    client.query('SELECT name, id FROM player', [], function(err, result) {
      if (err) console.log(err);
      done();
      res.render(path + 'lineup.html', { players: result.rows });
    });
  });
});

router.get('/players', function(req, res) {
  pg.connect(conString, function(err, client, done) {
    if (err) console.log(err);
    client.query('SELECT name, id FROM player', [], function(err, result) {
      if (err) console.log(err);
      done();
      res.render(path + 'players.html', { players: result.rows });
    });
  });
});

router.get('/teams', function(req, res) {
  pg.connect(conString, function(err, client, done) {
    client.query('SELECT name, id FROM team', [], function(err, result) {
      if (err) console.log(err);
      done();
      res.render(path + 'teams.html', { teams: result.rows });
    });
  });
});

router.get('/teammatches', function(req, res) {
  pg.connect(conString, function(err, client, done) {
    client.query('SELECT * FROM team_match', [], function(err, result) {
      if (err) console.log(err);
      done();
      res.end(JSON.stringify(result.rows));
    });
  });
});

router.get("/player",function(req,res){
  var q = qs.parse(url.parse(req.url).query)
  pg.connect(conString, function(err, client, done) {
    if (err) console.log(err);
    client.query('SELECT name, Position, Height, Division, apps, Goals, age, LValue, PredictedValue  FROM player WHERE id='+q.id, [], function(err, result) {
      if (err) console.log(err);
      done();
      var player = result.rows[0];
      console.log(player);
      client.query('SELECT team.name AS teamname, team.id as teamid, other_team.name AS otherteamname, other_team.id as otherteamid, player_match.Position, player_match.Goals, player_match.TotalPass FROM player_match INNER JOIN team_match ON team_match.id=teammatchid INNER JOIN team ON team_match.team=team.id INNER JOIN match ON match.id=team_match.match INNER JOIN team_match other_team_match ON other_team_match.match=match.id AND other_team_match.team!=team.id INNER JOIN team other_team ON other_team.id=other_team_match.team WHERE playerid=' + q.id, [], function(err, result) {
        if (err) console.log(err);
        var playermatches = result.rows;
        done();
        res.render(path + "player.html", { player: player, playermatches: playermatches });
      });
    });
  });
});

router.get("/team",function(req,res){
  var q = qs.parse(url.parse(req.url).query);
  pg.connect(conString, function(err, client, done) {
    client.query('SELECT name FROM team WHERE id='+q.id, [], function(err, result) {
      if (err) console.log(err);
      done();
      var team = result.rows[0];
      client.query('SELECT other_team.name AS otherteamname, other_team.id as otherteamid, team_match.Goals, other_team_match.Goals as otherteamgoals FROM team_match INNER JOIN match ON match.id=team_match.match INNER JOIN team_match other_team_match ON other_team_match.match=match.id AND other_team_match.team!=team_match.team INNER JOIN team other_team ON other_team.id=other_team_match.team WHERE team_match.team=' + q.id, [], function(err, result) {
        if (err) console.log(err);
        var teammatches = result.rows;
        done();
        res.render(path + "team.html", { team: team, teammatches: teammatches });
      });
    });
  });
});

router.get("/an", function(req, res) {
  simulate('1', '2', '1 2 3 4 5 6 7 8 9 10 11', '12 13 14 15 16 17 18 19 20 21 22', function(data) {
    res.end(data);
  });
});
app.use("/",router);

app.use(express.static('./frontend/public'));

app.use("*",function(req,res){
  res.sendFile(path + "404.html");
});

app.listen(3000,function(){
  console.log("Live at Port 3000");
});
