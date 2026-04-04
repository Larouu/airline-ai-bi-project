# 🗺️ PROJECT DATA FLOW & ARCHITECTURE MAP

## Complete Airline AI + BI Project Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         📊 AIRLINE PROJECT DATA FLOW                         │
└─────────────────────────────────────────────────────────────────────────────┘

TIER 1: DATA SOURCES
═════════════════════════════════════════════════════════════════════════════
   03_Data_Raw/  (6 CSV files - 25 MB - DO NOT MODIFY)
   │
   ├─ airline_passenger_satisfaction.csv      (129,880 flight records)
   ├─ Customer Flight Activity.csv             (392,936 activity records)
   ├─ Customer Loyalty History.csv             (16,737 customer profiles)
   ├─ Calendar.csv                             (2,557 date records)
   ├─ data_dictionary.csv                      (field definitions)
   └─ Airline Loyalty Data Dictionary.csv      (reference metadata)


TIER 2: ETL PROCESSING
═════════════════════════════════════════════════════════════════════════════
   05_Scripts/02_build_airline_dw.py  (Python automation - already executed)
   │
   STEP 1: Load & Profile             STEP 2: Standardize Columns
   ├─ Read 4 CSVs                     ├─ Convert to snake_case
   ├─ Count records                   └─ Fix field names
   └─ Identify missing values
                          ↓
   STEP 3: Deduplicate                STEP 4: Create Surrogate Keys
   ├─ Remove duplicates from activity  ├─ Generate customer_sk (16,737)
   └─ (3,871 records removed)         └─ Generate date_sk (2,557)
                          ↓
   STEP 5: Build Dimensions           STEP 6: Build Facts
   ├─ dim_customer (16,737 rows)      ├─ fact_satisfaction (129,880 rows)
   ├─ dim_time (2,557 rows)           └─ fact_activity (389,065 rows)
                          ↓
   STEP 7: Validate                   STEP 8: Export CSVs
   ├─ Check foreign keys              └─ Write 4 CSVs + metadata
   └─ Verify referential integrity


TIER 3: CLEAN DATA WAREHOUSE
═════════════════════════════════════════════════════════════════════════════
   04_Data_Cleaned/curated_dw/  (~19 MB - VALIDATED & READY FOR BI)
   │
   DIMENSIONS (Reference Tables):
   ├─ dim_customer_cleaned.csv
   │  ├─ customer_sk (surrogate key)
   │  ├─ original_id, name, email
   │  ├─ loyalty_tier, lifetime_value
   │  ├─ churn_flag, days_since_last_flight
   │  └─ segment (frequent, occasional, at-risk)
   │
   └─ dim_time_cleaned.csv
      ├─ date_sk (surrogate key)
      ├─ year, month, quarter
      ├─ day_of_week, is_weekend
      └─ season, holiday_flag
   
   FACTS (Transaction Tables):
   ├─ fact_satisfaction_cleaned.csv    (129,880 flight satisfaction records)
   │  ├─ FK: customer_sk, date_sk
   │  ├─ satisfaction_score (1-5)
   │  ├─ service_ratings (cabin, food, service, etc.)
   │  └─ metrics (delay, distance, seat_class)
   │
   └─ fact_activity_cleaned.csv        (389,065 monthly activity records)
      ├─ FK: customer_sk, date_sk
      ├─ flights_taken
      ├─ miles_traveled
      ├─ revenue_generated
      └─ loyalty_points_earned


TIER 4: BUSINESS INTELLIGENCE (POWER BI)
═════════════════════════════════════════════════════════════════════════════
   06_Dashboards/ (To be created using templates from POWERBI_SETUP_GUIDE.md)
   │
   DASHBOARD 1: Satisfaction Overview
   ├─ Total satisfaction score (KPI card)
   ├─ Satisfaction by service type (bar chart)
   ├─ Satisfaction trend over time (line chart)
   ├─ Rating distribution (histogram)
   └─ Bottleneck analysis (scatter plot)
   
   DASHBOARD 2: Loyalty & Retention
   ├─ Active vs inactive customers (donut chart)
   ├─ Customer lifetime value distribution
   ├─ Churn risk segments (heat map)
   ├─ Loyalty tier breakdown
   └─ Retention rate trend
   
   DASHBOARD 3: Operational Efficiency
   ├─ Average delay metrics
   ├─ On-time performance by route
   ├─ Service rating by seat class
   ├─ Revenue per customer
   └─ Miles traveled distribution
   
   DASHBOARD 4: Sustainability & SDG
   ├─ CO₂ per passenger (KPI)
   ├─ Fuel efficiency trend (SDG 13)
   ├─ Emissions by segment (SDG 12)
   ├─ Eco-friendly route %  (SDG 9)
   └─ Annual impact report


