# Unified Dataset Schema Catalog

**Author:** Vedika  
**Project:** Hackaging AI - MenoBalance AI Platform  
**Total Records:** 26,946
**Total Fields:** 71

## Data Sources Distribution

- **NHANES:** 15,560 records
- **Wearables:** 6,917 records
- **SWAN:** 2,469 records
- **SYNTHEA:** 1,000 records
- **UKBB:** 1,000 records

## Field Information

### participant_id
- **Type:** string
- **Missing:** 2,469 (9.2%)
- **Unique Values:** 24,477
- **Sample Values:** ['SYN0000001', 'SYN0000002', 'SYN0000003', 'SYN0000004', 'SYN0000005']

### age
- **Type:** float64
- **Missing:** 9,386 (34.8%)
- **Unique Values:** 81
- **Range:** 0.00 to 80.00
- **Mean:** 35.57 (SD: 24.60)
- **Sample Values:** [48.0, 43.0, 50.0, 57.0, 43.0]

### bmi
- **Type:** float64
- **Missing:** 9,386 (34.8%)
- **Unique Values:** 2,429
- **Range:** 8.59 to 92.30
- **Mean:** 26.41 (SD: 7.51)
- **Sample Values:** [25.78949042175864, 25.45503073392111, 25.926690736780245, 25.289380869276727, 19.90714890434641]

### race_ethnicity
- **Type:** object
- **Missing:** 6,917 (25.7%)
- **Unique Values:** 14
- **Sample Values:** ['Asian', 'White', 'White', 'White', 'White']

### smoking_status
- **Type:** object
- **Missing:** 9,386 (34.8%)
- **Unique Values:** 8
- **Sample Values:** ['Former', 'Former', 'Former', 'Never', 'Never']

### education
- **Type:** float64
- **Missing:** 10,386 (38.5%)
- **Unique Values:** 7
- **Range:** 1.00 to 9.00
- **Mean:** 3.70 (SD: 0.98)
- **Sample Values:** [3.0, 2.0, 2.0, 2.0, 2.0]

### physical_activity
- **Type:** float64
- **Missing:** 10,424 (38.7%)
- **Unique Values:** 966
- **Range:** 0.03 to 127.58
- **Mean:** 2.89 (SD: 6.39)
- **Sample Values:** [7.019328944623792, 7.895995548009331, 64.84157462594646, 4.034854152405372, 7.457400514618467]

### alcohol_frequency
- **Type:** float64
- **Missing:** 25,946 (96.3%)
- **Unique Values:** 5
- **Range:** 0.00 to 4.00
- **Mean:** 2.08 (SD: 1.15)
- **Sample Values:** [1.0, 4.0, 1.0, 3.0, 4.0]

### fsh
- **Type:** float64
- **Missing:** 9,451 (35.1%)
- **Unique Values:** 5,233
- **Range:** 0.21 to 187.70
- **Mean:** 14.04 (SD: 21.54)
- **Sample Values:** [17.182246799361668, 4.17235283136746, 9.818046742555422, 14.59478690301057, 13.603140834522518]

### estradiol
- **Type:** float64
- **Missing:** 9,484 (35.2%)
- **Unique Values:** 3,641
- **Range:** 1.20 to 15300.00
- **Mean:** 48.64 (SD: 392.29)
- **Sample Values:** [50.29131494345561, 60.70625111508787, 33.2255995707926, 32.85357564030438, 27.26840546682713]

### amh
- **Type:** float64
- **Missing:** 10,422 (38.7%)
- **Unique Values:** 1,404
- **Range:** 0.02 to 30.69
- **Mean:** 0.92 (SD: 1.67)
- **Sample Values:** [8.0, 8.0, 4.700666447180324, 2.670993706350727, 7.83482586970945]

### inhibin_b
- **Type:** float64
- **Missing:** 25,973 (96.4%)
- **Unique Values:** 973
- **Range:** 10.00 to 120.00
- **Mean:** 35.78 (SD: 14.75)
- **Sample Values:** [64.73192542124323, 30.642933555837686, 38.99346762316607, 23.464408919384358, 28.71527329555808]

### testosterone
- **Type:** float64
- **Missing:** 25,991 (96.5%)
- **Unique Values:** 955
- **Range:** 1.09 to 39.99
- **Mean:** 8.66 (SD: 4.85)
- **Sample Values:** [7.791952417361263, 5.371437983412399, 7.178437161305447, 12.98628776605965, 7.822352449508696]

### tsh
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### lh
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### progesterone
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### height
- **Type:** float64
- **Missing:** 10,386 (38.5%)
- **Unique Values:** 2,110
- **Range:** 0.78 to 196.38
- **Mean:** 11.45 (SD: 39.04)
- **Sample Values:** [161.90790922950137, 157.47843594409417, 168.1917451041918, 178.40450446023144, 146.24827530354256]

