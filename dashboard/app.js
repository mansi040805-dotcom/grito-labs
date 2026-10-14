/**
 * Grito Labs - Executive Marketing Attribution Dashboard
 * Client-Side Analytical Engine & Visualization Controller
 */

// 1. Data Store (Loaded from Processed Datasets)
const ATTRIBUTION_DATA = {
  channels: [
    "Google Search", "Meta Ads", "YouTube Ads", "Email Marketing", 
    "LinkedIn Ads", "Organic Search", "Referral & Direct"
  ],
  spend: {
    "Google Search": 82007.20,
    "Meta Ads": 85764.16,
    "YouTube Ads": 42456.05,
    "Email Marketing": 5218.13,
    "LinkedIn Ads": 47451.14,
    "Organic Search": 0.0,
    "Referral & Direct": 0.0
  },
  removal_effects: {
    "Google Search": 0.4363,
    "Meta Ads": 0.3832,
    "Email Marketing": 0.2765,
    "Organic Search": 0.2314,
    "YouTube Ads": 0.1988,
    "Referral & Direct": 0.1665,
    "LinkedIn Ads": 0.1130
  },
  models: {
    first_touch: {
      conversions: { "Google Search": 182.0, "Meta Ads": 449.0, "YouTube Ads": 317.0, "Email Marketing": 0.0, "LinkedIn Ads": 135.0, "Organic Search": 246.0, "Referral & Direct": 56.0 },
      revenue: { "Google Search": 213975.0, "Meta Ads": 524855.0, "YouTube Ads": 375012.5, "Email Marketing": 0.0, "LinkedIn Ads": 160877.5, "Organic Search": 297105.0, "Referral & Direct": 63532.5 }
    },
    last_touch: {
      conversions: { "Google Search": 496.0, "Meta Ads": 219.0, "YouTube Ads": 40.0, "Email Marketing": 302.0, "LinkedIn Ads": 17.0, "Organic Search": 127.0, "Referral & Direct": 184.0 },
      revenue: { "Google Search": 589730.0, "Meta Ads": 257402.5, "YouTube Ads": 47092.5, "Email Marketing": 356800.0, "LinkedIn Ads": 19535.0, "Organic Search": 148922.5, "Referral & Direct": 215875.0 }
    },
    linear: {
      conversions: { "Google Search": 308.0, "Meta Ads": 341.09, "YouTube Ads": 163.65, "Email Marketing": 235.67, "LinkedIn Ads": 94.72, "Organic Search": 161.51, "Referral & Direct": 80.35 },
      revenue: { "Google Search": 367230.98, "Meta Ads": 400940.75, "YouTube Ads": 191887.73, "Email Marketing": 278826.99, "LinkedIn Ads": 113143.55, "Organic Search": 190741.53, "Referral & Direct": 92585.98 }
    },
    time_decay: {
      conversions: { "Google Search": 329.97, "Meta Ads": 322.92, "YouTube Ads": 144.39, "Email Marketing": 256.35, "LinkedIn Ads": 84.86, "Organic Search": 153.19, "Referral & Direct": 93.32 },
      revenue: { "Google Search": 393927.24, "Meta Ads": 379713.78, "YouTube Ads": 168844.97, "Email Marketing": 302540.21, "LinkedIn Ads": 101715.37, "Organic Search": 180484.84, "Referral & Direct": 108131.08 }
    },
    u_shaped: {
      conversions: { "Google Search": 325.5, "Meta Ads": 336.44, "YouTube Ads": 172.07, "Email Marketing": 188.66, "LinkedIn Ads": 84.51, "Organic Search": 175.33, "Referral & Direct": 102.5 },
      revenue: { "Google Search": 386453.8, "Meta Ads": 394478.03, "YouTube Ads": 202675.6, "Email Marketing": 223546.42, "LinkedIn Ads": 100577.52, "Organic Search": 208606.12, "Referral & Direct": 119020.0 }
    },
    markov_chain: {
      conversions: { "Google Search": 334.68, "Meta Ads": 293.95, "YouTube Ads": 152.45, "Email Marketing": 212.04, "LinkedIn Ads": 86.65, "Organic Search": 177.52, "Referral & Direct": 127.73 },
      revenue: { "Google Search": 395172.44, "Meta Ads": 347084.09, "YouTube Ads": 180001.53, "Email Marketing": 250368.15, "LinkedIn Ads": 102308.5, "Organic Search": 209607.34, "Referral & Direct": 150815.44 }
    }
  }
};

