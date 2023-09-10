/*
counter = 1
function addVariableFieldsProduct(){
    
    var okay = false;
    if(counter<5){
        counter+=1;
        html = '<div id="div_id_variant'+counter+'" class="form-group"> \
        <label for="id_variant'+counter+'" class="">نوع المتغير '+counter+'\
        </label> <div> \
        <select name="variant'+counter+'" class="select form-control" id="id_variant'+counter+'"> \
        <option value="" selected="">---------</option> \
        </select> </div> </div>\
        <div id="div_id_variant_option'+counter+'" class="form-group"> \
        <label for="id_variant_option'+counter+'" class=""> إضافة إسم متغير '+counter+'\
        </label> <div> \
        <input type="text" name="variant_option'+counter+'" placeholder="مثال: لو لون (احمر ، ازرق، الخ... ) " maxlength="100" class="textinput textInput form-control" id="id_variant_option'+counter+'">\
         </div> </div>'

        //var product_form = document.getElementById('addProd');
        $("#addProdButton").before(html);
        okay = true;
    }
    else{
        alert("وصلت الي الحد الأقصي لخانات المتغيرات")
    }

    return okay;
    
}

function removeVariableFieldsProduct(){
    if(counter > 1){
        document.getElementById('div_id_variant'+counter+'').remove();
        document.getElementById('div_id_variant_option'+counter+'').remove();
        counter-=1
    }
    else{
        alert("لا يوجد خانات لحذفها")
    }
}
*/

// add product unit
$(document).ready(function(){

    $('#loading').hide()
    $('#showShippingCost').hide()

     /*
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
                    $('#id_variant1').append($(option1));
                    $('#id_variant2').append($(option2));
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
                    //var id_prod_variant = $("#id_prod_variant").val();
                    //var id_variant = $("#id_variant").val();
                    //if (id_prod_variant == id_variant){
                      //  var option3 = new Option(data.option_text, data.option_value);
                        //$('#id_variant_option').append($(option3));
                    //}
                    setTimeout(function(){
                        location.reload(true);
                    }, 1000);
                    
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
    */

    /*
    var all_variants = $('#addVariant');
    all_variants.click(function(){
        $.ajax({
            type: 'GET',
            url: "/myclient/get_variants/",
            //data: all_variants.serialize(),
            success: function (data) {
                //variants
                var okay = addVariableFieldsProduct()
                if (okay == true){
                    var arr = data.variants;
                    for(var i=0; i< arr.length; i++){
                        //alert(arr[i][0]);
                        var o = new Option(arr[i][1], arr[i][0]);
                        $(o).html(arr[i][1]);
                        $('#id_variant'+counter+'').append(o);
                    }   
                }
                
            },
            error: function(data) {
                alert("Something went wrong!");
            }
        });
        return false;
    });
    */


    var prod_droplist = $('#id_product')
    prod_droplist.on('change', function() {
        $.ajax({
            type: 'GET',
            url: "/myclient/get_product_data/",
            data: {'prod_id':JSON.stringify(prod_droplist.val())},
            success: function (data) { 
                result = data.result[0]
                $('#id_unit').val(result[0]).change()
                $('#id_quantity').val(result[1])
                $('#id_cost').val(result[2])
                $('#id_price').val(result[3])
                $('#id_discount').val(result[4])
                $('#id_variant1').val(result[5]).change()

                $('#id_variant_option1').val(result[6]).change()

                $('#id_variant2').val(result[7]).change()

                $('#id_variant_option2').val(result[8]).change()
            },
            error: function(data) {
                
            }
        });

        return false;
    });


    var courier_name, state_name;
    var courier = $('#id_courier')
    courier.on('change', function(){
        courier_name = document.getElementById("id_courier").value;
        state_name = document.getElementById("id_state").value;
        if(courier_name && state_name){
            getCourierShippingCost(courier_name, state_name)
        }
    });

    var state = $('#id_state')
    state.on('change', function(){
        courier_name = document.getElementById("id_courier").value;
        state_name = document.getElementById("id_state").value;
        if(courier_name && state_name){
            getCourierShippingCost(courier_name, state_name)
        }
    });
    

});

function getCourierShippingCost(courier, state){
    $.ajax({
        type: 'GET',
        url: "/myclient/get_courier_shipping_cost/",
        data: {'courier':JSON.stringify(courier), 'state':JSON.stringify(state)},
        success: function (data) { 
            $('#showShippingCost').show()
            $('#showShippingCost').text('')
            $('#showShippingCost').append(data.result)
        },
        error: function(data) {
            
        }
    });
}


function showloading(){
    $('#loading').show();
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

/*


*/