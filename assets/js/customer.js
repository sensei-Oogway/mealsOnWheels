function toggleSidebar() {
  var sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("show");
}

function cleanAllContainer_customer() {
  $(".app-home-body").html("");
  $(".app-restaurant-body").html("");
  $(".app-orders-container").html("");
}

function cleanAllContainer_restaurant() {}

function loadCustomerHome() {
  var container_element = $(".app-home-body");
  fetch("/restaurant/customer_loadhome", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      cleanAllContainer_customer();
      clearCart(false);
      return response.text();
    })
    .then((data) => {
      container_element.html(data);
      toggleSidebar();
    });
}

function openRestaurantPage(res_id) {
  var container_element = $(".app-restaurant-body");

  $.ajax({
    url: "/restaurant/customer_loadRestaurant",
    type: "POST",
    data: {
      restaurant_id: res_id,
    },
    success: function (response) {
      cleanAllContainer_customer();
      container_element.html(response);
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

function loadRestaurantHome(toggle) {
  var container_element = $(".app-restaurant-body");

  $.ajax({
    url: "/restaurant/restaurant_loadhome",
    type: "POST",
    data: {
      id: localStorage.getItem("userId"),
    },
    success: function (response) {
      cleanAllContainer_customer();
      container_element.html(response);
      if (toggle) {
        toggleSidebar();
      }
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

function searchByName(searchInput) {
  const restaurantCards = document.querySelectorAll(".restaurant-card");

  const searchText = searchInput.value.trim().toLowerCase();

  if (searchText.length >= 3) {
    restaurantCards.forEach((card) => {
      const cardTitle = card
        .querySelector(".card-title")
        .textContent.toLowerCase();
      if (cardTitle.startsWith(searchText)) {
        card.closest(".col-3").classList.remove("search-void");
      } else {
        card.closest(".col-3").classList.add("search-void");
      }
    });
  } else {
    restaurantCards.forEach((card) => {
      card.closest(".col-3").classList.remove("search-void");
    });
  }
}

function searchByCategory(element) {
  //Clear everything
  //   var searchCategory = "";

  const restaurantCards = document.querySelectorAll(".restaurant-card");
  restaurantCards.forEach((card) => {
    card.closest(".col-3").classList.remove("category-void");
  });

  if (element.classList.contains("category-selected")) {
    element.classList.remove("category-selected");
  } else {
    var categories = document.querySelectorAll(".category-list .card-link");
    categories.forEach((category) => {
      category.classList.remove("category-selected");
    });
    element.classList.add("category-selected");

    var searchCategory = $(element).attr("data-value");

    restaurantCards.forEach((card) => {
      if (card.querySelector(".cuisine").innerHTML != searchCategory) {
        card.closest(".col-3").classList.add("category-void");
      }
    });
  }
}

function searchByRating(value) {
  const restaurantCards = document.querySelectorAll(".restaurant-card");

  restaurantCards.forEach((card) => {
    card.closest(".col-3").classList.remove("rating-void");
  });

  if (value != -1) {
    document.getElementById("review_dropdown").textContent =
      "Rating " + value + "★";

    restaurantCards.forEach((card) => {
      if (parseInt(card.querySelector(".rating").innerHTML) < value) {
        card.closest(".col-3").classList.add("rating-void");
      }
    });
  } else {
    document.getElementById("review_dropdown").textContent = "Rating";
  }
}

function searchByDistance(value) {
  const restaurantCards = document.querySelectorAll(".restaurant-card");

  if (value != -1) {
    document.getElementById("distance_dropdown").textContent =
      value != ">10" ? "Distance <" + value + "Km" : "Distance " + value + "Km";

    restaurantCards.forEach((card) => {
      value = value == ">10" ? 15 : value;
      if (parseInt(card.querySelector(".distance").innerHTML) > value) {
        card.closest(".col-3").classList.add("distance-void");
      }
    });
  } else {
    document.getElementById("distance_dropdown").textContent = "Distance";
    restaurantCards.forEach((card) => {
      card.closest(".col-3").classList.remove("distance-void");
    });
  }
}

const elements = document.querySelectorAll(".custom-truncate");
elements.forEach((element) => {
  const originalText = element.innerText;
  element.dataset.originalText = originalText;
  element.innerText = originalText.substring(0, 50) + "..."; // Set a default maximum length before truncation
});

//Menu Item Modal
function openEditModal(id, name, description, price) {
  //Populate the fields
  document.getElementById("productName").value = name;
  document.getElementById("productDescription").value = description;
  document.getElementById("productPrice").value = price;

  $("#menuItemModalLabel").text("Edit Menu Item");
  $("#menuItemModal").attr("data-val", id);

  $(".add-menu-item").addClass("d-none");
  $(".delete-menu-item").removeClass("d-none");
  $(".edit-menu-item").removeClass("d-none");

  $(".add-menu").trigger("click");
}

async function saveItem() {
  var productName = document.getElementById("productName").value;
  var productDescription = document.getElementById("productDescription").value;
  var productPrice = document.getElementById("productPrice").value;

  var formData = {
    productName: productName,
    productDescription: productDescription,
    productPrice: productPrice,
  };

  var imageInput = document.getElementById("productImage");
  if (imageInput && imageInput.files.length > 0) {
    const imageData = await convertImageToBase64(imageInput.files[0]);
    formData["productImage"] = imageData;
  }

  if (!validateMenuForm(formData)) {
    var overlay = document.createElement("div");
    overlay.classList.add("toast-overlay");
    document.body.appendChild(overlay);

    toastr.error("Submission failed.", "Error", {
      closeButton: true,
      timeOut: 0,
      extendedTimeOut: 0,
      onCloseClick: function () {
        overlay.remove();
        $(".is-invalid").removeClass("is-invalid");
      },
    });

    return;
  }

  formData["owner_id"] = localStorage.getItem("userId");
  var jsonData = JSON.stringify(formData);
  console.log(jsonData);

  // Send data to server using POST call
  var container_element = $(".app-restaurant-body");

  $.ajax({
    url: "/restaurant/add_menu_item",
    type: "POST",
    data: formData,
    success: function (response) {
      //Toast
      toastr.success("Menu Item added successful!", "Success");
      document.getElementById("menuItemModalCloseBtn").click();
      loadRestaurantHome();
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

async function submitEditItem() {
  var dataToSend = {};

  var productName = document.getElementById("productName").value;
  var productDescription = document.getElementById("productDescription").value;
  var productPrice = document.getElementById("productPrice").value;

  if (productName.length > 1) {
    dataToSend["productName"] = productName;
  }
  if (productDescription.length > 1) {
    dataToSend["productDescription"] = productDescription;
  }
  if (productPrice.length > 1) {
    dataToSend["productPrice"] = productPrice;
  }
  if (productImage.length > 1) {
    const imageData = await convertImageToBase64(imageInput.files[0]);
    dataToSend["productImage"] = imageData;
  }

  dataToSend["productId"] = $("#menuItemModal").attr("data-val");

  dataToSend["owner_id"] = localStorage.getItem("userId");
  dataToSend["action"] = "edit";

  var jsonData = JSON.stringify(dataToSend);
  console.log(jsonData);

  // Send data to server using POST call
  $.ajax({
    url: "/restaurant/edit_menu_item",
    type: "POST",
    data: dataToSend,
    success: function (response) {
      //Toast
      toastr.success("Menu Item edited successfully!", "Success");
      document.getElementById("menuItemModalCloseBtn").click();
      loadRestaurantHome();
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });

  //

  document.getElementById("menuItemModalCloseBtn").click();
  $("#menuItemModalLabel").text("Add Menu Item");

  $(".add-menu-item").removeClass("d-none");
  $(".delete-menu-item").addClass("d-none");
  $(".edit-menu-item").addClass("d-none");
}

function deleteItem() {
  var dataToSend = {};
  dataToSend["productId"] = $("#menuItemModal").attr("data-val");
  dataToSend["owner_id"] = localStorage.getItem("userId");
  dataToSend["action"] = "delete";

  var jsonData = JSON.stringify(dataToSend);
  console.log(jsonData);

  // Send data to server using POST call
  $.ajax({
    url: "/restaurant/edit_menu_item",
    type: "POST",
    data: dataToSend,
    success: function (response) {
      //Toast
      toastr.success("Menu Item deleted successfully!", "Success");
      document.getElementById("menuItemModalCloseBtn").click();
      loadRestaurantHome();
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
  //

  document.getElementById("menuItemModalCloseBtn").click();
  $("#menuItemModalLabel").text("Add Menu Item");

  $(".add-menu-item").removeClass("d-none");
  $(".delete-menu-item").addClass("d-none");
  $(".edit-menu-item").addClass("d-none");
}

function clearMenuModal() {
  document.getElementById("productName").value = "";
  document.getElementById("productImage").value = "";
  document.getElementById("productDescription").value = "";
  document.getElementById("productPrice").value = "";
}

function validateMenuForm(formData) {
  var isValid = true;

  for (var id in formData) {
    if (formData[id].length <= 0) {
      isValid = false;
      document.getElementById(id).classList.add("is-invalid");
    }
  }

  if (!formData.productImage) {
    isValid = false;
    document.getElementById("productImage").classList.add("is-invalid");
  }

  return isValid;
}

function convertImageToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = function (event) {
      resolve(event.target.result);
    };

    reader.onerror = function (error) {
      reject(error);
    };

    reader.readAsDataURL(file);
  });
}

//Menu Item Modal

// Cart stuff
function toggleCartbar() {
  var cartbar = document.getElementById("cartbar");

  if (getCartCount() == 0) {
    $(".cart-item-container").addClass("d-none");
    $(".cart-total-container").addClass("d-none");
    $(".cart-empty-container").removeClass("d-none");
  } else {
    $(".cart-empty-container").addClass("d-none");
    $(".cart-item-container").removeClass("d-none");
    $(".cart-total-container").removeClass("d-none");
  }

  cartbar.classList.toggle("show");
}

function getCartCount() {
  return $(".cart-item").length;
}

function addToCart(restaurant_id, menu_id, menu_name, menu_price, menu_img) {
  //make it visible
  if (getCartCount() == 0) {
    $(".cart-empty-container").addClass("d-none");
    $(".cart-item-container").removeClass("d-none");
    $(".cart-total-container").removeClass("d-none");
  }
  //Create the element
  //Add to the container
  var newItem = $(
    '<div class="cart-item mx-2" data-val=' +
      menu_id +
      ">" +
      '<div class="cart-item-delete-button">' +
      "<button onclick='removeFromCart(this)'>" +
      '<i class="fas fa-times fa-lg" style="color: rgb(136, 23, 23)"></i>' +
      "</button>" +
      "</div>" +
      '<img src="' +
      menu_img +
      '" />' +
      '<div class="d-flex flex-column">' +
      "<span>" +
      menu_name +
      "</span>" +
      '<span class="fw-bold menu-price"> A$' +
      menu_price +
      "</span>" +
      "</div>" +
      "</div>"
  );

  $(".cart-item-container").append(newItem);

  //Calculate the new total
  var current_gross_ttl = parseFloat($(".cart-item-container").attr("total"));
  var items = JSON.parse($(".cart-item-container").attr("items"));
  items.push(menu_id);

  var current_price = parseFloat(menu_price);
  var gross_ttl = current_price + current_gross_ttl;
  var service_tax = (gross_ttl * 0.05).toFixed(2);
  service_tax = parseFloat(service_tax);
  var discount = localStorage.getItem("subscription") == "none" ? 0 : 0.1;

  var net_ttl = (
    gross_ttl +
    service_tax -
    (gross_ttl + service_tax) * discount
  ).toFixed(2);
  $(".cart-item-container").attr("total", gross_ttl.toFixed(2));
  $(".cart-item-container").attr("items", JSON.stringify(items));

  //Update the total UI
  $(".gross-total").html(gross_ttl);
  $(".tax").html(service_tax);
  $(".discount").html(discount == 0 ? "None" : "10%");

  $(".net-total").html(net_ttl + " A$");

  //Update the cart symbol
  if ($("#busy-cart-symbol").hasClass("invisible")) {
    $("#busy-cart-symbol").removeClass("invisible");
  }
}

function removeFromCart(element) {
  //Remove the existing element
  var card = $(element).closest(".cart-item");
  var price = parseFloat(card.find(".menu-price").text().split("$")[1]);

  var menu_id = card.attr("data-val");
  var items = JSON.parse($(".cart-item-container").attr("items"));
  items.splice(items.indexOf(menu_id), 1);
  $(".cart-item-container").attr("items", JSON.stringify(items));

  card.remove();

  //check for 0
  if (items.length == 0) {
    //empty the cart
    $(".cart-item-container").attr("total", 0);
    $(".cart-item-container").addClass("d-none");
    $(".cart-total-container").addClass("d-none");
    $(".cart-empty-container").removeClass("d-none");

    if (!$("#busy-cart-symbol").hasClass("invisible")) {
      $("#busy-cart-symbol").addClass("invisible");
    }

    return;
  }

  //Recalculate the value
  //Calculate the new total
  var current_gross_ttl = parseFloat($(".cart-item-container").attr("total"));

  var current_price = price;
  var gross_ttl = current_gross_ttl - current_price;
  var service_tax = (gross_ttl * 0.05).toFixed(2);
  service_tax = parseFloat(service_tax);
  var discount = localStorage.getItem("subscription") == "none" ? 0 : 0.1;

  var net_ttl = (
    gross_ttl +
    service_tax -
    (gross_ttl + service_tax) * discount
  ).toFixed(2);
  $(".cart-item-container").attr("total", gross_ttl.toFixed(2));

  //Update the total UI
  $(".gross-total").html(gross_ttl);
  $(".tax").html(service_tax);
  $(".discount").html(discount == 0 ? "None" : "10%");

  $(".net-total").html(net_ttl + " A$");
}

function clearCart(toggle) {
  $(".cart-item-container").html("");
  $(".cart-total-container").addClass("d-none");

  //empty the cart
  $(".cart-item-container").attr("total", 0);
  $(".cart-item-container").attr("items", "[]");
  $(".cart-item-container").addClass("d-none");
  $(".cart-total-container").addClass("d-none");
  $(".cart-empty-container").removeClass("d-none");

  if (!$("#busy-cart-symbol").hasClass("invisible")) {
    $("#busy-cart-symbol").addClass("invisible");
  }

  if (toggle) {
    toggleCartbar();
  }
}

function placeOrder() {
  //Get all menu_item_ids
  var items = $(".cart-item-container").attr("items");
  var restaurant_id = $(".restaurant-cover-container").attr("restaurant_id");
  var user_id = localStorage.getItem("userId");

  $.ajax({
    url: "/restaurant/create_order",
    type: "POST",
    data: {
      restaurant_id: restaurant_id,
      customer_email: user_id,
      menu_item_ids: items,
    },
    success: function (response) {
      if (response.order_id) {
        toastr.success("Order placed successfully!", "Success");
        clearCart(true);
      }
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}
// Cart stuf

//logout stuff
function logout() {
  user_type = localStorage.getItem("user");
  localStorage.clear();

  window.location.pathname = "/index";
//   location.reload();
}

//Order Pages
function loadCustomerOrdersPage() {
  var container_element = $(".app-orders-container");
  $.ajax({
    url: "/restaurant/customer_loadOrders",
    type: "POST",
    data: {
      email: localStorage.getItem("userId"),
    },
    success: function (response) {
      cleanAllContainer_customer();
      container_element.html(response);
      toggleSidebar();
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

function loadRestaurantOrdersPage() {
  var container_element = $(".app-orders-container");
  $.ajax({
    url: "/restaurant/restaurant_loadOrders",
    type: "POST",
    data: {
      email: localStorage.getItem("userId"),
    },
    success: function (response) {
      cleanAllContainer_customer();
      container_element.html(response);
      toggleSidebar();
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

function fetchCustomerOrderDetails(order_id, trigger) {
  $.ajax({
    url: "/restaurant/fetch_order_details",
    type: "POST",
    data: {
      order_id: order_id,
    },
    success: function (response) {
      data = response;
      //Populate
      $("#orderCustomerModal .order_restaurant_name").html(data.restaurant);
      $("#orderCustomerModal .order_price").html(data.total);
      $("#orderCustomerModal .order_status").html(data.status);

      $("#orderCustomerModal .order_menu").html("");

      $("#orderModalLabel").attr("order-id", data.id);

      menu_obj = data.menu;
      for (var i = 0; i < menu_obj.length; i++) {
        var newLi = $("<li>");
        newLi.html(menu_obj[i].name);
        $("#orderCustomerModal .order_menu").append(newLi);
      }

      if (data.courier) {
        $("#orderCustomerModal .order_delivery_name").html(data.courier.name);
        $("#orderCustomerModal .order_delivery_contact").html(
          data.courier.mobile
        );

        $("#orderCustomerModal .order_delivery_details").removeClass("d-none");
      } else {
        if (
          !$("#orderCustomerModal .order_delivery_details").hasClass("d-none")
        ) {
          $("#orderCustomerModal .order_delivery_details").addClass("d-none");
        }
      }

    if(data.status == "delivered" && data.feedback == ""){
        $("#orderCustomerModal .feedback-div").removeClass("d-none");
    }else{
        if(!$("#orderCustomerModal .feedback").hasClass("d-none")){
            $("#orderCustomerModal .feedback-div").addClass("d-none");
        }
    }

      //Trigger
      trigger.click();
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
}

function fetchRestaurantOrderDetails(order_id, trigger) {
    $.ajax({
      url: "/restaurant/fetch_order_details",
      type: "POST",
      data: {
        order_id: order_id,
      },
      success: function (response) {
        data = response;
        //Populate
        $("#orderRestaurantModal .order_restaurant_name").html("Items");
        $("#orderRestaurantModal .order_price").html(data.total);
        $("#orderRestaurantModal .order_status").html(data.status);
  
        $("#orderRestaurantModal .order_menu").html("");
  
        $("#orderRestaurantModal").attr("order-id", data.id);
  
        menu_obj = data.menu;
        for (var i = 0; i < menu_obj.length; i++) {
          var newLi = $("<li>");
          newLi.html(menu_obj[i].name);
          $("#orderRestaurantModal .order_menu").append(newLi);
        }
  
        if (data.courier) {
          $("#orderRestaurantModal .order_delivery_name").html(data.courier.name);
          $("#orderRestaurantModal .order_delivery_contact").html(
            data.courier.mobile
          );
  
          $("#orderRestaurantModal .order_delivery_details").removeClass("d-none");
        } else {
          if (
            !$("#orderRestaurantModal .order_delivery_details").hasClass("d-none")
          ) {
            $("#orderRestaurantModal .order_delivery_details").addClass("d-none");
          }
        }

        //Reset previous buttons
        if (
            !$("#orderRestaurantModal .accept-order").hasClass("d-none")
          ) {
            $("#orderRestaurantModal .accept-order").addClass("d-none");
          }

          if (
            !$("#orderRestaurantModal .reject-order").hasClass("d-none")
          ) {
            $("#orderRestaurantModal .reject-order").addClass("d-none");
          }

          if (
            !$("#orderRestaurantModal .feedback-div").hasClass("d-none")
          ) {
            $("#orderRestaurantModal .feedback-div").addClass("d-none");
          }

          if (
            !$("#orderRestaurantModal .delivery-div").hasClass("d-none")
          ) {
            $("#orderRestaurantModal .delivery-div").addClass("d-none");
          }

        //Based on Status
        if(data.status == "placed"){
            $("#orderRestaurantModal .accept-order").removeClass("d-none");
            $("#orderRestaurantModal .reject-order").removeClass("d-none");
        }else if(data.status == "courier_accepted"){
            $("#orderRestaurantModal .update-order").html("Ready to dispatch"); //ready_to_dispatch
            $("#orderRestaurantModal .update-order").attr("status", "ready_to_dispatch");
            $("#orderRestaurantModal .update-order").removeClass("d-none");
        }else if(data.status == "delivered" && data.feedback.length > 0){
            $("#orderRestaurantModal .feedback-p").html(data.feedback);
            $("#orderRestaurantModal .feedback-div").removeClass("d-none");
        }
  
        //Trigger
        trigger.click();
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      },
    });
  }

  function fetchCourierOrderDetails(order_id, trigger) {
    $.ajax({
      url: "/restaurant/fetch_order_details",
      type: "POST",
      data: {
        order_id: order_id,
      },
      success: function (response) {
        data = response;
        //Populate
        $("#orderCourierModal .order_restaurant_name").html(data.restaurant);
        $("#orderCourierModal .order_price").html(data.total);
        $("#orderCourierModal .order_status").html(data.status);
  
        $("#orderCourierModal .order_menu").html("");
  
        $("#orderCourierModal").attr("order-id", data.id);
  
        menu_obj = data.menu;
        for (var i = 0; i < menu_obj.length; i++) {
          var newLi = $("<li>");
          newLi.html(menu_obj[i].name);
          $("#orderCourierModal .order_menu").append(newLi);
        }

        //Reset previous buttons
        if (
            !$("#orderCourierModal .accept-order").hasClass("d-none")
          ) {
            $("#orderCourierModal .accept-order").addClass("d-none");
          }

          if (
            !$("#orderCourierModal .reject-order").hasClass("d-none")
          ) {
            $("#orderCourierModal .reject-order").addClass("d-none");
          }

          if (
            !$("#orderCourierModal .update-order").hasClass("d-none")
          ) {
            $("#orderCourierModal .update-order").addClass("d-none");
          }

          if (
            !$("#orderCourierModal .feedback-div").hasClass("d-none")
          ) {
            $("#orderCourierModal .feedback-div").addClass("d-none");
          }
  
        //Based on Status
        if(data.status == "waiting_for_courier"){
            $("#orderCourierModal .accept-order").removeClass("d-none");
            $("#orderCourierModal .reject-order").removeClass("d-none");
        }else if(data.status == "ready_to_dispatch" ){
            $("#orderCourierModal .update-order").html("Picked Up"); 
            $("#orderCourierModal .update-order").attr("status", "picked_up");
            $("#orderCourierModal .update-order").removeClass("d-none");
        }else if(data.status == "picked_up"){
            $("#orderCourierModal .update-order").html("Delivered"); 
            $("#orderCourierModal .update-order").attr("status", "delivered");
            $("#orderCourierModal .update-order").removeClass("d-none");
        }else if(data.status == "delivered" && data.feedback.length > 0){
            $("#orderCourierModal .feedback-p").html(data.feedback)
            $("#orderCourierModal .feedback-div").removeClass("d-none");
        }
  
        //Trigger
        trigger.click();
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      },
    });
  }

  function acceptRestaurantOrder(){
    var order_id = $("#orderRestaurantModal").attr("order-id");
    var owner_id = localStorage.getItem("userId");
    $.ajax({
        url: "/restaurant/status_update",
        type: "POST",
        data: {
          "order_id": order_id,
          "status":"accepted",
          "user_id":owner_id
        },
        success: function (response) {
          data = response;

          loadRestaurantOrdersPage();

        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }

  function acceptCourierOrder(){
    var order_id = $("#orderCourierModal").attr("order-id");
    var email = localStorage.getItem("userId");
    $.ajax({
        url: "/restaurant/status_update",
        type: "POST",
        data: {
          "order_id": order_id,
          "status":"courier_accepted",
          "user_id":email
        },
        success: function (response) {
          data = response;
          location.reload();

        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }

  function rejectRestaurantOrder(order_id){
    var order_id = $("#orderRestaurantModal").attr("order-id");
    var owner_id = localStorage.getItem("userId");
    $.ajax({
        url: "/restaurant/status_update",
        type: "POST",
        data: {
          "order_id": order_id,
          "status":"rejected",
          "user_id":owner_id
        },
        success: function (response) {
          data = response;

          loadRestaurantOrdersPage();

        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }

  function rejectCourierOrder(){
    var order_id = $("#orderCourierModal").attr("order-id");
    var email = localStorage.getItem("userId");
    $.ajax({
        url: "/restaurant/status_update",
        type: "POST",
        data: {
          "order_id": order_id,
          "status":"courier_rejected",
          "user_id":email
        },
        success: function (response) {
          data = response;
          location.reload();

        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }

  function updateRestaurantOrder(status){
    var order_id = $("#orderRestaurantModal").attr("order-id");
    var owner_id = localStorage.getItem("userId");

    var status = $("#orderRestaurantModal .update-order").attr("status");
    $.ajax({
        url: "/restaurant/status_update",
        type: "POST",
        data: {
          "order_id": order_id,
          "status":status,
          "user_id":owner_id
        },
        success: function (response) {
          data = response;

          loadRestaurantOrdersPage();

        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }

  function updateCourierOrder(status){
    var order_id = $("#orderCourierModal").attr("order-id");
    var email_id = localStorage.getItem("userId");

    var status = $("#orderCourierModal .update-order").attr("status");
    $.ajax({
        url: "/restaurant/status_update",
        type: "POST",
        data: {
          "order_id": order_id,
          "status":status,
          "user_id":email_id
        },
        success: function (response) {
          data = response;
          location.reload();
        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }

  function submitFeedback(){
    var order_id = $("#orderModalLabel").attr("order-id");
    var res_rating = $("#restaurantRating").val();
    var courier_rating =  $("#deliveryRating").val();
    var feedback = $("#feedbackText").val();

    $.ajax({
        url: "/restaurant/provide_feedback_to_order",
        type: "POST",
        data: {
          "order_id": order_id,
          "res_rating":res_rating,
          "courier_rating":courier_rating,
          "feedback":feedback
        },
        success: function (response) {
            toastr.success("ThankYou! for your feedback..", "Success");
        },
          error: function (xhr, status, error) {
            console.error(xhr.responseText);
          },
        });
  }