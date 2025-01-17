document.addEventListener("DOMContentLoaded", () => {
    const themeToggleButton = document.getElementById("theme-toggle");

    // Muat tema dari LocalStorage
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        enableDarkTheme();
    }

    // Tambahkan event listener untuk tombol
    themeToggleButton.addEventListener("click", () => {
        if (document.body.classList.contains("dark-theme")) {
            disableDarkTheme();
        } else {
            enableDarkTheme();
        }
    });

    function enableDarkTheme() {
        document.body.classList.add("dark-theme");
        document.querySelector(".container").classList.add("dark-theme");
        document.querySelectorAll("h1, h2, label, .explanation").forEach(el => {
            el.classList.add("dark-theme");
        });
        themeToggleButton.textContent = "Switch to Light Theme";

        // Simpan tema ke LocalStorage
        localStorage.setItem("theme", "dark");
    }

    function disableDarkTheme() {
        document.body.classList.remove("dark-theme");
        document.querySelector(".container").classList.remove("dark-theme");
        document.querySelectorAll("h1, h2, label, .explanation").forEach(el => {
            el.classList.remove("dark-theme");
        });
        themeToggleButton.textContent = "Switch to Dark Theme";

        // Simpan tema ke LocalStorage
        localStorage.setItem("theme", "light");
    }
});
