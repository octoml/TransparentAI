const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const port = process.env.PORT || 3000;
const taiapi = process.env.TAI_API_HOST || "127.0.0.1" ;
const axios = require('axios').default;

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  io.emit('chat message', "Welcome to chat! We have 3 bots for you to chat with, Huggy, Octo, and Oni(onnx). Try it out with 'Huggy: I was once walking down the street and'")
  socket.on('chat message', msg => {
    console.log(msg);
    io.emit('chat message', msg);
    if (msg.startsWith("Huggy")) {
        modelUrl = "http://" + taiapi + ":9000/engines/hf-gpt-2/completions"
        getPredictedText(io, modelUrl, "Huggy", msg.slice(5).trim())
    }
    if (msg.startsWith("Octo")) {
        modelUrl = "http://" + taiapi + ":9000/engines/octo-onnx-gpt-2/completions"
        getPredictedText(io, modelUrl, "Octo", msg.slice(5).trim())
    }
    if (msg.startsWith("Oni")) {
        modelUrl = "http://" + taiapi + ":9000/engines/onnx-gpt-2/completions"
        getPredictedText(io, modelUrl, "Oni", msg.slice(4).trim())
    }
  });
});


function getPredictedText(io, modelUrl, name, prompt) {
  axios.post(modelUrl, {
      prompt: prompt
    })
    .then(function(response) {
      // Idk why these aren't unified
      text = response.data.response[0].generated_text
      if (text == undefined) {
          text = response.data.response
      }
      console.log(text, response.headers['x-process-time']);
      text += ` (in ${parseFloat(response.headers['x-process-time']).toFixed(4)}s)`

      io.emit('chat message', name + " has generated" + text )
    })
    .catch(function (error) {
      console.log(error);
    });
}


http.listen(port, () => {
  console.log(`Socket.IO server running at http://localhost:${port}/`);
});
