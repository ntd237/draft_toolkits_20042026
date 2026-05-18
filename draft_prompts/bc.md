# Báo Cáo: Xây Dựng CSDL Nghiệp Vụ Tác Chiến Mạng Phục Vụ Huấn Luyện Mô Hình AI

---

## 1. Tóm Tắt Yêu Cầu

Người dùng cần hướng dẫn xây dựng **cơ sở dữ liệu (CSDL) nghiệp vụ tác chiến mạng** để huấn luyện các mô hình AI, tham khảo từ mô hình xây dựng CSDL chatbot — bao gồm: thu thập dữ liệu đa ngành, phần mềm nhập liệu không yêu cầu chuyên môn cao, hệ thống đánh giá/phân loại dữ liệu tự động, và tổ chức CSDL đa phương tiện (ảnh, video, âm thanh, văn bản, đa ngôn ngữ).

---

## 2. Tổng Quan Kiến Trúc CSDL Cho AI Training

Một CSDL phục vụ huấn luyện AI — dù là chatbot hay hệ thống tác chiến mạng — đều chia sẻ cùng một vòng đời dữ liệu:

```
Thu thập → Nhập liệu → Đánh giá/Kiểm định → Tổ chức/Lưu trữ → Phục vụ Training
```

Điểm khác biệt của CSDL tác chiến mạng so với chatbot thông thường nằm ở **tính nhạy cảm của domain**, **yêu cầu phân loại đa tầng** (theo mức độ nguy hiểm, loại tấn công, vector khai thác), và **tính đa phương tiện cao** (log file, pcap, screenshot, video demo exploit).

---

## 3. Thu Thập Dữ Liệu Đa Nguồn

### 3.1 Các Nguồn Dữ Liệu Tham Khảo Từ Chatbot Domain

Khi xây dựng CSDL chatbot, dữ liệu được thu thập từ nhiều ngành theo mô hình **domain-specific corpus collection**:

- **Ngành y tế**: Hội thoại bác sĩ-bệnh nhân, tài liệu y khoa, FAQ bệnh viện
- **Ngành tài chính**: Transcript tư vấn, báo cáo, quy định pháp lý
- **Ngành kỹ thuật**: Tài liệu kỹ thuật, ticket hỗ trợ, forum Stack Overflow

Phương pháp thu thập phổ biến: **web scraping có kiểm soát**, **crowdsourcing** (Amazon Mechanical Turk, Scale AI), **synthetic data generation**, và **human-in-the-loop annotation**.

### 3.2 Áp Dụng Cho CSDL Tác Chiến Mạng

| Nguồn | Loại dữ liệu | Phương pháp thu thập |
|---|---|---|
| CVE/NVD Database | Mô tả lỗ hổng, CVSS score | API crawl tự động |
| Threat Intelligence Feeds | IoC, TTPs, malware hash | STIX/TAXII protocol |
| Honeypot/Sandbox | Log tấn công thực tế, pcap | Automated capture |
| CTF Writeups | Kịch bản tấn công có nhãn | Web scraping + manual |
| MITRE ATT&CK | Chiến thuật, kỹ thuật, thủ tục | API + manual enrichment |
| Red Team Reports | Báo cáo pentest, PoC | Manual input từ chuyên gia |
| Malware Samples | Binary, behavior log | Sandbox analysis (Cuckoo) |

---

## 4. Phần Mềm Nhập Liệu Không Yêu Cầu Chuyên Môn Cao

### 4.1 Nguyên Tắc Thiết Kế (Low-Barrier Data Entry)

Tham khảo từ các nền tảng annotation thành công như **Label Studio**, **Prodigy**, **Doccano** — nguyên tắc cốt lõi là:

- **Progressive disclosure**: Chỉ hiển thị trường cần thiết theo từng bước, không overwhelm người dùng
- **Guided annotation**: Hướng dẫn inline, tooltip giải thích từng trường
- **Template-based input**: Form có sẵn theo loại sự kiện (phishing, DDoS, APT...), người dùng chỉ điền thông tin cụ thể
- **Auto-suggestion**: Gợi ý nhãn dựa trên nội dung đã nhập (dùng model nhỏ để pre-label)

### 4.2 Kiến Trúc Phần Mềm Nhập Liệu Đề Xuất

