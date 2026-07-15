import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')

  return (
    <div className="app-container">
      <header>
        <h1>🛡️ DataGuard Semantic</h1>
        <p>Moteur DLP - Prévention des fuites de données sensibles</p>
      </header>

      <main>
        {/* Zone où l'utilisateur colle le texte suspect */}
        <section className="input-section">
          <textarea
            placeholder="Collez l'email, le ticket ou le document à analyser ici..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button onClick={() => alert("Prochaine étape : connecter l'API !")}>
            Analyser le document
          </button>
        </section>

        {/* Zone où les résultats de l'API s'afficheront */}
        <section className="results-section">
          <h2>Rapport de Conformité</h2>
          <div className="placeholder">
            Aucune analyse en cours. Prêt à scanner.
          </div>
        </section>
      </main>
    </div>
  )
}

export default App