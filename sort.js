let sortDirection = {};

function sortTable(colIndex){

    const table = document.getElementById("leaderboard");
    const headers = table.querySelectorAll("th");
    const arrows = table.querySelectorAll(".sort-arrow");

    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    sortDirection[colIndex] = !sortDirection[colIndex];

    rows.sort((a,b)=>{

        let A = a.cells[colIndex].innerText;
        let B = b.cells[colIndex].innerText;

        if(!isNaN(A) && !isNaN(B)){
            A = Number(A);
            B = Number(B);
        }

        if(A < B) return sortDirection[colIndex] ? -1 : 1;
        if(A > B) return sortDirection[colIndex] ? 1 : -1;
        return 0;
    });

    rows.forEach(row => tbody.appendChild(row));

    updateRanks();
    updateArrows(colIndex);
}

function updateArrows(activeCol){

    document.querySelectorAll(".sort-arrow").forEach(a=>{
        a.innerText = "▲▼";
    });

    const header = document.querySelectorAll("#leaderboard th")[activeCol];
    const arrow = header.querySelector(".sort-arrow");

    if(!arrow) return;

    arrow.innerText = sortDirection[activeCol] ? "▲" : "▼";
}

function updateRanks(){

    const table = document.getElementById("leaderboard");
    const rows = table.tBodies[0].rows;

    for(let i=0;i<rows.length;i++){

        const rankCell = rows[i].cells[0];
        rankCell.innerText = i + 1;

        rows[i].classList.remove("rank1","rank2","rank3");

        if(i===0) rows[i].classList.add("rank1");
        if(i===1) rows[i].classList.add("rank2");
        if(i===2) rows[i].classList.add("rank3");
    }
}