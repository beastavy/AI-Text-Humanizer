#!/usr/bin/env python3
"""
AI Text Humanizer Pro - Native macOS App
Beautiful, modern GUI application for text humanization
"""

import sys
import os
import re
import random
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QComboBox, QCheckBox,
    QGroupBox, QSplitter, QFileDialog, QMessageBox, QProgressBar,
    QGraphicsDropShadowEffect, QFrame, QScrollArea, QSlider,
    QGridLayout
)
from PyQt6.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation,
    QEasingCurve, QRect, QPoint, QSize, pyqtProperty
)
from PyQt6.QtGui import (
    QFont, QPalette, QColor, QLinearGradient, QPainter,
    QBrush, QPen, QIcon, QPixmap, QFontDatabase, QTextCursor
)

try:
    from nltk.tokenize import word_tokenize
    NLTK_TOKENIZE_AVAILABLE = True
except ImportError:
    NLTK_TOKENIZE_AVAILABLE = False

try:
    from transformer.app import AcademicTextHumanizer, download_nltk_resources, NLP_GLOBAL
    TRANSFORMER_APP_AVAILABLE = True
except ImportError:
    TRANSFORMER_APP_AVAILABLE = False
    AcademicTextHumanizer = None
    download_nltk_resources = None
    NLP_GLOBAL = None


