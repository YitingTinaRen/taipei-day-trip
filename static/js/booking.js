
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
                render_booking_summary(username, data);
                render_separator();
                render_contact_payment(data);
                showFooter()

                card_info = document.getElementsByName("card-number")[0];
                card_info.addEventListener('keyup', function (event) {
                sanitizedValue=this.value.replace(/[^0-9]/gi, '');
                let finalValue="";
                let count=0;
                for (let i = 0; i < sanitizedValue.length;i++){
                    finalValue=finalValue+sanitizedValue[i];
                    if((i+1)%4===0 & (count+1)!==this.maxLength){
                        finalValue=finalValue+" ";
                        count++;
                    }
                    count++;
                }
                this.value=finalValue;
                }, false);
            }


        });
    }
});


//Functions:

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
            <input name="contact-name"/>
        </div>

        <div class="form-row">
            <div class="input-title" >聯絡信箱:</div>
            <input name="email"/>
        </div>

        <div class="form-row">
            <div class="input-title" >手機號碼:</div>
            <input name="phone"/>
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
            <input type="text" name="card-number" maxlength="19" name="credit-number" pattern="\d*" placeholder="**** **** **** ****" required/>
        </div>

        <div class="form-row">
            <div class="input-title" >過期時間:</div>
            <input type="text" name="exp-time" autocomplete="cc-exp" placeholder="MM / YY" required/>
        </div>

        <div class="form-row">
            <div class="input-title" >驗證密碼:</div>
            <input type="password" name="verif-code" minlength="3" pattern="[0-9]+" placeholder="CVV" required/>
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
