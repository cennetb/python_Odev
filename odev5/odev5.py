import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFileDialog, QHBoxLayout, QMainWindow, QAction, QInputDialog
import sqlite3

def baglan():
    return sqlite3.connect('metinler.db')

def veritabani_olustur():
    conn = baglan()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Metinler
                 (id INTEGER PRIMARY KEY, metin TEXT)''')
    conn.commit()
    conn.close()

def metin_ekle(metin):
    conn = baglan()
    c = conn.cursor()
    c.execute("INSERT INTO Metinler (metin) VALUES (?)", (metin,))
    conn.commit()
    conn.close()

def metin_sil():
    conn = baglan()
    c = conn.cursor()
    c.execute("DELETE FROM Metinler")
    conn.commit()
    conn.close()

def jaccard_benzerlik(metin1, metin2):
    kume1 = set(metin1.split())
    kume2 = set(metin2.split())
    benzer_kelimeler = kume1.intersection(kume2)
    farkli_kelimeler = kume1.union(kume2)
    return len(benzer_kelimeler) / len(farkli_kelimeler)

def cosine_similarity(metin1, metin2):
    kume1 = set(metin1.split())
    kume2 = set(metin2.split())
    benzer_kelimeler = kume1.intersection(kume2)
    return len(benzer_kelimeler) / ((len(kume1) * len(kume2)) ** 0.5)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user = None

        self.setWindowTitle("Metin Karşılaştırma Programı")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.username_label = QLabel("Kullanıcı Adı:")
        self.password_label = QLabel("Şifre:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Giriş Yap")
        self.register_button = QPushButton("Kayıt Ol")

        login_layout = QVBoxLayout()
        login_layout.addWidget(self.username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.register_button)

        self.central_widget.setLayout(login_layout)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            self.current_user = username
            self.show_menu()
        else:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı veya şifre yanlış!")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten mevcut!")
        else:
            c.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kullanıcı başarıyla kaydedildi!")
        conn.close()

    def show_menu(self):
        self.menu = MenuWidget(self, self.current_user)
        self.setCentralWidget(self.menu)

class MenuWidget(QWidget):
    def __init__(self, parent, current_user):
        super().__init__()
        self.parent = parent
        self.current_user = current_user

        layout = QVBoxLayout()
        compare_button = QPushButton("Metin Karşılaştır")
        operations_button = QPushButton("İşlemler")
        exit_button = QPushButton("Çıkış")

        layout.addWidget(compare_button)
        layout.addWidget(operations_button)
        layout.addWidget(exit_button)

        self.setLayout(layout)

        compare_button.clicked.connect(self.compare)
        operations_button.clicked.connect(self.operations)
        exit_button.clicked.connect(self.parent.close)

    def compare(self):
        self.compare_window = CompareWindow()
        self.compare_window.show()

    def operations(self):
        self.operations_window = OperationsWindow(self.current_user)
        self.operations_window.show()

class CompareWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Metin Karşılaştırma")
        self.setGeometry(100, 100, 400, 200)

        self.file1_label = QLabel("Metin 1 Dosyası:")
        self.file2_label = QLabel("Metin 2 Dosyası:")
        self.file1_input = QLineEdit()
        self.file2_input = QLineEdit()
        self.select_button1 = QPushButton("Dosya Seç")
        self.select_button2 = QPushButton("Dosya Seç")
        self.compare_button = QPushButton("Karşılaştır")
        self.result_label = QLabel("Sonuç:")

        layout = QVBoxLayout()
        layout.addWidget(self.file1_label)
        layout.addWidget(self.file1_input)
        layout.addWidget(self.select_button1)
        layout.addWidget(self.file2_label)
        layout.addWidget(self.file2_input)
        layout.addWidget(self.select_button2)
        layout.addWidget(self.compare_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.select_button1.clicked.connect(lambda: self.get_file_path(self.file1_input))
        self.select_button2.clicked.connect(lambda: self.get_file_path(self.file2_input))
        self.compare_button.clicked.connect(self.compare_texts)

    def get_file_path(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Text Files (*.txt)")
        if file_path:
            line_edit.setText(file_path)

    def compare_texts(self):
        file1_path = self.file1_input.text()
        file2_path = self.file2_input.text()

        try:
            with open(file1_path, 'r', encoding='utf-8') as file1, open(file2_path, 'r', encoding='utf-8') as file2:
                text1 = file1.read()
                text2 = file2.read()
                jaccard_similarity = jaccard_benzerlik(text1, text2)
                cosine_sim = cosine_similarity(text1, text2)
                self.result_label.setText(f"Jaccard Benzerlik: {jaccard_similarity:.2f}\nCosine Benzerlik: {cosine_sim:.2f}")
        except FileNotFoundError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli dosya yolları girin.")

class OperationsWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.current_user = current_user

        self.setWindowTitle("İşlemler")
        self.setGeometry(100, 100, 300, 200)

        password_button = QPushButton("Şifre Değiştir")

        layout = QVBoxLayout()
        layout.addWidget(password_button)

        self.setLayout(layout)

        password_button.clicked.connect(self.change_password)

    def change_password(self):
        password, ok = QInputDialog.getText(self, "Şifre Değiştir", "Yeni Şifre:")
        if ok:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("UPDATE Users SET password=? WHERE username=?", (password, self.current_user))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Başarılı", "Şifre başarıyla güncellendi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create users database if not exists
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.close()

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())