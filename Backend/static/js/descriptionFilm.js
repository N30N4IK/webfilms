document = addEventListener('DOMContentLoaded', function() { 
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const movieDetailsDiv = document.getElementById('movie-Details');
    
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const searchTerm = searchInput.valeu.toLowerCase();

        let foundMovie = null;
        for (let i = 0; i < movies.length; i++) {
            if (movies[i].title.toLowerCase().includes(searchTerm)) {
                foundMovie = movies[i];
                break;
            }
        }

        if (foundMovie) {
            displayMovieDetails(foundMovie);
        } else {
            movieDetailsDiv.innerHTML = "<p>Фильм не найден</p>";
        }
    });


    function displayMovieDetails(movie) {
        let html = `
        <div class='movie-details'>
            <div class='movie-poster'>
                <img src='${movie.poster}' alt='${movie.title} Poster'>
            </div>
            <div class='movie-info'>
                <h1>${movie.title} (${movie.year})</h1>
                <h2> О фильме</h2>
                <ul>
                    <li>Год производства: ${movie.year}</li>
                    <li>Страна: ${movie.country}</li>
                    <li>Жанр: ${movie.genre}</li>
                    <li>Режиссер: ${movie.director}</li>
                    <li>Сцценарий ${movie.screenwriter}</li>
                    <li>Продюсер: ${movie.producers}</li>
                    <li>Композитор: ${movie.composer}</li>
                    <li>Художник: ${movie.artist}</li>
                    <li>Возраст: ${movie.age_rating}</li>
                </ul>

                <div class='hashtags'>
                    <h3>Хештеги:</h3>
                    <ul>
                        ${movie.hashtags.map(tag => `<li>#${tag}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;

    movieDetailsDiv.innerHTML = html;
    }

    function handleRouteChange() {
        const urlParams = new URLSearchParams(window.location.search);
        const movieId = parseInt(urlParams.get('q'));

        if (movieId) {
            const movie = findMovieById(movieId);
            displayMovieDetails(movie)
        } else {
            movieDetailsDiv.innerHTML = '<p>Пожалуйста, укажите id фильма в url</p>';
        }
    }

    window.addEventListener('load', handleRouteChange);
    window.addEventListener('popstate', handleRouteChange);

    window.goToMovie = function(movieId) {
        const newUrl = `?q=${movieId}`;
        history.pushState({ movieId: movieId }, '', newUrl);
        handleRouteChange();
    };
});