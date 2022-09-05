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
function updateTableSorting(){
    let rt = $('#result_table');
    let data = [...rt.children().toArray()];
    data.sort((a, b) => b.cells.length - a.cells.length);
    rt.empty()
    data.forEach(e => rt.append(e));
}
// Init
$(function (){
    function loadTransaction(hash){
        $.ajax({
            url: `https://chain.so/api/v2/get_tx/BTC/${hash}`,
            type: "GET",
            crossDomain: true,
            success: function (data){
                if (data?.status === 'success'){
                    console.log([data.data.outputs.length, data.data.inputs.length, Math.max(data.data.outputs.length, data.data.inputs.length)])
                    $('#result_table').append(`
                        <tr>
                            <td>${data.data.txid}</td>
                            <td>${[...new Set(data.data.inputs.map(e => e.address))].join('<br>')}</td>
                            <td>${[...new Set(data.data.outputs.map(e => e.address))].join('<br>')}</td>
                            <td>BTC</td>
                            <td>${data.data.inputs.map(e => parseFloat(e.value)).reduce((a, b) => a+b, 0).toFixed(2)}</td>
                            <td>${Math.max(data.data.outputs.length, data.data.inputs.length)}</td>
                        </tr>`
                    )
                    updateTableSorting();
                }
            },
            error: function (data){
                $('#result_table').append(`<tr><td>Не удалось загрузить транзакцию</td></tr>`)
                updateTableSorting();
            }
        });
    }
    $.ajax({
        url: `/api/btc/get/${searchBlockId}`,
        type: 'GET',
        success: function (data){
            for (let tx_hash of data){
                loadTransaction(tx_hash);
            }
        },
        error: function (data){

        }
    });
})