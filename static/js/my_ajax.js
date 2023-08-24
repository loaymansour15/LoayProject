
// update archive button title
function archive_func(post_id, post_type){
    
    $.ajax({
        url: '/archive/',
        type: 'GET',
        data: { "post_id": JSON.stringify(post_id), 'post_type': JSON.stringify(post_type) },
        dataType: 'json',

        success: function (data) {
            if (data.result == true){
                $("#archiveB").text("تمت الإضافه للأرشيف");
                $('#archiveB').removeClass('btn btn-outline-secondary btn-block');
                $('#archiveB').addClass('btn btn-outline-success btn-block');
            } else {
                $("#archiveB").text("أضف إلي الأرشيف؟");
                $('#archiveB').removeClass('btn btn-outline-success btn-block');
                $('#archiveB').addClass('btn btn-outline-secondary btn-block');
            }
            
        }
    });
}



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
