const http = require('http');
const fs = require('fs');
const path = require('path');

const port = Number(process.env.PORT || 3000);
const buildDir = path.join(__dirname, 'build');

const mimeTypes = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.ico': 'image/x-icon',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.map': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
};

function sendFile(filePath, response) {
  fs.readFile(filePath, (error, data) => {
    if (error) {
      response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      response.end('Internal server error');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    response.writeHead(200, {
      'Content-Type': mimeTypes[ext] || 'application/octet-stream',
      'Cache-Control': ext === '.html' ? 'no-cache' : 'public, max-age=31536000, immutable',
    });
    response.end(data);
  });
}

const server = http.createServer((request, response) => {
  const requestPath = request.url === '/' ? '/index.html' : decodeURIComponent(request.url.split('?')[0]);
  const safePath = path.normalize(requestPath).replace(/^(\.\.[/\\])+/, '');
  const assetPath = path.join(buildDir, safePath);

  fs.stat(assetPath, (error, stats) => {
    if (!error && stats.isFile()) {
      sendFile(assetPath, response);
      return;
    }

    sendFile(path.join(buildDir, 'index.html'), response);
  });
});

server.listen(port, '0.0.0.0', () => {
  console.log(`Static frontend server running on port ${port}`);
});