```
┌─────────────────────────────────────────┐
│           Web-based Annotation UI       │
│  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Template │  │  Upload  │  │  Form  │ │
│  │ Selector │  │  Media   │  │ Wizard │ │
│  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────┘
              ↓ REST API
┌─────────────────────────────────────────┐
│         Validation & Pre-labeling       │
│  ┌──────────────┐  ┌───────────────────┐│
│  │ Format Check │  │  Auto-classifier  ││
│  │ (schema val) │  │  (suggest labels) ││
│  └──────────────┘  └───────────────────┘│
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│           Review Queue (Expert)         │
└─────────────────────────────────────────┘
```

**Công nghệ gợi ý**: Label Studio (open-source, hỗ trợ text/image/audio/video), kết hợp với backend FastAPI + PostgreSQL.

---

## 5. Hệ Thống Đánh Giá và Phân Tách Dữ Liệu

### 5.1 Pipeline Kiểm Định Tự Động (Automated Quality Assessment)

Tham khảo từ mô hình **data-centric AI** của Andrew Ng và các hệ thống như **Great Expectations**, **Cleanlab**:

**Tầng 1 — Schema Validation (tức thì khi nhập)**
- Kiểm tra định dạng bắt buộc (timestamp, IP format, CVE ID pattern)
- Phát hiện trường rỗng hoặc giá trị ngoài range cho phép
- Công cụ: Pydantic (Python), JSON Schema validation

**Tầng 2 — Semantic Consistency Check**
- Kiểm tra mâu thuẫn nội dung: ví dụ nhãn "phishing" nhưng không có URL/email trong nội dung
- Duplicate detection: MinHash LSH cho văn bản, perceptual hash cho ảnh
- Công cụ: Cleanlab (label error detection), custom rule engine

**Tầng 3 — Inter-Annotator Agreement (IAA)**
- Mỗi mẫu được ít nhất 2-3 người gán nhãn độc lập
- Tính Cohen's Kappa hoặc Fleiss' Kappa để đo độ đồng thuận
- Mẫu có Kappa < 0.6 được đưa vào **dispute queue** cho chuyên gia xử lý
- Công cụ: Label Studio có tích hợp IAA metrics

**Tầng 4 — Model-Assisted Review**
- Train một classifier nhỏ trên dữ liệu đã được xác nhận
- Dùng classifier này để flag các mẫu mới có confidence thấp hoặc prediction mâu thuẫn với nhãn người dùng đặt
- Công cụ: Prodigy (active learning loop)

### 5.2 Phân Tách Train/Validation/Test

Không phân tách ngẫu nhiên đơn thuần — cần **stratified split** theo:
- Loại tấn công (đảm bảo mỗi class đủ đại diện)
- Thời gian (temporal split: train trên dữ liệu cũ, test trên dữ liệu mới — tránh data leakage)
- Nguồn gốc (không để dữ liệu từ cùng một chiến dịch tấn công xuất hiện ở cả train và test)

---

## 6. Tổ Chức CSDL Đa Phương Tiện

### 6.1 Kiến Trúc Lưu Trữ Phân Tầng

```
CSDL Tác Chiến Mạng
├── Metadata Store (PostgreSQL / Elasticsearch)
│   ├── event_id, timestamp, source, labels, quality_score
│   ├── media_refs (foreign keys đến object storage)
│   └── annotation_history, annotator_id, review_status
│
├── Object Storage (MinIO / S3-compatible)
│   ├── /images/     → screenshot, network diagram, malware UI
│   ├── /videos/     → screen recording, demo exploit, training video
│   ├── /audio/      → voice command, intercepted communication
│   ├── /pcap/       → network capture files
│   └── /binaries/   → malware samples (encrypted at rest)
│
├── Document Store (Elasticsearch)
│   ├── Threat reports (full-text searchable)
│   ├── CVE descriptions
│   └── TTPs documentation
│
└── Vector Store (Qdrant / Weaviate / Milvus)
    ├── Text embeddings (cho semantic search)
    ├── Image embeddings (cho visual similarity)
    └── Behavior embeddings (cho malware clustering)
```

### 6.2 Schema Dữ Liệu Cốt Lõi

Mỗi bản ghi trong CSDL nên có cấu trúc thống nhất:

