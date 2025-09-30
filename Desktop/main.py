import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap, QIcon, QPalette, QBrush
from PyQt6.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainwindow.ui', self)
        
        # Установка затемненного фонового изображения
        self.set_dark_background()
        
        # ОТКРЫТИЕ ВО ВЕСЬ ЭКРАН
        self.showMaximized()
        
        # Загружаем логотип
        self.load_logo()
        
        # Подключаем обработчик кнопки
        self.aboutCompanyButton.clicked.connect(self.show_about_company)
    
    def set_dark_background(self):
        """Установка затемненного фонового изображения"""
        try:
            background_path = "background.jpg"  # Можно изменить на нужное изображение
            if os.path.exists(background_path):
                pixmap = QPixmap(background_path)
                if not pixmap.isNull():
                    # Масштабируем изображение под размер окна
                    scaled_pixmap = pixmap.scaled(
                        self.size(),
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    
                    # Создаем затемненную версию изображения
                    dark_pixmap = self.create_darkened_pixmap(scaled_pixmap)
                    
                    # Устанавливаем как фон
                    palette = QPalette()
                    palette.setBrush(QPalette.ColorRole.Window, QBrush(dark_pixmap))
                    self.setPalette(palette)
                    print("Фоновое изображение установлено")
            else:
                # Если изображение не найдено, используем темный градиент
                self.setStyleSheet("""
                    QMainWindow {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #2b1b0e, stop:1 #1a1008);
                    }
                """)
                print("Фоновое изображение не найдено, использован градиент")
        except Exception as e:
            print(f"Ошибка установки фона: {e}")
            # Резервный вариант - темный градиент
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #2b1b0e, stop:1 #1a1008);
                }
            """)
    
    def create_darkened_pixmap(self, pixmap):
        """Создает затемненную версию изображения"""
        try:
            # Создаем копию pixmap
            dark_pixmap = QPixmap(pixmap.size())
            dark_pixmap.fill(Qt.GlobalColor.transparent)
            
            # Рисуем затемненное изображение
            from PyQt6.QtGui import QPainter
            painter = QPainter(dark_pixmap)
            painter.setOpacity(0.6)  # Уровень затемнения (0.6 = 40% затемнения)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            
            return dark_pixmap
        except Exception as e:
            print(f"Ошибка создания затемненного изображения: {e}")
            return pixmap
    
    def resizeEvent(self, event):
        """Обработчик изменения размера окна для обновления фона"""
        super().resizeEvent(event)
        self.set_dark_background()
    
    def load_logo(self):
        try:
            logo_path = "logo2.png"
            if os.path.exists(logo_path):
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    # Проверяем размер изображения
                    if pixmap.width() <= 150 and pixmap.height() <= 150:
                        # Если изображение маленькое, используем без масштабирования
                        self.logoLabel.setPixmap(pixmap)
                    else:
                        # Если большое, масштабируем с качеством
                        scaled_pixmap = pixmap.scaled(
                            150, 150,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        self.logoLabel.setPixmap(scaled_pixmap)
                    
                    self.logoLabel.setText("")
                    self.logoLabel.setScaledContents(True)
                    print("Логотип загружен оптимальным способом")
        except Exception as e:
            print(f"Ошибка: {e}")
            self.logoLabel.setText("ЛОГОТИП")
    
    def show_about_company(self):
        about_text = """
<h2>О компании 'Dinker'</h2>
<p><b>Основана:</b> 2025 год</p>
<p><b>Специализация:</b> Производство высококачественных кондитерских изделий</p>
<br>
<h3>Основатели компании:</h3>
<b>Сучилин Михаил Максимович</b> - Решала команды. Несёт ответственность за предприятие и нашу горе-команду.<br><br>
<b>Тишин Денис Анатольевич</b> - Главный разраб и доставала Дипсика, создавший это окно и приложение в целом.<br><br>
<b>Пластунов Даниил Викторович</b> - Мастер кривых линий, создавший 2D план-схему предприятия.<br><br>
<b>Маркин Кирилл Евгеньевич</b> - Автор того самого значка, создавший логотип нашей недокомпании.<br><br>
<b>Умрихина Кристина Александровна</b> - Дизайнер-садист, придумавшая дизайн нашей кноподавки.<br><br>
<b>Пачас Иван Константинович</b> - Конструктор (не)съедобной еды, придумавший шоколадки и их состав.<br><br>
<b>Беспалов Андрей АндрееВИЧ</b> - Верховный сочинитель. Создатель самого цитируемого текста в компании.<br><br>
<b>Репко Максим Юрьевич</b> - Крёстный отец нашей компании. Главный одобрятель нашего бардака.<br>
</ul>
<br>
<p>Мы гордимся нашими традициями качества и инновационными подходами к производству.</p>
"""
        QMessageBox.about(self, "О компании", about_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Используйте файл .ico вместо .png
    try:
        app.setWindowIcon(QIcon('icon.ico'))
        print("Иконка приложения установлена")
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")
    
    window = MyWindow()
    window.show()
    sys.exit(app.exec())