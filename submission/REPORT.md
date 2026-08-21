# BÁO CÁO THỰC NGHIỆM MLOPS (LAB DAY 21)
**Học viên:** Trần Văn Tài | **Mã học viên:** 2A202601339  
**Khoá học:** AIInAction - VinUni (K3) | **Buổi:** Day 21 - CI/CD cho AI Systems

---

## 1. Bảng Tổng Hợp Kết Quả Thực Nghiệm (Bước 1 - 9 Lần Chạy)

Toàn bộ các thí nghiệm được thực hiện trên tập `train_phase1.csv` (2,998 mẫu) và đánh giá trên `eval.csv` (500 mẫu), được ghi vết tự động vào **MLflow Tracking (SQLite)**:

| STT | Run Name | `n_estimators` | `max_depth` | `min_samples_split` | Accuracy | F1-Score (Weighted) | Đánh Giá |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `shivering-koi-915` | **200** | **20** | **2** | **0.6840** | **0.6830** | 🏆 **Tối ưu nhất (Champion Model)** |
| 2 | `honorable-kit-469` | 100 | 20 | 2 | 0.6840 | 0.6829 | Tương đương (F1 thấp hơn xíu) |
| 3 | `respected-bee-410` | 300 | 20 | 2 | 0.6780 | 0.6767 | Tốt |
| 4 | `capable-crab-419` | 150 | 25 | 2 | 0.6780 | 0.6764 | Tốt |
| 5 | `abrasive-seal-499` | 200 | 10 | 5 | 0.6440 | 0.6417 | Khá |
| 6 | `mysterious-panda-825` | 50 | 5 | 2 | 0.5680 | 0.5536 | Trung bình |
| 7 | `masked-roo-829` | 100 | 5 | 2 | 0.5640 | 0.5534 | Baseline chuẩn |
| 8 | `bright-kit-272` | 100 | 5 | 2 | 0.5640 | 0.5534 | Baseline chuẩn |
| 9 | `delightful-colt-234` | 50 | 3 | 5 | 0.5580 | 0.5185 | Underfitting do cây quá nông |

---

## 2. Phân Tích & Lý Giải Bộ Siêu Tham Số Tối Ưu

### Bộ tham số được lựa chọn lưu vào `params.yaml`:
```yaml
n_estimators: 200
max_depth: 20
min_samples_split: 2
```

### Lý do kỹ thuật:
1. **Khắc phục Underfitting hoàn toàn**: Khi tăng độ sâu tối đa lên `max_depth = 20`, mô hình có đủ khả năng học các tổ hợp đặc trưng phức tạp của 12 chỉ số hóa sinh (nồng độ cồn, độ pH, độ axit, SO2 tự do/tổng), giúp Accuracy tăng vọt từ **55.8% lên 68.40%** (tăng +12.6%).
2. **Cân bằng Bias - Variance với Ensemble**: Sử dụng `n_estimators = 200` tạo ra tập hợp đủ lớn các cây quyết định độc lập, triệt tiêu phương sai cá thể và làm mượt biên phân lớp.
3. **F1-Score cao nhất (0.6830)**: F1-score phản ánh độ chính xác phân loại đồng đều trên cả 3 mức chất lượng rượu (thấp, trung bình, cao), tránh thiên lệch về nhóm đa số.

---

## 3. Khó Khăn Gặp Phải & Cách Giải Quyết

* **Khó khăn 1 (Môi trường Python 3.12 & MLflow)**: Khi chạy `train.py`, MLflow báo lỗi `ModuleNotFoundError: No module named 'pkg_resources'` do phiên bản `setuptools >= 80` mặc định trên Python 3.12.
  * **Giải pháp**: Cài đặt `setuptools-71.1.0` (`pip install "setuptools<72"`), giúp SQLite backend và Model Registry hoạt động ổn định.
* **Khó khăn 2 (Hiển thị UI)**: Giao diện MLflow UI mặc định ẩn các cột tham số và chỉ số đánh giá.
  * **Giải pháp**: Sử dụng tùy chọn `Columns` trên MLflow UI để bật hiển thị đầy đủ `accuracy`, `f1_score`, `max_depth`, `n_estimators`, `min_samples_split`, sắp xếp theo `accuracy` giảm dần để chụp màn hình minh chứng nộp bài.

---

## 4. Minh Chứng Ảnh Chụp Giao Diện (Artifacts)
Ảnh chụp giao diện MLflow UI lưu tại: `submission/screenshots/MLflowUI.png`
