document.addEventListener('DOMContentLoaded', () => {
    const filterButton = document.getElementById('filterButton');
    const filterDropdown = document.getElementById('filterDropdown');
    const applyFiltersButton = document.querySelector('.apply-filters');
    const searchInput = document.getElementById('searchInput');

    filterButton.addEventListener('click', () => {
        filterDropdown.classList.toggle('show'); // Toggle class for display
    });

    applyFiltersButton.addEventListener('click', () => {
        // Get the selected filters
        const selectedFilters = getSelectedFilters();

        // Construct the API URL with the filters
        const apiUrl = constructApiUrl(selectedFilters);

        // Perform the search with the API URL
        performSearch(apiUrl);

        // Hide the dropdown after applying filters
        filterDropdown.classList.remove('show');
    });

    function getSelectedFilters() {
        const filters = {};

        // Get selected genre(s)
        const genreCheckboxes = document.querySelectorAll('input[name="genre"]:checked');
        const selectedGenres = Array.from(genreCheckboxes).map(checkbox => checkbox.value);
        if (selectedGenres.length > 0) {
            filters.genres_name = selectedGenres.join(',');  // or use multiple genres.name=value parameters
        }

        // Get year
        const yearInput = document.querySelector('input[name="year"]');
        if (yearInput.value) {
            filters.year = yearInput.value;
        }

        // Get rating
        const ratingInput = document.querySelector('input[name="rating"]');
        if (ratingInput.value) {
            filters.rating_imdb = ratingInput.value;
        }

        return filters;
    }

    function constructApiUrl(filters) {
        let baseUrl = '/api/search-movies?';
        for (const key in filters) {
            baseUrl += `${key}=${encodeURIComponent(filters[key])}&`;
        }

        const searchQuery = searchInput.value;
        if (searchQuery) {
            baseUrl += `query=${encodeURIComponent(searchQuery)}&`;
        }

        return baseUrl.slice(0, -1); // Remove trailing '&'
    }

    async function performSearch(apiUrl) {
        try {
            const response = await fetch(apiUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            displayResults(data);  // Assumes displayResults function exists
        } catch (error) {
            console.error('Error fetching data:', error);
            // Handle error appropriately
        }
    }

    function displayResults(data) {
      console.log(data)
    }
});