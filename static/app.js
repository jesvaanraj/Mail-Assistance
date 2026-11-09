const $ = (id) => document.getElementById(id);
let reportText = "";
let reportName = "symptom_report";

function fillList(id, items) {
  const el = $(id);
  el.innerHTML = "";
  (items && items.length ? items : ["Not specified"]).forEach((t) => {
    const li = document.createElement("li");
    li.textContent = t; // textContent avoids HTML injection from model output
    el.appendChild(li);
  });
}

function showResult(r) {
  const risk = $("risk");
  risk.className = "risk " + r.risk_level;
  risk.textContent = r.risk_label;
  if (r.risk_reason) {
    const s = document.createElement("small");
    s.textContent = r.risk_reason;
    risk.appendChild(s);
  }

  fillList("symptomsList", r.reported_symptoms);
  $("durationOut").textContent = r.duration || r.profile.duration;

  const conds = $("conditionsList");
  conds.innerHTML = "";
  (r.possible_conditions || []).forEach((c) => {
    const li = document.createElement("li");
    const b = document.createElement("strong");
    b.textContent = c.name;
    const tag = document.createElement("span");
    tag.className = "cond-tag";
    tag.textContent = c.likelihood || "";
    li.append(b, tag, document.createTextNode(" – " + (c.reason || "")));
    conds.appendChild(li);
  });

  $("why").textContent = r.why_considered || "";
  fillList("followList", r.follow_up_questions);
  fillList("careList", r.self_care);
  $("attention").textContent = r.medical_attention || "";
  $("disclaimer").textContent = r.disclaimer;

  reportText = r.report_text;
  reportName = r.report_id || reportName;
  $("result").classList.remove("hidden");
  $("result").scrollIntoView({ behavior: "smooth" });
}

$("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  $("error").classList.add("hidden");
  $("result").classList.add("hidden");
  $("loading").classList.remove("hidden");
  $("submit").disabled = true;

  const body = {};
  ["age", "sex", "severity", "symptoms", "duration", "conditions", "medications", "allergies"]
    .forEach((k) => (body[k] = $(k).value));

  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    showResult(data);
  } catch (err) {
    $("error").textContent = err.message;
    $("error").classList.remove("hidden");
  } finally {
    $("loading").classList.add("hidden");
    $("submit").disabled = false;
  }
});

$("download").addEventListener("click", () => {
  const blob = new Blob([reportText], { type: "text/plain" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = reportName + ".txt";
  a.click();
  URL.revokeObjectURL(a.href);
});
