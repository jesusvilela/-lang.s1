const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const port = 3005;

// Proxy for LM Studio NLP Module
app.use('/v1', createProxyMiddleware({
    target: 'http://192.168.56.1:1234',
    changeOrigin: true,
    pathRewrite: {
        '^/v1': '/v1',
    },
}));

app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
    console.log(`§-LANG n-Cosmos AAA Visibility Node is LIVE.`);
    console.log(`Projected Hamiltonian Flow available at: http://localhost:${port}`);
    console.log(`Bidirectional NLP Channel (QHC) mapped to LM Studio.`);
});
