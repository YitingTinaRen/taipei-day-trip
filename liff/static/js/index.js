
function liff_closeWindow() {
    liff.closeWindow();
}

function call_off() {
    if (isLoggedIn == false) {
        alert("未登入LINE");
        liff.login({
            // redirectUri: "https://starfruit8106.synology.me:3001/liff/index",
            redirectUri: clientHost + "/liff/index",
        });
    } else {
        window.location.href = clientHost + "/liff/call-off";
    }
}

function liff_logout() {
    fetch("/liff/app/logout", {
        method: "PUT",
    }).then(
        response => response.json()
    ).then(data => {
        console.log("Success:", data);
        liff.logout()
        isLoggedIn = false;
    }).catch(error => {
        console.error("Error:", error);
    });
}
