const liff_id = '2001808224-L3wEzNpG';

//==========================LIFF API初始化================================
$(document).ready(function () {
    liff.init({
        liffId: liff_id
    });
});
//==========================LIFF API初始化================================

function liff_closeWindow() {
    liff.closeWindow();
}
