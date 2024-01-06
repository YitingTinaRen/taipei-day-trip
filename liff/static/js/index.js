const liff_id = '{{ liff_id }}';
let isLoggedIn = false;
console.log(liff_id)
$(document).ready(function () {
    fetch("/liff/app/liff-id", {
        method: "GET",
    }).then(
        response => response.json()
    ).then(data => {
        liff.init({
            liffId: data
        }).then(() => {
            // Check if the user is logged in after initialization
            isLoggedIn = liff.isLoggedIn();
            if (isLoggedIn == false) {
                liff.login({
                    redirectUri: clientHost + '/liff/index'
                })
            } else {
                let payload = {};
                payload['token'] = liff.getIDToken();
                fetch("app/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(payload),
                }).then(
                    response => response.json()
                ).then(data => {
                    console.log("Success:", data);
                }).catch(error => {
                    console.error("Error:", error);
                });
            }
        }).catch((err) => {
            console.error('LIFF initialization failed', err);
        });
    }).catch(error => {
        console.error("Error:", error);
    });
});


function liff_closeWindow() {
    liff.closeWindow();
}

function call_off() {
    if (isLoggedIn == false) {
        alert("未登入LINE");
        liff.login({
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
        liff.logout()
        isLoggedIn = false;
    }).catch(error => {
        console.error("Error:", error);
    });
}