const TOP_JOURNEY_PATHS = [
  { path: "Meta Ads > Email Marketing > Google Search", touches: 3, prospects: 412, conv: 148, cvr: "35.9%", rev: "$175,210" },
  { path: "YouTube Ads > Meta Ads > Email Marketing > Google Search", touches: 4, prospects: 328, conv: 122, cvr: "37.2%", rev: "$144,520" },
  { path: "Organic Search > Email Marketing > Google Search", touches: 3, prospects: 295, conv: 105, cvr: "35.6%", rev: "$124,800" },
  { path: "YouTube Ads > Email Marketing > Referral & Direct", touches: 3, prospects: 210, conv: 78, cvr: "37.1%", rev: "$92,410" },
  { path: "Meta Ads > Google Search", touches: 2, prospects: 390, conv: 92, cvr: "23.6%", rev: "$108,450" },
  { path: "Google Search (High Intent Single Touch)", touches: 1, prospects: 380, conv: 68, cvr: "17.9%", rev: "$80,520" },
  { path: "LinkedIn Ads > Google Search", touches: 2, prospects: 240, conv: 32, cvr: "13.3%", rev: "$38,010" }
];

const CAMPAIGNS_DATA = [
  { name: "Google Ads - Brand Search", spend: "$13,620", roas: "10.42x", cac: "$118.40", status: "MAINTAIN", color: "emerald" },
  { name: "Google Ads - High Intent Bootcamps", spend: "$46,416", roas: "2.47x", cac: "$472.43", status: "OPTIMIZE", color: "amber" },
  { name: "Google Ads - Conquesting", spend: "$21,971", roas: "1.92x", cac: "$595.30", status: "REDUCE", color: "rose" },
  { name: "Meta - Career Switcher Stories", spend: "$38,240", roas: "4.65x", cac: "$254.10", status: "SCALE", color: "emerald" },
  { name: "Meta - Reels RCA Capstone Demos", spend: "$27,810", roas: "3.92x", cac: "$298.50", status: "SCALE", color: "emerald" },
  { name: "Meta - Warm & Lookalike 2%", spend: "$19,714", roas: "3.12x", cac: "$360.20", status: "MAINTAIN", color: "amber" },
  { name: "YouTube - Free SQL Masterclass", spend: "$24,510", roas: "4.55x", cac: "$258.00", status: "SCALE", color: "emerald" },
  { name: "YouTube - Alumni Transformations", spend: "$17,946", roas: "3.81x", cac: "$306.40", status: "SCALE", color: "emerald" },
  { name: "Email - Live Weekend Workshop", spend: "$2,840", roas: "52.10x", cac: "$22.80", status: "SCALE", color: "emerald" },
  { name: "Email - 7-Day Curriculum Drip", spend: "$2,378", roas: "43.05x", cac: "$26.70", status: "SCALE", color: "emerald" },
  { name: "LinkedIn - Working Pro Upskill", spend: "$31,750", roas: "2.12x", cac: "$556.80", status: "REDUCE", color: "rose" },
  { name: "LinkedIn - RCA Thought Leadership", spend: "$15,701", roas: "2.24x", cac: "$528.20", status: "REDUCE", color: "rose" }
];

// 2. Budget Simulator Parameters (Calibrated Hill Curves)
const SIM_PARAMS = {
  "Google Search": { alpha: 198.5, beta: 32802.8, baseSpend: 82007.20, optSpend: 89387.85 },
  "Meta Ads": { alpha: 174.3, beta: 34305.6, baseSpend: 85764.16, optSpend: 84140.89 },
  "YouTube Ads": { alpha: 90.4, beta: 16982.4, baseSpend: 42456.05, optSpend: 53070.06 },
  "Email Marketing": { alpha: 125.7, beta: 2087.2, baseSpend: 5218.13, optSpend: 7827.20 },
  "LinkedIn Ads": { alpha: 51.4, beta: 18980.4, baseSpend: 47451.14, optSpend: 28470.68 }
};

let currentSimSpend = {};
Object.keys(SIM_PARAMS).forEach(k => currentSimSpend[k] = SIM_PARAMS[k].baseSpend);

let attributionChartInstance = null;
let currentActiveModel = "markov_chain";

// 3. Initialize Dashboard
document.addEventListener("DOMContentLoaded", () => {
  renderChart("markov_chain");
  renderRemovalEffects();
  renderJourneyPaths();
  renderCampaignsTable();
  initSimulatorSliders();
  updateSimulator();
});

// Switch Attribution Model
function switchModel(modelKey) {
  currentActiveModel = modelKey;
  document.querySelectorAll(".model-btn").forEach(btn => {
    btn.classList.remove("bg-indigo-600", "text-white");
    btn.classList.add("text-slate-400");
  });
  event.target.classList.remove("text-slate-400");
  event.target.classList.add("bg-indigo-600", "text-white");

  updateChartData(modelKey);
}

