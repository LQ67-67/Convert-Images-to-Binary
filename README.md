# Convert-Images-to-Binary
## 🧾 `Image to binary (Simple Version).py`

### 📌 简介 | Description

这是一个基础的图像转黑白脚本，使用 Python Pillow 库读取图像，打印像素值，并将图像转换为黑白后显示。
This is a basic image-to-binary converter using the Pillow library. It prints the pixel values and displays the converted black-and-white image.

### 🚀 功能 | Features

* 读取默认图像文件（默认文件名为 `1.jpg`）
* 打印图像每个像素的 RGB 值
* 将图像转换为黑白（二值图像）
* 显示转换后的图像

### ▶️ 使用方法 | How to Use

1. 安装 Pillow 库：
   Install Pillow:

   ```bash
   pip install pillow
   ```

2. 将你要转换的图像重命名为 `1.jpg` 并放在脚本所在目录。
   Rename your image as `1.jpg` and put it in the same directory as the script.

3. 运行脚本：
   Run the script:

   ```bash
   python "Image to binary (Simple Version).py"
   ```

### 📁 文件说明 | File

* `Image to binary (Simple Version).py`：主程序文件
  The main Python script

---

## 🧾 `images to binary (Complex Version).py`

### 📌 简介 | Description

一个拥有现代化界面的图像转黑白程序，支持图像增强（亮度、对比度、锐化）、实时预览、保存输出等功能。
A modern GUI-based image-to-binary converter. Supports brightness, contrast, sharpness adjustments, live preview, and saving results.

### 🚀 功能 | Features

* 支持 JPG、PNG、BMP、GIF 等多种格式
  Supports multiple image formats (JPG, PNG, BMP, GIF)
* 图像转换为灰度后进一步转为黑白（二值）图像
  Converts image to grayscale, then to binary (black & white)
* 可调图像增强设置（亮度、对比度、锐度）
  Adjustable image enhancement (brightness, contrast, sharpness)
* 实时预览原始与转换后的图像
  Live preview of original and binary images
* 可保存图像为 PNG/JPG/BMP
  Save output as PNG, JPG, or BMP
* 动画进度条与状态栏提示
  Animated progress bar and status messages
* 暗色主题现代 UI 设计
  Modern dark-themed user interface

### ▶️ 使用方法 | How to Use

1. 安装 Pillow 库：
   Install Pillow:

   ```bash
   pip install pillow
   ```

2. 运行程序：
   Run the application:

   ```bash
   python "images to binary (Complex Version).py"
   ```

3. 在界面中选择图像，点击 "Convert to Binary"，调整参数或保存结果。
   Browse an image in the GUI, click "Convert to Binary", adjust quality or save the result.

### 📁 文件说明 | Files

* `images to binary (Complex Version).py`：带图形界面的主程序
  Main GUI program file
