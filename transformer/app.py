import ssl
import random
import warnings
import re
import hashlib

import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# Try to import sentence_transformers, but handle if not available
try:
    from sentence_transformers import SentenceTransformer, util
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Synonym replacement will be limited.")

warnings.filterwarnings("ignore", category=FutureWarning)

CONTRACTION_MAP = {
    "don't": "do not", "doesn't": "does not", "didn't": "did not",
    "won't": "will not", "can't": "cannot", "couldn't": "could not",
    "wouldn't": "would not", "shouldn't": "should not", "mustn't": "must not",
    "isn't": "is not", "aren't": "are not", "wasn't": "was not",
    "weren't": "were not", "hasn't": "has not", "haven't": "have not",
    "hadn't": "had not", "let's": "let us",
    "i'm": "i am", "you're": "you are", "he's": "he is", "she's": "she is",
    "we're": "we are", "they're": "they are", "i'll": "i will",
    "you'll": "you will", "he'll": "he will", "she'll": "she will",
    "we'll": "we will", "they'll": "they will", "i've": "i have",
    "you've": "you have", "we've": "we have", "they've": "they have",
    "i'd": "i would", "you'd": "you would", "he'd": "he would",
    "she'd": "she would", "we'd": "we would", "they'd": "they would",
    "it's": "it is", "that's": "that is", "there's": "there is",
    "here's": "here is", "what's": "what is", "who's": "who is",
    "where's": "where is", "when's": "when is", "why's": "why is",
    "how's": "how is"
}

# Words that should NEVER be replaced by synonyms (function words, pronouns, common verbs)
SYNONYM_BLACKLIST = {
    "not", "no", "do", "does", "did", "is", "are", "was", "were",
    "be", "been", "being", "has", "have", "had", "the", "a", "an",
    "and", "or", "but", "if", "so", "yet", "for", "nor", "at", "by",
    "in", "on", "to", "up", "of", "it", "its", "this", "that", "i",
    "we", "he", "she", "they", "you", "me", "him", "her", "us", "them",
    "my", "your", "his", "our", "their", "can", "will", "would",
    "could", "should", "may", "might", "shall", "must",
    "very", "just", "also", "too", "now", "then", "here", "there",
    "all", "each", "every", "both", "few", "more", "most", "some",
    "any", "other", "new", "old", "own", "well", "still", "even",
    "get", "got", "go", "come", "make", "take", "give", "say", "see",
    "know", "think", "want", "need", "seem", "let", "put", "set",
    "much", "many", "only", "about", "into", "over", "after",
    "before", "between", "under", "through", "with", "from",
    "always", "never", "often", "sometimes",
    # AI High-Frequency Words (Wikipedia Cleanup)
    "delve", "crucial", "essential", "significant", "pivotal", "key", "landscape", "tapestry",
    "interplay", "intricate", "intricacies", "vibrant", "enduring", "testament", "underscore",
    "highlight", "fostering", "garner", "showcase", "additionally", "moreover", "furthermore"
}

# Synonyms for specific common words (fallback)
CURATED_SYNONYMS = {
    "use": "utilize",
    "start": "commence",
    "end": "conclude",
    "idea": "concept",
    "problem": "challenge",
    "result": "outcome",
    "change": "modify",
    "need": "require",
    "make": "produce",
    "get": "obtain",
    "many": "a substantial number of",
    "some": "specific",
    "all": "every single",
    "often": "frequently",
    "usually": "ordinarily",
    "always": "consistently",
    "never": "at no point",
    "fast": "rapid",
    "slow": "gradual",
    "big": "substantial",
    "small": "minimal",
    "good": "favorable",
    "bad": "unfavorable",
    "easy": "straightforward",
    "hard": "challenging",
    "help": "assist",
    "give": "provide",
    "take": "acquire",
    "do": "perform",
    "show": "demonstrate",
    "say": "state",
    "think": "believe",
    "know": "understand",
    "find": "identify",
    # De-Sloping Mappings (Wikipedia Guide)
    "serves as": "is",
    "stands as": "is",
    "marks a": "is a",
    "represents a": "is a",
    "functions as": "is",
    "boasts a": "has a",
    "features a": "has a",
    "offers a": "has a",
    "is a testament to": "is a reminder of",
    "underscores the importance": "shows the importance",
    "pivotal role": "important role",
    "evolving landscape": "changing environment",
    "deeply rooted in": "based on",
    "indelible mark": "lasting impact"
}

PHRASE_REWRITES = {
    r"\bi think\b": "I believe",
    r"\bi guess\b": "I infer",
    r"\ba lot of\b": "a substantial number of",
    r"\bkind of\b": "somewhat",
    r"\bsort of\b": "somewhat",
    r"\bso\b": "therefore",
    r"\bfor sure\b": "with certainty",
    r"\bin order to\b": "to",
    r"\bcan't\b": "cannot",
    r"\bwon't\b": "will not",
}

IRREGULAR_PARTICIPLES = {
    "be": "been", "begin": "begun", "break": "broken", "bring": "brought",
    "build": "built", "buy": "bought", "choose": "chosen", "come": "come",
    "do": "done", "draw": "drawn", "drink": "drunk", "drive": "driven",
    "eat": "eaten", "fall": "fallen", "find": "found", "fly": "flown",
    "forget": "forgotten", "get": "gotten", "give": "given", "go": "gone",
    "grow": "grown", "have": "had", "hear": "heard", "keep": "kept",
    "know": "known", "leave": "left", "make": "made", "pay": "paid",
    "read": "read", "run": "run", "say": "said", "see": "seen",
    "send": "sent", "show": "shown", "speak": "spoken", "take": "taken",
    "teach": "taught", "tell": "told", "think": "thought", "write": "written"
}

# Try to load spaCy model; gracefully fall back to a blank English pipeline
try:
    NLP_GLOBAL = spacy.load("en_core_web_sm")
except Exception:
    NLP_GLOBAL = spacy.blank("en")
    if "sentencizer" not in NLP_GLOBAL.pipe_names:
        NLP_GLOBAL.add_pipe("sentencizer")