function renderChart(modelKey) {
  const ctx = document.getElementById("attributionChart").getContext("2d");
  const model = ATTRIBUTION_DATA.models[modelKey];
  const labels = ATTRIBUTION_DATA.channels;
  const convData = labels.map(ch => model.conversions[ch]);
  const revData = labels.map(ch => Math.round(model.revenue[ch] / 1000)); // in $k

  attributionChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Attributed Conversions",
          data: convData,
          backgroundColor: "rgba(99, 102, 241, 0.8)",
          borderRadius: 6,
          yAxisID: "y"
        },
        {
          label: "Attributed Revenue ($k)",
          data: revData,
          backgroundColor: "rgba(16, 185, 129, 0.8)",
          borderRadius: 6,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: "#94a3b8", font: { size: 11, family: "Plus Jakarta Sans" } }
        },
        tooltip: {
          backgroundColor: "#0f172a",
          titleColor: "#f8fafc",
          bodyColor: "#cbd5e1",
          borderColor: "#334155",
          borderWidth: 1,
          padding: 10
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#94a3b8", font: { size: 10 } }
        },
        y: {
          type: "linear",
          position: "left",
          grid: { color: "rgba(51, 65, 85, 0.3)" },
          ticks: { color: "#94a3b8", font: { size: 10 } },
          title: { display: true, text: "Conversions", color: "#6366f1", font: { size: 10 } }
        },
        y1: {
          type: "linear",
          position: "right",
          grid: { drawOnChartArea: false },
          ticks: { color: "#94a3b8", font: { size: 10 } },
          title: { display: true, text: "Revenue ($k)", color: "#10b981", font: { size: 10 } }
        }
      }
    }
  });
}

function updateChartData(modelKey) {
  const model = ATTRIBUTION_DATA.models[modelKey];
  const labels = ATTRIBUTION_DATA.channels;
  attributionChartInstance.data.datasets[0].data = labels.map(ch => model.conversions[ch]);
  attributionChartInstance.data.datasets[1].data = labels.map(ch => Math.round(model.revenue[ch] / 1000));
  attributionChartInstance.update();
}

