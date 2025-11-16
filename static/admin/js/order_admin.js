(function($) {
    'use strict';
    
    // Функция для получения цены товара
    function getProductPrice(productId, priceField) {
        if (!productId) {
            return;
        }
        
        $.ajax({
            url: '/orders/admin/get-product-price/' + productId + '/',
            method: 'GET',
            success: function(data) {
                if (data.success) {
                    priceField.val(data.price);
                    calculateTotal();
                }
            },
            error: function() {
                console.error('Ошибка при получении цены товара');
            }
        });
    }
    
    // Функция расчета общей суммы
    function calculateTotal() {
        let total = 0;
        
        // Проходим по всем строкам inline формы (TabularInline)
        $('.inline-group tbody tr').each(function() {
            const $row = $(this);
            const quantityField = $row.find('input[name*="-quantity"]');
            const priceField = $row.find('input[name*="-price"]');
            
            if (quantityField.length && priceField.length && !$row.hasClass('empty-form')) {
                const quantity = parseFloat(quantityField.val()) || 0;
                const price = parseFloat(priceField.val()) || 0;
                total += quantity * price;
            }
        });
        
        // Обновляем отображение суммы
        let $totalDisplay = $('#order-total-display');
        if ($totalDisplay.length === 0) {
            // Создаем элемент для отображения суммы, если его нет
            $totalDisplay = $('<div id="order-total-display" style="padding: 10px; background: #f0f0f0; margin: 10px 0; font-weight: bold; font-size: 16px; border: 1px solid #ddd; border-radius: 4px;"></div>');
            $('.inline-group').after($totalDisplay);
        }
        $totalDisplay.html('Общая сумма заказа: <span style="color: #417690;">' + total.toFixed(2) + ' руб.</span>');
    }
    
    // Инициализация при загрузке страницы
    $(document).ready(function() {
        // Обработчик изменения товара в inline форме
        $(document).on('change', 'select[name*="-product"]', function() {
            const $row = $(this).closest('tr, .form-row, .inline-related');
            const productId = $(this).val();
            const priceField = $row.find('input[name*="-price"]');
            
            if (productId && priceField.length) {
                getProductPrice(productId, priceField);
            }
        });
        
        // Обработчик изменения количества или цены
        $(document).on('input change', 'input[name*="-quantity"], input[name*="-price"]', function() {
            calculateTotal();
        });
        
        // Обработчик удаления строки
        $(document).on('click', '.inline-group .delete input', function() {
            setTimeout(calculateTotal, 100);
        });
        
        // Первоначальный расчет суммы
        setTimeout(calculateTotal, 500);
    });
    
    // Обработка динамически добавляемых строк (для Django admin inline forms)
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function(event, $row) {
            const productSelect = $row.find('select[name*="-product"]');
            const priceField = $row.find('input[name*="-price"]');
            
            if (productSelect.length && priceField.length) {
                productSelect.on('change', function() {
                    const productId = $(this).val();
                    if (productId) {
                        getProductPrice(productId, priceField);
                    }
                });
                
                priceField.on('input change', calculateTotal);
            }
            
            setTimeout(calculateTotal, 100);
        });
        
        django.jQuery(document).on('formset:removed', function(event, $row) {
            setTimeout(calculateTotal, 100);
        });
    }
    
})(django.jQuery || jQuery);

