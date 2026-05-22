import "./main.css";
import "glightbox/dist/css/glightbox.min.css";

import GLightbox from "glightbox";

import { initCookieConsent } from "./cookie-consent.js";

const logStyle = "background: #222; color: #bada55";
console.log("%c Kaktos Generator!", logStyle);

window.copyToClipboard = function copyToClipboard(text) {
    void navigator.clipboard.writeText(text);
};

if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        void navigator.serviceWorker.register(
            "/static/js/service-worker.js",
        );
    });
}

if (document.querySelector(".glightbox")) {
    GLightbox({
        selector: ".glightbox",
        loop: true,
        touchNavigation: true,
        zoomable: true,
    });
}

initCookieConsent();
