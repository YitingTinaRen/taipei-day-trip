let prime='';
let page_data={};
fetch("/api/user/auth").then((res)=>{return res.json()})
.then(function(auth){
    if(!auth){
        window.location.replace("/")
    }else{
        let username=auth["data"]["name"]
        let email = auth["data"]["email"]
        // let userId=auth["data"]["id"]
        fetch("/api/member",{method:"POST"}).then((res) => { return res.json() })
        .then(async function(data){
           
            await render_member_summary(username, email);
            render_separator()
            render_booking_summary(username, data);
            showFooter()
            footer = document.querySelector(".footer");
            footer_box = document.querySelector(".footer_box");
            footer.style.height = "100%";
            footer.style.alignItems = "flex-start";
            footer_box.style.marginTop = "45px";



        });
    }
});

window.onclick = function (event) {
    if (event.target.classList[0] == "LoginForm" || event.target.classList[0] == "close-icon") {
        // event.target.style.display = "none";
        document.getElementById("id05").style.display="none";
        document.getElementById("id06").style.display = "none";
        msgs = document.querySelectorAll("#msg");
        if (msgs.length) {
            msgs[0].remove();
        }
        document.getElementById("1").value = "";
        document.getElementById("2").value = "";
        document.getElementById("3").value = "";
        document.getElementById("4").value = "";
        document.querySelector(".LoginForm-content .section").remove();
    }
}



//Functions:
function render_member_summary(username, email){
    return new Promise(function(resolve,reject){
        frame=document.querySelector(".frame");
        section = document.createElement("div");
        section.setAttribute("class", "section");
        section.style="margin-top:40px;";
        buttonStyle="flex:none;width:80px;height:36px; margin:20px 10px 0 0;background:#448899; border-radius:5px; font-family:'Noto Sans TC';font-style:normal;font0weight:400;font-size:16px;color:#FFFFFF;cursor:pointer;";

        // Insert image
        
        journeyImage = document.createElement("div");
        journeyImage.setAttribute("class","journey-image");
        journeyImage.style.position="relative";
        img = document.createElement("img");
        img.setAttribute("id", "profile");
        fetch("/api/memberPic", { method: "GET", }).then(function (res) {
            return res.json()
        }).then(function (result) {
            if (result["url"]) {
                img.src = result["url"];
            } else {
                img.src = "/static/imgs/member_icon.png";
            }
            clickbutton = document.createElement("div");
            clickbutton.setAttribute("id", "editProfile");
            fileuploader = document.createElement("input");
            fileuploader.setAttribute("id", "fileUpload");
            clickbutton.style = "background:black; opacity:40%; position:absolute;bottom:0;width:100%;font-size:20px;text-align:center;color:white;cursor:pointer;"
            clickbutton.appendChild(document.createTextNode("Click to edit!"));
            fileuploader.type = "file";
            fileuploader.style.display = "none";
            fileuploader.accept = "image/*";
            fileuploader.onchange = function (event) { loadFile(event) };
            journeyImage.appendChild(img);
            journeyImage.appendChild(fileuploader);
            journeyImage.appendChild(clickbutton);

            //fill in member summary
            journeyInfo = document.createElement("div");
            journeyInfo.setAttribute("class", "journey-info");
            title = document.createElement("div");
            Name = document.createElement("p");
            Email = document.createElement("p");
            NameChange = document.createElement("button");
            EmailChange = document.createElement("button");
            PswChange = document.createElement("button");
            NameChange.style.cssText = buttonStyle;
            EmailChange.style.cssText = buttonStyle;
            PswChange.style.cssText = buttonStyle;

            title.setAttribute("class", "title");
            NameChange.setAttribute("class", "button")
            EmailChange.setAttribute("class", "button")
            title.innerHTML = `會員資料：`;
            Name.innerHTML = `姓名：<span>${username}</span>`;
            Email.innerHTML = `Email：<span>${email}</span>`;
            NameChange.innerHTML = `更改姓名`;
            EmailChange.innerHTML = `更改信箱`;
            PswChange.innerHTML = `更改密碼`;
            NameChange.onclick = function () { nameChange() };
            EmailChange.onclick = function () { emailChange() };
            PswChange.onclick = function () { pswChange() };



            journeyInfo.appendChild(title);
            journeyInfo.appendChild(Name);
            journeyInfo.appendChild(Email);
            journeyInfo.appendChild(NameChange);
            journeyInfo.appendChild(EmailChange);
            journeyInfo.appendChild(PswChange);
            section.appendChild(journeyImage);
            section.appendChild(journeyInfo);
            frame.appendChild(section);

            const fileSelect = document.getElementById("fileUpload");
            const fileElem = document.getElementById("editProfile");

            fileElem.addEventListener("click", (e) => {
                if (fileElem) {
                    fileSelect.click();
                }
            }, false);
            resolve("done");
        });
    })

}


