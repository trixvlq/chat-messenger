let root = document.documentElement;

document.getElementById("switcher").addEventListener("click", function() {
    if (root.getAttribute('data-theme') === "dark") {
        root.setAttribute("data-theme", "light")
    } else {
        root.setAttribute("data-theme", "dark")
    };
});

(function() {
    root.setAttribute("data-theme", "dark");
})();

function dropdownFunction() {
    document.getElementById('profileDropdown').classList.toggle('show');
};

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            };
        };
    };
};
