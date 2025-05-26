$(document).ready(function () {
  $(".heading").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "bounceIn",
    },
    out: {
      effect: "bounceOut",
    },
  });

  // Siri Wave

  var siriWave = new SiriWave({
    container: document.getElementById("siri-container"),
    width: 640,
    height: 200,
    style: "ios9",
    amplitude: "1",
    speed: "0.30",
    autoStart: true,
  });

  // Siri message animation

  $(".message").textillate({
    loop: true,
    sync: true,
    in: {
      effect: "fadeInUp",
      sync: true,
    },
    out: {
      effect: "fadeOutUp",
      sync: true,
    },
  });

  // handling Mic button click event to show the siri wave

  $("#micButton").click(function (e) {
    e.preventDefault();
    eel.playStartSound();
    $(".oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.commands()()
  });


  // function to add the shortcut key for JARVIS activation and hotword detection
  
  function shortcutKey(e){
    // testing for the shortcut key combination of win+j
    //meta key refers to the windows key 
    if(e.key === 'j' && e.metaKey){
      e.preventDefault();
    eel.playStartSound();
    $(".oval").attr("hidden", true);
    $("#SiriWave").attr("hidden", false);
    eel.commands()()
    }
  }

  document.addEventListener('keydown', shortcutKey, false) // the false in the end means that the event will be captured in the bubbling phase i.e. when the event travels from the target back up to the root

  // function to send message to JARVIS using chat box
  
  function chatWithJARVIS(message){
    if(message.trim()!=""){
      $(".oval").attr("hidden", true); // hide the hood 
      $("#SiriWave").attr("hidden", false); //display the Siri wave
      eel.commands(message) // take the command and give it to the function to process it 
      $(".inputBox").val("") //clear the chat box after the query has been sent for processing to recieve the next query 
      $("#micButton").attr("hidden", false);   // show the mic button
      $("#sendButton").attr("hidden", true); // hide the send button
    }
  }

  function showSendButton(message){
    if(message.trim()==""){
      $("#micButton").attr("hidden", false);
      $("#sendButton").attr("hidden", true);
    }
    else{
      $("#micButton").attr("hidden", true);
      $("#sendButton").attr("hidden", false);
    }
  }

  // function to check for any queries in the chat box

  $(".inputBox").keyup(function (e) { 
    let message = $(".inputBox").val() //get the message written in the chat box
    showSendButton(message) //pass this to the function to show the send button    
  });

  // event handler to check for the click of the send button to send the query for processing

  $("#sendButton").click(function (e) { 
    e.preventDefault();
    let message =  $(".inputBox").val();   // get the message
    chatWithJARVIS(message) //send the query for processing
  });

  $(".inputBox").keydown(function (e) {     
    if(e.key=="Enter"){
      e.preventDefault() // adding this line outside of the if condition will prevent all actions including typing anything in the input box 
      let message = $(".inputBox").val(); //get the message
      chatWithJARVIS(message) //send it for processing
    }    
  });

});
