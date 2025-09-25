// AI Text Humanizer Pro - JavaScript Logic

class TextHumanizer {
    constructor() {
        this.contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "won't": "will not", "can't": "cannot", "couldn't": "could not",
            "wouldn't": "would not", "shouldn't": "should not", "mustn't": "must not",
            "isn't": "is not", "aren't": "are not", "wasn't": "was not",
            "weren't": "were not", "hasn't": "has not", "haven't": "have not",
            "hadn't": "had not",
            "I'm": "I am", "you're": "you are", "he's": "he is", "she's": "she is",
            "we're": "we are", "they're": "they are", "I'll": "I will",
            "you'll": "you will", "he'll": "he will", "she'll": "she will",
            "we'll": "we will", "they'll": "they will", "I've": "I have",
            "you've": "you have", "we've": "we have", "they've": "they have",
            "I'd": "I would", "you'd": "you would", "he'd": "he would",
            "she'd": "she would", "we'd": "we would", "they'd": "they would",
            "it's": "it is", "that's": "that is", "there's": "there is",
            "here's": "here is", "what's": "what is", "who's": "who is",
            "where's": "where is", "when's": "when is", "why's": "why is",
            "how's": "how is"
        };

        this.transitions = [
            "Moreover,", "Additionally,", "Furthermore,", "Hence,", 
            "Therefore,", "Consequently,", "Nonetheless,", "Nevertheless,"
        ];

        this.synonyms = {
            "good": "excellent", "bad": "poor", "big": "significant", "small": "minimal",
            "important": "crucial", "easy": "straightforward", "hard": "challenging",
            "help": "assist", "use": "utilize", "get": "obtain", "make": "create",
            "show": "demonstrate", "tell": "inform", "ask": "inquire", "try": "attempt",
            "start": "commence", "end": "conclude", "find": "discover", "know": "understand",
            "think": "consider", "feel": "perceive", "want": "desire", "need": "require",
            "like": "appreciate", "hate": "dislike", "love": "adore", "see": "observe",
            "hear": "perceive", "say": "state", "go": "proceed", "come": "arrive",
            "give": "provide", "take": "accept", "put": "place", "keep": "maintain",
            "let": "allow", "turn": "rotate", "move": "relocate", "work": "function",
            "play": "engage", "run": "operate", "walk": "proceed", "sit": "position",
            "stand": "position", "lie": "recline", "sleep": "rest", "eat": "consume",
            "drink": "consume", "buy": "purchase", "sell": "vend", "pay": "compensate",
            "cost": "expense", "price": "value", "money": "currency", "time": "duration",
            "day": "period", "night": "evening", "morning": "dawn", "afternoon": "midday",
            "evening": "dusk", "week": "period", "month": "period", "year": "period"
        };

