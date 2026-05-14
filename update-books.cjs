const fs = require('fs');

const html = fs.readFileSync('books.html', 'utf8');

// The JSON-LD might be inside <script type="application/ld+json">
const scriptMatch = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);

if (scriptMatch) {
    try {
        const json = JSON.parse(scriptMatch[1]);
        const itemList = json['@graph'] ? json['@graph'].find(g => g['@type'] === 'ItemList') : json;
        let elements = [];
        if (itemList && itemList.itemListElement) {
            elements = itemList.itemListElement.map(e => e.item);
        } else if (json.itemListElement) {
            elements = json.itemListElement.map(e => e.item);
        }

        const keywordRegex = /data|ai|iceberg|lakehouse|agent|llm|rag|context/i;
        const aiDataBooks = elements.filter(book => {
            if (book['@type'] !== 'Book') return false;
            const titleMatch = keywordRegex.test(book.name || '');
            const descMatch = keywordRegex.test(book.description || '');
            return titleMatch || descMatch;
        });

        // Let's also prepend the official Dremio/O'Reilly/Manning ones if they aren't here
        // But the user said: "use the actual books covers, you can find them at books.alexmerced.com, also include ALL the books related to data or ai from my repetoire"
        // Wait, the snippet above didn't show "Apache Iceberg: The Definitive Guide". Let's assume it might be in the first 10 items.
        // Let's look at all books.
        
        let astroCode = `---
import Layout from '../layouts/Layout.astro';

const books = [
`;
        aiDataBooks.forEach(b => {
            astroCode += `	{
		title: ${JSON.stringify(b.name)},
		description: ${JSON.stringify(b.description || '')},
		image: ${JSON.stringify(b.image || '')},
		link: ${JSON.stringify(b.url || '')}
	},
`;
        });
        
        astroCode += `];
---

<Layout title="Data & AI Books by Alex Merced" description="Explore the full repertoire of Data and AI books by Alex Merced.">
	<div class="container page-header">
		<h1>Data & AI Books</h1>
		<p>Explore all the books by Alex Merced covering AI, data lakehouses, Apache Iceberg, and modern data infrastructure.</p>
		<a href="https://books.alexmerced.com/" target="_blank" rel="noopener noreferrer" class="button primary" style="margin-top: 1rem;">View All 35+ Books at books.alexmerced.com</a>
	</div>

	<div class="container">
		<div class="books-grid">
			{books.map((book) => (
				<div class="book-card card">
					<div class="book-image">
						<img src={book.image} alt={book.title} loading="lazy" />
					</div>
					<div class="book-info">
						<h3>{book.title}</h3>
						<p>{book.description}</p>
						<a href={book.link} target="_blank" rel="noopener noreferrer" class="button">Get the Book</a>
					</div>
				</div>
			))}
		</div>
	</div>
</Layout>

<style>
	.page-header {
		text-align: center;
		margin-bottom: 4rem;
	}

	.page-header h1 {
		font-size: 3rem;
		color: var(--accent);
	}

	.books-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
		gap: 3rem;
		max-width: 1200px;
		margin: 0 auto;
	}

	.book-card {
		display: flex;
		flex-direction: column;
		height: 100%;
		transition: transform 0.3s;
	}

	.book-image {
		width: 100%;
		border-radius: 4px;
		overflow: hidden;
		margin-bottom: 1.5rem;
		box-shadow: 0 10px 20px rgba(0,0,0,0.3);
	}

	.book-image img {
		width: 100%;
		height: auto;
		display: block;
		aspect-ratio: 3/4;
		object-fit: cover;
	}

	.book-info {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.book-info h3 {
		font-size: 1.5rem;
		margin-bottom: 1rem;
		color: var(--text);
	}

	.book-info p {
		color: var(--text-muted);
		margin-bottom: 2rem;
		flex: 1;
	}

	.book-info .button {
		align-self: flex-start;
		width: 100%;
		text-align: center;
	}
</style>
`;
        fs.writeFileSync('src/pages/books.astro', astroCode);
        console.log('Successfully wrote src/pages/books.astro with ' + aiDataBooks.length + ' books.');
    } catch (e) {
        console.error('Error parsing JSON:', e);
    }
} else {
    console.log('No JSON-LD found');
}
