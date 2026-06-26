/**
 * main.js
 * Handles: drag-drop upload, image preview, loading state,
 *          confidence bar animation on result reveal.
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Elements ──────────────────────────────────────────────────────────────
  const uploadZone    = document.getElementById('upload-zone');
  const fileInput     = document.getElementById('file-input');
  const previewWrap   = document.getElementById('preview-wrapper');
  const previewImg    = document.getElementById('preview-img');
  const previewName   = document.getElementById('preview-filename');
  const removeBtn     = document.getElementById('preview-remove');
  const form          = document.getElementById('upload-form');
  const submitBtn     = document.getElementById('btn-predict');
  const loadingState  = document.getElementById('loading-state');
  const resultSection = document.getElementById('result-section');

  // ── File selection via click ───────────────────────────────────────────────
  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) showPreview(fileInput.files[0]);
  });

  // ── Drag and drop ─────────────────────────────────────────────────────────
  uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
  });

  ['dragleave', 'dragend'].forEach(evt =>
    uploadZone.addEventListener(evt, () => uploadZone.classList.remove('dragover'))
  );

  uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
      // Assign to the real file input so Flask receives it
      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      showPreview(file);
    }
  });

  // ── Preview ────────────────────────────────────────────────────────────────
  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src       = e.target.result;
      previewName.textContent = file.name;
      previewWrap.classList.add('visible');
      uploadZone.style.display = 'none';
      submitBtn.disabled   = false;
    };
    reader.readAsDataURL(file);
  }

  // ── Remove preview ─────────────────────────────────────────────────────────
  removeBtn.addEventListener('click', () => {
    fileInput.value          = '';
    previewImg.src           = '';
    previewWrap.classList.remove('visible');
    uploadZone.style.display = '';
    submitBtn.disabled       = true;
  });

  // ── Form submit → loading state ────────────────────────────────────────────
  if (form) {
    form.addEventListener('submit', () => {
      submitBtn.disabled = true;
      loadingState && loadingState.classList.add('visible');
    });
  }

  // ── Animate confidence bars on page load (result already rendered) ─────────
  animateBars();
});

/**
 * Animate all progress bar fills from 0 → their target width.
 * Target width is stored in data-width attribute set by the template.
 */
function animateBars() {
  const fills = document.querySelectorAll('[data-width]');
  if (!fills.length) return;

  // Small delay so the CSS transition is visible after paint
  requestAnimationFrame(() => {
    setTimeout(() => {
      fills.forEach(el => {
        el.style.width = el.dataset.width + '%';
      });
    }, 120);
  });
}
