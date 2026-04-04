# 🎯 AIRLINE AI + BI PROJECT - ORGANIZED STRUCTURE

## 📁 Project Organization Overview

```
Ailines project/
├── 01_Presentations/           ← 🎬 All presentation files
│   ├── AI_BI_Airline_Project_Slides_Pretty.pdf           (Primary - use this!)
│   ├── Presentation_Script_Speaker_Notes.md             (Jury script: 7 & 12 min)
│   └── [Other presentation materials]
│
├── 02_Documentation/            ← 📚 Complete project guides
│   ├── PROJECT_INDEX.md                                  (⭐ START HERE!)
│   ├── DW_QUICK_START.md                                (5-min overview)
│   ├── DW_PREPARATION_GUIDE.md                          (Schema + joins)
│   └── POWERBI_SETUP_GUIDE.md                           (BI dashboards)
│
├── 03_Data_Raw/                ← 📊 Original unprocessed data
│   ├── airline_passenger_satisfaction.csv               (129,880 records)
│   ├── Customer Flight Activity.csv                     (392,936 records)
│   ├── Customer Loyalty History.csv                     (16,737 records)
│   ├── Calendar.csv                                     (2,557 dates)
│   ├── data_dictionary.csv                              (Field definitions)
│   └── Airline Loyalty Data Dictionary.csv              (Reference)
│
├── 04_Data_Cleaned/            ← ✅ Cleaned DW-ready tables
│   └── curated_dw/
│       ├── dim_customer_cleaned.csv                     (16,737 rows)
│       ├── dim_time_cleaned.csv                         (2,557 rows)
│       ├── fact_satisfaction_cleaned.csv                (129,880 rows)
│       ├── fact_activity_cleaned.csv                    (389,065 rows)
│       ├── dw_schema_metadata.json                      (Schema definition)
│       ├── dw_sql_templates.json                        (SQL queries)
│       └── data_cleaning_audit.txt                      (Cleaning log)
│
├── 05_Scripts/                 ← 🔧 Automation & processing
│   ├── 02_build_airline_dw.py                           (Main DW builder)
│   ├── generate_slides_pdf.py                           (Slide generator)
│   └── generate_pretty_slides_pdf.py                    (Pretty PDF generator)
│
├── 06_Dashboards/              ← 📈 Power BI / Tableau templates
│   ├── [Dashboard 1: Satisfaction Overview].pbix        (To be created)
│   ├── [Dashboard 2: Loyalty & Retention].pbix          (To be created)
│   ├── [Dashboard 3: Operations].pbix                   (To be created)
│   └── [Dashboard 4: Sustainability].pbix               (To be created)
│
└── 07_Reports/                 ← 📋 Generated outputs & reports
    ├── [Executive Summary Report].pdf                   (To be created)
    ├── [Sustainability Impact Report].pdf               (To be created)
    └── [Technical Appendix].pdf                         (To be created)
```

---

## 🚀 QUICK START GUIDE

### **Step 1: Understand the Project (5 minutes)**
```
READ: 02_Documentation/PROJECT_INDEX.md
      └─ Master index of everything
```

### **Step 2: Review What Was Created (5 minutes)**
```
READ: 02_Documentation/DW_QUICK_START.md
      └─ Summary of cleaned data warehouse
```

### **Step 3: Learn the Data Structure (15 minutes)**
```
READ: 02_Documentation/DW_PREPARATION_GUIDE.md
      └─ Table relationships, joins, KPI formulas
```

### **Step 4: Build Power BI Dashboards (30-60 minutes)**
```
READ: 02_Documentation/POWERBI_SETUP_GUIDE.md
USE:  04_Data_Cleaned/curated_dw/*.csv           (Load these files)
DO:   Build dashboards following the guide
```

### **Step 5: Present to Jury (11-12 minutes)**
```
USE:  01_Presentations/AI_BI_Airline_Project_Slides_Pretty.pdf
READ: 01_Presentations/Presentation_Script_Speaker_Notes.md
DEMO: Your Power BI dashboards
```

