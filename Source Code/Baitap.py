import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import pygame.mixer
import os
import sys
class Critter:
    def __init__(self, name):
        # Khởi tạo Critter với tên và trạng thái mặc định-
        self.name = name
        self.hunger = 0
        self.boredom = 0

    def __pass_time(self):
        # Tăng chỉ số đói và chán khi ngủ
        if self.hunger < 10:
            self.hunger += 2
        if self.boredom < 10:
            self.boredom += 2

    def eat(self):
        # Giảm chỉ số đói khi ăn
        self.hunger = min(10, max(0, self.hunger -2))
        if self.hunger>0:
            return f"{self.name} đã ăn và cảm thấy no hơn!"
        elif self.hunger==0:
            return f"{self.name} no lắm rồi, không ăn nổi nữa"

    def play(self):
        # Giảm chỉ số chán khi chơi
        self.boredom = min(10, max(0, self.boredom -2))
        if self.boredom>0:
            return f"{self.name} đã chơi và rất vui!"
        elif self.boredom==0:
            return f"{self.name} chơi nhiều quá, mệt rồi!"

    def sleep(self):
        # Critter ngủ và thời gian trôi qua
        self.__pass_time()
        return f"{self.name} đã ngủ !"

    def get_status(self):
        # Trả về trạng thái hiện tại của Critter 
        return f"Tên: {self.name}\nĐói: {self.hunger}\nChán: {self.boredom}"

    def get_mood(self):
        # Xác định tâm trạng Critter dựa trên chỉ số đói và chán
        if self.hunger > 5 and self.boredom > 5:
            return "handb" 
        elif self.hunger > 5:
            return "hungry"
        elif self.boredom > 5:
            return "bored"
        else:
            return "happy"

    def tick_time(self):
        # Tăng chỉ số đói và chán theo thời gian thực
        if self.hunger < 10:
            self.hunger += 1
        if self.boredom < 10:
            self.boredom += 1

