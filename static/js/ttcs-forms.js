(function () {
    function bindTtcsForms() {
        document.querySelectorAll('form.ttcs-form').forEach(function (form) {
            if (form.dataset.ttcsBound === 'true') {
                return;
            }
            form.dataset.ttcsBound = 'true';

            var submitBtn = form.querySelector('[type="submit"]');
            form.addEventListener('submit', function () {
                if (!submitBtn || submitBtn.disabled) {
                    return;
                }
                submitBtn.disabled = true;
                var icon = submitBtn.querySelector('i');
                if (icon) {
                    icon.className = 'bi bi-hourglass-split me-2';
                }
                var label = submitBtn.getAttribute('data-loading-text') || 'Sending...';
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>' + label;
            });

            form.querySelectorAll('[data-char-count]').forEach(function (field) {
                var counterId = field.getAttribute('data-char-count');
                var counter = document.getElementById(counterId);
                if (!counter) {
                    return;
                }
                function updateCount() {
                    counter.textContent = field.value.length;
                }
                field.addEventListener('input', updateCount);
                updateCount();
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindTtcsForms);
    } else {
        bindTtcsForms();
    }
})();