```json
{
  "event_id": "uuid-v4",
  "created_at": "ISO8601",
  "data_type": "text|image|video|audio|pcap|binary",
  "content": {
    "raw_ref": "s3://bucket/path/to/file",
    "text_content": "...",
    "language": "vi|en|zh|...",
    "encoding": "utf-8"
  },
  "labels": {
    "attack_type": ["phishing", "apt", "ddos"],
    "mitre_technique": ["T1566.001"],
    "severity": "critical|high|medium|low",
    "confidence": 0.95
  },
  "quality": {
    "iaa_score": 0.82,
    "review_status": "approved|pending|disputed",
    "reviewed_by": ["expert_id_1"]
  },
  "metadata": {
    "source": "honeypot|manual|synthetic",
    "campaign_id": "...",
    "tlp_level": "RED|AMBER|GREEN|WHITE"
  }
}
```

### 6.3 Xử Lý Đa Ngôn Ngữ

- **Chuẩn hóa ngôn ngữ**: Dùng **langdetect** hoặc **fastText** để tự động detect ngôn ngữ khi nhập
- **Lưu trữ song ngữ**: Giữ nguyên bản gốc + bản dịch tiếng Anh (dùng DeepL API hoặc NLLB model của Meta)
- **Embedding đa ngôn ngữ**: Dùng **multilingual-e5** hoặc **LaBSE** để tạo vector representation thống nhất bất kể ngôn ngữ
- **Tokenization riêng biệt**: Mỗi ngôn ngữ cần tokenizer phù hợp (underthesea cho tiếng Việt, jieba cho tiếng Trung)

---

## 7. Quy Trình Tổng Thể Đề Xuất

```
Bước 1: Xác định ontology domain
         → Định nghĩa taxonomy tấn công mạng (dựa trên MITRE ATT&CK)
         → Thiết kế schema dữ liệu chuẩn

Bước 2: Xây dựng pipeline thu thập tự động
         → Crawl CVE, threat feeds, CTF writeups
         → Honeypot deployment để thu log thực tế

Bước 3: Triển khai annotation platform
         → Label Studio + custom plugin cho cybersecurity domain
         → Onboard annotators (không cần chuyên môn sâu)

Bước 4: Thiết lập quality pipeline
         → Automated validation (schema + semantic)
         → IAA measurement + expert review queue

Bước 5: Xây dựng hạ tầng lưu trữ
         → PostgreSQL (metadata) + MinIO (media) + Elasticsearch (text) + Qdrant (vectors)

Bước 6: Versioning & Governance
         → DVC (Data Version Control) để track dataset versions
         → Audit log mọi thay đổi
         → TLP classification cho dữ liệu nhạy cảm
```

---

## 8. Các Lưu Ý Quan Trọng

**Bảo mật dữ liệu**: CSDL tác chiến mạng chứa thông tin cực kỳ nhạy cảm. Cần mã hóa at-rest (AES-256) và in-transit (TLS 1.3), phân quyền truy cập theo role (RBAC), và audit log đầy đủ.

**Tránh data poisoning**: Với dữ liệu nhạy cảm, cần cơ chế phát hiện dữ liệu độc hại được cố tình nhập vào để làm lệch model (adversarial data injection).

**Cân bằng class**: Các loại tấn công hiếm (zero-day, APT) thường thiếu dữ liệu — cần chiến lược **data augmentation** hoặc **synthetic data generation** (dùng LLM để tạo kịch bản tấn công tổng hợp có kiểm soát).

**Temporal drift**: Các chiến thuật tấn công thay đổi theo thời gian — CSDL cần cơ chế **continuous update** và **model retraining trigger** khi phát hiện distribution shift.

---

## 9. Tài Liệu Tham Khảo

- [MITRE ATT&CK Framework](https://attack.mitre.org/) — Taxonomy chuẩn cho TTPs
- [Label Studio Documentation](https://labelstud.io/guide/) — Annotation platform
- [Cleanlab Documentation](https://docs.cleanlab.ai/) — Automated label error detection
- [Great Expectations](https://docs.greatexpectations.io/) — Data validation framework
- [STIX/TAXII Standard](https://oasis-open.github.io/cti-documentation/) — Threat intelligence sharing
- [DVC Documentation](https://dvc.org/doc) — Data version control
- [Multilingual-E5 (Microsoft)](https://huggingface.co/intfloat/multilingual-e5-large) — Multilingual embeddings
- [NIST SP 800-61](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) — Incident handling guide (tham khảo taxonomy)
