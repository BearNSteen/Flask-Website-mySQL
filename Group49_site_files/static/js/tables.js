function view(num) {
    const bod = document.getElementById('cvers').children
    for (let j = 0; j < bod.length; j++){
        bod[j].style.display = "none"
    }
    let r_num = num.toString();
    let row = "game" + r_num;
    const area = document.getElementsByClassName(row);
    for (let i=0; i < area.length; i++) {
        area[i].style.display = "table-row";
    }
}

function show(num) {
    const body = document.getElementById('gamerents').children
    for (let j = 0; j < body.length; j++){
        body[j].style.display = "none"
    }
    let int = num.toString();
    let row_class = "rent" + int;
    const to_show = document.getElementsByClassName(row_class);
    for (let i=0; i < to_show.length; i++) {
        to_show[i].style.display = "table-row";
    }
}