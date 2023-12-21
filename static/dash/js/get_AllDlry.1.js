function get_AllDlry() {
    ds_tbl = document.getElementById('ds_tbl');
    ds_tbl.innerHTML = '';
    $.ajax({
        type: "GET",
        url: deliverymanurl,

        success: function(data) {
            console.log(data);
            for (var i = 0; i < data.length; i++) {
                lst = '';
                for (var m = 0; m < data[i].lst.length; m++) {
                    htl = '<li>' + data[i].lst[m].area.area + '</li>';
                    lst += htl;
                }
                html = '<tr><td>' + data[i].name + '</td><td>' + data[i].phone + '</td><td><ol>' + lst + '</ol></td><td><div class="col-md-12"><select class="form-control" id="slArea' + data[i].id + '"> <option>Select Area</option></select></div></td><td><button type="button" class="btn btn-warning btn-rounded btn-fw" style="color: #ffffff;" onclick="DlryUpd(' + data[i].id + ')">Update Area</button></td><td><button type="button" class="btn btn-danger btn-rounded btn-fw" onclick="rmoveDlry(' + data[i].id + ')" style="color: #ffffff;">Remove</button></td></tr>';

                ds_tbl.innerHTML += html;
                getLSTDL(data[i].id);
            }
        },
        error: function(data) {
            window.alert(
                data.responseJSON.message);
        }
    });
}