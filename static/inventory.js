
async function loadCars(params = {}){
  const url = new URL(window.location.origin + "/api/cars");
  Object.entries(params).forEach(([k,v])=>{ if(v) url.searchParams.set(k,v); });
  const res = await fetch(url);
  const cars = await res.json();

  const sort = params.sort || "";
  cars.sort((a,b)=>{
    const pa = a.type==="rent" ? (a.price_per_day||0) : (a.price||0);
    const pb = b.type==="rent" ? (b.price_per_day||0) : (b.price||0);
    switch(sort){
      case "price-asc": return pa-pb;
      case "price-desc": return pb-pa;
      case "year-asc": return (parseInt(a.year||0)-parseInt(b.year||0));
      case "year-desc": return (parseInt(b.year||0)-parseInt(a.year||0));
      default: return 0;
    }
  });

  renderCars(cars);
}

function renderCars(cars){
  const grid = document.getElementById("cars-grid");
  const count = document.getElementById("result-count");
  grid.innerHTML = "";
  count.textContent = cars.length ? `${cars.length} results` : "No cars found";

  if(!cars.length){ grid.innerHTML = "<div class='text-slate-500'>No cars found.</div>"; return; }

  cars.forEach(car=>{
    const img = (car.images && car.images.length) ? car.images[0] : "/static/hero.jpg";
    const price = car.type==="rent" ? (car.price_per_day + " €/day") : (car.price + " €");
    const badge = car.type==="rent" ? "Rent" : "For Sale";
    const card = document.createElement("a");
    card.href = "/cars/" + car.id;
    card.className = "block rounded-2xl border bg-white shadow-sm overflow-hidden hover:shadow-md transition";
    card.innerHTML = `
      <div class="relative">
        <img src="${img}" class="w-full h-48 object-cover" alt="${car.make} ${car.model}" loading="lazy">
        <span class="absolute top-2 left-2 px-2 py-1 rounded-lg text-xs bg-black/70 text-white">${badge}</span>
      </div>
      <div class="p-4">
        <div class="flex items-center justify-between">
          <h3 class="font-semibold">${car.year} ${car.make} ${car.model}</h3>
          <div class="font-bold">${price}</div>
        </div>
        <div class="mt-1 text-slate-600 text-sm">${car.fuel||""} • ${car.transmission||""} • ${car.color||""}</div>
      </div>`;
    grid.appendChild(card);
  });
}

document.addEventListener("DOMContentLoaded",()=>{
  const params = new URLSearchParams(window.location.search);
  const tab = params.get("tab") || "rent";
  const form = document.getElementById("filters");
  const typeSel = document.getElementById("type");
  if(tab){ typeSel.value = tab; }
  loadCars({ type: typeSel.value });

  form.addEventListener("submit",(e)=>{
    e.preventDefault();
    const q = document.getElementById("q").value.trim();
    const type = typeSel.value;
    const sort = document.getElementById("sort").value;
    loadCars({ q, type, sort });
  });
});
