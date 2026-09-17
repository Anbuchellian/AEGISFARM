const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function request(path, options={}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  dashboard: () => request('/dashboard'),
  detections: () => request('/detections'),
  interventions: () => request('/interventions'),
  validation: () => request('/validation'),
  simulate: (payload) => request('/simulate', { method: 'POST', body: JSON.stringify(payload) }),
  addValidation: (payload) => request('/validation', { method: 'POST', body: JSON.stringify(payload) }),
  reset: () => request('/reset', { method: 'POST' }),
};
