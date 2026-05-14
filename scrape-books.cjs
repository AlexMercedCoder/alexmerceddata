const https = require('https');

https.get('https://books.alexmerced.com', (res) => {
    let data = '';

    res.on('data', (chunk) => {
        data += chunk;
    });

    res.on('end', () => {
        // Find all links that go to Amazon
        const books = [];
        const regex = /<a[^>]*href="([^"]*amazon\.com[^"]*)"[^>]*>.*?<img[^>]*src="([^"]*)"[^>]*>.*?<\/a>/gis;
        
        // Wait, the structure might be different. Let's just use a simple regex to find all books.
        // Actually, the structure from curl showed:
        // href="..."
        // src="..."
        // Let's just output the whole HTML to a file and parse it.
        const fs = require('fs');
        fs.writeFileSync('books.html', data);
        console.log('Saved books.html');
    });
}).on("error", (err) => {
    console.log("Error: " + err.message);
});
