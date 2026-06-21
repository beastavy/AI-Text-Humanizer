import { useState, useEffect } from 'react';
import { humanizeLocal, humanizeRemote } from './utils/humanizer';
import { humanizeBalanced } from './utils/clientAI';
import { initializeAds, showBannerAd } from './utils/ads';
import './App.css';

interface HistoryItem {
  id: number;
  text: string;
  original: string;
  date: string;
}

function App() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  // Modes: 'lite' | 'balanced' | 'pro'
  const [mode, setMode] = useState<'lite' | 'balanced' | 'pro'>('lite');

  // Download Progress for Balanced Mode
  const [downloadProgress, setDownloadProgress] = useState<{ status: string; progress: number } | null>(null);

  // const [apiUrl] = useState('https://ai-text-humanizer-u7rg.onrender.com');
  const apiUrl = 'https://ai-text-humanizer-u7rg.onrender.com';
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

  const [history, setHistory] = useState<HistoryItem[]>(() => {
    try {
      const saved = localStorage.getItem('humanizer_history');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [showHistory, setShowHistory] = useState(false);

  const [isCloudReady, setIsCloudReady] = useState<boolean | null>(null);

  useEffect(() => {
    // Cold Start Handler: Ping the server to wake it up
    const wakeUpServer = async () => {
      try {
        const baseUrl = apiUrl.replace(/\/$/, '');
        const response = await fetch(`${baseUrl}/api/health`);
        if (response.ok) {
          setIsCloudReady(true);
          console.log('✅ Cloud Connected');
        } else {
          setIsCloudReady(false);
          console.log('❌ Cloud Error');
        }
      } catch {
        setIsCloudReady(false);
        console.log('💤 Cloud Sleeping/Unreachable');
      }
    };
    if (mode === 'pro') {
      wakeUpServer();
    }
  }, [apiUrl, mode]);

  /* Haptic Feedback Helper */
  const triggerHaptic = () => {
    if (navigator.vibrate) navigator.vibrate(10);
  };

  const handleHumanize = async () => {
    if (!inputText.trim()) return;
    triggerHaptic();

    setIsProcessing(true);
    try {
      let result;

      if (mode === 'pro') {
        result = await humanizeRemote(inputText, apiUrl, options);
      } else if (mode === 'balanced') {
        // Balanced Mode (Client AI)
        const res = await humanizeBalanced(inputText, (data) => {
          if (data.status === 'progress') {
            setDownloadProgress({ status: data.file, progress: data.progress });
          } else if (data.status === 'done') {
            setDownloadProgress(null);
          }
        });

        // Calculate basic stats for client output since the model just returns text
        const words = res.transformed.trim().split(/\s+/).length;
        const inputWords = inputText.trim().split(/\s+/).length;

        result = {
          transformed: res.transformed,
          stats: {
            inputWords,
            outputWords: words,
            wordsAdded: words - inputWords
          }
        };
      } else {
        // Lite Mode
        // Simulate mobile processing lag for better UX feel
        await new Promise(resolve => setTimeout(resolve, 600));
        result = humanizeLocal(inputText, options);
      }

      setOutputText(result.transformed);
      setStats(result.stats);

      // Save to history
      const newItem = {
        id: Date.now(),
        text: result.transformed,
        original: inputText,
        date: new Date().toLocaleDateString()
      };

      const newHistory = [newItem, ...history].slice(0, 20); // Keep last 20
      setHistory(newHistory);
      localStorage.setItem('humanizer_history', JSON.stringify(newHistory));

    } catch (error) {
      console.error(error);
      alert('Transformation failed. Please check your connection.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCopy = () => {
    triggerHaptic();
    navigator.clipboard.writeText(outputText);
  };

  /* History Cleanup on Mount */
  useEffect(() => {
    // 1. Cleanup History
    const ONE_WEEK = 7 * 24 * 60 * 60 * 1000;
    const now = Date.now();
    const cleanHistory = history.filter((item: HistoryItem) => (now - item.id) < ONE_WEEK);

    if (cleanHistory.length !== history.length) {
      setHistory(cleanHistory);
      localStorage.setItem('humanizer_history', JSON.stringify(cleanHistory));
    }

    // 2. Initialize Ads
    initializeAds().then(() => {
      showBannerAd();
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* Comparison View Helpers */
  const renderDiff = () => {
    const inputWords = inputText.split(/\s+/);
    const outputWords = outputText.split(/\s+/);

    // Simple naive word diff for visualization
    // Green = New/Changed, Normal = Kept
    return outputWords.map((word, i) => {
      const isNew = !inputWords.includes(word);
      // This is a very basic "diff" - for production use 'diff' library
      // ideally we check if word exists in a window of inputWords
      return (
        <span key={i} className={isNew ? "diff-added" : ""}>
          {word}{' '}
        </span>
      );
    });
  };

  const [showDiff, setShowDiff] = useState(false);

  return (
    <div className="app-container">
      <header className="app-header animate-fade-in flex-row-between">
        <div>
          <h1 className="gold-gradient-text">Humanizer Pro</h1>
          <p className="subtitle">AI-to-Human Transformation</p>
        </div>
        <button
          className="history-btn glass-btn"
          onClick={() => { triggerHaptic(); setShowHistory(!showHistory); }}
          title="View History"
        >
          📜
        </button>
      </header>

      {showHistory && (
        <div className="history-overlay animate-fade-in" onClick={() => setShowHistory(false)}>
          <div className="history-sheet slide-up" onClick={e => e.stopPropagation()}>
            <div className="flex-row-between mb-2">
              <h3 className="gold-text">Recent History</h3>
              <button onClick={() => setShowHistory(false)} className="close-btn">✕</button>
            </div>
            <div className="history-list">
              {history.length === 0 ? (
                <div className="empty-state">
                  <span style={{ fontSize: '40px' }}>🕸️</span>
                  <p className="text-muted">No history yet. Start humanizing!</p>
                </div>
              ) : (
                history.map((item: HistoryItem) => (
                  <div key={item.id} className="history-item" onClick={() => {
                    triggerHaptic();
                    setInputText(item.original);
                    setOutputText(item.text);
                    setShowHistory(false);
                  }}>
                    <div className="history-date">{item.date}</div>
                    <div className="history-preview-box">
                      <span className="history-label">IN:</span> {item.original.substring(0, 40)}...
                    </div>
                    <div className="history-preview-box highlight">
                      <span className="history-label">OUT:</span> {item.text.substring(0, 40)}...
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}

      <main className="app-content">
        <div className="mode-toggle glass-card animate-fade-in">
          <div className="setting-row" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '12px' }}>
            <div className="mode-info">
              <span className="mode-title">
                {mode === 'pro' ? '🚀 Pro Mode (Cloud AI)' : mode === 'balanced' ? '🧠 Balanced Mode (Client AI)' : '📱 Lite Mode (Local)'}
              </span>
              <span className="mode-desc">
                {mode === 'pro' ? 'Full NLTK & Transformer power' : mode === 'balanced' ? 'High quality, runs offline (Download required)' : 'Fast, on-device processing'}
              </span>
            </div>

            <div className="intensity-picker w-full">
              <button className={`level-btn ${mode === 'lite' ? 'active' : ''}`} onClick={() => { triggerHaptic(); setMode('lite'); }} style={{ flex: 1 }}>Lite</button>
              <button className={`level-btn ${mode === 'balanced' ? 'active' : ''}`} onClick={() => { triggerHaptic(); setMode('balanced'); }} style={{ flex: 1 }}>Balanced</button>
              <button className={`level-btn ${mode === 'pro' ? 'active' : ''}`} onClick={() => { triggerHaptic(); setMode('pro'); }} style={{ flex: 1 }}>Pro</button>
            </div>
          </div>

          {/* Download Progress Bar for Balanced Mode */}
          {mode === 'balanced' && downloadProgress && (
            <div className="animate-fade-in" style={{ marginTop: '12px', background: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '8px' }}>
              <div className="flex-row-between mb-2">
                <span style={{ fontSize: '10px', color: 'var(--gold-primary)' }}>Downloading AI Model...</span>
                <span style={{ fontSize: '10px', color: '#fff' }}>{Math.round(downloadProgress.progress)}%</span>
              </div>
              <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px' }}>
                <div style={{
                  width: `${downloadProgress.progress}%`,
                  height: '100%',
                  background: 'var(--gold-primary)',
                  borderRadius: '2px',
                  transition: 'width 0.3s ease'
                }} />
              </div>
              <div style={{ fontSize: '9px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                {downloadProgress.status}
              </div>
            </div>
          )}

          {mode === 'pro' && (
            <div className="api-config animate-fade-in">
              <div className="flex-row-between">
                <label className="label-gold" style={{ marginBottom: 0 }}>Server Status</label>
                <div className={`status-badge ${isCloudReady === true ? 'ready' : isCloudReady === false ? 'offline' : 'connecting'}`}>
                  <span className="dot"></span>
                  {isCloudReady === true ? 'Connected' : isCloudReady === false ? 'Offline' : 'Connecting...'}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="card-group animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <div className="flex-row-between">
            <label className="label-gold">Source Text</label>
            {inputText && <span className="clear-btn" onClick={() => setInputText('')}>Clear</span>}
          </div>
          <textarea
            className="input-area"
            placeholder="Paste AI-generated text..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={6}
          />
          <div className="flex-row-between" style={{ marginTop: '8px', padding: '0 4px' }}>
            <span style={{
              fontSize: '10px',
              color: inputText.length > (mode !== 'lite' ? 10000 : 5000) ? '#e74c3c' : 'var(--text-secondary)'
            }}>
              {inputText.length} / {mode !== 'lite' ? '10,000' : '5,000'} chars
            </span>
            {inputText.length > (mode !== 'lite' ? 10000 : 5000) && (
              <span style={{ fontSize: '10px', color: '#e74c3c' }}>
                ⚠️ Limit Exceeded
              </span>
            )}
          </div>
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
            disabled={isProcessing || !inputText.trim() || inputText.length > (mode !== 'lite' ? 10000 : 5000)}
          >
            {isProcessing ? 'Processing...' : inputText.length > (mode !== 'lite' ? 10000 : 5000) ? 'Text Too Long' : 'Humanize Now'}
          </button>
        </div>

        {outputText && (
          <div className="output-container animate-fade-in" style={{ animationDelay: '0.4s' }}>
            <div className="card-group">
              <div className="flex-row-between">
                <div className="flex-row-center" style={{ gap: '8px' }}>
                  <label className="label-gold" style={{ marginBottom: 0 }}>Humanized Result</label>
                  <button className="icon-btn-sm" onClick={handleCopy} title="Copy">📋</button>
                </div>
                <div className="flex-row-center" style={{ gap: '8px' }}>
                  <span style={{ fontSize: '10px', color: 'var(--text-secondary)' }}>Show Changes</span>
                  <label className="switch" style={{ transform: 'scale(0.8)' }}>
                    <input
                      type="checkbox"
                      checked={showDiff}
                      onChange={() => { triggerHaptic(); setShowDiff(!showDiff); }}
                    />
                    <span className="slider"></span>
                  </label>
                </div>
              </div>

              {showDiff ? (
                <div className="output-area glass-card" style={{ whiteSpace: 'pre-wrap' }}>
                  {renderDiff()}
                </div>
              ) : (
                <textarea
                  className="output-area glass-card editable"
                  value={outputText}
                  onChange={(e) => setOutputText(e.target.value)}
                  rows={8}
                />
              )}
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
