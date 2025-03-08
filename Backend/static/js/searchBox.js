document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchHistoryList = document.getElementById('search-history')
    let searchHistory = JSON.parse(localStorage.getItem('searchHistory')) || []

    function updateSearchHistoryList() {
        searchHistoryList.innerHTML = '';
        searchHistory.forEach(term => {
            const li = document.createElement('li')
            li.textContent = term
            li.addEventListener('click', () => {
                searchInput.value = term;
                hideSearchHistory();
            });
            searchHistoryList.appendChild(li);
        });
    }

    function showSearchHistory() {
        searchHistoryList.classList.add('visible');
    }

    function hideSearchHistory() {
        searchHistoryList.classList.remove('visible');
    }

    function addToSearchHistory(term) {
        if (!searchHistory.includes(term)) {
            searchHistory.unshift(term);
            searchHistory = searchHistory.slice(0, 5);

            localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
            updateSearchHistoryList();
        }
    }

    searchInput.addEventListener('focus', () => {
        updateSearchHistoryList();
        showSearchHistory();
    });
    
    searchInput.addEventListener('blur', () =>  {
        setTimeout(hideSearchHistory, 100);
    });

    searchInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            const searchTerm = searchInput.value.trim();
            if (searchTerm) {
                addToSearchHistory(serachTerm);

                console.log('Выполняется поиск по запросу: ${searchTerm}');
                searchInput.value = '';
            }
        }
    });


    updateSearchHistoryList();
});