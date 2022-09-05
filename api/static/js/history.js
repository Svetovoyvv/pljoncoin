$(function(){
    $('.repeat_search').click(function(e){
        e.preventDefault();
        let bc_id = e.target.getAttribute('block-id');
        window.location.href = `/search/${bc_id}`;
    });
})

window.addEventListener('load', function (){
    //popup
    let a = document.getElementById('popup');
    let b = document.getElementById('popup_data')
    document.querySelector(".summa").addEventListener(
        'click',
        function (){
            a.classList.toggle('hide-popup');
            b.classList.add('hide-popup-d');
        }
    );
    a.addEventListener(
        'click',
        function (event){
            if (!event.target.classList.contains('popup-bg')) return;
            a.classList.toggle('hide-popup', true);
            b.classList.add('hide-popup-d',true);
        }
    );

    document.querySelector(".date").addEventListener(
        'click',
        function (){
            b.classList.toggle('hide-popup-d');
            a.classList.add('hide-popup');
        }
    );
    b.addEventListener(
        'click',
        function (event){
            if (!event.target.classList.contains('popup-bg-d')) return;
            b.classList.toggle('hide-popup-d', true);
            a.classList.add('hide-popup',true);
        }
    );



   //calendar

   const firstDate = new Date();
        const secondDate = new Date(Date.now() + 1000000000);
        const calendar = new dhx.Calendar("calendar", {
            css: "dhx_widget--bordered",
            range: true,
            value: [firstDate, secondDate]
    });

   //buttons
   document.querySelector("#date_delete").addEventListener(
    'click',
        function (){
            calendar.clear();
    });
    document.querySelector("#date_submit").addEventListener(
        'click',
            function (){
                b.classList.toggle('hide-popup-d');
    });
    document.querySelector("#submit_summa").addEventListener(
        'click',
            function (){
                a.classList.toggle('hide-popup');
    });
  
});

