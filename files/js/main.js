console.log('%c Kaktos Generator!', 'background: #222; color: #bada55');

// functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text);
}

// pwa
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/assets/js/service-worker.js');
    });
}
