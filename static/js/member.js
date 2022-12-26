let prime='';
let page_data={};
fetch("/api/user/auth").then((res)=>{return res.json()})
.then(function(auth){
    if(!auth){
        window.location.replace("/")
    }else{
        let username=auth["data"]["name"]
        // let userId=auth["data"]["id"]
        fetch("/api/member",{method:"POST"}).then((res) => { return res.json() })
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
                console.log(data)
                render_booking_summary(username, data);
                // render_separator();
                // render_contact_payment(data);
                showFooter()

                

            }


        });
    }
});




//Functions:

function render_booking_summary(username,data){
    // Insert welcome words
    headLine=document.querySelector(".head-line");
    headLine.innerHTML=`您好，${username}，您的歷史訂單如下`;

    if(!data){
        text=document.createElement("span");
        text.innerHTML=`目前沒有任何歷史訂單`;
        frame = document.querySelector(".frame");
        section=document.querySelector(".section");
        frame.insertBefore(text,section);
        return
    }

    for(let i=0;i<data.length;i++){
        if(i>0){
            //create section
            create_section(data[i], true);
            render_separator()
        }else{
            //create section
            create_section(data[i], false);
            render_separator()
        }
    }


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
function deleteOrder(booking_id){
    fetch("/api/member",
        {
            method: "DELETE",
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(booking_id),
        
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

function create_section(data, dataMoreThanOne){
    frame = document.querySelector(".frame");
    section=document.createElement("div");
    section.setAttribute("class", "section");
    if(dataMoreThanOne){
        section.style.marginTop="40px";
    }

    journey_image=document.createElement("div");
    journey_image.setAttribute("class","journey-image");
    img = document.createElement("img");
    img.src = data["images"];
    journey_image.appendChild(img);

    journey_info=document.createElement("div");
    journey_info.setAttribute("class","journey-info")
    journey_info.setAttribute("id",data["booking_id"])
    title = document.createElement("div");
    date = document.createElement("p");
    time = document.createElement("p");
    price = document.createElement("p");
    address = document.createElement("p");
    orderNum=document.createElement("p");
    deleteIcon = document.createElement("div")

    title.setAttribute("class", "title");
    deleteIcon.setAttribute("class", "delete-icon");
    title.innerHTML = `台北一日遊：<span>${data["name"]}</span>`;
    date.innerHTML = `日期：<span>${data["date"]}</span>`;
    if (data["time"] == "morning") {
        time.innerHTML = "時間：<span>早上九點到中午十二點</span>";
    } else {
        time.innerHTML = "時間：<span/cookbook>下午二點到下午五點</span>";
    }
    price.innerHTML = `費用：<span>新台幣${data["price"]}</span>`;
    address.innerHTML = `地點：<span>${data["address"]}<span>`;
    orderNum.innerHTML = `訂單號碼：<span>${data["order_num"]}<span>`;
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
    frame.appendChild(section);
    deleteIcon.addEventListener("click", function(e){
        console.log("click event")
        console.log(e.target.parentNode.parentNode.id)
        booking_id = e.target.parentNode.parentNode.id;
        deleteOrder(booking_id);
    },false);
}
