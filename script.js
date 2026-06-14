const BUSINESS_WHATSAPP_NUMBER = "905354315062";

const form = document.querySelector("#bookingForm");
const statusEl = document.querySelector("#formStatus");

function formatDate(value) {
  if (!value) return "";
  return new Intl.DateTimeFormat("tr-TR", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  }).format(new Date(`${value}T12:00:00`));
}

form?.addEventListener("submit", (event) => {
  event.preventDefault();
  const data = new FormData(form);
  const checkin = data.get("checkin");
  const checkout = data.get("checkout");

  if (checkin && checkout && new Date(checkout) <= new Date(checkin)) {
    statusEl.textContent = "Çıkış tarihi giriş tarihinden sonra olmalı.";
    return;
  }

  const message = [
    "Merhaba, kedi oteli için rezervasyon uygunluğu sormak istiyorum.",
    `Ad: ${data.get("name")}`,
    `Telefon: ${data.get("phone")}`,
    `Kedi sayısı: ${data.get("cats")}`,
    `Giriş: ${formatDate(checkin)}`,
    `Çıkış: ${formatDate(checkout)}`,
    `Not: ${data.get("note") || "Yok"}`,
  ].join("\n");

  statusEl.textContent = "WhatsApp mesajı hazırlanıyor...";
  window.open(`https://wa.me/${BUSINESS_WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`, "_blank", "noopener,noreferrer");
});
