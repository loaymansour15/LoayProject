
// add product unit
$(document).ready(function(){

    $('#message1success').hide();
    $('#message1error').hide();
    $('#message2success').hide();
    $('#message2error').hide();
    $('#message3success').hide();
    $('#message3error').hide();
    
    var frm = $('#addProdUnit');
    frm.submit(function () {
        $.ajax({
            type: 'POST',
            url: "/myclient/add_product_unit/",
            data: frm.serialize(),
            success: function (data) {
                if(data.exist == false){
                    $('#message1success').show();
                    $('#message1error').hide();
                    $('#message1success').empty();
                    $('#message1success').append(' تم إضافه الوحده  ');
                    var option = new Option(data.option_text, data.option_value);
                    $('#id_unit').append($(option));
                }  
                else{
                    $('#message1error').show();
                    $('#message1success').hide();
                    $('#message1error').empty();
                    $('#message1error').append(' تم إضافتها مسبقا  ');
                }
                    
            },
            error: function(data) {
                alert("Something went wrong!");
            }
        });
        return false;
    });

    var frm2 = $('#addProdVariant');
    frm2.submit(function () {
        $.ajax({
            type: 'POST',
            url: "/myclient/add_product_variant/",
            data: frm2.serialize(),
            success: function (data) {
                if(data.exist == false){
                    $('#message2success').show();
                    $('#message2error').hide();
                    $('#message2success').empty();
                    $('#message2success').append(' تم إضافه المتغير  ');
                    var option1 = new Option(data.option_text, data.option_value);//same option 
                    var option2 = new Option(data.option_text, data.option_value);//same option
                    $('#id_variant').append($(option1));
                    $('#id_prod_variant').append($(option2));
                }  
                else{
                    $('#message2error').show();
                    $('#message2success').hide();
                    $('#message2error').empty();
                    $('#message2error').append(' تم إضافتها مسبقا  ');
                }
                    
            },
            error: function(data) {
                alert("Something went wrong!");
            }
        });
        return false;
    });

    var frm3 = $('#addProdVarOptions');
    frm3.submit(function () {
        $.ajax({
            type: 'POST',
            url: "/myclient/add_product_variant_options/",
            data: frm3.serialize(),
            success: function (data) {
                if(data.exist == false){
                    $('#message3success').show();
                    $('#message3error').hide();
                    $('#message3success').empty();
                    $('#message3success').append(' تم إضافه إسم المتغير  ');
                    //id_prod_variant == id_variant
                    var id_prod_variant = $("#id_prod_variant").val();
                    var id_variant = $("#id_variant").val();
                    if (id_prod_variant == id_variant){
                        var option3 = new Option(data.option_text, data.option_value);
                        $('#id_variant_option').append($(option3));
                    }
                    
                }  
                else{
                    $('#message3error').show();
                    $('#message3success').hide();
                    $('#message3error').empty();
                    $('#message3error').append(' تم إضافتها مسبقا  ');
                }
                    
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
