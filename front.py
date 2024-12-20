import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent, QClipboard
from PyQt5.QtCore import Qt

class ImageApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image App")
        self.setGeometry(100, 100, 800, 600)

        # Set up the main layout
        main_layout = QVBoxLayout()

        # Image Input Layout
        image_layout = QHBoxLayout()

        # Entry for displaying image path and accepting pasted images
        self.image_path_entry = QLineEdit(self)
        self.image_path_entry.setPlaceholderText("Paste image path here or drag and drop an image")
        image_layout.addWidget(self.image_path_entry)

        # Browse Button
        browse_button = QPushButton("Browse Image", self)
        browse_button.clicked.connect(self.browse_image)
        image_layout.addWidget(browse_button)

        main_layout.addLayout(image_layout)

        # Drag and Drop Area
        self.drop_label = QLabel("Drag and Drop Image Here", self)
        self.drop_label.setStyleSheet("QLabel { background-color : lightgray; border: 1px solid black; }")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setScaledContents(True)  # Ensure the image scales with the QLabel
        self.drop_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drop_label.setMinimumSize(150, 150)
        main_layout.addWidget(self.drop_label, alignment=Qt.AlignCenter)

        self.setAcceptDrops(True)

        # Context Input
        self.context_label = QLabel("Enter Context:")
        main_layout.addWidget(self.context_label)
        self.context_entry = QLineEdit(self)
        main_layout.addWidget(self.context_entry)

        # Output Text Box
        self.output_label = QLabel("Output:")
        main_layout.addWidget(self.output_label)
        self.output_text = QTextEdit(self)
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

        # Set up clipboard monitoring
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.paste_image)

    def resizeEvent(self, event):
        """Override resize event to adjust QLabel size."""
        self.drop_label.setFixedSize(self.width() - 40, int(self.height() * 0.4))
        super().resizeEvent(event)

    def browse_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Browse Image", "", "Image Files (*.png;*.jpg;*.jpeg;*.bmp)", options=options)
        if file_path:
            self.image_path_entry.setText(file_path)
            self.display_image(file_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.image_path_entry.setText(file_path)
            self.display_image(file_path)

    def paste_image(self):
        mime_data = self.clipboard.mimeData()
        if mime_data.hasImage():
            image = self.clipboard.image()
            pixmap = QPixmap.fromImage(image.scaled(self.drop_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.drop_label.setPixmap(pixmap)
            self.image_path_entry.setText("Pasted Image")

    def display_image(self, file_path):
        image = QImage(file_path)
        pixmap = QPixmap.fromImage(image.scaled(self.drop_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.drop_label.setPixmap(pixmap)

        # Process the image here
        self.process_image(file_path)

    def process_image(self, file_path):
        # Example processing function
        print(f"Processing image at {file_path}")
        # Add your image processing code here

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageApp()
    ex.show()
    sys.exit(app.exec_())
