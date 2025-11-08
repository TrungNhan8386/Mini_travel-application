# Smart Tourism System -- Streamlit + Ollama (Colab/Pinggy)

Ứng dụng tạo lịch trình du lịch tự động theo ngày
(Morning/Afternoon/Evening) dựa trên thông tin người dùng nhập:\
**Origin -- Destination -- Dates -- Interests -- Pace**.

Giao diện FE được xây bằng **Streamlit**.\
LLM chạy ở BE được host bằng **Ollama** thông qua **Colab +
Pinggy**.

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
    │── model_LLM.ipynb
    │── README.md

------------------------------------------------------------------------

## 2. Cài đặt & chạy hệ thống

### Colab backend

Chạy file `model.ipynb` trên **Google Colab** để tạo server Ollama + Pinggy.

------------------------------------------------------------------------

## 3. Chạy Streamlit
    pip install streamlit
    streamlit run app.py
Sao chép link được tạo từ **Pinggy** rồi dán vào phần **Server settings** trên **web Streamlit**, nếu kết quả được trả về là 200 thì đã kết nối với Model thành công

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
