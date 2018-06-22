self.addEventListener('push', function(event) {
  //console.log('[Service Worker] Push Received.');
  //console.log(`[Service Worker] Push had this data: "${event.data.text()}"`);

  const title = 'Kerrex\'s tasker';
  const options = {
    body: event.data.text(),
    icon: "clock-icon.png"
  };

  event.waitUntil(self.registration.showNotification(title, options));
});
