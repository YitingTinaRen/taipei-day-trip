var nextPage=0;
var keyword="";
var list;
var isLoading=false;

fetch("/api/user/auth").then((response)=>{return response.json()}).then(function(auth){
    if(!auth){
        document.querySelectorAll(".RightItem2")[0].style.display='block';
        document.querySelectorAll(".RightItem2")[1].style.display='none';
    }else{
        document.querySelectorAll(".RightItem2")[0].style.display='none';
        document.querySelectorAll(".RightItem2")[1].style.display='block';
    }
})


LoadData();

function createBlock(Count, data){
    //Create elements inside Content block
    let container=document.createElement('div');
    let imgDiv=document.createElement('div');
    let OverlaptextDiv=document.createElement('div');
    let BottomtextDiv=document.createElement('div');
    let BottomtextleftDiv=document.createElement('div');
    let BottomtextrightDiv=document.createElement('div');
    let img=document.createElement('img');
    let textSpan=document.createElement('span');
    img.src = data.data[Count].images[0];

    // set attributes
    container.setAttribute("class","block");
    container.setAttribute("id",data.data[Count].id);
    img.setAttribute("class","pic");
    imgDiv.setAttribute("class","block_pic");
    OverlaptextDiv.setAttribute("class","block_text_overlap");
    BottomtextDiv.setAttribute("class","block_text_bottom");
    BottomtextleftDiv.setAttribute("class","block_text_bottom_text_L");
    BottomtextrightDiv.setAttribute("class","block_text_bottom_text_R");
    textSpan.setAttribute("class","text_span");

    textSpan.appendChild(document.createTextNode(data.data[Count].name));
    OverlaptextDiv.appendChild(textSpan);

    let textLeft=document.createTextNode(data.data[Count].mrt)
    let textRight=document.createTextNode(data.data[Count].category)

    imgDiv.appendChild(img);
    container.appendChild(imgDiv);
    container.appendChild(OverlaptextDiv);
    BottomtextleftDiv.appendChild(textLeft);
    BottomtextrightDiv.appendChild(textRight);
    BottomtextDiv.appendChild(BottomtextleftDiv);
    BottomtextDiv.appendChild(BottomtextrightDiv);
    container.appendChild(BottomtextDiv);

    Count++;
    return {'Count':Count, 'container':container}
}

function NoMoreData(GrandParentNode,ParentNode){
    //Not used yet
    let buttonNode=document.querySelector(".button");
    buttonNode.textContent="No more data";
    GrandParentNode.insertBefore(ParentNode,buttonNode);
    return;
}

function LoadData(){
    // console.log("nextPage= "+nextPage);
    isLoading=true;
    if (nextPage===null){return;}
    fetch(["/api/attractions?page="+nextPage+"&keyword="+keyword]).then(function(response){
        return response.json();
    }).then(function (data){
        isLoading=false;
        if(data.error){
            let message=document.createElement('div');
            message.appendChild(document.createTextNode(data.message));
            mainframe.appendChild(message);
            return;
        }
        nextPage=data.nextPage;
        dataAmount=data.data.length;
        let mainframe=document.querySelector(".mainframe");
        for (let i=0;i<3;i++){
            let Content=document.createElement('div');
            let blank1=document.createElement('div');
            let blank2=document.createElement('div');
            let blankDesk=document.createElement('div');
            let funcOutput={};
            
            
            Content.setAttribute("class","Content");
            blank1.setAttribute("class","blank");
            blank2.setAttribute("class","blank");
            blankDesk.setAttribute("class","blank_desk");
            
            createContent(Content, blank1, blank2, blankDesk, mainframe,4*i, dataAmount, data)
            
            footer=document.querySelector(".footer");
            footer.style.visibility="visible";

            
        }
        if(nextPage && (document.querySelector(".mainframe").scrollHeight+document.querySelector(".mainframe").offsetTop)<=window.innerHeight && !isLoading){
                LoadData();
        }
        return;
    })
    
}

