# Benchmark test documents

A set of longer, realistically formatted documents for testing the AI Document
Red Alert detector across formats (DOCX, text PDF, scanned/image PDF), languages
(English, Gujarati) and risk types.

**These are SYNTHETIC benchmark documents.** Every document carries a visible
"SYNTHETIC BENCHMARK — NOT A GENUINE DOCUMENT" banner on every page (and a
diagonal "SYNTHETIC SAMPLE" watermark on the PDFs). All people, companies,
banks, account numbers, Aadhaar/PAN numbers and events are fictional. The
Aadhaar numbers are format-valid (correct Verhoeff check digit) but do not
belong to any real person. These files are for detector testing only and are
not real documents.

## What each file exercises, and how the detector scored it

| # | File | Format | Scenario | Expected / actual |
|---|------|--------|----------|-------------------|
| 01 | Infosec_Policy_SPW | DOCX (3 pp.) | A normal IT policy with a **buried off-book-payments clause** and an annexure of staff Aadhaar/PAN/salary accounts and admin passwords | **Red (100)** — policy violation + sensitive data |
| 02 | Travel_Expense_Policy_AEC | DOCX (2 pp.) | An ordinary travel & expense policy | **Yellow (59)** — borderline; see note below |
| 03 | Settlement_Demand_Letter (scanned) | **Image-only PDF** | An extortion / "settlement" demand letter — tests **OCR** | **Red (100)** — threats, bank/UPI details |
| 04 | Intimidation_Letter_NoKeywords | DOCX (2 pp.) | A veiled intimidation letter with **no explicit threat keywords** — tests the **AI meaning-model** | **Yellow (70)** — AI reads threat 0.92 / policy 0.77 |
| 05 | Recovery_Notice_Gujarati | DOCX (3 pp.) | A **Gujarati** debt-recovery-cum-threat notice with Aadhaar/PAN | **Red (100)** — Gujarati threats + sensitive data |
| 06 | Divorce_MoU_RiskyClauses | PDF (3 pp.) | A mutual-consent divorce settlement with **one-sided / risky clauses** (blank signed cheques, total waiver, ₹25 lakh penalty) and personal data | **Red (100)** — sensitive data, risky clauses |
| 07 | Offer_Letter_NLT | DOCX (2 pp.) | An HR appointment letter | **Yellow (64)** — borderline; see note below |
| 08 | Internal_Memo_OffBook_Payment | DOCX (2 pp.) | An internal memo approving an **off-the-books vendor payment** (fraud/collusion) | **Red (100)** — policy violation + bank details |
| 09 | Office_Circular_Holidays | DOCX (2 pp.) | A plain festival-holiday / office-timings circular | **Green (0)** — true negative control |

## Note on the "borderline" documents (02 and 07)

The travel policy and offer letter were intended as clean controls but score
Yellow, because the detector currently **over-flags formal HR/legal language**:
the AI meaning-model reads routine terms (notice period, verification,
misconduct, "not permitted") as mild threat, and words like "bank account"
count as risky keywords. This is a real property of the detector worth being
aware of — document 09 is the dependable Green true-negative.

## Not included

A bank phishing / credential-harvesting notice was deliberately **not** created:
a convincing document that asks for passwords/OTPs would work as a real phishing
attack. If you need to exercise the "request for passwords/PINs" signal, write a
short mock sample yourself or mark one clearly as a drill.
