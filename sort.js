let sortDirection = {};  // tracks sorting direction
let initialRows = [];    // store initial table order

document.addEventListener("DOMContentLoaded", () => {
    // Store the original order
    const tbody = document.querySelector("#leaderboard tbody");
    initialRows = Array.from(tbody.rows);
});

function sortTable(colIndex){
    const table = document.getElementById("leaderboard");
    const tbody = table.tBodies[0];

    // If Weeks Won column is clicked (index 2), reset to original order
    if(colIndex === 2){
        initialRows.forEach(row => tbody.appendChild(row));
        updateRanks();
        updateArrows(null); // remove arrows
        return;
    }

    // Toggle sort direction for other columns
    sortDirection[colIndex] = !sortDirection[colIndex];

    const rows = Array.from(tbody.rows);

    rows.sort((a, b) => {
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

function updateRanks(){
    const rows = document.querySelectorAll("#leaderboard tbody tr");
    rows.forEach((row, i) => {
        const rankCell = row.cells[0];
        rankCell.innerText = i + 1;

        row.classList.remove("rank1","rank2","rank3");
        if(i===0) row.classList.add("rank1");
        if(i===1) row.classList.add("rank2");
        if(i===2) row.classList.add("rank3");
    });
}

function updateArrows(activeCol){
    const arrows = document.querySelectorAll(".sort-arrow");
    arrows.forEach(a => a.innerText = "▲▼");
    if(activeCol === null) return; // nothing active
    const header = document.querySelectorAll("#leaderboard th")[activeCol];
    const arrow = header.querySelector(".sort-arrow");
    if(arrow){
        arrow.innerText = sortDirection[activeCol] ? "▲" : "▼";
    }
}