---

## 📂 FOLDER DETAILS & CONTENTS

### **01_Presentations/** 🎬
Your complete presentation package for jury defense:

| File | Purpose | Use When |
|------|---------|----------|
| `AI_BI_Airline_Project_Slides_Pretty.pdf` | Professional slides (16 pages) | Presenting to jury |
| `Presentation_Script_Speaker_Notes.md` | Full scripts + timing | Preparing your speech |
| `AI_BI_Airline_Project_Slides.md` | Source outline | Reference/editing |
| `AI_BI_Airline_Project_Presentation.md` | Detailed content | Deep reference |

👉 **Use Pretty PDF** - it's the most professional!

---

### **02_Documentation/** 📚
Complete reference guides for understanding and building your project:

| File | Purpose | Read Time |
|------|---------|-----------|
| `PROJECT_INDEX.md` | Master reference + roadmap | 10 min |
| `DW_QUICK_START.md` | What was created + quick facts | 5 min |
| `DW_PREPARATION_GUIDE.md` | DW architecture + joins + KPIs | 20 min |
| `POWERBI_SETUP_GUIDE.md` | Load data + dashboard templates | 30 min |

👉 **Read in order**: INDEX → QUICK_START → DW_GUIDE → POWERBI_GUIDE

---

### **03_Data_Raw/** 📊
Original unprocessed airline datasets (read-only reference):

| File | Records | Size | Description |
|------|---------|------|-------------|
| `airline_passenger_satisfaction.csv` | 129,880 | 12.6 MB | Service ratings per flight |
| `Customer Flight Activity.csv` | 392,936 | 10.8 MB | Monthly customer activity |
| `Customer Loyalty History.csv` | 16,737 | 1.7 MB | Customer profile & CLV |
| `Calendar.csv` | 2,557 | 112 KB | Time reference table |
| `data_dictionary.csv` | - | - | Field descriptions |

👉 **Don't modify these** - they're your source of truth!

---

### **04_Data_Cleaned/** ✅
Clean, DW-ready tables (ready for Power BI & analysis):

**Directory**: `04_Data_Cleaned/curated_dw/`

| File | Type | Rows | Purpose |
|------|------|------|---------|
| `dim_customer_cleaned.csv` | **Dimension** | 16,737 | Customer profile + loyalty tier |
| `dim_time_cleaned.csv` | **Dimension** | 2,557 | Time reference for trends |
| `fact_satisfaction_cleaned.csv` | **Fact** | 129,880 | Service ratings & metrics |
| `fact_activity_cleaned.csv` | **Fact** | 389,065 | Monthly activity + FK to customers |
| `dw_schema_metadata.json` | Metadata | - | Technical schema definition |
| `dw_sql_templates.json` | Reference | - | Pre-written SQL queries |
| `data_cleaning_audit.txt` | Log | - | Data processing audit trail |

👉 **Use these for Power BI** - they're cleaned & validated!

---

### **05_Scripts/** 🔧
Python automation scripts for data processing:

| Script | Purpose | When to Run |
|--------|---------|------------|
| `02_build_airline_dw.py` | Main DW builder (cleans + transforms) | After updating raw data |
| `generate_slides_pdf.py` | Creates basic PDF from markdown | For simple slide PDFs |
| `generate_pretty_slides_pdf.py` | Creates styled PDF presentation | For professional presentations |

👉 **Already run** - but re-run if you update raw data!

```bash
# To refresh cleaned data after updating raw CSVs:
python 05_Scripts/02_build_airline_dw.py
```

---

### **06_Dashboards/** 📈
Power BI & Tableau dashboard templates (to be built by you):

**Planned Dashboards**:
1. **Dashboard 1: Satisfaction Overview**
   - Satisfaction by segment
   - Service bottlenecks
   - Trends over time

2. **Dashboard 2: Loyalty & Retention**
   - Active vs cancelled customers
   - CLV analysis
   - Churn prediction

3. **Dashboard 3: Operational Efficiency**
   - On-time performance
   - Average delays
   - Service rating heatmap

