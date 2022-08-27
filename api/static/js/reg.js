$(function(){
    $('#reg_btn').on('click', function (e){
        e.preventDefault();
        let form = $('#reg_form');
        let fls = form.children();
        for (el of fls){
            if (el.tagName.toUpperCase() !== 'BUTTON' && el.value === '' || !el.checkValidity()){
                alert(1)
                console.log(el)
                return el.reportValidity();
            }
            if (fls[2].value !== fls[3].value)
                return alert('Пароли не совпадают');
        }
        $.ajax('/api/auth/register', {
            method: 'POST',
            data: JSON.stringify({
                username: fls[0].value,
                email: fls[1].value,
                password: fls[2].value,
            }),
            contentType: 'application/json',
            success: function (data){
                alert('Вы успешно зарегистрировались с id ' + data.id);
                window.location.href = '/#login';
            },
            statusCode: {
                400: function (){
                    alert('Пользователь с таким именем уже существует');
                }
            }
        })
    })
})