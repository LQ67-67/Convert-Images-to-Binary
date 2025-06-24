import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import os
import threading
import time


class ModernImageToBinaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Image to Binary Converter")
        self.root.geometry("1200x800")
        self.root.configure(bg='#16213e')
        self.root.minsize(1000, 700)

        # 图像处理设置
        self.image_quality = {
            'sharpness': 1.2,  # 锐化程度
            'contrast': 1.1,  # 对比度
            'brightness': 1.0  # 亮度
        }

        # 设置窗口图标和样式
        self.setup_styles()

        # 变量
        self.image_path = tk.StringVar()
        self.original_image = None
        self.binary_image = None
        self.is_processing = False

        # 创建主界面
        self.create_main_interface()

        # 启动动画
        self.start_animations()

    def setup_styles(self):
        """设置现代化的样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 自定义样式
        self.style.configure('Modern.TFrame', background='#1a1a2e')
        self.style.configure('Card.TFrame', background='#16213e', relief='flat')
        self.style.configure('Modern.TButton',
                             background='#0f3460',
                             foreground='white',
                             borderwidth=0,
                             focuscolor='none')

    def create_main_interface(self):
        """创建主界面"""
        # 主容器
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # 顶部标题区域
        self.create_header(main_container)

        # 二进制数显示区域
        self.create_binary_display(main_container)

        # 主要内容区域
        content_frame = tk.Frame(main_container, bg='#1a1a2e')
        content_frame.pack(fill='both', expand=True, pady=20)

        # 左侧控制面板
        self.create_control_panel(content_frame)

        # 右侧图像显示区域
        self.create_image_display(content_frame)

        # 底部状态栏
        self.create_status_bar(main_container)

    def create_header(self, parent):
        """创建顶部标题区域"""
        header_frame = tk.Frame(parent, bg='#1a1a2e')
        header_frame.pack(fill='x', pady=(0, 20))

        # 主标题
        title_label = tk.Label(
            header_frame,
            text="Image to Binary Converter",
            font=('Segoe UI', 32, 'bold'),
            fg='#e94560',
            bg='#1a1a2e'
        )
        title_label.pack()

        # 副标题
        subtitle_label = tk.Label(
            header_frame,
            text="Transform your images into stunning black and white binary art",
            font=('Segoe UI', 14),
            fg='#8b8b8b',
            bg='#1a1a2e'
        )
        subtitle_label.pack(pady=(5, 0))

        # 装饰线
        separator = tk.Frame(header_frame, height=3, bg='#e94560')
        separator.pack(fill='x', pady=20)

    def create_binary_display(self, parent):
        """创建二进制数显示区域"""
        binary_frame = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        binary_frame.pack(fill='x', pady=(0, 20))

        # 标题
        binary_title = tk.Label(
            binary_frame,
            text="Binary Number Showcase",
            font=('Segoe UI', 16, 'bold'),
            fg='#e94560',
            bg='#16213e'
        )
        binary_title.pack(pady=(20, 15))

        # 数字容器
        numbers_container = tk.Frame(binary_frame, bg='#16213e')
        numbers_container.pack(pady=(0, 20))

        numbers = [196, 111, 56]
        colors = ['#e94560', '#00d4aa', '#ff6b6b']

        for i, (num, color) in enumerate(zip(numbers, colors)):
            num_frame = tk.Frame(numbers_container, bg='#0f3460', relief='flat', bd=0)
            num_frame.pack(side='left', padx=10, pady=5)

            # 数字标签
            num_label = tk.Label(
                num_frame,
                text=f"Number {i + 1}",
                font=('Segoe UI', 12, 'bold'),
                fg='white',
                bg='#0f3460'
            )
            num_label.pack(pady=(10, 5))

            # 十进制数
            decimal_label = tk.Label(
                num_frame,
                text=str(num),
                font=('Segoe UI', 18, 'bold'),
                fg=color,
                bg='#0f3460'
            )
            decimal_label.pack()

            # 二进制数
            binary = bin(num)[2:].zfill(8)
            binary_label = tk.Label(
                num_frame,
                text=binary,
                font=('Consolas', 14, 'bold'),
                fg='#00d4aa',
                bg='#0f3460'
            )
            binary_label.pack(pady=(5, 10))

    def create_image_display(self, parent):
        """创建右侧图像显示区域"""
        image_frame = tk.Frame(parent, bg='#16213e')
        image_frame.pack(side='right', fill='both', expand=True)

        # 原始图像区域
        original_frame = tk.LabelFrame(
            image_frame,
            text="Original Image",
            font=('Segoe UI', 12, 'bold'),
            fg='#e94560',
            bg='#16213e',
            relief='flat',
            bd=1
        )
        original_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))

        # 原始图像信息标签
        self.original_info_label = tk.Label(
            original_frame,
            text="No image loaded",
            font=('Segoe UI', 9),
            fg='#8b8b8b',
            bg='#16213e'
        )
        self.original_info_label.pack(pady=(5, 0))

        self.original_canvas = tk.Canvas(
            original_frame,
            bg='#0f3460',
            width=400,
            height=400,
            relief='flat',
            bd=0,
            highlightthickness=0,
            selectbackground='#e94560'
        )
        self.original_canvas.pack(padx=10, pady=10, fill='both', expand=True)

        # 二进制图像区域
        binary_frame = tk.LabelFrame(
            image_frame,
            text="Binary Image",
            font=('Segoe UI', 12, 'bold'),
            fg='#e94560',
            bg='#16213e',
            relief='flat',
            bd=1
        )
        binary_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))

        # 二进制图像信息标签
        self.binary_info_label = tk.Label(
            binary_frame,
            text="No binary image",
            font=('Segoe UI', 9),
            fg='#8b8b8b',
            bg='#16213e'
        )
        self.binary_info_label.pack(pady=(5, 0))

        self.binary_canvas = tk.Canvas(
            binary_frame,
            bg='#0f3460',
            width=400,
            height=400,
            relief='flat',
            bd=0,
            highlightthickness=0,
            selectbackground='#e94560'
        )
        self.binary_canvas.pack(padx=10, pady=10, fill='both', expand=True)

    def create_status_bar(self, parent):
        """创建底部状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select an image to begin")

        status_frame = tk.Frame(parent, bg='#0f3460', relief='flat', bd=0)
        status_frame.pack(fill='x', pady=(20, 0))

        status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            relief='flat',
            anchor='w',
            font=('Segoe UI', 10),
            bg='#0f3460',
            fg='#8b8b8b',
            padx=10,
            pady=5
        )
        status_bar.pack(fill='x')

    def start_animations(self):
        """启动界面动画"""

        def animate_progress():
            while True:
                if self.is_processing:
                    for i in range(101):
                        if not self.is_processing:
                            break
                        self.progress_var.set(i)
                        time.sleep(0.02)
                    self.progress_var.set(0)
                time.sleep(0.1)

        animation_thread = threading.Thread(target=animate_progress, daemon=True)
        animation_thread.start()

    def browse_file(self):
        """浏览文件"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png *.bmp *.gif'),
            ('JPEG files', '*.jpg *.jpeg'),
            ('PNG files', '*.png'),
            ('All files', '*.*')
        ]

        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=file_types
        )

        if filename:
            self.image_path.set(filename)
            self.load_original_image()

    def load_original_image(self):
        """加载原始图像"""
        try:
            self.original_image = Image.open(self.image_path.get())

            # 更新图像信息显示
            img_width, img_height = self.original_image.size
            img_format = self.original_image.format or "Unknown"
            img_mode = self.original_image.mode

            info_text = f"Size: {img_width}×{img_height} | Format: {img_format} | Mode: {img_mode}"
            self.original_info_label.config(text=info_text)

            self.display_image(self.original_image, self.original_canvas)
            self.convert_btn.config(state='normal')
            self.status_var.set(f"✓ Loaded: {os.path.basename(self.image_path.get())}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load image: {str(e)}")
            self.status_var.set("❌ Image loading failed")
            self.original_info_label.config(text="Failed to load image")

    def convert_to_binary(self):
        """转换为二进制图像"""
        if not self.original_image:
            messagebox.showwarning("Warning", "Please select an image file first")
            return

        self.is_processing = True
        self.convert_btn.config(state='disabled')
        self.status_var.set("🔄 Converting image...")

        def conversion_thread():
            try:
                # 转换为灰度图
                gray_image = self.original_image.convert('L')

                # 转换为二进制图像
                self.binary_image = gray_image.convert('1')

                # 在主线程中更新UI
                self.root.after(0, self.conversion_complete)

            except Exception as e:
                self.root.after(0, lambda: self.conversion_error(str(e)))

        thread = threading.Thread(target=conversion_thread, daemon=True)
        thread.start()

    def conversion_complete(self):
        """转换完成"""
        self.is_processing = False
        self.convert_btn.config(state='normal')
        self.save_btn.config(state='normal')

        # 显示二进制图像
        self.display_image(self.binary_image, self.binary_canvas)

        # 更新二进制图像信息显示
        if self.binary_image:
            img_width, img_height = self.binary_image.size
            info_text = f"Binary Size: {img_width}×{img_height} | Mode: {self.binary_image.mode}"
            self.binary_info_label.config(text=info_text)

        self.status_var.set("✅ Conversion completed successfully")
        messagebox.showinfo("Success", "Image successfully converted to binary format!")

    def conversion_error(self, error_msg):
        """转换错误"""
        self.is_processing = False
        self.convert_btn.config(state='normal')
        messagebox.showerror("Error", f"Conversion failed: {error_msg}")
        self.status_var.set("❌ Conversion failed")

    def display_image(self, image, canvas):
        """在画布上显示图像 - 使用高质量渲染"""
        if image is None:
            return

        canvas.delete("all")

        # 获取画布的实际尺寸
        canvas.update_idletasks()  # 确保画布尺寸已更新
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 400
            canvas_height = 400

        # 获取图像尺寸
        img_width, img_height = image.size

        # 计算最佳缩放比例，保持宽高比
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y) * 0.95  # 留出一些边距

        # 计算新的图像尺寸
        new_width = max(1, int(img_width * scale))
        new_height = max(1, int(img_height * scale))

        # 使用最高质量的图像缩放算法
        try:
            if scale > 1:
                # 放大图像：使用BICUBIC + 锐化
                resized_image = image.resize((new_width, new_height), Image.Resampling.BICUBIC)
                # 应用轻微锐化以增强细节
                resized_image = resized_image.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            else:
                # 缩小图像：使用LANCZOS以获得最佳质量
                resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        except Exception:
            # 如果高级算法失败，使用默认算法
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 应用图像增强处理
        try:
            # 锐化处理
            if self.image_quality['sharpness'] != 1.0:
                enhancer = ImageEnhance.Sharpness(resized_image)
                resized_image = enhancer.enhance(self.image_quality['sharpness'])

            # 对比度调整
            if self.image_quality['contrast'] != 1.0:
                enhancer = ImageEnhance.Contrast(resized_image)
                resized_image = enhancer.enhance(self.image_quality['contrast'])

            # 亮度调整
            if self.image_quality['brightness'] != 1.0:
                enhancer = ImageEnhance.Brightness(resized_image)
                resized_image = enhancer.enhance(self.image_quality['brightness'])

        except Exception as e:
            # 如果图像处理失败，继续使用原始调整后的图像
            pass

        # 创建高质量的PhotoImage
        try:
            photo = ImageTk.PhotoImage(resized_image)
        except Exception:
            # 如果PhotoImage创建失败，尝试转换图像模式
            try:
                if resized_image.mode not in ('RGB', 'RGBA', 'L', '1'):
                    resized_image = resized_image.convert('RGB')
                photo = ImageTk.PhotoImage(resized_image)
            except Exception:
                # 最后的备选方案
                resized_image = resized_image.convert('RGB')
                photo = ImageTk.PhotoImage(resized_image)

        # 计算图像在画布中的位置（居中显示）
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2

        # 在画布上显示图像
        canvas.create_image(x, y, anchor='nw', image=photo)
        canvas.image = photo  # 保持引用防止垃圾回收

        # 添加边框以突出显示
        canvas.create_rectangle(x - 1, y - 1, x + new_width + 1, y + new_height + 1,
                                outline='#e94560', width=2)

    def save_result(self):
        """保存结果"""
        if not self.binary_image:
            messagebox.showwarning("Warning", "No binary image to save")
            return

        file_types = [
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg'),
            ('BMP files', '*.bmp'),
            ('All files', '*.*')
        ]

        filename = filedialog.asksaveasfilename(
            title="Save Binary Image",
            defaultextension=".png",
            filetypes=file_types
        )

        if filename:
            try:
                self.binary_image.save(filename)
                self.status_var.set(f"💾 Saved: {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Image saved successfully to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {str(e)}")
                self.status_var.set("❌ Save failed")

    def update_image_quality(self, *args):
        """更新图像质量设置并重新显示图像"""
        self.image_quality['sharpness'] = self.sharpness_var.get()
        self.image_quality['contrast'] = self.contrast_var.get()
        self.image_quality['brightness'] = self.brightness_var.get()

        # 重新显示原始图像
        if self.original_image:
            self.display_image(self.original_image, self.original_canvas)

        # 重新显示二进制图像
        if self.binary_image:
            self.display_image(self.binary_image, self.binary_canvas)

    def reset_image_quality(self):
        """重置图像质量设置到默认值"""
        # 重置默认值
        self.image_quality = {
            'sharpness': 1.2,
            'contrast': 1.1,
            'brightness': 1.0
        }

        # 更新滑块值
        self.sharpness_var.set(1.2)
        self.contrast_var.set(1.1)
        self.brightness_var.set(1.0)

        # 重新显示图像
        if self.original_image:
            self.display_image(self.original_image, self.original_canvas)

        if self.binary_image:
            self.display_image(self.binary_image, self.binary_canvas)

        self.status_var.set("✅ Image quality reset to default")

    def apply_preset(self, preset):
        """应用预设图像质量"""
        if preset == 'high_quality':
            self.image_quality = {
                'sharpness': 1.5,
                'contrast': 1.5,
                'brightness': 1.5
            }
        elif preset == 'standard':
            self.image_quality = {
                'sharpness': 1.2,
                'contrast': 1.1,
                'brightness': 1.0
            }
        elif preset == 'sharp':
            self.image_quality = {
                'sharpness': 1.8,
                'contrast': 1.8,
                'brightness': 1.8
            }

        # 更新滑块值
        self.sharpness_var.set(self.image_quality['sharpness'])
        self.contrast_var.set(self.image_quality['contrast'])
        self.brightness_var.set(self.image_quality['brightness'])

        # 重新显示图像
        if self.original_image:
            self.display_image(self.original_image, self.original_canvas)

        if self.binary_image:
            self.display_image(self.binary_image, self.binary_canvas)

        self.status_var.set("✅ Image quality preset applied")

    def create_control_panel(self, parent):
        """创建左侧控制面板"""
        control_frame = tk.Frame(parent, bg='#16213e', relief='flat', bd=0)
        control_frame.pack(side='left', fill='y', padx=(0, 20))

        # 文件选择区域
        file_section = tk.LabelFrame(
            control_frame,
            text="File Selection",
            font=('Segoe UI', 12, 'bold'),
            fg='#e94560',
            bg='#16213e',
            relief='flat',
            bd=1
        )
        file_section.pack(fill='x', pady=(0, 20))

        # 文件路径显示
        self.file_entry = tk.Entry(
            file_section,
            textvariable=self.image_path,
            font=('Segoe UI', 10),
            state='readonly',
            bg='#0f3460',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=5
        )
        self.file_entry.pack(fill='x', padx=10, pady=10)

        # 浏览按钮
        browse_btn = tk.Button(
            file_section,
            text="📁 Browse Files",
            command=self.browse_file,
            font=('Segoe UI', 11, 'bold'),
            bg='#e94560',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            activebackground='#d63384',
            activeforeground='white'
        )
        browse_btn.pack(pady=(0, 10))

        # 转换控制区域
        convert_section = tk.LabelFrame(
            control_frame,
            text="Conversion",
            font=('Segoe UI', 12, 'bold'),
            fg='#e94560',
            bg='#16213e',
            relief='flat',
            bd=1
        )
        convert_section.pack(fill='x', pady=(0, 20))

        # 转换按钮
        self.convert_btn = tk.Button(
            convert_section,
            text="🔄 Convert to Binary",
            command=self.convert_to_binary,
            font=('Segoe UI', 11, 'bold'),
            bg='#00d4aa',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            activebackground='#00b894',
            activeforeground='white',
            state='disabled'
        )
        self.convert_btn.pack(pady=10)

        # 保存按钮
        self.save_btn = tk.Button(
            convert_section,
            text="💾 Save Result",
            command=self.save_result,
            font=('Segoe UI', 11, 'bold'),
            bg='#ff6b6b',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            activebackground='#ee5a52',
            activeforeground='white',
            state='disabled'
        )
        self.save_btn.pack(pady=(0, 10))

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            convert_section,
            variable=self.progress_var,
            maximum=100,
            length=200,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)

        # 图像质量控制面板
        quality_section = tk.LabelFrame(
            control_frame,
            text="Image Quality Settings",
            font=('Segoe UI', 12, 'bold'),
            fg='#e94560',
            bg='#16213e',
            relief='flat',
            bd=1
        )
        quality_section.pack(fill='x', pady=(10, 0))

        # 锐化控制
        sharpness_frame = tk.Frame(quality_section, bg='#16213e')
        sharpness_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            sharpness_frame,
            text="Sharpness:",
            font=('Segoe UI', 9),
            fg='#8b8b8b',
            bg='#16213e'
        ).pack(side='left')

        self.sharpness_var = tk.DoubleVar(value=self.image_quality['sharpness'])
        sharpness_scale = tk.Scale(
            sharpness_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            variable=self.sharpness_var,
            orient='horizontal',
            bg='#16213e',
            fg='#8b8b8b',
            highlightthickness=0,
            troughcolor='#0f3460',
            activebackground='#e94560',
            command=self.update_image_quality
        )
        sharpness_scale.pack(side='right', fill='x', expand=True, padx=(10, 0))

        # 对比度控制
        contrast_frame = tk.Frame(quality_section, bg='#16213e')
        contrast_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            contrast_frame,
            text="Contrast:",
            font=('Segoe UI', 9),
            fg='#8b8b8b',
            bg='#16213e'
        ).pack(side='left')

        self.contrast_var = tk.DoubleVar(value=self.image_quality['contrast'])
        contrast_scale = tk.Scale(
            contrast_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            variable=self.contrast_var,
            orient='horizontal',
            bg='#16213e',
            fg='#8b8b8b',
            highlightthickness=0,
            troughcolor='#0f3460',
            activebackground='#e94560',
            command=self.update_image_quality
        )
        contrast_scale.pack(side='right', fill='x', expand=True, padx=(10, 0))

        # 亮度控制
        brightness_frame = tk.Frame(quality_section, bg='#16213e')
        brightness_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            brightness_frame,
            text="Brightness:",
            font=('Segoe UI', 9),
            fg='#8b8b8b',
            bg='#16213e'
        ).pack(side='left')

        self.brightness_var = tk.DoubleVar(value=self.image_quality['brightness'])
        brightness_scale = tk.Scale(
            brightness_frame,
            from_=0.5,
            to=1.5,
            resolution=0.1,
            variable=self.brightness_var,
            orient='horizontal',
            bg='#16213e',
            fg='#8b8b8b',
            highlightthickness=0,
            troughcolor='#0f3460',
            activebackground='#e94560',
            command=self.update_image_quality
        )
        brightness_scale.pack(side='right', fill='x', expand=True, padx=(10, 0))

        # 重置按钮
        reset_frame = tk.Frame(quality_section, bg='#16213e')
        reset_frame.pack(fill='x', padx=10, pady=10)

        reset_btn = tk.Button(
            reset_frame,
            text="Reset to Default",
            command=self.reset_image_quality,
            font=('Segoe UI', 9, 'bold'),
            bg='#e94560',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2'
        )
        reset_btn.pack(side='right')

        # 预设按钮框架
        preset_frame = tk.Frame(quality_section, bg='#16213e')
        preset_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(
            preset_frame,
            text="Presets:",
            font=('Segoe UI', 9, 'bold'),
            fg='#8b8b8b',
            bg='#16213e'
        ).pack(side='left')

        # 高质量预设
        high_quality_btn = tk.Button(
            preset_frame,
            text="High Quality",
            command=lambda: self.apply_preset('high_quality'),
            font=('Segoe UI', 8, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=10,
            pady=3,
            cursor='hand2'
        )
        high_quality_btn.pack(side='left', padx=(10, 5))

        # 标准预设
        standard_btn = tk.Button(
            preset_frame,
            text="Standard",
            command=lambda: self.apply_preset('standard'),
            font=('Segoe UI', 8, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=10,
            pady=3,
            cursor='hand2'
        )
        standard_btn.pack(side='left', padx=5)

        # 锐利预设
        sharp_btn = tk.Button(
            preset_frame,
            text="Sharp",
            command=lambda: self.apply_preset('sharp'),
            font=('Segoe UI', 8, 'bold'),
            bg='#e67e22',
            fg='white',
            relief='flat',
            padx=10,
            pady=3,
            cursor='hand2'
        )
        sharp_btn.pack(side='left', padx=5)

        # 信息面板
        info_section = tk.LabelFrame(
            control_frame,
            text="Information",
            font=('Segoe UI', 12, 'bold'),
            fg='#e94560',
            bg='#16213e',
            relief='flat',
            bd=1
        )
        info_section.pack(fill='x')

        info_text = tk.Text(
            info_section,
            height=8,
            font=('Segoe UI', 9),
            bg='#0f3460',
            fg='#8b8b8b',
            relief='flat',
            bd=0,
            wrap='word'
        )
        info_text.pack(fill='both', padx=10, pady=10)
        info_text.insert('1.0',
                         "Welcome to the Modern Image to Binary Converter!\n\n"
                         "Features:\n"
                         "• Convert images to black & white\n"
                         "• Real-time preview\n"
                         "• Multiple output formats\n"
                         "• Modern UI design\n\n"
                         "Supported formats:\n"
                         "JPG, PNG, BMP, GIF"
                         )
        info_text.config(state='disabled')


def main():
    root = tk.Tk()
    app = ModernImageToBinaryGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()