function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let btn_increment = document.querySelectorAll(".increment-btn")

btn_increment.forEach( btn1=>{
    btn1.addEventListener('click', addProduct1)
})

function addProduct1(e){
    let product_id = e.target.value
    let url = "/increment_product"
    
    let data = {id:product_id}

    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": "application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)

    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data
        console.log(data)

    })
    .catch(err=>{
        console.log(err)
    })
}

let btn_decrement = document.querySelectorAll(".decrement-btn")

btn_decrement.forEach( btn2=>{
    btn2.addEventListener('click', addProduct)
})

function addProduct(e){
    let product_id = e.target.value
    let url = "/decrement_product"
    
    let data = {id:product_id}

    fetch(url, {
        method: 'POST',
        headers: {"Content-Type": "application/json", 'X-CSRFToken': csrftoken},
        body: JSON.stringify(data)

    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("num_of_items").innerHTML = data

        console.log(data)

    })
    .catch(err=>{
        console.log(err)
    })
}
