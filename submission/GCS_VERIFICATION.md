# GCS Artifact Verification

- Verification date: 2026-08-21
- Bucket: `gs://mlops-wine-k3-2a202601339`
- Method: read-only Google Cloud Storage SDK listing
- Reproduce: `python scripts/verify_gcs_artifacts.py`

```text
GCS bucket: gs://mlops-wine-k3-2a202601339
DVC objects: 5
OK  gs://mlops-wine-k3-2a202601339/dvc/files/md5/58/53e7711c78f02286e65fca6cb6e124  (368068 bytes)
OK  gs://mlops-wine-k3-2a202601339/dvc/files/md5/98/97f43b603ae73814d500dea1ddbf6f  (552046 bytes)
OK  gs://mlops-wine-k3-2a202601339/dvc/files/md5/b1/1de6b7adaa93a44278fd7e168b2288  (30769 bytes)
OK  gs://mlops-wine-k3-2a202601339/dvc/files/md5/c4/3afab731fd6431a94f888fdc687876  (184090 bytes)
OK  gs://mlops-wine-k3-2a202601339/dvc/files/md5/fd/073d6651b2ff224c0da1eb1c049a32  (184134 bytes)
OK  gs://mlops-wine-k3-2a202601339/models/latest/metrics.json  (171 bytes)
OK  gs://mlops-wine-k3-2a202601339/models/latest/model.pkl  (41843089 bytes)
VERIFICATION PASSED: DVC data and production model artifacts exist in GCS.
```
