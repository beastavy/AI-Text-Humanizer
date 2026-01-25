/**
 * Core Humanization Logic Ported from Python
 */

interface TransformationStats {
  inputWords: number;
  outputWords: number;
  wordsAdded: number;
}

const CONTRACTION_MAP: Record<string, string> = {
  "don't": "do not", "doesn't": "does not", "didn't": "did not",
  "won't": "will not", "can't": "cannot", "couldn't": "could not",
  "wouldn't": "would not", "shouldn't": "should not", "mustn't": "must not",
  "isn't": "is not", "aren't": "are not", "wasn't": "was not",
  "weren't": "were not", "hasn't": "has not", "haven't": "have not",
  "hadn't": "had not",
  "i'm": "I am", "you're": "you are", "he's": "he is", "she's": "she is",
  "we're": "we are", "they're": "they are", "i'll": "I will",
  "you'll": "you will", "he'll": "he will", "she'll": "she will",
  "we'll": "we will", "they'll": "they will", "i've": "I have",
  "you've": "you have", "we've": "we have", "they've": "they have",
  "i'd": "I would", "you'd": "you would", "he'd": "he would",
  "she'd": "she would", "we'd": "we would", "they'd": "they would",
  "it's": "it is", "that's": "that is", "there's": "there is",
  "here's": "here is", "what's": "what is", "who's": "who is",
  "where's": "where is", "when's": "when is", "why's": "why is",
  "how's": "how is"
};

const ACADEMIC_TRANSITIONS = [
  "Moreover,", "Additionally,", "Furthermore,", "Hence,",
  "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,"
];

const SYNONYM_MAP: Record<string, string[]> = {
  "good": ["advantageous", "beneficial", "exemplary", "favourable"],
  "bad": ["detrimental", "problematic", "adverse", "suboptimal"],
  "think": ["contemplate", "hypothesize", "postulate", "assert"],
  "work": ["function", "operate", "perform", "execute"],
  "problem": ["complication", "dilemma", "impediment", "challenge"],
  "important": ["paramount", "pivotal", "essential", "significant"],
  "many": ["multitudinous", "numerous", "copious", "myriad"],
  "show": ["demonstrate", "illustrate", "elucidate", "manifest"],
  "use": ["utilize", "employ", "implement", "deploy"],
  "idea": ["concept", "paradigm", "proposition", "notion"]
};

export const humanizeLocal = (
  text: string,
  options: {
    useTransitions: boolean;
    useSynonyms: boolean;
    intensity: 'light' | 'medium' | 'heavy'
  }
): { transformed: string; stats: TransformationStats } => {
  if (!text.trim()) return { transformed: '', stats: { inputWords: 0, outputWords: 0, wordsAdded: 0 } };

  const inputWords = text.trim().split(/\s+/).length;
  let result = text;

  // 1. Expand Contractions
  Object.entries(CONTRACTION_MAP).forEach(([contraction, expansion]) => {
    const regex = new RegExp(`\\b${contraction}\\b`, 'gi');
    result = result.replace(regex, (match) => {
      return match[0] === match[0].toUpperCase()
        ? expansion.charAt(0).toUpperCase() + expansion.slice(1)
        : expansion;
    });
  });

  // 2. Add Academic Transitions
  if (options.useTransitions) {
    const sentences = result.split(/([.!?])\s+/);
    if (sentences.length > 2) {
      const pTransition = options.intensity === 'heavy' ? 0.5 : options.intensity === 'medium' ? 0.3 : 0.1;

      for (let i = 2; i < sentences.length; i += 2) {
        if (Math.random() < pTransition) {
          const transition = ACADEMIC_TRANSITIONS[Math.floor(Math.random() * ACADEMIC_TRANSITIONS.length)];
          if (sentences[i]) {
            sentences[i] = transition + " " + sentences[i].charAt(0).toLowerCase() + sentences[i].slice(1);
          }
        }
      }
      result = sentences.join('');
    }
  }

  // 3. Synonym Replacement
  if (options.useSynonyms) {
    const pSynonym = options.intensity === 'heavy' ? 0.4 : options.intensity === 'medium' ? 0.2 : 0.1;

    Object.entries(SYNONYM_MAP).forEach(([word, synonyms]) => {
      const regex = new RegExp(`\\b${word}\\b`, 'gi');
      result = result.replace(regex, (match) => {
        if (Math.random() < pSynonym) {
          const syn = synonyms[Math.floor(Math.random() * synonyms.length)];
          return match[0] === match[0].toUpperCase()
            ? syn.charAt(0).toUpperCase() + syn.slice(1)
            : syn;
        }
        return match;
      });
    });
  }

  const outputWords = result.trim().split(/\s+/).length;

  return {
    transformed: result,
    stats: {
      inputWords,
      outputWords,
      wordsAdded: outputWords - inputWords
    }
  };
};

export const humanizeRemote = async (
  text: string,
  apiUrl: string,
  options: any
): Promise<{ transformed: string; stats: TransformationStats }> => {
  const response = await fetch(`${apiUrl}/api/transform`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      use_passive: true, // Advanced feature
      use_synonyms: options.useSynonyms,
      intensity: options.intensity,
      style: 'academic'
    })
  });

  if (!response.ok) throw new Error('Remote transformation failed');

  const data = await response.json();
  return {
    transformed: data.transformed_text,
    stats: {
      inputWords: data.statistics.input_words,
      outputWords: data.statistics.output_words,
      wordsAdded: data.statistics.output_words - data.statistics.input_words
    }
  };
};