### weight
- **Type:** float64
- **Missing:** 10,388 (38.6%)
- **Unique Values:** 2,512
- **Range:** 3.20 to 254.30
- **Mean:** 65.93 (SD: 30.99)
- **Sample Values:** [58.45005900703814, 50.55825003625158, 63.15818758788718, 72.72139930170957, 78.92544198753347]

### systolic_bp
- **Type:** float64
- **Missing:** 25,946 (96.3%)
- **Unique Values:** 1,000
- **Range:** 72.35 to 167.28
- **Mean:** 119.09 (SD: 14.78)
- **Sample Values:** [124.74537482304216, 106.72126970813666, 122.71594114156623, 139.54917055974096, 128.79248700589176]

### diastolic_bp
- **Type:** float64
- **Missing:** 25,946 (96.3%)
- **Unique Values:** 1,000
- **Range:** 51.67 to 111.13
- **Mean:** 79.71 (SD: 9.83)
- **Sample Values:** [87.30958976376216, 73.49340172631616, 59.09697101146843, 78.29741753204094, 77.34395439713894]

### heart_rate
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### waist_circumference
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### hip_circumference
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### hot_flashes
- **Type:** boolean
- **Missing:** 25,946 (96.3%)
- **Unique Values:** 2
- **Sample Values:** [True, True, True, False, False]

### mood_swings
- **Type:** boolean
- **Missing:** 25,946 (96.3%)
- **Unique Values:** 2
- **Sample Values:** [True, False, False, False, True]

### sleep_disturbance
- **Type:** object
- **Missing:** 10,386 (38.5%)
- **Unique Values:** 26
- **Sample Values:** [False, False, True, False, False]

### depression_score
- **Type:** float64
- **Missing:** 11,386 (42.3%)
- **Unique Values:** 6
- **Range:** 0.00 to 9.00
- **Mean:** 0.21 (SD: 0.62)
- **Sample Values:** [5.397605346934028e-79, 5.397605346934028e-79, 5.397605346934028e-79, 5.397605346934028e-79, 5.397605346934028e-79]

### anxiety_score
- **Type:** float64
- **Missing:** 11,386 (42.3%)
- **Unique Values:** 6
- **Range:** 0.00 to 9.00
- **Mean:** 0.20 (SD: 0.58)
- **Sample Values:** [5.397605346934028e-79, 5.397605346934028e-79, 5.397605346934028e-79, 5.397605346934028e-79, 5.397605346934028e-79]

### stress_score
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### sleep_quality
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### fatigue_score
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### steps_day
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### sedentary_minutes
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### light_minutes
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### moderate_minutes
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### vigorous_minutes
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### avg_heart_rate
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### hrv_proxy
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### activity_window_fraction
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### sleep_duration
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### sleep_efficiency
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### menopause_stage
- **Type:** object
- **Missing:** 25,556 (94.8%)
- **Unique Values:** 5
- **Sample Values:** ['Late', 'Early', 'Early', 'Post', 'Early']

### menopause_stage_encoded
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### time_to_menopause_months
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### menopause_event
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### fmp_date
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### last_followup_date
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### age_at_menopause
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### menopause_age_group
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### hot_flash_severity
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### mood_severity
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### sleep_severity
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### total_symptom_burden
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### symptom_frequency
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### symptom_duration
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### visit_number
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### months_from_baseline
- **Type:** float64
- **Missing:** 24,477 (90.8%)
- **Unique Values:** 1
- **Range:** 0.00 to 0.00
- **Mean:** 0.00 (SD: 0.00)
- **Sample Values:** [0.0, 0.0, 0.0, 0.0, 0.0]

### amh_decline_rate
- **Type:** float64
- **Missing:** 25,946 (96.3%)
- **Unique Values:** 811
- **Range:** 0.01 to 0.25
- **Mean:** 0.09 (SD: 0.08)
- **Sample Values:** [0.0522740473050631, 0.01, 0.042896999729938, 0.0117655904878072, 0.165148571007548]

### fsh_trajectory
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### hormone_change_velocity
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### symptom_progression
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### cvd_risk
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### bone_density_risk
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### cognitive_risk
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### diabetes_risk
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### osteoporosis_risk
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### data_source
- **Type:** object
- **Missing:** 0 (0.0%)
- **Unique Values:** 5
- **Sample Values:** ['SYNTHEA', 'SYNTHEA', 'SYNTHEA', 'SYNTHEA', 'SYNTHEA']

### sample_date
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### collection_method
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### study_phase
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

### data_quality_score
- **Type:** float64
- **Missing:** 26,946 (100.0%)
- **Unique Values:** 0
- **Range:** nan to nan
- **Mean:** nan (SD: nan)
- **Sample Values:** []

