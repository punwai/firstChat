$(function() {
  var ws_path = 'ws' + '://' + window.location.host + "/chat/";
  console.log("Connecting to " + ws_path);
  socket = new ReconnectingWebSocket(ws_path);

  socket.onopen = function () {
        console.log("Connected to chat socket");
    };
  socket.onclose = function () {
      console.log("Disconnected from chat socket");
  };


  // functions
  inRoom = function(roomId){
    return $("#room-"+roomId).length>0;
  };

  socket.onmessage = function(message) {
    console.log("Got websocket message " + message.data);
    var data = JSON.parse(message.data);

    if(data.error){
      alert(data.error);
      return;
    }

    if(data.join){
      console.log("joining room " + data.join);
      var roomdiv = $(
        "<div class='room' id='room-" + data.join + "'>"+
        "<h2>" + data.display_name + "</h2>" +
        "<div class='messages'></div>" +
        "<form>" +
        "<input id='chattext' type='text'>" +
        "<input id='chatsub' placeholder='send!' type='submit'/>" +
        "</form>" +
        "</div>"
      );
      $("#chats").append(roomdiv);
      roomdiv.find("#chatsub").on("click", function () {
        socket.send(JSON.stringify({
            "command": "send",
            "room": data.join,
            "message": roomdiv.find("#chattext").val()
        }));
        roomdiv.find("#chattext").val("");
        return false;
      });
    } else if (data.leave) {
      console.log("Leaving room " + data.leave);
      $("#room-"+data.leave).remove();
    } else if (data.message){
      var msgdiv = $("#room-" + data.room + " .messages");
      ok_msg = "<div class='message'>" +
              "<p>" +
              "<span class='username'>" + data.username + "</span>" +
              ": " +
              "<span class='body'>" + data.message + "</span>" +
              "</p>" +
              "</div>";
      msgdiv.append(ok_msg);
      msgdiv.scrollTop(msgdiv.prop("scrollHeight"))
    } else {
      console.log("Cannot handle message!");
    }

  }


  $("li.room-link").click(function () {
      roomId = $(this).attr("data-room-id");
      if (inRoom(roomId)) {
          // Leave room
          $(this).removeClass("joined");
          socket.send(JSON.stringify({
              "command": "leave",  // determines which handler will be used (see chat/routing.py)
              "room": roomId
          }));
      } else {
          // Join room
          $(this).addClass("joined");
          socket.send(JSON.stringify({
              "command": "join",
              "room": roomId
          }));
      }
  });
});
