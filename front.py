import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent, QClipboard
from PyQt5.QtCore import Qt, QMimeData

class ImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image App")  # Set the window title
        self.setGeometry(100, 100, 800, 600)  # Set the window geometry (position and size)

        # Set up the main layout
        main_layout = QVBoxLayout()

        # Image Input Layout
        image_layout = QHBoxLayout()
        
        # Entry for displaying image path and accepting pasted images
        self.image_path_entry = QLineEdit(self)
        self.image_path_entry.setPlaceholderText("Paste image path here or drag and drop an image")
        image_layout.addWidget(self.image_path_entry)

        # Browse Button to select image
        browse_button = QPushButton("Browse Image", self)
        browse_button.clicked.connect(self.browse_image)
        image_layout.addWidget(browse_button)

        main_layout.addLayout(image_layout)  # Add image input layout to main layout

        # Drag and Drop Area
        self.drop_label = QLabel("Drag and Drop Image Here", self)
        self.drop_label.setStyleSheet("QLabel { background-color : lightgray; border: 1px solid black; }")
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setScaledContents(False)  # Avoid automatic scaling, we'll handle it manually
        self.drop_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.drop_label.setMinimumSize(300, 300)  # Set a more appropriate minimum size
        main_layout.addWidget(self.drop_label, 1)  # Add the drop label with a stretch factor

        self.setAcceptDrops(True)  # Enable drag and drop support

        # Context Input Layout
        context_layout = QVBoxLayout()
        self.context_label = QLabel("Enter Context:")
        context_layout.addWidget(self.context_label)
        self.context_entry = QLineEdit(self)
        context_layout.addWidget(self.context_entry)
        main_layout.addLayout(context_layout)

        # Output Text Box Layout
        output_layout = QVBoxLayout()
        self.output_label = QLabel("Output:")
        output_layout.addWidget(self.output_label)
        self.output_text = QTextEdit(self)
        self.output_text.setFixedHeight(100)  # Set a fixed height for the output text box
        output_layout.addWidget(self.output_text)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)  # Set the main layout for the QWidget

        # Set up clipboard monitoring
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.paste_image)

        self.current_pixmap = None  # To keep track of the currently displayed image

    def resizeEvent(self, event):
        """Override resize event to adjust QLabel size."""
        super().resizeEvent(event)
        if self.current_pixmap:
            self.adjust_pixmap(self.current_pixmap)

    def browse_image(self):
        """Open a file dialog to browse and select an image."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Browse Image", "", "Image Files (*.png;*.jpg;*.jpeg;*.bmp)", options=options)
        if file_path:
            self.image_path_entry.setText(file_path)
            self.display_image(file_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Handle drop events for drag-and-drop functionality."""
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.image_path_entry.setText(file_path)
            self.display_image(file_path)

    def paste_image(self):
        """Handle pasting of images from clipboard."""
        mime_data = self.clipboard.mimeData()
        if mime_data.hasImage():
            image = self.clipboard.image()
            self.display_image(image=image)

    def display_image(self, file_path=None, image=None):
        """Display the selected or pasted image."""
        if file_path:
            image = QImage(file_path)
        
        if image:
            pixmap = QPixmap.fromImage(image)
            self.current_pixmap = pixmap
            self.adjust_pixmap(pixmap)

    def adjust_pixmap(self, pixmap):
        """Maintain the aspect ratio of the image and resize it to fit within drop_label dimensions."""
        label_width = self.drop_label.width()
        label_height = self.drop_label.height()
        # Maintain aspect ratio and scale the image
        scaled_pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.drop_label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageApp()
    ex.show()
    sys.exit(app.exec_())
