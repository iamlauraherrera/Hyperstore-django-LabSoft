function updateCart(data) {
    console.log("data = ", data);
    document.getElementById("amount").innerText = 'Cop. ' + data.amount;
    document.getElementById("totalamount").innerText = 'Cop. ' + data.totalamount;
}

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);
    
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText = data.quantity;
            updateCart(data);
        }
    });
});

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);

    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText = data.quantity;
            updateCart(data);
        }
    });
});

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    console.log("pid =", id);

    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            updateCart(data);
            eml.closest('.row').remove();
        }
    });
});


$('.plus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
            prod_id: id
        },
        success: function(data){
            window.location.href = 'http://localhost:8000/product-detail/' + id;
        }
    });
});

$('.minus-wishlist').click(function(){
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function(data){
            window.location.href = 'http://localhost:8000/product-detail/' + id;
        }
    });
});