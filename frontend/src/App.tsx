import { useState, type ChangeEvent, type DragEvent } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import './App.css'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '')

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [results, setResults] = useState<string[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [consentModalOpen, setConsentModalOpen] = useState(false)
  const [consentChoice, setConsentChoice] = useState<boolean | null>(null)
  const [dragActive, setDragActive] = useState(false)

  const resetPreview = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
    }
    setPreviewUrl('')
    setSelectedFile(null)
    setResults([])
    setError('')
    setConsentChoice(null)
  }

  const isImageFile = (file: File) => file.type.startsWith('image/')

  const handleFileSelection = (file?: File) => {
    if (!file) return

    if (!isImageFile(file)) {
      setError('Please choose an image file (PNG, JPG, JPEG, WEBP, etc.).')
      return
    }

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl)
    }

    setSelectedFile(file)
    setPreviewUrl(URL.createObjectURL(file))
    setResults([])
    setError('')
    setConsentChoice(null)
    setConsentModalOpen(true)
  }

  const handleFileSelect = (event: ChangeEvent<HTMLInputElement>) => {
    handleFileSelection(event.target.files?.[0])
    event.target.value = ''
  }

  const handleDragOver = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault()
    setDragActive(true)
  }

  const handleDragLeave = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault()
    setDragActive(false)
  }

  const handleDrop = (event: DragEvent<HTMLLabelElement>) => {
    event.preventDefault()
    setDragActive(false)
    handleFileSelection(event.dataTransfer.files?.[0])
  }

  const handleConsent = async (decision: boolean) => {
    if (!selectedFile) return

    setConsentChoice(decision)
    setConsentModalOpen(false)
    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch(`${API_BASE_URL}/images/search?user_consent=${decision}`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('The search request failed.')
      }

      const data = await response.json()
      const nextResults = Array.isArray(data.results) ? data.results : []

      setResults(nextResults)
      if (nextResults.length === 0) {
        setError('No matching images were returned from the backend.')
      }
    } catch (err) {
      setError(`Unable to reach the VISTA backend at ${API_BASE_URL}. Check your VITE_API_BASE_URL setting and try again.`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app-shell">
      <motion.section
        className="hero-grid"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45 }}
      >
        <article className="glass-card upload-card">
          <div className="upload-header">
            <div>
              <p className="eyebrow">VISTA</p>
              <h2>Upload an image to search</h2>
            </div>
            <span className="status-pill">Ready</span>
          </div>

          <label
            className={`upload-surface${dragActive ? ' is-dragging' : ''}`}
            htmlFor="image-upload"
            onDragOver={handleDragOver}
            onDragEnter={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              id="image-upload"
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              hidden
            />
            <div className="upload-icon">⬆</div>
            <strong>Upload your image and get relevant visuals</strong>
            <span>Click here, or drag and drop a PNG, JPG, or WEBP file.</span>
          </label>

          {selectedFile && (
            <div className="selected-panel">
              <div className="preview-wrap">
                {previewUrl ? <img src={previewUrl} alt="Selected preview" className="preview-image" /> : null}
              </div>
              <div>
                <p className="label-text">Selected file</p>
                <strong>{selectedFile.name}</strong>
                <p className="muted">You will choose whether VISTA may use this image for the search.</p>
              </div>
              <button type="button" className="text-button" onClick={resetPreview}>Clear</button>
            </div>
          )}

          {error ? <p className="error-text">{error}</p> : null}
        </article>
      </motion.section>

      <motion.section
        className="results-panel glass-card"
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.08 }}
      >
        <div className="results-header">
          <div>
            <p className="eyebrow">Results</p>
            <h2>Visual matches</h2>
          </div>
          <span className="status-pill">{loading ? 'Searching…' : results.length ? 'Live results' : 'Awaiting upload'}</span>
        </div>

        {consentChoice !== null ? (
          <p className="consent-note">Consent selected: {consentChoice ? 'Yes, use this image for the search.' : 'No, do not use this image for the search.'}</p>
        ) : null}

        {results.length > 0 ? (
          <div className="result-grid">
            {results.map((url, index) => (
              <motion.figure
                key={`${url}-${index}`}
                className="result-card"
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.25, delay: index * 0.03 }}
              >
                <img src={url} alt={`Search result ${index + 1}`} className="result-image" />
              </motion.figure>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <p>Search results will appear here after you confirm the upload.</p>
          </div>
        )}
      </motion.section>

      <AnimatePresence>
        {consentModalOpen && selectedFile ? (
          <motion.div
            className="modal-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.article
              className="modal-card glass-card"
              initial={{ y: 18, opacity: 0, scale: 0.98 }}
              animate={{ y: 0, opacity: 1, scale: 1 }}
              exit={{ y: 8, opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.2 }}
            >
              <p className="eyebrow">Consent</p>
              <h3>Would you like VISTA to use this image for the search?</h3>
              <p className="modal-copy">
                VISTA uses your uploaded image only to find similar visuals. You can allow or decline this before the search starts.
              </p>
              <div className="modal-actions">
                <button type="button" className="ghost-button" onClick={() => handleConsent(false)}>No, keep it private</button>
                <button type="button" className="primary-button" onClick={() => handleConsent(true)}>Yes, use it</button>
              </div>
            </motion.article>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </main>
  )
}

export default App