class CritterApp:
    def __init__(self, root):
        # Khởi tạo giao diện và các thành phần chính của ứng dụng
        self.root = root
        self.root.title("Chăm Sóc Thú Ảo")
        self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))
        self.critter = None

        self.current_animation = None
        self.current_animation_index = 0

        # Load hình nền
        self.bg_image = None
        try:
            bg_path = resource_path(os.path.join("Resource_pack", "background.png"))
            if os.path.exists(bg_path):
                img = Image.open(bg_path).resize((1920, 1080), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(img)
                self.bg_label = tk.Label(root, image=self.bg_image)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            else:
                raise FileNotFoundError(f"Không tìm thấy {bg_path}")
        except Exception as e:
            self.bg_label = tk.Label(root, text=f"Lỗi tải nền: {str(e)}", bg="gray")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Khung hiển thị thú cưng
        self.pet_frame = tk.LabelFrame(root, text="🐾 Thú Cưng 🐾", 
                               font=("Times New Roman", 18, "bold"), bg="#FFFFFF", fg="#4A148C", 
                               bd=6, relief="ridge")
        self.pet_frame.place(x=50, y=100, width=350, height=300)

        self.pet_label = tk.Label(self.pet_frame, text="Chưa có Thú Cưng", 
                          font=("Times New Roman", 16, "italic"), bg="#FFFFFF", fg="#4A148C")
        self.pet_label.pack(expand=True, padx=10, pady=10)

        # Khung thao tác
        self.action_frame = tk.LabelFrame(root, text="🎮 Tương tác 🎮", 
                                  font=("Times New Roman", 18, "bold"), bg="#FFFFFF", fg="#4A148C", 
                                  bd=6, relief="ridge")
        self.action_frame.place(x=450, y=100, width=500, height=500)

        # Nhãn và ô nhập tên Critter
        self.name_label = tk.Label(self.action_frame, text="Nhập tên thú cưng:", 
                           font=("Times New Roman", 16, "bold"), bg="#FFFFFF", fg="#6F068A")
        self.name_label.place(x=10, y=20)

        self.name_entry = tk.Entry(self.action_frame, font=("Times New Roman", 16), bd=2, relief="solid", bg="#FFF9C4", fg="#4A148C")
        self.name_entry.place(x=180, y=20, width=280)

        self.create_button = ttk.Button(self.action_frame, text="🚀 Tạo Thú Cưng", command=self.create_critter)
        self.create_button.place(x=170, y=70, width=150)
        self.create_button.bind('<Button-1>', self.play_click_sound)

        # Các nút Cho ăn, Chơi, Ngủ
        self.eat_button = ttk.Button(self.action_frame, text="🍽️Cho ăn", command=self.eat, state=tk.DISABLED)
        self.eat_button.place(x=10, y=120, width=150)
        self.eat_button.bind('<Button-1>', self.play_click_sound)

        self.play_button = ttk.Button(self.action_frame, text="🎾Chơi", command=self.play, state=tk.DISABLED)
        self.play_button.place(x=170, y=120, width=150)
        self.play_button.bind('<Button-1>', self.play_click_sound)

        self.sleep_button = ttk.Button(self.action_frame, text="🌙Ngủ", command=self.sleep, state=tk.DISABLED)
        self.sleep_button.place(x=330, y=120, width=150)
        self.sleep_button.bind('<Button-1>', self.play_click_sound)

        # Trạng thái của Critter
        self.status_label = tk.Label(self.action_frame, text="Chưa có Thú Cưng", 
                                        font=("Times New Roman", 16, "italic"), bg="#FFF9C4", fg="#4A148C", 
                                        wraplength=480, justify="left", bd=4, relief="groove")
        self.status_label.place(x=10, y=180, width=480, height=280)

        # Cấu hình style cho nút ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Times New Roman", 14), padding=5)

        # Load ảnh hoạt hình cho Critter theo trạng thái
        self.pet_images = {}
        for mood in ["happy", "hungry", "bored","handb"]:
            try:
                gif_path = resource_path(os.path.join("Resource_pack", f"pet_{mood}.gif"))
                if os.path.exists(gif_path):
                    im = Image.open(gif_path)
                    frames = []
                    for frame in ImageSequence.Iterator(im):
                        frame = frame.resize((200, 200), Image.LANCZOS)
                        frames.append(ImageTk.PhotoImage(frame))
                    self.pet_images[mood] = frames
                else:
                    raise FileNotFoundError(f"Không tìm thấy {gif_path}")
            except Exception as e:
                self.pet_images[mood] = None
                print(f"Lỗi tải ảnh pet_{mood}: {str(e)}")

        # Khởi tạo pygame mixer và phát nhạc nền
        self.background_music = None
        self.click_sound = None
        try:
            pygame.mixer.init()
            music_path = resource_path(os.path.join("Sound_pack", "background_music.mp3"))
            click_sound_path = resource_path(os.path.join("Sound_pack", "click_sound.mp3"))
            if os.path.exists(music_path):
                self.background_music = pygame.mixer.Sound(music_path)
                self.background_music.play(-1)
            else:
                raise FileNotFoundError("Không tìm thấy background_music.wav hoặc background_music.mp3")
            if os.path.exists(click_sound_path):
                self.click_sound = pygame.mixer.Sound(click_sound_path)
            else:
                print(f"Không tìm thấy {click_sound_path}")
        except Exception as e:
            print(f"Lỗi tải nhạc nền: {str(e)}")

    def update_realtime(self):
        # Cập nhật trạng thái và hình ảnh real-time
        if self.critter:
            self.critter.tick_time()
            self.update_status()
            self.update_pet_image()
        self.root.after(2000, self.update_realtime)  # Lặp lại sau 2 giây

    def create_critter(self):
        # Tạo Critter mới với tên nhập vào
        name = self.name_entry.get().strip()
        if not name:
            self.status_label.config(text="Lỗi: Vui lòng nhập tên cho thú cưng!")
            return
        self.critter = Critter(name)
        self.update_status()
        self.update_pet_image()
        self.eat_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.NORMAL)
        self.sleep_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"Đã tạo thú cưng {name}!\n{self.critter.get_status()}")
        self.update_realtime()  # Bắt đầu cập nhật real-time khi tạo thú cưng

    def eat(self):
        # Xử lý sự kiện cho Critter ăn
        if self.critter:
            message = self.critter.eat()
            self.update_status(message)
            self.update_pet_image()
        else:
            self.status_label.config(text="Lỗi: Hãy tạo một thú cưng trước!")

    def play(self):
        # Xử lý sự kiện cho Critter chơi
        if self.critter:
            message = self.critter.play()
            self.update_status(message)
            self.update_pet_image()
        else:
            self.status_label.config(text="Lỗi: Hãy tạo một thú cưng trước!")

    def sleep(self):
        # Xử lý sự kiện cho Critter ngủ
        if self.critter:
            message = self.critter.sleep()
            self.update_status(message)
            self.update_pet_image()
        else:
            self.status_label.config(text="Lỗi: Hãy tạo một thú cưng trước!")

    def update_status(self, message=""):
        # Cập nhật trạng thái Critter trên giao diện
        if self.critter:
            status = self.critter.get_status()
            if message:
                self.status_label.config(text=f"{message}\n{status}")
            else:
                self.status_label.config(text=status)
        else:
            self.status_label.config(text="Chưa có Thú Cưng")

    def update_pet_image(self):
        # Cập nhật ảnh động của Critter theo trạng thái
        if self.critter:
            mood = self.critter.get_mood()
            frames = self.pet_images.get(mood)
            if frames:
                self.current_animation = frames
                self.current_animation_index = 0
                self.animate()
            else:
                self.pet_label.config(image="", text=f"Không tìm thấy ảnh pet_{mood}.gif")
        else:
            self.pet_label.config(image="", text="Chưa có Thú Cưng")

    def animate(self):
        # Hiển thị ảnh động cho Critter
        if self.current_animation:
            frame = self.current_animation[self.current_animation_index]
            self.pet_label.config(image=frame, text="")
            self.pet_label.image = frame
            self.current_animation_index = (self.current_animation_index + 1) % len(self.current_animation)
            self.root.after(200, self.animate)

    def play_click_sound(self, event=None):
        # Phát âm thanh khi nhấn nút
        if self.click_sound:
            self.click_sound.stop()
            self.click_sound.play()

def resource_path(relative_path):
    # Lấy đường dẫn tuyệt đối đến tài nguyên (dùng cho cả .py và .exe)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Chạy ứng dụng CritterApp
    root = tk.Tk()
    app = CritterApp(root)
    root.mainloop()