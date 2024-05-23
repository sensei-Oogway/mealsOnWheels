function registrationAccSelect(element) {
  var value = element.getAttribute("data-value");
  console.log(value);

  $(".type-1").addClass("d-none");
  $(".type-2").addClass("d-none");
  $(".type-3").addClass("d-none");

  if (value == "customer") {
    $(".type-1").removeClass("d-none");
    $(".registration-submit").attr("user_type", "customer");
  } else if (value == "restaurant") {
    $(".type-2").removeClass("d-none");
    $(".registration-submit").attr("user_type", "owner");
  } else if (value == "delivery") {
    $(".type-3").removeClass("d-none");
    $(".registration-submit").attr("user_type", "courier");
  }

  $(".stage-one").addClass("d-none");
  $(".stage-two").removeClass("d-none");
}
function openRegistrationForm() {
  $(".login-container").addClass("d-none");
  $(".register-container").removeClass("d-none");
}

function submitLoginForm() {
  var email = $("#username").val();
  var password = $("#pwd").val();

  if (email.length <= 0 || password.length <= 0) {
    toastr.error(
      "Login failed.\n<div>Please try again with proper values.</div>",
      "Error",
      {
        closeButton: true,
        timeOut: 2000,
      }
    );
  } else {
    console.log(email + " " + password);

    var jsonData = JSON.stringify({ email: email, password: password });
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonData,
    })
      .then((response) => {
        if (!response.ok) {
          toastr.error("Login failed.<div>Try again.</div>", "Error", {
            closeButton: true,
            timeOut: 3000,
          });
          return;
        }
        return response.json();
      })
      .then((data) => {
        if (data?.status == 200) {
          var user_type = data.type;
          localStorage.setItem("userType", user_type);
          localStorage.setItem("userId", JSON.parse(data.user)[0].pk);
          localStorage.setItem(
            "subscription",
            JSON.parse(data.user)[0].fields?.subscription
          );

          if (user_type == "customer") {
            var newPageUrl = "restaurant/customer_home";
            window.location.href = newPageUrl;
          } else if (user_type == "owner") {
            $.ajax({
              url: "restaurant/restaurant_home",
              type: "POST",
              data: {
                id: localStorage.getItem("userId"),
              },
              success: function (response) {
                document.open();
                document.write(response);
                document.close();
              },
              error: function (xhr, status, error) {
                console.error(xhr.responseText);
              },
            });
          } else if(user_type == "courier"){
            $.ajax({
              url: "restaurant/courier_home",
              type: "POST",
              data: {
                email: localStorage.getItem("userId"),
              },
              success: function (response) {
                document.open();
                document.write(response);
                document.close();
              },
              error: function (xhr, status, error) {
                console.error(xhr.responseText);
              },
            });
          }
        } else {
          toastr.error(
            "Login failed.<div>Try again.</div>" + data.message,
            "Error",
            {
              closeButton: true,
              timeOut: 3000,
            }
          );
        }
      })
      .catch((error) => {
        toastr.error("Login failed, retry!", "Error", {
          closeButton: true,
          timeOut: 2000,
        });
      });
  }
}

async function submitRegistrationForm(element) {
  var formData = {};

  var form = document.getElementById("registration-form");
  var formElements = form.querySelectorAll(
    ".form-control:not(.d-none), .form-select:not(.d-none)"
  );

  formElements.forEach(function (element) {
    if (!element.closest("div").classList.contains("d-none")) {
      var id = element.id;
      var value = element.value;
      formData[id] = value;
    }
  });

  if (!validateForm(formData)) {
    console.log("Form validation failed");
    var overlay = document.createElement("div");
    overlay.classList.add("toast-overlay");
    document.body.appendChild(overlay);

    toastr.error(
      "Form registration failed. Please try again with proper values. \nNote: Password should be minimum 8 characters",
      "Error",
      {
        closeButton: true,
        timeOut: 0,
        extendedTimeOut: 0,
        onCloseClick: function () {
          overlay.remove();
          $(".is-invalid").removeClass("is-invalid");
        },
      }
    );

    return;
  }

  var imageInput = document.getElementById("image");
  if (imageInput && imageInput.files.length > 0) {
    const imageData = await convertImageToBase64(imageInput.files[0]);
    formData["image"] = imageData;
  }

  var user_type = $(".registration-submit").attr("user_type");
  formData["user_type"] = user_type;

  var jsonData = JSON.stringify(formData);
  console.log(jsonData);

  // Send data to server using POST call
  fetch("/register_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      // Add any additional headers if needed
    },
    body: jsonData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Handle server response
      if (data?.status == 200) {
        toastr.success("Registration successful! Proceeding to login page...", "Success");
        var overlay = document.createElement("div");
        overlay.classList.add("toast-overlay");
        document.body.appendChild(overlay);

        setTimeout(() => Window.location="/index", 3000);
        location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
 
function validateForm(formData) {
  var isValid = true;

  for (var id in formData) {
    switch (id) {
      case "email":
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData[id])) {
          isValid = false;
          document.getElementById(id).classList.add("is-invalid");
        } else {
          document.getElementById(id).classList.remove("is-invalid");
        }
        break;
      case "password":
        if (formData[id].length < 8) {
          isValid = false;
          document.getElementById(id).classList.add("is-invalid");
        } else {
          document.getElementById(id).classList.remove("is-invalid");
        }
        break;
      default:
        if (formData[id].length <= 0) {
          isValid = false;
          document.getElementById(id).classList.add("is-invalid");
          break;
        }
    }
  }

  return isValid; // TO DO CHANGE IT BACK to isValid
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

function checkForPreviousUsage() {
  var userData = localStorage.getItem("userId");
  if (userData) {
    var userType = localStorage.getItem("userType");

    if (userType == "customer") {
      var currentUrl = window.location.href;
      var newPageUrl = "restaurant/customer_home";
      window.location.href = newPageUrl;
    } else if (userType == "owner") {
      $.ajax({
        url: "restaurant/restaurant_home",
        type: "POST",
        data: {
          id: localStorage.getItem("userId"),
        },
        success: function (response) {
          document.open();
          document.write(response);
          document.close();
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
        },
      });
    } else if(userType == "courier"){
      $.ajax({
        url: "restaurant/courier_home",
        type: "POST",
        data: {
          email: localStorage.getItem("userId"),
        },
        success: function (response) {
          document.open();
          document.write(response);
          document.close();
        },
        error: function (xhr, status, error) {
          console.error(xhr.responseText);
        },
      });
    }
}
}