class HumanizerCore:
    """Text humanization core with advanced NLP support and fallbacks"""

    def __init__(self):
        self.nltk_available = False
        self.academic_humanizer = None
        self.last_error = None

        if TRANSFORMER_APP_AVAILABLE:
            try:
                download_nltk_resources()
                self.nltk_available = True
            except Exception as e:
                self.nltk_available = False
                self.last_error = f"NLTK init failed: {str(e)}"
        else:
            self.last_error = "transformer.app not available"

        self.contractions = {
            "don't": "do not", "doesn't": "does not", "didn't": "did not",
            "won't": "will not", "can't": "cannot", "couldn't": "could not",
            "wouldn't": "would not", "shouldn't": "should not",
            "isn't": "is not", "aren't": "are not", "wasn't": "was not",
            "weren't": "were not", "hasn't": "has not", "haven't": "have not",
            "I'm": "I am", "you're": "you are", "he's": "he is",
            "she's": "she is", "we're": "we are", "they're": "they are",
            "I'll": "I will", "you'll": "you will", "he'll": "he will",
            "I've": "I have", "you've": "you have", "we've": "we have",
            "it's": "it is", "that's": "that is", "there's": "there is"
        }

        self.academic_transitions = [
            "Moreover", "Additionally", "Furthermore", "Hence",
            "Therefore", "Consequently", "Nonetheless", "Nevertheless",
            "In addition", "As a result", "For this reason", "In contrast",
            "On the other hand", "Similarly", "Likewise", "In particular",
            "Specifically", "To illustrate", "For instance", "Indeed"
        ]

        self.formal_synonyms = {
            "good": ["excellent", "favorable", "beneficial", "advantageous"],
            "bad": ["unfavorable", "detrimental", "adverse", "problematic"],
            "important": ["crucial", "significant", "essential", "vital"],
            "show": ["demonstrate", "illustrate", "exhibit", "reveal"],
            "use": ["utilize", "employ", "implement", "apply"],
            "make": ["create", "produce", "construct", "develop"],
            "get": ["obtain", "acquire", "receive", "procure"],
            "think": ["consider", "believe", "contemplate", "ponder"],
            "say": ["state", "express", "articulate", "convey"],
            "big": ["substantial", "considerable", "significant", "extensive"],
            "small": ["minimal", "limited", "modest", "minor"],
            "many": ["numerous", "multiple", "various", "several"],
            "few": ["limited", "minimal", "scarce", "sparse"]
        }

    def _build_academic_humanizer(self, settings):
        if not TRANSFORMER_APP_AVAILABLE:
            self.last_error = "transformer.app not available"
            return
            
        intensity = settings.get('intensity_label', 'Medium')

        if intensity == "Heavy":
            p_passive = 0.4
            p_synonyms = 0.4
            p_transitions = 0.5
        elif intensity == "Light":
            p_passive = 0.2
            p_synonyms = 0.2
            p_transitions = 0.3
        else:
            p_passive = 0.3
            p_synonyms = 0.3
            p_transitions = 0.4

        if not settings.get('add_transitions', True):
            p_transitions = 0.0
        if not settings.get('enhance_vocabulary', True):
            p_synonyms = 0.0
        if not settings.get('use_passive', False):
            p_passive = 0.0

        try:
            self.academic_humanizer = AcademicTextHumanizer(
                p_passive=p_passive,
                p_synonym_replacement=p_synonyms,
                p_academic_transition=p_transitions,
                use_sentence_transformers=settings.get('use_sentence_transformers', True)
            )
            self.last_error = None
        except Exception as e:
            self.academic_humanizer = None
            self.last_error = f"AcademicTextHumanizer init failed: {str(e)}"

    def _humanize_with_academic(self, text, settings):
        self._build_academic_humanizer(settings)
        if not self.academic_humanizer:
            return None

        try:
            result = self.academic_humanizer.humanize_text(
                text,
                use_passive=settings.get('use_passive', False),
                use_synonyms=settings.get('use_synonyms', True),
                preserve_structure=settings.get('preserve_structure', False)
            )
            self.last_error = None
            return result
        except Exception as e:
            self.last_error = f"Advanced humanization failed: {str(e)}"
            return None

    def expand_contractions(self, text):
        """Expand contractions in text (fallback logic)"""
        result = text
        for contraction, expansion in self.contractions.items():
            pattern = r'\b' + re.escape(contraction) + r'\b'
            result = re.sub(pattern, expansion, result, flags=re.IGNORECASE)
        return result

    def add_transitions(self, text, intensity=0.3):
        """Add academic transitions between sentences (fallback logic)"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        if len(sentences) <= 1:
            return text

        result = [sentences[0]]
        for i in range(1, len(sentences)):
            if random.random() < intensity and sentences[i]:
                transition = random.choice(self.academic_transitions)
                if not any(sentences[i].startswith(t) for t in self.academic_transitions):
                    sentences[i] = f"{transition}, {sentences[i][0].lower()}{sentences[i][1:]}"
            result.append(sentences[i])

        return ' '.join(result)

    def enhance_vocabulary(self, text):
        """Replace common words with more sophisticated alternatives (fallback logic)"""
        words = text.split()
        result = []

        for word in words:
            clean_word = word.lower().strip('.,!?;:')
            if clean_word in self.formal_synonyms and random.random() < 0.3:
                replacement = random.choice(self.formal_synonyms[clean_word])
                if word[0].isupper():
                    replacement = replacement.capitalize()
                if word[-1] in '.,!?;:':
                    replacement += word[-1]
                result.append(replacement)
            else:
                result.append(word)

        return ' '.join(result)

    def add_subordinate_clauses(self, text):
        """Add subordinate clauses to make sentences more complex (fallback logic)"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        result = []

        for sentence in sentences:
            if len(sentence.split()) > 5 and random.random() < 0.2:
                clause = random.choice([
                    ", which is particularly noteworthy,",
                    ", a fact that warrants consideration,",
                    ", as research indicates,",
                    ", according to recent findings,",
                    ", an aspect worth noting,"
                ])
                words = sentence.split()
                mid = len(words) // 2
                words.insert(mid, clause)
                sentence = ' '.join(words)
            result.append(sentence)

        return ' '.join(result)

    def _basic_transform(self, text, settings):
        """Apply lightweight transformations without advanced NLP stack"""
        result = text

        if settings.get('expand_contractions', True):
            result = self.expand_contractions(result)

        if settings.get('add_transitions', True):
            intensity = settings.get('transition_intensity', 0.3)
            result = self.add_transitions(result, intensity)

        if settings.get('enhance_vocabulary', True):
            result = self.enhance_vocabulary(result)

        if settings.get('use_passive', False):
            # Simple passive conversion fallback
            sentences = re.split(r'(?<=[.!?])\s+', result)
            result_sentences = []
            for sentence in sentences:
                words = sentence.split()
                for idx, word in enumerate(words):
                    if word.lower() in ['is', 'are', 'was', 'were', 'be', 'been', 'being']:
                        if idx + 1 < len(words) and words[idx + 1].endswith('ing'):
                            words[idx + 1] = 'being ' + words[idx + 1]
                        break
                result_sentences.append(' '.join(words))
            result = ' '.join(result_sentences)

        # In fallback mode, synonym enhancement is controlled by 'enhance_vocabulary'

        if settings.get('add_clauses', False):
            result = self.add_subordinate_clauses(result)

        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\s+([.,!?;:])', r'\1', result)
        return result.strip()

    def humanize(self, text, settings):
        """Main humanization function"""
        if not text.strip():
            return text

        advanced_result = self._humanize_with_academic(text, settings)
        if advanced_result is not None:
            return advanced_result

        if settings.get('preserve_structure', False):
            lines = text.split('\n')
            processed_lines = []
            for line in lines:
                if not line.strip():
                    processed_lines.append('')
                    continue
                line_settings = dict(settings)
                line_settings['preserve_structure'] = False
                processed_lines.append(self._basic_transform(line, line_settings))
            return '\n'.join(processed_lines)

        return self._basic_transform(text, settings)


