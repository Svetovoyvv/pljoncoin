window.addEventListener('load', function (){

    let e = document.getElementById('popup');
    document.querySelector("body > section.section-main > header > ul > li.account > a.auth").addEventListener(
        'click',
        function (){
            e.classList.toggle('hide-popup');
        }
    );
    e.addEventListener(
        'click',
        function (event){
            if (!event.target.classList.contains('popup-bg') && !event.target.classList.contains('popup-parent')) return;
            e.classList.toggle('hide-popup', true);
        }
    );
    if (window.location.hash === '#login'){
        e.classList.toggle('hide-popup');
    }
});
$(function(){
    $('#login_btn').on('click', function (e){
        e.preventDefault();
        let form = $('#login_form');
        let fls = form.find('input');
        for (let el of fls){
            console.log(el)
            if (el.tagName.toUpperCase() !== 'BUTTON' && el.value === '' || !el.checkValidity())
                return el.reportValidity();
        }


        $.ajax('/api/auth/login', {
            method: 'POST',
            data: JSON.stringify({
                email: fls[0].value,
                password: fls[1].value,
            }),
            contentType: 'application/json',
            crossDomain: true,
            success: function (data){
                document.cookie = 'token=' + encodeURI(data.token);
                window.location.href = '/';
            },
            statusCode:{
                400: function (){
                    alert('Неверный логин или пароль');
                }
            }
        })

    })

})
$(function(){
    $('#search_button').click(function(){
        let search = $('#search_text').val();
        window.location.href = `/search/${search}`;
    })
})
