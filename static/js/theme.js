class ThemeManager {

    constructor() {

        this.html = document.documentElement;

        this.init();
    }

    init() {

        const saved =
            localStorage.getItem('theme');

        const systemDark =
            window.matchMedia(
                '(prefers-color-scheme: dark)'
            ).matches;

        if (
            saved === 'dark' ||
            (!saved && systemDark)
        ) {
            this.enableDark();
        }
    }

    toggle() {

        if (
            this.html.classList.contains('dark')
        ) {
            this.disableDark();
        } else {
            this.enableDark();
        }
    }

    enableDark() {

        this.html.classList.add('dark');

        localStorage.setItem(
            'theme',
            'dark'
        );
    }

    disableDark() {

        this.html.classList.remove('dark');

        localStorage.setItem(
            'theme',
            'light'
        );
    }
}

const theme =
    new ThemeManager();

updateIcon();

document
.getElementById('themeToggle')
.addEventListener(
    'click',
    () => {
        theme.toggle();
        updateIcon();
     }
);

function updateIcon() {

    const icon =
        document.getElementById("themeIcon");

    if (
        document.documentElement
        .classList
        .contains("dark")
    ) {

        icon.textContent = "☀️";

    } else {

        icon.textContent = "🌙";
    }
}
