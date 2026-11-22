// Simpan pilihan area & sign ke sessionStorage, lalu pindah ke questions.html

const state = {
    age_months: 24,
    area: null,
    observed_signs: [],
    duration: "several_months",
    settings: [],
    red_flags: [],
};

// Muat sign dari API
async function loadSigns() {
    const res = await fetch("/api/signs");
    const data = await res.json();
    window.__signData = data;
    renderAreaChecklist(data);
    renderRedFlags(data.red_flags);
}

function renderAreaChecklist(data) {
    const grid = document.getElementById("signGrid");
    if (!grid) return;
    grid.innerHTML = "";
    data.areas.forEach((area) => {
        const block = document.createElement("div");
        block.className = "sign-block";
        block.innerHTML = `<h4>${area.label}</h4>`;
        area.signs.forEach((sign) => {
            const label = document.createElement("label");
            label.className = "choice";
            label.innerHTML = `
        <input type="checkbox" value="${sign.code}" data-area="${area.key}">
        <span><strong>${sign.code}</strong> ${sign.label}</span>
      `;
            block.appendChild(label);
        });
        grid.appendChild(block);
    });
    grid.addEventListener("change", updateObserved);
}

function updateObserved() {
    const checked = [...document.querySelectorAll("#signGrid input:checked")];
    state.observed_signs = checked.map((c) => c.value);
    // Set area = area pertama yang dipilih
    if (checked.length) state.area = checked[0].dataset.area;
}

function renderRedFlags(redFlags) {
    const container = document.getElementById("redFlagGrid");
    if (!container) return;
    container.innerHTML = "";
    redFlags.forEach((rf) => {
        const label = document.createElement("label");
        label.className = "choice";
        label.innerHTML = `
      <input type="checkbox" value="${rf.code}" class="red-flag-input">
      <span><strong>${rf.label}</strong><br><small>${rf.question}</small></span>
    `;
        container.appendChild(label);
    });
    container.addEventListener("change", () => {
        state.red_flags = [...container.querySelectorAll("input:checked")].map(
            (c) => c.value,
        );
    });
}

document.getElementById("continueBtn")?.addEventListener("click", async (e) => {
    e.preventDefault();
    // Ambil durasi
    const dur = document.querySelector('input[name="duration"]:checked');
    if (dur) state.duration = dur.value;
    // Ambil settings
    state.settings = [
        ...document.querySelectorAll('input[name="setting"]:checked'),
    ].map((c) => c.value);

    sessionStorage.setItem("kindred_state", JSON.stringify(state));

    // Kirim ke backend
    try {
        const res = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(state),
        });
        const result = await res.json();
        sessionStorage.setItem("kindred_result", JSON.stringify(result));
        window.location.href = "/results";
    } catch (err) {
        console.error(err);
        alert("Gagal menganalisis. Cek konsol.");
    }
});

loadSigns();
