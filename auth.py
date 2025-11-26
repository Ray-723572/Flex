{% load static %}
<style>
  
    @import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');
    
    * {
        box-sizing: border-box;
    }
    
    body {
        background: #1c496c;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        font-family: 'Montserrat', sans-serif;
        height: 100vh;
        margin: -20px 0 50px;
    }
    
    h1 {
        font-weight: bold;
        margin: 0;
    }
    
    h2 {
        text-align: center;
    }
    
    p {
        font-size: 14px;
        font-weight: 100;
        line-height: 20px;
        letter-spacing: 0.5px;
        margin: 20px 0 30px;
    }
    
    span {
        font-size: 12px;
    }
    
    a {
        color: #333;
        font-size: 14px;
        text-decoration: none;
        margin: 15px 0;
    }
    
    button {
        border-radius: 20px;
        border: 1px solid #6495ED;
        background-color: #6495ED;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: bold;
        padding: 12px 45px;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: transform 80ms ease-in;
    }
    
    button:active {
        transform: scale(0.95);
    }
    
    button:focus {
        outline: none;
    }
    
    button.ghost {
        background-color: transparent;
        border-color: #FFFFFF;
    }
    
    form {
        background-color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0 50px;
        height: 100%;
        text-align: center;
    }
    
    input {
        background-color: #eee;
        border: none;
        padding: 12px 15px;
        margin: 8px 0;
        width: 100%;
    }
    
    .container {
        background-color: #fff;
        border-radius: 10px;
          box-shadow: 0 14px 28px rgba(0,0,0,0.25), 
                0 10px 10px rgba(0,0,0,0.22);
        position: relative;
        overflow: hidden;
        width: 768px;
        max-width: 100%;
        min-height: 480px;
    }
    
    .form-container {
        position: absolute;
        top: 0;
        height: 100%;
        transition: all 0.6s ease-in-out;
    }
    
    .sign-in-container {
        left: 0;
        width: 50%;
        z-index: 2;
    }
    
    .container.right-panel-active .sign-in-container {
        transform: translateX(100%);
    }
    
    .sign-up-container {
        left: 0;
        width: 50%;
        opacity: 0;
        z-index: 1;
    }
    
    .container.right-panel-active .sign-up-container {
        transform: translateX(100%);
        opacity: 1;
        z-index: 5;
        animation: show 0.6s;
    }
    
    @keyframes show {
        0%, 49.99% {
            opacity: 0;
            z-index: 1;
        }
        
        50%, 100% {
            opacity: 1;
            z-index: 5;
        }
    }
    
    .overlay-container {
        position: absolute;
        top: 0;
        left: 50%;
        width: 50%;
        height: 100%;
        overflow: hidden;
        transition: transform 0.6s ease-in-out;
        z-index: 100;
    }
    
    .container.right-panel-active .overlay-container{
        transform: translateX(-100%);
    }
    
    .overlay {
        background: #6495ED;
        background: -webkit-linear-gradient(to right, #6495ED, #6495ED);
        background: linear-gradient(to right, #6495ED, #6495ED);
        background-repeat: no-repeat;
        background-size: cover;
        background-position: 0 0;
        color: #FFFFFF;
        position: relative;
        left: -100%;
        height: 100%;
        width: 200%;
          transform: translateX(0);
        transition: transform 0.6s ease-in-out;
    }
    
    .container.right-panel-active .overlay {
          transform: translateX(50%);
    }
    
    .overlay-panel {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0 40px;
        text-align: center;
        top: 0;
        height: 100%;
        width: 50%;
        transform: translateX(0);
        transition: transform 0.6s ease-in-out;
    }
    
    .overlay-left {
        transform: translateX(-20%);
    }
    
    .container.right-panel-active .overlay-left {
        transform: translateX(0);
    }
    
    .overlay-right {
        right: 0;
        transform: translateX(0);
    }
    
    .container.right-panel-active .overlay-right {
        transform: translateX(20%);
    }
    
    .social-container {
        margin: 20px 0;
    }
    
    .social-container a {
        border: 1px solid #DDDDDD;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin: 0 5px;
        height: 40px;
        width: 40px;
    }
    
    footer {
        background-color: #222;
        color: #fff;
        font-size: 14px;
        bottom: 0;
        position: fixed;
        left: 0;
        right: 0;
        text-align: center;
        z-index: 999;
    }
    
    footer p {
        margin: 10px 0;
    }
    
    footer i {
        color: red;
    }
    
    footer a {
        color: #3c97bf;
        text-decoration: none;
    }

    .errorDisplay {
        color: red;
    }
    .modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

/* The Close Button */

</style>

{% url 'update_license_date' as updateLicense %}

<div class="container" id="container">
    <div class="form-container sign-up-container">
        
        <img src="{% static 'styles/assets/images/logo11.jpg' %}" alt="azure" height="70px" weight="100px" style="margin-bottom: -8rem;margin-top:5rem;margin-left:4rem;" />
        <form action="#">
                <!-- <h1>Create Account</h1> -->
                <!-- <div class="social-container">
                    <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                    <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
                </div> -->
                <!-- <span>or use your email for registration</span> -->
                <input type="text" placeholder="Name" />
                <input type="email" placeholder="Email" />
                <input type="password" placeholder="Password" />
                <button>Sign Up</button>
        </form>
    </div>
    <div class="form-container sign-in-container">
        <img src="{% static 'styles/assets/images/ce.jpg' %}" alt="azure"  style="margin-bottom: -8rem;margin-top:5rem;margin-left:2rem;"   />
        <form method="post">
            <!-- <h1>Sign in</h1> -->
            <!-- <div class="social-container">
                    <a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
                    <a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
            </div> -->
            <!-- <span>use your account</span> -->
           
            <input type="text" placeholder="Username" formControlName="username" name="username" required/>
            <input type="password" placeholder="Password"  name="password" formControlName="password" placeholder="Enter password" required/>
            
            {% comment %} {% if Lerror%}
            <div class="errorDisplay">
                License is exipre/invalid please update the license.
            </div>
            <button>Update License</button>
            <a href="{{ updateLicense }}" class="card">
                <h3 class="title">update License</h3>
      </a>

            {% elif error%}
            <div class="errorDisplay">
                Username or password is not valid.111
            </div>
            {% endif %}
            <a href="#">Forgot your password?</a>
            <button>Sign In</button> {% endcomment %}
 <a href="#">Forgot your password?</a>
            <button>Sign In</button>
            
            {% if Lerror%}
            <div class="errorDisplay">
                License is exipre/invalid please update the license.
            </div>
            
           <button> <a href="{{ updateLicense }}" style="color: white;" >
               update License
            </a>
            </button>

            {% elif error%}
            <div class="errorDisplay">
                Username or password is not valid.222
            </div>
            {% endif %}
           
        </form>
       
    </div>
    <div class="overlay-container">
        <div class="overlay">
            <div class="overlay-panel overlay-left">
                
                <h2>Unify Your Multi-Cloud Management</h2>
                <p>To keep connected with us please login with your personal info</p>
                <button class="ghost" id="signIn">Sign In</button>
            </div>
            <div class="overlay-panel overlay-right">
                <!-- <h1>Hello, Friend!</h1> -->
                <img src="{% static 'styles/assets/images/LTIM.NS_BIG.D-47434682.png' %}" alt="lti" height="50rem" weight="10rem"/><br>
                <h2>Unify Your Multi-Cloud Management</h2>
                <p>Control everything from one place.
Maximize efficiency, reduce complexity, and accelerate productivity with seamless cloud operations.</p>
                {% comment %} <button class="ghost" id="signUp">Sign Up</button> {% endcomment %}
            </div>
        </div>
    </div>
</div>

{% comment %} <div>
    <h1>ADD sign in</h1>
    <a href="{% url 'django_auth_adfs:login' %}">Login</a>
    <a href="{% url 'django_auth_adfs:login-no-sso' %}">Login (no SSO)</a>
    <!--<a href="{% url 'django_auth_adfs:logout' %}?next=/">AAD Logout</a>-->
</div> {% endcomment %}
<!-- 
<footer>
    <p>
        Created with <i class="fa fa-heart"></i> by
        <a target="_blank" href="https://florin-pop.com">Florin Pop</a>
        - Read how I created this and how you can join the challenge
        <a target="_blank" href="https://www.florin-pop.com/blog/2019/03/double-slider-sign-in-up-form/">here</a>.
    </p>
</footer> 
-->
<!-- 
<footer>
    <p>
        Created with <i class="fa fa-heart"></i> by
        <a target="_blank" href="https://florin-pop.com">Florin Pop</a>
            - Read how I created this and how you can join the challenge
        <a target="_blank" href="https://www.florin-pop.com/blog/2019/03/double-slider-sign-in-up-form/">here</a>.
    </p>
</footer>
-->
<script>
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');
    
    //signUpButton.addEventListener('click', () => { container.classList.add("right-panel-active");});
    
    //signInButton.addEventListener('click', () => { container.classList.remove("right-panel-active"); });
    // Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
</script>
