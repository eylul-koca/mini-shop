// Flash mesajlarını 4 saniye sonra otomatik kapat
document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 4000);
  });
});

// Silme işlemi için onay iste
function confirmDelete(message) {
  return confirm(message || 'Bu ürünü silmek istediğinden emin misin?');
}
