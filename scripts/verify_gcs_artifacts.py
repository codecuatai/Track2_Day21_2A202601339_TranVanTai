"""Read-only verification of the DVC cache and production model in GCS."""

import os

from google.cloud import storage


DEFAULT_BUCKET = "mlops-wine-k3-2a202601339"
REQUIRED_PRODUCTION_OBJECTS = {
    "models/latest/model.pkl",
    "models/latest/metrics.json",
}


def verify_gcs_artifacts(bucket_name: str) -> list[tuple[str, int]]:
    """Return verified object names/sizes or raise when required artifacts are absent."""
    client = storage.Client()
    objects = {
        blob.name: int(blob.size or 0)
        for prefix in ("dvc/", "models/latest/")
        for blob in client.list_blobs(bucket_name, prefix=prefix)
    }

    dvc_objects = sorted(name for name in objects if name.startswith("dvc/"))
    missing = sorted(REQUIRED_PRODUCTION_OBJECTS - objects.keys())

    if not dvc_objects:
        raise SystemExit(f"FAILED: gs://{bucket_name}/dvc/ contains no DVC objects.")
    if missing:
        raise SystemExit(
            "FAILED: required production objects are missing: " + ", ".join(missing)
        )

    verified = [(name, objects[name]) for name in sorted(objects)]
    print(f"GCS bucket: gs://{bucket_name}")
    print(f"DVC objects: {len(dvc_objects)}")
    for name, size in verified:
        print(f"OK  gs://{bucket_name}/{name}  ({size} bytes)")
    print("VERIFICATION PASSED: DVC data and production model artifacts exist in GCS.")
    return verified


if __name__ == "__main__":
    verify_gcs_artifacts(os.environ.get("GCS_BUCKET", DEFAULT_BUCKET))
