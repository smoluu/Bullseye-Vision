const http = require("http");
const path = require("path");
const fs = require("fs");
const { type } = require("os");
require("dotenv").config();
const root = __dirname;

var server = http.createServer(function (req, res) {
  console.log(`${req.method} ${"request to:"} ${req.url}`);

  if(req.url == "/"){req.url = "/index.html"}
  const extension = path.extname(req.url);
  firstUrlSegment = req.url.split("/")[1]
  const filePath = path.join(root,"public",req.url)
  
  console.log("Full filePath: ", filePath)
  
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/html" });
      res.end("404: File not found");
    } else {
      res.writeHead(200, { "Content-Type": type });
      res.end(data);
    }
  });

});

server.listen(process.env.PORT);

console.log(
  `SERVER LISTENING AT: http://${process.env.HOST}:${process.env.PORT}`
);
