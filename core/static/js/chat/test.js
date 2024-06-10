function dropdownFunction() {
    document.getElementById('profileDropdown').classList.toggle('show');
};

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            console.log(i);
            console.log(dropdowns.length);
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            };
        };
    };
};

var userModal = document.getElementById('usersProfile');
var profileBtn = document.getElementById('profileBtn');
var spanClose = document.getElementById('close')
var friendListModal = document.getElementById('friendList');
var friendListBtn = document.getElementById('friendsBtn');
var closeBtn = document.getElementById('closeBtn');

profileBtn.onclick = function() {
    userModal.style.display = 'block';
};
spanClose.onclick = function() {
    userModal.style.display = 'none';
};
friendListBtn.onclick = function() {
    friendListModal.style.display = 'block';
};
closeBtn.onclick = function() {
    friendListModal.style.display = 'none';
};
window.onclick = function(event) {
    if (event.target == userModal) {
        userModal.style.display = "none";
    };
    if (event.target == friendListModal) {
        friendListModal.style.display = 'none';
    }
};