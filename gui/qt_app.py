import sys
import os
import threading
from PyQt6 import QtWidgets, QtGui, QtCore

def resource_path(*parts: str) -> str:
    """Resolve path to bundled resources under PyInstaller or source tree."""
    try:
        base = getattr(sys, '_MEIPASS')  # PyInstaller temp dir
    except AttributeError:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base, *parts)

# Configure NLP resources to use bundled data inside the app
try:
    import nltk
    bundled_nltk = resource_path('nltk_data')
    if os.path.isdir(bundled_nltk) and bundled_nltk not in nltk.data.path:
        nltk.data.path.insert(0, bundled_nltk)
except Exception:
    pass

try:
    import spacy
    # Prefer the bundled spaCy model if present (installed into site-packages during build)
    _ = spacy.load("en_core_web_sm")
except Exception:
    # If not available, the app will still run but with degraded features handled by transformer.app
    pass

# Use existing logic
from transformer.app import AcademicTextHumanizer

class HumanizerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Text Humanizer Pro")
        self.setMinimumSize(1000, 720)
        self.setWindowIcon(QtGui.QIcon(resource_path("icon.icns")))

        root = QtWidgets.QWidget()
        self.setCentralWidget(root)
        layout = QtWidgets.QVBoxLayout(root)

        # Header
        header = QtWidgets.QLabel("✨ AI Text Humanizer Pro")
        header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("font-size: 26px; font-weight: 700; padding: 12px; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2); color: white; border-radius: 10px;")
        layout.addWidget(header)

        # Controls row
        controls = QtWidgets.QHBoxLayout()
        layout.addLayout(controls)

        self.passive_cb = QtWidgets.QCheckBox("Enable Passive Voice")
        self.synonyms_cb = QtWidgets.QCheckBox("Enable Synonym Replacement")
        self.structure_cb = QtWidgets.QCheckBox("Preserve Structure")
        self.synonyms_cb.setChecked(True)

        controls.addWidget(self.passive_cb)
        controls.addWidget(self.synonyms_cb)
        controls.addWidget(self.structure_cb)
        controls.addStretch(1)

        intensity_label = QtWidgets.QLabel("Intensity:")
        self.intensity_combo = QtWidgets.QComboBox()
        self.intensity_combo.addItems(["Light", "Medium", "Heavy"])
        self.intensity_combo.setCurrentText("Medium")
        controls.addWidget(intensity_label)
        controls.addWidget(self.intensity_combo)

        # Splitter for input/output
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(splitter, 1)

        # Input
        left = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.addWidget(QtWidgets.QLabel("📝 Input Text:"))
        self.input_edit = QtWidgets.QPlainTextEdit()
        self.input_edit.setPlaceholderText("Paste your AI-generated text here...")
        left_layout.addWidget(self.input_edit, 1)

        # Buttons under input
        in_btn_row = QtWidgets.QHBoxLayout()
        self.load_file_btn = QtWidgets.QPushButton("Open .txt file…")
        self.clear_btn = QtWidgets.QPushButton("Clear")
        in_btn_row.addWidget(self.load_file_btn)
        in_btn_row.addStretch(1)
        in_btn_row.addWidget(self.clear_btn)
        left_layout.addLayout(in_btn_row)

        # Output
        right = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right)
        right_layout.addWidget(QtWidgets.QLabel("✨ Humanized Text:"))
        self.output_edit = QtWidgets.QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        right_layout.addWidget(self.output_edit, 1)

        # Buttons under output
        out_btn_row = QtWidgets.QHBoxLayout()
        self.copy_btn = QtWidgets.QPushButton("Copy Output")
        out_btn_row.addStretch(1)
        out_btn_row.addWidget(self.copy_btn)
        right_layout.addLayout(out_btn_row)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([600, 600])

        # Bottom row: actions + status
        bottom_row = QtWidgets.QHBoxLayout()
        layout.addLayout(bottom_row)
        self.humanize_btn = QtWidgets.QPushButton("🚀 Humanize Text")
        self.humanize_btn.setMinimumHeight(44)
        self.progress = QtWidgets.QProgressBar()
        self.progress.setRange(0, 100)
        self.status_label = QtWidgets.QLabel("Ready")
        bottom_row.addWidget(self.humanize_btn)
        bottom_row.addWidget(self.progress, 1)
        bottom_row.addWidget(self.status_label)

        # Stats
        stats_row = QtWidgets.QHBoxLayout()
        layout.addLayout(stats_row)
        self.input_words_lbl = QtWidgets.QLabel("Input Words: 0")
        self.output_words_lbl = QtWidgets.QLabel("Output Words: 0")
        stats_row.addWidget(self.input_words_lbl)
        stats_row.addWidget(self.output_words_lbl)
        stats_row.addStretch(1)

        # Signals
        self.humanize_btn.clicked.connect(self.on_humanize)
        self.copy_btn.clicked.connect(self.on_copy)
        self.clear_btn.clicked.connect(self.input_edit.clear)
        self.load_file_btn.clicked.connect(self.on_load_file)

    def post(self, fn):
        """Execute a callable on the GUI thread."""
        QtCore.QTimer.singleShot(0, fn)

    def set_busy(self, busy: bool):
        self.humanize_btn.setEnabled(not busy)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor if busy else QtCore.Qt.CursorShape.ArrowCursor)

    def on_load_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open text file", "", "Text Files (*.txt)")
        if path:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    self.input_edit.setPlainText(f.read())
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to read file:\n{e}")

    def on_copy(self):
        text = self.output_edit.toPlainText()
        if text:
            QtWidgets.QApplication.clipboard().setText(text)
            self.status_label.setText("Copied to clipboard")

    def on_humanize(self):
        # Immediate debug feedback
        print("Humanize button clicked!")
        self.status_label.setText("Humanize button clicked - starting...")

        text = self.input_edit.toPlainText().strip()
        if not text:
            QtWidgets.QMessageBox.warning(self, "No input", "Please enter some text to humanize.")
            return

        print(f"Processing text: {len(text)} characters")
        use_passive = self.passive_cb.isChecked()
        use_synonyms = self.synonyms_cb.isChecked()
        preserve_structure = self.structure_cb.isChecked()
        intensity = self.intensity_combo.currentText()

        # Map intensity to probabilities
        p_passive = 0.4 if intensity == "Heavy" else 0.3 if intensity == "Medium" else 0.2
        p_syn = 0.4 if intensity == "Heavy" else 0.3 if intensity == "Medium" else 0.2
        p_trans = 0.5 if intensity == "Heavy" else 0.4 if intensity == "Medium" else 0.3

        def task():
            try:
                self.post(lambda: self.set_busy(True))
                self.post(lambda: self.status_label.setText("Analyzing text…"))
                self.post(lambda: self.progress.setValue(15))

                # Debug: Check if text is being passed correctly
                self.post(lambda: self.status_label.setText(f"Processing {len(text)} characters…"))
                self.post(lambda: self.progress.setValue(25))

                humanizer = AcademicTextHumanizer(
                    p_passive=p_passive,
                    p_synonym_replacement=p_syn,
                    p_academic_transition=p_trans,
                    use_sentence_transformers=False,
                )

                self.post(lambda: self.status_label.setText("Processing with AI models…"))
                self.post(lambda: self.progress.setValue(50))

                transformed = humanizer.humanize_text(
                    text,
                    use_passive=use_passive,
                    use_synonyms=use_synonyms,
                    preserve_structure=preserve_structure,
                )

                self.post(lambda: self.status_label.setText("Finalizing…"))
                self.post(lambda: self.progress.setValue(85))

                # Debug: Check if transformation actually happened
                if transformed == text:
                    self.post(lambda: self.status_label.setText("No changes made - checking input…"))
                else:
                    self.post(lambda: self.status_label.setText("Transformation complete!"))

                in_words = len(text.split())
                out_words = len(transformed.split())

                self.post(lambda: self.output_edit.setPlainText(transformed))
                self.post(lambda: self.input_words_lbl.setText(f"Input Words: {in_words}"))
                self.post(lambda: self.output_words_lbl.setText(f"Output Words: {out_words}"))
                self.post(lambda: self.progress.setValue(100))
                self.post(lambda: self.status_label.setText("Done"))
                self.post(lambda: self.set_busy(False))
            except Exception as e:
                print(f"Error in humanize task: {e}")
                self.post(lambda: self.set_busy(False))
                self.post(lambda: self.status_label.setText("Error"))
                self.post(lambda: QtWidgets.QMessageBox.critical(self, "Error", f"Failed to humanize text:\n{e}"))

        threading.Thread(target=task, daemon=True).start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = HumanizerWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
