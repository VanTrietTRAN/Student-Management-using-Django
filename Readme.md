# Pandosima intern starter project
We publish this repository to help students, who wisht to join Pandosima's intership/open training program, have chance to adtap with technologies and build something for yourself.
* Checkout this project as a starter point.
* Follow the guideline in Readme files to setup enviroment, build and run the backend, frontend. 
* Then take a look on the project's structure, coding convention,...
* Read the requirements in Todo.md files to implement/develop features and functions as your own.

## Requirements

* MySQL Client 8.0
* Python 3.12.2. Note: One Mac OSX, after install python, make sure to go to the `Applications/<your python folder>` and rund the command `Install Certificates.command`.
* Node 22.14.0 (LTS) or later
* [Gettex](https://mlocati.github.io/articles/gettext-iconv-windows.html)
* You have to follow [this guide](./devtools/Readme.md) to setup local development environment before starting config or build source code.
## Preparing accounts
(Only creates these accounts for your local debuging puporse. On the server side, we already created these accounts for all environments.)
1. Create account for mailing service
    * Register an new [Google Account](https://accounts.google.com/) for mailing service 
    * Turn on [2-Steps Verification](https://support.google.com/accounts/answer/185839) for your account
    * Create an [App Passwords](https://support.google.com/mail/answer/185833) for your mailing service
    * Remember [SMTP setup options](https://support.google.com/a/answer/176600?hl=en#zippy=%2Cuse-the-restricted-gmail-smtp-server%2Cuse-the-gmail-smtp-server) to fill in `backend/config.env` later.

## Install dependencies

### Create virtual environemnt

* For Linux:

```
    python3 -m venv .venv
    source .venv/bin/activate
```

* For Mac OS:

```
    python3 -m venv .venv
    source .venv/bin/activate
```

* For Windows:

```
    py -3 -m venv .venv
    .venv\scripts\activate
```

### Install dependencies

```
    pip3 install -r requirements/base.txt
```
Note: For Mac OSX, before installing python libraries, you might have to install addition tools and export environment variables
#### Install addition tools:
```
brew install mysql-client pkg-config
```
#### Export environment variables:
```
export CFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -I/usr/local/include/ ${CFLAGS}"
export LDFLAGS="-isysroot $(xcrun --show-sdk-path) -L/usr/local/lib -L/usr/lib"
export CPPFLAGS="-isysroot $(xcrun --show-sdk-path) -I/usr/include -L/usr/lib"
export LDFLAGS="-L/opt/homebrew/opt/mysql-client/lib"
export CPPFLAGS="-I/opt/homebrew/opt/mysql-client/include"
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
```

## Config and build

### Create RSA private key

Go to the [backend](./backend/) folder and runt the command below on your terminal. If you are using Windows, the command below should be run in git bash shell instead.

```
    openssl genrsa -out oidc.key 4096
```

### Config environment variables
Copy the [backend/config.env.sample](backend/config.env.sample) to `backend/config.env`, then open the file and change values for environment variables.

### Migrate data
From the [backend](backend) folder, runt this command:
```
# Student Management (Pandosima starter)

Hướng dẫn rút gọn, tập trung vào phát triển cục bộ trên Windows (PowerShell).

Mục đích: cung cấp các bước cần thiết để chạy backend (Django) và frontend (Nuxt) trên Windows.

## Yêu cầu cơ bản
- Python 3.12+ (sử dụng `py` trên Windows)
- Node.js (khuyến nghị phiên bản tương thích với `package.json` trong `business/`)
- MySQL client / MySQL server (hoặc cấu hình DB tương ứng trong `backend/config.env`)

## Thiết lập & chạy trên Windows (PowerShell)

1) Chuẩn bị backend

```powershell
# vào thư mục backend
cd .\backend

# tạo virtual environment và kích hoạt
py -3 -m venv .venv
.\.venv\Scripts\Activate

# cài Python dependencies
pip install -r requirements/base.txt

# sao chép file mẫu cấu hình và chỉnh lại các biến môi trường (DB, EMAIL, BUSINESS_HOST...)
Copy-Item -Path .\config.env.sample -Destination .\config.env
# (Mở .\config.env và chỉnh các giá trị phù hợp với máy của bạn)

# áp dụng migrations
py manage.py migrate

# tạo các tài khoản mặc định (dùng cho phát triển cục bộ)
py create_default_accounts.py

# chạy backend
py manage.py runserver 127.0.0.1:8000
```

2) Chạy frontend (business)

Mở PowerShell mới và chạy:

```powershell
cd .\business
npm install
npm run dev
# dev server theo package.json sẽ lắng nghe ở 127.0.0.1:3008 (mở http://127.0.0.1:3008/ để truy cập)
```

3) Lưu ý tạo RSA key cho OIDC

Nếu dự án yêu cầu `oidc.key`, bạn có thể tạo bằng OpenSSL. Trên Windows, dùng Git Bash hoặc WSL để chạy:

```bash
openssl genrsa -out oidc.key 4096
```

## Tài khoản mặc định (dành cho môi trường dev)
- Student: student@university.edu / student123  (is_staff=False, is_superuser=False)
- Lecture: lecture@university.edu / lecture123  (is_staff=True, is_superuser=False)
- Admin: admin@university.edu / admin123  (is_staff=True, is_superuser=True)

Những tài khoản này được tạo bởi `backend/create_default_accounts.py`. Chỉ dùng cho phát triển cục bộ.

## Debug / Dev mode
- Nếu muốn phát triển frontend song song với backend, bật trong `backend/config.env`:

```
BUSINESS_FRONTEND_DEV_MODE=True
```

Sau đó chạy `npm run dev` trong `business/`.

## Ghi chú ngắn
- Tài liệu gốc chứa nhiều phần dành cho Mac/Linux, Docker và localization. README này đã được rút gọn để chỉ giữ các phần thiết yếu cho phát triển cục bộ trên Windows. Nếu bạn cần các hướng dẫn cho Docker hoặc macOS, tôi có thể khôi phục hoặc thêm vào file riêng.
