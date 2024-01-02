
function liff_closeWindow() {
    liff.closeWindow();
}

function call_off() {
    if (isLoggedIn != true) {
        alert("未登入LINE");
        liff.login({
            // redirectUri: "https://starfruit8106.synology.me:3001/liff/index",
            redirectUri: "https://5672-118-170-42-151.ngrok-free.app/liff/index",
        });
    } else {
        alert("已登入LINE");
        window.location.href = "https://5672-118-170-42-151.ngrok-free.app/liff/call-off";
    }
}

function liff_logout() {
    liff.logout()
    isLoggedIn = false;
    console.log('User logged out');
}
