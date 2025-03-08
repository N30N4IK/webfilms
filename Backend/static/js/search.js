document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const searchResultsDiv = document.getElementById('searchResults');

    searchButton.addEventListener('click', async () => {
        const query = searchInput.value;
        if (!query) {
            alert('Please enter a search query');
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/search-movies?q=${encodeURIComponent(query)}`);  //  Изменен URL
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error fetching data:', error);
            searchResultsDiv.textContent = 'An error occurred while fetching data.';
        }
    });

    function displayResults(data) {
        searchResultsDiv.innerHTML = ''; // Очищаем предыдущие результаты

        if (data && data.docs && data.docs.length > 0) { // Проверяем структуру ответа
            data.docs.forEach(movie => {
                const movieElement = document.createElement('div');
                movieElement.innerHTML = `
                    <h2>${movie.name} (${movie.year})</h2>
                    <p>${movie.description || 'No description available'}</p>
                    <img src="${movie.poster?.url || 'placeholder.jpg'}" alt="${movie.name} poster" width="100">
                `;  // Добавьте проверку на существование poster.url
                searchResultsDiv.appendChild(movieElement);
            });
        } else {
            searchResultsDiv.textContent = 'No movies found matching your search.';
        }
    }
});