        this.sampleTexts = [
            "I don't think this approach will work. It's not good enough for our needs. We can't implement it without proper planning. The team needs to understand the requirements better before we proceed.",
            "You're right about the issue. We should fix it as soon as possible. It's important to get this done quickly. Let me know if you need any help with the implementation.",
            "The project is going well. We've made good progress this week. The team is working hard and we're on track to meet our deadlines. I think we can finish everything on time.",
            "This is a great idea! We should definitely try it. It might help us solve the problem we've been having. Let's discuss it in the next meeting and see what everyone thinks.",
            "I'm not sure about this solution. It seems too complicated for what we need. Maybe we should look for a simpler approach. What do you think about trying something different?"
        ];
    }

    expandContractions(text) {
        let result = text;
        for (const [contraction, expansion] of Object.entries(this.contractions)) {
            const pattern = new RegExp(`\\b${this.escapeRegExp(contraction)}\\b`, 'gi');
            result = result.replace(pattern, expansion);
        }
        return result;
    }

    addAcademicTransitions(text) {
        const sentences = text.split('. ');
        if (sentences.length > 1) {
            for (let i = 1; i < sentences.length; i++) {
                if (Math.random() < 0.3) {
                    const transition = this.transitions[Math.floor(Math.random() * this.transitions.length)];
                    sentences[i] = `${transition} ${sentences[i]}`;
                }
            }
        }
        return sentences.join('. ');
    }

    convertToPassive(text) {
        const sentences = text.split('. ');
        const passiveSentences = [];
        
        for (let sentence of sentences) {
            if (Math.random() < 0.2) {
                sentence = sentence.replace(/\bI do\b/gi, "It is done by me");
                sentence = sentence.replace(/\bwe can\b/gi, "it can be done by us");
                sentence = sentence.replace(/\byou should\b/gi, "it should be done by you");
                sentence = sentence.replace(/\bthey will\b/gi, "it will be done by them");
                sentence = sentence.replace(/\bI will\b/gi, "it will be done by me");
                sentence = sentence.replace(/\bwe will\b/gi, "it will be done by us");
            }
            passiveSentences.push(sentence);
        }
        
        return passiveSentences.join('. ');
    }

    replaceWithSynonyms(text) {
        let result = text;
        for (const [word, synonym] of Object.entries(this.synonyms)) {
            const pattern = new RegExp(`\\b${this.escapeRegExp(word)}\\b`, 'gi');
            if (Math.random() < 0.3) {
                result = result.replace(pattern, synonym);
            }
        }
        return result;
    }

    humanizeText(text, options = {}) {
        if (!text.trim()) return text;

        let result = text;

        // Step 1: Expand contractions
        result = this.expandContractions(result);

        // Step 2: Add academic transitions
        result = this.addAcademicTransitions(result);

        // Step 3: Convert to passive voice (if enabled)
        if (options.usePassive) {
            result = this.convertToPassive(result);
        }

        // Step 4: Replace with synonyms (if enabled)
        if (options.useSynonyms) {
            result = this.replaceWithSynonyms(result);
        }

        // Step 5: Apply intensity
        if (options.intensity === 'heavy') {
            result = this.addMoreFormality(result);
        }

        return result;
    }

    addMoreFormality(text) {
        // Add more formal language patterns
        let result = text;
        
        // Replace informal phrases
        const formalReplacements = {
            "a lot of": "numerous",
            "lots of": "many",
            "a bunch of": "several",
            "kind of": "somewhat",
            "sort of": "rather",
            "pretty much": "essentially",
            "in a way": "to some extent",
            "at the end of the day": "ultimately",
            "when it comes to": "regarding",
            "as far as": "concerning"
        };

        for (const [informal, formal] of Object.entries(formalReplacements)) {
            const pattern = new RegExp(this.escapeRegExp(informal), 'gi');
            result = result.replace(pattern, formal);
        }

        return result;
    }

    escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    countWords(text) {
        return text.trim().split(/\s+/).filter(word => word.length > 0).length;
    }

    countSentences(text) {
        return text.split(/[.!?]+/).filter(sentence => sentence.trim().length > 0).length;
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    const humanizer = new TextHumanizer();
    
    // Get DOM elements
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const transformBtn = document.getElementById('transformBtn');
    const copyBtn = document.getElementById('copyBtn');
    const outputSection = document.getElementById('outputSection');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const successToast = document.getElementById('successToast');
    
    // Configuration elements
    const usePassive = document.getElementById('usePassive');
    const useSynonyms = document.getElementById('useSynonyms');
    const preserveStructure = document.getElementById('preserveStructure');
    const intensity = document.getElementById('intensity');
    const style = document.getElementById('style');
    
    // Quick action buttons
    const loadSample = document.getElementById('loadSample');
    const clearAll = document.getElementById('clearAll');
    
    // Statistics elements
    const inputWords = document.getElementById('inputWords');
    const inputSentences = document.getElementById('inputSentences');
    const outputWords = document.getElementById('outputWords');
    const outputSentences = document.getElementById('outputSentences');

    // Transform button click handler
    transformBtn.addEventListener('click', function() {
        const text = inputText.value.trim();
        
        if (!text) {
            showToast('Please enter some text to transform.', 'error');
            return;
        }

        // Show loading overlay
        showLoadingOverlay();

        // Simulate processing time
        setTimeout(() => {
            try {
                // Get options
                const options = {
                    usePassive: usePassive.checked,
                    useSynonyms: useSynonyms.checked,
                    preserveStructure: preserveStructure.checked,
                    intensity: intensity.value,
                    style: style.value
                };

                // Transform text
                const transformed = humanizer.humanizeText(text, options);

                // Update output
                outputText.value = transformed;

                // Update statistics
                updateStatistics(text, transformed);

                // Show output section
                outputSection.style.display = 'block';
                outputSection.scrollIntoView({ behavior: 'smooth' });

                // Hide loading overlay
                hideLoadingOverlay();

                showToast('Text transformed successfully!', 'success');

            } catch (error) {
                console.error('Error transforming text:', error);
                hideLoadingOverlay();
                showToast('Error transforming text. Please try again.', 'error');
            }
        }, 1500);
    });

    // Copy button click handler
    copyBtn.addEventListener('click', function() {
        const text = outputText.value;
        
        if (!text) {
            showToast('No text to copy.', 'error');
            return;
        }

        // Copy to clipboard
        navigator.clipboard.writeText(text).then(() => {
            showToast('Text copied to clipboard!', 'success');
        }).catch(() => {
            // Fallback for older browsers
            outputText.select();
            document.execCommand('copy');
            showToast('Text copied to clipboard!', 'success');
        });
    });

    // Load sample text
    loadSample.addEventListener('click', function() {
        const randomSample = humanizer.sampleTexts[Math.floor(Math.random() * humanizer.sampleTexts.length)];
        inputText.value = randomSample;
        showToast('Sample text loaded!', 'success');
    });

    // Clear all
    clearAll.addEventListener('click', function() {
        inputText.value = '';
        outputText.value = '';
        outputSection.style.display = 'none';
        
        // Reset checkboxes
        usePassive.checked = false;
        useSynonyms.checked = false;
        preserveStructure.checked = false;
        
        showToast('All cleared!', 'success');
    });

    // Update statistics
    function updateStatistics(originalText, transformedText) {
        inputWords.textContent = humanizer.countWords(originalText);
        inputSentences.textContent = humanizer.countSentences(originalText);
        outputWords.textContent = humanizer.countWords(transformedText);
        outputSentences.textContent = humanizer.countSentences(transformedText);
    }

    // Show loading overlay
    function showLoadingOverlay() {
        loadingOverlay.style.display = 'flex';
    }

    // Hide loading overlay
    function hideLoadingOverlay() {
        loadingOverlay.style.display = 'none';
    }

    // Show toast notification
    function showToast(message, type = 'success') {
        const toast = successToast;
        const toastMessage = toast.querySelector('.toast-message');
        const toastIcon = toast.querySelector('.toast-icon');
        
        toastMessage.textContent = message;
        
        if (type === 'success') {
            toast.className = 'toast toast-success';
            toastIcon.textContent = '✅';
        } else if (type === 'error') {
            toast.className = 'toast toast-error';
            toastIcon.textContent = '❌';
        }
        
        toast.style.display = 'flex';
        
        // Hide after 3 seconds
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add some interactive effects
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add typing effect to header
    const headerTitle = document.querySelector('.header-title');
    const originalText = headerTitle.textContent;
    headerTitle.textContent = '';
    
    let i = 0;
    const typeWriter = () => {
        if (i < originalText.length) {
            headerTitle.textContent += originalText.charAt(i);
            i++;
            setTimeout(typeWriter, 100);
        }
    };
    
    // Start typing effect after a short delay
    setTimeout(typeWriter, 500);

    // Add scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .step-card, .app-card, .config-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    console.log('AI Text Humanizer Pro initialized successfully!');
});
