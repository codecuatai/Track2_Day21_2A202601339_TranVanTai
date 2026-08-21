import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from dotenv import load_dotenv

# Tải biến môi trường từ .env nếu có
load_dotenv()

# BONUS 1: Ho tro Remote Tracking voi DagsHub neu co bien moi truong
tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
mlflow.set_tracking_uri(tracking_uri)
print(f"MLflow Tracking URI: {tracking_uri}")

EVAL_THRESHOLD = 0.70



def check_data_distribution(df: pd.DataFrame) -> dict:
    """
    [BONUS 5]: Kiem tra ty le phan phoi cac lop nhan trong tap du lieu.
    In canh bao neu co lop chiem duoi 10% tong mau.
    """
    class_counts = df["target"].value_counts(normalize=True).to_dict()
    class_distribution = {int(k): round(float(v), 4) for k, v in sorted(class_counts.items())}
    
    print("\n--- [BONUS 5] PHAN PHOI TY LE LOP DU LIEU ---")
    for cls_label, prop in class_distribution.items():
        msg = f"  - Lop {cls_label}: {prop * 100:.2f}%"
        if prop < 0.10:
            print(f"{msg}  [CANH BAO: Chiem < 10% - Mat can bang du lieu!]")
        else:
            print(msg)
    print("--------------------------------------------\n")
    return class_distribution


def generate_performance_report(y_true, y_pred, acc: float, f1: float) -> str:
    """
    [BONUS 3]: Tao bao cao hieu suat chi tiet gom Confusion Matrix va Precision/Recall cho tung lop.
    """
    cm = confusion_matrix(y_true, y_pred)
    target_names = ["0 (thap)", "1 (trung_binh)", "2 (cao)"]
    
    unique_labels = sorted(list(set(y_true) | set(y_pred)))
    selected_target_names = [target_names[i] for i in unique_labels if i < len(target_names)]
    
    report_str = classification_report(
        y_true, 
        y_pred, 
        labels=unique_labels,
        target_names=selected_target_names if len(selected_target_names) == len(unique_labels) else None,
        digits=4,
        zero_division=0
    )
    
    cm_str = "Ma Tran Nhap Nho (Confusion Matrix):\n"
    cm_str += "       " + " ".join([f"Pred_{i:>2}" for i in unique_labels]) + "\n"
    for i, row in enumerate(cm):
        actual_label = unique_labels[i] if i < len(unique_labels) else i
        row_str = " ".join([f"{val:>7}" for val in row])
        cm_str += f"True_{actual_label:>2} {row_str}\n"

    full_report = (
        "===========================================================\n"
        "             BAO CAO HIEU SUAT MO HINH CHI TIET            \n"
        "===========================================================\n\n"
        f"Do chinh xac tong the (Accuracy): {acc:.4f}\n"
        f"F1-Score (Weighted):             {f1:.4f}\n\n"
        f"{cm_str}\n"
        "Chi tiet Precision / Recall / F1 tung lop:\n"
        f"{report_str}\n"
        "===========================================================\n"
    )
    return full_report


def build_model(params: dict):
    """
    [BONUS 2]: Khoi tao mo hinh dua tren model_type tu params.yaml.
    Ho tro: random_forest, gradient_boosting, extra_trees, logistic_regression.
    """
    model_params = params.copy()
    model_type = model_params.pop("model_type", "random_forest")

    if model_type == "gradient_boosting":
        valid_keys = {"n_estimators", "max_depth", "min_samples_split", "learning_rate", "subsample"}
        filtered = {k: v for k, v in model_params.items() if k in valid_keys}
        return GradientBoostingClassifier(**filtered, random_state=42), model_type
    elif model_type == "extra_trees":
        valid_keys = {"n_estimators", "max_depth", "min_samples_split", "min_samples_leaf"}
        filtered = {k: v for k, v in model_params.items() if k in valid_keys}
        return ExtraTreesClassifier(**filtered, random_state=42), model_type
    elif model_type == "logistic_regression":
        return LogisticRegression(max_iter=1000, random_state=42), model_type
    else:
        # Default: random_forest
        valid_keys = {"n_estimators", "max_depth", "min_samples_split", "min_samples_leaf"}
        filtered = {k: v for k, v in model_params.items() if k in valid_keys}
        return RandomForestClassifier(**filtered, random_state=42), "random_forest"


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow (Tich hop Bonus 2, 3, 5).
    """
    # 1. Doc du lieu
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)

    # [BONUS 5]: Kiem tra phan phoi du lieu truoc khi train
    class_dist = check_data_distribution(df_train)

    # 2. Tach dac trung (X) va nhan (y)
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    with mlflow.start_run():
        # Ghi nhan sieu tham so vao MLflow
        mlflow.log_params(params)

        # [BONUS 2]: Khoi tao mo hinh theo model_type
        model, model_type = build_model(params)
        mlflow.log_param("actual_model_type", model_type)
        print(f"Dang huan luyen thuat toan: [{model_type}]...")
        model.fit(X_train, y_train)

        # Du doan tren tap danh gia
        preds = model.predict(X_eval)
        acc = float(accuracy_score(y_eval, preds))
        f1 = float(f1_score(y_eval, preds, average="weighted"))

        # Ghi nhan chi so vao MLflow
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        # In ket qua
        print(f"Ket qua [{model_type}] -> Accuracy: {acc:.4f} | F1: {f1:.4f}")

        # [BONUS 3]: Sinh bao cao hieu suat chi tiet va ghi ra file outputs/report.txt
        os.makedirs("outputs", exist_ok=True)
        report_text = generate_performance_report(y_eval, preds, acc, f1)
        with open("outputs/report.txt", "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"Da xuat bao cao hieu suat chi tiet ra outputs/report.txt")

        # [BONUS 5]: Luu metrics.json gom ca accuracy, f1 va class_distribution
        metrics_data = {
            "accuracy": acc,
            "f1_score": f1,
            "model_type": model_type,
            "class_distribution": class_dist
        }
        with open("outputs/metrics.json", "w", encoding="utf-8") as f:
            json.dump(metrics_data, f, indent=2)

        # Luu model ra models/model.pkl
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

    return acc


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)