function createContent(Content, blank1, blank2, blankDesk, mainframe, Count, dataAmount, data){
    if (!nextPage && Count>=dataAmount){return;}
    funcOutput=createBlock(Count, data);
    Count=funcOutput.Count;
    Content.appendChild(funcOutput.container);
    Content.appendChild(blank1);

    if (!nextPage && Count>=dataAmount){
        Content.appendChild(funcOutput.container);
        mainframe.appendChild(Content);
        return;
    }
    funcOutput=createBlock(Count,data);
    Count=funcOutput.Count;
    Content.appendChild(funcOutput.container);
    Content.appendChild(blankDesk);
    if (!nextPage && Count>=dataAmount){
        Content.appendChild(funcOutput.container);
        mainframe.appendChild(Content);
        return;
    }
    funcOutput=createBlock(Count, data);
    Count=funcOutput.Count;
    Content.appendChild(funcOutput.container);
    Content.appendChild(blank2);
    if (!nextPage && Count>=dataAmount){
        Content.appendChild(funcOutput.container);
        mainframe.appendChild(Content);
        return;
    }
    funcOutput=createBlock(Count, data);
    Count=funcOutput.Count;
    Content.appendChild(funcOutput.container);
    mainframe.appendChild(Content);
}

// scroll event handling
var didScroll = false;

window.addEventListener("wheel",wheelfunc);
function wheelfunc(){
    didScroll = true;

    if ( didScroll ) {
    didScroll = false;

    if ((window.innerHeight + window.scrollY) >= document.querySelector(".mainframe").offsetHeight+document.querySelector(".mainframe").offsetTop){
        if(!isLoading){LoadData();}
        
    }
    }
}


function removeAllChildNodes(parent) {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

// Keyword search
function searchKeyword(){
    elmt=document.querySelector(".mainframe");
    removeAllChildNodes(elmt);
    nextPage=0;
    keyword=document.getElementById("keyword").value;
    LoadData();
}

function findAttractionID(data, name){
    for(let i=0;i<data.data.length;i++){
        if(data.data[i].name==name){
            return data.data[i].id;
        }
    }
}

// (A) GET CATEGORY DATA FROM SERVER VIA AJAX FETCH
fetch("/api/categories")
.then((res) => res.json())
.then((data) => {
    // (B) GET HTML ELEMENTS
    let filter = document.getElementById("keyword"), // search box
    list_wrapper = document.getElementById("category_list"); // list item wrapper
    
    // (C) DRAW HTML LIST
    let cat_count=0;
    for (let i of data.data) {
        let li = document.createElement("div");
        let cat_text=document.createTextNode(i);
        li.setAttribute("id",["cat-"+cat_count])
        li.appendChild(cat_text);
        list_wrapper.appendChild(li);
        cat_count++;
    }

    list_wrapper.style.visibility = "hidden"; // hide
    //When user clicks search bar, show the category list
    filter.addEventListener('click',function(e){
        list_wrapper.style.visibility="visible"; //show
    },false)

    // (D) only show matching results
    list = document.querySelectorAll("#category_list div");
    filter.onkeyup = () => {
        // (D1) GET CURRENT SEARCH TERM
        let search = filter.value.toLowerCase();
    
        // (D2) LOOP THROUGH LIST ITEMS - ONLY SHOW THOSE THAT MATCH SEARCH
        for (let i of list) {
            let item = i.innerHTML.toLowerCase();
            if (item.indexOf(search) == -1) { i.classList.add("hide"); }
            else { i.classList.remove("hide"); }
        }
    };
    
    // fill in search bar when selected.
    const catPressed = e => {
        targetId=e.target.id;
        elmt=document.getElementById(targetId);
        filter.value= elmt.textContent;
        filter.style.color= "#000000";
        list_wrapper.style.visibility="hidden";
        
    }
    for (let i of list) {
        i.addEventListener("click", catPressed);
    }

    // hide the list when user click on window area except for search bar
    document.addEventListener('click', function(e) {
        e = e || window.event;
        var target = e.target || e.srcElement;
        if(target.id != "keyword"){
            list_wrapper.style.visibility="hidden";
        }
    }, false);

    });

// redirect to attraction page.
document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement;
    // console.log(target.classList[0])
    if(target.classList[0]=="block"){
        ID=target.id;
        window.location.assign("/attraction/"+ID);
    }else if(target.parentNode.classList[0] =="block"){
        target=target.parentNode;
        ID=target.id;
        window.location.assign("/attraction/"+ID);
    }else if(target.parentNode.parentNode.classList[0]=="block"){
        target=target.parentNode.parentNode;
        ID=target.id;
        window.location.assign("/attraction/"+ID);
    }else if(target.parentNode.parentNode.parentNode.classList[0]=="block"){
        target=target.parentNode.parentNode.parentNode;
        ID=target.id;
        window.location.assign("/attraction/"+ID);
    }      
        
}, false);

