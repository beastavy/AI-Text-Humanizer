import ssl
import random
import warnings

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

        # Common academic transitions
        self.academic_transitions = [
            "Moreover,", "Additionally,", "Furthermore,", "Hence,", 
            "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,"
        ]

    def humanize_text(self, text, use_passive=False, use_synonyms=False, preserve_structure=False):
        if preserve_structure:
            # Structure preservation mode
            lines = text.split('\n')
            transformed_lines = []

            for line in lines:
                line = line.strip()

                # Skip empty lines but preserve them
                if not line:
                    transformed_lines.append('')
                    continue

                # Check if line looks like a heading
                if self._is_heading(line):
                    # Process heading with minimal changes
                    processed_heading = self.expand_contractions(line)
                    transformed_lines.append(processed_heading)
                else:
                    # Process as regular paragraph
                    processed_paragraph = self._process_paragraph(line, use_passive, use_synonyms)
                    transformed_lines.append(processed_paragraph)

            return '\n'.join(transformed_lines)
        else:
            # Original single-paragraph mode (default) - ensure transformations happen
            try:
                doc = self.nlp(text)
                transformed_sentences = []
                sentences_list = list(doc.sents)

                for i, sent in enumerate(sentences_list):
                    sentence_str = sent.text.strip()

                    # 1. Expand contractions (always do this)
                    sentence_str = self.expand_contractions(sentence_str)

                    # 2. Add academic transitions more intelligently
                    # Only add transitions between sentences (not to the first sentence)
                    # and only if the sentence doesn't already start with a transition
                    if (i > 0 and random.random() < self.p_academic_transition
                        and not sentence_str.startswith(('Moreover,', 'Furthermore,', 'Additionally,',
                                                       'However,', 'Nevertheless,', 'Therefore,',
                                                       'Hence,', 'Consequently,', 'And', 'But', 'Or'))):
                        sentence_str = self.add_academic_transitions(sentence_str)

                    # 3. Optionally convert to passive
                    if use_passive and random.random() < self.p_passive:
                        sentence_str = self.convert_to_passive(sentence_str)

                    # 4. Optionally replace words with synonyms
                    if use_synonyms and random.random() < self.p_synonym_replacement:
                        sentence_str = self.replace_with_synonyms(sentence_str)

                    transformed_sentences.append(sentence_str)

                return ' '.join(transformed_sentences)
            except Exception as e:
                # If spaCy fails, fall back to basic processing
                return self._fallback_humanize(text, use_passive, use_synonyms)
    
    def _fallback_humanize(self, text, use_passive=False, use_synonyms=False):
        """Fallback humanization when spaCy fails"""
        sentences = nltk.sent_tokenize(text)
        transformed_sentences = []

        for i, sentence in enumerate(sentences):
            # 1. Expand contractions (always do this)
            sentence = self.expand_contractions(sentence)

            # 2. Add academic transitions
            if (i > 0 and random.random() < self.p_academic_transition
                and not sentence.startswith(('Moreover,', 'Furthermore,', 'Additionally,',
                                           'However,', 'Nevertheless,', 'Therefore,',
                                           'Hence,', 'Consequently,', 'And', 'But', 'Or'))):
                sentence = self.add_academic_transitions(sentence)

            # 3. Optionally convert to passive (simplified)
            if use_passive and random.random() < self.p_passive:
                # Simple passive conversion fallback
                words = sentence.split()
                for j, word in enumerate(words):
                    if word.lower() in ['is', 'are', 'was', 'were', 'be', 'been', 'being']:
                        if j + 1 < len(words):
                            words[j] = word.lower()
                            if words[j+1].endswith('ing'):
                                words[j+1] = 'being ' + words[j+1]
                            break

            # 4. Optionally replace words with synonyms
            if use_synonyms and random.random() < self.p_synonym_replacement:
                sentence = self.replace_with_synonyms(sentence)

            transformed_sentences.append(sentence)

        return ' '.join(transformed_sentences)
    
    def _is_heading(self, line):
        """Determine if a line is likely a heading"""
        if len(line.split()) <= 8 and not line.endswith(('.', '!', '?')):
            return True
        if line.isupper() and len(line) < 50:
            return True
        if line.startswith(('Introduction', 'Conclusion', 'Methodology', 'Results', 'Discussion', 'Abstract')):
            return True
        return False
    
    def _process_paragraph(self, paragraph, use_passive=False, use_synonyms=False):
        """Process a full paragraph while preserving sentence structure"""
        try:
            doc = self.nlp(paragraph)
            transformed_sentences = []
            sentences_list = list(doc.sents)

            for i, sent in enumerate(sentences_list):
                sentence_str = sent.text.strip()

                # 1. Expand contractions
                sentence_str = self.expand_contractions(sentence_str)

                # 2. Add academic transitions more intelligently
                # Only add transitions between sentences (not to the first sentence)
                # and only if the sentence doesn't already start with a transition
                if (i > 0 and random.random() < self.p_academic_transition
                    and not sentence_str.startswith(('Moreover,', 'Furthermore,', 'Additionally,',
                                                   'However,', 'Nevertheless,', 'Therefore,',
                                                   'Hence,', 'Consequently,', 'And', 'But', 'Or'))):
                    sentence_str = self.add_academic_transitions(sentence_str)

                # 3. Optionally convert to passive
                if use_passive and random.random() < self.p_passive:
                    sentence_str = self.convert_to_passive(sentence_str)

                # 4. Optionally replace words with synonyms
                if use_synonyms and random.random() < self.p_synonym_replacement:
                    sentence_str = self.replace_with_synonyms(sentence_str)

                transformed_sentences.append(sentence_str)

            return ' '.join(transformed_sentences)
        except Exception:
            # Fallback to basic processing
            return self._fallback_humanize(paragraph, use_passive, use_synonyms)

    def expand_contractions(self, sentence):
        contraction_map = {
            "n't": " not", "'re": " are", "'s": " is", "'ll": " will",
            "'ve": " have", "'d": " would", "'m": " am"
        }
        tokens = word_tokenize(sentence)
        expanded_tokens = []
        for token in tokens:
            lower_token = token.lower()
            replaced = False
            for contraction, expansion in contraction_map.items():
                if contraction in lower_token and lower_token.endswith(contraction):
                    new_token = lower_token.replace(contraction, expansion)
                    if token[0].isupper():
                        new_token = new_token.capitalize()
                    expanded_tokens.append(new_token)
                    replaced = True
                    break
            if not replaced:
                expanded_tokens.append(token)

        return ' '.join(expanded_tokens)

    def add_academic_transitions(self, sentence):
        """Add academic transitions more intelligently"""
        # Only add transitions to sentences that don't already start with transitions
        # and don't start with certain words that indicate they're already connected
        if (sentence.startswith(('Moreover,', 'Furthermore,', 'Additionally,', 'However,',
                               'Nevertheless,', 'Therefore,', 'Hence,', 'Consequently,',
                               'In addition,', 'As a result,', 'For this reason,'))
            or sentence.startswith(('And', 'But', 'Or', 'So', 'Yet', 'The', 'This', 'It'))):
            return sentence

        transition = random.choice(self.academic_transitions)
        return f"{transition} {sentence}"

    def convert_to_passive(self, sentence):
        doc = self.nlp(sentence)
        subj_tokens = [t for t in doc if t.dep_ == 'nsubj' and t.head.dep_ == 'ROOT']
        dobj_tokens = [t for t in doc if t.dep_ == 'dobj']

        if subj_tokens and dobj_tokens:
            subject = subj_tokens[0]
            dobj = dobj_tokens[0]
            verb = subject.head
            if subject.i < verb.i < dobj.i:
                passive_str = f"{dobj.text} {verb.lemma_} by {subject.text}"
                original_str = ' '.join(token.text for token in doc)
                chunk = f"{subject.text} {verb.text} {dobj.text}"
                if chunk in original_str:
                    sentence = original_str.replace(chunk, passive_str)
        return sentence

    def replace_with_synonyms(self, sentence):
        tokens = word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)

        new_tokens = []
        for (word, pos) in pos_tags:
            if pos.startswith(('J', 'N', 'V', 'R')) and wordnet.synsets(word):
                if random.random() < 0.5:
                    synonyms = self._get_synonyms(word, pos)
                    if synonyms:
                        best_synonym = self._select_closest_synonym(word, synonyms)
                        new_tokens.append(best_synonym if best_synonym else word)
                    else:
                        new_tokens.append(word)
                else:
                    new_tokens.append(word)
            else:
                new_tokens.append(word)

        return ' '.join(new_tokens)

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
                if lemma_name.lower() != word.lower():
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
            max_score_index = cos_scores.argmax().item()
            max_score = cos_scores[max_score_index].item()
            if max_score >= 0.5:
                return synonyms[max_score_index]
            return None
        except Exception:
            # Fallback to random selection if there's an error
            return random.choice(synonyms)