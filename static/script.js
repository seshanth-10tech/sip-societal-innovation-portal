let analyzedChallenge = null;

function setProblem(text) {
    const input = document.getElementById('problemInput');
    if (!input) return;
    input.value = text;
    input.focus();
    updateCharacterCount();
}

function updateCharacterCount() {
    const input = document.getElementById('problemInput');
    const count = document.getElementById('characterCount');
    if (input && count) count.textContent = `${input.value.length} / 1200`;
}

function showError(message) {
    const error = document.getElementById('formError');
    if (!error) return;
    error.textContent = message;
    error.hidden = false;
}

function clearError() {
    const error = document.getElementById('formError');
    if (error) { error.hidden = true; error.textContent = ''; }
}

async function sendProblem() {
    const input = document.getElementById('problemInput');
    const button = document.getElementById('sendButton');
    if (!input || !button) return;
    const problem = input.value.trim();
    clearError();
    if (!problem) { showError('Add a few details about the challenge before continuing.'); input.focus(); return; }
    if (problem.length < 12) { showError('A little more detail will help us find the right team.'); input.focus(); return; }

    button.disabled = true;
    button.querySelector('span').textContent = 'Finding a good match…';
    const progress = document.getElementById('analysisProgress');
    if (progress) {
        progress.hidden = false;
        document.body.style.overflow = 'hidden';
    }
    try {
        const request = fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ problem })
        }).then(async response => {
            const data = await response.json();
            if (!response.ok || !data.success) return { error: new Error(data.error || 'Unable to analyze this challenge right now.') };
            return { data };
        }).catch(error => ({ error }));

        await runFiveStepAnalysis();
        const outcome = await request;
        if (outcome.error) throw outcome.error;
        const data = outcome.data;
        analyzedChallenge = data;
        updateAnalysisCard(data);
        const result = document.getElementById('routingResult');
        result.hidden = false;
        const submitButton = document.getElementById('submitChallengeButton');
        submitButton.hidden = false;
        submitButton.disabled = false;
        submitButton.innerHTML = 'Submit this challenge <span>↗</span>';
        document.getElementById('journeyMatch')?.classList.add('active');
        result.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } catch (error) {
        showError(error.message || 'We couldn’t connect just now. Please try again.');
    } finally {
        if (progress) progress.hidden = true;
        document.body.style.overflow = '';
        button.disabled = false;
        button.querySelector('span').textContent = 'Find the right team';
    }
}

async function runFiveStepAnalysis() {
    const stages = [
        ['Reading the challenge', 'Picking out the situation and the people affected.'],
        ['Identifying the problem area', 'Connecting the issue to relevant areas of work.'],
        ['Assessing urgency', 'Checking signals that help set a response priority.'],
        ['Finding the right expertise', 'Matching the challenge to a suitable team.'],
        ['Matching a university', 'Selecting an institution and a practical first step.']
    ];
    const started = performance.now();
    const items = [...document.querySelectorAll('.analysis-steps li')];
    const title = document.getElementById('analysisStageTitle');
    const description = document.getElementById('analysisStageDescription');
    const elapsed = document.getElementById('analysisElapsed');
    const fill = document.getElementById('analysisClockFill');

    for (let index = 0; index < stages.length; index++) {
        items.forEach((item, itemIndex) => {
            item.classList.toggle('current', itemIndex === index);
            if (itemIndex < index) item.classList.add('complete');
            else item.classList.remove('complete');
        });
        title.textContent = stages[index][0];
        description.textContent = stages[index][1];
        elapsed.textContent = String(index + 1).padStart(2, '0');
        fill.style.width = `${(index + 1) * 20}%`;
        await new Promise(resolve => setTimeout(resolve, Math.max(0, started + (index + 1) * 1000 - performance.now())));
    }

    items.forEach(item => { item.classList.remove('current'); item.classList.add('complete'); });
}

function updateAnalysisCard(data) {
    const college = data.university_details || {};
    document.getElementById('problemCategory').textContent = data.category || data.domain || 'General';
    document.getElementById('problemPriority').textContent = data.priority || 'Medium';
    document.getElementById('matchedUniversity').textContent = college.name || data.university || 'Not identified';
    document.getElementById('matchedUniversityLocation').textContent = college.location || 'Jharkhand';
    document.getElementById('matchedUniversityFocus').textContent = college.focus_areas || data.category || data.domain || 'Multidisciplinary research';
    document.getElementById('matchedUniversityScore').textContent = `${Number(college.match_score) || 0}%`;
    document.getElementById('matchedTeam').textContent = data.team || 'Innovation Team';
    document.getElementById('suggestedSolution').textContent = data.solution || 'Start by speaking with the people affected, then work with a local institution to test a practical next step.';
}

async function submitChallenge() {
    const button = document.getElementById('submitChallengeButton');
    if (!analyzedChallenge || !button) return;
    button.disabled = true;
    button.textContent = 'Submitting…';
    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const data = await response.json();
        if (!response.ok || !data.success) throw new Error(data.error || 'Submission failed. Please try again.');
        document.getElementById('resultRecordNumber').textContent = data.register_number;
        button.textContent = 'Challenge submitted ✓';
        button.disabled = true;
        analyzedChallenge = null;
        const input = document.getElementById('problemInput');
        input.value = '';
        updateCharacterCount();
        const note = document.createElement('p');
        note.className = 'submission-success';
        note.setAttribute('role', 'status');
        note.textContent = `Your challenge is now in the register. Keep this number: ${data.register_number}.`;
        document.querySelector('.result-actions').append(note);
    } catch (error) {
        showError(error.message || 'We couldn’t submit the challenge. Please try again.');
        button.disabled = false;
        button.innerHTML = 'Submit this challenge <span>↗</span>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('problemInput')?.addEventListener('input', updateCharacterCount);
});
