# Smart Tourism System -- Streamlit + Ollama (Colab/Pinggy)

Ứng dụng tạo lịch trình du lịch tự động theo ngày
(Morning/Afternoon/Evening) dựa trên thông tin người dùng nhập:\
**Origin -- Destination -- Dates -- Interests -- Pace**.

Giao diện FE được xây bằng **Streamlit**.\
LLM chạy ở BE được host bằng **Ollama** thông qua **Colab +
Pinggy/ngrok**.

Ứng dụng hỗ trợ:\
✅ Login / Register\
✅ Lưu lịch sử chat theo từng người dùng\
✅ Sinh lịch trình đa ngày\
✅ Tuân thủ format rõ ràng Morning/Afternoon/Evening\
✅ Tách FE & BE độc lập

------------------------------------------------------------------------

## 1. Cấu trúc dự án

    project/
    │── app.py
    │── data/
    │── 2a_ollama_pinggy_ngrok.py
    │── README.md
    │── requirements.txt

------------------------------------------------------------------------

## 2. Cài đặt & chạy hệ thống

### 2.1. Máy local

    pip install -r requirements.txt

### 2.2. Colab backend

Chạy file `2a_ollama_pinggy_ngrok.py` để tạo server Ollama + Pinggy.

------------------------------------------------------------------------

## 3. Chạy Streamlit

    streamlit run app.py

------------------------------------------------------------------------

## 4. Computational Thinking Report

### 4.1. Decomposition

Phân rã hệ thống thành FE, BE, quản lý user, chat history, prompt
engine.

### 4.2. Pattern Recognition

Nhận dạng mô hình lặp lại: Morning/Afternoon/Evening, workflow
login→input→LLM→output.

### 4.3. Abstraction

Giữ các yếu tố cốt lõi: origin, destination, dates, interests, pace.

### 4.4. Algorithm Design

    START
    User login
    User input travel info
    Build prompt
    Send to LLM
    Display itinerary
    Save history
    END

------------------------------------------------------------------------

## 5. Khuyến nghị model

-   Qwen 0.5B → nhanh nhất\
-   LLaMA 3.2 1B → cân bằng\
-   Qwen 1.5B → chi tiết hơn

------------------------------------------------------------------------

## 6. Tác giả

Sinh viên: ...\
Môn: Computational Thinking\
Dự án: Smart Tourism System 2025
