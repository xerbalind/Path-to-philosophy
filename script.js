function voegToe(begin, eind) {
    fetch(`cgi-bin/voeg_toe.cgi?begin=${begin}&eind=${eind}`)
        .then(antwoord => antwoord.json())
        .then(data => {
            console.log(data);
            let html = "";
            for (let item of data["path"]) {
                html += `<li>${item}</li>`;
            }
            document.querySelector("#items").innerHTML = html;
        });
}

document.querySelector("#toevoegKnop").addEventListener("click", () => {
    const begin = document.querySelector("#start_veld").value;
    const eind = document.querySelector("#stop_veld").value;
    voegToe(begin, eind);
});
