from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel, QApplication, QFileDialog
from PyQt5.QtGui import QFont
import sys, os, random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
user_mail = os.getenv('USER_MAIL')
user_passwd = os.getenv('USER_PASSWD')
mail_to = os.getenv("MAIL_TO")
print(user_mail)
print(user_passwd)
print(mail_to)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.root()
        
    def root(self):
        layout = QVBoxLayout()

        # Font settings
        font = QFont("Arial", 14)
        font.setItalic(True)

        # Label for selected photo folder
        self.photo_label = QLabel("Select a folder with your photos:")
        self.photo_label.setFont(font)
        layout.addWidget(self.photo_label)

        # Button to select photo folder
        self.photo_button = QPushButton("Select Folder")
        self.photo_button.setFont(font)
        layout.addWidget(self.photo_button)
        self.photo_button.clicked.connect(self.select_folder)

        # Text input for custom message
        self.message_input = QTextEdit()
        self.message_input.setFont(font)
        self.message_input.setPlaceholderText("Enter your message here...")
        layout.addWidget(self.message_input)

        # Submit button
        self.submit = QPushButton("Submit")
        self.submit.setFont(font)
        layout.addWidget(self.submit)
        self.submit.clicked.connect(self.send_email)
        
        self.setLayout(layout)
        self.setFixedHeight(800)        
        self.setFixedWidth(700)        
        self.setWindowTitle("Photo Message Sender")
        self.show()

    def select_folder(self):
        self.folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if self.folder:
            self.photo_label.setText(f'Selected Folder: {self.folder}')
    
    def send_email(self):
        if not hasattr(self, 'folder') or not self.folder:
            self.photo_label.setText("Please select a folder first.")
            return
        
        # Select a random photo
        photos = os.listdir(self.folder)
        if not photos:
            self.photo_label.setText("The selected folder is empty.")
            return
        
        photo = random.choice(photos)
        photo_path = os.path.join(self.folder, photo)

        # Get the message from the user
        message = self.message_input.toPlainText()

        if not message:
            self.photo_label.setText("Please enter a message.")
            return

        # Send the email
        try:
            self.email_with_attachment(mail_to, message, photo_path)
            self.photo_label.setText("Email sent successfully!")
        except Exception as e:
            print(e)
            self.photo_label.setText(f"Failed to send email: {str(e)}")

    def email_with_attachment(self, recipient, message, attachment):
        msg = MIMEMultipart()
        msg['From'] = user_mail
        msg['To'] = recipient
        msg['Subject'] = "A Special Message for You"

        msg.attach(MIMEText(message, 'plain'))

        with open(attachment, "rb") as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment)}")
            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user_mail, user_passwd)
        server.sendmail(user_mail, recipient, msg.as_string())
        server.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
