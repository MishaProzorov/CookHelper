// Загрузка отзывов при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadReviews();
});

async function loadReviews() {
    try {
        const response = await fetch('/api/reviews');
        const reviews = await response.json();

        const container = document.getElementById('reviewsContainer');
        container.innerHTML = '';

        if (reviews.length === 0) {
            container.innerHTML = '<p class="text-muted">Пока нет отзывов. Будьте первым!</p>';
            return;
        }

        reviews.forEach(review => {
            const reviewCard = createReviewCard(review);
            container.appendChild(reviewCard);
        });
    } catch (error) {
        console.error('Ошибка загрузки отзывов:', error);
    }
}

function createReviewCard(review) {
    const col = document.createElement('div');
    col.className = 'col-md-12 mb-3';

    const stars = '⭐'.repeat(review.rating);
    const date = new Date(review.created_at).toLocaleDateString('ru-RU');

    col.innerHTML = `
        <div class="card">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="mb-0">${review.author_gmail}</h6>
                    <small class="text-muted">${date}</small>
                </div>
                <div class="mb-2">${stars}</div>
                <p class="card-text">${review.text}</p>
            </div>
        </div>
    `;

    return col;
}

// Обработка отправки формы
document.getElementById('reviewForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch('/api/reviews', {
            method: 'POST',
            credentials: 'include',
            body: formData
        });

        if (response.ok) {
            this.reset();
            loadReviews();
        } else {
            const error = await response.json();
            alert('Ошибка: ' + error.detail);
        }
    } catch (error) {
        alert('Произошла ошибка при отправке отзыва');
        console.error(error);
    }
});
