import pytesseract
import tkinter as tk
from PIL import ImageGrab
import threading
import time

# Координаты областей на экране
REGION_1 = (1374, 10, 1446, 36)  # (x1, y1, x2, y2)

class ScreenParserOverlay:
    def __init__(self):
        self.running = True
        self.current_value = "690k"
        
        # Создаем окно оверлея
        self.root = tk.Tk()
        self.root.title("Screen Parser")
        self.root.geometry("200x60")
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        
        # Убираем декорации окна
        self.root.attributes('-type', 'splash')
        
        # Метка для отображения текста
        self.label = tk.Label(
            self.root,
            text=self.current_value,
            font=("Arial", 24, "bold"),
            fg='#00FF00',  # Зеленый
            bg='black'
        )
        self.label.pack(expand=True, fill='both')
        
        # Позиционируем окно у указанных координат
        self.root.geometry(f"+1374+10")
        
        # Запускаем поток чтения экрана
        self.thread = threading.Thread(target=self.read_screen, daemon=True)
        self.thread.start()
        
        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def read_screen(self):
        """Постоянно читает текст с экрана"""
        while self.running:
            try:
                # Захватываем область экрана
                screenshot = ImageGrab.grab(bbox=REGION_1)
                
                # Читаем текст с помощью Tesseract
                text = pytesseract.image_to_string(screenshot).strip()
                
                if text and text != self.current_value:
                    self.current_value = text
                    # Обновляем метку в главном потоке
                    self.root.after(0, self.update_label)
                
                time.sleep(0.5)  # Обновляем каждые 0.5 секунды
                
            except Exception as e:
                print(f"Ошибка при чтении экрана: {e}")
                time.sleep(1)
    
    def update_label(self):
        """Обновляет текст в окне"""
        self.label.config(text=self.current_value)
    
    def on_closing(self):
        """Закрытие приложения"""
        self.running = False
        self.root.destroy()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


if __name__ == "__main__":
    app = ScreenParserOverlay()
    app.run()
