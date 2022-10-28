$(function(){
    $('#input_search').on('input', function(e){
        let value = e.target.value.toLowerCase();
        for (let el of $('.table_row')){
            $(el).toggle(el.children[0].innerText.toLowerCase().includes(value) || el.children[1].innerText.toLowerCase().includes(value));
        }
    });
    $('.history_button').click(function(e){
        e.preventDefault();
        window.location.href = e.target.getAttribute('link');
    });
});