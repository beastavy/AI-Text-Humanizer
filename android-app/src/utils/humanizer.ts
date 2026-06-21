/**
 * Core Humanization Logic Ported from Python
 */

interface TransformationStats {
  inputWords: number;
  outputWords: number;
  wordsAdded: number;
}

export interface HumanizerOptions {
  useTransitions: boolean;
  useSynonyms: boolean;
  intensity: 'light' | 'medium' | 'heavy';
  usePassive?: boolean;
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
  "good": ["advantageous", "beneficial", "exemplary", "favourable", "superior"],
  "bad": ["detrimental", "problematic", "adverse", "suboptimal", "unfavorable"],
  "think": ["contemplate", "hypothesize", "postulate", "assert", "theorize"],
  "work": ["function", "operate", "perform", "execute", "endeavor"],
  "problem": ["complication", "dilemma", "impediment", "challenge", "obstacle"],
  "important": ["paramount", "pivotal", "essential", "significant", "crucial"],
  "many": ["multitudinous", "numerous", "copious", "myriad", "countless"],
  "show": ["demonstrate", "illustrate", "elucidate", "manifest", "exhibit"],
  "use": ["utilize", "employ", "implement", "deploy", "leverage"],
  "idea": ["concept", "paradigm", "proposition", "notion", "construct"],
  "make": ["construct", "fabricate", "generate", "produce", "synthesize"],
  "help": ["assist", "aid", "facilitate", "support", "bolster"],
  "change": ["alter", "modify", "transform", "adapt", "evolve"],
  "big": ["substantial", "considerable", "extensive", "massive", "significant"],
  "small": ["diminutive", "negligible", "minimal", "minute", "limited"],
  "start": ["commence", "initiate", "inaugurate", "instigate", "launch"],
  "end": ["conclude", "terminate", "cease", "finalize", "culminate"],
  "need": ["require", "necessitate", "demand", "entail", "warrant"],
  "say": ["articulate", "express", "state", "declare", "proclaim"],
  "know": ["comprehend", "perceive", "understand", "grasp", "cognize"]
};

export const humanizeLocal = (
  text: string,
  options: HumanizerOptions
): { transformed: string; stats: TransformationStats } => {
  if (!text.trim()) return { transformed: '', stats: { inputWords: 0, outputWords: 0, wordsAdded: 0 } };

  const inputWords = text.trim().split(/\s+/).length;

  // Split into paragraphs to preserve structure
  const paragraphs = text.split('\n');

  const transformedParagraphs = paragraphs.map(paragraph => {
    if (!paragraph.trim()) return paragraph; // Preserve empty lines

    let result = paragraph;

    // 1. Expand Contractions
    Object.entries(CONTRACTION_MAP).forEach(([contraction, expansion]) => {
      const regex = new RegExp(`\\b${contraction}\\b`, 'gi');
      result = result.replace(regex, (match) => {
        return match[0] === match[0].toUpperCase()
          ? expansion.charAt(0).toUpperCase() + expansion.slice(1)
          : expansion;
      });
    });

    // 2. Add Academic Transitions (Only for longer paragraphs)
    if (options.useTransitions) {
      const sentences = result.split(/([.!?])\s+/);
      const pTransition = options.intensity === 'heavy' ? 0.7 : options.intensity === 'medium' ? 0.4 : 0.2;

      for (let i = 0; i < sentences.length; i++) {
        if (sentences[i].length < 5 || ['.', '!', '?'].includes(sentences[i])) continue;

        if (i > 0 && Math.random() < pTransition) {
          const transition = ACADEMIC_TRANSITIONS[Math.floor(Math.random() * ACADEMIC_TRANSITIONS.length)];
          if (!sentences[i].trim().startsWith(transition)) {
            sentences[i] = transition + " " + sentences[i].charAt(0).toLowerCase() + sentences[i].slice(1);
          }
        }
      }
      result = sentences.join(' '); // Rejoin with space within paragraph
    }

    // 3. Synonym Replacement
    if (options.useSynonyms) {
      const pSynonym = options.intensity === 'heavy' ? 0.8 : options.intensity === 'medium' ? 0.5 : 0.3;

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
    return result;
  });

  const finalResult = transformedParagraphs.join('\n');
  const outputWords = finalResult.trim().split(/\s+/).length;

  return {
    transformed: finalResult,
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
  options: HumanizerOptions
): Promise<{ transformed: string; stats: TransformationStats }> => {
  // Ensure no trailing slash
  const baseUrl = apiUrl.replace(/\/$/, '');

  const response = await fetch(`${baseUrl}/api/transform`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      use_passive: Boolean(options?.usePassive),
      use_synonyms: options.useSynonyms,
      intensity: options.intensity,
      style: 'academic',
      preserve_structure: true // Vital for headings/paragraphs
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