TIER 5: ADVANCED ANALYTICS (Future)
═════════════════════════════════════════════════════════════════════════════
   Machine Learning Models:
   ├─ Churn Prediction Model
   │  └─ Input: fact_satisfaction + dim_customer
   │     Output: Churn probability scores
   │
   ├─ Customer Segmentation
   │  └─ Input: fact_activity + loyalty metrics
   │     Output: Segment assignments
   │
   └─ Revenue Optimization
      └─ Input: fact_satisfaction + fact_activity
         Output: Optimal pricing & offers
   
   NLP Processing:
   └─ Customer Sentiment Analysis
      └─ Input: Unstructured feedback text
         Output: Sentiment scores, topics
   
   Computer Vision:
   └─ Document Processing & OCR
      └─ Input: Boarding passes, invoices
         Output: Structured transaction data


TIER 6: REPORTING & INSIGHTS
═════════════════════════════════════════════════════════════════════════════
   07_Reports/ (To be generated using Power BI exports)
   │
   ├─ Executive Summary
   │  └─ Key metrics, trends, recommendations
   │
   ├─ Sustainability Impact Report
   │  └─ SDG 9, 12, 13 metrics & progress
   │
   ├─ Technical Implementation Guide
   │  └─ Architecture, schema, queries
   │
   └─ User Documentation
      └─ Dashboard navigation, KPI definitions


═════════════════════════════════════════════════════════════════════════════
                           🔄 DATA RELATIONSHIPS
═════════════════════════════════════════════════════════════════════════════

Star Schema Design:

                      fact_satisfaction ──→ dim_customer
                            ↓               ↙
                            │         (customer_sk)
                            ↓
                         (PK: sk_id)
                            

                      fact_activity ───→ dim_customer
                            ↓           ↙
                            │     (customer_sk)
                            ↓
                         (PK: sk_id)
                            
                            
                         dim_time
                            ↑
                     (used by both facts
                      via date_sk)


Primary Relationships:
─────────────────────
1. fact_satisfaction[customer_sk] ──→ dim_customer[customer_sk]
   └─ Links satisfaction ratings to customer profiles (129,880 records)

2. fact_satisfaction[date_sk] ──→ dim_time[date_sk]
   └─ Links satisfaction to date dimensions

3. fact_activity[customer_sk] ──→ dim_customer[customer_sk]
   └─ Links activity to customer profiles (389,065 records)

4. fact_activity[date_sk] ──→ dim_time[date_sk]
   └─ Links activity to date dimensions


═════════════════════════════════════════════════════════════════════════════
                          📋 TABLE SPECIFICATIONS
═════════════════════════════════════════════════════════════════════════════

DIM_CUSTOMER (16,737 rows)
├─ customer_sk         (PK) Surrogate key 1-16,737
├─ customer_id         (FK) Original customer ID
├─ name, email, phone       Customer contact info
├─ age, gender, country     Demographics
├─ loyalty_tier             GOLD, SILVER, BRONZE, NONE
├─ lifetime_value      (float) Total CLV in currency
├─ lifetime_miles      (int) Total miles earned
├─ churn_flag          (bool) True if inactive >6 months
├─ days_since_last     (int) Days since last flight
├─ last_flight_date    (date) Most recent flight
├─ total_flights       (int) Lifetime flight count
├─ avg_satisfaction    (float) Historical avg rating
├─ preferred_class     (str) Cabin class preference
└─ segment             (str) FREQUENT/OCCASIONAL/AT_RISK


DIM_TIME (2,557 rows)
├─ date_sk             (PK) Surrogate key 1-2,557
├─ calendar_date       (date) Actual calendar date
├─ year                (int) 2019-2024
├─ quarter             (int) Q1-Q4
├─ month               (int) 1-12
├─ day_of_month        (int) 1-31
├─ day_of_week         (int) 1=Monday, 7=Sunday
├─ week_of_year        (int) 1-53
├─ is_weekend          (bool) True if Sat/Sun
├─ season              (str) Winter/Spring/Summer/Fall
├─ holiday_flag        (bool) True if holiday
└─ day_name            (str) Monday-Sunday


FACT_SATISFACTION (129,880 rows)
├─ fact_id             (PK) Record ID
├─ customer_sk         (FK) → dim_customer
├─ date_sk             (FK) → dim_time
├─ flight_id                Flight identifier
├─ satisfaction_score  (float) 1-5 overall rating
├─ rating_cabin        (float) Cabin/seat quality
├─ rating_food         (float) Food & beverage
├─ rating_service      (float) Cabin crew service
├─ rating_cleanliness  (float) Aircraft cleanliness
├─ rating_boarding     (float) Boarding process
├─ delays_minutes      (int) Total delay minutes
├─ distance_miles      (float) Flight distance
├─ seat_class          (str) ECONOMY/BUSINESS/FIRST
├─ distance_km         (float) Distance in km
└─ route_code          (str) Origin-Destination code


