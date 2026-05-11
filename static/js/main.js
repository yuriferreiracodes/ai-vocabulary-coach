// Scroll chat to bottom after HTMX swaps
document.body.addEventListener('htmx:afterSwap', function (e) {
  if (e.detail.target && e.detail.target.id === 'messages') {
    e.detail.target.scrollTop = e.detail.target.scrollHeight;
  }
});

// Show loading state on form submit buttons
document.body.addEventListener('htmx:beforeRequest', function (e) {
  const btn = e.detail.elt.querySelector('button[type="submit"]');
  if (btn) {
    btn.disabled = true;
    btn.dataset.originalText = btn.textContent;
    btn.textContent = 'Loading…';
  }
});

document.body.addEventListener('htmx:afterRequest', function (e) {
  const btn = e.detail.elt.querySelector('button[type="submit"]');
  if (btn && btn.dataset.originalText) {
    btn.disabled = false;
    btn.textContent = btn.dataset.originalText;
    delete btn.dataset.originalText;
  }
});
