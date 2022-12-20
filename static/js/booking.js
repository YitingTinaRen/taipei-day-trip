let prime='';
let page_data={"prime":"", "order":{"price":"","trip":{},"data":"","time":""}, "contact":{"name":"", "email":"", "phone":""}};
fetch("/api/user/auth").then((res)=>{return res.json()})
.then(function(auth){
    if(!auth){
        window.location.replace("/")
    }else{
        let username=auth["data"]["name"]
        fetch("/api/booking",{method:"GET"}).then((res) => { return res.json() })
        .then(function(data){
            if(!data){
                render_booking_summary(username, data);
                showFooter()
                footer=document.querySelector(".footer");
                footer_box=document.querySelector(".footer_box");
                footer.style.height="100%";
                footer.style.alignItems="flex-start";
                footer_box.style.marginTop="45px";

            }else{
                page_data["order"]["trip"]["attraction"] = data.data.attraction;
                page_data["order"]["price"] = data.data.price;
                page_data["order"]["data"] = data.data.date;
                page_data["order"]["time"] = data.data.time;
                render_booking_summary(username, data);
                render_separator();
                render_contact_payment(data);
                showFooter()

                // card_info = document.getElementsByName("card-number")[0];
                // card_info.addEventListener('keyup', function (event) {
                // sanitizedValue=this.value.replace(/[^0-9]/gi, '');
                // let finalValue="";
                // let count=0;
                // for (let i = 0; i < sanitizedValue.length;i++){
                //     finalValue=finalValue+sanitizedValue[i];
                //     if((i+1)%4===0 & (count+1)!==this.maxLength){
                //         finalValue=finalValue+" ";
                //         count++;
                //     }
                //     count++;
                // }
                // this.value=finalValue;
                // }, false);

                //TapPay
                // import { TPDirect } from "https://js.tappaysdk.com/sdk/tpdirect/v5.14.0";
                
                TPDirect.setupSDK(126865, "app_iOcvyk9GjaA4Gfl4jyE1jnFhyyBETkthHT9wfFBh71Dbu1Gfksbfzrgtq7F2", "sandbox");
                let fields = {
                    number: { 
                        element: '#card-number',
                        placeholder: '**** **** **** ****'
                     },
                    expirationDate: { 
                        element: '#card-expiration-date',
                        placeholder: 'MM / YY'
                     },
                    ccv: { element: '#card-ccv',
                        placeholder: 'CCV'
                    }
                }
                TPDirect.card.setup({
                    fields: fields,
                    styles: {
                        'input': {
                            // 'color': 'gray'
                            'font-family': 'Noto Sans TC',
                            'font-style': 'normal',
                            'font-weight': '500',
                            'font-size': '16px'
                        },
                        ':focus': { 'color': 'black' },
                        '.valid': { 'color': 'green' },
                        '.invalid': { 'color': 'red' },
                    },
                    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
                    isMaskCreditCardNumber: true,
                    maskCreditCardNumberRange: {
                        beginIndex: 6,
                        endIndex: 11
                    }
                });

                TPDirect.card.onUpdate(function (update) {
                    const submitButton = document.querySelector('.confirm button');
                    if (update.canGetPrime) {
                        submitButton.removeAttribute('disabled')
                    } else {
                        submitButton.setAttribute('disabled', true)
                    }

                    /* Change card type display when card type change */
                    /* ============================================== */

                    // cardTypes = ['visa', 'mastercard', ...]
                    // var newType = update.cardType === 'unknown' ? '' : update.cardType
                    // $('#cardtype').text(newType)

                    /* Change form-group style when tappay field status change */
                    /* ======================================================= */

                });

                button = document.querySelector(".confirm button");
                button.addEventListener("click", function (event) { onSubmit(event) });
                console.log(prime);

            }


        });
    }
});




//Functions:
function onSubmit(event) {
    event.preventDefault()
    

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        console.log('can not get prime')
        return
    }
    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            console.log('get prime error ' + result.msg)
            return
        }
        console.log('get prime 成功, prime: ' + result.card.prime)
        page_data["prime"]=result.card.prime;
        page_data["contact"]["name"] = document.getElementsByName("contact-name")[0].value;
        page_data["contact"]["email"] = document.getElementsByName("email")[0].value;
        page_data["contact"]["phone"] = document.getElementsByName("phone")[0].value;
        console.log(page_data)
        fetch("/api/orders", {
            method: "POST",
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(page_data),
        }).then((res) => { return res.json() })
        .then(function (data){
            console.log(data);
            window.location.replace("/thankyou?number="+data["data"]["number"]);
        });
        

        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
}

