"""
Centralized Multilingual Localization Service for FALCON-Q
Supports Marathi (mr), Hindi (hi), and English (en).
IBM Qiskit Fall Fest 2026 · Problem Statement VNQFF-04 · Team TISSOT.
"""

from typing import Dict, Any, Optional

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # Navigation & Brand
        "app_title": "FALCON-AI | Crop Health Decision Support Platform",
        "service_subtitle": "IBM Qiskit Fall Fest 2026 · Problem Statement VNQFF-04 · Team TISSOT",
        "nav_farmer_portal": "Farmer Portal",
        "nav_expert_desk": "Expert Review Desk",
        "nav_officer_dashboard": "Agriculture Officer Dashboard",
        "nav_login": "Login / Register",
        "nav_logout": "Logout",
        "language_select": "Language",

        # Hero & Upload
        "hero_eyebrow": "EARLY DETECTION & INTEGRATED CROP HEALTH MANAGEMENT",
        "hero_title": "Protect your crops with AI diagnosis and expert guidance",
        "hero_desc": "Upload a field photograph of your affected crop. Get instant AI detection, micro-climate risk assessment, and verified agricultural officer advisories.",
        "start_assessment": "Start Crop Health Diagnosis",
        "upload_subtext": "Capture a photo with your mobile camera or choose a leaf picture from device.",
        "btn_open_camera": "Open Camera",
        "btn_upload_pc": "Upload Image",
        "drop_zone_text": "Drop crop photo here or browse files",
        "drop_zone_sub": "JPG, JPEG, PNG, or WEBP (up to 15 MB)",
        "step1_select_crop": "1. Select Crop",
        "step2_select_location": "2. Farm & Location",
        "step3_select_stage": "3. Crop Growth Stage",
        "step4_upload_image": "4. Upload Leaf Photo",
        "btn_run_diagnosis": "Run AI Diagnosis & Risk Assessment",
        "btn_analyzing": "Analyzing Image & Weather...",

        # Quality & Errors
        "quality_issue_title": "Image Quality Issue",
        "quality_issue_msg": "The image quality is not sufficient for reliable analysis. Please upload a clearer image showing the affected part of the crop.",
        "invalid_file": "Invalid or corrupt file. Please select a valid image.",

        # Statuses
        "status_identified": "Identified",
        "status_healthy": "Healthy Foliage",
        "status_uncertain": "Uncertain (Expert Review Required)",
        "status_unknown": "Unknown / Unclassified Condition",
        "status_image_quality_issue": "Image Quality Issue",
        "status_pending_expert": "Awaiting Agricultural Expert Review",
        "status_verified": "Expert Verified Diagnosis",
        "status_lab_referral": "Referred for Laboratory Confirmation",
        "status_follow_up": "Follow-up Required",
        "status_closed": "Case Resolved & Closed",

        # Taxonomy & Roles
        "type_disease": "Crop Disease (Pathogen)",
        "type_pest": "Insect Pest Infestation",
        "type_healthy": "Healthy Crop",
        "type_unknown": "Unclassified Symptom",

        # Severity & Risk
        "severity_none": "None",
        "severity_low": "Low",
        "severity_moderate": "Moderate",
        "severity_high": "High",
        "severity_critical": "Critical",
        "severity_not_assessed": "Not Assessed",
        "risk_low": "Low Risk",
        "risk_moderate": "Moderate Risk",
        "risk_high": "High Risk",
        "risk_critical": "Critical Epidemic Risk",
        "risk_factors_title": "Contributing Risk Factors",
        "confidence_label": "AI Confidence",
        "severity_label": "Foliage Severity",
        "damage_area_label": "Estimated Visible Damage",
        "leaf_area_label": "Leaf Coverage",
        "weather_context_title": "Local Micro-Climate Context",
        "weather_temp": "Temperature",
        "weather_humidity": "Relative Humidity",
        "weather_rain": "Precipitation",
        "weather_source": "Source",
        "weather_unavailable": "Live weather telemetry unavailable for this coordinate",

        # Advisory Sections
        "advisory_title": "Integrated Pest Management (IPM) Advisory",
        "immediate_action_title": "Immediate Action",
        "monitoring_title": "Field Monitoring",
        "cultural_title": "Cultural & Preventive Measures",
        "biological_title": "Biological Control",
        "chemical_title": "Safe Chemical Guidance",
        "safety_title": "Farmer Safety & Legal Precautions",
        "referral_alert_title": "When to Contact Officer / KVK",
        "follow_up_alert": "Recommended follow-up observation in {days} days",

        # Follow up & Confirmation
        "followup_title": "Follow-up Observation & Field Outcome",
        "outcome_improved": "Condition Improved",
        "outcome_unchanged": "Condition Unchanged",
        "outcome_worsened": "Condition Worsened",
        "outcome_resolved": "Condition Completely Resolved",
        "btn_submit_followup": "Upload Follow-up Image",
        "btn_confirm_outcome": "Confirm Field Outcome",

        # Expert Desk
        "expert_desk_title": "Agricultural Expert & Doctor Review Portal",
        "pending_cases_count": "Cases Pending Review",
        "btn_confirm_ai": "Confirm AI Diagnosis",
        "btn_correct_ai": "Correct Diagnosis",
        "btn_refer_lab": "Refer to Laboratory",
        "btn_request_image": "Request Clearer Photo",
        "expert_notes_placeholder": "Add agronomic notes, chemical prescription, or cultural guidance...",

        # Officer Dashboard & GIS
        "dashboard_title": "Maharashtra Agriculture Officer GIS Intelligence",
        "total_observations": "Total Field Cases",
        "disease_cases": "Disease Outbreaks",
        "pest_cases": "Pest Infestations",
        "high_risk_alerts": "High Risk Alerts",
        "hotspot_map_title": "Geospatial Outbreak Hotspots (Maharashtra)",
        "district_distribution_title": "Top District Outbreaks",

        # Footer
        "footer_text": "FALCON-Q · IBM Qiskit Fall Fest 2026 · Problem Statement VNQFF-04 · Team TISSOT",

        # Reference Navigation & Dashboard
        "sidebar_subtitle": "AI for Healthy Crops · Prosperous Maharashtra",
        "nav_dashboard": "Dashboard",
        "nav_diagnose": "Diagnose Crop",
        "nav_fields": "My Fields",
        "nav_alerts": "Pest Alerts",
        "nav_weather": "Weather & Risk",
        "nav_hotspots": "Hotspot Map",
        "nav_advisory": "Treatment Advisory",
        "nav_reports": "Reports & Insights",
        "nav_expert_connect": "Expert Connect",
        "nav_knowledge": "Knowledge Hub",
        "nav_sensors": "Smart Traps & Sensors",
        "search_placeholder": "Search crops, diseases, advisories...",
        "hero_headline": "Healthy Crops, Brighter Tomorrows",
        "hero_supporting": "AI • Farmers • Sustainable Agriculture",
        "hero_quote": "Nirogi Sheti, Samruddh Maharashtra",
        "kpi_fields": "My Fields",
        "kpi_main_crop": "Main Crop",
        "kpi_crop_health": "Crop Health",
        "kpi_current_weather": "Current Weather",
        "recent_diagnosis_title": "Recent Diagnosis",
        "risk_forecast_title": "7-Day Disease Risk Forecast",
        "upcoming_alerts_title": "Upcoming Alerts",
        "btn_get_advisory": "Get Treatment Advisory",
        "btn_save_result": "Save Result",
        "btn_track_case": "Track Case",
        "btn_upload_another": "Upload Another Image",
        "unknown_state_title": "Unable to confidently identify this crop condition.",
        "unknown_state_desc": "Your case has been submitted to an agricultural expert for review.",
        "sensor_dashboard_title": "Smart Traps & Field Sensors",
        "sensor_dashboard_subtitle": "Live data from devices deployed in your fields.",
        "sensor_status_ready": "Sensor integration ready",
        "sensor_awaiting_data": "Awaiting sensor data",
        "pest_activity_trend": "Pest Activity Trend (Catch / Trap / Day)",
        "hotspot_title": "Pest Infestation Hotspot Map",
        "hotspot_subtitle": "Real-time view of pest and disease incidence across Maharashtra.",
        "advisory_view_title": "Treatment Advisory",
        "advisory_view_subtitle": "Personalized and location-specific recommendations for better crop health.",
        "quick_actions": "Quick Actions",
        "action_download_pdf": "Download PDF",
        "action_share": "Share",
        "action_consult_expert": "Consult Expert",
        "opt_immediate": "1. Immediate Action",
        "opt_organic": "2. Organic / IPM Option",
        "opt_chemical": "3. Chemical Option",
        "opt_additional": "4. Additional Information & Monitoring",
        "safe_use_notice": "Strictly comply with Maharashtra Agriculture Dept & CIBRC recommendations. Use PPE.",
        "waiting_period_label": "Waiting Period (Pre-Harvest Interval)",
        "follow_up_date_label": "Recommended Follow-up Inspection",
        "need_help_title": "Need Expert Agronomic Guidance?",
        "need_help_desc": "Connect with Taluka Agriculture Officer or KVK SMS advisory helpline.",

        # Navigation & Section Titles
        "nav_my_fields": "My Farms",
        "nav_treatment_advisory": "Treatment Advisory",
        "nav_weather_risk": "Weather & Risk",
        "nav_pest_alerts": "Surveillance Bulletin",
        "nav_hotspot_map": "Hotspot Map",
        "nav_smart_traps": "Smart Traps & Sensors",
        "nav_main_menu": "Main Navigation",
        "nav_officials_section": "Expert & Administration",

        # Subtitles
        "fields_subtitle": "Manage farm plots, crop growth stages, irrigation telemetry, and active disease monitoring.",
        "advisory_subtitle": "Personalized and location-specific recommendations for better crop health.",
        "alerts_subtitle": "Real-time taluka-level pest and disease alerts issued by Agriculture Department and State Universities.",
        "weather_subtitle": "Micro-climate telemetry, spray suitability indices, and disease favorability models.",
        "hotspots_subtitle": "Interactive spatial geospatial map based on live farmer diagnostic telemetry and verified cases.",
        "expert_subtitle": "Review and confirm AI crop diagnoses, suggest chemical prescriptions, and verify field cases.",
        "officer_subtitle": "District and taluka level pest outbreaks, disease spread analytics, and emergency advisories.",
        "sensors_subtitle": "Live telemetry from IoT smart pheromone traps, soil probes, and field sensors.",

        # Diagnose Page Elements
        "page_diagnose_title": "AI Crop Health Diagnosis & Prescription",
        "page_diagnose_subtitle": "Upload a clear crop photo for instant disease and pest identification backed by expert recommendations.",
        "awaiting_scan_title": "Diagnostic Results Will Appear Here",
        "awaiting_scan_sub": "Select a supported crop on the left, upload a clear leaf photo, and click 'Run AI Crop Health Diagnosis'.",
        "btn_choose_gallery": "Choose from Gallery",
        "btn_take_photo": "Take Photo",
        "btn_run_ai_diagnosis": "Run AI Crop Health Diagnosis",
        "try_sample_specimens": "Try Sample Leaf Specimens:",
        "step2_select_stage": "2. Crop Growth Stage",
        "step3_select_location": "3. Farm & Field Location",
        "step4_upload_photo": "4. Upload Leaf Photograph",
        "drag_drop_title": "Tap to browse from device or drag & drop photo here",
        "drag_drop_sub": "Supports JPEG, PNG, WEBP formats up to 15MB",

        # Labels & Metrics
        "label_district": "District",
        "label_taluka": "Taluka",
        "label_village": "Village / Locality",
        "metric_confidence": "AI Confidence",
        "metric_damage": "Foliage Damage",
        "metric_severity": "Severity Level",

        # Dashboard & Action Buttons
        "disease_risk_forecast": "7-Day Disease Risk Forecast",
        "pest_outbreak_alerts": "Pest Outbreak Alerts",
        "forecast_details": "Forecast Details",
        "all_alerts": "All Alerts",
        "kpi_my_fields": "My Fields",
        "kpi_weather": "Weather",
        "btn_diagnose_now": "Start Diagnosis Now",
        "btn_view_alerts": "Surveillance Bulletin",
        "btn_weather": "Weather & Spray Advisories",
        "modal_auth_title": "Sign In / Register",
        "label_fullname": "Full Name",
        "label_password": "Password",

        # Treatment Advisory Tab & Cards
        "adv_plan_badge": "Recommended IPM Treatment Plan",
        "adv_rec_source": "Recommendation Source:",
        "adv_source_guidelines": "MPKV Rahuri & CIBRC IPM Guidelines",
        "adv_card1_title": "1. Immediate Sanitation & Cultural Controls",
        "adv_card1_sub": "Immediate Action & Cultural Sanitation",
        "adv_card2_title": "2. Biological & Eco-Friendly Controls",
        "adv_card2_sub": "Biological & Biopesticide Measures",
        "adv_card3_title": "3. Approved Chemical Control (Threshold-Based)",
        "adv_card3_sub": "Chemical Control with Safety Waiting Period",
        "adv_card4_title": "4. Crop Stage Monitoring & Follow-Up",
        "adv_card4_sub": "Stage Precautions & Follow-up Timeline",
        "adv_cultural_practice_label": "Cultural Practice:",
        "adv_safe_pollinators": "Safe for beneficial pollinators and honeybees.",
        "adv_phi_label": "Pre-Harvest Interval (PHI): 14 Days",
        "adv_cibrc_title": "CIBRC Registered Pesticide Verification",
        "adv_cibrc_sub": "Enter commercial trade name to verify Central Insecticides Board approval, dosage, and waiting periods:",
        "adv_cibrc_placeholder": "e.g. Coragen, Nativo, Amistar Top...",
        "btn_verify": "Verify",
        "btn_submit_followup_photo": "Submit Follow-Up Photo",

        # Weather Indices
        "weather_spray_index": "Foliar Spray Suitability Index",
        "weather_evapo_index": "Evapotranspiration & Heat Stress",
        "label_weather_advisory": "Weather Advisory:",

        # Farm Cards
        "farm_active": "Active Farm",
        "farm_primary_crop": "Primary Crop",
        "farm_area": "Area",
        "farm_acres": "Acres",
        "farm_irrigation": "Irrigation",
        "farm_drip": "Drip Irrigation",
        "farm_state": "State",
        "farm_surveillance": "Surveillance Active",
        "farm_check_health": "Check Crop Health",

        # Work History & Audit Modal
        "work_history_title": "User Activity & Work History Log",
        "work_history_subtitle": "Complete audit trail of user logins, search queries, voice consultations, and crop diagnoses.",
        "btn_close": "Close",

        # Additional Advisory & Section Elements
        "adv_safety_label": "Safety:",
        "adv_safety_text": "Safety: Wear standard PPE kit. Never spray against prevailing wind directions.",
        "adv_phi_warning": "Misidentified spraying risks severe crop phytotoxicity and financial loss.",
        "btn_print_advisory": "Print Advisory",
        "btn_share_whatsapp": "Share via WhatsApp",
        "advisory_empty_title": "No Diagnosis Initiated Yet",
        "advisory_empty_sub": "You have not run any crop health diagnosis yet. Upload or scan a leaf photograph in the Crop Health Diagnosis section to generate your verified, crop-specific Integrated Pest Management (IPM) treatment plan.",
        "btn_start_diagnosis_now": "Start Crop Diagnosis Now",
        "btn_return_dashboard": "Return to Dashboard",
        "weather_fungal_index": "Fungal Spore Germination Index",
        "weather_pest_index": "Insect Pest Multiplication Rate",
        "weather_wind_high_advice": "High wind speed ({wind} km/h) or precipitation detected. Avoid foliar spraying now.",
        "weather_wind_optimal_advice": "Wind speed ({wind} km/h) is optimal. Morning hours are suitable for foliar spraying.",
        "farm_portfolio_title": "My Farms (Farm Field Portfolio)",
        "farm_register_new": "Register New Farm",
        "farm_no_registered": "No Farms Registered Yet",
        "farm_register_sub": "Register your farm plots to begin automated health monitoring.",
        "btn_register_first_farm": "Register First Farm",
        "log_login": "User Login",
        "log_logout": "User Logout",
        "log_search": "Search Query",
        "log_diagnosis": "Crop Diagnosis",
        "log_diagnosis_rejected": "Diagnosis Rejected",
        "log_voice_query": "Voice Consultation",
        "log_language_change": "Language Change",
        "log_view_advisory": "View Advisory",
        "log_completed_action": "Completed action",
        "log_loading": "Loading activity logs...",
        "log_empty": "No activity recorded yet for this account."
    },

    "mr": {
        # Navigation & Brand
        "app_title": "फाल्कन-एआय | पीक आरोग्य निर्णय सहाय्य प्रणाली",
        "service_subtitle": "आयबीएम किट फॉल फेस्ट २०२६ · VNQFF-04 · टीम TISSOT",
        "nav_farmer_portal": "शेतकरी सेवा",
        "nav_expert_desk": "कृषी तज्ज्ञ पुनरावलोकन",
        "nav_officer_dashboard": "कृषी अधिकारी डॅशबोर्ड",
        "nav_login": "प्रवेश / नोंदणी",
        "nav_logout": "बाहेर पडा",
        "language_select": "भाषा",

        # Hero & Upload
        "hero_eyebrow": "लवकर निदान व एकात्मिक पीक कीड-रोग व्यवस्थापन",
        "hero_title": "एआय तंत्रज्ञान आणि कृषी तज्ज्ञांच्या सल्ल्याने पिकांचे रक्षण करा",
        "hero_desc": "बाधित पिकाचे छायाचित्र अपलोड करा. झटपट एआय निदान, हवामान-आधारित धोका मूल्यांकन आणि अधिकृत कृषी सल्ला मिळवा.",
        "start_assessment": "पीक आरोग्य तपासणी सुरू करा",
        "upload_subtext": "मोबाईल कॅमेऱ्याने स्पष्ट फोटो काढा किंवा गॅलरीतून निवडा.",
        "btn_open_camera": "कॅमेरा उघडा",
        "btn_upload_pc": "फोटो निवडा",
        "drop_zone_text": "पिकाचा फोटो येथे टाका किंवा फाईल निवडा",
        "drop_zone_sub": "JPG, JPEG, PNG किंवा WEBP (कमाल १५ MB)",
        "step1_select_crop": "१. पीक निवडा",
        "step2_select_location": "२. शेत व ठिकाण",
        "step3_select_stage": "३. पिकाची वाढ अवस्था",
        "step4_upload_image": "४. पानाचा फोटो अपलोड करा",
        "btn_run_diagnosis": "एआय रोग निदान व धोका तपासा",
        "btn_analyzing": "फोटो व स्थानिक हवामान तपासत आहे...",

        # Quality & Errors
        "quality_issue_title": "फोटोची गुणवत्ता अपुरी आहे",
        "quality_issue_msg": "विश्वसनीय विश्लेषणासाठी फोटोची गुणवत्ता पुरेशी नाही. कृपया पिकाचा बाधित भाग स्पष्ट दिसेल असा दुसरा फोटो अपलोड करा.",
        "invalid_file": "अवैध फाईल प्रकार. कृपया वैध फोटो निवडा.",

        # Statuses
        "status_identified": "रोग/कीड निश्चित ओळखली",
        "status_healthy": "निरोगी पीक",
        "status_uncertain": "संशयित / अनिश्चित (तज्ज्ञ पुनरावलोकन आवश्यक)",
        "status_unknown": "अपरिचित / अनाकलनीय लक्षणे (तज्ज्ञांकडे वर्ग)",
        "status_image_quality_issue": "फोटो अस्पष्ट / अपुरी गुणवत्ता",
        "status_pending_expert": "कृषी तज्ज्ञांच्या तपासणीसाठी प्रलंबित",
        "status_verified": "कृषी तज्ज्ञांनी प्रमाणित केलेले निदान",
        "status_lab_referral": "प्रयोगशाळा तपासणीसाठी शिफारस",
        "status_follow_up": "पाठपुरावा निरीक्षण आवश्यक",
        "status_closed": "प्रकरण पूर्ण व बंद",

        # Taxonomy & Roles
        "type_disease": "पीक रोग (बुरशी / जिवाणू / विषाणू)",
        "type_pest": "कीटकांचा प्रादुर्भाव (कीड)",
        "type_healthy": "निरोगी पीक",
        "type_unknown": "अनाकलनीय लक्षण",

        # Severity & Risk
        "severity_none": "नाही",
        "severity_low": "कमी (सौम्य)",
        "severity_moderate": "मध्यम",
        "severity_high": "जास्त (तीव्र)",
        "severity_critical": "अतिगंभीर",
        "severity_not_assessed": "तपासले नाही",
        "risk_low": "कमी धोका",
        "risk_moderate": "मध्यम धोका",
        "risk_high": "उच्च धोका",
        "risk_critical": "अतिगंभीर प्रादुर्भाव धोका",
        "risk_factors_title": "धोका निर्माण करणारे घटक",
        "confidence_label": "एआय अचूकता (विश्वासार्हता)",
        "severity_label": "पानांवरील तीव्रता",
        "damage_area_label": "अंदाजित बाधित क्षेत्र",
        "leaf_area_label": "पानाचा आकार",
        "weather_context_title": "स्थानिक सूक्ष्म-हवामान परिस्थिती",
        "weather_temp": "तापमान",
        "weather_humidity": "हवेतील आर्द्रता",
        "weather_rain": "पाऊस",
        "weather_source": "माहिती स्रोत",
        "weather_unavailable": "या स्थानासाठी थेट हवामान उपलब्ध नाही",

        # Advisory Sections
        "advisory_title": "एकात्मिक कीड व रोग व्यवस्थापन (IPM) सल्ला",
        "immediate_action_title": "त्वरित करावयाची उपाययोजना",
        "monitoring_title": "शेत पाहणी व निरीक्षण",
        "cultural_title": "मशागती व प्रतिबंधात्मक उपाय",
        "biological_title": "जैविक नियंत्रण पद्धती",
        "chemical_title": "सुरक्षित रासायनिक उपाय (फवारणी)",
        "safety_title": "शेतकरी सुरक्षितता व कायदेशीर खबरदारी",
        "referral_alert_title": "कृषी अधिकारी / केव्हीके कडे कधी संपर्क साधावा",
        "follow_up_alert": "शिफारस: पुढील {days} दिवसांत पुन्हा पाहणी करून फोटो अपलोड करा",

        # Follow up & Confirmation
        "followup_title": "पाठपुरावा निरीक्षण व प्रत्यक्ष शेतातील परिणाम",
        "outcome_improved": "स्थिती सुधारली",
        "outcome_unchanged": "स्थिती जैसे थे आहे",
        "outcome_worsened": "स्थिती अधिक बिघडली",
        "outcome_resolved": "रोग/कीड पूर्णपणे नियंत्रणात आली",
        "btn_submit_followup": "पाठपुरावा फोटो अपलोड करा",
        "btn_confirm_outcome": "प्रत्यक्ष शेत परिणाम नोंदवा",

        # Expert Desk
        "expert_desk_title": "कृषी तज्ज्ञ व कृषी डॉक्टर पुनरावलोकन पोर्टल",
        "pending_cases_count": "तपासणीसाठी प्रलंबित प्रकरणे",
        "btn_confirm_ai": "एआय निदान मान्य करा",
        "btn_correct_ai": "निदान दुरुस्त करा",
        "btn_refer_lab": "प्रयोगशाळेकडे वर्ग करा",
        "btn_request_image": "अधिक स्पष्ट फोटो मागा",
        "expert_notes_placeholder": "कृषी सल्ला, औषध शिफारस किंवा सूचना लिहा...",

        # Officer Dashboard & GIS
        "dashboard_title": "महाराष्ट्र कृषी अधिकारी भौगोलिक बुद्धिमत्ता (GIS)",
        "total_observations": "एकूण नोंदवलेली प्रकरणे",
        "disease_cases": "रोग प्रादुर्भाव",
        "pest_cases": "कीड प्रादुर्भाव",
        "high_risk_alerts": "उच्च धोक्याचे इशारे",
        "hotspot_map_title": "भौगोलिक हॉटस्पॉट नकाशा (महाराष्ट्र राज्य)",
        "district_distribution_title": "जिल्हानिहाय प्रादुर्भाव प्रमाण",

        # Footer
        "footer_text": "फाल्कन-क्यू · आयबीएम किट फॉल फेस्ट २०२६ · VNQFF-04 · टीम TISSOT",

        # Reference Navigation & Dashboard
        "sidebar_subtitle": "पिकांचे उत्तम आरोग्य · समृद्ध महाराष्ट्र",
        "nav_dashboard": "डॅशबोर्ड",
        "nav_diagnose": "पीक निदान",
        "nav_fields": "माझी शेती",
        "nav_alerts": "कीड-रोग अलर्ट",
        "nav_weather": "हवामान व धोका",
        "nav_hotspots": "हॉटस्पॉट नकाशा",
        "nav_advisory": "उपचार सल्ला",
        "nav_reports": "अहवाल व विश्लेषण",
        "nav_expert_connect": "कृषी तज्ज्ञ सल्ला",
        "nav_knowledge": "ज्ञान केंद्र",
        "nav_sensors": "स्मार्ट ट्रॅप व सेन्सर्स",
        "search_placeholder": "पीक, रोग, सल्ला शोधा...",
        "hero_headline": "निरोगी पिके, उज्ज्वल भविष्य",
        "hero_supporting": "एआय • शेतकरी • शाश्वत शेती",
        "hero_quote": "निरोगी शेती, समृद्ध महाराष्ट्र",
        "kpi_fields": "माझी शेती",
        "kpi_main_crop": "मुख्य पीक",
        "kpi_crop_health": "पीक आरोग्य",
        "kpi_current_weather": "सद्य हवामान",
        "recent_diagnosis_title": "मागील पीक निदान",
        "risk_forecast_title": "७ दिवसांचा रोग धोका अंदाज",
        "upcoming_alerts_title": "आगामी सूचना व अलर्ट",
        "btn_get_advisory": "उपचार सल्ला पहा",
        "btn_save_result": "निकाल जतन करा",
        "btn_track_case": "प्रकरण स्थिती पहा",
        "btn_upload_another": "दुसरा फोटो अपलोड करा",
        "unknown_state_title": "या लक्षणांचे ठामपणे निदान होऊ शकले नाही.",
        "unknown_state_desc": "हे प्रकरण कृषी तज्ज्ञांच्या तपासणीसाठी वर्ग करण्यात आले आहे.",
        "sensor_dashboard_title": "स्मार्ट ट्रॅप व शेती सेन्सर्स",
        "sensor_dashboard_subtitle": "शेतातील उपकरणांकडून मिळणारी थेट माहिती.",
        "sensor_status_ready": "सेन्सर जोडणीसाठी सज्ज",
        "sensor_awaiting_data": "माहितीची प्रतीक्षा",
        "pest_activity_trend": "कीड हालचाल प्रमाण (ट्रॅप/दिवस)",
        "hotspot_title": "कीड प्रादुर्भाव भौगोलिक हॉटस्पॉट नकाशा",
        "hotspot_subtitle": "महाराष्ट्र राज्यातील कीड व रोगांचे थेट भौगोलिक दृश्य.",
        "advisory_view_title": "एकात्मिक उपचार सल्ला",
        "advisory_view_subtitle": "उत्तम पीक आरोग्यासाठी वैयक्तिकृत व स्थानिक हवामान-आधारित शिफारसी.",
        "quick_actions": "जलद कृती",
        "action_download_pdf": "पीडीएफ डाउनलोड",
        "action_share": "शेअर करा",
        "action_consult_expert": "तज्ज्ञांचा सल्ला घ्या",
        "opt_immediate": "१. त्वरित करावयाची उपाययोजना",
        "opt_organic": "२. सेंद्रिय / जैविक व मशागतीचे उपाय",
        "opt_chemical": "३. रासायनिक उपाय (नियंत्रित फवारणी)",
        "opt_additional": "४. अतिरिक्त माहिती, खबरदारी व पाठपुरावा",
        "safe_use_notice": "महाराष्ट्र कृषी विभाग व CIBRC शिफारसींचे तंतोतंत पालन करा. संरक्षक पोशाख वापरा.",
        "waiting_period_label": "फवारणीनंतर काढणी प्रतीक्षा कालावधी (PHI)",
        "follow_up_date_label": "पुढील पाहणीची शिफारस",
        "need_help_title": "तज्ज्ञ कृषी डॉक्टरांचे मार्गदर्शन हवे आहे का?",
        "need_help_desc": "तालुका कृषी अधिकारी किंवा केव्हीके कृषी विज्ञान केंद्राशी संपर्क साधा.",

        # Navigation & Section Titles
        "nav_my_fields": "माझी शेती",
        "nav_treatment_advisory": "उपचार सल्ला",
        "nav_weather_risk": "हवामान व धोका",
        "nav_pest_alerts": "निरीक्षण बुलेटिन",
        "nav_hotspot_map": "हॉटस्पॉट नकाशा",
        "nav_smart_traps": "स्मार्ट ट्रॅप्स व सेन्सर्स",
        "nav_main_menu": "मुख्य नेव्हिगेशन",
        "nav_officials_section": "तज्ज्ञ व प्रशासन",

        # Subtitles
        "fields_subtitle": "शेताचे भूखंड, पिकाची वाढ अवस्था, सिंचन माहिती आणि रोग निरीक्षणाचे व्यवस्थापन करा.",
        "advisory_subtitle": "उत्कृष्ट पीक आरोग्यासाठी वैयक्तिक आणि स्थान-विशिष्ट शिफारसी.",
        "alerts_subtitle": "कृषी विभाग आणि राज्य कृषी विद्यापीठांद्वारे जारी केलेले रिअल-टाइम तालुका-स्तरीय कीड आणि रोग अलर्ट.",
        "weather_subtitle": "स्थानिक सूक्ष्म-हवामान, फवारणी उपयुक्तता निर्देशांक आणि रोग अनुकूलता मॉडेल.",
        "hotspots_subtitle": "शेतकऱ्यांचे थेट निदान आणि प्रमाणित प्रकरणांवर आधारित नकाशा.",
        "expert_subtitle": "एआय पीक निदानाचे पुनरावलोकन व प्रमाणीकरण करा, औषधोपचार सुचवा आणि शेतातील प्रकरणे तपासा.",
        "officer_subtitle": "जिल्हा व तालुका पातळीवरील कीड प्रादुर्भाव, रोग प्रसार विश्लेषण आणि आणीबाणी सल्ला.",
        "sensors_subtitle": "स्मार्ट फेरोमोन ट्रॅप्स, माती तपासणी साधने आणि सेन्सर्सवरून थेट माहिती.",

        # Diagnose Page Elements
        "page_diagnose_title": "एआय पीक आरोग्य निदान व उपचार",
        "page_diagnose_subtitle": "तज्ज्ञांच्या शिफारसींसह झटपट रोग व कीड ओळखण्यासाठी पिकाचा स्पष्ट फोटो अपलोड करा.",
        "awaiting_scan_title": "निदान निकाल येथे दिसतील",
        "awaiting_scan_sub": "डावीकडे समर्थित पीक निवडा, पानाचा स्पष्ट फोटो अपलोड करा आणि 'एआय पीक आरोग्य निदान करा' वर क्लिक करा.",
        "btn_choose_gallery": "गॅलरीतून निवडा",
        "btn_take_photo": "फोटो काढा",
        "btn_run_ai_diagnosis": "एआय पीक आरोग्य निदान करा",
        "try_sample_specimens": "नमुना पानांचे नमुने पहा:",
        "step2_select_stage": "२. पिकाची वाढ अवस्था",
        "step3_select_location": "३. शेत व शेताचे ठिकाण",
        "step4_upload_photo": "४. पानाचा फोटो अपलोड करा",
        "drag_drop_title": "फोटो निवडण्यासाठी येथे टॅप करा किंवा ड्रॅग करा",
        "drag_drop_sub": "JPEG, PNG, WEBP प्रकार समर्थित (कमाल १५ MB)",

        # Labels & Metrics
        "label_district": "जिल्हा",
        "label_taluka": "तालुका",
        "label_village": "गाव / परिसर",
        "metric_confidence": "एआय विश्वासार्हता",
        "metric_damage": "पानावरील नुकसान",
        "metric_severity": "तीव्रता पातळी",

        # Dashboard & Action Buttons
        "disease_risk_forecast": "७-दिवसीय रोग धोका अंदाज",
        "pest_outbreak_alerts": "कीड प्रादुर्भाव सूचना",
        "forecast_details": "अंदाज तपशील",
        "all_alerts": "सर्व सूचना",
        "kpi_my_fields": "माझी शेती",
        "kpi_weather": "हवामान",
        "btn_diagnose_now": "निदान सुरू करा",
        "btn_view_alerts": "निरीक्षण बुलेटिन",
        "btn_weather": "हवामान व फवारणी सल्ला",
        "modal_auth_title": "प्रवेश / नोंदणी करा",
        "label_fullname": "पूर्ण नाव",
        "label_password": "पासवर्ड",

        # Treatment Advisory Tab & Cards
        "adv_plan_badge": "शिफारस केलेली एकात्मिक कीड व्यवस्थापन (IPM) योजना",
        "adv_rec_source": "शिफारस स्रोत:",
        "adv_source_guidelines": "महात्मा फुले कृषी विद्यापीठ राहुरी व CIBRC मार्गदर्शक तत्त्वे",
        "adv_card1_title": "१. त्वरित स्वच्छता व मशागतीची कामे",
        "adv_card1_sub": "त्वरित कृती व शेतातील स्वच्छता",
        "adv_card2_title": "२. जैविक व पर्यावरणपूरक उपाय",
        "adv_card2_sub": "जैविक व जैव-कीटकनाशक उपाय",
        "adv_card3_title": "३. अधिकृत रासायनिक नियंत्रण (आर्थिक नुकसान पातळीनुसार)",
        "adv_card3_sub": "सुरक्षित प्रतीक्षा कालावधीसह रासायनिक नियंत्रण",
        "adv_card4_title": "४. पिकाची वाढ अवस्था निरीक्षण व पाठपुरावा",
        "adv_card4_sub": "वाढ अवस्थेतील खबरदारी व पाठपुरावा वेळापत्रक",
        "adv_cultural_practice_label": "मशागत पद्धती:",
        "adv_safe_pollinators": "उपयुक्त परागीभवन कीटक आणि मधमाश्यांसाठी सुरक्षित.",
        "adv_phi_label": "कापणीपूर्व प्रतीक्षा कालावधी (PHI): १४ दिवस",
        "adv_cibrc_title": "CIBRC नोंदणीकृत कीटकनाशक पडताळणी",
        "adv_cibrc_sub": "केंद्रीय कीटकनाशक मंडळ (CIBRC) मान्यता, प्रमाण आणि प्रतीक्षा कालावधी तपासण्यासाठी व्यापारी नाव टाका:",
        "adv_cibrc_placeholder": "उदा. कोराजन, नेटिव्हो, ॲमिस्टार टॉप...",
        "btn_verify": "तपासा",
        "btn_submit_followup_photo": "पाठपुरावा फोटो पाठवा",

        # Weather Indices
        "weather_spray_index": "फवारणी उपयुक्तता निर्देशांक",
        "weather_evapo_index": "बाष्पीभवन व उष्णता ताण",
        "label_weather_advisory": "हवामान सल्ला:",

        # Farm Cards
        "farm_active": "सक्रिय शेत",
        "farm_primary_crop": "मुख्य पीक",
        "farm_area": "क्षेत्रफळ",
        "farm_acres": "एकर",
        "farm_irrigation": "सिंचन",
        "farm_drip": "ठिबक सिंचन",
        "farm_state": "राज्य",
        "farm_surveillance": "निरीक्षण सुरू",
        "farm_check_health": "पीक आरोग्य तपासा",

        # Work History & Audit Modal
        "work_history_title": "वापरकर्ता कृती व कामाचा इतिहास लॉग",
        "work_history_subtitle": "लॉगिन, शोध, व्हॉइस सल्ला आणि पीक निदानाची संपूर्ण ऑडिट नोंद.",
        "btn_close": "बंद करा",

        # Additional Advisory & Section Elements
        "adv_safety_label": "सुरक्षितता खबरदारी:",
        "adv_safety_text": "सुरक्षितता: प्रमाणित PPE किट (संरक्षक पोशाख) वापरा. वाऱ्याच्या उलट दिशेने कधीही फवारणी करू नका.",
        "adv_phi_warning": "चुकीच्या किंवा अनावश्यक फवारणीमुळे पिकाचे नुकसान (फायटोटॉक्सिसिटी) आणि आर्थिक हानी होऊ शकते.",
        "btn_print_advisory": "सल्ला मुद्रित करा",
        "btn_share_whatsapp": "व्हॉट्सॲपवर शेअर करा",
        "advisory_empty_title": "अद्याप पीक निदान सुरू केलेले नाही",
        "advisory_empty_sub": "तुम्ही अद्याप कोणतेही पीक आरोग्य निदान चालवलेले नाही. प्रमाणित एकात्मिक कीड व्यवस्थापन (IPM) उपचार आराखडा तयार करण्यासाठी पीक आरोग्य निदान विभागात पानाचा फोटो अपलोड करा किंवा स्कॅन करा.",
        "btn_start_diagnosis_now": "आता पीक निदान सुरू करा",
        "btn_return_dashboard": "डॅशबोर्डवर परत जा",
        "weather_fungal_index": "बुरशी बीजाणू अंकुरण निर्देशांक",
        "weather_pest_index": "कीड वाढ दर",
        "weather_wind_high_advice": "वाऱ्याचा वेग जास्त ({wind} किमी/तास) किंवा पाऊस आढळला. सध्या फवारणी करणे टाळा.",
        "weather_wind_optimal_advice": "वाऱ्याचा वेग ({wind} किमी/तास) अनुकूल आहे. सकाळच्या वेळेत फवारणी करणे योग्य राहील.",
        "farm_portfolio_title": "माझी शेती (शेत भूखंड संच)",
        "farm_register_new": "नवीन शेत नोंदणी करा",
        "farm_no_registered": "अद्याप कोणतेही शेत नोंदणीकृत नाही",
        "farm_register_sub": "स्वयंचलित पीक आरोग्य निरीक्षणासाठी तुमच्या शेताची नोंदणी करा.",
        "btn_register_first_farm": "पहिले शेत नोंदवा",
        "log_login": "प्रवेश (लॉगिन)",
        "log_logout": "बाहेर पडले (लॉगआउट)",
        "log_search": "शोध",
        "log_diagnosis": "पीक निदान",
        "log_diagnosis_rejected": "निदान नाकारले",
        "log_voice_query": "व्हॉइस सल्ला",
        "log_language_change": "भाषा बदल",
        "log_view_advisory": "उपचार सल्ला पाहिला",
        "log_completed_action": "कृती पूर्ण झाली",
        "log_loading": "कामाचा इतिहास लोड होत आहे...",
        "log_empty": "या खात्यासाठी अद्याप कोणतीही कृती नोंदलेली नाही."
    },

    "hi": {
        # Navigation & Brand
        "app_title": "फाल्कन-एआई | फसल स्वास्थ्य निर्णय सहायता प्रणाली",
        "service_subtitle": "आईबीएम किस्कित फॉल फेस्ट 2026 · VNQFF-04 · टीम TISSOT",
        "nav_farmer_portal": "किसान पोर्टल",
        "nav_expert_desk": "कृषि विशेषज्ञ समीक्षा",
        "nav_officer_dashboard": "कृषि अधिकारी डैशबोर्ड",
        "nav_login": "लॉग इन / पंजीकरण",
        "nav_logout": "लॉग आउट",
        "language_select": "भाषा",

        # Hero & Upload
        "hero_eyebrow": "प्रारंभिक पहचान एवं एकीकृत फसल रोग व कीट प्रबंधन",
        "hero_title": "एआई निदान और कृषि विशेषज्ञ मार्गदर्शन से फसलों की सुरक्षा करें",
        "hero_desc": "प्रभावित फसल की तस्वीर अपलोड करें। त्वरित एआई पहचान, मौसम-आधारित जोखिम मूल्यांकन और प्रमाणित कृषि सलाह प्राप्त करें।",
        "start_assessment": "फसल स्वास्थ्य जांच शुरू करें",
        "upload_subtext": "मोबाइल कैमरे से साफ फोटो लें या गैलरी से चुनें।",
        "btn_open_camera": "कैमरा खोलें",
        "btn_upload_pc": "फोटो चुनें",
        "drop_zone_text": "फसल की फोटो यहाँ खींचें या फाइल चुनें",
        "drop_zone_sub": "JPG, JPEG, PNG या WEBP (अधिकतम 15 MB)",
        "step1_select_crop": "1. फसल चुनें",
        "step2_select_location": "2. खेत व स्थान",
        "step3_select_stage": "3. फसल वृद्धि अवस्था",
        "step4_upload_image": "4. पत्ती की तस्वीर अपलोड करें",
        "btn_run_diagnosis": "एआई रोग पहचान एवं जोखिम जांचें",
        "btn_analyzing": "छवि व मौसम का विश्लेषण हो रहा है...",

        # Quality & Errors
        "quality_issue_title": "तस्वीर की गुणवत्ता अपर्याप्त है",
        "quality_issue_msg": "विश्वसनीय विश्लेषण के लिए तस्वीर की गुणवत्ता पर्याप्त नहीं है। कृपया प्रभावित हिस्से की स्पष्ट तस्वीर दोबारा अपलोड करें।",
        "invalid_file": "अमान्य फाइल। कृपया वैध तस्वीर चुनें।",

        # Statuses
        "status_identified": "सटीक पहचान हो गई",
        "status_healthy": "स्वस्थ फसल",
        "status_uncertain": "अनिश्चित (विशेषज्ञ समीक्षा आवश्यक)",
        "status_unknown": "अज्ञात लक्षण (विशेषज्ञ को भेजा गया)",
        "status_image_quality_issue": "धुंधली / अपर्याप्त गुणवत्ता वाली तस्वीर",
        "status_pending_expert": "कृषि विशेषज्ञ समीक्षा हेतु लंबित",
        "status_verified": "विशेषज्ञ द्वारा प्रमाणित निदान",
        "status_lab_referral": "प्रयोगशाला जांच हेतु अनुशंसित",
        "status_follow_up": "पुनरावलोकन आवश्यक",
        "status_closed": "मामला हल व बंद",

        # Taxonomy & Roles
        "type_disease": "फसल रोग (रोगजनक)",
        "type_pest": "कीट प्रकोप",
        "type_healthy": "स्वस्थ फसल",
        "type_unknown": "अज्ञात लक्षण",

        # Severity & Risk
        "severity_none": "कोई नहीं",
        "severity_low": "कम (हल्का)",
        "severity_moderate": "मध्यम",
        "severity_high": "अधिक (तीव्र)",
        "severity_critical": "अति गंभीर",
        "severity_not_assessed": "जांच नहीं की गई",
        "risk_low": "कम जोखिम",
        "risk_moderate": "मध्यम जोखिम",
        "risk_high": "उच्च जोखिम",
        "risk_critical": "अति गंभीर जोखिम",
        "risk_factors_title": "जोखिम कारक",
        "confidence_label": "एआई सटीकता",
        "severity_label": "पत्ती पर गंभीरता",
        "damage_area_label": "अनुमानित प्रभावित क्षेत्र",
        "leaf_area_label": "पत्ती क्षेत्र",
        "weather_context_title": "स्थानीय सूक्ष्म जलवायु स्थिति",
        "weather_temp": "तापमान",
        "weather_humidity": "आर्द्रता",
        "weather_rain": "वर्षा",
        "weather_source": "स्रोत",
        "weather_unavailable": "इस स्थान के लिए मौसम डेटा उपलब्ध नहीं है",

        # Advisory Sections
        "advisory_title": "एकीकृत कीट एवं रोग प्रबंधन (IPM) सलाह",
        "immediate_action_title": "तत्काल कार्रवाई",
        "monitoring_title": "खेत निगरानी",
        "cultural_title": "कृषि एवं निवारक उपाय",
        "biological_title": "जैविक नियंत्रण",
        "chemical_title": "सुरक्षित रासायनिक मार्गदर्शन",
        "safety_title": "किसान सुरक्षा एवं सावधानियां",
        "referral_alert_title": "कृषि अधिकारी / केवीके से कब संपर्क करें",
        "follow_up_alert": "अनुशंसा: अगले {days} दिनों में दोबारा जांच कर तस्वीर अपलोड करें",

        # Follow up & Confirmation
        "followup_title": "फॉलो-अप अवलोकन एवं खेत परिणाम",
        "outcome_improved": "स्थिति में सुधार हुआ",
        "outcome_unchanged": "स्थिति वैसी ही है",
        "outcome_worsened": "स्थिति और बिगड़ी",
        "outcome_resolved": "रोग/कीट पूरी तरह समाप्त",
        "btn_submit_followup": "फॉलो-अप फोटो अपलोड करें",
        "btn_confirm_outcome": "खेत परिणाम की पुष्टि करें",

        # Expert Desk
        "expert_desk_title": "कृषि विशेषज्ञ पोर्टल",
        "pending_cases_count": "समीक्षा हेतु लंबित मामले",
        "btn_confirm_ai": "एआई निदान की पुष्टि करें",
        "btn_correct_ai": "निदान सही करें",
        "btn_refer_lab": "प्रयोगशाला रेफर करें",
        "btn_request_image": "स्पष्ट फोटो मांगें",
        "expert_notes_placeholder": "सलाह या कीटनाशक निर्देश लिखें...",

        # Officer Dashboard & GIS
        "dashboard_title": "महाराष्ट्र कृषि अधिकारी जीआईएस इंटेलिजेंस",
        "total_observations": "कुल दर्ज मामले",
        "disease_cases": "रोग प्रकोप",
        "pest_cases": "कीट प्रकोप",
        "high_risk_alerts": "उच्च जोखिम चेतावनी",
        "hotspot_map_title": "भौगोलिक हॉटस्पॉट मानचित्र (महाराष्ट्र)",
        "district_distribution_title": "जिलावार प्रकोप दर",

        # Footer
        "footer_text": "फाल्कन-क्यू · आईबीएम किस्कित फॉल फेस्ट 2026 · VNQFF-04 · टीम TISSOT",

        # Reference Navigation & Dashboard
        "sidebar_subtitle": "फसलों का उत्तम स्वास्थ्य · समृद्ध महाराष्ट्र",
        "nav_dashboard": "डैशबोर्ड",
        "nav_diagnose": "फसल निदान",
        "nav_fields": "मेरे खेत",
        "nav_alerts": "कीट-रोग अलर्ट",
        "nav_weather": "मौसम व जोखिम",
        "nav_hotspots": "हॉटस्पॉट नक्शा",
        "nav_advisory": "उपचार सलाह",
        "nav_reports": "रिपोर्ट्स एवं विश्लेषण",
        "nav_expert_connect": "कृषि विशेषज्ञ परामर्श",
        "nav_knowledge": "ज्ञान केंद्र",
        "nav_sensors": "स्मार्ट ट्रैप एवं सेंसर्स",
        "search_placeholder": "फसल, रोग, सलाह खोजें...",
        "hero_headline": "स्वस्थ फसलें, उज्ज्वल भविष्य",
        "hero_supporting": "एआई • किसान • संधारणीय कृषि",
        "hero_quote": "निरोगी खेती, समृद्ध महाराष्ट्र",
        "kpi_fields": "मेरे खेत",
        "kpi_main_crop": "मुख्य फसल",
        "kpi_crop_health": "फसल स्वास्थ्य",
        "kpi_current_weather": "वर्तमान मौसम",
        "recent_diagnosis_title": "हालिया फसल निदान",
        "risk_forecast_title": "७ दिनों का रोग जोखिम पूर्वानुमान",
        "upcoming_alerts_title": "आगामी सूचनाएं एवं अलर्ट",
        "btn_get_advisory": "उपचार सलाह देखें",
        "btn_save_result": "परिणाम सहेजें",
        "btn_track_case": "मामला ट्रैक करें",
        "btn_upload_another": "दूसरी तस्वीर अपलोड करें",
        "unknown_state_title": "इस स्थिति की निश्चित पहचान नहीं हो सकी।",
        "unknown_state_desc": "यह मामला कृषि विशेषज्ञ समीक्षा के लिए भेज दिया गया है।",
        "sensor_dashboard_title": "स्मार्ट ट्रैप एवं फील्ड सेंसर्स",
        "sensor_dashboard_subtitle": "खेत में स्थापित उपकरणों से प्राप्त लाइव डेटा।",
        "sensor_status_ready": "सेंसर एकीकरण तैयार",
        "sensor_awaiting_data": "डेटा की प्रतीक्षा",
        "pest_activity_trend": "कीट गतिविधि रुझान (ट्रैप/दिन)",
        "hotspot_title": "कीट प्रकोप भौगोलिक हॉटस्पॉट नक्शा",
        "hotspot_subtitle": "महाराष्ट्र भर में कीट एवं रोग प्रकोप का वास्तविक दृश्य।",
        "advisory_view_title": "एकीकृत उपचार सलाह",
        "advisory_view_subtitle": "बेहतर फसल स्वास्थ्य के लिए व्यक्तिगत एवं स्थानीय सिफारिशें।",
        "quick_actions": "त्वरित कार्रवाई",
        "action_download_pdf": "पीडीएफ डाउनलोड",
        "action_share": "साझा करें",
        "action_consult_expert": "विशेषज्ञ से परामर्श लें",
        "opt_immediate": "१. तत्काल कार्रवाई",
        "opt_organic": "२. जैविक एवं एकीकृत नियंत्रण",
        "opt_chemical": "३. रासायनिक उपाय",
        "opt_additional": "४. अतिरिक्त जानकारी एवं निगरानी",
        "safe_use_notice": "महाराष्ट्र कृषि विभाग और CIBRC दिशानिर्देशों का कड़ाई से पालन करें।",
        "waiting_period_label": "कटाई प्रतीक्षा अवधि (PHI)",
        "follow_up_date_label": "अनुशंसित अगली जांच",
        "need_help_title": "कृषि विशेषज्ञ का मार्गदर्शन चाहिए?",
        "need_help_desc": "तालुका कृषि अधिकारी अथवा कृषि विज्ञान केंद्र से संपर्क करें।",

        # Navigation & Section Titles
        "nav_my_fields": "मेरे खेत",
        "nav_treatment_advisory": "उपचार सलाह",
        "nav_weather_risk": "मौसम और जोखिम",
        "nav_pest_alerts": "निगरानी बुलेटिन",
        "nav_hotspot_map": "हॉटस्पॉट नक्शा",
        "nav_smart_traps": "स्मार्ट ट्रैप और सेंसर",
        "nav_main_menu": "मुख्य नेविगेशन",
        "nav_officials_section": "विशेषज्ञ और प्रशासन",

        # Subtitles
        "fields_subtitle": "खेत के भूखंड, फसल वृद्धि अवस्था, सिंचाई और रोग निगरानी का प्रबंधन करें।",
        "advisory_subtitle": "बेहतर फसल स्वास्थ्य के लिए व्यक्तिगत और स्थान-विशिष्ट सिफारिशें।",
        "alerts_subtitle": "कृषि विभाग और राज्य विश्वविद्यालयों द्वारा जारी वास्तविक समय तालुका-स्तरीय कीट और रोग अलर्ट।",
        "weather_subtitle": "सूक्ष्म-जलवायु जानकारी, छिड़काव उपयुक्तता सूचकांक और रोग अनुकूलता मॉडल।",
        "hotspots_subtitle": "किसानों के निदान और सत्यापित मामलों पर आधारित इंटरेक्टिव नक्शा।",
        "expert_subtitle": "एआई फसल निदान की समीक्षा और पुष्टि करें, उपचार सुझाएं और मामलों की जांच करें।",
        "officer_subtitle": "जिला और तालुका स्तर पर कीट प्रकोप, रोग प्रसार विश्लेषण और आपातकालीन सलाह।",
        "sensors_subtitle": "स्मार्ट फेरोमोन ट्रैप, मिट्टी जांच उपकरण और सेंसर से लाइव डेटा।",

        # Diagnose Page Elements
        "page_diagnose_title": "एआई फसल स्वास्थ्य निदान और उपचार",
        "page_diagnose_subtitle": "विशेषज्ञों की सिफारिशों के साथ त्वरित रोग और कीट पहचान के लिए फसल की स्पष्ट तस्वीर अपलोड करें।",
        "awaiting_scan_title": "निदान परिणाम यहां दिखाई देंगे",
        "awaiting_scan_sub": "बाईं ओर समर्थित फसल चुनें, स्पष्ट पत्ती फोटो अपलोड करें और 'एआई फसल स्वास्थ्य निदान' पर क्लिक करें।",
        "btn_choose_gallery": "गैलरी से चुनें",
        "btn_take_photo": "फोटो खींचें",
        "btn_run_ai_diagnosis": "एआई फसल स्वास्थ्य निदान चलाएं",
        "try_sample_specimens": "नमूना पत्ती के नमूने देखें:",
        "step2_select_stage": "२. फसल वृद्धि अवस्था",
        "step3_select_location": "३. खेत और स्थान",
        "step4_upload_photo": "४. पत्ती का फोटो अपलोड करें",
        "drag_drop_title": "डिवाइस से चुनने के लिए यहां टैप करें या फोटो खींचें",
        "drag_drop_sub": "JPEG, PNG, WEBP प्रारूप समर्थित (अधिकतम १५ MB)",

        # Labels & Metrics
        "label_district": "जिला",
        "label_taluka": "तालुका",
        "label_village": "गांव / क्षेत्र",
        "metric_confidence": "एआई सटीकता",
        "metric_damage": "पत्ती का नुकसान",
        "metric_severity": "गंभीरता स्तर",

        # Dashboard & Action Buttons
        "disease_risk_forecast": "७-दिवसीय रोग जोखिम पूर्वानुमान",
        "pest_outbreak_alerts": "कीट प्रकोप अलर्ट",
        "forecast_details": "पूर्वानुमान विवरण",
        "all_alerts": "सभी अलर्ट",
        "kpi_my_fields": "मेरे खेत",
        "kpi_weather": "मौसम",
        "btn_diagnose_now": "अभी निदान शुरू करें",
        "btn_view_alerts": "निगरानी बुलेटिन",
        "btn_weather": "मौसम और छिड़काव सलाह",
        "modal_auth_title": "साइन इन / पंजीकरण",
        "label_fullname": "पूरा नाम",
        "label_password": "पासवर्ड",

        # Treatment Advisory Tab & Cards
        "adv_plan_badge": "अनुशंसित एकीकृत कीट प्रबंधन (IPM) योजना",
        "adv_rec_source": "सिफारिश स्रोत:",
        "adv_source_guidelines": "महात्मा फुले कृषि विश्वविद्यालय राहुरी और CIBRC दिशानिर्देश",
        "adv_card1_title": "१. त्वरित स्वच्छता और कृषि क्रियाएं",
        "adv_card1_sub": "त्वरित कार्रवाई और खेत की स्वच्छता",
        "adv_card2_title": "२. जैविक और पर्यावरण अनुकूल नियंत्रण",
        "adv_card2_sub": "जैविक और जैव-कीटनाशक उपाय",
        "adv_card3_title": "३. अनुमोदित रासायनिक नियंत्रण (सीमा-आधारित)",
        "adv_card3_sub": "सुरक्षित प्रतीक्षा अवधि के साथ रासायनिक नियंत्रण",
        "adv_card4_title": "४. फसल वृद्धि अवस्था निगरानी और अनुवर्ती कार्रवाई",
        "adv_card4_sub": "वृद्धि अवस्था सावधानियां और अनुवर्ती समयसीमा",
        "adv_cultural_practice_label": "कृषि पद्धति:",
        "adv_safe_pollinators": "लाभकारी परागणकों और मधुमक्खियों के लिए सुरक्षित।",
        "adv_phi_label": "कटाई पूर्व प्रतीक्षा अवधि (PHI): १४ दिन",
        "adv_cibrc_title": "CIBRC पंजीकृत कीटनाशक सत्यापन",
        "adv_cibrc_sub": "केंद्रीय कीटनाशक बोर्ड अनुमोदन, खुराक और प्रतीक्षा अवधि सत्यापित करने के लिए व्यापारिक नाम दर्ज करें:",
        "adv_cibrc_placeholder": "उदा. कोराजन, नेटिवो, एमिस्टार टॉप...",
        "btn_verify": "सत्यापित करें",
        "btn_submit_followup_photo": "अनुवर्ती फोटो भेजें",

        # Weather Indices
        "weather_spray_index": "छिड़काव उपयुक्तता सूचकांक",
        "weather_evapo_index": "वाष्पीकरण और ताप तनाव",
        "label_weather_advisory": "मौसम सलाह:",

        # Farm Cards
        "farm_active": "सक्रिय खेत",
        "farm_primary_crop": "मुख्य फसल",
        "farm_area": "क्षेत्रफल",
        "farm_acres": "एकड़",
        "farm_irrigation": "सिंचाई",
        "farm_drip": "ड्रिप सिंचाई",
        "farm_state": "राज्य",
        "farm_surveillance": "निगरानी सक्रिय",
        "farm_check_health": "फसल स्वास्थ्य जांचें",

        # Work History & Audit Modal
        "work_history_title": "उपयोगकर्ता गतिविधि और कार्य इतिहास लॉग",
        "work_history_subtitle": "उपयोगकर्ता लॉगिन, खोज, वॉयस परामर्श और फसल निदान का पूरा ऑडिट रिकॉर्ड।",
        "btn_close": "बंद करें",

        # Additional Advisory & Section Elements
        "adv_safety_label": "सुरक्षा सावधानी:",
        "adv_safety_text": "सुरक्षा: मानक पीपीई किट पहनें। हवा की विपरीत दिशा में कभी भी छिड़काव न करें।",
        "adv_phi_warning": "गलत या अनावश्यक छिड़काव से फसल को नुकसान और आर्थिक हानि हो सकती है।",
        "btn_print_advisory": "सलाह प्रिंट करें",
        "btn_share_whatsapp": "व्हाट्सएप पर साझा करें",
        "advisory_empty_title": "अभी तक कोई फसल निदान शुरू नहीं हुआ है",
        "advisory_empty_sub": "आपने अभी तक कोई फसल स्वास्थ्य निदान नहीं चलाया है। प्रमाणित एकीकृत कीट प्रबंधन (IPM) उपचार योजना तैयार करने के लिए फसल स्वास्थ्य निदान अनुभाग में पत्ती की तस्वीर अपलोड या स्कैन करें।",
        "btn_start_diagnosis_now": "अभी फसल निदान शुरू करें",
        "btn_return_dashboard": "डैशबोर्ड पर वापस जाएं",
        "weather_fungal_index": "फफूंद बीजाणु अंकुरण सूचकांक",
        "weather_pest_index": "कीट वृद्धि दर",
        "weather_wind_high_advice": "हवा की गति अधिक ({wind} किमी/घंटा) या वर्षा दर्ज की गई। अभी छिड़काव करने से बचें।",
        "weather_wind_optimal_advice": "हवा की गति ({wind} किमी/घंटा) अनुकूल है। सुबह के समय छिड़काव करना उपयुक्त रहेगा।",
        "farm_portfolio_title": "मेरे खेत (फार्म फील्ड पोर्टफोलियो)",
        "farm_register_new": "नया खेत पंजीकृत करें",
        "farm_no_registered": "अभी तक कोई खेत पंजीकृत नहीं है",
        "farm_register_sub": "स्वचालित फसल स्वास्थ्य निगरानी शुरू करने के लिए अपने खेत के भूखंड पंजीकृत करें।",
        "btn_register_first_farm": "पहला खेत पंजीकृत करें",
        "log_login": "लॉग इन",
        "log_logout": "लॉग आउट",
        "log_search": "खोज",
        "log_diagnosis": "फसल निदान",
        "log_diagnosis_rejected": "निदान अस्वीकृत",
        "log_voice_query": "वॉयस परामर्श",
        "log_language_change": "भाषा परिवर्तन",
        "log_view_advisory": "उपचार सलाह देखी",
        "log_completed_action": "कार्रवाई पूरी हुई",
        "log_loading": "गतिविधि लॉग लोड हो रहे हैं...",
        "log_empty": "इस खाते के लिए अभी कोई गतिविधि दर्ज नहीं है।"
    }
}