4. **Dashboard 4: Sustainability & SDG**
   - CO₂ per passenger
   - Fuel efficiency
   - Emission trends

👉 **Build using POWERBI_SETUP_GUIDE.md**

---

### **07_Reports/** 📋
Final reports & outputs (to be generated by you):

**Example Reports to Create**:
- Executive Summary Report (1-2 pages)
- Sustainability Impact Report (SDG metrics)
- Technical Implementation Appendix
- Dashboard User Guide

👉 **Export from Power BI or create as PDF**

---

## 🎯 KEY FILE LOCATIONS FOR YOUR WORKFLOW

### **For Presentations**:
```
01_Presentations/AI_BI_Airline_Project_Slides_Pretty.pdf
01_Presentations/Presentation_Script_Speaker_Notes.md
```

### **For Data Loading**:
```
04_Data_Cleaned/curated_dw/
  ├─ dim_customer_cleaned.csv
  ├─ dim_time_cleaned.csv
  ├─ fact_satisfaction_cleaned.csv
  └─ fact_activity_cleaned.csv
```

### **For Reference Guides**:
```
02_Documentation/PROJECT_INDEX.md                    ← Start here
02_Documentation/DW_PREPARATION_GUIDE.md             ← Joins & architecture
02_Documentation/POWERBI_SETUP_GUIDE.md              ← Dashboard building
```

### **For Data Processing**:
```
05_Scripts/02_build_airline_dw.py                    ← Main automation
```

---

## 📋 CHECKLIST: NEXT STEPS

- [ ] Read `02_Documentation/PROJECT_INDEX.md`
- [ ] Read `02_Documentation/DW_QUICK_START.md`
- [ ] Open Power BI Desktop
- [ ] Load 4 CSV files from `04_Data_Cleaned/curated_dw/`
- [ ] Create relationship: `fact_activity[customer_sk]` → `dim_customer[customer_sk]`
- [ ] Follow dashboard templates in `02_Documentation/POWERBI_SETUP_GUIDE.md`
- [ ] Build 4 dashboards (Satisfaction, Loyalty, Operations, Sustainability)
- [ ] Review `01_Presentations/Presentation_Script_Speaker_Notes.md`
- [ ] Practice 7 or 12-minute presentation
- [ ] Prepare live Power BI demo for jury
- [ ] Generate final reports in `07_Reports/`

---

## 🔄 UPDATING YOUR PROJECT

### **If you modify raw data**:
1. Update files in `03_Data_Raw/`
2. Run: `python 05_Scripts/02_build_airline_dw.py`
3. Cleaned tables auto-regenerate in `04_Data_Cleaned/curated_dw/`
4. Refresh Power BI data sources

### **If you update presentations**:
1. Edit markdown in `01_Presentations/`
2. Run PDF generator script (or export from PowerPoint)
3. Update version in dated filename

### **If you add new dashboards**:
1. Save `.pbix` files in `06_Dashboards/`
2. Document in `06_Dashboards/README.md`
3. Reference in reports

---

## 📊 PROJECT STATISTICS

| Metric | Value |
|--------|-------|
| **Total Project Size** | ~55 MB |
| **Presentations** | 4 files |
| **Documentation** | 4 guides |
| **Raw Data Files** | 6 CSV files |
| **Cleaned Tables** | 4 CSV files |
| **Scripts** | 3 Python files |
| **Unique Customers** | 16,737 |
| **Total Records** | 530,552 |
| **Data Quality** | 100% referential integrity ✓ |

---

## ✨ ORGANIZED, PROFESSIONAL, READY TO PRESENT!

Your airline AI + BI project is now organized with:
- ✅ Clear folder structure
- ✅ Professional presentations
- ✅ Complete documentation
- ✅ Cleaned data (DW-ready)
- ✅ Reusable scripts
- ✅ Dashboard templates
- ✅ Report framework

**Next Action**: Open `02_Documentation/PROJECT_INDEX.md` and start building! 🚀
