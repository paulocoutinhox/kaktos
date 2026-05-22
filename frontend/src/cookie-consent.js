const STORAGE_KEY = "kaktos:cookie-consent";
const STORAGE_VERSION = 1;

const CATEGORIES = ["necessary", "analytics"];

const CONSENT_MAP = {
    analytics: ["analytics_storage"],
};

const DEFAULT_CHOICES = { necessary: true, analytics: false };

function readStoredChoice() {
    try {
        const raw = window.localStorage.getItem(STORAGE_KEY);
        if (!raw) {
            return null;
        }
        const parsed = JSON.parse(raw);
        if (parsed && parsed.version === STORAGE_VERSION && parsed.categories) {
            return parsed;
        }
        return null;
    } catch {
        return null;
    }
}

function persistChoice(categories) {
    const payload = {
        version: STORAGE_VERSION,
        decidedAt: new Date().toISOString(),
        categories,
    };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function ensureGtag() {
    window.dataLayer = window.dataLayer || [];
    if (typeof window.gtag !== "function") {
        window.gtag = function gtag() {
            window.dataLayer.push(arguments);
        };
    }
    return window.gtag;
}

function applyConsentToGtag(categories) {
    const gtag = ensureGtag();
    const update = {};
    for (const category of Object.keys(CONSENT_MAP)) {
        const granted = Boolean(categories[category]);
        for (const flag of CONSENT_MAP[category]) {
            update[flag] = granted ? "granted" : "denied";
        }
    }
    gtag("consent", "update", update);
}

function dispatchEvent(categories) {
    window.dispatchEvent(new CustomEvent("kaktos:consent-updated", { detail: { categories } }));
}

function syncToggles(root, categories) {
    const inputs = root.querySelectorAll("[data-cookie-consent-category]");
    inputs.forEach((input) => {
        const category = input.dataset.cookieConsentCategory;
        if (category === "necessary") {
            input.checked = true;
            return;
        }
        input.checked = Boolean(categories[category]);
    });
}

function setBannerState(root, state) {
    root.dataset.state = state;
    root.setAttribute("aria-hidden", state === "hidden" ? "true" : "false");
    const modal = root.querySelector(".cookie-consent-modal");
    if (modal) {
        modal.setAttribute("aria-hidden", state === "preferences" ? "false" : "true");
    }
}

function readToggleSelection(root) {
    const selection = { ...DEFAULT_CHOICES };
    const inputs = root.querySelectorAll("[data-cookie-consent-category]");
    inputs.forEach((input) => {
        const category = input.dataset.cookieConsentCategory;
        if (!CATEGORIES.includes(category)) {
            return;
        }
        selection[category] = category === "necessary" ? true : input.checked;
    });
    return selection;
}

function commitChoice(root, categories) {
    persistChoice(categories);
    applyConsentToGtag(categories);
    syncToggles(root, categories);
    setBannerState(root, "hidden");
    dispatchEvent(categories);
}

function handleAction(root, action) {
    if (action === "accept") {
        commitChoice(root, { necessary: true, analytics: true });
        return;
    }
    if (action === "reject") {
        commitChoice(root, { necessary: true, analytics: false });
        return;
    }
    if (action === "save") {
        commitChoice(root, readToggleSelection(root));
        return;
    }
    if (action === "preferences") {
        setBannerState(root, "preferences");
        return;
    }
    if (action === "open") {
        const stored = readStoredChoice();
        syncToggles(root, stored ? stored.categories : DEFAULT_CHOICES);
        setBannerState(root, "preferences");
        return;
    }
    if (action === "close") {
        const stored = readStoredChoice();
        setBannerState(root, stored ? "hidden" : "banner");
    }
}

function bindActions(root) {
    document.addEventListener("click", (event) => {
        const target = event.target.closest("[data-cookie-consent-action]");
        if (!target) {
            return;
        }
        event.preventDefault();
        handleAction(root, target.dataset.cookieConsentAction);
    });
}

function bootstrap() {
    const root = document.getElementById("cookie-consent");
    if (!root) {
        return;
    }

    const stored = readStoredChoice();
    const initialChoice = stored ? stored.categories : DEFAULT_CHOICES;

    syncToggles(root, initialChoice);

    if (stored) {
        applyConsentToGtag(stored.categories);
        setBannerState(root, "hidden");
    } else {
        setBannerState(root, "banner");
    }

    bindActions(root);
}

export function initCookieConsent() {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap, { once: true });
        return;
    }
    bootstrap();
}