# Common Advisory Phrases & Recommendations Translation Dictionary
ADVISORY_PHRASE_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Unknown / General Advisory
    "DO NOT APPLY PESTICIDES OR CHEMICAL CONCOCTIONS. Take clear photographs of upper and lower leaf surfaces, stem, and whole plant.": {
        "en": "DO NOT APPLY PESTICIDES OR CHEMICAL CONCOCTIONS. Take clear photographs of upper and lower leaf surfaces, stem, and whole plant.",
        "mr": "कीटकनाशके किंवा रासायनिक मिश्रणे फवारू नका. पानांची वरची व खालची बाजू, खोड आणि संपूर्ण रोपाचे स्पष्ट फोटो काढा.",
        "hi": "कीटनाशक या रासायनिक मिश्रण का छिड़काव न करें। पत्ती की ऊपरी और निचली सतह, तना और पूरे पौधे की स्पष्ट तस्वीर लें।"
    },
    "Observe whether symptoms are localized to a single plant or widespread along irrigation channels.": {
        "en": "Observe whether symptoms are localized to a single plant or widespread along irrigation channels.",
        "mr": "लक्षणे एकाच रोपापुरती मर्यादित आहेत की पाटाच्या पाण्यासोबत पसरली आहेत याचे निरीक्षण करा.",
        "hi": "देखें कि लक्षण केवल एक पौधे तक सीमित हैं या सिंचाई की नालियों के साथ फैले हुए हैं।"
    },
    "Note down recent fertilization, pesticide sprays, irrigation dates, and weather anomalies.": {
        "en": "Note down recent fertilization, pesticide sprays, irrigation dates, and weather anomalies.",
        "mr": "अलिकडच्या खत वापराची, औषध फवारणीची, पाण्याच्या पाळीची आणि हवामानातील बदलांची नोंद ठेवा.",
        "hi": "हालिया खाद, कीटनाशक छिड़काव, सिंचाई और मौसम बदलाव का रिकॉर्ड नोट करें।"
    },
    "Tag the affected plant with a flag for field officer inspection.": {
        "en": "Tag the affected plant with a flag for field officer inspection.",
        "mr": "कृषी अधिकाऱ्यांच्या तपासणीसाठी बाधित रोपाला खूण किंवा निशाण लावा.",
        "hi": "कृषि अधिकारी के निरीक्षण के लिए प्रभावित पौधे पर निशान या झंडी लगाएं।"
    },
    "Collect suspected specimen in clean, dry paper envelope for laboratory inspection.": {
        "en": "Collect suspected specimen in clean, dry paper envelope for laboratory inspection.",
        "mr": "संशयित नमुना प्रयोगशाळा तपासणीसाठी स्वच्छ, कोरड्या कागदी पाकिटात गोळा करा.",
        "hi": "संदिग्ध नमूने को प्रयोगशाला जांच के लिए साफ, सूखे कागज के लिफाफे में एकत्र करें।"
    },
    "Strictly withhold pesticide spraying until agricultural university / KVK expert provides prescription.": {
        "en": "Strictly withhold pesticide spraying until agricultural university / KVK expert provides prescription.",
        "mr": "कृषी विद्यापीठ किंवा केव्हीके तज्ज्ञांचे औषधोपचार मार्गदर्शन मिळेपर्यंत कीटकनाशक फवारणी थांबवा.",
        "hi": "कृषि विश्वविद्यालय या केवीके विशेषज्ञ की सलाह मिलने तक कीटनाशक छिड़काव पूरी तरह रोकें।"
    },
    "Misidentified spraying risks severe crop phytotoxicity and financial loss.": {
        "en": "Misidentified spraying risks severe crop phytotoxicity and financial loss.",
        "mr": "चुकीच्या औषध फवारणीमुळे पिकांचे गंभीर नुकसान (फायटोटॉक्सिसिटी) आणि आर्थिक हानी होऊ शकते.",
        "hi": "गलत छिड़काव से फसल को गंभीर नुकसान और आर्थिक हानि हो सकती है।"
    },
    "Immediate escalation to Agricultural Officer / Krishi Vigyan Kendra.": {
        "en": "Immediate escalation to Agricultural Officer / Krishi Vigyan Kendra.",
        "mr": "तालुका कृषी अधिकारी किंवा कृषी विज्ञान केंद्राशी त्वरित संपर्क साधा.",
        "hi": "तुरंत तालुका कृषि अधिकारी अथवा कृषि विज्ञान केंद्र से संपर्क करें।"
    },
    # Fall Armyworm / Insects
    "Handpick and destroy visible larvae in whorls. Clean field borders and eradicate alternative grass weed hosts.": {
        "en": "Handpick and destroy visible larvae in whorls. Clean field borders and eradicate alternative grass weed hosts.",
        "mr": "कोंबामधील (पोंगा) अळ्या वेचून नष्ट करा. शेताचे बांध स्वच्छ ठेवा आणि गवताळ तणे नष्ट करा.",
        "hi": "पत्तियों के पोंगे से दिखने वाली इल्लियों को चुनकर नष्ट करें। खेत की मेड़ें साफ रखें और खरपतवार हटाएं।"
    },
    "Carry out deep inter-cultivation to expose pupae to natural predators and sunlight.": {
        "en": "Carry out deep inter-cultivation to expose pupae to natural predators and sunlight.",
        "mr": "कोश उन्हात उघडे पडून नष्ट होण्यासाठी आणि पक्ष्यांना दिसण्यासाठी शेतात खोल आंतरमशागत करा.",
        "hi": "कोशों को धूप और पक्षियों के संपर्क में लाने के लिए गहरी निराई-गुड़ाई करें।"
    },
    "Spray 5% Neem Seed Kernel Extract (NSKE) or Azadirachtin 10,000 ppm @ 2 ml/L water. Apply entomopathogenic fungus Metarhizium rileyi @ 5 g/L into whorls.": {
        "en": "Spray 5% Neem Seed Kernel Extract (NSKE) or Azadirachtin 10,000 ppm @ 2 ml/L water. Apply entomopathogenic fungus Metarhizium rileyi @ 5 g/L into whorls.",
        "mr": "५% निंबोळी अर्क (NSKE) किंवा अझाडिरॅक्टिन १०,००० पीपीएम @ २ मिली/लिटर फवारा. मेटारायझियम रिलेयी ही जैविक बुरशी @ ५ ग्रॅम/लिटर पोंग्यात टाका.",
        "hi": "5% नीम बीज अर्क (एनएसकेई) या एजाडिराक्टिन 10,000 पीपीएम @ 2 मिली/लीटर का छिड़काव करें। मेटाराइजियम रिलेई @ 5 ग्राम/लीटर पोंगे में डालें।"
    },
    "If whorl infestation exceeds 10%: Apply Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L directly into whorls using a knapsack sprayer.": {
        "en": "If whorl infestation exceeds 10%: Apply Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L directly into whorls using a knapsack sprayer.",
        "mr": "१०% पेक्षा जास्त पोंग्यांमध्ये प्रादुर्भाव आढळल्यास: क्लोराँट्रानिलीप्रोल १८.५% एससी @ ०.४ मिली/लिटर किंवा स्पिनोटोरम ११.७% एससी @ ०.५ मिली/लिटर थेट पोंग्यात फवारा.",
        "hi": "यदि 10% से अधिक पोंगे प्रभावित हों: क्लोरेंट्रानिलिप्रोल 18.5% एससी @ 0.4 मिली/लीटर या स्पिनेटोरम 11.7% एससी @ 0.5 मिली/लीटर सीधे पोंगे में छिड़कें।"
    },
    "Safety: Wear standard PPE kit. Never spray against prevailing wind directions.": {
        "en": "Safety: Wear standard PPE kit. Never spray against prevailing wind directions.",
        "mr": "सुरक्षितता: प्रमाणित PPE किट वापरा. वाऱ्याच्या विरुद्ध दिशेने कधीही फवारणी करू नका.",
        "hi": "सुरक्षा: मानक पीपीई किट पहनें। हवा की विपरीत दिशा में कभी भी छिड़काव न करें।"
    },
    # Healthy Foliage
    "Continue regular crop scouting every 7 days; zero synthetic pesticide application required.": {
        "en": "Continue regular crop scouting every 7 days; zero synthetic pesticide application required.",
        "mr": "दर ७ दिवसांनी नियमित शेत पाहणी सुरू ठेवा; कोणत्याही रासायनिक कीटकनाशकाची गरज नाही.",
        "hi": "हर 7 दिनों में नियमित खेत निरीक्षण जारी रखें; किसी भी रासायनिक कीटनाशक की आवश्यकता नहीं है।"
    },
    "Maintain balanced nutrition with bio-fertilizers (Azotobacter, PSB).": {
        "en": "Maintain balanced nutrition with bio-fertilizers (Azotobacter, PSB).",
        "mr": "जिवाणू खते (ॲझोटोबॅक्टर, पीएसबी) वापरून संतुलित पोषण व्यवस्थापन ठेवा.",
        "hi": "जैव उर्वरकों (एजोटोबैक्टर, पीएसबी) के साथ संतुलित पोषण बनाए रखें।"
    },
    "Avoid unnecessary chemical spraying to preserve beneficial insects and pollinators.": {
        "en": "Avoid unnecessary chemical spraying to preserve beneficial insects and pollinators.",
        "mr": "उपयुक्त मित्रकीटक व मधमाश्यांचे रक्षण करण्यासाठी विनाकारण रासायनिक फवारणी टाळा.",
        "hi": "मित्र कीटों और परागणकों के संरक्षण के लिए अनावश्यक रासायनिक छिड़काव से बचें।"
    },
    # Rust & Blight Common
    "Spray Propiconazole 25 EC @ 1 ml/L or Mancozeb 75 WP @ 2.5 g/L at the first appearance of pustules.": {
        "en": "Spray Propiconazole 25 EC @ 1 ml/L or Mancozeb 75 WP @ 2.5 g/L at the first appearance of pustules.",
        "mr": "तांबेरा रोगाचे ठिपके दिसताच प्रोपिकोनाझोल २५ ईसी @ १ मिली/लिटर किंवा मॅन्कोझेब ७५ डब्ल्यूपी @ २.५ ग्रॅम/लिटर फवारा.",
        "hi": "रस्ट के धब्बे दिखते ही प्रोपिकोनाजोल 25 ईसी @ 1 मिली/लीटर या मैंकोजेब 75 डब्ल्यूपी @ 2.5 ग्राम/लीटर का छिड़काव करें।"
    },
    "Apply Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L for systemic curative protection.": {
        "en": "Apply Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L for systemic curative protection.",
        "mr": "रोग नियंत्रणासाठी ॲझॉक्सीस्ट्रॉबिन १८.२% + डिफेनोकोनाझोल ११.४% एससी @ १ मिली/लिटर फवारा.",
        "hi": "प्रभावी रोग नियंत्रण के लिए एजोक्सीस्ट्रोबिन 18.2% + डिफेनोकोनाजोल 11.4% एससी @ 1 मिली/लीटर का छिड़काव करें।"
    }
}

