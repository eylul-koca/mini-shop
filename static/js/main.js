// Flash mesajlarını 4 saniye sonra kapat
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });

  // Dark mode sayfa açılınca hatırla
  if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark');
    const btn = document.querySelector('.dark-toggle');
    if (btn) btn.textContent = '☀️';
  }
});

// Silme onayı
function confirmDelete(message) {
  return confirm(message || 'Bu ürünü silmek istediğinden emin misin?');
}

// Ürün arama
function searchProducts() {
  const input = document.getElementById('searchInput').value.toLowerCase();
  const cards = document.querySelectorAll('.product-card');
  cards.forEach(function(card) {
    const name = card.querySelector('h3').textContent.toLowerCase();
    card.parentElement.style.display = name.includes(input) ? '' : 'none';
  });
}

// Dark mode toggle
function toggleDark() {
  document.body.classList.toggle('dark');
  const btn = document.querySelector('.dark-toggle');
  const isDark = document.body.classList.contains('dark');
  btn.textContent = isDark ? '☀️' : '🌙';
  localStorage.setItem('darkMode', isDark);
}