function loadFile(event){
    let image = document.getElementById('profile');
    image.src = URL.createObjectURL(event.target.files[0]);
    
    let form = new FormData();
    form.append("userPic", event.target.files[0])
    fetch("/api/memberPic",{
        method:"POST",
        body:form,
    }).then(function(res){
        return res.json()
    }).then(function(result){
        console.log(result);
    });
}

function render_booking_summary(username,data){
    // Insert welcome words
    frame = document.querySelector(".frame");
    headLine = document.createElement("div");
    headLine.setAttribute("class", "head-line");
    // headLine=document.querySelector(".head-line");
    headLine.innerHTML=`您好，${username}，您的歷史訂單如下`;
    frame.appendChild(headLine);
    listContainer=document.createElement("div");
    listContainer.setAttribute("class","journey-info")
    listContainer.style="max-width:980px; width:80%;margin:0;"
    frame.appendChild(listContainer);
    if(!data.length){
        text=document.createElement("span");
        text.innerHTML=`目前沒有任何歷史訂單`;

        dummyDiv=document.createElement("div");
        dummyDiv.style="width:100%;height:30px;"
        frame = document.querySelector(".frame");
        frame.appendChild(text);
        frame.appendChild(dummyDiv);
        
        return
    }

    for(let i=0;i<data.length;i++){
        list=document.createElement("p");
        list.setAttribute("id","order-"+data[i]["id"])
        list.style="cursor:pointer";
        list.textContent=data[i]["order_num"];
        list.addEventListener("click", function(event){
            console.log(event.target.textContent)
            fetch("api/order/" + event.target.textContent).then(function (res){
                return res.json();
            }).then(function (data){
                console.log(data);
                create_section(data);
                ID06=document.getElementById("id06").style.display="flex";
                window.addEventListener("click",function(event){
                    if(event.target.id ==="id06"){
                        document.getElementById("id06").style.display = "none";
                    }
                });
            });
            
        })
        listContainer.appendChild(list);

    }
    dummyDiv = document.createElement("div");
    dummyDiv.style = "width:100%;height:30px;"
    frame.appendChild(dummyDiv);

}

