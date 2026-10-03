import streamlit as st
st.image("IMG_5330.jpg")
# ==============================
# CẤU HÌNH TRANG
# ==============================

st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ==============================
# TIÊU ĐỀ
# ==============================

st.title("💰 TÍNH LÃI GỬI TIẾT KIỆM")
st.write("Nhập thông tin tiền gửi để tính tiền lãi và số tiền nhận được.")

st.divider()

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================

def format_money(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")


# ==============================
# NHẬP THÔNG TIN
# ==============================

st.subheader("📋 Thông tin tiền gửi")

so_tien_gui = st.number_input(
    "💵 Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=10_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "📅 Kỳ hạn (tháng)",
    min_value=1,
    max_value=120,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "📈 Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f"
)

hinh_thuc = st.selectbox(
    "💳 Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

st.divider()

# ==============================
# NÚT TÍNH TOÁN
# ==============================

if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
    
    elif lai_suat < 0:
        st.error("Lãi suất không hợp lệ.")

    else:

        # Chuyển lãi suất % sang số thập phân
        lai_suat_nam = lai_suat / 100

        # Thời gian gửi tính theo năm
        thoi_gian_nam = ky_han / 12

        # ======================================
        # TRƯỜNG HỢP NHẬN LÃI CUỐI KỲ
        # ======================================

        if hinh_thuc == "Cuối kỳ":

            tong_tien_lai = (
                so_tien_gui
                * lai_suat_nam
                * thoi_gian_nam
            )

            tien_lai_dinh_ky = tong_tien_lai

            tong_tien_nhan = so_tien_gui + tong_tien_lai

            so_ky_nhan_lai = 1

        # ======================================
        # TRƯỜNG HỢP NHẬN LÃI HÀNG THÁNG
        # ======================================

        elif hinh_thuc == "Hàng tháng":

            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat_nam
                / 12
            )

            so_ky_nhan_lai = ky_han

            tong_tien_lai = (
                tien_lai_dinh_ky
                * so_ky_nhan_lai
            )

            tong_tien_nhan = so_tien_gui + tong_tien_lai

        # ======================================
        # TRƯỜNG HỢP NHẬN LÃI HÀNG QUÝ
        # ======================================

        else:

            tien_lai_dinh_ky = (
                so_tien_gui
                * lai_suat_nam
                / 4
            )

            so_ky_nhan_lai = ky_han // 3

            # Nếu kỳ hạn không chia hết cho 3,
            # phần tháng lẻ vẫn được tính theo tỷ lệ thời gian
            tong_tien_lai = (
                so_tien_gui
                * lai_suat_nam
                * thoi_gian_nam
            )

            tong_tien_nhan = so_tien_gui + tong_tien_lai

        # ==============================
        # HIỂN THỊ KẾT QUẢ
        # ==============================

        st.success("✅ Tính toán thành công!")

        st.subheader("📊 Kết quả")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💵 Tiền lãi định kỳ",
                format_money(tien_lai_dinh_ky)
            )

        with col2:
            st.metric(
                "💰 Tổng tiền lãi",
                format_money(tong_tien_lai)
            )

        st.metric(
            "🏦 Tổng tiền gốc + lãi",
            format_money(tong_tien_nhan)
        )

        # ==============================
        # CHI TIẾT
        # ==============================

        st.divider()

        st.subheader("📝 Chi tiết khoản tiền gửi")

        st.write(f"**Số tiền gửi:** {format_money(so_tien_gui)}")
        st.write(f"**Kỳ hạn:** {ky_han} tháng")
        st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
        st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

        if hinh_thuc == "Cuối kỳ":
            st.info(
                f"Bạn nhận toàn bộ tiền lãi "
                f"{format_money(tong_tien_lai)} vào cuối kỳ."
            )

        elif hinh_thuc == "Hàng tháng":
            st.info(
                f"Mỗi tháng bạn nhận khoảng "
                f"{format_money(tien_lai_dinh_ky)} tiền lãi."
            )

        else:
            st.info(
                f"Mỗi quý bạn nhận khoảng "
                f"{format_money(tien_lai_dinh_ky)} tiền lãi."
            )

# ==============================
# GHI CHÚ
# ==============================

st.divider()

st.caption(
    "ℹ️ Công cụ sử dụng phương pháp tính lãi đơn, "
    "chưa tính lãi kép hoặc các chính sách riêng của từng ngân hàng."
)
