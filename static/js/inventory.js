
async function loadCars(params = {}) {
  const url = new URL(window.location.origin + "/api/cars");
  Object.entries(params).forEach(([k,v]) => { if (v) url.searchParams.set(k, v); });
  const res = await fetch(url);
  const cars = await res.json();
  renderCars(cars);
}

function renderCars(cars) {
  const grid = document.getElementById("cars-grid");
  grid.innerHTML = "";
  if (!cars.length) {
    grid.innerHTML = '<div class="text-muted">No cars found.</div>';
    return;
  }
  cars.forEach(car => {
    const img = (car.images && car.images.length) ? car.images[0] : "https://picsum.photos/640/360?blur=2";
    const price = car.type === "rent" ? (car.price_per_day + " €/day") : (car.price + " €");
    const badge = car.type === "rent" ? "Rent" : "Sale";
    const el = document.createElement("div");
    el.className = "col";
    el.innerHTML = `
      <div class="card h-100 position-relative shadow-sm">
        <span class="badge text-bg-primary badge-type">${badge}</span>
        <img src="${img}" class="card-img-top" alt="${car.make} ${car.model}">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title mb-1">${car.year} ${car.make} ${car.model}</h5>
          <p class="card-text small text-muted mb-2">
            ${car.fuel || ""} • ${car.transmission || ""} • ${car.color || ""}
          </p>
          <div class="mt-auto d-flex justify-content-between align-items-center">
            <strong>${price}</strong>
            <a href="/cars/${car.id}" class="btn btn-sm btn-outline-dark">View</a>
          </div>
        </div>
      </div>`;
    grid.appendChild(el);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const initialType = params.get("type") || "";
  if (initialType) {
    const sel = document.getElementById("type");
    if (sel) sel.value = initialType;
  }

  loadCars({ type: initialType });

  const form = document.getElementById("filters");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const q = document.getElementById("q").value.trim();
    const type = document.getElementById("type").value;
    loadCars({ q, type });
  });
});
