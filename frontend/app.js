const API_BASE = "/api";

function getToken(){
  return localStorage.getItem("jwt_token") || "";
}

async function apiFetch(path, opts = {}){
  const url = path.startsWith("http") ? path : `${API_BASE}${path}`;
  const headers = opts.headers ? {...opts.headers} : {};
  headers["Content-Type"] = headers["Content-Type"] || "application/json";

  const token = getToken();
  if (token){
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(url, {...opts, headers});
  if (!res.ok){
    const text = await res.text().catch(()=> "");
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
  if (res.status === 204) return null;
  return await res.json();
}

function getQueryParam(name){
  const u = new URL(window.location.href);
  return u.searchParams.get(name);
}

function clear(el){
  while(el.firstChild) el.removeChild(el.firstChild);
}

function formatMoney(n){
  const num = Number(n);
  return num.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
}

