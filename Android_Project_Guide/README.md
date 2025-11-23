# Android 版 Anan's Sketchbook Chat Box 构建指南

这个指南将帮助你使用 Flutter 将此项目构建为 Android 应用 (APK)。Flutter 是一个跨平台的 UI 框架，非常适合这种图形处理应用。

## 1. 准备工作

### 安装 Flutter SDK

如果你还没有安装 Flutter，请访问 [Flutter 官网](https://flutter.dev/docs/get-started/install) 按照教程安装 Flutter SDK 并配置 Android 开发环境（Android Studio）。

### 验证环境

在终端运行以下命令，确保没有报错：

```bash
flutter doctor
```

## 2. 创建新项目

在你的工作目录中（不要在当前 Python 项目文件夹内，建议在外面新建一个文件夹），运行：

```bash
flutter create sketchbook_chat_box
cd sketchbook_chat_box
```

## 3. 复制代码和配置

我们将使用本目录 (`Android_Project_Guide`) 中生成的文件来替换新项目中的文件。

1.  **替换 `pubspec.yaml`**:
    将 `Android_Project_Guide/pubspec.yaml` 的内容复制并覆盖到你新创建的 `sketchbook_chat_box/pubspec.yaml` 中。

2.  **替换 `lib/main.dart`**:
    将 `Android_Project_Guide/lib/main.dart` 的内容复制并覆盖到 `sketchbook_chat_box/lib/main.dart` 中。

## 4. 导入资源文件

这是最重要的一步。你需要将 Python 项目中的图片和字体复制到 Flutter 项目中。

1.  在 `sketchbook_chat_box` 项目根目录下，创建一个名为 `assets` 的文件夹。
2.  在 `assets` 文件夹内，创建两个子文件夹：`BaseImages` 和 `fonts`。
3.  **复制图片**:
    将 Python 项目中的 `BaseImages` 文件夹内的**所有图片文件**（如 `base.png`, `开心.png` 等）复制到 `sketchbook_chat_box/assets/BaseImages/` 中。
    _注意：确保文件名与 `lib/main.dart` 代码中的 `_emotionMap` 映射一致。_
4.  **复制字体**:
    将 Python 项目中的 `font.ttf` 文件复制到 `sketchbook_chat_box/assets/fonts/` 中。如果没有 `font.ttf`，请找一个你喜欢的字体文件重命名为 `font.ttf` 放进去。

此时你的目录结构应该像这样：

```
sketchbook_chat_box/
  assets/
    BaseImages/
      base.png
      开心.png
      ...
    fonts/
      font.ttf
  lib/
    main.dart
  pubspec.yaml
  ...
```

## 5. 获取依赖并运行

在 `sketchbook_chat_box` 目录下打开终端：

1.  获取依赖包：

    ```bash
    flutter pub get
    ```

2.  连接你的 Android 手机（开启 USB 调试）或启动模拟器。

3.  运行应用：
    ```bash
    flutter run
    ```

## 6. 打包 APK

如果你想生成可以安装的 APK 文件分享给别人：

```bash
flutter build apk --release
```

构建完成后，APK 文件通常位于 `build/app/outputs/flutter-apk/app-release.apk`。

## 功能说明

- **文字输入**: 输入你想说的话。
- **表情切换**: 点击下拉菜单选择表情，或者在文字中包含 `#开心#` 等标签自动切换。
- **变色文字**: 使用 `【` 和 `】` 包裹的文字会变成紫色（如代码中配置）。
- **生成并分享**: 点击按钮后，应用会生成图片并调用系统的分享功能（可以直接发送给 QQ、微信好友）。

## 注意事项

- 代码中的坐标 `_textArea` 是根据默认的 `base.png` 设置的。如果你修改了底图尺寸，可能需要调整 `lib/main.dart` 中的 `_textArea` 坐标。
- 目前只实现了“文字转图片”的功能，因为在 Android 上处理剪贴板图片权限较复杂且体验不佳，直接输入文字生成是更流畅的移动端体验。
