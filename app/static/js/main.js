$('#submit-login').click(function () {
    const form = document.getElementById('sing-in-form');

    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();

        form.classList.add('was-validated');
    } else {
        form.classList.add('was-validated');
        $.ajax({
            url: '/login',
            data: $('#sing-in-form').serialize(),
            type: 'POST',
            beforeSend: async function () {
                $('.preloader').css("display", "block");
            },
            success: function (response) {
                $('.preloader').css("display", "none");
                const result = JSON.parse(response);

                if (result['status'] === 'Bad') {
                    alert(result['error']);
                } else {
                    window.location = '/';
                }

            },
            error: function (error) {
                alert(error);
            }
        });
    }
});

$('#submit-register').click(function () {
    const form = document.getElementById('register-form');

    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();

        form.classList.add('was-validated');
    } else {
        form.classList.add('was-validated');
        $.ajax({
            url: '/register',
            data: $('#register-form').serialize(),
            type: 'POST',
            beforeSend: async function () {
                $('.preloader').css("display", "block");
            },
            success: function (response) {
                $('.preloader').css("display", "none");
                const result = JSON.parse(response);

                if (result['status'] === 'Bad') {
                    alert(result['error']);
                } else {
                    window.location = '/';
                }

            },
            error: function (error) {
                alert(error);
            }
        });
    }
});

$('#block-user').click(function () {
    $.ajax({
        url: '/block_user',
        data: $('#block-form').serialize(),
        type: 'POST',
        beforeSend: async function () {
            $('.preloader').css("display", "block");
        },
        success: function (response) {
            $('.preloader').css("display", "none");
            const result = JSON.parse(response);
            if (result['status'] === 'Bad') {
                alert(result['error'])
            } else {
                location.reload();
            }

        },
        error: function (error) {
            alert(error);
        }
    });
});

$('#unblock-user').click(function () {
    $.ajax({
        url: '/unblock_user',
        data: $('#unblock-form').serialize(),
        type: 'POST',
        beforeSend: async function () {
            $('.preloader').css("display", "block");
        },
        success: function (response) {
            $('.preloader').css("display", "none");
            const result = JSON.parse(response);

            if (result['status'] === 'Bad') {
                alert(result['error'])
            } else {
                location.reload();
            }
        },
        error: function (error) {
            alert(error);
        }
    });
});

$('#button_login').click(function () {
    $('#ModalLogin').modal();
});

$(function () {
    $("img.lazy").Lazy();
});

moment.locale('ru');

function flask_moment_render(elem) {
    $(elem).text(eval('moment("' + $(elem).data('timestamp') + '").' + $(elem).data('format') + ';'));
    $(elem).removeClass('flask-moment').show();
}

function flask_moment_render_all() {
    $('.flask-moment').each(function () {
        flask_moment_render(this);
        if ($(this).data('refresh')) {
            (function (elem, interval) {
                setInterval(function () {
                    flask_moment_render(elem)
                }, interval);
            })(this, $(this).data('refresh'));
        }
    })
}

$(document).ready(function () {
    flask_moment_render_all();
});