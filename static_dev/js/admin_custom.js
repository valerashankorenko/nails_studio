document.addEventListener('DOMContentLoaded', function() {
    const serviceTypeSelect = document.getElementById('id_service_type');
    const serviceSelect = document.getElementById('id_service');

    if (serviceTypeSelect) {
        serviceTypeSelect.addEventListener('change', function() {
            const serviceType = this.value;
            const url = new URL(window.location.href);
            url.searchParams.set('service_type', serviceType);
            window.location.href = url.toString();  // Перезагружаем страницу с новым параметром
        });
    }
});
