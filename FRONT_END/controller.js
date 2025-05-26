// This file has all the functions that are called externally by Python using the eel module

$(document).ready(function () {

    eel.initialize()() // call the initialize function in the begining from the back end

    // Function to display the spoken text
    eel.expose(displayMessage);
    function displayMessage(string) {
        $(".message li:first").text(string);
        $(".message").textillate('start');
    }

    // Function to display back the hood after the required function is done
    eel.expose(displayHood);
    function displayHood() {
        $(".oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
    }

    // Handling escape situation in case of some malfunction or infinite loop issue
    $(document).keydown(function (e) {
        if (e.key === "Escape" || e.keyCode === 27) {
            displayHood();
        }
    });

    // -------------------------------------------------- Section for Chat History -------------------------------------------------- 

    // Function for the sender's message 
    eel.expose(sendersMessage)
    function sendersMessage(message) {
        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    eel.expose(recieversMessage)
    function recieversMessage(message) {

        var chatBox = document.getElementById("chat-canvas-body");
        if (message.trim() !== "") {
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Scroll to the bottom of the chat box
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }


    // Logic for face authentication start

    
    // Hide Loader and display Face Auth animation
    eel.expose(hideLoader)
    function hideLoader() {

        $("#Loader").attr("hidden", true); // hide the spinning blue circles part
        $("#FaceAuth").attr("hidden", false); // show the animation for face authentication

    }
    // Hide Face authentication animation and display successful authentication animation
    eel.expose(hideFaceAuth)
    function hideFaceAuth() {

        $("#FaceAuth").attr("hidden", true); // This is the face scan animation
        $("#FaceAuthSuccess").attr("hidden", false); // This is the success animation

    }
    // Hide success and display 
    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {

        $("#FaceAuthSuccess").attr("hidden", true); // Hide the sucessful authentication
        $("#HelloGreet").attr("hidden", false); // Show the hello hand wave animation

    }


    // Hide Start Page and display blob
    eel.expose(hideStart)
    function hideStart() {

        $("#Start").attr("hidden", true); // hide the whole face authentiation part after the check is over

        setTimeout(function () {
            $(".oval").addClass("animate__animated animate__zoomIn"); // add the fade in animation to the blob after 1 second of the authentication

        }, 1000)
        setTimeout(function () {
            $(".oval").attr("hidden", false); // Display the maine JARVIS hood after 1 second
        }, 1000)
    }

    // Logic for face authentication end


});
