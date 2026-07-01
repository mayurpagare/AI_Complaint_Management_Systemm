document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        root.setAttribute("data-theme", savedTheme);
    }

    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
            root.setAttribute("data-theme", nextTheme);
            localStorage.setItem("theme", nextTheme);
        });
    });

    const navToggle = document.querySelector("[data-nav-toggle]");
    const navMenu = document.querySelector("[data-nav-menu]");
    if (navToggle && navMenu) {
        navToggle.addEventListener("click", () => navMenu.classList.toggle("is-open"));
    }

    document.querySelectorAll(".btn").forEach((button) => {
        button.addEventListener("click", (event) => {
            const ripple = document.createElement("span");
            const rect = button.getBoundingClientRect();
            ripple.className = "ripple";
            ripple.style.left = `${event.clientX - rect.left}px`;
            ripple.style.top = `${event.clientY - rect.top}px`;
            button.appendChild(ripple);
            window.setTimeout(() => ripple.remove(), 700);
        });
    });

    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!window.confirm(form.dataset.confirm)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll("form[data-validate]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const invalid = Array.from(form.querySelectorAll("[required]")).find((field) => !field.value.trim());
            if (invalid) {
                event.preventDefault();
                invalid.focus();
                return;
            }
            showLoader();
        });
    });

    window.addEventListener("beforeunload", () => {
        const active = document.activeElement;
        if (active && (active.tagName === "A" || active.tagName === "BUTTON")) {
            showLoader();
        }
    });

    window.setTimeout(() => {
        document.querySelectorAll(".flash").forEach((flash) => flash.remove());
    }, 5000);
});

function showLoader() {
    const loader = document.getElementById("pageLoader");
    if (loader) {
        loader.classList.add("is-visible");
    }
}