# Crop Name Translations
CROP_NAME_MAP: Dict[str, Dict[str, str]] = {
    "maize": {"en": "Maize", "mr": "मका", "hi": "मक्का"},
    "corn": {"en": "Maize", "mr": "मका", "hi": "मक्का"},
    "tomato": {"en": "Tomato", "mr": "टोमॅटो", "hi": "टमाटर"},
    "soybean": {"en": "Soybean", "mr": "सोयाबीन", "hi": "सोयाबीन"},
    "cotton": {"en": "Cotton", "mr": "कापूस", "hi": "कपास"},
    "grape": {"en": "Grape", "mr": "द्राक्ष", "hi": "अंगूर"},
    "wheat": {"en": "Wheat", "mr": "गहू", "hi": "गेहूं"},
    "rice": {"en": "Rice", "mr": "भात / तांदूळ", "hi": "धान / चावल"},
    "sugarcane": {"en": "Sugarcane", "mr": "ऊस", "hi": "गन्ना"},
    "onion": {"en": "Onion", "mr": "कांदा", "hi": "प्याज"},
    "potato": {"en": "Potato", "mr": "बटाटा", "hi": "आलू"},
    "cucumber": {"en": "Cucumber", "mr": "काकडी", "hi": "खीरा"},
    "chili": {"en": "Chili", "mr": "मिरची", "hi": "मिर्च"},
    "banana": {"en": "Banana", "mr": "केळी", "hi": "केला"},
    "citrus": {"en": "Citrus", "mr": "संत्रा / मोसंबी", "hi": "नींबू / संतरा"},
    "cherry": {"en": "Cherry", "mr": "चेरी", "hi": "चेरी"},
    "strawberry": {"en": "Strawberry", "mr": "स्ट्रॉबेरी", "hi": "स्ट्रॉबेरी"},
    "apple": {"en": "Apple", "mr": "सफरचंद", "hi": "सेब"}
}

