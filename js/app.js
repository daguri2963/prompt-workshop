const form = document.querySelector('#improve-form');
const draftInput = document.querySelector('#draft');
const charCount = document.querySelector('#char-count');
const formMessage = document.querySelector('#form-message');
const submitButton = document.querySelector('#submit-button');
const exampleButton = document.querySelector('#example-button');
const purposeInput = document.querySelector('#purpose');
const formatInput = document.querySelector('#format');
const emptyState = document.querySelector('#result-empty');
const loadingState = document.querySelector('#result-loading');
const resultContent = document.querySelector('#result-content');
const improvedPrompt = document.querySelector('#improved-prompt');
const reasonList = document.querySelector('#reason-list');
const copyButton = document.querySelector('#copy-button');
const copyMessage = document.querySelector('#copy-message');

let latestPrompt = '';

function showState(state) {
  emptyState.hidden = state !== 'empty';
  loadingState.hidden = state !== 'loading';
  resultContent.hidden = state !== 'result';
}

function showMessage(message) {
  formMessage.textContent = message;
  formMessage.hidden = !message;
}

draftInput.addEventListener('input', () => {
  charCount.textContent = `${draftInput.value.length.toLocaleString('ko-KR')} / 1,000자`;
  if (formMessage.textContent) showMessage('');
});

exampleButton.addEventListener('click', () => {
  draftInput.value = '신입사원에게 보낼 환영 메일을 써줘';
  draftInput.dispatchEvent(new Event('input'));
  draftInput.focus();
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const draft = draftInput.value.trim();
  if (!draft) {
    showMessage('초안을 한 문장 이상 입력해 주세요.');
    draftInput.focus();
    return;
  }

  showMessage('');
  copyMessage.textContent = '';
  submitButton.disabled = true;
  submitButton.firstChild.textContent = '다듬는 중… ';
  showState('loading');

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 25000);
  try {
    const response = await fetch('/api/improve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ draft, purpose: purposeInput.value, format: formatInput.value }),
      signal: controller.signal,
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || '요청을 처리하지 못했습니다. 잠시 후 다시 시도해 주세요.');
    if (typeof data.improved_prompt !== 'string' || !data.improved_prompt.trim()) throw new Error('결과를 표시할 수 없습니다. 다시 시도해 주세요.');
    latestPrompt = data.improved_prompt.trim();
    improvedPrompt.textContent = latestPrompt;
    reasonList.replaceChildren();
    for (const reason of Array.isArray(data.reasons) ? data.reasons.slice(0, 3) : []) {
      const item = document.createElement('li');
      item.textContent = String(reason);
      reasonList.append(item);
    }
    showState('result');
  } catch (error) {
    showState('empty');
    showMessage(error.name === 'AbortError' ? '응답이 오래 걸리고 있어요. 잠시 후 다시 시도해 주세요.' : error.message || '연결에 문제가 생겼어요. 다시 시도해 주세요.');
  } finally {
    clearTimeout(timeout);
    submitButton.disabled = false;
    submitButton.firstChild.textContent = '프롬프트 다듬기 ';
  }
});

copyButton.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(latestPrompt);
    copyMessage.textContent = '복사했어요! 원하는 AI 도구에 붙여 넣어 보세요.';
  } catch {
    copyMessage.textContent = '자동 복사가 안 되면 위 문장을 선택해서 복사해 주세요.';
  }
});