function render_booking_summary(username,data){
    // Insert welcome words
    headLine=document.querySelector(".head-line");
    headLine.innerHTML=`您好，${username}，待預定的行程如下`;

    if(!data){
        text=document.createElement("span");
        text.innerHTML=`目前沒有任何待預定的行程`;
        frame = document.querySelector(".frame");
        section=document.querySelector(".section");
        frame.insertBefore(text,section);
        return
    }
    
    // Insert image
    journeyImage=document.querySelector(".journey-image");
    img=document.createElement("img");
    img.src=data.data["attraction"]["image"];
    journeyImage.appendChild(img);

    //fill in booking summary
    journeyInfo=document.querySelector(".journey-info");
    title=document.createElement("div");
    date=document.createElement("p");
    time=document.createElement("p");
    price = document.createElement("p");
    address = document.createElement("p");
    deleteIcon=document.createElement("div")

    title.setAttribute("class","title");
    deleteIcon.setAttribute("class","delete-icon");
    title.innerHTML=`台北一日遊：<span>${data.data["attraction"]["name"]}</span>`;
    date.innerHTML = `日期：<span>${data.data["date"]}</span>`;
    if (data.data["time"] == "morning"){
        time.innerHTML = "時間：<span>早上九點到中午十二點</span>";
    }else{
        time.innerHTML = "時間：<span>下午二點到下午五點</span>";
    }
    price.innerHTML = `費用：<span>新台幣${data.data["price"]}</span>`;
    address.innerHTML=`地點：<span>${data.data["attraction"]["address"]}<span>`;
    deleteIcon.innerHTML = `<img onclick="deleteBooking()" src="/static/imgs/icon_delete.png"/>`;

    journeyInfo.appendChild(title);
    journeyInfo.appendChild(date);
    journeyInfo.appendChild(time);
    journeyInfo.appendChild(price);
    journeyInfo.appendChild(address);
    journeyInfo.appendChild(deleteIcon);

}

function render_separator(){
    frame=document.querySelector(".frame");
    separator=document.createElement("my-separator");
    frame.appendChild(separator);
}

function render_contact_payment(data){
    frame = document.querySelector(".frame");
    contact_content=document.createElement("div");
    contact_content.setAttribute("class","content");
    contact_content.innerHTML=`
        <div class="head-line">您的聯絡資訊</div>
                
        <div class="form-row">
            <div class="input-title" >聯絡姓名:</div>
            <input type="text" name="contact-name" required/>
        </div>

        <div class="form-row">
            <div class="input-title" >聯絡信箱:</div>
            <input type="email" name="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"/ required>
        </div>

        <div class="form-row">
            <div class="input-title" >手機號碼:</div>
            <input type="text"name="phone" pattern="pattern=/((?=(09))[0-9]{10})$/g" required/>
        </div>

        <div class="form-row">
            <div class="notice-text" >請保持手機暢通，準時到達，導覽人員將用手機與您聯繫，務必留下正確的聯絡方式。</div>
        </div>
    `;
    frame.appendChild(contact_content);

    render_separator();

    payment_content = document.createElement("div");
    payment_content.setAttribute("class", "content");
    payment_content.innerHTML = `
        <div class="head-line">信用卡付款資訊</div>
        <div class="form-row">
            <div class="input-title" >卡片號碼:</div>
            <div class="tpfield" id="card-number"></div>
            <!--<input type="text" class="tpfield" id="card-number" name="card-number" maxlength="19"  pattern="\d*" placeholder="**** **** **** ****" required/>-->
        </div>

        <div class="form-row">
            <div class="input-title" >過期時間:</div>
            <div class="tpfield" id="card-expiration-date"></div>
            <!--<input type="text" class="tpfield" id="card-expiration-date" name="exp-time" autocomplete="cc-exp" placeholder="MM / YY" required/>-->
        </div>

        <div class="form-row">
            <div class="input-title" >驗證密碼:</div>
            <div class="tpfield" id="card-ccv"></div>
            <!--<input type="password" class="tpfield" id="card-ccv" name="verif-code" minlength="3" pattern="[0-9]+" placeholder="CCV" required/>-->
        </div>
    `;
    frame.appendChild(payment_content);

    render_separator();

    confirm=document.createElement("div");
    confirm.setAttribute("class","confirm");
    confirm.innerHTML=`
        <div class="notice-text">總價：新台幣 ${data.data["price"]}</div>
        <button>確認訂購並付款</button>
    `;
    frame.appendChild(confirm);
}

function deleteBooking(){
    fetch("/api/booking",
        {
            method: "DELETE",
        }
    ).then(function (res) {
        return res.json();
    }).then(function (result) {
        if (result.hasOwnProperty("ok")) {
            window.location.reload();
        }
    });
}

function setNumberFormGroupToError(selector) {
    $(selector).addClass('has-error')
    $(selector).removeClass('has-success')
}

function setNumberFormGroupToSuccess(selector) {
    $(selector).removeClass('has-error')
    $(selector).addClass('has-success')
}

function setNumberFormGroupToNormal(selector) {
    $(selector).removeClass('has-error')
    $(selector).removeClass('has-success')
}