# Stage Name Translations
STAGE_NAME_MAP: Dict[str, Dict[str, str]] = {
    "vegetative": {"en": "Vegetative", "mr": "वानस्पतिक वाढ", "hi": "वानस्पतिक वृद्धि"},
    "flowering": {"en": "Flowering", "mr": "फुलोरा अवस्था", "hi": "फूल अवस्था"},
    "fruiting": {"en": "Fruiting", "mr": "फळधारणा अवस्था", "hi": "फल लगना"},
    "seedling": {"en": "Seedling", "mr": "रोप अवस्था", "hi": "पौध अवस्था"},
    "maturity": {"en": "Maturity", "mr": "परिपक्वता", "hi": "परिपक्वता"}
}

# Disease / Condition Name Translations
CONDITION_NAME_MAP: Dict[str, Dict[str, str]] = {
    "corn smut": {"en": "Corn Smut", "mr": "मका काजळी रोग", "hi": "मक्का कंडुवा रोग"},
    "corn_smut": {"en": "Corn Smut", "mr": "मका काजळी रोग", "hi": "मक्का कंडुवा रोग"},
    "fall armyworm": {"en": "Fall Armyworm", "mr": "लष्करी अळी", "hi": "फॉल आर्मीवर्म"},
    "corn common rust": {"en": "Corn Common Rust", "mr": "मका तांबेरा रोग", "hi": "मक्का रस्ट रोग"},
    "corn northern leaf blight": {"en": "Corn Northern Leaf Blight", "mr": "मका पानांवरील करपा", "hi": "मक्का पत्ती झुलसा"},
    "tomato early blight": {"en": "Tomato Early Blight", "mr": "टोमॅटो लवकर येणारा करपा", "hi": "टमाटर अगेती झुलसा"},
    "tomato late blight": {"en": "Tomato Late Blight", "mr": "टोमॅटो उशिरा येणारा करपा", "hi": "टमाटर पछेती झुलसा"},
    "tomato bacterial leaf spot": {"en": "Tomato Bacterial Leaf Spot", "mr": "टोमॅटो जिवाणूजन्य ठिपके", "hi": "टमाटर जीवाणु पत्ती धब्बा"},
    "soybean asian rust": {"en": "Soybean Asian Rust", "mr": "सोयाबीन तांबेरा रोग", "hi": "सोयाबीन गेरुआ रोग"},
    "cotton pink bollworm": {"en": "Cotton Pink Bollworm", "mr": "कापूस गुलाबी बोंडअळी", "hi": "कपास गुलाबी सुंडी"},
    "cotton bacterial blight": {"en": "Cotton Bacterial Blight", "mr": "कापूस जिवाणू करपा", "hi": "कपास जीवाणु झुलसा"},
    "grape downy mildew": {"en": "Grape Downy Mildew", "mr": "द्राक्ष केवडा रोग", "hi": "अंगूर डाउनी मिल्ड्यू"},
    "rice blast": {"en": "Rice Blast", "mr": "भात करपा रोग", "hi": "धान ब्लास्ट रोग"},
    "rice sheath blight": {"en": "Rice Sheath Blight", "mr": "भात कडा करपा", "hi": "धान शीथ ब्लाइट"},
    "healthy foliage": {"en": "Healthy Foliage", "mr": "निरोगी पाने", "hi": "स्वस्थ पत्तियां"},
    "unclassified condition": {"en": "Unclassified Condition", "mr": "अनाकलनीय लक्षणे (तज्ज्ञ तपासणी आवश्यक)", "hi": "अज्ञात लक्षण (विशेषज्ञ समीक्षा आवश्यक)"},
    "unknown_condition": {"en": "Unidentified Condition", "mr": "अनाकलनीय लक्षणे (तज्ज्ञ तपासणी आवश्यक)", "hi": "अज्ञात लक्षण (विशेषज्ञ समीक्षा आवश्यक)"}
}


