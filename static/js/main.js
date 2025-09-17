// Основной JavaScript файл

document.addEventListener('DOMContentLoaded', function() {
    // Обработка форм авторизации и регистрации
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit(this, '/auth/login/');
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleFormSubmit(this, '/auth/register/');
        });
    }
    
    // Обработка добавления в корзину
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const quantity = this.dataset.quantity || 1;
            addToCart(productId, quantity);
        });
    });
    
    // Обработка обновления количества в корзине
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const cartItemId = this.dataset.cartItemId;
            const quantity = this.value;
            updateCartItem(cartItemId, quantity);
        });
    });
    
    // Обработка удаления из корзины
    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
    removeFromCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const cartItemId = this.dataset.cartItemId;
            removeFromCart(cartItemId);
        });
    });
});

// Функция обработки отправки форм
function handleFormSubmit(form, url) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    
    // Показываем загрузку
    submitButton.disabled = true;
    submitButton.textContent = 'Загрузка...';
    
    // Очищаем предыдущие ошибки
    clearFormErrors(form);
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Закрываем модальное окно
            const modal = form.closest('.modal');
            if (modal) {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                modalInstance.hide();
            }
            // Перезагружаем страницу
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showFormErrors(form, data.errors);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Произошла ошибка при отправке формы');
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.textContent = originalText;
    });
}

// Функция добавления товара в корзину
function addToCart(productId, quantity) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    
    fetch(`/orders/add-to-cart/${productId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Обновляем счетчик корзины если есть
            updateCartCounter();
        } else {
            showAlert('danger', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Произошла ошибка при добавлении товара в корзину');
    });
}

// Функция обновления количества товара в корзине
function updateCartItem(cartItemId, quantity) {
    const formData = new FormData();
    formData.append('quantity', quantity);
    
    fetch(`/orders/update-cart/${cartItemId}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Перезагружаем страницу для обновления общей суммы
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('danger', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Произошла ошибка при обновлении корзины');
    });
}

// Функция удаления товара из корзины
function removeFromCart(cartItemId) {
    if (!confirm('Вы уверены, что хотите удалить этот товар из корзины?')) {
        return;
    }
    
    fetch(`/orders/remove-from-cart/${cartItemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('success', data.message);
            // Удаляем элемент из DOM
            const cartItem = document.querySelector(`[data-cart-item-id="${cartItemId}"]`);
            if (cartItem) {
                cartItem.remove();
            }
            // Перезагружаем страницу для обновления общей суммы
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showAlert('danger', data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', 'Произошла ошибка при удалении товара из корзины');
    });
}

// Функция отображения ошибок формы
function showFormErrors(form, errors) {
    Object.keys(errors).forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        const errorElement = form.querySelector(`#${fieldName}_error`);
        
        if (field && errorElement) {
            field.classList.add('is-invalid');
            errorElement.textContent = errors[fieldName];
        }
    });
}

// Функция очистки ошибок формы
function clearFormErrors(form) {
    const invalidFields = form.querySelectorAll('.is-invalid');
    const errorElements = form.querySelectorAll('.invalid-feedback');
    
    invalidFields.forEach(field => {
        field.classList.remove('is-invalid');
    });
    
    errorElements.forEach(element => {
        element.textContent = '';
    });
}

// Функция отображения уведомлений
function showAlert(type, message) {
    const alertContainer = document.querySelector('.container.mt-3') || createAlertContainer();
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // Автоматически скрываем уведомление через 5 секунд
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Функция создания контейнера для уведомлений
function createAlertContainer() {
    const container = document.createElement('div');
    container.className = 'container mt-3';
    document.querySelector('main').insertBefore(container, document.querySelector('main').firstChild);
    return container;
}

// Функция получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция обновления счетчика корзины
function updateCartCounter() {
    // Здесь можно добавить логику обновления счетчика корзины
    // Например, через AJAX запрос для получения количества товаров в корзине
}