def download_nltk_resources():
    """
    Download required NLTK resources if not already installed.
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    resources = ['punkt', 'averaged_perceptron_tagger', 'punkt_tab','wordnet','averaged_perceptron_tagger_eng']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception as e:
            print(f"Error downloading {resource}: {str(e)}")


# This class  contains methods to humanize academic text, such as improving readability or
# simplifying complex language.
class AcademicTextHumanizer:
    """
    Transforms text into a more formal (academic) style:
      - Expands contractions
      - Adds academic transitions
      - Optionally converts some sentences to passive voice
      - Optionally replaces words with synonyms for more formality
    """

    def __init__(
        self,
        model_name='paraphrase-MiniLM-L6-v2',
        p_passive=0.2,
        p_synonym_replacement=0.3,
        p_academic_transition=0.3,
        seed=None,
        use_sentence_transformers=True,
    ):
        if seed is not None:
            random.seed(seed)

        # Robust spaCy pipeline: prefer en_core_web_sm; fallback to blank('en') with sentencizer
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = spacy.blank("en")
            if "sentencizer" not in self.nlp.pipe_names:
                self.nlp.add_pipe("sentencizer")
        
        # Initialize sentence transformer only if available and loading succeeds
        self.model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE and use_sentence_transformers:
            try:
                # Avoid network if model cannot be found; rely on cached/bundled if present
                self.model = SentenceTransformer(model_name)
            except Exception:
                # Graceful degradation when model can't be loaded/downloaded
                self.model = None

        self.p_passive = p_passive
        self.p_synonym_replacement = p_synonym_replacement
        self.p_academic_transition = p_academic_transition

        # Style-specific transitions
        self.style_transitions = {
            'academic': [
                "Moreover,", "Additionally,", "Furthermore,", "Hence,",
                "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,",
                "It is worth noting that", "Significantly,", "In this regard,"
            ],
            'professional': [
                "Additionally,", "As a result,", "In summary,", "Importantly,",
                "Moving forward,", "To that end,", "With this in mind,",
                "Building on this,", "In practice,"
            ],
            'formal': [
                "Furthermore,", "Moreover,", "Accordingly,", "Thus,",
                "In light of the above,", "Notwithstanding,", "Henceforth,",
                "Consequently,", "It should be noted that"
            ]
        }
        # Default fallback
        self.academic_transitions = self.style_transitions['academic']
        self.synonym_replace_limit = 2

    def humanize_text(self, text, use_passive=False, use_synonyms=False, preserve_structure=False, intensity="medium", style="academic"):
        # Select transitions based on style
        self.academic_transitions = self.style_transitions.get(style, self.style_transitions['academic'])
        self._seed_for_request(text, use_passive, use_synonyms, preserve_structure, intensity, style)
        # Map intensity to probabilities
        if intensity == "very_heavy":
            p_passive_val = 0.9
            p_synonym_val = 0.98
            p_transition_val = 0.95
            self.p_shuffle = 0.8  # Aggressive shuffling
            self.p_split = 0.7    # Aggressive splitting
            self.synonym_replace_limit = 8
        elif intensity == "heavy":
            p_passive_val = 0.7
            p_synonym_val = 0.8
            p_transition_val = 0.7
            self.p_shuffle = 0.3
            self.p_split = 0.3
            self.synonym_replace_limit = 4
        elif intensity == "light":
            p_passive_val = 0.1
            p_synonym_val = 0.2
            p_transition_val = 0.2
            self.p_shuffle = 0.0
            self.p_split = 0.0
            self.synonym_replace_limit = 1
        else:  # medium (default)
            p_passive_val = self.p_passive
            p_synonym_val = self.p_synonym_replacement
            p_transition_val = self.p_academic_transition
            self.p_shuffle = 0.1
            self.p_split = 0.1
            self.synonym_replace_limit = 2

        if preserve_structure:
            # Structure preservation mode
            lines = text.split('\n')
            transformed_lines = []

            for line in lines:
                stripped = line.strip()

                # Skip empty lines but preserve them
                if not stripped:
                    transformed_lines.append('')
                    continue

                # Check if line looks like a heading
                if self._is_heading(stripped):
                    # Process heading with minimal changes
                    processed_heading = self.expand_contractions(stripped)
                    transformed_lines.append(processed_heading)
                else:
                    # Process as regular paragraph
                    processed_paragraph = self._process_paragraph(
                        stripped,
                        use_passive,
                        use_synonyms,
                        p_passive_val,
                        p_synonym_val,
                        p_transition_val,
                        style
                    )
                    transformed_lines.append(processed_paragraph)

            transformed_text = '\n'.join(transformed_lines)
            transformed_text = self._ensure_minimum_change(
                text,
                transformed_text,
                use_synonyms,
                intensity
            )
            return self._cleanup_text(transformed_text)
        else:
            # Non-preserve mode: still respect paragraph breaks (double newlines)
            # Split text into paragraphs, process each one, rejoin with original spacing
            paragraphs = re.split(r'(\n\s*\n)', text)
            transformed_parts = []

            for part in paragraphs:
                # If this part is just whitespace/newlines, preserve it as-is
                if not part.strip():
                    transformed_parts.append(part)
                    continue

                # Check if this part is a heading line
                stripped_part = part.strip()
                if self._is_heading(stripped_part):
                    transformed_parts.append(self.expand_contractions(stripped_part))
                    continue

                # Process this paragraph
                try:
                    doc = self.nlp(stripped_part)
                    transformed_sentences = []
                    sentences_list = list(doc.sents)
                    
                    force_action = (len(sentences_list) == 1 and intensity in ("heavy", "very_heavy"))

                    for i, sent in enumerate(sentences_list):
                        sentence_str = sent.text.strip()

                        # 1. Expand contractions and informal phrases
                        sentence_str = self.expand_contractions(sentence_str)
                        sentence_str = self.rewrite_common_phrases(sentence_str)

                        # De-Sloping (Wikipedia Pattern Removal)
                        sentence_str = self._de_slope_sentence(sentence_str)

                        # 2. Mechanical Transformations
                        if use_passive and (random.random() < p_passive_val or force_action):
                            sentence_str = self.convert_to_passive(sentence_str)

                        if use_synonyms and (random.random() < p_synonym_val or force_action):
                            sentence_str = self.replace_with_synonyms(sentence_str)

                        if intensity == "very_heavy" and random.random() < 0.25:
                            sentence_str = self._swap_clauses(sentence_str)

                        # 3. Stylistic Injections
                        should_add_transition = not (sentence_str.startswith(('However,', 'Therefore,', 'Moreover,', 'Furthermore,', 
                                                            'Additionally,', 'Consequently,', 'In addition,', 'On the other hand,',
                                                            'Moving forward,', 'Building on',
                                                            'In light of', 'Significantly,', 'In this regard,', 'Actually,', 'Honestly,')))
                        
                        if i > 0 and should_add_transition and (intensity in ('heavy', 'very_heavy') or random.random() < p_transition_val):
                            soft_transitions = ["Actually,", "Honestly,", "In fact,", "The thing is,", "As it turns out,", "Interestingly,", "To be fair,"]
                            is_formal = intensity not in ("heavy", "very_heavy") or random.random() < 0.4
                            
                            if is_formal:
                                sentence_str = self.add_academic_transitions(sentence_str)
                            else:
                                sentence_str = f"{random.choice(soft_transitions)} {sentence_str[0].lower()}{sentence_str[1:]}"

                        sentence_str = self._inject_fillers(sentence_str, intensity)
                        
                        if intensity == "very_heavy":
                            sentence_str = self._inject_personality(sentence_str)

                        if intensity == "very_heavy" and random.random() < 0.15:
                            sentence_str = self._add_human_nuance(sentence_str, style)

                        transformed_sentences.append(sentence_str)

                    if intensity == "very_heavy":
                        transformed_sentences = self._apply_burstiness(transformed_sentences)

                    if intensity in ("heavy", "very_heavy"):
                        final_sentences = self._apply_rhythmic_variety(transformed_sentences)
                    else:
                        final_sentences = transformed_sentences

                    transformed_parts.append(' '.join(final_sentences))
                except Exception:
                    transformed_parts.append(self._fallback_humanize(stripped_part, use_passive, use_synonyms))

            transformed_text = '\n\n'.join(p for p in transformed_parts if p.strip())
            transformed_text = self._ensure_minimum_change(
                text,
                transformed_text,
                use_synonyms,
                intensity
            )
            return self._cleanup_text(transformed_text)
    
    def _fallback_humanize(self, text, use_passive=False, use_synonyms=False):
        """Fallback humanization when spaCy fails"""
        sentences = self._split_sentences(text)
        transformed_sentences = []

        for i, sentence in enumerate(sentences):
            # 1. Expand contractions (always do this)
            sentence = self.expand_contractions(sentence)
            sentence = self.rewrite_common_phrases(sentence)

            # 2. Add academic transitions
            if (i > 0 and random.random() < self.p_academic_transition
                and not sentence.startswith(('Moreover,', 'Furthermore,', 'Additionally,',
                                           'However,', 'Nevertheless,', 'Therefore,',
                                           'Hence,', 'Consequently,', 'And', 'But', 'Or'))):
                sentence = self.add_academic_transitions(sentence)

            # 3. Optionally convert to passive (simplified)
            if use_passive and random.random() < self.p_passive:
                sentence = self.convert_to_passive(sentence)

            # 4. Optionally replace words with synonyms
            if use_synonyms and random.random() < self.p_synonym_replacement:
                sentence = self.replace_with_synonyms(sentence)

            transformed_sentences.append(sentence)

        transformed_text = ' '.join(transformed_sentences)
        transformed_text = self._ensure_minimum_change(
            text,
            transformed_text,
            use_synonyms,
            "medium"
        )
        return self._cleanup_text(transformed_text)
    
    def _is_heading(self, line):
        """Determine if a line is likely a heading"""
        stripped = line.strip()
        if not stripped:
            return False
        # Short lines without sentence-ending punctuation are likely headings
        word_count = len(stripped.split())
        if word_count <= 10 and not stripped.endswith(('.', '!', '?')):
            return True
        # All-caps lines
        if stripped.isupper() and len(stripped) < 80:
            return True
        # Common academic section headers
        heading_starters = (
            'Introduction', 'Conclusion', 'Methodology', 'Results', 'Discussion',
            'Abstract', 'References', 'Appendix', 'Summary', 'Overview',
            'Concepts and', 'Concept and', 'Ensuring', 'Recommended',
            'Impact on', 'Step ', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5',
        )
        if stripped.startswith(heading_starters):
            return True
        # Pattern: "Step N", "Section N", "Part N", "Q2(A):", numbered headings
        if re.match(r'^(Step|Section|Part|Chapter|Phase|Q\d)\s*[\d(]', stripped, re.IGNORECASE):
            return True
        # Lines ending with a colon and fewer than 12 words (sub-headings)
        if stripped.endswith(':') and word_count <= 12:
            return True
        return False
    
    def _process_paragraph(
        self,
        paragraph,
        use_passive=False,
        use_synonyms=False,
        p_passive_val=0.2,
        p_synonym_val=0.3,
        p_transition_val=0.3,
        style='academic'
    ):
        """Process a full paragraph while preserving sentence structure"""
        try:
            doc = self.nlp(paragraph)
            transformed_sentences = []
            sentences_list = list(doc.sents)

            for i, sent in enumerate(sentences_list):
                sentence_str = sent.text.strip()

                # 1. Expand contractions
                sentence_str = self.expand_contractions(sentence_str)
                sentence_str = self.rewrite_common_phrases(sentence_str)

                # 2. Add academic transitions more intelligently
                # Only add transitions between sentences (not to the first sentence)
                # and only if the sentence doesn't already start with a transition
                if (i > 0 and random.random() < p_transition_val
                    and not sentence_str.startswith(('Moreover,', 'Furthermore,', 'Additionally,',
                                                   'However,', 'Nevertheless,', 'Therefore,',
                                                   'Hence,', 'Consequently,', 'And', 'But', 'Or'))):
                    sentence_str = self.add_academic_transitions(sentence_str)

                # 3. Optionally convert to passive
                if use_passive and random.random() < p_passive_val:
                    sentence_str = self.convert_to_passive(sentence_str)

                # 4. Advanced: Clause Swapping
                if random.random() < 0.2:
                    sentence_str = self._swap_clauses(sentence_str)

                # 5. Optionally replace words with synonyms
                if use_synonyms and random.random() < p_synonym_val:
                    sentence_str = self.replace_with_synonyms(sentence_str)
                
                # 6. Advanced: Add Mid-sentence Human Nuance
                if random.random() < 0.15:
                    sentence_str = self._add_human_nuance(sentence_str, style)

                # 7. NEW: Anti-Detection: Sentence Splitting
                if random.random() < 0.1:
                    fragments = self._split_long_sentences(sentence_str)
                    transformed_sentences.extend(fragments)
                else:
                    transformed_sentences.append(sentence_str)

            # 8. Anti-Detection: Sentence Shuffling
            if random.random() < 0.1:
                transformed_sentences = self._shuffle_sentences(transformed_sentences)

            # 9. Apply Burstiness to the paragraph
            transformed_sentences = self._apply_burstiness(transformed_sentences)

            transformed_text = ' '.join(transformed_sentences)
            transformed_text = self._ensure_minimum_change(
                paragraph,
                transformed_text,
                use_synonyms,
                "medium"
            )
            return self._cleanup_text(transformed_text)
        except Exception:
            # Fallback to basic processing
            return self._fallback_humanize(paragraph, use_passive, use_synonyms)

    def expand_contractions(self, sentence):
        result = sentence
        for contraction, expansion in CONTRACTION_MAP.items():
            pattern = r"\b" + re.escape(contraction) + r"\b"
            result = re.sub(
                pattern,
                lambda match: self._match_case(expansion, match.group(0)),
                result,
                flags=re.IGNORECASE
            )
        return result

    def rewrite_common_phrases(self, sentence):
        result = sentence
        for pattern, replacement in PHRASE_REWRITES.items():
            result = re.sub(
                pattern,
                lambda match: self._match_case(replacement, match.group(0)),
                result,
                flags=re.IGNORECASE
            )
        return result

    def add_academic_transitions(self, sentence):
        """Add academic transitions more intelligently"""
        # Only add transitions to sentences that don't already start with transitions
        # and don't start with certain words that indicate they're already connected
        if (sentence.startswith(('Moreover,', 'Furthermore,', 'Additionally,', 'However,',
                               'Nevertheless,', 'Therefore,', 'Hence,', 'Consequently,',
                               'In addition,', 'As a result', 'For this reason,'))
            or sentence.startswith(('And', 'But', 'Or', 'So', 'Yet'))):
            return sentence

        transition = random.choice(self.academic_transitions)
        
        # Lowercase the first word of the original sentence unless it's "I"
        words = sentence.split()
        if words and words[0].lower() != "i" and not words[0][0].isdigit():
            words[0] = words[0][0].lower() + words[0][1:]
        
        return f"{transition} {' '.join(words)}"

    def convert_to_passive(self, sentence):
        doc = self.nlp(sentence)
        # Avoid trying passive conversion when no dependency parser is available.
        if not any(token.dep_ for token in doc):
            return sentence

        subj_tokens = [t for t in doc if t.dep_ == 'nsubj' and t.head.dep_ == 'ROOT']
        dobj_tokens = [t for t in doc if t.dep_ == 'dobj']

        if subj_tokens and dobj_tokens:
            subject = subj_tokens[0]
            dobj = dobj_tokens[0]
            verb = subject.head
            
            # Avoid passive conversion for linking verbs (be, seem, etc.)
            if verb.lemma_.lower() in ("be", "seem", "become", "appear", "remain"):
                return sentence
                
            if subject.i < verb.i < dobj.i:
                # Find any auxiliary verbs
                aux_tokens = [t for t in doc if t.dep_ in ('aux', 'auxpass') and t.head == verb]

                participle = self._to_past_participle(verb)
                if not participle:
                    return sentence

                obj_text = ' '.join(tok.text for tok in dobj.subtree if not tok.is_punct)
                obj_text = self._to_subject_pronoun_phrase(obj_text)
                
                subj_text = ' '.join(tok.text for tok in subject.subtree if not tok.is_punct)
                subj_text = self._to_object_pronoun_phrase(subj_text)
                ending = sentence[-1] if sentence and sentence[-1] in ".!?" else ""

                if aux_tokens:
                    # Handle auxiliaries: "has forced" → "have been forced by"
                    aux_text = ' '.join(tok.text for tok in sorted(aux_tokens, key=lambda t: t.i))
                    processed_aux = self._process_auxiliary(aux_text, obj_text)
                    sentence = f"{obj_text.capitalize()} {processed_aux} {participle} by {subj_text}{ending}"
                else:
                    aux = self._select_passive_aux(verb, obj_text)
                    sentence = f"{obj_text.capitalize()} {aux} {participle} by {subj_text}{ending}"
        return sentence

    def _match_case(self, replacement, original):
        if original.isupper():
            return replacement.upper()
        if original and original[0].isupper():
            return replacement[0].upper() + replacement[1:]
        return replacement

    def _to_past_participle(self, verb_token):
        lemma = verb_token.lemma_.lower()
        if not lemma.isalpha():
            return None
        if lemma in IRREGULAR_PARTICIPLES:
            return IRREGULAR_PARTICIPLES[lemma]
        if lemma.endswith("e"):
            return f"{lemma}d"
        if len(lemma) > 2 and lemma.endswith("y") and lemma[-2] not in "aeiou":
            return f"{lemma[:-1]}ied"
        return f"{lemma}ed"

    def _select_passive_aux(self, verb_token, obj_text):
        obj_text_lower = obj_text.lower()
        is_plural_obj = obj_text_lower in ("we", "they", "them", "us") or obj_text_lower.endswith('s')
        is_i = obj_text_lower == "i"
        
        if verb_token.tag_ == "VBD": # Past
            if is_i: return "was"
            return "were" if is_plural_obj else "was"
        
        if verb_token.tag_ in ("VBP", "VB", "VBZ"): # Present classes
            if is_i: return "am"
            return "are" if is_plural_obj else "is"
            
        return "was"

    def _to_object_pronoun_phrase(self, phrase):
        mapping = {
            "i": "me", "we": "us", "he": "him", "she": "her", "they": "them", "who": "whom"
        }
        res = mapping.get(phrase.lower(), phrase)
        if phrase[0].isupper() and len(res) > 0:
            return res[0].upper() + res[1:]
        return res

    def _to_subject_pronoun_phrase(self, phrase):
        mapping = {
            "me": "i", "us": "we", "him": "he", "her": "she", "them": "they", "whom": "who"
        }
        clean = phrase.lower().strip()
        res = mapping.get(clean, phrase)
        if (phrase and phrase[0].isupper()) or (clean in mapping and clean == phrase.lower()):
            if res.lower() in mapping.values():
                return res.capitalize() if phrase and phrase[0].isupper() else res
        return res

    def replace_with_synonyms(self, sentence):
        tokens = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        # Increase replacement density for higher intensities
        density_divisor = 5 if self.synonym_replace_limit > 4 else 9
        max_replacements = max(1, min(self.synonym_replace_limit, len(tokens) // density_divisor + 1))
        replacements = 0

        new_tokens = []
        for (word, pos) in pos_tags:
            # Skip short words, blacklisted words, and non-content POS
            if (len(word) < 4
                or word.lower() in SYNONYM_BLACKLIST
                or (not word.isalpha())
                or not pos.startswith(('J', 'N', 'V', 'R'))
                or not wordnet.synsets(word)
                or replacements >= max_replacements):
                new_tokens.append(word)
                continue
            
            # Additional check: Skip if lemma is in blacklist
            lemma = wordnet.morphy(word.lower(), wordnet.VERB if pos.startswith('V') else wordnet.NOUN)
            if lemma and lemma in SYNONYM_BLACKLIST:
                new_tokens.append(word)
                continue

            if random.random() < 0.5:
                best_synonym = self._get_best_synonym(word, pos)
                if best_synonym:
                    # Match the case of the original word
                    if word[0].isupper():
                        best_synonym = best_synonym[0].upper() + best_synonym[1:]
                    
                    # Heuristic for pluralization: if original was plural noun, try to pluralize synonym
                    if pos == 'NNS' and (word.lower().endswith('s') or word.lower().endswith('es')) and not best_synonym.lower().endswith('s'):
                        best_synonym = self._inflect_noun(best_synonym, 'plural')
                    
                    # Tense Preservation for verbs
                    if pos.startswith('V'):
                        best_synonym = self._inflect_verb(best_synonym, pos)

                    new_tokens.append(best_synonym)
                    replacements += 1
                else:
                    new_tokens.append(word)
            else:
                new_tokens.append(word)

        return self._detokenize(new_tokens)

    def _get_best_synonym(self, word, pos):
        curated = CURATED_SYNONYMS.get(word.lower())
        if curated:
            return curated
        synonyms = self._get_synonyms(word, pos)
        if not synonyms:
            return None
        return self._select_closest_synonym(word, synonyms)

    def _get_synonyms(self, word, pos):
        wn_pos = None
        if pos.startswith('J'):
            wn_pos = wordnet.ADJ
        elif pos.startswith('N'):
            wn_pos = wordnet.NOUN
        elif pos.startswith('R'):
            wn_pos = wordnet.ADV
        elif pos.startswith('V'):
            wn_pos = wordnet.VERB

        synonyms = set()
        for syn in wordnet.synsets(word, pos=wn_pos):
            for lemma in syn.lemmas():
                lemma_name = lemma.name().replace('_', ' ')
                if (
                    lemma_name.lower() != word.lower()
                    and lemma_name.isalpha()
                    and len(lemma_name) <= 16
                    and len(lemma_name) >= 3
                ):
                    synonyms.add(lemma_name)
        return list(synonyms)

    def _select_closest_synonym(self, original_word, synonyms):
        if not synonyms:
            return None
        
        # If sentence transformers is not available, just return a random synonym
        if not SENTENCE_TRANSFORMERS_AVAILABLE or self.model is None:
            return random.choice(synonyms)
        
        try:
            original_emb = self.model.encode(original_word, convert_to_tensor=True)
            synonym_embs = self.model.encode(synonyms, convert_to_tensor=True)
            cos_scores = util.cos_sim(original_emb, synonym_embs)[0]
            
            # Sort synonyms by score descending
            scored_synonyms = []
            for idx, score in enumerate(cos_scores):
                scored_synonyms.append((synonyms[idx], score.item()))
            
            scored_synonyms.sort(key=lambda x: x[1], reverse=True)
            
            # Anti-Detection Strategy: Lexical Randomness
            # Aggressively pick non-top synonyms for high perplexity
            similarity_threshold = 0.5  # Loosen threshold for variety
            candidates = [s for s in scored_synonyms if s[1] >= similarity_threshold]
            if not candidates: return None
            
            # For heavier intensities, be even more random
            if len(candidates) >= 4 and random.random() < 0.5:
                # Pick from 2nd, 3rd, or 4th
                choice = random.choice(candidates[1:4])
                return choice[0]
            elif len(candidates) >= 2 and random.random() < 0.4:
                return candidates[1][0]
                
            return candidates[0][0]
        except Exception:
            return random.choice(synonyms)

    def _detokenize(self, tokens):
        text = ' '.join(tokens)
        # Fix punctuation spacing
        text = re.sub(r"\s+([,.;:!?])", r"\1", text)
        # Fix parentheses spacing
        text = re.sub(r"\(\s+", "(", text)
        text = re.sub(r"\s+\)", ")", text)
        # Only collapse apostrophes that are clearly part of contractions
        # (e.g. n 't -> n't), NOT expanded forms like 'do not'
        text = re.sub(r"(\w)\s+'\s*(t|s|re|ll|ve|d|m)\b", r"\1'\2", text)
        return text

    def _split_sentences(self, text):
        try:
            return nltk.sent_tokenize(text)
        except Exception:
            return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

    def _cleanup_text(self, text):
        """Final cleanup of text artifacts, punctuation, and normalization"""
        # Normalization (Wiki Cleanup Guide)
        text = text.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        text = text.replace('—', ' - ') # Reduce em-dash weight
        
        # Remove redundant transitions (e.g., "Additionally, Because")
        patterns = [
            r"\b(Moreover|Additionally|Furthermore|Therefore),?\s+(Because|Although|Since|While|However|As|If)\b",
            r"\b(Because|Although|Since|While|As|If),?\s+(Moreover|Additionally|Furthermore|Therefore|Consequently)\b"
        ]
        for pattern in patterns:
            text = re.sub(pattern, r"\2", text, flags=re.IGNORECASE)
            
        # Fix spacing artifacts WITHIN lines only (preserve newlines)
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)
        # Collapse multiple spaces to single space, but NOT newlines
        text = re.sub(r"[^\S\n]+", " ", text)
        # Normalize excessive blank lines (3+ newlines to 2)
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        # Final case fixing for sentences (within each line)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line:
                line = re.sub(r"(^|[.!?]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), line)
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()

    def _seed_for_request(self, text, use_passive, use_synonyms, preserve_structure, intensity, style):
        key = f"{text}|{use_passive}|{use_synonyms}|{preserve_structure}|{intensity}|{style}"
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        random.seed(int(digest[:16], 16))

    def _ensure_minimum_change(self, original, transformed, use_synonyms, intensity):
        if transformed.strip() == original.strip():
            transformed = self.rewrite_common_phrases(transformed)

        # If high intensity requested and output is too similar, force lexical changes.
        if intensity in ("heavy", "very_heavy") and use_synonyms:
            target_delta = 0.18 if intensity == "very_heavy" else 0.10
            if self._lexical_delta_ratio(original, transformed) < target_delta:
                # Be more aggressive: replace more words if possible
                tokens = transformed.split()
                for i in range(len(tokens)):
                    if self._lexical_delta_ratio(original, transformed) >= target_delta:
                        break
                    word = tokens[i].strip('.,!?:;')
                    if len(word) > 4 and word.lower() not in SYNONYM_BLACKLIST:
                        pos = nltk.pos_tag([word])[0][1]
                        if pos.startswith(('J', 'N', 'V', 'R')):
                            syn = self._get_best_synonym(word, pos)
                            if syn:
                                transformed = transformed.replace(word, syn, 1)
        return transformed

    def _de_slope_sentence(self, sentence):
        """Removes AI writing signature patterns (De-Sloping) based on WikiProject AI Cleanup"""
        # 1. Significance Scrubbing (Removing "pivotal moment", "evolving landscape", etc.)
        # Specific phrases first to avoid internal collisions
        slop_phrases = [
            (r"\bmarking\s+a\s+pivotal\s+moment\b", "being significant"),
            (r"\bkey\s+turning\s+point\b", "important change"),
            (r"\bevolving\s+.*?\s*landscape\b", "changing environment"),
            (r"\bfocal\s+point\b", "center"),
            (r"\bindelible\s+mark\b", "lasting impact"),
            (r"\bdeeply\s+rooted\s+in\b", "based on"),
            (r"\bintricate\s+interplay\b", "complex relationship"),
            (r"\bprofound\s+impact\b", "big effect"),
            (r"\bgroundbreaking\b", "new"),
            (r"\bserves\s+as\s+a\s+testament\s+to\b", "shows"),
            (r"\bstands\s+as\s+a\s+testament\s+to\b", "is a reminder of")
        ]
        for pattern, replacement in slop_phrases:
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)

        # 2. Copula Restoration: "serves as" -> "is", "boasts a" -> "has a"
        robotic_copulas = {
            r"\b(serves|stands)\s+as\b": "is",
            r"\b(marks|represents|shaping)\s+a\b": "is a",
            r"\b(boasts|features|offers)\s+a\b": "has a",
            r"\bis\s+a\s+testament\s+to\b": "is a reminder of",
            r"\bis\s+an\s+enduring\s+testament\s+to\b": "is a reminder of"
        }
        for pattern, replacement in robotic_copulas.items():
            sentence = re.sub(pattern, replacement, sentence, flags=re.IGNORECASE)

        # 3. Negative Parallelism Reduction: "Not only... but also..."
        sentence = re.sub(r"\bnot\s+only\s+(.*?)\s+but\s+also\s+(.*?)\b", r"\1 and \2", sentence, flags=re.IGNORECASE)

        return sentence

    def _inject_personality(self, sentence):
        """Injects subjective human reflections/opinions (The 'Soul')"""
        if random.random() > 0.3: # Don't overdo it
            return sentence
            
        markers = [
            "I keep thinking about how",
            "Honestly, it seems like",
            "I genuinely feel that",
            "The thing is, we often forget that",
            "It's kind of unsettling, but",
            "To be perfectly honest,",
            "I've always found it interesting that"
        ]
        
        # Only inject at the start if it doesn't already have a transition
        if not sentence.split()[0].endswith(','):
            prefix = random.choice(markers)
            # Adjust the first word of the sentence to lowercase
            words = sentence.split()
            if words:
                words[0] = words[0].lower() if words[0].lower() != "i" else words[0]
                return f"{prefix} {' '.join(words)}"
        return sentence

    def _inject_fillers(self, sentence, intensity):
        """Injects human-like hedge words using dependency parsing for natural placement"""
        if intensity not in ("heavy", "very_heavy") or random.random() > 0.5:
            return sentence
            
        fillers = [
            "essentially", "primarily", "reportedly", "arguably", "broadly speaking", 
            "basically", "relatively", "in a sense"
        ]
        
        try:
            doc = NLP_GLOBAL(sentence)
            # Find a good spot: right after the subject or the main verb
            candidates = []
            for token in doc:
                if token.dep_ in ("nsubj", "nsubjpass") and token.head.pos_ == "VERB":
                    candidates.append(token.i + 1)
                elif token.dep_ == "ROOT" and token.pos_ == "VERB":
                    candidates.append(token.i)
            
            if candidates:
                idx = random.choice(candidates)
                filler = random.choice(fillers)
                words = [t.text for t in doc]
                words.insert(idx, filler)
                return " ".join(words)
        except:
            pass # Fallback to original simple splitting if spaCy fails
            
        return sentence

    def _apply_rhythmic_variety(self, sentences):
        """Enforces a mix of sentence lengths (Short-Long-Short)"""
        if len(sentences) < 3: return sentences
        
        new_sentences = []
        for i, s in enumerate(sentences):
            # Every 3rd sentence, try to make it "punchy" (short)
            if i % 3 == 2 and len(s.split()) > 12:
                # Find a comma or 'and' to truncate
                doc = NLP_GLOBAL(s)
                found_split = False
                for token in doc:
                    if token.text.lower() in (",", "and", "but") and 5 < token.i < 10:
                        new_sentences.append(doc[:token.i].text + ".")
                        # If there's a lot left, add it as a separate sentence
                        if len(doc) - token.i > 5:
                            remaining = doc[token.i+1:].text
                            if remaining:
                                new_sentences.append(remaining[0].upper() + remaining[1:])
                        found_split = True
                        break
                if not found_split:
                    new_sentences.append(s)
            else:
                new_sentences.append(s)
        return new_sentences

    def _lexical_delta_ratio(self, original, transformed):
        original_words = re.findall(r"\b\w+\b", original.lower())
        transformed_words = re.findall(r"\b\w+\b", transformed.lower())
        if not original_words:
            return 0.0
        changed = sum(1 for a, b in zip(original_words, transformed_words) if a != b)
        changed += abs(len(original_words) - len(transformed_words))
        return changed / max(1, len(original_words))

    def _swap_clauses(self, sentence):
        """Swaps subordinating clauses for structural variety"""
        # Example: "Because it rained, the game was off" -> "The game was off because it rained"
        doc = self.nlp(sentence)
        if len(doc) < 8: return sentence

        # Look for subordinating conjunction at the start
        first_token = doc[0]
        if first_token.pos_ == "SCONJ" or first_token.text.lower() in ["although", "because", "since", "while", "though"]:
            # Find the comma that separates the clauses
            comma_idx = -1
            for i, token in enumerate(doc):
                if token.text == "," and token.head.pos_ == "VERB":
                    comma_idx = i
                    break
            
            if comma_idx > 2 and comma_idx < len(doc) - 3:
                # We have a candidate for swapping
                clause_a = doc[0:comma_idx].text
                clause_b = doc[comma_idx+1:].text.strip()
                
                # Clean up punctuation from clause_b
                ending = ""
                if clause_b and clause_b[-1] in ".!?":
                    ending = clause_b[-1]
                    clause_b = clause_b[:-1]
                
                # Lowercase the first word of the original first clause, except 'I'
                clause_a_words = clause_a.split()
                if clause_a_words:
                    clause_a_words[0] = clause_a_words[0].lower() if clause_a_words[0].lower() != "i" else clause_a_words[0]
                clause_a = " ".join(clause_a_words)
                
                # Uppercase the first word of the new first clause
                clause_b_words = clause_b.split()
                if clause_b_words:
                    clause_b_words[0] = clause_b_words[0].capitalize()
                clause_b = " ".join(clause_b_words)
                
                return f"{clause_b} {clause_a}{ending}"
        
        return sentence

    def _apply_burstiness(self, sentences):
        """Diverges sentence lengths by joining short ones or splitting long ones"""
        if len(sentences) < 2: return sentences
        
        new_sentences = []
        i = 0
        while i < len(sentences):
            curr = sentences[i].strip()
            
            # 1. Join two very short sentences
            if i + 1 < len(sentences):
                next_sent = sentences[i+1].strip()
                curr_len = len(curr.split())
                next_len = len(next_sent.split())
                
                # Join logic: short + moderately short sentences
                if curr_len < 8 and next_len < 12 and not curr.endswith("?"):
                    # Join with a semicolon, em-dash or conjunction
                    connector = random.choice([";", "—", ", and", ", while"])
                    
                    # Remove ending punctuation from first sentence
                    if curr.endswith((".", "!", "?")): 
                        curr = curr[:-1]
                    
                    # Lowercase the next sentence's first words intelligently
                    next_words = next_sent.split()
                    if next_words:
                        # Lowercase first word if it's not "I"
                        if next_words[0].lower() != "i":
                            # Maintain the comma if it exists but lowercase the word
                            if next_words[0].endswith(","):
                                next_words[0] = next_words[0][:-1].lower() + ","
                            else:
                                next_words[0] = next_words[0].lower()
                        
                        # Special case: If the first word was a transition like "Additionally," 
                        # then lowercase the SECOND word too
                        if len(next_words) > 1 and next_sent.startswith(("Moreover,", "Additionally,", "Furthermore,", "Hence,", "Therefore,")):
                             if next_words[1].lower() != "i":
                                 next_words[1] = next_words[1].lower()
                    
                    next_sent_fixed = " ".join(next_words)
                    new_sentences.append(f"{curr}{connector} {next_sent_fixed}")
                    i += 2
                    continue
            
            new_sentences.append(curr)
            i += 1
            
        return new_sentences

    def _add_human_nuance(self, sentence, style):
        """Adds subtle human nuances like mid-sentence fillers or intensifiers"""
        words = sentence.split()
        if len(words) < 10: return sentence
        
        # Style-dependent nuances
        nuances = {
            "academic": ["primarily", "essentially", "effectively", "specifically", "namely"],
            "professional": ["actually", "particularly", "rather", "distinctly", "frequent"],
            "formal": ["it should be understood that", "it is evident that", "notably"]
        }
        
        options = nuances.get(style, nuances["academic"])
        filler = random.choice(options)
        
        # Find a good place to insert (e.g. after a verb or comma)
        doc = self.nlp(sentence)
        insertion_idx = -1
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                insertion_idx = token.i + 1
                break
        
        if insertion_idx > 0 and insertion_idx < len(doc) - 2:
            sent_tokens = [t.text for t in doc]
            sent_tokens.insert(insertion_idx, filler)
            return self._detokenize(sent_tokens)
        return sentence
            
    def _convert_to_active(self, sentence):
        """Converts passive voice to active for natural rhythm variety"""
        # Example: "The book was read by John" -> "John read the book"
        doc = self.nlp(sentence)
        auxpass_tokens = [t for t in doc if t.dep_ == 'auxpass']
        if not auxpass_tokens: return sentence

        # Find agent (by phrase)
        agent_tokens = [t for t in doc if t.dep_ == 'agent']
        if not agent_tokens: return sentence

        pobj_tokens = [t for t in agent_tokens[0] if t.dep_ == 'pobj']
        if not pobj_tokens: return sentence

        # Find subject of passive sentence (the original object)
        nsubjpass_tokens = [t for t in doc if t.dep_ == 'nsubjpass']
        if not nsubjpass_tokens: return sentence

        # Find verb
        verb = nsubjpass_tokens[0].head
        
        # Construct active sentence
        agent_text = ' '.join(tok.text for tok in pobj_tokens[0].subtree)
        object_text = ' '.join(tok.text for tok in nsubjpass_tokens[0].subtree)
        
        # Determine tense from auxpass ("was/were" -> past, "is/are" -> present)
        auxpass = auxpass_tokens[0].text.lower()
        is_past = auxpass in ("was", "were", "been")
        is_plural_agent = pobj_tokens[0].tag_ in ("NNS", "NNPS") or agent_text.lower() in ("we", "they")
        
        # Get base tense of verb
        lemma = verb.lemma_.lower()
        if is_past:
            # Try to get past tense: prefer VBD tag if exists, otherwise heuristic
            if lemma == "be": active_verb = "was" if not is_plural_agent else "were"
            elif lemma == "go": active_verb = "went"
            elif lemma == "take": active_verb = "took"
            elif lemma == "do": active_verb = "did"
            elif lemma == "see": active_verb = "saw"
            elif lemma == "make": active_verb = "made"
            elif lemma == "find": active_verb = "found"
            else:
                # Heuristic for regular past
                active_verb = lemma + ("ed" if not lemma.endswith("e") else "d")
                if len(lemma) > 2 and lemma.endswith("y") and lemma[-2] not in "aeiou":
                    active_verb = lemma[:-1] + "ied"
        else:
            # Present tense
            if is_plural_agent or agent_text.lower() == "i":
                active_verb = lemma
            else:
                # 3rd person singular
                if lemma.endswith(("s", "x", "ch", "sh", "z")): active_verb = lemma + "es"
                elif len(lemma) > 2 and lemma.endswith("y") and lemma[-2] not in "aeiou": active_verb = lemma[:-1] + "ies"
                else: active_verb = lemma + "s"

        ending = sentence[-1] if sentence and sentence[-1] in ".!?" else ""
        
        # Construct: Y did X
        return f"{agent_text.capitalize()} {active_verb} {object_text}{ending}"

    def _split_long_sentences(self, sentence):
        """Splits long sentences at conjunctions to increase burstiness"""
        doc = self.nlp(sentence)
        if len(doc) <= 15: return [sentence]
        
        # Look for conjunctions (and, but, although, while) that separate clauses
        split_point = -1
        for token in doc:
            # Look for coordinating conjunctions or subordinating conjunctions in the middle
            # Exclude "that" as it often follows "it seems" or other hedges
            if token.pos_ == "CCONJ" or (token.pos_ == "SCONJ" and token.i > 5 and token.text.lower() != "that"):
                # Ensure it has a verb as a children or head (likely a clause)
                if any(child.pos_ == "VERB" for child in token.head.children) or token.head.pos_ == "VERB":
                    # Check if it's roughly in the middle (between 30% and 70%)
                    pos_ratio = token.i / len(doc)
                    if 0.3 < pos_ratio < 0.7:
                        split_point = token.i
                        break
        
        if split_point != -1:
            # Split into two
            part1 = doc[0:split_point].text.strip()
            # If it ends with a comma, remove it
            if part1.endswith(","): part1 = part1[:-1]
            
            connector = doc[split_point].text
            part2 = doc[split_point+1:].text.strip()
            
            # Combine based on connector type
            if connector.lower() in ["and", "but", "so", "yet"]:
                # "Part 1. Connector, part 2."
                return [f"{part1}.", f"{connector.capitalize()}, {part2}"]
            else:
                # Just split
                return [f"{part1}.", f"{connector.capitalize()} {part2}"]
                
        return [sentence]

    def _shuffle_sentences(self, sentences):
        """Occasionally swaps non-linked sentences to break AI patterns"""
        if len(sentences) < 3: return sentences
        
        # Candidate pairs: adjacent sentences that don't start with transitions
        candidates = []
        for i in range(len(sentences) - 1):
            s1 = sentences[i].strip()
            s2 = sentences[i+1].strip()
            
            # Don't swap if either starts with a known transition or link word
            links = ("however", "therefore", "moreover", "additionally", "first", "second", "finally", "then", "consequently", "but", "and", "it", "this")
            if not s1.lower().startswith(links) and not s2.lower().startswith(links):
                # Don't swap if s1 is very short (could be a heading or intro)
                if len(s1.split()) > 5:
                    candidates.append(i)
        
        if candidates and random.random() < getattr(self, 'p_shuffle', 0.1):
            idx = random.choice(candidates)
            sentences[idx], sentences[idx+1] = sentences[idx+1], sentences[idx]
            
        return sentences

    def _inflect_noun(self, word, form='plural'):
        lemma = word.lower()
        if form == 'plural':
            if lemma.endswith(('ch', 'sh', 'x', 's', 'z')): return word + "es"
            if len(lemma) > 2 and lemma.endswith('y') and lemma[-2] not in 'aeiou': return word[:-1] + "ies"
            return word + "s"
        return word

    def _inflect_verb(self, word, pos):
        """Inflects a verb lemma based on the desired POS tag"""
        lemma = word.lower()
        
        # Mapping common irregular past/participle forms for inflection
        # Note: IRREGULAR_PARTICIPLES is available globally for VBN
        irregular_vbd = {
            "take": "took", "go": "went", "be": "was", "do": "did", "see": "saw",
            "find": "found", "make": "made", "give": "gave", "get": "got",
            "say": "said", "come": "came", "think": "thought", "know": "knew"
        }
        
        if pos == 'VBD': # Past tense
            if lemma in irregular_vbd: return irregular_vbd[lemma]
            if lemma.endswith('e'): return word + 'd'
            if len(lemma) > 2 and lemma.endswith('y') and lemma[-2] not in 'aeiou': return word[:-1] + 'ied'
            return word + 'ed'
        
        if pos == 'VBN': # Past participle
            if lemma in IRREGULAR_PARTICIPLES: return IRREGULAR_PARTICIPLES[lemma]
            if lemma.endswith('e'): return word + 'd'
            if len(lemma) > 2 and lemma.endswith('y') and lemma[-2] not in 'aeiou': return word[:-1] + 'ied'
            return word + 'ed'
            
        if pos == 'VBZ': # 3rd person singular present
            if lemma == 'be': return 'is'
            if lemma == 'have': return 'has'
            if lemma.endswith(('s', 'x', 'ch', 'sh', 'z')): return word + 'es'
            if len(lemma) > 2 and lemma.endswith('y') and lemma[-2] not in 'aeiou': return word[:-1] + 'ies'
            return word + 's'
            
        if pos == 'VBG': # Gerund / present participle
            if lemma.endswith('e') and not lemma == 'be': return word[:-1] + 'ing'
            return word + 'ing'
            
        return word
    def _process_auxiliary(self, aux_text, obj_text):
        """Processes auxiliary verbs for correct passive voice and agreement"""
        obj_text_lower = obj_text.lower()
        is_plural_obj = obj_text_lower in ("we", "they", "them", "us") or obj_text_lower.endswith('s')
        
        aux_lower = aux_text.lower()
        
        # Handle "has/have/had"
        if "had" in aux_lower:
            return "had been"
        if "has" in aux_lower or "have" in aux_lower:
            return "have been" if is_plural_obj else "has been"
            
        # Handle "is/are/was/were"
        if "was" in aux_lower or "were" in aux_lower:
            main_aux = "were" if is_plural_obj else "was"
            return f"{main_aux} being"
        if "is" in aux_lower or "are" in aux_lower:
            main_aux = "are" if is_plural_obj else "is"
            return f"{main_aux} being"
            
        # Handle modals (can, will, should, etc.)
        return f"{aux_text} be"

    def _apply_intense_burstiness(self, sentences):
        """Randomly joins sentences to create complex human-like rhythm"""
        if len(sentences) < 3: return sentences
        
        new_sentences = []
        i = 0
        while i < len(sentences):
            if i < len(sentences) - 1 and random.random() < 0.4:
                # Join sentences with a semicolon or conjunction
                s1 = sentences[i].strip()
                s2 = sentences[i+1].strip()
                # Remove period from s1
                if s1.endswith('.'): s1 = s1[:-1]
                # Lowercase first word of s2
                s2_tokens = s2.split()
                if s2_tokens: s2_tokens[0] = s2_tokens[0].lower() if s2_tokens[0].lower() != "i" else s2_tokens[0]
                
                connector = random.choice([";", "; additionally,", ", and", "\u2014"])
                new_sentences.append(f"{s1}{connector} {' '.join(s2_tokens)}")
                i += 2
            else:
                new_sentences.append(sentences[i])
                i += 1
        return new_sentences

    def _inject_personality(self, sentence):
        """Injects subjective human reflections/opinions (The 'Soul')"""
        if random.random() > 0.3: # Don't overdo it
            return sentence
            
        markers = [
            "I keep thinking about how",
            "Honestly, it seems like",
            "I genuinely feel that",
            "The thing is, we often forget that",
            "It's kind of unsettling, but",
            "To be perfectly honest,",
            "I've always found it interesting that"
        ]
        
        # Only inject at the start if it doesn't already have a transition
        if not sentence.split()[0].endswith(','):
            prefix = random.choice(markers)
            # Adjust the first word of the sentence to lowercase
            words = sentence.split()
            if words:
                words[0] = words[0].lower() if words[0].lower() != "i" else words[0]
                return f"{prefix} {' '.join(words)}"
        return sentence

    def _inject_fillers(self, sentence, intensity):
        """Injects human-like hedge words using dependency parsing for natural placement"""
        if intensity not in ("heavy", "very_heavy") or random.random() > 0.5:
            return sentence
            
        fillers = [
            "essentially", "primarily", "reportedly", "arguably", "broadly speaking", 
            "basically", "relatively", "in a sense"
        ]
        
        try:
            doc = NLP_GLOBAL(sentence)
            # Find a good spot: right after the subject or the main verb
            candidates = []
            for token in doc:
                if token.dep_ in ("nsubj", "nsubjpass") and token.head.pos_ == "VERB":
                    candidates.append(token.i + 1)
                elif token.dep_ == "ROOT" and token.pos_ == "VERB":
                    candidates.append(token.i)
            
            if candidates:
                idx = random.choice(candidates)
                filler = random.choice(fillers)
                words = [t.text for t in doc]
                words.insert(idx, filler)
                return " ".join(words)
        except:
            # Simple fallback if spaCy dependency info is limited
            tokens = sentence.split()
            if len(tokens) > 10:
                idx = random.randint(2, min(len(tokens) - 3, 8))
                tokens.insert(idx, random.choice(fillers))
                return " ".join(tokens)
            
        return sentence

    def _apply_rhythmic_variety(self, sentences):
        """Enforces a mix of sentence lengths (Short-Long-Short)"""
        if len(sentences) < 3: return sentences
        
        new_sentences = []
        for i, s in enumerate(sentences):
            # Every 3rd sentence, try to make it "punchy" (short)
            if i % 3 == 2 and len(s.split()) > 12:
                # Find a comma or 'and' to truncate
                try:
                    doc = NLP_GLOBAL(s)
                    found_split = False
                    for token in doc:
                        if token.text.lower() in (",", "and", "but") and 5 < token.i < 10:
                            new_sentences.append(doc[:token.i].text + ".")
                            # If there's a lot left, add it as a separate sentence
                            if len(doc) - token.i > 5:
                                remaining = doc[token.i+1:].text
                                if remaining:
                                    new_sentences.append(remaining[0].upper() + remaining[1:])
                            found_split = True
                            break
                    if not found_split:
                        new_sentences.append(s)
                except:
                    new_sentences.append(s)
            else:
                new_sentences.append(s)
        return new_sentences
