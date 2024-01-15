var express = require('express');
var path = require('path');
const dotenv = require('dotenv');

dotenv.config();
var app = express();

port = process.env.PORT || 80


app.use(express.static(path.join(__dirname, 'public')));
app.use("/css", express.static("./node_modules/bootstrap/dist/css"));
app.use("/js", express.static("./node_modules/bootstrap/dist/js"));

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname, "/pages/index.html"))
});

app.listen(process.env.PORT)
console.log("Server started: localhost:" + process.env.PORT )