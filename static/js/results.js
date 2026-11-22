// Render hasil dari sessionStorage ke results.html
document.addEventListener("DOMContentLoaded", () => {
    const raw = sessionStorage.getItem("kindred_result");
    if (!raw) return;
    const result = JSON.parse(raw);

    // Tampilkan inferred classes
    const inferredEl = document.getElementById("inferredClasses");
    if (inferredEl) {
        inferredEl.innerHTML = result.inferred_classes
            .map((c) => `<span class="pill mint">${c}</span>`)
            .join(" ");
    }

    // Tampilkan skor urgensi
    const scoreEl = document.getElementById("urgencyScore");
    if (scoreEl) scoreEl.textContent = `${result.overall_urgency}/100`;

    // Tampilkan red flag alert
    if (result.is_red_flag_case) {
        const alert = document.getElementById("redFlagAlert");
        if (alert) alert.style.display = "block";
    }

    // Render related conditions
    const listEl = document.getElementById("relatedConditions");
    if (listEl) {
        listEl.innerHTML = result.related_conditions.map((c, i) => `
      <article class="candidate-card">
        <div class="candidate-top">
          <div>
            <span class="pill">Kandidat ${String(i + 1).padStart(2, "0")}</span>
            <h3>${c.label}</h3>
          </div>
          <span class="pill mint">Skor ${c.urgency_score}</span>
        </div>
        <div class="evidence">
          ${c.matched_core.map((s) => `<span>Sign ${s}</span>`).join(" ")}
        </div>
        <details>
          <summary>Kenapa topik ini muncul?</summary>
          <p>Ontology memiliki relasi core sign antara kondisi ini dengan ${c.matched_core.join(", ")}. Match ratio: ${(c.ratio * 100).toFixed(0)}%.</p>
        </details>
      </article>
    `).join("");
    }

    // Rekomendasi
    document.getElementById("recAssessments").innerHTML =
        result.recommended_assessments.map((a) => `<li>${a}</li>`).join("");
    document.getElementById("recProfessionals").innerHTML =
        result.recommended_professionals.map((p) => `<li>${p}</li>`).join("");
    document.getElementById("recTherapies").innerHTML =
        result.recommended_therapies.map((t) => `<li>${t}</li>`).join("");
});