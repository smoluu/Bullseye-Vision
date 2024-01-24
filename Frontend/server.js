const http = require("http");
const path = require("path");
const fs = require("fs");
require("dotenv").config();

http.createServer(function (req, res) 
  {
    path == req.url.toLowerCase();

    if (path == "/") res.writeHead(200, { "Content-Type": "text/html" });
    res.end();
    console.log(req.url);
  })
  .listen(process.env.PORT);
console.log(`SERVER LISTENING AT: 
  http://${process.env.HOST}:${process.env.PORT}`);
