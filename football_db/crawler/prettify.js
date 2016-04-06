var fs = require('fs');
fs.readFile("data.json", function(err, data) {
    if (err) {
        return console.log(err);
    } else {
        console.log("no error for file read");
        var object = JSON.parse(data)
        var pretty_string = JSON.stringify(object, null, 4);
        fs.writeFile("data_pretty.json", pretty_string, function(err) {
            if (err) {
                return console.log(err)
            } else {
                console.log("saved to data_pretty.json")
            }
        });
    }

});