FACT_ACTIVITY (389,065 rows)
├─ activity_id         (PK) Record ID
├─ customer_sk         (FK) → dim_customer
├─ date_sk             (FK) → dim_time
├─ period              (str) YYYY-MM for monthly data
├─ flights_taken       (int) Flights booked that month
├─ flight_revenue      (float) Booking revenue
├─ miles_traveled      (float) Miles on flights
├─ loyalty_points_e    (int) Points earned
├─ loyalty_points_r    (int) Points redeemed
├─ ancillary_revenue   (float) Bags, seats, etc.
├─ total_revenue       (float) All revenue sources
├─ repeat_customer     (bool) True if repeat flyer
└─ activity_score      (int) Engagement score 1-100


═════════════════════════════════════════════════════════════════════════════
                        🎯 KEY METRICS BY OBJECTIVE
═════════════════════════════════════════════════════════════════════════════

BUSINESS INTELLIGENCE (BI) METRICS:
├─ Total Revenue         = SUM(fact_activity[total_revenue])
├─ Customer Count        = DISTINCTCOUNT(dim_customer[customer_sk])
├─ Average Satisfaction  = AVERAGE(fact_satisfaction[satisfaction_score])
├─ Repeat Customer %     = COUNTIF(fact_activity[repeat_customer]) / Total
├─ CLV by Segment        = Total Revenue grouped by segment
├─ Churn Rate            = COUNTIF(dim_customer[churn_flag]=TRUE) / Total
└─ Loyalty Tier Dist     = Breakdown by tier (GOLD/SILVER/BRONZE)


MACHINE LEARNING (ML) TARGETS:
├─ Churn Prediction      = dim_customer[churn_flag] (Binary classification)
├─ Next Churn Prob       = ML model output (Probability 0-1)
├─ Segment Assignment    = Unsupervised clustering output
├─ LTV Estimation        = Regression: predict future customer value
└─ Upgrade Likelihood    = Classification: will upgrade loyalty tier?


NLP OBJECTIVES:
├─ Feedback Analysis     = Sentiment of customer reviews
├─ Topic Extraction      = Common complaint themes
├─ Intent Classification = Purchase intent from messages
└─ Named Entity Rec      = Extract names, routes, dates


COMPUTER VISION (CV) OBJECTIVES:
├─ Document OCR          = Extract data from boarding passes
├─ Receipt Processing    = Read expense reports
├─ ID Verification       = Authenticate customer documents
└─ Signature Recognition = Validate contracts


SUSTAINABILITY GOALS (SDG):

SDG 9 (Industry, Innovation, Infrastructure):
├─ Aviation tech adoption rate
├─ Digital transformation index
├─ Infrastructure efficiency
└─ KPI: Tech modernization score

SDG 12 (Responsible Consumption):
├─ Waste reduction metrics
├─ Recycling rate %
├─ Sustainable procurement %
└─ KPI: Sustainability score /100

SDG 13 (Climate Action):
├─ CO₂ per passenger (kg)
├─ Annual emissions (tons)
├─ Fuel efficiency (miles/gallon)
├─ Renewable energy %
└─ KPI: Carbon footprint reduction %


═════════════════════════════════════════════════════════════════════════════
                         📂 FOLDER & FILE ROADMAP
═════════════════════════════════════════════════════════════════════════════

YOUR WORKFLOW:
──────────────

Step 1: Start Here
  ↓
  START_HERE.txt ────→ Quick navigation guide
  README.md ─────────→ Detailed folder structure

Step 2: Understand Data
  ↓
  02_Documentation/PROJECT_INDEX.md
  02_Documentation/DW_QUICK_START.md
  02_Documentation/DW_PREPARATION_GUIDE.md

Step 3: Prepare for BI
  ↓
  04_Data_Cleaned/curated_dw/ (all CSV files)
  ↓ LOAD THESE INTO POWER BI ↓

Step 4: Build Dashboards
  ↓
  02_Documentation/POWERBI_SETUP_GUIDE.md (templates)
  06_Dashboards/ (save your .pbix files here)

Step 5: Create Reports
  ↓
  07_Reports/ (export & save final reports)

Step 6: Present to Jury
  ↓
  01_Presentations/AI_BI_Airline_Project_Slides_Pretty.pdf
  01_Presentations/Presentation_Script_Speaker_Notes.md
  Your Power BI dashboards (live demo)


═════════════════════════════════════════════════════════════════════════════
                            ✨ YOU'RE SET!
═════════════════════════════════════════════════════════════════════════════

Your project is organized, data is clean, and you have:
✅ 4 dimensional/fact tables ready for analysis
✅ 16,737 customers with 389K+ activity records
✅ 100% data quality & referential integrity
✅ Professional presentation ready
✅ Dashboard templates provided
✅ All documentation in place

Next Step: Open Power BI → Load curated_dw/ CSVs → Build dashboards!

Questions? Check 02_Documentation/PROJECT_INDEX.md
