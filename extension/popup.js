document.addEventListener('DOMContentLoaded', function () {
    const verifyBtn = document.getElementById('verify-btn');
    const claimInput = document.getElementById('claim-input');
    const loadingDiv = document.getElementById('loading');
    const resultSection = document.getElementById('result-section');
    const errorMsg = document.getElementById('error-msg');
    const detailsBtn = document.getElementById('details-btn');
    const detailsSection = document.getElementById('details-section');

    // Try to populate input with page title
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        if (tabs[0] && tabs[0].title) {
            claimInput.value = tabs[0].title;
        }
    });

    verifyBtn.addEventListener('click', async function () {
        const claim = claimInput.value.trim();
        if (!claim) return;

        // UI Reset
        errorMsg.classList.add('hidden');
        resultSection.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        verifyBtn.disabled = true;

        try {
            const response = await fetch('http://localhost:8001/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ claim: claim })
            });

            if (!response.ok) {
                throw new Error('API Error: ' + response.statusText);
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            errorMsg.textContent = error.message || 'Failed to connect to MumbAI backend.';
            errorMsg.classList.remove('hidden');
        } finally {
            loadingDiv.classList.add('hidden');
            verifyBtn.disabled = false;
        }
    });

    detailsBtn.addEventListener('click', function () {
        detailsSection.classList.toggle('hidden');
        detailsBtn.textContent = detailsSection.classList.contains('hidden') ? 'View Agent Workflow' : 'Hide Details';
    });

    function displayResults(data) {
        resultSection.classList.remove('hidden');

        // Verdict
        const verdictEl = document.getElementById('verdict');
        verdictEl.textContent = data.verdict;
        verdictEl.className = data.verdict.toLowerCase(); // for styling (true/false/uncertain)

        // Confidence
        document.getElementById('confidence-score').textContent = (data.confidence * 100).toFixed(0) + '%';
        document.getElementById('confidence-bar').style.width = (data.confidence * 100) + '%';

        // Explanation
        document.getElementById('explanation').textContent = data.explanation;

        // Evidence
        const evidenceList = document.getElementById('evidence-list');
        evidenceList.innerHTML = '';
        data.evidence.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `[${item.label}] ${item.sentence} (${(item.score * 100).toFixed(0)}%)`;
            evidenceList.appendChild(li);
        });

        // Credibility
        const credList = document.getElementById('credibility-list');
        credList.innerHTML = '';
        data.credibility_report.forEach(item => {
            const li = document.createElement('li');
            const link = document.createElement('a');
            link.href = item.url;
            link.target = '_blank';
            link.textContent = item.domain;
            link.className = 'source-link';

            const statusSpan = document.createElement('span');
            statusSpan.textContent = ` • ${item.status}`;
            statusSpan.className = `status-${item.status.toLowerCase()}`;

            li.appendChild(link);
            li.appendChild(statusSpan);
            credList.appendChild(li);
        });
    }
});
