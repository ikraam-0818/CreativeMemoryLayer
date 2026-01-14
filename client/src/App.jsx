import { useState } from 'react'
import { ProjectList } from './components/ProjectList'
import { Studio } from './components/Studio'

function App() {
  const [projectId, setProjectId] = useState(null)

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-purple-500 selection:text-white">
      {projectId ? (
        <Studio
          projectId={projectId}
          onBack={() => setProjectId(null)}
        />
      ) : (
        <ProjectList
          onSelectProject={setProjectId}
        />
      )}
    </div>
  )
}

export default App
