let root = document.documentElement;

document.getElementById("switcher").addEventListener("click", function() {
    if (root.getAttribute('data-theme') === "dark") {
        root.setAttribute("data-theme", "light")
    } else {
        root.setAttribute("data-theme", "dark")
    };
});

(function() {
    root.setAttribute("data-theme", "light");
})();