function render_separator(){
    frame=document.querySelector(".frame");
    separator=document.createElement("my-separator");
    frame.appendChild(separator);
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
function deleteOrder(order_num){
    fetch("/api/member",
        {
            method: "DELETE",
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(order_num),
        
        }
    ).then(function (res) {
        return res.json();
    }).then(function (result) {
        if (result.hasOwnProperty("ok")) {
            window.location.reload();
        }
        console.log("delete order receives response from backend.")
        console.log(result)
    });
}

function create_section(data){
    frame = document.querySelector(".frame");
    section=document.createElement("div");
    section.setAttribute("class", "section");
    section.style.marginTop="40px";

    journey_image=document.createElement("div");
    journey_image.setAttribute("class","journey-image");
    img = document.createElement("img");
    img.src = data["data"]["trip"]["attraction"]["image"];
    journey_image.appendChild(img);

    journey_info=document.createElement("div");
    journey_info.setAttribute("class","journey-info")
    // journey_info.setAttribute("id",data["booking_id"])
    title = document.createElement("div");
    date = document.createElement("p");
    time = document.createElement("p");
    price = document.createElement("p");
    address = document.createElement("p");
    orderNum=document.createElement("p");
    deleteIcon = document.createElement("div")

    title.setAttribute("class", "title");
    deleteIcon.setAttribute("class", "delete-icon");
    title.innerHTML = `台北一日遊：<span>${data["data"]["trip"]["attraction"]["name"]}</span>`;
    date.innerHTML = `日期：<span>${data["data"]["trip"]["date"]}</span>`;
    if (data["data"]["trip"]["time"] == "morning") {
        time.innerHTML = "時間：<span>早上九點到中午十二點</span>";
    } else {
        time.innerHTML = "時間：<span/cookbook>下午二點到下午五點</span>";
    }
    price.innerHTML = `費用：<span>新台幣${data["data"]["price"]}</span>`;
    address.innerHTML = `地點：<span>${data["data"]["trip"]["attraction"]["address"]}<span>`;
    orderNum.innerHTML = `訂單號碼：<span>${data["data"]["number"]}<span>`;
    deleteIcon.innerHTML = `<img src="/static/imgs/icon_delete.png"/>`;

    journey_info.appendChild(title);
    journey_info.appendChild(date);
    journey_info.appendChild(time);
    journey_info.appendChild(price);
    journey_info.appendChild(address);
    journey_info.appendChild(orderNum);
    journey_info.appendChild(deleteIcon);

    section.appendChild(journey_image);
    section.appendChild(journey_info);
    // frame.appendChild(section);
    Id06 = document.querySelector("#id06 .LoginForm-content");
    Id06.appendChild(section);

    deleteIcon.addEventListener("click", function(e){
        // console.log("click event")
        // console.log(e.target.parentNode.parentNode.children[5].children[0].textContent)
        order_num = e.target.parentNode.parentNode.children[5].children[0].textContent;
        deleteOrder(order_num);
    },false);
}

function nameChange(){
    form=document.querySelector("#id05");
    form.style.display='flex';
    document.getElementById("1").style.display="block";
    document.getElementById("2").style.display = "none";
    document.getElementById("3").style.display = "none";
    document.getElementById("4").style.display = "none";

    document.getElementById("2").value = "";
    document.getElementById("3").value = "";
    document.getElementById("4").value = "";
}
function emailChange() {
    form = document.querySelector("#id05");
    form.style.display = 'flex';
    document.getElementById("1").style.display = "none";
    document.getElementById("2").style.display = "block";
    document.getElementById("3").style.display = "none";
    document.getElementById("4").style.display = "none";

    document.getElementById("1").value = "";
    document.getElementById("3").value = "";
    document.getElementById("4").value = "";

}
function pswChange() {
    form = document.querySelector("#id05");
    form.style.display = 'flex';
    document.getElementById("1").style.display = "none";
    document.getElementById("2").style.display = "none";
    document.getElementById("3").style.display = "block";
    document.getElementById("4").style.display = "block";

    document.getElementById("1").value = "";
    document.getElementById("2").value = "";
}

function updateNewMemberInfo(){
    username=document.getElementById("1").value;
    email=document.getElementById("2").value;
    oldPsw=document.getElementById("3").value;
    newPsw=document.getElementById("4").value;
    data={"username":username, "email":email, "oldPsw":oldPsw, "newPsw":newPsw};

    fetch("/api/user",
        {
            method: "PATCH",
            headers:{'Content-Type':'application/json',},
            body:JSON.stringify(data),
        }
    ).then(function(res){
        return res.json();
    }).then(function (result){
        container=document.querySelectorAll(".container")[2];
        msg=document.createElement("div");
        msg.setAttribute("class","form_text");
        msg.setAttribute("id", "msg");
        msg.innerHTML=`${result["message"]}`;
        container.appendChild(msg);

        fetch("/api/user/auth").then((res) => { return res.json() })
        .then(function (auth) {
            document.getElementsByClassName("journey-info")[0].children[1].children[0].textContent = auth["data"]["name"];
            document.getElementsByClassName("journey-info")[0].children[2].children[0].textContent = auth["data"]["email"];
        });

        
    });
}
