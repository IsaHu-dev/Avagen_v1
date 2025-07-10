$(document).on('click', '[id^="download-avatar-btn-"]', function (event) {
  event.preventDefault();
  
  // Show success popup immediately
  showDownloadSuccessPopup();
  
  // Trigger the download after a short delay
  setTimeout(function() {
    window.location.href = this.href;
  }.bind(this), 1000);
});

function showDownloadSuccessPopup() {
  // Clone the hidden template
  const template = document.getElementById('download-success-template');
  const popup = template.querySelector('.popup').cloneNode(true);
  
  // Add popup to the message container
  const messageContainer = document.querySelector('.message-container');
  if (!messageContainer) {
    const newContainer = document.createElement('div');
    newContainer.className = 'message-container';
    document.body.appendChild(newContainer);
  }
  
  const container = document.querySelector('.message-container');
  container.innerHTML = '';
  container.appendChild(popup);
  
  // Show the popup
  popup.style.display = 'block';
  
  // Auto-hide after 5 seconds
  setTimeout(function() {
    popup.style.display = 'none';
  }, 5000);
  
  // Handle close button
  popup.querySelector('.close').addEventListener('click', function() {
    popup.style.display = 'none';
  });
}