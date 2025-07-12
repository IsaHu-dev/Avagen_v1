/* jshint esversion: 6 */
/* global $ */

$(document).on('click', '[id^="download-avatar-btn-"]', function (event) {
  event.preventDefault();

  showDownloadSuccessPopup();

  setTimeout(() => {
    window.location.href = this.href;
  }, 1000);
});

function showDownloadSuccessPopup() {
  const popup = createDownloadPopup();
  ensureMessageContainerExists();
  displayPopup(popup);
  attachCloseHandler(popup);
}

function createDownloadPopup() {
  const template = document.getElementById('download-success-template');
  return template.querySelector('.popup').cloneNode(true);
}

function ensureMessageContainerExists() {
  if (!document.querySelector('.message-container')) {
    const newContainer = document.createElement('div');
    newContainer.className = 'message-container';
    document.body.appendChild(newContainer);
  }
}

function displayPopup(popup) {
  const container = document.querySelector('.message-container');
  container.innerHTML = '';
  container.appendChild(popup);
  popup.style.display = 'block';

  setTimeout(() => {
    popup.style.display = 'none';
  }, 5000);
}

function attachCloseHandler(popup) {
  popup.querySelector('.close').addEventListener('click', () => {
    popup.style.display = 'none';
  });
}
