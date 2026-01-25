import { useState } from 'react';
import { humanizeLocal, humanizeRemote } from './utils/humanizer';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [proMode, setProMode] = useState(false);
  const [apiUrl, setApiUrl] = useState('https://your-humanizer-api.render.com');
  const [options, setOptions] = useState({
    useTransitions: true,
    useSynonyms: true,
    intensity: 'medium' as 'light' | 'medium' | 'heavy'
  });
  const [stats, setStats] = useState({
    inputWords: 0,
    outputWords: 0,
    wordsAdded: 0
  });

  const handleHumanize = async () => {
    if (!inputText.trim()) return;

    setIsProcessing(true);
    try {
      let result;
      if (proMode) {
        result = await humanizeRemote(inputText, apiUrl, options);
      } else {
        // Simulate mobile processing lag for better UX feel
        await new Promise(resolve => setTimeout(resolve, 600));
        result = humanizeLocal(inputText, options);
      }

      setOutputText(result.transformed);
      setStats(result.stats);
    } catch (error) {
      console.error(error);
      alert('Transformation failed. Please check your API URL or connection.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(outputText);
  };

  return (
    <div className="app-container">
      <header className="app-header animate-fade-in">
        <h1 className="gold-gradient-text">Humanizer Pro</h1>
        <p className="subtitle">AI-to-Human Transformation</p>
      </header>

      <main className="app-content">
        <div className="mode-toggle glass-card animate-fade-in">
          <div className="setting-row">
            <div className="mode-info">
              <span className="mode-title">{proMode ? '🚀 Pro Mode (Cloud AI)' : '📱 Lite Mode (Local)'}</span>
              <span className="mode-desc">{proMode ? 'Full NLTK & Transformer power' : 'Fast, on-device processing'}</span>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={proMode}
                onChange={() => setProMode(!proMode)}
              />
              <span className="slider"></span>
            </label>
          </div>
          {proMode && (
            <div className="api-config animate-fade-in">
              <label className="label-gold">API Endpoint</label>
              <input
                type="text"
                className="input-area sm"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                placeholder="https://..."
              />
            </div>
          )}
        </div>

        <div className="card-group animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <label className="label-gold">Source Text</label>
          <textarea
            className="input-area"
            placeholder="Paste AI-generated text..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={6}
          />
        </div>

        <div className="settings-panel glass-card animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <div className="setting-row">
            <span>Academic Transitions</span>
            <label className="switch">
              <input
                type="checkbox"
                checked={options.useTransitions}
                onChange={() => setOptions({ ...options, useTransitions: !options.useTransitions })}
              />
              <span className="slider"></span>
            </label>
          </div>
          <div className="setting-row">
            <span>Synonym Replacement</span>
            <label className="switch">
              <input
                type="checkbox"
                checked={options.useSynonyms}
                onChange={() => setOptions({ ...options, useSynonyms: !options.useSynonyms })}
              />
              <span className="slider"></span>
            </label>
          </div>
          <div className="setting-row">
            <span>Intensity</span>
            <div className="intensity-picker">
              {(['light', 'medium', 'heavy'] as const).map(lev => (
                <button
                  key={lev}
                  className={`level-btn ${options.intensity === lev ? 'active' : ''}`}
                  onClick={() => setOptions({ ...options, intensity: lev })}
                >
                  {lev}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="action-container animate-fade-in" style={{ animationDelay: '0.3s' }}>
          <button
            className="gold-button w-full"
            onClick={handleHumanize}
            disabled={isProcessing || !inputText.trim()}
          >
            {isProcessing ? 'Processing...' : 'Humanize Now'}
          </button>
        </div>

        {outputText && (
          <div className="output-container animate-fade-in" style={{ animationDelay: '0.4s' }}>
            <div className="card-group">
              <label className="label-gold">Humanized Result</label>
              <div className="output-area glass-card">
                {outputText}
              </div>
            </div>

            <div className="stats-grid glass-card">
              <div className="stat-card">
                <span className="stat-val">{stats.inputWords}</span>
                <span className="stat-lab">In Words</span>
              </div>
              <div className="stat-card">
                <span className="stat-val">{stats.outputWords}</span>
                <span className="stat-lab">Out Words</span>
              </div>
              <div className="stat-card">
                <span className="stat-val gold-gradient-text">+{stats.wordsAdded}</span>
                <span className="stat-lab">Expansion</span>
              </div>
            </div>

            <button className="gold-button outline w-full" onClick={handleCopy}>
              Copy Result
            </button>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>© 2026 Obsidian AI Labs</p>
      </footer>
    </div>
  );
}

export default App;
