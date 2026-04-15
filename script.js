async function sortNotes() {
    let notes = document.getElementById("notes").value
        .split("\n")
        .map(n => n.trim())
        .filter(n => n !== "");

    let loading = document.getElementById("loading");
    let output = document.getElementById("output");

    loading.classList.remove("hidden");
    loading.innerText = "⏳ Processing...";
    output.innerHTML = "";

    // 🔥 Message after delay (Render wake-up)
    let delayMsg = setTimeout(() => {
        loading.innerText = "⏳ First request may take 1-2 minutes...";
    }, 5000);

    try {
        let res = await fetch("https://ai-notes-auto-sorter.onrender.com/sort-notes", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ notes })
        });

        // ❌ Handle bad response
        if (!res.ok) {
            throw new Error("Server error: " + res.status);
        }

        let text = await res.text();

        // ❌ Handle empty response
        if (!text) {
            throw new Error("Empty response from server");
        }

        let data = JSON.parse(text);

        clearTimeout(delayMsg);
        loading.classList.add("hidden");

        if (data.sorted_notes) {
            display(data.sorted_notes);
        } else {
            output.innerText = "No data received";
        }

    } catch (e) {
        clearTimeout(delayMsg);
        loading.classList.add("hidden");
        output.innerText = "❌ Error: " + e.message;
    }
}
