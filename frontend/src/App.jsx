import { useEffect, useState } from 'react'
import { createTask, deleteTask, fetchTasks, updateTask } from './api'
import './App.css'

// Reihenfolge fürs Durchschalten: open → in_progress → done → open
const NEXT_STATUS = { open: 'in_progress', in_progress: 'done', done: 'open' }

const STATUS_LABEL = {
  open: 'Offen',
  in_progress: 'In Arbeit',
  done: 'Erledigt',
}

function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTasks()
      .then(setTasks)
      .catch((err) => setError(`Backend nicht erreichbar: ${err.message}`))
      .finally(() => setLoading(false))
  }, [])

  async function handleCreate(event) {
    event.preventDefault()
    if (!title.trim()) return
    try {
      const task = await createTask({ title: title.trim(), description })
      setTasks((prev) => [...prev, task])
      setTitle('')
      setDescription('')
      setError(null)
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleCycleStatus(task) {
    try {
      const updated = await updateTask(task.id, {
        status: NEXT_STATUS[task.status],
      })
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    try {
      await deleteTask(id)
      setTasks((prev) => prev.filter((t) => t.id !== id))
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main className="app">
      <header>
        <h1>CloudOps Capstone</h1>
        <p className="subtitle">Aufgaben- & Ticket-Verwaltung</p>
      </header>

      <form className="task-form" onSubmit={handleCreate}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Neue Aufgabe…"
          aria-label="Titel"
          maxLength={200}
          required
        />
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Beschreibung (optional)"
          aria-label="Beschreibung"
          maxLength={2000}
        />
        <button type="submit">Hinzufügen</button>
      </form>

      {error && <p className="error">{error}</p>}
      {loading && <p>Lade Aufgaben…</p>}

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id} className={`task status-${task.status}`}>
            <div className="task-text">
              <span className="task-title">{task.title}</span>
              {task.description && (
                <span className="task-description">{task.description}</span>
              )}
            </div>
            <div className="task-actions">
              <button
                className="status-badge"
                onClick={() => handleCycleStatus(task)}
                title="Klicken zum Weiterschalten"
              >
                {STATUS_LABEL[task.status]}
              </button>
              <button
                className="delete"
                onClick={() => handleDelete(task.id)}
                aria-label={`${task.title} löschen`}
              >
                ✕
              </button>
            </div>
          </li>
        ))}
      </ul>

      {!loading && tasks.length === 0 && !error && (
        <p className="empty">Noch keine Aufgaben – leg die erste an!</p>
      )}
    </main>
  )
}

export default App
