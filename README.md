# triageguard

Financial Exception Review Agent — Build Plan
1. Project goal

Build a deployable AI agent that reviews financial-operation exceptions against internal policy, recommends an action, assigns risk and confidence, escalates uncertain cases, and stores a complete audit trail.

2. MVP use case

Start with:

KYC identity mismatch review

The agent compares a customer record with a source record and decides whether the discrepancy is minor, requires additional documentation, should be rejected, or must be escalated.

3. User story

As a financial operations analyst, I want an AI system to review customer identity mismatches against internal policy so that straightforward cases are resolved faster and risky cases are escalated with clear evidence.

4. Input

The user submits:

Case ID
Exception type
Customer name
Date of birth
Address
Account last four digits
Source-system values
Optional notes
5. Output

The system returns:

Decision
Risk level
Confidence score
Explanation
Required next action
Policy citation
Human-review flag
6. Decision options
Decision	Meaning
Auto-approve	Minor, policy-allowed mismatch
Request documents	More evidence is required
Reject	Clear policy failure
Escalate	High-risk or ambiguous case
Close duplicate	Case already exists or was resolved
7. Agent workflow
Step	Function
1. Intake	Validate the case using Pydantic
2. Classification	Confirm the exception category
3. Retrieval	Fetch relevant policy sections
4. Comparison	Identify matching and mismatching fields
5. Decision	Generate a structured recommendation
6. Guardrail	Prevent automatic action on risky cases
7. Evaluation	Score confidence and evidence coverage
8. Audit	Save input, policy evidence, output and timestamps
8. LangGraph nodes
START
  ↓
validate_case
  ↓
classify_exception
  ↓
retrieve_policy
  ↓
compare_records
  ↓
generate_decision
  ↓
apply_guardrails
  ↓
evaluate_output
  ↓
save_audit_log
  ↓
END
9. Tech stack
Layer	Technology
Backend	FastAPI
Workflow	LangGraph
Validation	Pydantic
LLM	OpenAI or Anthropic
Database	Supabase Postgres
Retrieval	Supabase pgvector or keyword search
Frontend	Streamlit
Observability	Langfuse
Testing	Pytest
Deployment	Railway
10. Database tables
cases
case_id
exception_type
customer_record
source_record
status
created_at
decisions
case_id
decision
risk_level
confidence
explanation
required_action
human_review_required
created_at
policy_chunks
policy_id
section
content
embedding
audit_logs
case_id
node_name
input_payload
output_payload
latency
error
timestamp
11. Policy documents

Create three mock policies:

Policy	Coverage
KYC-01	Acceptable name variations
KYC-02	Date-of-birth mismatches
KYC-03	Address verification and required documents
12. Guardrails

The system must always require human review when:

Date of birth does not match
Account identifiers do not match
More than one major field differs
Confidence is below 0.80
Fraud indicators appear
No relevant policy evidence is retrieved
13. Evaluation criteria
Metric	Target
Valid JSON output	100%
Correct policy citation	90%+
Correct escalation	90%+
Unsupported claims	0
Response latency	Under 5 seconds
14. Golden test cases

Create at least 10 cases:

Exact match
Middle-name variation
Abbreviated address
Changed city
Date-of-birth mismatch
Account-number mismatch
Missing address
Duplicate case
Multiple mismatches
Low-confidence ambiguous case