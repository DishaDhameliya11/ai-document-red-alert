from app.ai.anomaly_detector import detect_abnormal_patterns
from app.ai.heatmap_generator import generate_document_heatmap
from app.ai.indian_compliance_detector import detect_indian_compliance_data
from app.ai.keyword_detector import detect_risky_keywords
from app.ai.policy_violation_detector import detect_policy_violations
from app.ai.risk_report_generator import generate_risk_report
from app.ai.risk_scoring import calculate_risk_result
from app.ai.sensitive_info_detector import detect_sensitive_information
from app.ai.summarizer import generate_basic_summary
from app.ai.tampering_detector import detect_tampering_suspicion
from app.ai.threat_detector import detect_threats

def analyze_document_text(text: str) -> dict:
    keyword_analysis = detect_risky_keywords(text)
    sensitive_info_analysis = detect_sensitive_information(text)
    policy_violation_analysis = detect_policy_violations(text)
    threat_analysis = detect_threats(text)
    anomaly_analysis = detect_abnormal_patterns(text)
    indian_compliance_analysis = detect_indian_compliance_data(text)
    tampering_analysis = detect_tampering_suspicion(text)

    document_heatmap = generate_document_heatmap(
        keyword_analysis=keyword_analysis,
        sensitive_info_analysis=sensitive_info_analysis,
        policy_violation_analysis=policy_violation_analysis,
        threat_analysis=threat_analysis,
    )

    risk_result = calculate_risk_result(
        keyword_risk_score=keyword_analysis["keyword_risk_score"],
        sensitive_risk_score=sensitive_info_analysis["sensitive_risk_score"],
        policy_risk_score=policy_violation_analysis["policy_risk_score"],
        threat_risk_score=threat_analysis["threat_risk_score"],
        anomaly_risk_score=anomaly_analysis["anomaly_risk_score"],
        compliance_risk_score=indian_compliance_analysis["compliance_risk_score"],
        tampering_risk_score=tampering_analysis["tampering_risk_score"],
    )

    risk_report = generate_risk_report(
        risk_analysis=risk_result,
        keyword_analysis=keyword_analysis,
        sensitive_info_analysis=sensitive_info_analysis,
        policy_violation_analysis=policy_violation_analysis,
        threat_analysis=threat_analysis,
        anomaly_analysis=anomaly_analysis,
        indian_compliance_analysis=indian_compliance_analysis,
    )

    summary = generate_basic_summary(text)

    return {
        "summary": summary,
        "keyword_analysis": keyword_analysis,
        "sensitive_info_analysis": sensitive_info_analysis,
        "policy_violation_analysis": policy_violation_analysis,
        "threat_analysis": threat_analysis,
        "risk_analysis": risk_result,
        "anomaly_analysis": anomaly_analysis,
        "risk_report": risk_report,
        "tampering_analysis": tampering_analysis,
        "indian_compliance_analysis": indian_compliance_analysis,
        "document_heatmap": document_heatmap,
    }