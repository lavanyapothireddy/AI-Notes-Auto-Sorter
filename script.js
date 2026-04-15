async function sortNotes() {
    let notes = document.getElementById("notes").value
        .split("\n")
        .map(n => n.trim())
        .filter(n => n !== "");

    document.getElementById("loading").classList.remove("hidden");
    document.getElementById("output").innerHTML = "";

    try {
        let res = await fetch("/sort-notes", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ notes })
        });

        let data = await res.json();

        document.getElementById("loading").classList.add("hidden");

        display(data.sorted_notes);

    } catch (e) {
        document.getElementById("output").innerText = "Error: " + e;
    }
}

function display(data) {
    let output = document.getElementById("output");

    for (let cat in data) {
        let div = document.createElement("div");
        div.className = "category";

        div.innerHTML = `<h3>📌 ${cat}</h3>`;

        data[cat].forEach(n => {
            div.innerHTML += `<p>• ${n}</p>`;
        });

        output.appendChild(div);
    }
}

function loadExample() {
    document.getElementById("notes").value =
`iot sensors and actuators
esp32 microcontroller
binary tree traversal
quick sort algorithm`;
}

function downloadJSON() {
    let text = document.getElementById("output").innerText;
    let blob = new Blob([text], {type: "application/json"});
    let a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "notes.json";
    a.click();
}