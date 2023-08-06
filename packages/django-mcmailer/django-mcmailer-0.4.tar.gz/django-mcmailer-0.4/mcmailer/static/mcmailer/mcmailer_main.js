window.onload = function () {
    if (typeof (django) !== 'undefined' && typeof (django.jQuery) !== 'undefined') {
        (function ($) {
            let content = $('#id_html_body'),
                html_body_textarea = document.getElementById('id_html_body');
            html_body_textarea.onkeyup = function () {
                let html_preview = document.getElementById('html_preview');
                if (html_preview) {
                    html_preview.innerHTML = this.value;
                }
            }
            content.trigger('keyup');
        }(django.jQuery));
    }
};