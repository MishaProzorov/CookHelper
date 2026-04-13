/**
 * search.js — логика страницы поиска рецептов
 * Использует AJAX для обращения к /recipes/search
 */

document.addEventListener('DOMContentLoaded', function () {
    // === Элементы DOM ===
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const recipeTypeFilter = document.getElementById('recipeTypeFilter');
    const dietFilter = document.getElementById('dietFilter');
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    const recipesGrid = document.getElementById('recipesGrid');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const noResults = document.getElementById('noResults');

    // === Debounce: задержка перед отправкой запроса ===
    let debounceTimer = null;
    const DEBOUNCE_DELAY = 500; // 500 мс после последнего ввода

    // === Обработчик поиска ===
    function performSearch() {
        const query = searchInput.value.trim();
        const recipeType = recipeTypeFilter.value;
        const diet = dietFilter.value;

        // Минимальная длина запроса — 3 символа (требование API)
        if (query.length < 3) {
            recipesGrid.innerHTML = '';
            noResults.classList.add('d-none');
            return;
        }

        showLoading();
        fetchRecipes(query, recipeType, diet);
    }

    // === AJAX-запрос к API ===
    async function fetchRecipes(query, recipeType, diet) {
        // Формируем URL с параметрами
        const params = new URLSearchParams();
        params.append('query', query);
        if (recipeType) params.append('recipe_type', recipeType);
        if (diet) params.append('diet', diet);

        try {
            const response = await fetch(`/recipes/search?${params.toString()}`);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const recipes = await response.json();
            renderRecipes(recipes);
        } catch (error) {
            console.error('Ошибка при поиске рецептов:', error);
            showError('Произошла ошибка при поиске. Попробуйте позже.');
        }
    }

    // === Рендер карточек рецептов ===
    function renderRecipes(recipes) {
        hideLoading();

        if (!recipes || recipes.length === 0) {
            recipesGrid.innerHTML = '';
            noResults.classList.remove('d-none');
            return;
        }

        noResults.classList.add('d-none');

        recipesGrid.innerHTML = recipes.map(function (recipe) {
            const imageHtml = recipe.image
                ? `<img src="${recipe.image}" alt="${escapeHtml(recipe.title)}" class="recipe-card-img" loading="lazy">`
                : `<div class="recipe-card-img-placeholder">🍽️</div>`;

            return `
                <div class="col-lg-4 col-md-6 col-sm-6">
                    <div class="recipe-card" onclick="window.location.href='/recipe/${recipe.id}'">
                        <div class="recipe-card-img-wrapper">
                            ${imageHtml}
                        </div>
                        <div class="recipe-card-body">
                            <h6 class="recipe-card-title">${escapeHtml(recipe.title)}</h6>
                            <a href="/recipe/${recipe.id}" class="recipe-card-btn" onclick="event.stopPropagation();">
                                Открыть
                            </a>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    // === Показать / скрыть загрузку ===
    function showLoading() {
        loadingIndicator.classList.remove('d-none');
        noResults.classList.add('d-none');
        recipesGrid.innerHTML = '';
    }

    function hideLoading() {
        loadingIndicator.classList.add('d-none');
    }

    // === Показать ошибку ===
    function showError(message) {
        hideLoading();
        recipesGrid.innerHTML = `<div class="col-12 text-center"><p class="text-danger">${message}</p></div>`;
    }

    // === Экранирование HTML (защита от XSS) ===
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // === Привязка событий ===

    // Кнопка "Найти"
    searchBtn.addEventListener('click', performSearch);

    // Enter в поле ввода
    searchInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch();
        }
    });

    // Debounce при вводе текста
    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(performSearch, DEBOUNCE_DELAY);
    });

    // Изменение фильтров — автоматический поиск
    recipeTypeFilter.addEventListener('change', function () {
        if (searchInput.value.trim().length >= 3) {
            performSearch();
        }
    });

    dietFilter.addEventListener('change', function () {
        if (searchInput.value.trim().length >= 3) {
            performSearch();
        }
    });

    // Кнопка сброса фильтров
    resetFiltersBtn.addEventListener('click', function () {
        recipeTypeFilter.value = '';
        dietFilter.value = '';
        if (searchInput.value.trim().length >= 3) {
            performSearch();
        }
    });
});
