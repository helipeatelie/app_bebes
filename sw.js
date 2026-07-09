self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  return self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // Esse arquivo só precisa existir com o evento 'fetch' para o Chrome reconhecer como App.
  // A mágica real de carregamento continua por conta do Streamlit.
});