// Get the Login/signup form
var LoginForm = document.getElementById('id01');

// When the user clicks anywhere outside of the LoginForm, close it
window.onclick = function(event) {
    if (event.target == LoginForm) {
        LoginForm.style.display = "none";
    }
}


function register(){
    uname=document.getElementsByName("uname")[0].value;
    email=document.getElementsByName("email")[1].value;
    psw=document.getElementsByName("psw")[1].value;
    data={"name":uname, "email":email, "password":psw};
    console.log(data);

    fetch("/api/user",
        {
            method:"POST",
            headers:{
                'Content-Type':'application/json',
            },
            body:JSON.stringify(data),
        }
    ).then(function(res){
        return res.json();
    }).then(function(result){
        console.log(result);
        if(result['ok']){
            success_text="註冊成功!";
            if(document.querySelectorAll("#id02 .LoginForm-content .form_text").length==1){
                referenceNode=document.querySelector("#id02 .LoginForm-content .form_text");
                parentNode=document.querySelector("#id02 .LoginForm-content .container");
                newNode=document.createElement("div");
                newNode.setAttribute("class","form_text");
                newNode.appendChild(document.createTextNode(success_text));
                parentNode.insertBefore(newNode,referenceNode);
            }else{
                document.querySelectorAll("#id02 .LoginForm-content .form_text")[0].textContent=success_text;
            }
        }
        if(result['error']){
            if(document.querySelectorAll("#id02 .LoginForm-content .form_text").length==1){
                referenceNode=document.querySelector("#id02 .LoginForm-content .form_text");
                parentNode=document.querySelector("#id02 .LoginForm-content .container");
                newNode=document.createElement("div");
                newNode.setAttribute("class","form_text");
                newNode.appendChild(document.createTextNode(result["message"]));
                parentNode.insertBefore(newNode,referenceNode);
            }else{
                document.querySelectorAll("#id02 .LoginForm-content .form_text")[0].textContent=result["message"];
            }
        }
    });
}

function login(){
    email=document.getElementsByName("email")[0].value;
    psw=document.getElementsByName("psw")[0].value;
    data={"email":email, "password":psw};

    fetch("/api/user/auth",
        {
            method:"PUT",
            headers:{
                'Content-Type':'application/json',
            },
            body:JSON.stringify(data),
        }
    ).then(function(res){
        return res.json();
    }).then(function(result){
        console.log(result);
        if(result['ok']){
            window.location.reload();
        }
        else if(result['error']){
            console.log(result);
            if(document.querySelectorAll("#id01 .LoginForm-content .form_text").length ==1){
                referenceNode=document.querySelector("#id01 .LoginForm-content .form_text");
                parentNode=document.querySelector("#id01 .LoginForm-content .container");
                newNode=document.createElement("div");
                newNode.setAttribute("class","form_text");
                newNode.appendChild(document.createTextNode(result["message"]));
                parentNode.insertBefore(newNode,referenceNode);
            }else{
                document.querySelectorAll("#id01 .LoginForm-content .form_text")[0].textContent=result["message"];
            }
        }
    });
}

function logout(){
    fetch("/api/user/auth",
        {
            method:"DELETE",
        }
    ).then(function(res){
        return res.json();
    }).then(function(result){
        console.log(result);
        if(result){
            window.location.reload();
        }
    });
}