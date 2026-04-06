// admin_jewellery.js
(function() {
  function parseVal(id) {
    const el = document.getElementById(id);
    if (!el) return 0;
    // some fields may have commas etc.
    const v = el.value ? el.value.replace(/,/g, '') : '';
    const num = parseFloat(v);
    return isNaN(num) ? 0 : num;
  }

  function formatNum(n) {
    return (Math.round((n + Number.EPSILON) * 100) / 100).toFixed(2);
  }

  function updateTotal() {
    const gold = parseVal('id_gold_value');
    const stone = parseVal('id_stone_value');
    const making = parseVal('id_making_charges');
    const gst = parseVal('id_gst');
    const total = gold + stone + making + gst;

    // update price input (so it saves)
    const priceInput = document.getElementById('id_price');
    if (priceInput) priceInput.value = formatNum(total);

    // update total_price input if present (editable)
    const totalInput = document.getElementById('id_total_price');
    if (totalInput) {
      totalInput.value = formatNum(total);
    }

    // update readonly display of total_price (Django admin renders readonly as <p class="readonly">)
    const fieldWrapper = document.querySelector('.form-row.field-total_price');
    if (fieldWrapper) {
      // find existing readonly element
      let readonlyEl = fieldWrapper.querySelector('.readonly');
      if (!readonlyEl) {
        // create a readonly-like element
        readonlyEl = document.createElement('p');
        readonlyEl.className = 'readonly';
        fieldWrapper.appendChild(readonlyEl);
      }
      readonlyEl.innerText = formatNum(total);
    }

    // optionally show a small live total next to labels (for extra feedback)
    let liveSpan = document.getElementById('live_total_display');
    if (!liveSpan) {
      const priceFieldRow = document.querySelector('.form-row.field-price .field-box');
      if (priceFieldRow) {
        liveSpan = document.createElement('div');
        liveSpan.id = 'live_total_display';
        liveSpan.style.marginTop = '6px';
        liveSpan.style.fontWeight = '600';
        liveSpan.style.color = '#b89c00';
        priceFieldRow.appendChild(liveSpan);
      }
    }
    if (liveSpan) liveSpan.innerText = 'Live Total: ₹' + formatNum(total);
  }

  function bindInputs() {
    const ids = ['id_gold_value', 'id_stone_value', 'id_making_charges', 'id_gst'];
    ids.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', updateTotal);
        // also update on change (e.g., pasted)
        el.addEventListener('change', updateTotal);
      }
    });
    // run once on load
    updateTotal();
  }

  // Wait until DOM ready (admin sometimes loads fields via JS)
  document.addEventListener('DOMContentLoaded', function() {
    // small delay to ensure admin fields are rendered
    setTimeout(bindInputs, 200);
  });
})();