function renderRemovalEffects() {
  const container = document.getElementById("removalEffectsContainer");
  const effects = Object.entries(ATTRIBUTION_DATA.removal_effects).sort((a, b) => b[1] - a[1]);

  container.innerHTML = effects.map(([ch, val]) => {
    const pct = (val * 100).toFixed(1);
    const color = val > 0.3 ? "bg-emerald-500" : (val > 0.18 ? "bg-indigo-500" : "bg-rose-500");
    return `
      <div>
        <div class="flex justify-between text-xs mb-1">
          <span class="text-slate-300 font-medium">${ch}</span>
          <span class="font-bold text-white font-mono">${pct}% drop</span>
        </div>
        <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
          <div class="${color} h-1.5 rounded-full transition-all duration-500" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderJourneyPaths() {
  const container = document.getElementById("journeyPathsList");
  container.innerHTML = TOP_JOURNEY_PATHS.map((item, idx) => `
    <div class="py-2.5 flex items-center justify-between">
      <div class="max-w-[70%]">
        <div class="text-xs font-semibold text-slate-200">${item.path}</div>
        <div class="text-[11px] text-slate-400 mt-0.5">${item.touches} touches · ${item.prospects} prospects · CVR: <span class="text-emerald-400 font-bold">${item.cvr}</span></div>
      </div>
      <div class="text-right">
        <div class="text-xs font-bold text-indigo-300 font-mono">${item.conv} Enrolled</div>
        <div class="text-[11px] text-slate-400 font-mono">${item.rev}</div>
      </div>
    </div>
  `).join("");
}

function renderCampaignsTable() {
  const tbody = document.getElementById("campaignTableBody");
  tbody.innerHTML = CAMPAIGNS_DATA.map(c => `
    <tr class="hover:bg-slate-800/40 transition">
      <td class="p-2 font-sans font-medium text-slate-200 text-xs">${c.name}</td>
      <td class="p-2 text-slate-300 text-xs">${c.spend}</td>
      <td class="p-2 font-bold text-slate-100 text-xs">${c.roas}</td>
      <td class="p-2 text-slate-400 text-xs">${c.cac}</td>
      <td class="p-2">
        <span class="px-1.5 py-0.5 rounded text-[10px] font-bold ${
          c.status === "SCALE" ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" :
          c.status === "MAINTAIN" ? "bg-amber-500/20 text-amber-400 border border-amber-500/30" :
          "bg-rose-500/20 text-rose-400 border border-rose-500/30"
        }">${c.status}</span>
      </td>
    </tr>
  `).join("");
}

// 4. Simulator Engine
function initSimulatorSliders() {
  const container = document.getElementById("simulatorSliders");
  container.innerHTML = Object.keys(SIM_PARAMS).map(ch => {
    const p = SIM_PARAMS[ch];
    const min = Math.round(p.baseSpend * 0.5);
    const max = Math.round(p.baseSpend * 1.5);
    return `
      <div class="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800">
        <div class="flex justify-between items-center text-xs font-semibold mb-1">
          <span class="text-slate-300">${ch}</span>
          <span class="text-indigo-400 font-mono" id="val_${cleanId(ch)}">$${Math.round(p.baseSpend).toLocaleString()}</span>
        </div>
        <input type="range" min="${min}" max="${max}" value="${p.baseSpend}" step="200" 
          oninput="handleSliderChange('${ch}', this.value)" class="w-full mt-2 cursor-pointer">
        <div class="flex justify-between text-[10px] text-slate-500 mt-1 font-mono">
          <span>-$${Math.round(p.baseSpend - min).toLocaleString()}</span>
          <span>+$${Math.round(max - p.baseSpend).toLocaleString()}</span>
        </div>
      </div>
    `;
  }).join("");
}

function cleanId(str) {
  return str.replace(/[^a-zA-Z0-9]/g, "_");
}

function handleSliderChange(ch, val) {
  currentSimSpend[ch] = parseFloat(val);
  document.getElementById(`val_${cleanId(ch)}`).innerText = `$${Math.round(val).toLocaleString()}`;
  updateSimulator();
}

function updateSimulator() {
  let totalSpend = 0;
  let totalConv = 0;
  const organicConv = 177.52 + 127.73; // Organic + Referral

  Object.keys(SIM_PARAMS).forEach(ch => {
    const s = currentSimSpend[ch];
    const p = SIM_PARAMS[ch];
    totalSpend += s;
    const c = p.alpha * Math.log(1 + s / p.beta);
    totalConv += c;
  });

  const totalAllConv = totalConv + organicConv;
  const avgRevPerConv = 1188.63; // empirical average net tuition
  const totalRev = totalAllConv * avgRevPerConv;
  const roas = totalRev / totalSpend;

  const baseSpend = 262896.68;
  const baseConv = 1385.0;
  const baseRev = 1646260.0;
  const baseRoas = 6.26;

  const deltaSpend = totalSpend - baseSpend;
  const deltaConv = totalAllConv - baseConv;
  const deltaRev = totalRev - baseRev;
  const deltaRoas = roas - baseRoas;

  document.getElementById("simSpend").innerText = `$${Math.round(totalSpend).toLocaleString()}`;
  document.getElementById("simConv").innerText = totalAllConv.toFixed(1);
  document.getElementById("simRev").innerText = `$${Math.round(totalRev).toLocaleString()}`;
  document.getElementById("simRoas").innerText = `${roas.toFixed(2)}x`;

  const convDeltaEl = document.getElementById("simConvDelta");
  convDeltaEl.innerText = `${deltaConv >= 0 ? "+" : ""}${deltaConv.toFixed(1)} students (${(deltaConv / baseConv * 100).toFixed(1)}%)`;
  convDeltaEl.className = `text-[10px] font-semibold ${deltaConv >= 0 ? "text-emerald-400" : "text-rose-400"}`;

  const revDeltaEl = document.getElementById("simRevDelta");
  revDeltaEl.innerText = `${deltaRev >= 0 ? "+" : ""}$${Math.round(deltaRev).toLocaleString()} net revenue`;
  revDeltaEl.className = `text-[10px] font-semibold ${deltaRev >= 0 ? "text-emerald-400" : "text-rose-400"}`;
}

function applyOptimalBudget() {
  Object.keys(SIM_PARAMS).forEach(ch => {
    currentSimSpend[ch] = SIM_PARAMS[ch].optSpend;
    const input = document.querySelector(`input[oninput*="${ch}"]`);
    if (input) input.value = SIM_PARAMS[ch].optSpend;
    document.getElementById(`val_${cleanId(ch)}`).innerText = `$${Math.round(SIM_PARAMS[ch].optSpend).toLocaleString()}`;
  });
  updateSimulator();
}

function resetBudget() {
  Object.keys(SIM_PARAMS).forEach(ch => {
    currentSimSpend[ch] = SIM_PARAMS[ch].baseSpend;
    const input = document.querySelector(`input[oninput*="${ch}"]`);
    if (input) input.value = SIM_PARAMS[ch].baseSpend;
    document.getElementById(`val_${cleanId(ch)}`).innerText = `$${Math.round(SIM_PARAMS[ch].baseSpend).toLocaleString()}`;
  });
  updateSimulator();
}