class HumanizerThread(QThread):
    """Background thread for text processing"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    status = pyqtSignal(str)

    def __init__(self, text, settings, humanizer):
        super().__init__()
        self.text = text
        self.settings = settings
        self.humanizer = humanizer
    
    def run(self):
        """Process text in background"""
        self.status.emit("🔄 Loading NLP pipelines...")
        self.progress.emit(20)
        self.msleep(300)

        self.status.emit("🧠 Processing with spaCy & NLTK...")
        self.progress.emit(40)
        self.msleep(300)

        self.status.emit("✨ Enhancing text with AI models...")
        self.progress.emit(60)
        self.msleep(300)

        self.status.emit("🎯 Finalizing transformations...")
        self.progress.emit(80)
        self.msleep(300)

        result = self.humanizer.humanize(self.text, self.settings)

        self.status.emit("✅ Complete!")
        self.progress.emit(100)
        self.msleep(200)

        self.finished.emit(result)


class ModernButton(QPushButton):
    """Custom styled button with animations"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(102, 126, 234, 80))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        """Animate on hover"""
        super().enterEvent(event)
        self.setStyleSheet(self.styleSheet() + """
            QPushButton {
                transform: translateY(-2px);
            }
        """)
    
    def leaveEvent(self, event):
        """Reset on leave"""
        super().leaveEvent(event)
        # Reset style


class StatsWidget(QFrame):
    """Statistics display widget"""
    
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        self.input_words = self.create_stat("Input Words", "0")
        self.output_words = self.create_stat("Output Words", "0")
        self.improvement = self.create_stat("Improvement", "+0")
        
        layout.addWidget(self.input_words)
        layout.addWidget(QFrame())  # Separator
        layout.addWidget(self.output_words)
        layout.addWidget(QFrame())  # Separator
        layout.addWidget(self.improvement)
        
        self.setLayout(layout)
    
    def create_stat(self, label, value):
        """Create a stat widget"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #4CAF50;
            }
        """)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        text_label = QLabel(label)
        text_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                text-transform: uppercase;
            }
        """)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(text_label)
        widget.setLayout(layout)
        
        # Store labels for updates
        widget.value_label = value_label
        widget.text_label = text_label
        
        return widget
    
    def update_stats(self, input_count, output_count):
        """Update statistics"""
        self.input_words.value_label.setText(str(input_count))
        self.output_words.value_label.setText(str(output_count))
        diff = output_count - input_count
        self.improvement.value_label.setText(f"+{diff}" if diff > 0 else str(diff))


class AITextHumanizerApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.humanizer = HumanizerCore()
        self.current_intensity_label = "Medium"
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("AI Text Humanizer Pro")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f7fa, stop:1 #c3cfe2);
            }
            QTextEdit {
                background: white;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                padding: 15px;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 15px;
                line-height: 1.6;
            }
            QTextEdit:focus {
                border-color: #667eea;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 22px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #764ba2, stop:1 #667eea);
            }
            QPushButton:pressed {
                background: #5a67d8;
            }
            QLabel {
                color: #2c3e50;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            }
            QCheckBox {
                color: #2c3e50;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #667eea;
            }
            QCheckBox::indicator:checked {
                background: #667eea;
            }
            QComboBox {
                background: white;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                padding: 8px;
                min-width: 150px;
            }
            QProgressBar {
                border: none;
                border-radius: 8px;
                background: #e1e5e9;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: #e1e5e9;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 18px;
                height: 18px;
                background: #667eea;
                border-radius: 9px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #764ba2;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Settings panel
        settings_panel = self.create_settings_panel()
        main_layout.addWidget(settings_panel)
        
        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Input panel
        input_panel = self.create_input_panel()
        content_splitter.addWidget(input_panel)
        
        # Output panel
        output_panel = self.create_output_panel()
        content_splitter.addWidget(output_panel)
        
        content_splitter.setSizes([600, 600])
        main_layout.addWidget(content_splitter)
        
        # Stats widget
        self.stats_widget = StatsWidget()
        main_layout.addWidget(self.stats_widget)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumHeight(8)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #7f8c8d; padding: 10px;")
        main_layout.addWidget(self.status_label)

        if self.humanizer.nltk_available:
            self.status_label.setText("✅ Advanced Python libraries (spaCy, NLTK) loaded.")
        else:
            self.status_label.setText("⚠️ Running in basic mode. Install spaCy/NLTK for full features.")
    
    def create_header(self):
        """Create application header"""
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("✨ AI Text Humanizer Pro")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Transform AI-generated text into natural, human-like writing")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        header.setLayout(layout)
        
        return header
    
    def create_settings_panel(self):
        """Create settings panel"""
        panel = QGroupBox("⚙️ Transformation Settings")
        layout = QGridLayout()

        self.use_passive_cb = QCheckBox("Enable Passive Voice")
        self.use_passive_cb.setChecked(False)

        self.use_synonyms_cb = QCheckBox("Enable Synonym Replacement")
        self.use_synonyms_cb.setChecked(True)

        self.preserve_structure_cb = QCheckBox("Preserve Structure")
        self.preserve_structure_cb.setChecked(False)

        self.add_transitions_cb = QCheckBox("Add Academic Transitions")
        self.add_transitions_cb.setChecked(True)

        self.enhance_vocabulary_cb = QCheckBox("Enhance Vocabulary")
        self.enhance_vocabulary_cb.setChecked(True)

        intensity_label = QLabel("Intensity:")
        self.intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.intensity_slider.setMinimum(1)
        self.intensity_slider.setMaximum(10)
        self.intensity_slider.setValue(5)
        self.intensity_value = QLabel(self.current_intensity_label)

        self.intensity_slider.valueChanged.connect(self.update_intensity_label)

        layout.addWidget(self.use_passive_cb, 0, 0)
        layout.addWidget(self.use_synonyms_cb, 0, 1)
        layout.addWidget(self.preserve_structure_cb, 0, 2)
        layout.addWidget(self.add_transitions_cb, 1, 0)
        layout.addWidget(self.enhance_vocabulary_cb, 1, 1)
        layout.addWidget(intensity_label, 2, 0)
        layout.addWidget(self.intensity_slider, 2, 1)
        layout.addWidget(self.intensity_value, 2, 2)

        panel.setLayout(layout)
        return panel
    
    def create_input_panel(self):
        """Create input text panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Label
        label = QLabel("📝 Input Text")
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        
        # Text area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Paste your AI-generated text here...\n\n"
            "Example: I don't think this approach will work. "
            "It's not good enough for our needs."
        )
        
        # Buttons
        button_layout = QHBoxLayout()
        
        load_button = ModernButton("📁 Load File")
        load_button.clicked.connect(self.load_file)
        
        clear_button = ModernButton("🗑️ Clear")
        clear_button.clicked.connect(lambda: self.input_text.clear())
        
        humanize_button = ModernButton("🚀 Humanize")
        humanize_button.clicked.connect(self.humanize_text)
        humanize_button.setStyleSheet(humanize_button.styleSheet() + """
            QPushButton {
                font-size: 18px;
                padding: 15px 40px;
            }
        """)
        
        button_layout.addWidget(load_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()
        button_layout.addWidget(humanize_button)
        
        layout.addWidget(label)
        layout.addWidget(self.input_text)
        layout.addLayout(button_layout)
        
        panel.setLayout(layout)
        return panel
    
    def create_output_panel(self):
        """Create output text panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Label
        label = QLabel("✨ Humanized Text")
        label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        
        # Text area
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText(
            "Your humanized text will appear here..."
        )
        self.output_text.setReadOnly(True)
        # Explicitly set text color to ensure visibility
        self.output_text.setStyleSheet("""
            QTextEdit {
                background: white;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                padding: 15px;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 15px;
                line-height: 1.6;
                color: #2c3e50;
            }
        """)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        copy_button = ModernButton("📋 Copy")
        copy_button.clicked.connect(self.copy_output)
        
        save_button = ModernButton("💾 Save")
        save_button.clicked.connect(self.save_file)
        
        button_layout.addWidget(copy_button)
        button_layout.addWidget(save_button)
        button_layout.addStretch()
        
        layout.addWidget(label)
        layout.addWidget(self.output_text)
        layout.addLayout(button_layout)
        
        panel.setLayout(layout)
        return panel
    
    def update_intensity_label(self, value):
        """Update intensity label based on slider value"""
        if value <= 3:
            self.current_intensity_label = "Light"
        elif value <= 7:
            self.current_intensity_label = "Medium"
        else:
            self.current_intensity_label = "Heavy"
        self.intensity_value.setText(self.current_intensity_label)
    
    def get_settings(self):
        """Get current settings"""
        # Derive intensity label from slider to keep advanced pipeline in sync
        val = self.intensity_slider.value()
        if val <= 3:
            intensity_label = "Light"
        elif val <= 7:
            intensity_label = "Medium"
        else:
            intensity_label = "Heavy"

        return {
            'expand_contractions': True,  # always expand contractions
            'add_transitions': self.add_transitions_cb.isChecked(),
            'enhance_vocabulary': self.enhance_vocabulary_cb.isChecked(),
            'add_clauses': False,
            'transition_intensity': self.intensity_slider.value() / 10.0,
            'use_passive': self.use_passive_cb.isChecked(),
            'use_synonyms': self.use_synonyms_cb.isChecked(),
            'preserve_structure': self.preserve_structure_cb.isChecked(),
            'intensity_label': intensity_label,
            'use_sentence_transformers': self.use_synonyms_cb.isChecked(),
        }
    
    def humanize_text(self):
        """Humanize the input text"""
        text = self.input_text.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Warning", "Please enter some text to humanize.")
            return
        
        # Disable UI during processing
        self.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create and start worker thread
        self.worker = HumanizerThread(text, self.get_settings(), self.humanizer)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_humanization_complete)
        self.worker.start()
    
    def on_humanization_complete(self, result):
        """Handle completion of humanization"""
        self.output_text.setPlainText(result)
        
        # Update statistics (prefer NLTK tokenization if available)
        if self.humanizer.nltk_available and NLTK_TOKENIZE_AVAILABLE:
            try:
                input_count = len(word_tokenize(self.input_text.toPlainText()))
                output_count = len(word_tokenize(result))
            except:
                input_count = len(self.input_text.toPlainText().split())
                output_count = len(result.split())
        else:
            input_count = len(self.input_text.toPlainText().split())
            output_count = len(result.split())
        self.stats_widget.update_stats(input_count, output_count)
        
        # Re-enable UI
        self.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Show appropriate status message
        if self.humanizer.last_error:
            error_msg = f"⚠️ Fallback mode used. {self.humanizer.last_error}"
            self.status_label.setText(error_msg)
            QTimer.singleShot(5000, lambda: self.status_label.setText(""))
        else:
            self.status_label.setText("✅ Humanization complete!")
            QTimer.singleShot(3000, lambda: self.status_label.setText(""))
    
    def load_file(self):
        """Load text from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.input_text.setPlainText(f.read())
                self.status_label.setText(f"✅ Loaded: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
    
    def save_file(self):
        """Save output to file"""
        if not self.output_text.toPlainText():
            QMessageBox.warning(self, "Warning", "No output text to save.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Text File", "humanized_text.txt", "Text Files (*.txt)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.output_text.toPlainText())
                self.status_label.setText(f"✅ Saved: {Path(file_path).name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
    
    def copy_output(self):
        """Copy output text to clipboard"""
        if not self.output_text.toPlainText():
            QMessageBox.warning(self, "Warning", "No output text to copy.")
            return
        
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        self.status_label.setText("✅ Text copied to clipboard!")
        QTimer.singleShot(2000, lambda: self.status_label.setText(""))


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("AI Text Humanizer Pro")
    app.setOrganizationName("AI Text Solutions")
    app.setApplicationDisplayName("AI Text Humanizer Pro")
    
    # Create and show main window
    window = AITextHumanizerApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