def get_translation(key: str, lang: str = "mr") -> str:
    """Retrieves translation with fallback to English."""
    norm_lang = (lang or "mr").lower()
    lang_dict = TRANSLATIONS.get(norm_lang, TRANSLATIONS.get("en", {}))
    if key in lang_dict:
        return lang_dict[key]
    # Check phrase map
    if key in ADVISORY_PHRASE_TRANSLATIONS:
        return ADVISORY_PHRASE_TRANSLATIONS[key].get(norm_lang, key)
    return TRANSLATIONS.get("en", {}).get(key, key)


def translate_text(text: str, lang: str = "mr") -> str:
    """Translates any arbitrary sentence or term using full catalogs."""
    if not text:
        return text
    norm_lang = (lang or "mr").lower()
    if norm_lang == "en":
        return text
    trimmed = text.strip()
    if trimmed in ADVISORY_PHRASE_TRANSLATIONS:
        return ADVISORY_PHRASE_TRANSLATIONS[trimmed].get(norm_lang, trimmed)
    low = trimmed.lower()
    if low in CONDITION_NAME_MAP:
        return CONDITION_NAME_MAP[low].get(norm_lang, trimmed)
    if low in CROP_NAME_MAP:
        return CROP_NAME_MAP[low].get(norm_lang, trimmed)
    if low in STAGE_NAME_MAP:
        return STAGE_NAME_MAP[low].get(norm_lang, trimmed)
    return get_translation(trimmed, norm_lang)


def get_all_translations(lang: str = "mr") -> Dict[str, str]:
    """Returns complete catalog in requested language (mr, hi, en) with fallback and phrase lookups."""
    norm_lang = (lang or "mr").lower()
    base = dict(TRANSLATIONS.get("en", {}))
    if norm_lang in TRANSLATIONS and norm_lang != "en":
        base.update(TRANSLATIONS[norm_lang])
    # Also expose phrases and condition mappings so frontend can look them up directly by text
    for phrase, trans in ADVISORY_PHRASE_TRANSLATIONS.items():
        base[phrase] = trans.get(norm_lang, phrase)
    for cond, trans in CONDITION_NAME_MAP.items():
        base[f"cond_{cond}"] = trans.get(norm_lang, cond)
    for crop, trans in CROP_NAME_MAP.items():
        base[f"crop_{crop}"] = trans.get(norm_lang, crop)
    return base



