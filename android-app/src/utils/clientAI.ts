
import { pipeline, env } from '@xenova/transformers';

// Skip local check to download from Hugging Face Hub directly
env.allowLocalModels = false;
env.useBrowserCache = true;

// Contraction Map for pre-processing
// Safe expansion to standard english forms
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

export interface ModelProgressData {
    status: string;
    progress: number;
    file: string;
}

// Define the model class singleton
class ClientAI {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    static instance: any = null;
    static modelName = 'Xenova/LaMini-Flan-T5-248M';

    static async getInstance(progressCallback: (data: ModelProgressData) => void) {
        if (!this.instance) {
            console.log('📦 Initializing Client AI Model (248M)...');
            this.instance = await pipeline('text2text-generation', this.modelName, {
                quantized: false,
                progress_callback: progressCallback
            });
            console.log('✅ Client AI Model Loaded');
        }
        return this.instance;
    }
}

// 2. Academic Transitions (Same as Python script)
const ACADEMIC_TRANSITIONS = [
    "Moreover,", "Additionally,", "Furthermore,", "Hence,",
    "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,"
];

// Helper: Split into sentences safely
const splitSentences = (text: string): string[] => {
    return text.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [text];
};

export const humanizeBalanced = async (
    text: string,
    progressCallback: (data: ModelProgressData) => void
): Promise<{ transformed: string }> => {
    try {
        const generator = await ClientAI.getInstance(progressCallback);

        // Step A: Pre-process Contractions (Global)
        let processedText = text;
        Object.entries(CONTRACTION_MAP).forEach(([contraction, expansion]) => {
            const regex = new RegExp(`\\b${contraction}\\b`, 'gi');
            processedText = processedText.replace(regex, (match) => {
                return match[0] === match[0].toUpperCase()
                    ? expansion.charAt(0).toUpperCase() + expansion.slice(1)
                    : expansion;
            });
        });

        const sentences = splitSentences(processedText);
        const results: string[] = [];

        // Step B: Sentence-by-Sentence Processing
        // This ensures we maintain the *structure* exactly like the NLTK loop
        for (let i = 0; i < sentences.length; i++) {
            let sentence = sentences[i].trim();
            if (!sentence) continue;

            // 1. Logic: Inject Transitions (Mimicking Python script)
            // Add random transition if it's not the first sentence and doesn't have one
            if (i > 0 && Math.random() < 0.3) {
                const hasTransition = ACADEMIC_TRANSITIONS.some(t => sentence.startsWith(t));
                if (!hasTransition) {
                    const transition = ACADEMIC_TRANSITIONS[Math.floor(Math.random() * ACADEMIC_TRANSITIONS.length)];
                    sentence = `${transition} ${sentence.charAt(0).toLowerCase() + sentence.slice(1)}`;
                }
            }

            // 2. Logic: Artificial Intelligence (Synonym/Paraphrasing)
            // REVISED PROMPT: Explicit instruction to PRESERVE ERRORS (Typos/Grammar).
            // AI fixing errors is the #1 tell for detectors. We want "Academic/Formal vocabulary" but "Human structure/mistakes".
            const prompt = `Rewrite this sentence using more academic words. Do not correct typos or grammar. Keep the same meaning: ${sentence}`;

            try {
                const output = await generator(prompt, {
                    max_new_tokens: 200,
                    temperature: 0.8,     // High temp for variety
                    do_sample: true,
                    top_k: 50,            // Wide choice of words
                    repetition_penalty: 1.25 // Force it to pick new synonyms
                });

                let finalSent = output[0].generated_text;

                // Safety: If it hallucinated or failed, keep original
                if (!finalSent || finalSent.length < 5) {
                    finalSent = sentence;
                }
                // Cleanup prompt echo if any
                if (finalSent.startsWith(prompt)) {
                    finalSent = finalSent.substring(prompt.length).trim();
                }

                results.push(finalSent);

            } catch {
                console.warn("Sentence generation failed, reusing original");
                results.push(sentence);
            }
        }

        return { transformed: results.join(' ') };

    } catch (error) {
        console.error("Client AI Error:", error);
        return { transformed: text };
    }
};
