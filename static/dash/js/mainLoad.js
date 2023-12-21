function mainLoad() {
    const uname = getCookie("UIDN");
    const upic = getCookie("UIDP");
    pname = document.getElementById("prfpic");
    gname = document.getElementById("wname");
    gname.innerHTML = uname;


}