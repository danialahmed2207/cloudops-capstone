// Zentrale API-Schicht: alle Backend-Aufrufe an einem Ort.
// Die Pfade sind relativ (/api/...) – im Dev-Modus leitet der Vite-Proxy
// sie ans Backend weiter, in Produktion später Nginx.

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail ?? `HTTP ${response.status}`)
  }
  // DELETE liefert 204 No Content – da gibt es kein JSON
  return response.status === 204 ? null : response.json()
}

export function fetchTasks() {
  return request('/api/tasks')
}

export function createTask(task) {
  return request('/api/tasks', { method: 'POST', body: JSON.stringify(task) })
}

export function updateTask(id, changes) {
  return request(`/api/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(changes),
  })
}

export function deleteTask(id) {
  return request(`/api/tasks/${id}`, { method: 'DELETE' })
}
