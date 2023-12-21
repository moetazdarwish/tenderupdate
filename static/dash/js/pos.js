const mainurl = 'http://127.0.0.1:8000'
const get_BrInvurl = 'http://127.0.0.1:8000/branches/get_BrInv/'
const add_CartActionurl = 'http://127.0.0.1:8000/account/add_CartAction/'
const add_Customerurl = 'http://127.0.0.1:8000/crm/add_Customer/'
const find_Customerurl = 'http://127.0.0.1:8000/crm/find_Customer/'
const get_allCustomerurl = 'http://127.0.0.1:8000/crm/get_allCustomer/'
const get_CartListurl = 'http://127.0.0.1:8000/account/get_CartList/'
const add_CartCustomerurl = 'http://127.0.0.1:8000/account/add_CartCustomer/'



function getCookie(name) {
    var cookieArr = document.cookie.split(";")
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}


//  rcep_id = getCookie("RPID")

function get_selgProduct() {
    lst = document.getElementById('po_lst')
    dm_tbl = document.getElementById('dm_tbl')
    lst.innerHTML = ''

    dm_tbl.innerHTML = ''

    $.ajax({
        type: "GET",
        url: get_BrInvurl,

        success: function(data) {
            console.log(data)
            for (var i = 0; i < data.length; i++) {
                html = '<div class="col-md-4"><div class="col-md-6 col-lg-12 grid-margin stretch-card"><div class="card bg-primary card-rounded"><div class="card-body pb-0"><h4 class="card-title card-title-dash text-white mb-4">' +
                    data[i].product.name + '</h4><div class="row"><div class="col-sm-6"><p class="status-summary-ight-white mb-1">' +
                    data[i].quantity.qty + '</p><h2 class="text-info">' +
                    data[i].price + '</h2></div><div class="col-sm-6 "><img class="img-xs rounded-circle float-right" src="' + mainurl + data[i].product.photo + '" alt="Profile image"></div></div><div class="row"><button type="button" class="btn btn-success btn-rounded btn-icon" onclick="addItem(' +
                    data[i].id + ')"> Add</button></div></div></div></div></div>'

                lst.innerHTML += html
            }


        },
        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}

function addItem(id) {
    $.ajax({
        type: "POST",
        url: add_CartActionurl,

        data: {
            'item_id': id
        },
        success: function(data) {
            console.log(data)


        },
        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}
// get_selgProduct()
function nSales() {
    po_lst = document.getElementById('po_lst')
    po_lst.innerHTML = ''

    html = '<div class="col-md-6"><button class="btn" style="border-color: brown;"><div class="col-md-6 col-lg-12 grid-margin stretch-card" onclick="get_selgProduct()"><div class="card bg-primary card-rounded" style="height: 150px;"><div class="card-body pb-0"><h4 class="card-title card-title-dash text-white mb-4"> </h4><div class="row"><div class=""><h1 style="color: rgb(255, 255, 255);text-align: center;">On Site</h1></div></div><div class="row"><div class="container-md"></div></div></div></div></div></button></div><div class="col-md-6"><button class="btn" style="border-color: brown;"><div class="col-md-6 col-lg-12 grid-margin stretch-card" style="height: 150px;"> <div class="card bg-primary card-rounded"> <div class="card-body pb-0"><h4 class="card-title card-title-dash text-white mb-4"> </h4><div class="row"><div class="col-sm-4"></div><div class="row" style=" align-content: center"><div class=""><h1 style="color: rgb(252, 249, 249);text-align: center;"> Delivery</h1></div></div><div class="row"><div class="container-md"> </div></div></div></div></div></div></button></div>'
    po_lst.innerHTML = html
}

function get_CartList() {
    ds_tbl = document.getElementById('dm_tbl')
    ds_tbl.innerHTML = ''

    $.ajax({
        type: "GET",
        url: get_CartListurl,


        success: function(data) {
            console.log(data)
            for (var i = 0; i < data.items.length; i++) {

                html = ' <tr><td>' + data.items[i].product.name + '</td><td>' + data.items[i].quantity + '</td><td>' + data.items[i].price + '</td><td>' + data.items[i].total.total + '</td></tr>'
                ds_tbl.innerHTML += html
            }
            htl = '<tr><td colspan="3" style="text-align: center;">Sub Total</td><td colspan="1">' + data.sub_total.sub_total + '</td></tr><tr><td colspan="3" style="text-align: center;">Items</td><td colspan="1">' + data.sub_total.items + '</td></tr><tr><td colspan="3" style="text-align: center;"> Total</td><td colspan="1">' + data.sub_total.total + '</td></tr>'
            ds_tbl.innerHTML += htl
        },

        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}

function get_CstmData() {
    dm_tbl = document.getElementById('dm_tbl')
    dm_tbl.innerHTML = ''
    html = '<tr><td>name</td><td>address</td><td><button type="button" class="btn btn-success btn-rounded btn-fw" style="color: aliceblue;">Start</button></td></tr>'
}

function add_cstomer() {
    c_nme = document.getElementById('c_nme').value
    c_phn = document.getElementById('c_phn').value
    c_add = document.getElementById('c_add').value



    $.ajax({
        type: "POST",
        url: add_Customerurl,
        data: {
            'c_nme': c_nme,
            'c_phn': c_phn,
            'c_add': c_add,
        },


        success: function(data) {
            console.log(data)

        },

        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}

function find_custmr() {
    find_Customerurl
    c_fnd = document.getElementById('c_fnd').value
    dm_tbl = document.getElementById('dm_tbl')
    dm_tbl.innerHTML = ''
    $.ajax({
        type: "POST",
        url: find_Customerurl,
        data: {
            'c_fnd': c_fnd,

        },


        success: function(data) {
            console.log(data)
            for (var i = 0; i < data.length; i++) {

                html = ' <tr><td>' + data[i].name + '</td><td>' + data[i].addres + '</td><td>' + data[i].phone + '</td><td><button type="button" class="btn btn-success btn-rounded btn-fw" style="color: aliceblue;" onclick="add_cstOrder(' + data[i].id + ')" >select</button></td></tr>'
                dm_tbl.innerHTML += html
            }

        },

        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}

function get_allCustomer() {


    dm_tbl = document.getElementById('dm_tbl')
    dm_tbl.innerHTML = ''
    $.ajax({
        type: "GET",
        url: get_allCustomerurl,



        success: function(data) {
            console.log(data)
            for (var i = 0; i < data.length; i++) {

                html = ' <tr><td>' + data[i].name + '</td><td>' + data[i].addres + '</td><td>' + data[i].phone + '</td><td><button type="button" class="btn btn-success btn-rounded btn-fw" style="color: aliceblue;" >select</button></td></tr>'
                dm_tbl.innerHTML += html
            }

        },

        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}

function cstrPg() {
    pgcg = document.getElementById('pgcg')
    pgcg.innerHTML = ''
    html = ' <div class="row" style="align-items: center" id="po_lst"><div class="col-md-6"><div class="form-group"><input type="text" class="form-control" id="c_fnd" placeholder="Search by number"></div></div><div class="col-md-3"><div class="form-group"><button type="button" class="btn btn-primary btn-rounded btn-fw" style="color: aliceblue;" onclick="find_custmr()">Find</button></div></div><div class="col-md-3"><div class="form-group"><button type="button" class="btn btn-success btn-rounded btn-fw" style="color: aliceblue;" onclick="add_cstomer()">Create</button></div></div></div><div class="table-responsive "><table class="table "><tbody id="dm_tbl"><tr><td><div class="col-sm-9"><input type="text" class="form-control" id="c_nme" placeholder="Name"></div></td><td><div class="col-sm-9"><input type="text" class="form-control" id="c_phn" placeholder="Phone"></div></td></tr><tr><td><div class="col-sm-9"><input type="text" class="form-control" id="c_add" placeholder="Address"></div></td></tr></tbody></table></div>'
    pgcg.innerHTML = html
}

function add_cstOrder(id) {

    // dm_tbl = document.getElementById('dm_tbl')
    // dm_tbl.innerHTML = ''
    $.ajax({
        type: "POST",
        url: add_CartCustomerurl,
        data: {
            'cst': id
        },

        success: function(data) {
            console.log(data)
                // for (var i = 0; i < data.length; i++) {

            //     html = ' <tr><td>' + data[i].name + '</td><td>' + data[i].addres + '</td><td>' + data[i].phone + '</td><td><button type="button" class="btn btn-success btn-rounded btn-fw" style="color: aliceblue;" >select</button></td></tr>'
            //     dm_tbl.innerHTML += html
            // }
            get_selgProduct()
        },

        error: function(data) {
            window.alert('<span class="text-white" style="font-size: 18px;">' +
                data.responseJSON.message + '</span><br><span class="text-white">For Any Issue Contact Support </span>')
        }
    });
}