
// add product unit
$(document).ready(function(){
    
    var frm = $('#addProdUnit');
    frm.submit(function () {
        $.ajax({
            type: 'POST',
            url: "/myclient/add_product_unit/",
            data: frm.serialize(),
            success: function (data) {
                alert(data.p_unit);
            },
            error: function(data) {
                alert("Something went wrong!");
            }
        });
        return false;
    });

});


// delete a row from table
function deleteTableRow(id){

    var row = document.getElementById(id);
    var table = row.parentNode;
    while ( table && table.tagName != 'TABLE' )
        table = table.parentNode;
    if ( !table )
        return;
    table.deleteRow(row.rowIndex);
}
