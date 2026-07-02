from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.data.sample_cases import SAMPLE_CASES
from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.review_service import build_review_response

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def ui_preview() -> HTMLResponse:
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>TriageGuard Review UI</title>
  <style>
    body { font-family: Inter, system-ui, sans-serif; background: #f4f7fb; color: #111827; margin: 0; padding: 0; }
    header { background: #1f2937; color: white; padding: 1rem 1.5rem; }
    main { display: grid; gap: 1rem; padding: 1rem; max-width: 1200px; margin: 0 auto; }
    .panel { background: white; border-radius: 16px; box-shadow: 0 10px 30px rgba(15,23,42,.08); padding: 1rem; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    textarea { width: 100%; min-height: 220px; font-family: monospace; font-size: 0.95rem; border: 1px solid #d1d5db; border-radius: 0.75rem; padding: 0.75rem; resize: vertical; }
    button { border: none; background: #2563eb; color: white; padding: 0.85rem 1.25rem; font-size: 0.95rem; border-radius: 0.75rem; cursor: pointer; }
    button:disabled { opacity: 0.6; cursor: not-allowed; }
    select { width: 100%; border: 1px solid #d1d5db; border-radius: 0.75rem; padding: 0.75rem; }
    .diff-row { display: flex; justify-content: space-between; gap: 0.5rem; padding: 0.6rem 0; border-bottom: 1px solid #e5e7eb; }
    .diff-row:last-child { border-bottom: none; }
    .diff-key { color: #374151; font-weight: 600; width: 30%; }
    .diff-value { width: 35%; white-space: pre-wrap; }
    .diff-value.mismatch { background: #fee2e2; }
    .diff-value.match { background: #ecfdf5; }
  </style>
</head>
<body>
  <header>
    <h1>TriageGuard Review UI</h1>
    <p>Load a sample case, submit it to the review API, and inspect the decision plus record differences.</p>
  </header>
  <main>
    <section class="panel">
      <h2>Sample case</h2>
      <label for="sampleSelector">Choose a case:</label>
      <select id="sampleSelector"></select>
      <div style="margin-top:1rem; display:flex; gap:0.75rem; flex-wrap:wrap;">
        <button id="loadSampleBtn">Load sample</button>
        <button id="reviewCaseBtn">Review case</button>
      </div>
    </section>

    <div class="grid-2">
      <section class="panel">
        <h2>Request payload</h2>
        <textarea id="requestJson" spellcheck="false"></textarea>
      </section>
      <section class="panel">
        <h2>Response output</h2>
        <textarea id="responseJson" spellcheck="false" readonly></textarea>
      </section>
    </div>

    <section class="panel">
      <h2>Field differences</h2>
      <div id="diffContainer"></div>
    </section>
  </main>

  <script>
    const sampleSelector = document.getElementById('sampleSelector');
    const requestJson = document.getElementById('requestJson');
    const responseJson = document.getElementById('responseJson');
    const diffContainer = document.getElementById('diffContainer');
    const loadSampleBtn = document.getElementById('loadSampleBtn');
    const reviewCaseBtn = document.getElementById('reviewCaseBtn');
    let samples = [];

    async function fetchSamples() {
      const response = await fetch('/sample-cases');
      samples = await response.json();
      sampleSelector.innerHTML = samples.map((item, index) => `<option value="${index}">${item.case_id} — ${item.exception_type}</option>`).join('');
      loadSample();
    }

    function loadSample() {
      const selected = samples[sampleSelector.value] || samples[0];
      requestJson.value = JSON.stringify(selected, null, 2);
      responseJson.value = '';
      renderDiff(selected);
    }

    function renderDiff(caseData) {
      const profile = caseData.customer_profile || {};
      const source = caseData.source_record || {};
      const fields = [
        { label: 'Full name', key: 'full_name' },
        { label: 'Date of birth', key: 'date_of_birth' },
        { label: 'Address', key: 'address' },
        { label: 'Account last four', key: 'account_last_four' },
      ];
      diffContainer.innerHTML = fields.map(({ label, key }) => {
        const expected = profile[key] ?? '';
        const actual = key === 'full_name' ? source.name || '' : source[key] || '';
        const isMatch = expected === actual;
        return `
          <div class="diff-row">
            <div class="diff-key">${label}</div>
            <div class="diff-value ${isMatch ? 'match' : 'mismatch'}">${expected}</div>
            <div class="diff-value ${isMatch ? 'match' : 'mismatch'}">${actual}</div>
          </div>
        `;
      }).join('');
    }

    async function reviewCase() {
      reviewCaseBtn.disabled = true;
      try {
        const requestBody = JSON.parse(requestJson.value);
        const response = await fetch('/review', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });
        const result = await response.json();
        responseJson.value = JSON.stringify(result, null, 2);
      } catch (error) {
        responseJson.value = 'Error: ' + (error.message || error);
      } finally {
        reviewCaseBtn.disabled = false;
      }
    }

    sampleSelector.addEventListener('change', loadSample);
    loadSampleBtn.addEventListener('click', loadSample);
    reviewCaseBtn.addEventListener('click', reviewCase);
    fetchSamples();
  </script>
</body>
</html>
    """
    return HTMLResponse(content=html)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/review", response_model=ReviewResponse)
def review_case(case: ReviewRequest) -> ReviewResponse:
    return build_review_response(case)


@router.get("/sample-cases")
def get_sample_cases() -> list[dict]:
    return SAMPLE_CASES
